# Codex Engineering Skills

A collection of 17 reusable [Agent Skills](https://agentskills.io/specification) for engineering software with Codex. Each skill provides a focused workflow, decision boundaries, and selectively loaded references. The collection covers application development, data systems, security, reliability, research, testing, and engineering coordination.

The guiding approach is to inspect the actual project, research consequential uncertainties, preserve suitable existing systems, choose the simplest sound change, and verify observable behavior. These skills support engineering judgment; they do not guarantee security, correctness, or production readiness.

**Navigate:** [Catalog](#skill-catalog) · [Install](#installation) · [Use](#using-the-skills) · [Validate](#validation) · [Contribute](CONTRIBUTING.md) · [Inventory](docs/inventory.md) · [Releases](docs/releases.md) · [Governance](docs/governance.md) · [Evidence](docs/distribution-verification.md) · [Historical work report](docs/work-completion-report.md)

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

Consumers need **Node.js 22.20+ and npm/npx** for the tested Skills CLI. Python is only for maintainers. This repository is public; skill installation needs no GitHub account or token.

Browse the collection without installing:

```sh
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --list
```

For a **fresh** global Codex installation, install one skill or the complete collection:

```sh
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --skill redis-production-engineering -a codex -g --copy --yes
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --skill '*' -a codex -g --copy --yes
npx --yes skills@1.7.4 list -g -a codex
```

> **Existing installations need backup and review first.** Skills CLI 1.7.4 can replace manual or modified same-name folders. Its `check` command is mutating, and unsupported `--dry-run`/`--check` flags do not make it read-only. Do not run it as a harmless update probe.

Read the [installation and update guide](docs/installing-and-updating.md) for selected/multiple/all updates, read-only release comparisons, tracking metadata, Windows copy/link behavior, safe replacement, removal, and recovery. Published CLI behavior was verified against its source and disposable installations; upstream `main` may contain unreleased differences.

For a stable source, select an existing tag from [Releases](https://github.com/lofingoindia/codex-engineering-skills/releases) and use `"lofingoindia/codex-engineering-skills#REF"`. A full commit also works. `@NAME` selects a skill, not a release. Pinned refs remain pinned on update; a new release does not update installed skills automatically. See [versioning and releases](docs/releases.md).

The tested CLI installs global Codex skills into `~/.agents/skills`. Some older Codex installers/manual installations use `~/.codex/skills`; check your host, back up local changes, and avoid duplicate same-name installations. These commands do not migrate the older directory. For project scope, omit `-g` from a new project-root installation. Refresh discovery as required by the host.

The built-in Codex `$skill-installer` remains an alternative for installing a selected GitHub skill directory. Follow that installed tool's own supported destination and collision behavior; it has separate tracking from the Skills CLI.

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

Using the skills requires a Codex host that supports Agent Skills. The installation path above additionally uses Node/npm; the Markdown skills themselves have no Python runtime dependency. Maintaining this repository requires **Git and Python 3.11+ with pip/venv**, plus the pinned development dependency in `requirements-dev.txt`. The configured CI matrix uses Python 3.13 on Windows, Ubuntu, and macOS; actual execution evidence is recorded separately. Project-specific frameworks are needed only when working on the relevant application, not to validate this collection.

After the [development setup](CONTRIBUTING.md#development-setup):

```sh
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/package_skills.py --output-dir dist/review-1
python scripts/release_manifest.py --ref HEAD --package-dir dist/review-1 --json-output .runs/release-manifest.json
```

Validation reuses OpenAI's external skill-creator validator, then checks names, local Markdown resource paths, case portability, optional UI metadata, unfinished scaffolds, and bundled Python syntax. Packaging validates first, verifies ZIP contents against source bytes, and refuses to overwrite existing archives. `dist/` is ignored; use a fresh `--output-dir` for another packaging run.

To validate one repository skill, pass its name or directory; use an explicit path for installed copies:

```sh
python scripts/validate_skills.py go-backend-engineering
python scripts/validate_skills.py /path/to/user-skills/go-backend-engineering
```

The upstream validator must be available; it is not copied into this repository. See [setup and limitations](CONTRIBUTING.md). These commands establish packaging and structural validity, not engineering quality or automatic activation. Optional [evaluation utilities](evals/README.md) preserve selected discovery, activation, review, and implementation scenarios; preparing a case does not launch a model. Normal CI runs no paid/model evaluations.

## Repository layout

```text
skills/             Self-contained installable skills
scripts/            Validation and packaging entry points
tests/              Focused tooling regression tests
evals/              Optional cases, synthetic fixtures, and runner
docs/               Installation, releases, governance, and dated evidence
.github/            CI, dependency updates, issue forms, and PR template
AGENTS.md           Instructions for agents maintaining this collection
CONTRIBUTING.md     Setup, development, validation, and review workflow
SECURITY.md         Private reporting and security maintenance policy
```

## Maintenance and feedback

See [CONTRIBUTING.md](CONTRIBUTING.md) before adding or changing a skill. Keep activation boundaries precise, references selective, examples portable, and claims backed by appropriate evidence. Review upstream changes against actual versions rather than silently changing project architectures.

Report reproducible problems through [GitHub issues](https://github.com/lofingoindia/codex-engineering-skills/issues), including the skill name, commit, host version, expected behavior, and redacted evidence. Report possible credential exposure privately to a repository maintainer through an existing private channel; do not place secrets in an issue or public evaluation trace.

## License

Original skills, synthetic fixtures, and tooling are licensed under [MIT](LICENSE), allowing reuse, modification, and redistribution with the notice retained. Each skill includes its own notice for individual installation. Linked documentation and external tools retain their respective licenses; this repository does not relicense them. This is an independently maintained collection, not an official OpenAI product.
