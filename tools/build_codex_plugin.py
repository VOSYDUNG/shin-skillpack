#!/usr/bin/env python3
"""Build the bounded, skills-only Codex distribution of Shin Agentic Work."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = "shin-agentic-work"
SOURCE = Path("codex") / PLUGIN
UPSTREAM = {
    "productivity": ("outcome-work-management",),
    "product-management": (
        "product-brainstorming", "synthesize-research", "write-spec",
        "sprint-planning", "metrics-review",
    ),
    "operations": ("process-optimization", "risk-assessment", "runbook"),
}
LOCAL_SKILLS = {PLUGIN, "nnc-ai-oser"}
FORBIDDEN_PARTS = {
    ".git", ".claude", ".codex", "workspace", "workspaces", "private",
    "secrets", "credentials", ".env", ".mcp.json",
    ".app.json", ".DS_Store",
}
FORBIDDEN_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".sqlite", ".db"}
IGNORED_DIRS = {"__pycache__", ".pytest_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
FRONT_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s|$)")
FRONT_ALLOWED = {"name", "description", "metadata", "license", "allowed-tools"}
CONNECTOR_LINK = "[CONNECTORS.md](../../CONNECTORS.md)"
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _checked_source(relative: Path, *, directory: bool = False) -> Path:
    """Accept only real, in-repository, non-symlinked source paths."""
    root = ROOT.resolve(strict=True)
    candidate = ROOT / relative
    if any(part in FORBIDDEN_PARTS or part.startswith(".env") for part in relative.parts):
        raise ValueError(f"private source path refused: {relative}")
    if candidate.is_symlink() or any(part.is_symlink() for part in candidate.parents if part != ROOT):
        raise ValueError(f"symlink source refused: {relative}")
    resolved = candidate.resolve(strict=True)
    if not _within(resolved, root):
        raise ValueError(f"source escaped repository: {relative}")
    if directory != resolved.is_dir():
        raise ValueError(f"unexpected source type: {relative}")
    if not directory and resolved.suffix.lower() in FORBIDDEN_SUFFIXES:
        raise ValueError(f"private source file refused: {relative}")
    return resolved


def _copy_file(relative: Path, target: Path) -> None:
    source = _checked_source(relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def _copy_tree(relative: Path, target: Path) -> None:
    source = _checked_source(relative, directory=True)
    for current, dirs, files in os.walk(source, followlinks=False):
        here = Path(current)
        if any((here / name).is_symlink() for name in dirs + files):
            raise ValueError(f"symlink source refused: {here}")
        dirs[:] = [name for name in dirs if name not in IGNORED_DIRS]
        dirs.sort()
        files.sort()
        for name in dirs:
            child = here / name
            _checked_source(child.relative_to(ROOT), directory=True)
        for name in files:
            if Path(name).suffix.lower() in IGNORED_SUFFIXES:
                continue
            child = here / name
            _copy_file(child.relative_to(ROOT), target / child.relative_to(source))


def _normalise_frontmatter(skill_file: Path, expected_name: str) -> None:
    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {skill_file}")
    chunks: dict[str, list[str]] = {}
    key: str | None = None
    for line in match.group(1).splitlines():
        found = FRONT_KEY.match(line)
        if found:
            key = found.group(1)
            if key in chunks:
                raise ValueError(f"duplicate frontmatter key {key}: {skill_file}")
            chunks[key] = [line]
        elif key is not None and (line.startswith((" ", "\t")) or not line.strip()):
            chunks[key].append(line)
        else:
            raise ValueError(f"invalid frontmatter line: {skill_file}")
    if not chunks.get("name") or not chunks.get("description"):
        raise ValueError(f"name/description required: {skill_file}")
    if not chunks["name"][0].split(":", 1)[1].strip() or not chunks["description"][0].split(":", 1)[1].strip():
        raise ValueError(f"empty name/description: {skill_file}")
    header = [f"name: {expected_name}"]
    for field in ("description", "metadata", "license", "allowed-tools"):
        header.extend(chunks.get(field, []))
    body = text[match.end():]
    if CONNECTOR_LINK in body:
        body = body.replace(CONNECTOR_LINK, "[CONNECTORS.md](references/CONNECTORS.md)")
    skill_file.write_text("---\n" + "\n".join(header).rstrip() + "\n---\n" + body, encoding="utf-8", newline="\n")


def _validate_manifest(path: Path, *, codex: bool) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("name") != PLUGIN or (codex and data.get("skills") != "./skills/"):
        raise ValueError(f"unexpected plugin manifest: {path}")
    if any(key in data for key in ("apps", "mcpServers", "hooks")):
        raise ValueError(f"non-skills capability in manifest: {path}")


def _validate_resources(package: Path) -> None:
    for skill_file in sorted((package / "skills").glob("*/SKILL.md")):
        for target in MARKDOWN_LINK.findall(skill_file.read_text(encoding="utf-8")):
            if target.startswith(("#", "http://", "https://", "mailto:", "codex://", "app://")):
                continue
            local = (skill_file.parent / target.split("#", 1)[0]).resolve()
            if not _within(local, package.resolve()) or not local.exists() or local.is_symlink():
                raise ValueError(f"broken or unsafe skill link in {skill_file}: {target}")


def _files(package: Path) -> list[Path]:
    return sorted((p for p in package.rglob("*") if p.is_file()), key=lambda p: p.relative_to(package).as_posix())


def _checksums(package: Path) -> str:
    return "".join(
        f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(package).as_posix()}\n"
        for p in _files(package) if p != package / "SHA256SUMS"
    )


def _verify_owned(package: Path) -> None:
    if package.is_symlink() or not package.is_dir():
        raise ValueError(f"existing output is not a regular package: {package}")
    for item in package.rglob("*"):
        if item.is_symlink():
            raise ValueError(f"symlink in existing output refused: {item}")
    marker = package / "SHA256SUMS"
    if not marker.is_file() or marker.is_symlink() or marker.read_text(encoding="utf-8") != _checksums(package):
        raise ValueError(f"existing output is not an intact package built by this tool: {package}")
    _validate_manifest(package / ".codex-plugin" / "plugin.json", codex=True)


def _write_zip(package: Path, destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in _files(package):
            info = zipfile.ZipInfo(file.relative_to(package).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def _verify_old_zip(path: Path) -> None:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"existing zip is not a regular file: {path}")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or ".codex-plugin/plugin.json" not in names or "SHA256SUMS" not in names:
            raise ValueError(f"existing zip was not built by this tool: {path}")
        manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
        if manifest.get("name") != PLUGIN or manifest.get("skills") != "./skills/":
            raise ValueError(f"existing zip has unexpected manifest: {path}")
        checksums = "".join(
            f"{hashlib.sha256(archive.read(name)).hexdigest()}  {name}\n"
            for name in sorted(names) if name != "SHA256SUMS"
        )
        if archive.read("SHA256SUMS").decode("utf-8") != checksums:
            raise ValueError(f"existing zip integrity check failed: {path}")


def build(output_parent: Path) -> dict[str, object]:
    output_parent = output_parent.absolute()
    if output_parent.is_symlink():
        raise ValueError(f"symlink output parent refused: {output_parent}")
    output_parent.mkdir(parents=True, exist_ok=True)
    output_parent = output_parent.resolve(strict=True)
    codex_parent = output_parent / "codex"
    if codex_parent.is_symlink():
        raise ValueError(f"symlink output folder refused: {codex_parent}")
    codex_parent.mkdir(exist_ok=True)
    package = codex_parent / PLUGIN
    zip_path = output_parent / f"{PLUGIN}.zip"
    if not _within(package.resolve(), codex_parent.resolve()) or package.parent != codex_parent:
        raise ValueError("package target escaped owned output folder")
    if package.exists() or package.is_symlink():
        _verify_owned(package)
    if zip_path.exists() or zip_path.is_symlink():
        _verify_old_zip(zip_path)

    with tempfile.TemporaryDirectory(prefix=f".{PLUGIN}-build-", dir=codex_parent) as scratch:
        staged = Path(scratch) / PLUGIN
        staged.mkdir()
        source = _checked_source(SOURCE, directory=True)
        allowed_source_files = {
            Path("plugin.json"), Path(".codex-plugin/plugin.json"),
        }
        for current, dirs, files in os.walk(source, followlinks=False):
            here = Path(current)
            if any((here / name).is_symlink() for name in dirs + files):
                raise ValueError(f"symlink source refused: {here}")
            dirs[:] = [name for name in dirs if name not in IGNORED_DIRS]
            for name in dirs + files:
                if Path(name).suffix.lower() in IGNORED_SUFFIXES:
                    continue
                item = here / name
                rel = item.relative_to(source)
                if not (rel.parts[0] == "skills" and len(rel.parts) >= 2 and rel.parts[1] in LOCAL_SKILLS) and rel not in allowed_source_files and rel != Path("skills") and rel != Path(".codex-plugin"):
                    raise ValueError(f"unexpected source plugin content: {item}")
                _checked_source(item.relative_to(ROOT), directory=item.is_dir())
        for rel in sorted(allowed_source_files):
            _copy_file(SOURCE / rel, staged / rel)
            _validate_manifest(staged / rel, codex=rel == Path(".codex-plugin/plugin.json"))
        for skill in sorted(LOCAL_SKILLS):
            _copy_tree(SOURCE / "skills" / skill, staged / "skills" / skill)
            if not (staged / "skills" / skill / "SKILL.md").is_file():
                raise ValueError(f"missing local skill: {skill}")
        for plugin, skills in UPSTREAM.items():
            for skill in skills:
                rel = Path("plugins") / plugin / "skills" / skill
                destination = staged / "skills" / skill
                _copy_tree(rel, destination)
                skill_file = destination / "SKILL.md"
                if not skill_file.is_file():
                    raise ValueError(f"missing upstream skill: {rel}")
                _normalise_frontmatter(skill_file, skill)
                if "[CONNECTORS.md](references/CONNECTORS.md)" in skill_file.read_text(encoding="utf-8"):
                    _copy_file(Path("plugins") / plugin / "CONNECTORS.md", destination / "references" / "CONNECTORS.md")
        _copy_file(Path("LICENSE"), staged / "LICENSE")
        _copy_file(Path("NOTICE.md"), staged / "NOTICE.md")
        _validate_resources(staged)
        (staged / "SHA256SUMS").write_text(_checksums(staged), encoding="utf-8", newline="\n")
        with tempfile.NamedTemporaryFile(prefix=f".{PLUGIN}-", suffix=".zip", dir=output_parent, delete=False) as temp_zip:
            staged_zip = Path(temp_zip.name)
        try:
            _write_zip(staged, staged_zip)
            backup = Path(scratch) / "old-package"
            if package.exists():
                package.rename(backup)
            try:
                staged.rename(package)
                os.replace(staged_zip, zip_path)
            except Exception:
                if package.exists():
                    package.rename(Path(scratch) / "failed-package")
                if backup.exists():
                    backup.rename(package)
                raise
        finally:
            staged_zip.unlink(missing_ok=True)
    return {
        "package": str(package),
        "zip": str(zip_path),
        "skills": len(LOCAL_SKILLS) + sum(map(len, UPSTREAM.values())),
        "files": len(_files(package)),
        "zip_sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-parent", type=Path, default=ROOT / "dist", help="Parent for codex/shin-agentic-work and ZIP")
    args = parser.parse_args()
    print(json.dumps(build(args.output_parent), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
