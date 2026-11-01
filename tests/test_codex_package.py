"""Tests for the bounded Codex package builder."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "build_codex_plugin.py"
spec = importlib.util.spec_from_file_location("build_codex_plugin", SCRIPT)
assert spec and spec.loader
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class CodexPackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.output = Path(self.temp.name) / "output"
        self.original_root = builder.ROOT
        builder.ROOT = self.root
        self.addCleanup(setattr, builder, "ROOT", self.original_root)
        manifest = json.dumps({"name": builder.PLUGIN, "skills": "./skills/"})
        source = self.root / builder.SOURCE
        write(source / "plugin.json", manifest)
        write(source / ".codex-plugin" / "plugin.json", manifest)
        for name in builder.LOCAL_SKILLS:
            write(source / "skills" / name / "SKILL.md", f"---\nname: {name}\ndescription: Local method.\n---\n\n# {name}\n")
        for plugin, skills in builder.UPSTREAM.items():
            write(self.root / "plugins" / plugin / "CONNECTORS.md", "# Connector placeholders\n")
            for name in skills:
                body = f"# {name}\n"
                if name in {"write-spec", "runbook"}:
                    body += "See [CONNECTORS.md](../../CONNECTORS.md).\n"
                write(
                    self.root / "plugins" / plugin / "skills" / name / "SKILL.md",
                    f"---\nname: {name}\ndescription: Upstream method.\nargument-hint: Claude only\nuser-invocable: true\nmetadata:\n  short-description: Useful\nallowed-tools: Read\n---\n\n{body}",
                )
        write(self.root / "LICENSE", "Apache-2.0\n")
        write(self.root / "NOTICE.md", "Attribution\n")

    def test_repeat_build_is_deterministic_and_self_contained(self) -> None:
        write(self.root / builder.SOURCE / "skills" / "nnc-ai-oser" / "scripts" / "__pycache__" / "helper.pyc", "cached")
        first = builder.build(self.output)
        package = Path(first["package"])
        first_zip = Path(first["zip"]).read_bytes()
        second = builder.build(self.output)
        self.assertEqual(first, second)
        self.assertEqual(first_zip, Path(first["zip"]).read_bytes())
        self.assertEqual(first["skills"], 11)
        self.assertTrue((package / ".codex-plugin" / "plugin.json").is_file())
        self.assertTrue((package / "plugin.json").is_file())
        self.assertEqual((package / "SHA256SUMS").read_text(encoding="utf-8"), builder._checksums(package))
        for plugin, skills in builder.UPSTREAM.items():
            for name in skills:
                skill = package / "skills" / name / "SKILL.md"
                text = skill.read_text(encoding="utf-8")
                self.assertIn(f"name: {name}", text)
                self.assertNotIn("argument-hint:", text)
                self.assertNotIn("user-invocable:", text)
                self.assertIn("allowed-tools: Read", text)
                self.assertNotIn("../../CONNECTORS.md", text)
                if "references/CONNECTORS.md" in text:
                    self.assertTrue((skill.parent / "references" / "CONNECTORS.md").is_file())
        with zipfile.ZipFile(first["zip"]) as archive:
            self.assertIn(".codex-plugin/plugin.json", archive.namelist())
            self.assertIn("plugin.json", archive.namelist())
            self.assertIn("SHA256SUMS", archive.namelist())
            self.assertEqual(archive.read("SHA256SUMS"), (package / "SHA256SUMS").read_bytes())
            self.assertFalse(any("workspace" in name or ".mcp" in name or ".app" in name for name in archive.namelist()))
            self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in archive.namelist()))

    def test_private_source_fails_before_replacing_existing_output(self) -> None:
        first = builder.build(self.output)
        old_zip = Path(first["zip"]).read_bytes()
        write(self.root / builder.SOURCE / "skills" / builder.PLUGIN / "workspace" / "private.json", "secret")
        with self.assertRaisesRegex(ValueError, "private source path"):
            builder.build(self.output)
        self.assertEqual(old_zip, Path(first["zip"]).read_bytes())
        self.assertEqual((Path(first["package"]) / "SHA256SUMS").read_text(encoding="utf-8"), builder._checksums(Path(first["package"])))

    def test_unowned_output_is_preserved(self) -> None:
        target = self.output / "codex" / builder.PLUGIN
        write(target / "keep.txt", "mine")
        with self.assertRaisesRegex(ValueError, "not an intact package"):
            builder.build(self.output)
        self.assertEqual((target / "keep.txt").read_text(encoding="utf-8"), "mine")

    def test_source_symlink_is_rejected(self) -> None:
        skill = self.root / builder.SOURCE / "skills" / builder.PLUGIN
        outside = Path(self.temp.name) / "outside.txt"
        write(outside, "secret")
        try:
            (skill / "link.txt").symlink_to(outside)
        except OSError:
            self.skipTest("symlink creation unavailable")
        with self.assertRaisesRegex(ValueError, "symlink source refused"):
            builder.build(self.output)

    def test_broken_skill_link_fails_without_publishing(self) -> None:
        skill = self.root / builder.SOURCE / "skills" / builder.PLUGIN / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\n[missing](references/missing.md)\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "broken or unsafe skill link"):
            builder.build(self.output)
        self.assertFalse((self.output / "codex" / builder.PLUGIN).exists())
        self.assertFalse((self.output / f"{builder.PLUGIN}.zip").exists())


if __name__ == "__main__":
    unittest.main()
