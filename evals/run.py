#!/usr/bin/env python3
"""Prepare one disposable skill case; --execute explicitly opts into a Codex run.

Consolidates the original API/PostgreSQL/discovery runners. No fixed model,
personal paths, global-config writes or sandbox bypass. See evals/README.md.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SUITE = Path(__file__).resolve().parent


def identifier(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", value):
        raise argparse.ArgumentTypeError("Use a short identifier containing letters, numbers, underscores or hyphens")
    return value


def prepare(case: dict, condition: str, label: str, run_root: Path, model: str | None = None) -> dict:
    if condition not in ("skill", "baseline") or case["mode"] not in ("review", "implementation", "discovery"):
        raise ValueError("Unsupported evaluation condition or mode")
    for value in (case["id"], case["skill"], label):
        identifier(value)
    run_root = run_root.resolve()
    out = run_root / f"{case['id']}-{condition}-{label}"
    out.mkdir(parents=True, exist_ok=False)
    workspace = out / "workspace"
    workspace.mkdir()
    if "fixture" in case:
        identifier(case["fixture"])
        source = SUITE / "fixtures" / case["fixture"]
        shutil.copytree(source, workspace, dirs_exist_ok=True)
    # A nested repository bounds repository-scoped instruction discovery.
    subprocess.run(["git", "init", "--quiet", str(workspace)], check=True, capture_output=True)
    skill = ROOT / "skills" / case["skill"]
    if not (skill / "SKILL.md").is_file():
        raise ValueError("Case references an unavailable skill")
    selected = workspace / ".agents/skills" / case["skill"]
    if condition == "skill":
        shutil.copytree(skill, selected)
    prompt = case["prompt"]
    if condition == "baseline":
        prompt = prompt.replace(f"Use ${case['skill']} to ", "")
    if case["mode"] != "discovery":
        scope = ("This is a disposable fixture. Work only in this workspace; do not change global files, "
                 "access real services/credentials, or inspect the parent corpus, rubric or other runs. "
                 "You may read the selected local skill and relevant official public documentation. ")
        if case["mode"] == "review":
            scope += "Review only; do not create or modify files. Answer in at most 550 words. "
        else:
            scope += "Make and verify the requested changes. Report actual checks and limits. "
        prompt = scope + "\n\n" + prompt
    (out / "prompt.txt").write_text(prompt, encoding="utf-8")
    # Disable common duplicate installations for this invocation only, in BOTH arms.
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    duplicates = {codex_home / "skills" / case["skill"] / "SKILL.md",
                  Path.home() / ".codex/skills" / case["skill"] / "SKILL.md",
                  Path.home() / ".agents/skills" / case["skill"] / "SKILL.md"}
    entries = ["{path=" + json.dumps(path.as_posix()) + ",enabled=false}" for path in sorted(duplicates)]
    entries.append("{path=" + json.dumps((selected / "SKILL.md").as_posix()) +
                   ",enabled=" + ("true" if condition == "skill" else "false") + "}")
    sandbox = "workspace-write" if case["mode"] == "implementation" else "read-only"
    command = ["codex", "exec", "--ignore-user-config", "--ephemeral", "--sandbox", sandbox,
               "--skip-git-repo-check", "--json", "--cd", str(workspace),
               "--output-last-message", str(out / "answer.txt"),
               "-c", "approval_policy=\"never\"", "-c", "skills.config=[" + ",".join(entries) + "]"]
    if model:
        command += ["--model", model]
    command.append("-")
    metadata = {"case": case["id"], "condition": condition, "mode": case["mode"],
                "expected_trigger": case.get("trigger"), "executed": False,
                "model_requested": model, "workspace": str(workspace),
                "skill_sha256": hashlib.sha256((skill / "SKILL.md").read_bytes()).hexdigest(),
                "command": command}
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return {"output": out, "prompt": prompt, "metadata": metadata}


def stop_owned_process(process):
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, timeout=10)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def execute(prepared: dict, timeout: int) -> int:
    out, metadata = prepared["output"], prepared["metadata"]
    options = {"start_new_session": True} if os.name != "nt" else {
        "creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW}
    started = time.monotonic()
    with (out / "trace.jsonl").open("w", encoding="utf-8") as stdout, (out / "stderr.txt").open("w", encoding="utf-8") as stderr:
        process = subprocess.Popen(metadata["command"], stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                   text=True, encoding="utf-8", **options)
        try:
            process.communicate(prepared["prompt"], timeout=timeout)
            code = process.returncode
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            try:
                stop_owned_process(process)
            finally:
                if process.poll() is None:
                    process.kill()
                process.communicate()
            code = 124
    metadata.update({"executed": True, "exit_code": code,
                     "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                     "elapsed_seconds": round(time.monotonic() - started, 2)})
    for line in (out / "trace.jsonl").read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed":
            metadata["usage"] = event.get("usage")
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return code


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=identifier)
    parser.add_argument("--condition", choices=["skill", "baseline"], default="skill")
    parser.add_argument("--label", type=identifier, default="v1")
    parser.add_argument("--run-root", type=Path, default=ROOT / ".runs/evals")
    parser.add_argument("--model", help="Optional exact model ID; otherwise uses the CLI's supported default")
    parser.add_argument("--execute", action="store_true", help="Explicitly launch Codex; may incur usage/cost")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)
    cases = json.loads((SUITE / "cases.json").read_text(encoding="utf-8"))
    if args.list:
        for case in cases:
            print(f"{case['id']}: {case['mode']} / {case['skill']} / expected trigger={case.get('trigger')}")
        return 0
    if not args.case or args.timeout <= 0:
        parser.error("Provide --case and a positive --timeout")
    case = next((case for case in cases if case["id"] == args.case), None)
    if not case:
        parser.error("Unknown case; use --list")
    try:
        prepared = prepare(case, args.condition, args.label, args.run_root, args.model)
        print(f"Prepared {case['id']} ({args.condition}); output: {prepared['output']}", flush=True)
        if args.execute:
            return execute(prepared, args.timeout)
        print("Codex was NOT launched. Review the prompt/metadata before using --execute.")
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        parser.exit(2, f"Evaluation could not complete: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
