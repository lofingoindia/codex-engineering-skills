"""Focused repository tooling regressions; no model calls or external services."""
import importlib.util
import io
import json
import os
import shutil
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_skills as validator
import package_skills as packager

spec = importlib.util.spec_from_file_location("eval_runner", ROOT / "evals/run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class SkillChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.creator = validator.find_creator()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.skill = self.base / "example-skill"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Verify an example behavior.\n---\n"
            "# Example\nUse [details](references/details.md).\n", encoding="utf-8")
        (self.skill / "references/details.md").write_text("# Details\n", encoding="utf-8")
        (self.skill / "LICENSE").write_text("Fixture license notice\n", encoding="utf-8")

    def check(self):
        return validator.validate_skill(self.skill, self.creator)

    def test_valid_self_contained_skill(self):
        self.assertTrue(self.check()["pass"])

    def test_missing_resource_fails(self):
        (self.skill / "references/details.md").unlink()
        self.assertFalse(self.check()["pass"])

    def test_reference_definition_missing_resource_fails(self):
        with (self.skill / "SKILL.md").open("a", encoding="utf-8") as output:
            output.write("[additional]: missing.md\n")
        self.assertFalse(self.check()["pass"])

    def test_escape_and_file_uri_rejected(self):
        (self.base / "private.md").write_text("Outside\n", encoding="utf-8")
        for target in ("../private.md", "%2e%2e/private.md", "file:///private.md"):
            with self.subTest(target=target):
                self.assertIsNotNone(validator.resource_error(self.skill, self.skill / "SKILL.md", target))

    def test_portable_case_is_checked(self):
        self.assertIsNotNone(validator.resource_error(self.skill, self.skill / "SKILL.md", "references/DETAILS.md"))

    def test_external_links_and_heading_anchors_are_not_local_resources(self):
        for target in ("https://example.com/docs", "mailto:maintainer@example.com", "#details"):
            self.assertIsNone(validator.resource_error(self.skill, self.skill / "SKILL.md", target))

    def test_encoded_spaces_and_code_examples(self):
        (self.skill / "references/with space.md").write_text("Details\n", encoding="utf-8")
        with (self.skill / "SKILL.md").open("a", encoding="utf-8") as output:
            output.write("[spaced](references/with%20space.md)\n```md\n[example](not-a-resource.md)\n```\n")
        self.assertTrue(self.check()["pass"])

    def test_name_must_match_directory(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("name: example-skill", "name: another-skill"), encoding="utf-8")
        self.assertFalse(self.check()["pass"])

    def test_missing_description_fails(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("description: Verify an example behavior.", "description: ''"), encoding="utf-8")
        self.assertFalse(self.check()["pass"])

    def test_optional_explicit_only_policy_is_valid(self):
        (self.skill / "agents").mkdir()
        (self.skill / "agents/openai.yaml").write_text("policy:\n  allow_implicit_invocation: false\n", encoding="utf-8")
        self.assertTrue(self.check()["pass"])

    def test_missing_ui_asset_fails(self):
        (self.skill / "agents").mkdir()
        (self.skill / "agents/openai.yaml").write_text("interface:\n  icon_small: assets/missing.png\n", encoding="utf-8")
        self.assertFalse(self.check()["pass"])

    def test_bundled_python_is_parsed_without_execution(self):
        (self.skill / "scripts").mkdir()
        script = self.skill / "scripts/helper.py"
        script.write_text("raise RuntimeError('Must not execute during syntax checks')\n", encoding="utf-8")
        self.assertTrue(self.check()["pass"])
        script.write_text("def broken(:\n", encoding="utf-8")
        self.assertFalse(self.check()["pass"])

    def test_explicit_missing_validator_does_not_fall_back(self):
        with self.assertRaises(ValueError):
            validator.find_creator(self.base / "missing.py")

    def test_duplicate_selection_is_rejected(self):
        with self.assertRaises(ValueError):
            validator.skill_paths([str(self.skill), str(self.skill)])

    def test_repository_name_resolves_from_another_working_directory(self):
        original = Path.cwd()
        self.addCleanup(os.chdir, original)
        os.chdir(self.base)
        expected = ROOT / "skills/api-design-engineering"
        self.assertEqual(validator.skill_paths(["api-design-engineering"]), [expected.resolve()])
        with self.assertRaisesRegex(ValueError, "more than once"):
            validator.skill_paths(["api-design-engineering", str(expected)])
        self.assertEqual(validator.skill_paths(["./example-skill"]), [self.skill.resolve()])

    def test_missing_name_and_invalid_directory_have_useful_errors(self):
        with self.assertRaisesRegex(ValueError, "Unknown repository skill.*explicit directory"):
            validator.skill_paths(["not-a-real-skill"])
        with self.assertRaisesRegex(ValueError, "SKILL.md"):
            validator.skill_paths([str(self.base)])
        with self.assertRaises(ValueError):
            validator.skill_paths([".."])

    def test_source_change_after_validation_is_rejected_without_an_archive(self):
        original = validator.validate_skill
        def changing_validation(*args):
            result = original(*args)
            (self.skill / "LICENSE").write_bytes(b"Changed after validation\n")
            return result
        with patch.object(packager, "validate_skill", side_effect=changing_validation):
            with self.assertRaisesRegex(ValueError, "changed"):
                packager.package_skill(self.skill, self.base / "dist", self.creator)
        self.assertFalse((self.base / "dist/example-skill.zip").exists())

    def test_binary_and_hidden_resources_are_packaged_without_changes(self):
        (self.skill / ".hidden").write_bytes(b"\x00\xff\r\n")
        (self.skill / "asset.bin").write_bytes(bytes(range(256)))
        packager.package_skill(self.skill, self.base / "dist", self.creator)
        with zipfile.ZipFile(self.base / "dist/example-skill.zip") as archive:
            self.assertEqual(archive.read("example-skill/.hidden"), b"\x00\xff\r\n")
            self.assertEqual(archive.read("example-skill/asset.bin"), bytes(range(256)))

    def test_packaging_cli_writes_json_and_handles_validator_timeout(self):
        report = self.base / "report.json"
        with redirect_stdout(io.StringIO()):
            self.assertEqual(packager.main([str(self.skill), "--output-dir", str(self.base / "dist"),
                                            "--json-output", str(report)]), 0)
        data = json.loads(report.read_text(encoding="utf-8"))
        self.assertTrue(data["pass"])
        self.assertEqual(data["skills"][0]["skill"], "example-skill")
        with patch.object(packager, "validate_skill", side_effect=subprocess.TimeoutExpired("validator", 30)):
            with self.assertRaises(SystemExit) as raised:
                packager.main([str(self.skill), "--output-dir", str(self.base / "next")])
        self.assertEqual(raised.exception.code, 1)

    def test_output_inside_any_selected_skill_is_rejected_before_writing(self):
        second = self.base / "second-skill"
        shutil.copytree(self.skill, second)
        manifest = second / "SKILL.md"
        manifest.write_text(manifest.read_text(encoding="utf-8").replace("example-skill", "second-skill"), encoding="utf-8")
        destination = second / "dist"
        with self.assertRaises(SystemExit):
            packager.main([str(self.skill), str(second), "--output-dir", str(destination)])
        self.assertFalse(destination.exists())
        with self.assertRaises(SystemExit):
            packager.main([str(self.skill), "--output-dir", str(self.base / "dist"),
                           "--json-output", str(self.skill / "report.json")])
        self.assertFalse((self.base / "dist").exists())

    def test_failed_archive_write_removes_only_its_new_archive(self):
        destination = self.base / "dist"
        with patch.object(zipfile.ZipFile, "writestr", side_effect=OSError("Synthetic write failure")):
            with self.assertRaisesRegex(OSError, "Synthetic"):
                packager.package_skill(self.skill, destination, self.creator)
        self.assertFalse((destination / "example-skill.zip").exists())

    def test_current_directory_is_an_explicit_skill_path(self):
        original = Path.cwd()
        self.addCleanup(os.chdir, original)
        os.chdir(self.skill)
        self.assertEqual(validator.skill_paths(["."]), [self.skill.resolve()])

    def test_validation_json_output_cannot_modify_selected_skill_but_external_reports_can_be_reused(self):
        for output in (self.skill / "SKILL.md", self.skill / "references/details.md", self.skill / "new/report.json"):
            with self.subTest(output=output):
                before = output.read_bytes() if output.exists() else None
                with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
                    validator.main([str(self.skill), "--json-output", str(output)])
                self.assertEqual(raised.exception.code, 2)
                self.assertEqual(output.read_bytes() if output.exists() else None, before)
        output = self.base / "evidence.json"
        output.write_text("Old evidence", encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(validator.main([str(self.skill), "--json-output", str(output)]), 0)
        self.assertTrue(json.loads(output.read_text(encoding="utf-8"))["pass"])

    def test_resolved_child_escape_is_rejected_before_reading_content(self):
        linked = self.skill / "escaped.bin"
        linked.write_bytes(b"Synthetic resource")
        outside = self.base / "outside.bin"
        outside.write_bytes(b"Synthetic external resource")
        original_resolve, original_read = Path.resolve, Path.read_bytes
        def resolved(path, *args, **kwargs):
            return outside if path == linked else original_resolve(path, *args, **kwargs)
        def read(path):
            if path == linked:
                self.fail("Read content through an escaped resource")
            return original_read(path)
        with patch.object(Path, "resolve", resolved), patch.object(Path, "read_bytes", read):
            result = self.check()
            self.assertFalse(result["pass"])
            self.assertTrue(any("escapes the skill package" in error for error in result["errors"]))
            self.assertNotIn("escaped.bin", {item["path"] for item in result["files"]})
            with self.assertRaises(ValueError):
                packager.package_skill(self.skill, self.base / "dist", self.creator)
        self.assertFalse((self.base / "dist").exists())

    @unittest.skipUnless(os.name == "nt", "Windows junction regression")
    def test_windows_junction_resources_and_root_aliases_are_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "private.bin").write_bytes(b"Synthetic external bytes")
        script = self.base / "junction.ps1"
        script.write_text("param([string]$linkPath, [string]$targetPath)\n"
                          "New-Item -ItemType Junction -Path $linkPath -Target $targetPath -ErrorAction Stop | Out-Null\n",
                          encoding="utf-8")
        linked, alias = self.skill / "linked", self.base / "root-alias"
        for path, target in ((linked, outside), (alias, self.skill)):
            result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                                     "-File", str(script), str(path), str(target)], capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.addCleanup(path.rmdir)  # Remove only this junction; never recurse into its target.
        self.assertFalse(linked.is_symlink(), "Exercise a junction rather than the existing symlink check")
        result = self.check()
        self.assertFalse(result["pass"])
        self.assertNotIn("linked/private.bin", {item["path"] for item in result["files"]})
        with self.assertRaises(ValueError):
            packager.package_skill(self.skill, self.base / "dist", self.creator)
        with self.assertRaisesRegex(ValueError, "junction"):
            validator.skill_paths([str(alias)])
        with patch.object(validator.subprocess, "run", side_effect=AssertionError("Read a root junction before rejection")):
            self.assertFalse(validator.validate_skill(alias, self.creator)["pass"])
            with self.assertRaises(ValueError):
                packager.package_skill(alias, self.base / "dist", self.creator)
        self.assertEqual((outside / "private.bin").read_bytes(), b"Synthetic external bytes")
        self.assertFalse((self.base / "dist").exists())

    def test_archive_contains_exact_source_and_notice(self):
        result = packager.package_skill(self.skill, self.base / "dist", self.creator)
        with zipfile.ZipFile(self.base / "dist/example-skill.zip") as archive:
            self.assertEqual(set(archive.namelist()), {"example-skill/" + item["path"] for item in self.check()["files"]})
            self.assertEqual(archive.read("example-skill/LICENSE"), (self.skill / "LICENSE").read_bytes())
            self.assertEqual(archive.read("example-skill/references/details.md"), (self.skill / "references/details.md").read_bytes())
        self.assertEqual(result["files"], 3)
        with self.assertRaises(FileExistsError):
            packager.package_skill(self.skill, self.base / "dist", self.creator)

    def test_archive_cannot_be_created_inside_source(self):
        with self.assertRaises(ValueError):
            packager.package_skill(self.skill, self.skill / "dist", self.creator)
        self.assertFalse((self.skill / "dist").exists())


