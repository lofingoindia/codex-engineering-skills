"""Release provenance regressions use a disposable, synthetic Git repository."""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import stat
import sys
import tempfile
import unittest
import warnings
from contextlib import redirect_stdout
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import release_manifest as release


class ReleaseManifestChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "source"
        self.repo.mkdir()
        self.git("init", "--template=", ".")
        self.write_skill("alpha-skill")
        self.write_skill("beta-skill")
        self.commit()
        self.git("tag", "-a", "v1.0.0", "-m", "Synthetic release")
        self.first = self.git("rev-parse", "HEAD").strip()

    def git(self, *arguments):
        result = subprocess.run(["git", "-C", str(self.repo), "-c", "core.autocrlf=false",
                                 "-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid",
                                 "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false", *arguments],
                                capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def write_skill(self, name):
        folder = self.repo / "skills" / name
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_bytes(f"---\nname: {name}\ndescription: Synthetic fixture.\n---\n".encode())
        (folder / ".binary").write_bytes(b"\x00\xff\r\n")

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "-m", "Synthetic content")

    def build(self, ref="HEAD", previous=None, package_dir=None):
        return release.build_manifest(ref, previous, package_dir, repo=self.repo)

    def packages(self):
        destination = self.base / "packages"
        destination.mkdir()
        for folder in (self.repo / "skills").iterdir():
            with zipfile.ZipFile(destination / (folder.name + ".zip"), "w") as archive:
                for path in folder.iterdir():
                    archive.writestr(folder.name + "/" + path.name, path.read_bytes())
        return destination

    def test_explicit_annotated_tag_is_version_authority_and_commit_is_immutable(self):
        manifest = self.build("v1.0.0")
        self.assertEqual(manifest["collection_version"], "1.0.0")
        self.assertEqual(manifest["source_commit"], self.first)
        self.assertEqual(manifest, self.build("refs/tags/v1.0.0"))
        self.assertIsNone(self.build()["collection_version"])
        self.assertNotIn(str(self.repo), json.dumps(manifest))
        self.assertNotIn("fixture@example", json.dumps(manifest))

    def test_identity_matches_complete_portable_inventory(self):
        skill = self.build()["skills"][0]
        files = []
        for path in sorted((self.repo / "skills/alpha-skill").iterdir()):
            data = path.read_bytes()
            files.append({"path": path.name, "mode": "100644", "bytes": len(data),
                          "sha256": hashlib.sha256(data).hexdigest()})
        expected = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":"),
                                             ensure_ascii=False).encode("utf-8")).hexdigest()
        self.assertEqual(skill["files"], files)
        self.assertEqual(skill["content_sha256"], expected)
        self.assertEqual(skill["git_tree_sha"], self.git("rev-parse", "HEAD:skills/alpha-skill").strip())

    def test_worktree_bytes_and_timestamps_do_not_change_committed_identity(self):
        before = self.build()
        path = self.repo / "skills/alpha-skill/.binary"
        os.utime(path, (1, 1))
        path.write_bytes(b"Uncommitted changes")
        (self.repo / "skills/alpha-skill/untracked").write_bytes(b"Extra")
        self.assertEqual(before, self.build())
        self.assertEqual(path.read_bytes(), b"Uncommitted changes")

    def test_doc_commit_changes_no_skill_and_file_change_targets_one_skill(self):
        (self.repo / "README.md").write_bytes(b"Collection documentation")
        self.commit()
        self.assertEqual(self.build(previous="v1.0.0")["changes"], {"added": [], "changed": [], "removed": []})
        (self.repo / "skills/alpha-skill/.binary").write_bytes(b"Changed")
        self.commit()
        self.assertEqual(self.build(previous="v1.0.0")["changes"], {"added": [], "changed": ["alpha-skill"], "removed": []})

    def test_added_and_removed_skills_are_reported(self):
        self.git("rm", "-r", "skills/beta-skill")
        self.write_skill("gamma-skill")
        self.commit()
        manifest = self.build(previous="v1.0.0")
        self.assertEqual(manifest["previous_source_commit"], self.first)
        self.assertEqual(manifest["changes"], {"added": ["gamma-skill"], "changed": [], "removed": ["beta-skill"]})

    def test_git_executable_mode_changes_identity_on_every_host(self):
        self.git("update-index", "--chmod=+x", "skills/alpha-skill/.binary")
        self.git("commit", "-m", "Executable fixture")
        manifest = self.build(previous="v1.0.0")
        self.assertEqual(manifest["changes"]["changed"], ["alpha-skill"])
        self.assertEqual(manifest["skills"][0]["files"][0]["mode"], "100755")

    def test_invalid_option_like_and_noncommit_refs_fail_clearly(self):
        for ref in ("does-not-exist", "--output=unexpected", "HEAD:skills", ""):
            with self.subTest(ref=ref), self.assertRaisesRegex(ValueError, "requested ref"):
                self.build(ref)
        with self.assertRaises(ValueError):
            self.build(previous="missing-previous")
        self.git("branch", "v9.9.9")
        with self.assertRaises(ValueError):
            self.build("v9.9.9")  # A similarly named branch is not a release tag.

    def test_complete_packages_match_exact_committed_bytes_and_report_archive_digests(self):
        directory = self.packages()
        manifest = self.build("v1.0.0", package_dir=directory)
        self.assertEqual(len(manifest["packages"]), 2)
        for package in manifest["packages"]:
            self.assertEqual(package["sha256"], hashlib.sha256((directory / package["filename"]).read_bytes()).hexdigest())
        self.assertNotIn(str(directory), json.dumps(manifest))

    def test_package_from_another_version_is_rejected(self):
        directory = self.packages()
        (self.repo / "skills/alpha-skill/.binary").write_bytes(b"Next version")
        self.commit()
        self.git("tag", "v1.0.1")
        self.assertEqual(self.build("v1.0.0", package_dir=directory)["collection_version"], "1.0.0")
        with self.assertRaisesRegex(ValueError, "bytes differ"):
            self.build("v1.0.1", package_dir=directory)

    def test_duplicate_traversal_missing_extra_and_tampered_members_are_rejected(self):
        directory = self.packages()
        path = directory / "alpha-skill.zip"
        original = path.read_bytes()
        for member, data in (("alpha-skill/SKILL.md", b"Duplicate"), ("../escape", b"Unsafe"),
                             ("alpha-skill/extra", b"Extra")):
            with self.subTest(member=member), warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                path.write_bytes(original)
                with zipfile.ZipFile(path, "a") as archive:
                    archive.writestr(member, data)
                with self.assertRaisesRegex(ValueError, "inventory"):
                    self.build(package_dir=directory)
        for contents in ({"alpha-skill/SKILL.md": b"Only one member"},
                         {"alpha-skill/SKILL.md": (self.repo / "skills/alpha-skill/SKILL.md").read_bytes(),
                          "alpha-skill/.binary": b"Tampered"}):
            with zipfile.ZipFile(path, "w") as archive:
                for member, data in contents.items():
                    archive.writestr(member, data)
            with self.assertRaises(ValueError):
                self.build(package_dir=directory)

    def test_missing_extra_and_corrupt_archives_are_rejected(self):
        directory = self.packages()
        path = directory / "alpha-skill.zip"
        original = path.read_bytes()
        path.unlink()
        with self.assertRaisesRegex(ValueError, "inventory"):
            self.build(package_dir=directory)
        path.write_bytes(original)
        extra = directory / "unexpected.zip"
        extra.write_bytes(b"Not a package")
        with self.assertRaisesRegex(ValueError, "unexpected"):
            self.build(package_dir=directory)
        extra.unlink()
        path.write_bytes(b"Corrupt")
        with self.assertRaisesRegex(ValueError, "corrupt"):
            self.build(package_dir=directory)

    def test_symlink_source_and_archive_members_are_rejected_without_extracting(self):
        blob = self.git("rev-parse", "HEAD:skills/alpha-skill/.binary").strip()
        self.git("update-index", "--add", "--cacheinfo", f"120000,{blob},skills/linked-skill")
        self.git("commit", "-m", "Synthetic symlink")
        with self.assertRaisesRegex(ValueError, "materialized"):
            self.build()
        directory = self.packages()
        with zipfile.ZipFile(directory / "alpha-skill.zip", "w") as archive:
            for path in (self.repo / "skills/alpha-skill").iterdir():
                info = zipfile.ZipInfo("alpha-skill/" + path.name)
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(info, path.read_bytes())
        with self.assertRaisesRegex(ValueError, "regular file"):
            self.build("v1.0.0", package_dir=directory)

    def test_cli_output_is_json_and_refuses_overwrite(self):
        expected = self.build("v1.0.0")
        # The command's repo remains anchored to its installation; isolate this fixture seam.
        with patch.object(release, "build_manifest", return_value=expected):
            capture = io.StringIO()
            with redirect_stdout(capture):
                self.assertEqual(release.main(["--ref", "v1.0.0"]), 0)
            self.assertEqual(json.loads(capture.getvalue()), expected)
            output = self.base / "manifest.json"
            self.assertEqual(release.main(["--json-output", str(output)]), 0)
            original = output.read_bytes()
            with self.assertRaises(SystemExit) as raised:
                release.main(["--json-output", str(output)])
            self.assertEqual(raised.exception.code, 1)
            self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
