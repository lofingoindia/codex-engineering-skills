#!/usr/bin/env python3
"""Validate and package self-contained skills; adapted from the original ZIP helpers."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

from validate_skills import ROOT, find_creator, skill_paths, validate_skill


def source_snapshot(skill: Path, files: list[dict]) -> dict[str, bytes]:
    paths = {path.relative_to(skill).as_posix(): path for path in skill.rglob("*")
             if path.is_file() or path.is_symlink()}
    if set(paths) != {item["path"] for item in files} or any(path.is_symlink() for path in paths.values()):
        raise ValueError("Skill source inventory changed after validation")
    snapshot = {}
    for item in files:
        data = paths[item["path"]].read_bytes()
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError("Skill source bytes changed after validation")
        snapshot[item["path"]] = data
    return snapshot


def package_skill(skill: Path, destination: Path, creator: Path) -> dict:
    if skill.is_symlink():
        raise ValueError("Skill directory must be materialized, not a symlink")
    original_skill = skill
    skill = skill.resolve()
    destination = destination.resolve()
    if destination.is_relative_to(skill):
        raise ValueError("Archive destination must be outside the skill")
    result = validate_skill(original_skill, creator)
    if not result["pass"]:
        raise ValueError(f"{skill.name} did not validate: {result['errors']}")
    snapshot = source_snapshot(skill, result["files"])
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / (skill.name + ".zip")
    # Exclusively create before the cleanup boundary; never delete a pre-existing file.
    stream = archive.open("xb")
    try:
        with stream, zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as output:
            for relative, data in snapshot.items():
                info = zipfile.ZipInfo.from_file(skill / relative, f"{skill.name}/{relative}", strict_timestamps=False)
                output.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)
        with zipfile.ZipFile(archive) as output:
            if output.testzip() is not None or set(output.namelist()) != {f"{skill.name}/{rel}" for rel in snapshot}:
                raise ValueError("Archive integrity failed")
            for relative, data in snapshot.items():
                if output.read(f"{skill.name}/{relative}") != data:
                    raise ValueError("Archive bytes differ from validated source")
        source_snapshot(skill, result["files"])
    except Exception:
        archive.unlink()
        raise
    return {"skill": skill.name, "files": len(snapshot), "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", help="Repository skill names or explicit directory paths")
    parser.add_argument("--creator-validator", type=Path)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--json-output", type=Path, help="Optional local packaging evidence file")
    args = parser.parse_args(argv)
    try:
        creator = find_creator(args.creator_validator)
        selected = skill_paths(args.skills)
        destination = args.output_dir.resolve()
        if any(destination.is_relative_to(skill) for skill in selected):
            raise ValueError("Archive destination must be outside every selected skill")
        if len({skill.name for skill in selected}) != len(selected):
            raise ValueError("Selected skills have duplicate package names")
        if args.json_output:
            if args.json_output.exists():
                raise FileExistsError("JSON output already exists; choose a new evidence file")
            if any(args.json_output.resolve().is_relative_to(skill) for skill in selected):
                raise ValueError("JSON output must be outside every selected skill")
        results = []
        for skill in selected:
            result = package_skill(skill, args.output_dir, creator)
            results.append(result)
            print(f"PASS {result['skill']}: {result['files']} files; sha256 {result['sha256']}")
        if args.json_output:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            with args.json_output.open("x", encoding="utf-8") as report:
                report.write(json.dumps({"pass": True, "skills": results}, indent=2) + "\n")
    except (OSError, ValueError, subprocess.TimeoutExpired, zipfile.BadZipFile) as exc:
        parser.exit(1, f"Packaging failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