class EvaluationUtilities(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        self.case = next(case for case in cases if case["id"] == "p02-invoice-edit")

    def test_prepare_default_never_launches_codex(self):
        with patch.object(runner, "execute", side_effect=AssertionError("Unexpected model call")), redirect_stdout(io.StringIO()):
            code = runner.main(["--case", self.case["id"], "--run-root", str(self.base)])
        self.assertEqual(code, 0)
        meta = json.loads((self.base / "p02-invoice-edit-skill-v1/metadata.json").read_text(encoding="utf-8"))
        self.assertFalse(meta["executed"])
        self.assertIn("workspace-write", meta["command"])
        self.assertNotIn("danger-full-access", meta["command"])
        self.assertNotIn("--model", meta["command"])

    def test_baseline_does_not_copy_target_skill(self):
        prepared = runner.prepare(self.case, "baseline", "baseline", self.base)
        workspace = Path(prepared["metadata"]["workspace"])
        self.assertTrue((workspace / "service.py").is_file())
        self.assertFalse((workspace / ".agents/skills/api-design-engineering").exists())
        self.assertNotIn("enabled=true", " ".join(prepared["metadata"]["command"]))
        self.assertNotIn("rubric", prepared["prompt"].split("\n\n", 1)[-1])

    def test_unsafe_run_identifiers_and_reuse_rejected(self):
        for value in ("../escape", "x/y", "x\\y", ".", "a" * 65):
            with self.subTest(value=value), self.assertRaises(Exception):
                runner.prepare(self.case, "skill", value, self.base)
        runner.prepare(self.case, "skill", "fresh", self.base)
        with self.assertRaises(FileExistsError):
            runner.prepare(self.case, "skill", "fresh", self.base)

    def test_review_uses_read_only_sandbox(self):
        case = dict(self.case, id="review-case", mode="review")
        prepared = runner.prepare(case, "skill", "review", self.base)
        self.assertIn("read-only", prepared["metadata"]["command"])

    def test_all_cases_prepare_and_include_negative_activation_probes(self):
        cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        self.assertTrue(any(case.get("trigger") is False for case in cases))
        for case in cases:
            with self.subTest(case=case["id"]):
                prepared = runner.prepare(case, "skill", "corpus", self.base)
                self.assertFalse(prepared["metadata"]["executed"])
                self.assertTrue((Path(prepared["metadata"]["workspace"]) / ".agents/skills" / case["skill"] / "SKILL.md").is_file())

    def test_timeout_stops_owned_process(self):
        port_file = self.base / "port.txt"
        script = ("import pathlib,socket,time; s=socket.socket(); s.bind(('127.0.0.1',0)); "
                  "s.listen(); pathlib.Path(__import__('sys').argv[1]).write_text(str(s.getsockname()[1])); time.sleep(30)")
        prepared = {"output": self.base, "prompt": "", "metadata": {
            "command": [sys.executable, "-c", script, str(port_file)]}}
        self.assertEqual(runner.execute(prepared, 2), 124)
        self.assertTrue(port_file.exists(), "Child did not reach readiness before the deadline")
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", int(port_file.read_text())))
        self.assertEqual(prepared["metadata"]["exit_code"], 124)

    def test_preserved_holdout_detects_known_fixture_defect(self):
        result = subprocess.run([sys.executable, str(ROOT / "evals/verify_implementation.py"),
                                 "invoice", str(ROOT / "evals/fixtures/invoice"),
                                 "--pattern", "test_tenant_and_object_permissions_have_no_effects"],
                                capture_output=True, text=True, timeout=20)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('"tests": 1', result.stdout)
        self.assertIn('"failures": 1', result.stdout)
        self.assertIn('"errors": 0', result.stdout)

    def test_checker_closes_secondary_database_connections_even_on_failure(self):
        # Keep real SQLite connections alive so garbage collection cannot hide leaks.
        wrapper = """
import runpy, sqlite3, sys
original_connect = sqlite3.connect
connections = []
class TrackedConnection(sqlite3.Connection):
    closed = False
    def close(self):
        super().close()
        self.closed = True
def connect(*args, **kwargs):
    kwargs.setdefault('factory', TrackedConnection)
    connection = original_connect(*args, **kwargs)
    connections.append(connection)
    return connection
sqlite3.connect = connect
checker, fixture = sys.argv[1:]
sys.argv = [checker, 'reservation', fixture, '--pattern', 'test_replay_after_connection_restart']
try:
    runpy.run_path(checker, run_name='__main__')
except SystemExit:
    pass  # The unmodified fixture is intentionally defective.
leaks = [connection for connection in connections if not connection.closed]
for connection in leaks:
    connection.close()
assert len(connections) >= 2, 'Did not exercise the secondary connection'
assert not leaks, 'Checker left a database connection open'
"""
        result = subprocess.run([sys.executable, "-c", wrapper,
                                 str(ROOT / "evals/verify_implementation.py"),
                                 str(ROOT / "evals/fixtures/reservation")],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
