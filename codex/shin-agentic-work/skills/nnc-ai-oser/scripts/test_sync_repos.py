"""Network-free regression tests; local URLs are injected below the CLI validator."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import sync_repos as sync


def run_git(cwd, *args):
    completed = subprocess.run(["git", *args], cwd=cwd, capture_output=True, check=True)
    return completed.stdout.decode().strip()


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.source = self.root / "source"
        self.source.mkdir()
        run_git(self.source, "init", "-b", "main")
        run_git(self.source, "config", "user.email", "fixture@example.invalid")
        run_git(self.source, "config", "user.name", "Fixture")
        (self.source / "data.csv").write_text("id\n1\n")
        run_git(self.source, "add", ".")
        run_git(self.source, "commit", "-m", "initial")
        self.remote = self.root / "remote.git"
        run_git(self.root, "clone", "--bare", str(self.source), str(self.remote))
        run_git(self.source, "remote", "add", "origin", str(self.remote))
        self.repo = dict(name="project", url=str(self.remote), branch="main")
        self.target = self.workspace / "project"

    def clone(self):
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["status"], "synced", result)
        run_git(self.target, "config", "user.email", "fixture@example.invalid")
        run_git(self.target, "config", "user.name", "Fixture")
        return result

    def remote_commit(self):
        (self.source / "extra.json").write_text('{"value": 1}\n')
        run_git(self.source, "add", ".")
        run_git(self.source, "commit", "-m", "remote advance")
        run_git(self.source, "push", "origin", "main")

    def test_missing_dry_run_does_not_create_directory(self):
        result = sync.sync_repository(self.repo, self.workspace, False)
        self.assertEqual(result["status"], "missing_dry_run")
        self.assertFalse(self.target.exists())

    def test_clone_and_fast_forward(self):
        first = self.clone()
        self.assertEqual(first["tracked_file_extension_counts"], {".csv": 1})
        self.remote_commit()
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["status"], "synced", result)
        self.assertIn("fast_forwarded", result["actions"])
        self.assertEqual(result["sha"], run_git(self.source, "rev-parse", "HEAD"))
        self.assertEqual(result["tracked_file_extension_counts"], {".csv": 1, ".json": 1})
        self.assertEqual((result["ahead"], result["behind"]), (0, 0))

    def test_inventory_does_not_fetch(self):
        first = self.clone()
        self.remote_commit()
        result = sync.sync_repository(self.repo, self.workspace, False)
        self.assertEqual(result["status"], "inventory_only")
        self.assertEqual(result["sha"], first["sha"])
        self.assertEqual(result["remote_freshness"], "local_refs_only")
        self.assertFalse((self.target / "extra.json").exists())

    def test_dirty_worktree_preserves_changes_and_does_not_fetch(self):
        self.clone()
        initial_remote = run_git(self.target, "rev-parse", "origin/main")
        self.remote_commit()
        (self.target / "data.csv").write_text("id\nlocal work\n")
        (self.target / "untracked.txt").write_text("keep me")
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "dirty_worktree")
        self.assertEqual((self.target / "data.csv").read_text(), "id\nlocal work\n")
        self.assertEqual((self.target / "untracked.txt").read_text(), "keep me")
        self.assertEqual(run_git(self.target, "rev-parse", "origin/main"), initial_remote)

    def test_wrong_origin_is_redacted(self):
        self.clone()
        remote = "https://secret-token@github.com/private/repo.git"
        run_git(self.target, "remote", "set-url", "origin", remote)
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "origin_mismatch")
        self.assertNotIn("secret-token", json.dumps(result))
        self.assertEqual(result["actions"], [])

    def test_branch_mismatch_does_not_switch(self):
        self.clone()
        run_git(self.target, "switch", "-c", "work-in-progress")
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "branch_mismatch")
        self.assertEqual(run_git(self.target, "branch", "--show-current"), "work-in-progress")

    def test_detached_head_is_blocked(self):
        self.clone()
        run_git(self.target, "checkout", "--detach")
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "detached_head")

    def test_diverged_history_preserves_local_head(self):
        self.clone()
        (self.target / "local.txt").write_text("local")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-m", "local change")
        local_head = run_git(self.target, "rev-parse", "HEAD")
        self.remote_commit()
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "diverged_history")
        self.assertEqual((result["ahead"], result["behind"]), (1, 1))
        self.assertEqual(run_git(self.target, "rev-parse", "HEAD"), local_head)

    def test_local_ahead_is_preserved_without_push(self):
        initial = self.clone()
        (self.target / "local.txt").write_text("local")
        run_git(self.target, "add", ".")
        run_git(self.target, "commit", "-m", "local change")
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["status"], "local_ahead")
        self.assertEqual(result["ahead"], 1)
        self.assertEqual(run_git(self.remote, "rev-parse", "main"), initial["sha"])

    def test_rewritten_origin_is_blocked(self):
        self.clone()
        run_git(self.target, "config", "url.https://secret@example.invalid/.insteadOf", str(self.remote))
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "origin_mismatch")
        self.assertNotIn("secret", json.dumps(result))

    def test_linked_worktree_is_blocked(self):
        run_git(self.source, "worktree", "add", "-b", "linked", str(self.target))
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "unsupported_git_directory_or_linked_worktree")

    def test_symlink_or_junction_escape_is_blocked(self):
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "mklink", "/J", str(self.target), str(self.source)],
                           capture_output=True, check=True)
            self.addCleanup(lambda: os.rmdir(self.target) if self.target.exists() else None)
        else:
            self.target.symlink_to(self.source, target_is_directory=True)
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "path_outside_workspace")

    def test_git_directory_escape_is_blocked(self):
        self.clone()
        metadata = self.target / ".git"
        moved = self.root / "outside-metadata"
        metadata.rename(moved)
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "mklink", "/J", str(metadata), str(moved)],
                           capture_output=True, check=True)
            self.addCleanup(lambda: os.rmdir(metadata) if metadata.exists() else None)
        else:
            metadata.symlink_to(moved, target_is_directory=True)
        result = sync.sync_repository(self.repo, self.workspace, True)
        self.assertEqual(result["error"], "unsupported_git_directory_or_linked_worktree")

    def test_output_cannot_overwrite_repository_or_existing_file(self):
        self.clone()
        with self.assertRaisesRegex(sync.SyncError, "output_inside_repository"):
            sync.output_path(str(self.target / "data.csv"), self.workspace, [self.repo])
        existing = self.root / "report.json"
        existing.write_text("keep")
        with self.assertRaisesRegex(sync.SyncError, "output_already_exists"):
            sync.output_path(str(existing), self.workspace, [self.repo])
        self.assertEqual(existing.read_text(), "keep")

    def test_cli_reports_all_entries_and_nonzero_for_blocked(self):
        self.target.mkdir()
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps(dict(schema_version=1, repositories=[
            dict(name="project", url="https://github.com/example/project.git", branch="main"),
            dict(name="missing", url="https://github.com/example/missing.git", branch="main")
        ])))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = sync.main(["--manifest", str(manifest), "--workspace", str(self.workspace)])
        report = json.loads(output.getvalue())
        self.assertEqual(code, 1)
        self.assertEqual(len(report["entries"]), 2)
        self.assertEqual(report["entries"][1]["status"], "missing_dry_run")


class ValidationTests(unittest.TestCase):
    def test_url_validation(self):
        self.assertEqual(sync.validate_url("https://github.com/VOSYDUNG/nnc-claude-plugins.git"),
                         "https://github.com/VOSYDUNG/nnc-claude-plugins.git")
        for value in ["git@github.com:owner/repo", "https://token@github.com/o/r.git",
                      "http://github.com/o/r", "https://github.com.evil/o/r",
                      "https://github.com/o/r?token=secret", "https://github.com/o/r#secret",
                      "https://github.com/o/r/tree/main", "https://github.com/o/..",
                      "https://github.com:443/o/r", "file:///tmp/repo"]:
            with self.subTest(value=value), self.assertRaises(sync.SyncError):
                sync.validate_url(value)

    def test_branch_and_name_validation(self):
        self.assertEqual(sync.validate_branch("release/2026-09"), "release/2026-09")
        for value in ["--upload-pack=evil", "HEAD", "a..b", "a b", "a@{b", "a:b", "a\\b", "", "a.lock"]:
            with self.subTest(value=value), self.assertRaises(sync.SyncError):
                sync.validate_branch(value)
        for value in ["..", "../outside", "a/b", "a\\b", "NUL", "CON.txt", "name.", "C:drive"]:
            with self.subTest(value=value), self.assertRaises(sync.SyncError):
                sync.validate_name(value)


if __name__ == "__main__":
    unittest.main()
