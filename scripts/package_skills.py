#!/usr/bin/env python3
"""Validate and package self-contained skills; adapted from the original ZIP helpers."""
import argparse
import hashlib
from pathlib import Path
import zipfile

from validate_skills import ROOT, find_creator, skill_paths, validate_skill


def package_skill(skill: Path, destination: Path, creator: Path) -> dict:
    skill = skill.resolve()
    destination = destination.resolve()
    if destination.is_relative_to(skill):
        raise ValueError("Archive destination must be outside the skill")
    result = validate_skill(skill, creator)
    if not result["pass"]:
        raise ValueError(f"{skill.name} did not validate: {result['errors']}")
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / (skill.name + ".zip")
    files = [skill / item["path"] for item in result["files"]]
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as output:
        for path in files:
            output.write(path, (Path(skill.name) / path.relative_to(skill)).as_posix())
    with zipfile.ZipFile(archive) as output:
        if output.testzip() is not None or len(output.namelist()) != len(files):
            raise ValueError("Archive integrity failed")
        for path in files:
            if output.read((Path(skill.name) / path.relative_to(skill)).as_posix()) != path.read_bytes():
                raise ValueError("Archive bytes differ from skill source")
    return {"skill": skill.name, "files": len(files), "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*")
    parser.add_argument("--creator-validator", type=Path)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args(argv)
    try:
        creator = find_creator(args.creator_validator)
        for skill in skill_paths(args.skills):
            result = package_skill(skill, args.output_dir, creator)
            print(f"PASS {result['skill']}: {result['files']} files; sha256 {result['sha256']}")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Packaging failed: {exc}\n")


if __name__ == "__main__":
    main()
