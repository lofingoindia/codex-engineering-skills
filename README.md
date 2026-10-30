# Codex Engineering Skills

A collection of 17 reusable [Agent Skills](https://agentskills.io/specification) for engineering software with Codex. Each skill provides a focused workflow, decision boundaries, and selectively loaded references. The collection covers application development, data systems, security, reliability, research, testing, and engineering coordination.

The guiding approach is to inspect the actual project, research consequential uncertainties, preserve suitable existing systems, choose the simplest sound change, and verify observable behavior. These skills support engineering judgment; they do not guarantee security, correctness, or production readiness.

**Navigate:** [Catalog](#skill-catalog) · [Install](#installation) · [Use](#using-the-skills) · [Validate](#validation) · [Contribute](CONTRIBUTING.md) · [Inventory](docs/inventory.md)

## Skill catalog

Every directory below is independently installable and includes its own `SKILL.md`, Codex UI metadata, references, and license notice.

| Skill | Responsibility |
| --- | --- |
| [api-design-engineering](skills/api-design-engineering/) | API contracts, HTTP behavior, compatibility, authorization, and service integration. |
| [deep-readonly-system-audit](skills/deep-readonly-system-audit/) | Evidence-driven architecture, security, correctness, and reliability audits with an authorized report. |
| [distributed-systems-reliability](skills/distributed-systems-reliability/) | Partial failure, idempotency, delivery semantics, concurrency, and recovery across system boundaries. |
| [engineering-research-intelligence](skills/engineering-research-intelligence/) | Version-aware upstream research and source-code study applied to the existing project. |
| [flutter-app-engineering](skills/flutter-app-engineering/) | Flutter/Dart application architecture, state, networking, UX, security, and release reliability. |
| [go-backend-engineering](skills/go-backend-engineering/) | Go services and workers, concurrency, contexts, integrations, resource ownership, and recovery. |
| [multi-tenant-access-control](skills/multi-tenant-access-control/) | Tenant isolation, authorization, memberships, administrative access, workers, and caches. |
| [nextjs-fullstack-engineering](skills/nextjs-fullstack-engineering/) | Next.js websites and SaaS applications, rendering, routing, caching, security, and deployment. |
| [nodejs-backend-engineering](skills/nodejs-backend-engineering/) | Node.js services and workers, runtime behavior, asynchronous execution, security, and reliability. |
| [postgresql-data-engineering](skills/postgresql-data-engineering/) | PostgreSQL schemas, queries, transactions, migrations, pooling, security, and recovery. |
| [react-vite-dashboard-engineering](skills/react-vite-dashboard-engineering/) | React + Vite dashboards, loading states, API efficiency, routing, accessibility, and performance. |
| [real-world-test-engineering](skills/real-world-test-engineering/) | Failure discovery and behavior-focused unit, component, integration, and contract testing. |
| [redis-production-engineering](skills/redis-production-engineering/) | Redis application and infrastructure decisions, atomic state, caching, isolation, and recovery. |
| [repository-structure-engineering](skills/repository-structure-engineering/) | File ownership, modules, package boundaries, sharing, and safe repository restructuring. |
| [saas-security-engineering](skills/saas-security-engineering/) | SaaS authentication, sessions, input handling, secrets, integrations, and abuse resistance. |
| [task-subagent-orchestration](skills/task-subagent-orchestration/) | Proportional planning, skill selection, useful delegation, integration, and task reporting. |
| [universal-database-engineering](skills/universal-database-engineering/) | Workload-driven data modeling, integrity, database selection, indexing, and schema evolution. |

## Installation

### Install an individual skill

In Codex, ask the built-in installer:

```text
Use $skill-installer to install the skill at
https://github.com/lofingoindia/codex-engineering-skills/tree/main/skills/go-backend-engineering
```

Replace the last directory with a catalog entry. While this repository is private, your GitHub account and Git credentials must have access. Use the installer's supported authentication; never paste credentials into prompts or commit them. To reproduce a particular version, use a commit SHA in place of `main`.

The installer supplied with the migration environment installs to `$CODEX_HOME/skills` (normally `~/.codex/skills`) and refuses an existing destination. [Current Codex documentation](https://learn.chatgpt.com/docs/build-skills) describes user skills in `~/.agents/skills` and repository skills in `.agents/skills`. Discovery paths depend on the installed Codex/installer version. Check your host's instructions and installation result; avoid installing duplicate copies of the same name into both user directories. The migration preserved the working global installations in their original directory.

### Install the collection manually

Clone the repository, then copy each desired **complete skill directory**, including its `LICENSE`, into your host's supported user skills directory. There is no runtime dependency on this repository or its sibling skills.

This PowerShell example uses the current documented user directory and checks **all** name conflicts before copying anything:

```powershell
git clone https://github.com/lofingoindia/codex-engineering-skills.git
Set-Location codex-engineering-skills
$skillDestination = Join-Path $HOME '.agents/skills' # Adjust for your Codex host.
$sourceSkills = @(Get-ChildItem -LiteralPath ./skills -Directory)
$conflicts = @($sourceSkills | Where-Object {
    Test-Path -LiteralPath (Join-Path $skillDestination $_.Name)
})
if ($conflicts.Count) { throw "Existing skills: $($conflicts.Name -join ', ')" }
New-Item -ItemType Directory -Path $skillDestination -Force | Out-Null
foreach ($skill in $sourceSkills) {
    Copy-Item -LiteralPath $skill.FullName -Destination $skillDestination -Recurse -ErrorAction Stop
}
```

On macOS/Linux, the equivalent operation is to copy complete selected folders to the supported user directory after checking for collisions. For repository-local installation, copy selected folders to `.agents/skills/` in that project instead. Check whether those copies should be committed with that project's maintainers.

Use a new Codex turn/session to refresh discovery as required by your host. Updates are deliberate: review changes, back up local modifications, and replace the selected installation. Pulling this source repository does not update installed copies automatically.

## Using the skills

Invoke a skill explicitly with `$` and its name, or let Codex select one from its activation description:

```text
Use $postgresql-data-engineering to investigate concurrent updates in our order workflow.
Inspect our existing schema and tests before proposing changes.
```

```text
Use $real-world-test-engineering to reproduce this bug and add a focused regression test.
```

Load only skills relevant to the task. Specialist implementation skills complement research, testing, and orchestration without requiring every skill on every request. Repository instructions, user scope, and read-only boundaries still apply. Subagent capabilities, browser/device access, network access, and service integrations depend on the host; skill installation does not supply those capabilities.

## Validation

Using the skills requires a Codex host that supports Agent Skills. Maintaining this repository additionally requires **Git and Python 3.11+ with pip/venv**, plus the pinned development dependency in `requirements-dev.txt`. CI uses Python 3.13 on Windows and Ubuntu. Project-specific frameworks are needed only when working on the relevant application, not to validate this collection.

After the [development setup](CONTRIBUTING.md#development-setup):

```sh
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/package_skills.py
```

Validation reuses OpenAI's external skill-creator validator, then checks names, local Markdown resource paths, case portability, optional UI metadata, unfinished scaffolds, and bundled Python syntax. Packaging validates first, verifies ZIP contents against source bytes, and refuses to overwrite existing archives. `dist/` is ignored; use a fresh `--output-dir` for another packaging run.

To validate one repository or installed copy, pass its directory:

```sh
python scripts/validate_skills.py skills/go-backend-engineering
python scripts/validate_skills.py /path/to/user-skills/go-backend-engineering
```

The upstream validator must be available; it is not copied into this repository. See [setup and limitations](CONTRIBUTING.md). These commands establish packaging and structural validity, not engineering quality or automatic activation. Optional [evaluation utilities](evals/README.md) preserve selected discovery, activation, review, and implementation scenarios; preparing a case does not launch a model. Normal CI runs no paid/model evaluations.

## Repository layout

```text
skills/             Self-contained installable skills
scripts/            Validation and packaging entry points
tests/              Focused tooling regression tests
evals/              Optional cases, synthetic fixtures, and runner
docs/               Migration inventory, source hashes, verification record
.github/workflows/  Windows/Linux validation
AGENTS.md           Instructions for agents maintaining this collection
CONTRIBUTING.md     Setup, development, validation, and review workflow
```

## Maintenance and feedback

See [CONTRIBUTING.md](CONTRIBUTING.md) before adding or changing a skill. Keep activation boundaries precise, references selective, examples portable, and claims backed by appropriate evidence. Review upstream changes against actual versions rather than silently changing project architectures.

Report reproducible problems through [GitHub issues](https://github.com/lofingoindia/codex-engineering-skills/issues), including the skill name, commit, host version, expected behavior, and redacted evidence. Report possible credential exposure privately to a repository maintainer through an existing private channel; do not place secrets in an issue or public evaluation trace.

## License

Original skills, synthetic fixtures, and tooling are licensed under [MIT](LICENSE), allowing reuse, modification, and redistribution with the notice retained. Each skill includes its own notice for individual installation. Linked documentation and external tools retain their respective licenses; this repository does not relicense them. This is an independently maintained collection, not an official OpenAI product.
