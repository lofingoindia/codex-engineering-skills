# Optional skill evaluations

These utilities preserve useful custom evaluation work without making ordinary validation expensive. They are not required to install a skill. No model evaluation runs in CI or during default preparation.

## Contents and provenance

- `cases.json`: 13 preserved API scenarios, one PostgreSQL review scenario, and two metadata discovery probes adapted from the original session helpers. API cases include positive and negative activation expectations plus review and implementation rubrics.
- `fixtures/invoice` and `fixtures/reservation`: synthetic Python/SQLite applications with deliberately incomplete tests and known authorization/concurrency/idempotency defects.
- `fixtures/postgresql-review`: synthetic schema and caller for read-only PostgreSQL review; no live database is configured or contacted by preparation.
- `verify_implementation.py`: preserved behavioral checks for changed invoice/reservation artifacts, with bounded worker cleanup, explicit database connection closure, and optional test selection.
- `run.py`: one consolidated runner replacing overlapping discovery/API/PostgreSQL helpers. It has no fixed model, personal paths, sandbox bypass, or global configuration writes.

Fixture source bytes were retained. Deliberate defects are evaluation input, not production examples. Do not fix the committed fixtures or treat their existing passing tests as proof of correctness.

## Prepare before executing

Requires Git and Python 3.11+. Execution also requires a compatible authenticated Codex CLI. Check `codex exec --help` if your CLI version differs.

```sh
python evals/run.py --list
python evals/run.py --case p02-invoice-edit --label inspection
python evals/run.py --case p02-invoice-edit --condition baseline --label inspection
```

Preparation creates a fresh `.runs/evals/<case>-<condition>-<label>/` containing the prompt, command/metadata, and disposable workspace. Existing output is never overwritten. It initializes a nested Git repository to bound project instruction discovery. The skill condition copies only the target package into workspace `.agents/skills/`; the baseline does not. Review both generated prompts and commands.

An actual model run requires the separate, explicit opt-in and a fresh label:

```sh
python evals/run.py --case p02-invoice-edit --label trial-1 --execute --timeout 300
python evals/run.py --case p02-invoice-edit --condition baseline --label trial-1 --execute --timeout 300
```

Add `--model EXACT_SUPPORTED_ID` only if you need an explicit model; otherwise the CLI selects its supported default. Review/discovery runs request a read-only sandbox; implementation requests workspace-write. Commands set `approval_policy="never"` within that sandbox and use no sandbox bypass. On timeout/interruption the runner attempts to terminate its owned process group/tree and records exit code 124. It does not terminate unrelated processes or manage external services.

Use an isolated environment for untrusted code. A Codex sandbox and scope prompt are not a VM or secret-store boundary. The local host may still supply credentials, network access, other skills, or tools. Rubrics live outside the workspace but are not cryptographically hidden or inaccessible by guarantee. Do not use real credentials or production services. Raw outputs are ignored because they can contain sensitive context.

## Inspect outcomes honestly

`metadata.json` records the requested condition, target SKILL hash, command, execution status, elapsed time, exit code, and token usage only when the CLI reports it. A prepared case has `executed: false`. A zero process exit alone is not a behavioral PASS.

Inspect `answer.txt`, `trace.jsonl`, changes, and actual test evidence. For implicit activation probes, verify actual tool/file reads and task applicability; self-reported skill use is insufficient. Metadata-only discovery verifies availability, not appropriate activation. Negative cases should avoid loading the irrelevant target. Normal tooling tests prepare all cases but do not establish these behavioral outcomes.

Common global copies of the target skill are disabled through **per-invocation** configuration in both arms. No installed file is edited. Other inherited skills, instructions, model variability, and host settings can still confound comparisons. Record model/CLI, relevant context, skill commit, repeated runs if justified, and unresolved confounders. Do not claim a measured improvement from these fixtures alone.

## Implementation checks

After a disposable implementation run, inspect and trust its code before executing it. The checker imports the artifact's `service.py` and executes subprocesses; it is not a safe loader for hostile code.

```sh
python evals/verify_implementation.py invoice .runs/evals/p02-invoice-edit-skill-trial-1/workspace
python evals/verify_implementation.py reservation .runs/evals/p03-reservation-skill-trial-1/workspace
```

Run the artifact's own tests as well. `--pattern TEST_METHOD_NAME` selects one held-out check. Unmodified fixtures are expected to fail meaningful checks. The SQLite concurrency checks use multiple processes and widen a scheduling window; they are stress regressions, not deterministic proof of all interleavings or PostgreSQL/MySQL semantics.

Keep generated workspaces, traces, answers, logs, archives, and timing/usage outputs out of Git. Published evidence should be a bounded, redacted account of what actually executed and what it established.
