#!/usr/bin/env python3
"""Describe committed skill content and optionally verify its release ZIPs.

Reads Git objects without checkout. An explicit vMAJOR.MINOR.PATCH tag is the
collection version authority; other refs have collection_version=null. Content
identity is SHA-256 of the sorted file inventory encoded as compact, key-sorted
UTF-8 JSON, including each relative path, Git mode, byte count and byte digest.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RELEASE_TAG = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def git(repo: Path, *arguments: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *arguments], capture_output=True, timeout=30)
    if result.returncode:
        # Git diagnostics can contain local absolute paths; keep public output bounded.
        raise ValueError(f"Git {arguments[0]} failed; verify that the repository and requested ref exist locally")
    return result.stdout


def resolve_source(repo: Path, ref: str) -> tuple[str, str | None]:
    tag = ref.removeprefix("refs/tags/")
    version = tag[1:] if RELEASE_TAG.fullmatch(tag) else None
    selected = "refs/tags/" + tag if version else ref
    commit = git(repo, "rev-parse", "--verify", "--end-of-options", selected + "^{commit}").decode("ascii").strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise ValueError("Git did not resolve one immutable source commit")
    return commit, version


def safe_member(name: str) -> bool:
    parts = name.split("/")
    return (bool(name) and not name.startswith("/") and "\\" not in name and ":" not in name
            and not any(ord(character) < 32 for character in name)
            and all(part not in ("", ".", "..") for part in parts))


def skill_inventory(repo: Path, commit: str) -> list[dict]:
    groups = {}
    listing = git(repo, "ls-tree", "-r", "-z", "--full-tree", commit, "--", "skills/")
    for row in listing.split(b"\0"):
        if not row:
            continue
        metadata, raw_path = row.split(b"\t", 1)
        path = raw_path.decode("utf-8")
        parts = PurePosixPath(path).parts
        mode, kind, object_id = metadata.decode("ascii").split()
        if len(parts) < 3:
            if mode in ("120000", "160000"):
                raise ValueError("Source skills must be materialized regular directories")
            continue  # Collection-level files are not independently installed skills.
        name, relative = parts[1], "/".join(parts[2:])
        if not SKILL_NAME.fullmatch(name) or not safe_member(path):
            raise ValueError("Source contains an unsafe skill package path")
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError(f"{name}/{relative}: materialized regular files required")
        data = git(repo, "cat-file", "blob", object_id)
        groups.setdefault(name, []).append({"path": relative, "mode": mode, "bytes": len(data),
                                           "sha256": hashlib.sha256(data).hexdigest()})
    if not groups:
        raise ValueError("No committed skills found at the selected source")
    trees = {}
    for row in git(repo, "ls-tree", "-z", commit + ":skills").split(b"\0"):
        if row:
            metadata, name = row.split(b"\t", 1)
            mode, kind, object_id = metadata.decode("ascii").split()
            if kind == "tree":
                trees[name.decode("utf-8")] = object_id
    skills = []
    for name, files in sorted(groups.items()):
        files.sort(key=lambda item: item["path"])
        if not any(item["path"] == "SKILL.md" for item in files):
            raise ValueError(f"{name}: committed skill has no SKILL.md")
        canonical = json.dumps(files, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        skills.append({"skill": name, "path": "skills/" + name,
                       "git_tree_sha": trees[name], "content_sha256": hashlib.sha256(canonical).hexdigest(), "files": files})
    return skills


def verify_packages(skills: list[dict], directory: Path) -> list[dict]:
    if not directory.is_dir():
        raise ValueError("Package directory does not exist")
    expected_archives = {item["skill"] + ".zip" for item in skills}
    actual_archives = {item.name for item in directory.glob("*.zip")}
    if actual_archives != expected_archives:
        raise ValueError("Package inventory differs from source: missing=" +
                         repr(sorted(expected_archives - actual_archives)) + "; unexpected=" +
                         repr(sorted(actual_archives - expected_archives)))
    results = []
    for skill in skills:
        filename = skill["skill"] + ".zip"
        path = directory / filename
        if path.is_symlink():
            raise ValueError(f"{filename}: package must be a materialized archive")
        expected = {skill["skill"] + "/" + item["path"]: item for item in skill["files"]}
        data = path.read_bytes()
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                infos = archive.infolist()
                names = [item.orig_filename for item in infos]
                if (len(names) != len(set(names)) or any(not safe_member(name) for name in names)
                        or set(names) != set(expected)):
                    raise ValueError(f"{filename}: archive member inventory differs from source or is unsafe")
                for info in infos:
                    kind = stat.S_IFMT(info.external_attr >> 16)
                    if kind not in (0, stat.S_IFREG):
                        raise ValueError(f"{filename}: regular file members required")
                    source = expected[info.filename]
                    if info.file_size != source["bytes"]:
                        raise ValueError(f"{filename}: archive bytes differ from selected Git source")
                    member_data = archive.read(info)
                    if hashlib.sha256(member_data).hexdigest() != source["sha256"]:
                        raise ValueError(f"{filename}: archive bytes differ from selected Git source")
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as exc:
            raise ValueError(f"{filename}: unreadable or corrupt archive") from exc
        results.append({"skill": skill["skill"], "filename": filename, "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})
    return results


def build_manifest(ref="HEAD", previous=None, package_dir=None, *, repo=ROOT) -> dict:
    commit, version = resolve_source(repo, ref)
    skills = skill_inventory(repo, commit)
    manifest = {"schema_version": 1, "collection_version": version, "source_commit": commit, "skills": skills}
    if previous is not None:
        old_commit, _ = resolve_source(repo, previous)
        old = {item["skill"]: item["content_sha256"] for item in skill_inventory(repo, old_commit)}
        current = {item["skill"]: item["content_sha256"] for item in skills}
        manifest["previous_source_commit"] = old_commit
        manifest["changes"] = {"added": sorted(current.keys() - old.keys()),
                               "changed": sorted(name for name in current.keys() & old.keys() if current[name] != old[name]),
                               "removed": sorted(old.keys() - current.keys())}
    if package_dir is not None:
        manifest["packages"] = verify_packages(skills, Path(package_dir))
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="Existing local Git ref; release version requires an explicit vMAJOR.MINOR.PATCH tag")
    parser.add_argument("--previous", help="Optional previous local Git ref for skill changes")
    parser.add_argument("--package-dir", type=Path, help="Verify a complete collection of existing skill ZIPs against the selected Git source")
    parser.add_argument("--json-output", type=Path, help="New output file; defaults to stdout and refuses existing files")
    args = parser.parse_args(argv)
    try:
        manifest = build_manifest(args.ref, args.previous, args.package_dir)
        data = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        if args.json_output:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            with args.json_output.open("x", encoding="utf-8", newline="\n") as output:
                output.write(data)
        else:
            print(data, end="")
    except (ValueError, OSError, UnicodeError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"Manifest failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
