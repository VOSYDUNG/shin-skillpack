#!/usr/bin/env python3
"""Inventory GitHub repositories; explicitly opt in to conservative fast-forward sync.

No repository file contents are read. The CLI accepts only canonical GitHub HTTPS
URLs. Internal functions deliberately accept fixture URLs for network-free tests.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit


class SyncError(Exception):
    """A fixed, credential-free diagnostic code."""


def git(cwd: Path | None, *args: str, optional: bool = False) -> str | None:
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0",
               GCM_INTERACTIVE="never")
    # Inherited Git directory overrides must not redirect commands elsewhere.
    for key in list(env):
        if key.startswith("GIT_") and key not in {
            "GIT_OPTIONAL_LOCKS", "GIT_TERMINAL_PROMPT", "GIT_SSL_CAINFO",
            "GIT_SSL_CAPATH", "GIT_SSH", "GIT_SSH_COMMAND"}:
            del env[key]
    command = ["git", "-c", "core.fsmonitor=false", "-c", "submodule.recurse=false",
               "-c", f"core.hooksPath={os.devnull}", *args]
    try:
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                                timeout=180, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise SyncError("git_unavailable_or_timeout") from None
    if result.returncode:
        if optional:
            return None
        raise SyncError("git_command_failed")
    return result.stdout.decode("utf-8", errors="replace").rstrip("\r\n")


def validate_name(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}", value):
        raise SyncError("invalid_repository_name")
    if value.endswith(".") or value.split(".")[0].upper() in {
        "CON", "PRN", "AUX", "NUL", *[f"COM{i}" for i in range(1, 10)],
        *[f"LPT{i}" for i in range(1, 10)]}:
        raise SyncError("invalid_repository_name")
    return value


def validate_url(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(
            r"https://github\.com/[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+", value):
        raise SyncError("invalid_github_url")
    parsed = urlsplit(value)
    repository = parsed.path.rsplit("/", 1)[-1]
    if repository in {".", "..", ".git"} or not repository.removesuffix(".git"):
        raise SyncError("invalid_github_url")
    return value


def validate_branch(value: object) -> str:
    if not isinstance(value, str) or not value or value.startswith("-") or value == "HEAD":
        raise SyncError("invalid_branch")
    if git(None, "check-ref-format", "--branch", value, optional=True) != value:
        raise SyncError("invalid_branch")
    return value


def read_manifest(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, UnicodeError):
        raise SyncError("manifest_unreadable_or_invalid_json") from None
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise SyncError("unsupported_manifest_schema")
    repositories = data.get("repositories")
    if not isinstance(repositories, list):
        raise SyncError("invalid_repositories_list")
    names = set()
    validated = []
    for item in repositories:
        if not isinstance(item, dict):
            raise SyncError("invalid_repository_entry")
        name = validate_name(item.get("name"))
        if name.casefold() in names:
            raise SyncError("duplicate_repository_name")
        names.add(name.casefold())
        role = item.get("role")
        if role is not None and (not isinstance(role, str) or len(role) > 200):
            raise SyncError("invalid_repository_role")
        validated.append(dict(name=name, url=validate_url(item.get("url")),
                              branch=validate_branch(item.get("branch")), role=role))
    return validated


def confined_path(workspace: Path, name: str) -> Path:
    candidate = workspace / validate_name(name)
    resolved = candidate.resolve()
    if resolved == workspace or not resolved.is_relative_to(workspace):
        raise SyncError("path_outside_workspace")
    return resolved


def verify_repository(target: Path, expected_url: str) -> None:
    # Refuse linked worktrees and git-dir indirection, including .git symlinks
    # pointing outside the selected directory. This keeps all writes local.
    metadata = target / ".git"
    if not metadata.is_dir() or not metadata.resolve().is_relative_to(target):
        raise SyncError("unsupported_git_directory_or_linked_worktree")
    top = git(target, "rev-parse", "--show-toplevel")
    if Path(top).resolve() != target:
        raise SyncError("repository_root_mismatch")
    configured = git(target, "config", "--get-all", "remote.origin.url", optional=True)
    effective = git(target, "remote", "get-url", "--all", "origin", optional=True)
    if configured != expected_url or effective != expected_url:
        raise SyncError("origin_mismatch")


def inventory(target: Path, branch: str, entry: dict) -> None:
    entry["sha"] = git(target, "rev-parse", "--verify", "HEAD")
    entry["branch"] = git(target, "symbolic-ref", "--quiet", "--short", "HEAD", optional=True)
    entry["clean"] = not bool(git(target, "status", "--porcelain=v1", "--untracked-files=all"))
    reference = f"refs/remotes/origin/{branch}"
    counts = git(target, "rev-list", "--left-right", "--count", f"HEAD...{reference}", optional=True)
    if counts is not None:
        ahead, behind = map(int, counts.split())
        entry.update(ahead=ahead, behind=behind)
    files = git(target, "ls-files", "--stage", "-z")
    extensions = Counter()
    links = []
    for record in files.split("\0"):
        if not record:
            continue
        metadata, filename = record.split("\t", 1)
        mode, sha, stage = metadata.split()
        if mode == "160000":
            links.append(dict(path=filename, sha=sha))
        else:
            extensions[Path(filename).suffix.lower() or "[none]"] += 1
    entry.update(tracked_file_extension_counts=dict(sorted(extensions.items())), gitlinks=links)


def sync_repository(repository: dict, workspace: Path, apply: bool) -> dict:
    entry = dict(name=repository["name"], expected_branch=repository["branch"],
                 status="pending", sha=None, branch=None, clean=None, ahead=None,
                 behind=None, actions=[], tracked_file_extension_counts={}, gitlinks=[])
    try:
        target = confined_path(workspace, repository["name"])
        entry["path"] = str(target)
        if not target.exists():
            if not apply:
                entry["status"] = "missing_dry_run"
                return entry
            # Resolve Git's insteadOf rules without connecting, before clone can
            # contact an endpoint different from the manifest's approved URL.
            if git(workspace, "ls-remote", "--get-url", repository["url"]) != repository["url"]:
                raise SyncError("clone_url_rewritten")
            git(workspace, "clone", "--no-recurse-submodules", "--single-branch", "--branch",
                repository["branch"], "--", repository["url"], str(target))
            entry["actions"].append("cloned")
        if not target.is_dir():
            raise SyncError("target_is_not_directory")
        verify_repository(target, repository["url"])
        inventory(target, repository["branch"], entry)
        if entry["branch"] is None:
            raise SyncError("detached_head")
        if entry["branch"] != repository["branch"]:
            raise SyncError("branch_mismatch")
        if not entry["clean"]:
            raise SyncError("dirty_worktree")
        if apply:
            git(target, "fetch", "--no-tags", "--no-recurse-submodules", "origin",
                f"refs/heads/{repository['branch']}:refs/remotes/origin/{repository['branch']}")
            entry["actions"].append("fetched")
            inventory(target, repository["branch"], entry)
        if entry["ahead"] and entry["behind"]:
            raise SyncError("diverged_history")
        if apply and entry["behind"]:
            # Recheck local state immediately before the only update operation.
            verify_repository(target, repository["url"])
            inventory(target, repository["branch"], entry)
            if entry["branch"] != repository["branch"] or not entry["clean"]:
                raise SyncError("repository_changed_during_sync")
            git(target, "merge", "--ff-only", f"refs/remotes/origin/{repository['branch']}")
            entry["actions"].append("fast_forwarded")
            inventory(target, repository["branch"], entry)
        entry["status"] = ("local_ahead" if apply and entry["ahead"] else
                           "synced" if apply else "inventory_only")
        entry["remote_freshness"] = "fetched_this_run" if apply else "local_refs_only"
    except SyncError as error:
        entry.update(status="blocked", error=str(error))
    except (OSError, ValueError, TypeError):
        entry.update(status="failed", error="local_inspection_failed")
    return entry


def output_path(path: str | None, workspace: Path, repositories: list[dict]) -> Path | None:
    if path is None:
        return None
    target = Path(path).resolve()
    for repository in repositories:
        repo_path = (workspace / repository["name"]).resolve()
        if target == repo_path or target.is_relative_to(repo_path):
            raise SyncError("output_inside_repository")
    # Also avoid altering a surrounding project checkout's tracked files.
    if target.exists():
        raise SyncError("output_already_exists")
    if not target.parent.is_dir():
        raise SyncError("output_parent_missing")
    parent_repo = git(target.parent, "rev-parse", "--show-toplevel", optional=True)
    if parent_repo:
        relative = target.relative_to(Path(parent_repo).resolve()).as_posix()
        tracked = git(Path(parent_repo), "ls-files", "--error-unmatch", "--", relative, optional=True)
        if tracked is not None:
            raise SyncError("output_is_tracked_file")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    report = dict(schema_version=1, observed_at=datetime.now(timezone.utc).isoformat(),
                  mode="apply" if args.apply else "inventory", entries=[], errors=[])
    destination = None
    try:
        workspace = Path(args.workspace)
        if not workspace.is_absolute() or not workspace.is_dir():
            raise SyncError("workspace_must_be_existing_absolute_directory")
        workspace = workspace.resolve()
        repositories = read_manifest(Path(args.manifest))
        destination = output_path(args.output, workspace, repositories)
        for repository in repositories:
            report["entries"].append(sync_repository(repository, workspace, args.apply))
    except SyncError as error:
        report["errors"].append(str(error))
    except (OSError, ValueError, TypeError):
        report["errors"].append("local_configuration_failed")
    failed = bool(report["errors"]) or any(e["status"] in {"blocked", "failed"} for e in report["entries"])
    report["ok"] = not failed
    serialized = json.dumps(report, ensure_ascii=True, indent=2) + "\n"
    if destination is not None:
        try:
            # Exclusive creation avoids overwriting code or a concurrent writer.
            with destination.open("x", encoding="utf-8") as output:
                output.write(serialized)
        except OSError:
            report["errors"].append("output_write_failed")
            report["ok"] = False
            failed = True
            serialized = json.dumps(report, ensure_ascii=True, indent=2) + "\n"
    sys.stdout.write(serialized)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
