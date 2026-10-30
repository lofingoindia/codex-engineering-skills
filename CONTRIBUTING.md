# Contributing

Skills should help an agent reason better about the existing project. Prefer focused workflows, clear activation boundaries, selective references, and evidence over rigid recipes or infrastructure.

## Development setup

Use Git and a standard Python 3.11+ installation with pip/venv. CI uses 3.13. Stripped embedded Python distributions may lack pip/venv or ignore `PYTHONPATH`; install a normal development interpreter for this workflow.

```sh
python -m venv .venv
```

Activate `.venv` with `.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` on macOS/Linux, then:

```sh
python -m pip install -r requirements-dev.txt
```

Validation calls OpenAI's **external** `quick_validate.py`. It first looks in `.tools/openai-skills`, then in the installed `$CODEX_HOME/skills/.system/skill-creator` (default `~/.codex`). To reproduce the CI dependency:

```sh
git clone https://github.com/openai/skills.git .tools/openai-skills
git -C .tools/openai-skills checkout 49f948faa9258a0c61caceaf225e179651397431
```

That upstream checkout is ignored and not distributed with this repository. Its license and instructions remain its own. Alternatively, pass your supported validator explicitly:

```sh
python scripts/validate_skills.py --creator-validator /path/to/quick_validate.py
```

Keep the CI upstream commit deliberate: review changed validation behavior before updating it. The pinned upstream validator is a practical baseline, not a complete implementation of every optional field allowed by the open specification. A valid specification extension may need an upstream update or a documented compatibility decision; do not silently bypass failures.

## Everyday checks

```sh
python scripts/validate_skills.py skills/api-design-engineering
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/package_skills.py skills/api-design-engineering --output-dir dist/review-1
```

Validation exits nonzero for invalid skills or an unavailable validator. An optional `--json-output .runs/validation.json` retains local evidence. Packaging verifies CRC, file inventory, and source bytes, and refuses existing ZIPs. Choose a fresh output directory for another run. Neither tool installs or changes global skills.

The local reference check recognizes inline Markdown links/images and reference definitions outside fenced examples. It checks file existence, containment, path case, and optional UI asset paths. It does not check remote URL availability, heading anchors, arbitrary prose paths, or every possible Markdown dialect. Bundled Python is parsed without execution; other script languages require documented native checks. These tools do not measure agent behavior or certify security.

## Adding or updating a skill

1. Check the catalog for an existing owner. Extend the appropriate skill when scope already fits; add a new one only for a distinct responsibility.
2. Use the available `skill-creator` workflow with output under `skills/`, or add a standards-compliant self-contained folder. Keep `SKILL.md` focused on decisions and actions. Add conditional references only when useful.
3. Add accurate `name` and `description` metadata, compatible `agents/openai.yaml`, and a copy of the root `LICENSE`. Preserve third-party notices if independently licensed material is legitimately included.
4. Inspect current primary documentation and relevant source/tests for technical claims. Link sources where they support the guidance, with version gates where needed.
5. Validate the changed package. Exercise script behavior and realistic decision boundaries where the change warrants it. Reuse existing fixtures/tooling; do not turn every guidance edit into a benchmark campaign.
6. Update the README catalog and any affected commands. Review the complete diff for unintended behavior changes, broken references, private information, and redistribution issues.

Do not regenerate the original migration manifest for normal changes. It records the imported snapshot; Git records later intentional changes. Package-relative resources must not require repository-level tooling at invocation time.

## Optional evaluations

See [evals/README.md](evals/README.md). Preparation is local and free of model calls. `--execute` deliberately starts Codex and can incur usage/cost. Review the fixture, prompt, command, sandbox, credentials, network permissions, and installed skill context first. Use a supported sandboxed environment and synthetic data. Agent evaluations are not part of normal CI.

Report observed results with the case, skill commit, model/host, conditions, actual checks, and limitations. A baseline comparison without equivalent context is not causal evidence. Do not commit raw traces, local paths, credentials, or generated agent changes.

## Pull requests and issue reports

Describe the concrete problem and resulting behavior, relevant research, and executed verification. Explain remaining limits honestly. Keep PRs focused, and preserve existing users' invocation names and sound conventions. CI validates on Windows and Ubuntu with read-only repository permissions and pinned dependencies/actions.

Report bugs with reproducible, redacted examples. Keep security-sensitive reports private through an existing maintainer contact. Never include real tokens, customer data, or internal infrastructure in fixtures or issues. Contributions to original collection content are submitted under the repository's MIT license unless clearly agreed otherwise.
