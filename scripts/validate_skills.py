#!/usr/bin/env python3
"""Validate skill folders using the upstream creator plus repository resource checks.

Adapted from the collection's original validate_skill.py workspace helper.
The upstream validator is an external dependency, never vendored here.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


def find_creator(explicit: Path | None = None) -> Path:
    home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    candidates = [explicit] if explicit else [
        ROOT / ".tools/openai-skills/skills/.system/skill-creator/scripts/quick_validate.py",
        home / "skills/.system/skill-creator/scripts/quick_validate.py",
    ]
    for candidate in candidates:
        if candidate and candidate.is_file():
            return candidate.resolve()
    raise ValueError("Upstream quick_validate.py not found; pass --creator-validator PATH. See CONTRIBUTING.md.")


def skill_paths(arguments: list[str]) -> list[Path]:
    paths = [Path(item).resolve() for item in arguments] if arguments else sorted((ROOT / "skills").iterdir())
    if not paths:
        raise ValueError("No skills selected")
    if len(set(paths)) != len(paths):
        raise ValueError("The same skill was selected more than once")
    return paths


def markdown_targets(text: str):
    """Inline links/images and reference definitions, excluding fenced examples."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            value = marker.group(1)
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        for match in re.finditer(r"\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[\"'][^)]*[\"'])?\s*\)", line):
            yield number, match.group(1).strip("<>")
        definition = re.match(r"^\s{0,3}\[[^]]+\]:\s*(<[^>]+>|\S+)", line)
        if definition:
            yield number, definition.group(1).strip("<>")


def resource_error(root: Path, source: Path, target: str) -> str | None:
    if target.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", target):
        return "absolute resource path"
    parsed = urlsplit(target)
    if parsed.scheme == "file":
        return "file URI is not a portable package resource"
    if parsed.scheme:
        return None  # Remote availability and non-file URI schemes are outside local validation.
    if not parsed.path:
        return None  # Heading anchors are not checked by this validator.
    decoded = unquote(parsed.path)
    if "\\" in decoded or Path(decoded).is_absolute():
        return "use portable relative paths with forward slashes"
    destination = (source.parent / decoded).resolve()
    if not destination.is_relative_to(root.resolve()):
        return "resource escapes the skill package"
    if not destination.exists():
        return "missing resource"
    # Detect Linux-breaking case differences even on a case-insensitive host.
    relative = os.path.relpath(source.parent / decoded, root)
    cursor = root
    for part in Path(relative).parts:
        if part == "..":
            cursor = cursor.parent
        elif part != ".":
            if part not in {item.name for item in cursor.iterdir()}:
                return "resource path has incorrect letter case"
            cursor = cursor / part
    return None


def validate_skill(skill: Path, creator: Path) -> dict:
    errors, warnings, links, files = [], [], [], []
    skill = skill.resolve()
    manifest = skill / "SKILL.md"
    if not skill.is_dir() or not manifest.is_file():
        return {"skill": skill.name, "pass": False, "errors": ["Missing skill directory or SKILL.md"], "warnings": [], "files": [], "links": []}
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(creator), str(skill)],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    if result.returncode:
        errors.append("Upstream validator: " + (result.stdout + result.stderr).strip()[:1200])
    try:
        text = manifest.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
        front = yaml.safe_load(match.group(1)) if match else None
        if not isinstance(front, dict):
            raise ValueError("frontmatter must be a mapping")
        if front.get("name") != skill.name:
            errors.append("Manifest name must match its directory")
        if not isinstance(front.get("description"), str) or not front["description"].strip():
            errors.append("Description must be nonempty")
    except (ValueError, yaml.YAMLError, UnicodeError) as exc:
        errors.append("Manifest: " + str(exc))
    for path in sorted(skill.rglob("*")):
        if path.is_symlink():
            errors.append(f"{path.relative_to(skill).as_posix()}: distribute materialized resources, not symlinks")
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(skill).as_posix()
        data = path.read_bytes()
        files.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        if path.suffix in (".md", ".yaml", ".yml", ".py"):
            try:
                content = data.decode("utf-8")
            except UnicodeError:
                errors.append(f"{rel}: expected UTF-8")
                continue
            if path.suffix == ".md":
                for line, target in markdown_targets(content):
                    issue = resource_error(skill, path, target)
                    links.append({"source": rel, "line": line, "target": target, "pass": issue is None})
                    if issue:
                        errors.append(f"{rel}:{line}: {issue}: {target}")
            if path.suffix == ".py":
                try:
                    ast.parse(content, filename=rel)
                except SyntaxError as exc:
                    errors.append(f"{rel}:{exc.lineno}: Python syntax error")
            if "[TODO:" in content:
                errors.append(f"{rel}: unfinished creator scaffold")
        elif path.suffix in (".sh", ".js", ".mjs", ".cjs", ".ps1", ".ts"):
            warnings.append(f"{rel}: syntax/execution requires its own documented native check")
    ui_file = skill / "agents/openai.yaml"
    if ui_file.exists():
        try:
            ui = yaml.safe_load(ui_file.read_text(encoding="utf-8"))
            if not isinstance(ui, dict):
                raise ValueError("UI metadata must be a mapping")
            interface = ui.get("interface", {})
            if not isinstance(interface, dict):
                raise ValueError("interface must be a mapping")
            for key in ("display_name", "short_description"):
                if key in interface and (not isinstance(interface[key], str) or not interface[key].strip()):
                    raise ValueError(f"{key} must be nonempty text")
            short = interface.get("short_description")
            if short is not None and not 25 <= len(short) <= 64:
                raise ValueError("short_description must have 25–64 characters")
            for key in ("icon_small", "icon_large"):
                if key in interface:
                    icon = interface[key]
                    if not isinstance(icon, str) or urlsplit(icon).scheme:
                        raise ValueError(f"{key} must be a local relative path")
                    # UI asset paths are relative to the skill root.
                    issue = resource_error(skill, manifest, icon)
                    if issue:
                        raise ValueError(f"{key}: {issue}")
            policy = ui.get("policy", {})
            if not isinstance(policy, dict) or ("allow_implicit_invocation" in policy and not isinstance(policy["allow_implicit_invocation"], bool)):
                raise ValueError("allow_implicit_invocation must be a boolean when present")
        except (ValueError, yaml.YAMLError, UnicodeError, TypeError) as exc:
            errors.append("agents/openai.yaml: " + str(exc))
    return {"skill": skill.name, "pass": not errors, "errors": errors, "warnings": warnings, "files": files, "links": links}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", help="Skill directory paths; defaults to this repository's skills/")
    parser.add_argument("--creator-validator", type=Path)
    parser.add_argument("--json-output", type=Path, help="Optional local evidence file; do not commit generated output")
    args = parser.parse_args(argv)
    try:
        creator = find_creator(args.creator_validator)
        results = [validate_skill(path, creator) for path in skill_paths(args.skills)]
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, f"Validation could not complete: {exc}\n")
    for result in results:
        print(f"{'PASS' if result['pass'] else 'FAIL'} {result['skill']} ({len(result['files'])} files)")
        for message in result["errors"]:
            print("  ERROR " + message)
        for message in result["warnings"]:
            print("  NOTE " + message)
    summary = {"pass": all(item["pass"] for item in results), "skills": results,
               "scope": "Upstream metadata plus local resources/UI/Python syntax; no activation or semantic agent evaluation"}
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
