# Codex Engineering Skills: Complete Work Report and Repository Guide

| Report detail | Value |
| --- | --- |
| Prepared | 30 October 2026, Asia/Calcutta |
| Repository | [lofingoindia/codex-engineering-skills](https://github.com/lofingoindia/codex-engineering-skills) |
| Published consolidation commit | [`9cd5767b01ea7d898d547053d33f9e5b679e0d21`](https://github.com/lofingoindia/codex-engineering-skills/commit/9cd5767b01ea7d898d547053d33f9e5b679e0d21) |
| Default branch | `main` |
| Visibility at verification | Private; it was not changed. |

This report explains what was completed, where everything belongs, how to use and maintain the collection, and what the checks established. Its migration figures refer to the published consolidation commit above. This report and its README navigation link were added afterward as documentation; later revisions are recorded in Git history.

## 1. Outcome and status

The existing custom engineering skills were consolidated into one Git repository, documented, validated, committed, and pushed. Their working global installations were preserved. The repository contains reusable tooling and optional evaluation assets alongside the independently installable skill packages.

| Deliverable | Actual result |
| --- | --- |
| Custom skills discovered | **17** |
| Skills copied successfully | **17 of 17** |
| Missing or incomplete discovered skills | **None** |
| Original skill source files preserved | **133**, totaling **681,508 bytes** |
| Original supporting reference files | **99**, included in those 133 files |
| Additional package license notices | **17**, one per skill |
| Original synthetic fixture files preserved | **9** |
| Files in the published consolidation commit | **177** |
| Global installations | Original files unchanged; no relocation |
| Structural validation | **17 of 17 passed** |
| Tooling regression tests | **24 passed** on local Windows/Python 3.13 |
| Complete skill ZIP packages | **17 of 17 verified** |
| Optional evaluation cases | **16 prepared successfully** without model execution |
| GitHub publication | Pushed to existing `main`; remote file contents and modes matched local Git |
| Hosted Windows/Ubuntu CI | **Not executed:** account-level runner restriction prevented startup |

**Consolidation and publication: PASS. Overall verification: PARTIAL**, because hosted CI has not run. Structural and tooling success does not establish that every skill improves agent behavior, guarantees security, or makes an application production-ready.

## 2. How the work was carried out

| Task | Work completed | Evidence | Status |
| --- | --- | --- | --- |
| 1. Discover and investigate | Inspected the real user skill installation, creation workspace, existing tooling, local destination, remote repository, and relevant instructions. Distinguished custom content from system/plugin dependencies. | Inventory of 17 skills and 133 source files; remote confirmed empty, private, and using `main`. | PASS |
| 2. Establish and preserve | Connected the destination to the existing remote; copied complete packages into `skills/`; retained source names, metadata, references, and bytes. | SHA-256 comparisons against the original snapshot and global installations. | PASS |
| 3. Preserve useful tooling | Adapted validation and packaging helpers; consolidated optional evaluation runners; retained synthetic fixtures and semantic checks; added focused tooling tests and CI. | Structural checks, 24 final tests, and 17 verified ZIPs. | PASS |
| 4. Document and review | Created README, repository AGENTS, contribution instructions, provenance, verification record, and MIT notices. Reviewed public-content risks and corrected one inherited checker cleanup defect. | Local documentation links checked; content scans and independent read-only review; cleanup regression failed before the fix and passed afterward. | PASS |
| 5. Publish and verify | Committed and pushed the intended files; compared the GitHub tree with local paths, blob hashes, and file modes; checked branch synchronization and Actions. | All 177 published files matched; README and AGENTS accessible; local and remote `main` matched. Actions created no jobs because startup was restricted. | PARTIAL |

An independent read-only reviewer assisted with publication review. The lead retained implementation ownership, verified corrections, and performed integration and publication. No behavioral model-evaluation campaign was run during this consolidation.

## 3. Repository map: what each folder holds

```text
codex-engineering-skills/
├── README.md                         Collection overview and installation guide
├── AGENTS.md                         Instructions for agents maintaining this repository
├── CONTRIBUTING.md                   Contributor setup and change workflow
├── LICENSE                           MIT license for original collection content
├── requirements-dev.txt              Pinned Python development dependency
├── .gitignore                        Files that must stay out of version control
├── .gitattributes                    Portable text handling and imported-byte preservation
├── .github/
│   └── workflows/
│       └── validate.yml              Configured Windows/Ubuntu verification workflow
├── skills/
│   └── <skill-name>/                 One independent installable package per skill
│       ├── SKILL.md                  Activation metadata and primary workflow
│       ├── LICENSE                   License carried with individual installations
│       ├── agents/
│       │   └── openai.yaml           Codex display metadata
│       └── references/
│           └── *.md                 Selectively loaded engineering detail and sources
├── scripts/
│   ├── validate_skills.py            External upstream validation plus local checks
│   └── package_skills.py             Validated, byte-checked ZIP packaging
├── tests/
│   └── test_tooling.py               Regression tests for repository tooling
├── evals/
│   ├── README.md                     Optional evaluation usage and limitations
│   ├── cases.json                    Prompts, expected activation, and review rubrics
│   ├── run.py                        Prepare a case; explicitly opt into model execution
│   ├── verify_implementation.py      Behavioral checks for disposable changed fixtures
│   └── fixtures/
│       ├── invoice/                 Synthetic invoice API with known defects
│       ├── reservation/             Synthetic reservation workflow with known defects
│       └── postgresql-review/       Synthetic schema/caller for read-only review
└── docs/
    ├── inventory.md                  Imported package and tooling provenance
    ├── source-manifest.json          Historical source paths, byte sizes, and SHA-256s
    ├── verification.md               Executed migration checks and confidence limits
    └── work-completion-report.md     This end-to-end report and repository guide
```

### `skills/`: the actual installable content

This is the collection's main product. Each child directory is one skill that can be copied or installed separately. It carries the files needed for its own instructions and relative references. A selected skill does not need all the other skill folders installed beside it.

The current 17 packages contain Markdown instructions, YAML UI metadata, and license notices. They do not bundle application code, executable utilities, templates, or binary assets. Their references link to external technical sources rather than distributing an entire copied documentation library.

### `scripts/`: tools for maintaining the collection

These scripts validate and package skill directories. They are used by contributors and CI. Installing a skill does not require installing the repository's Python tooling into the target application.

### `tests/`: tests of the tools

These are focused automated tests of validators, packaging, evaluation preparation, cleanup, and preserved checker behavior. A passing test here establishes the tested tooling behavior. It does not mean all 17 skills underwent successful agent-behavior evaluations.

### `evals/`: optional evaluation material

This folder preserves reusable scenarios and deliberately defective synthetic applications. It supports future investigation of discovery, activation, engineering review, and implementation decisions. It is separate from ordinary validation because model runs can cost time and usage and require suitable isolation.

### `docs/`: evidence and explanations

Use [inventory.md](inventory.md) to understand what was imported and why particular tooling was retained. Use [source-manifest.json](source-manifest.json) for original file hashes. Use [verification.md](verification.md) for executed checks. This report combines those records with a practical guide to the repository.

### `.github/workflows/`: hosted automation

The workflow describes the intended Windows and Ubuntu verification jobs. It is committed and available on GitHub. Its first run was blocked before any job started; the configuration's presence must not be represented as a successful hosted test result.

## 4. The 17 skills and when to use them

The file counts below describe the current package layout at consolidation: original source files plus the added license notice. References are already included in each count.

| Skill directory | What it helps with | Typical request | Package files / references |
| --- | --- | --- | ---: |
| [api-design-engineering](../skills/api-design-engineering/) | API contracts, protocol selection, HTTP semantics, compatibility, authorization, and integration reliability. | Design an endpoint, review an API change, or fix retry behavior at an API boundary. | 8 / 5 |
| [deep-readonly-system-audit](../skills/deep-readonly-system-audit/) | Evidence-driven architecture, security, correctness, and reliability audits with an authorized report. | Audit a system without implementing fixes or changing the audited environment. | 6 / 3 |
| [distributed-systems-reliability](../skills/distributed-systems-reliability/) | Idempotency, delivery guarantees, partial failures, concurrency, and recovery across services and external effects. | Prevent duplicate work or repair recovery across a database, queue, worker, and provider. | 7 / 4 |
| [engineering-research-intelligence](../skills/engineering-research-intelligence/) | Version-aware upstream research, source/test study, and evidence applied to the actual codebase. | Investigate an unfamiliar API, production failure mechanism, or consequential tradeoff. | 10 / 7 |
| [flutter-app-engineering](../skills/flutter-app-engineering/) | Flutter/Dart architecture, state, lifecycles, API efficiency, navigation, smooth UX, security, and releases. | Fix duplicate fetching, a lifecycle bug, loading behavior, or native integration. | 11 / 8 |
| [go-backend-engineering](../skills/go-backend-engineering/) | Go services/workers, goroutines, contexts, HTTP, integrations, resource ownership, and shutdown. | Investigate goroutine leaks, cancellation, service throughput, or recovery. | 10 / 7 |
| [multi-tenant-access-control](../skills/multi-tenant-access-control/) | Tenant isolation, memberships, permissions, administrative access, workers, and caches. | Review cross-tenant access or implement a permission-sensitive workflow. | 7 / 4 |
| [nextjs-fullstack-engineering](../skills/nextjs-fullstack-engineering/) | Next.js public sites and authenticated SaaS, rendering, routing, fetching, caching, security, and deployment. | Fix stale data, improve navigation/loading, or review server/client boundaries. | 10 / 7 |
| [nodejs-backend-engineering](../skills/nodejs-backend-engineering/) | Node.js runtime/async behavior, integrations, security, streams, diagnostics, and process reliability. | Debug event-loop blocking, leaks, worker behavior, or graceful shutdown. | 9 / 6 |
| [postgresql-data-engineering](../skills/postgresql-data-engineering/) | PostgreSQL modeling, queries, indexes, transactions, migrations, pooling, security, and recovery. | Diagnose a transaction race, improve a query, or plan a safe migration. | 9 / 6 |
| [react-vite-dashboard-engineering](../skills/react-vite-dashboard-engineering/) | React + Vite dashboards, server state, authentication, routing, loading/recovery UX, accessibility, and performance. | Repair excess requests, a broken loading state, or permission-aware navigation. | 8 / 5 |
| [real-world-test-engineering](../skills/real-world-test-engineering/) | User-driven edge cases, meaningful assertions, test levels, integration boundaries, and reproducible verification. | Expose a bug with a regression test or improve shallow/flaky tests. | 10 / 7 |
| [redis-production-engineering](../skills/redis-production-engineering/) | Redis caching, atomic state, messaging, isolation, resource use, infrastructure, and recovery. | Review cache correctness, expiry, shared state, or an operational Redis problem. | 10 / 7 |
| [repository-structure-engineering](../skills/repository-structure-engineering/) | File ownership, module/package boundaries, sharing, polyglot layout, and safe restructuring. | Decide where code belongs or safely extract a shared package. | 11 / 8 |
| [saas-security-engineering](../skills/saas-security-engineering/) | Authentication, sessions, untrusted input, secrets, integrations, and abuse resistance. | Investigate a security issue or review a sensitive application change. | 7 / 4 |
| [task-subagent-orchestration](../skills/task-subagent-orchestration/) | Scope classification, proportional task planning, skill selection, useful delegation, integration, and reporting. | Coordinate a substantial change while keeping small work direct. | 7 / 4 |
| [universal-database-engineering](../skills/universal-database-engineering/) | Workload-driven data modeling, integrity, database architecture, indexing tradeoffs, and evolution. | Design a data model or compare database choices against a real workload. | 10 / 7 |

Related skills complement one another. For example, a PostgreSQL tenant-isolation fix may involve the PostgreSQL, access-control, and testing skills. That does not require loading unrelated frontend or mobile guidance. Their activation descriptions define their narrower boundaries.

## 5. What the files inside each skill do

| File or directory | Responsibility | When to change it |
| --- | --- | --- |
| `SKILL.md` | YAML frontmatter supplies `name` and `description`; the body provides the primary actionable workflow and routes to references. | Change activation, responsibilities, decision boundaries, or the main workflow. |
| `agents/openai.yaml` | Codex-facing display metadata, including a human-readable name and short description. | Update how the skill is presented or supported optional host metadata. |
| `references/*.md` | Detailed engineering guidance, examples, tradeoffs, and authoritative source links loaded when relevant. | Improve a specific technical topic without bloating the main workflow. |
| `LICENSE` | Carries the MIT notice with an independently installed/copied package. | Retain it when redistributing; change terms only with appropriate authorization. |

The package name and its `SKILL.md` name must agree. Local resources must use correct-case relative paths and stay inside the package. Copying only `SKILL.md` would lose the supporting references and legal notice.

## 6. Validation and packaging tools

### `scripts/validate_skills.py`

The validator accepts one or more skill directory paths, or checks all repository skills when none are supplied. It reuses OpenAI's external `quick_validate.py`, then performs repository-specific resource checks.

It checks upstream metadata validity; directory/name agreement; a nonempty description; local inline/reference-style Markdown links outside fenced examples; path containment and case; optional UI metadata and local icon targets; unfinished creator scaffolds; and bundled Python syntax. It records file byte sizes and SHA-256s in optional JSON evidence. Symlink resources inside packages are rejected in favor of materialized portable resources.

It does not fetch every external URL, validate heading anchors, recognize every Markdown dialect, execute arbitrary bundled scripts, or judge the quality of engineering advice. Non-Python scripts need their own documented native checks.

```sh
# All skills
python scripts/validate_skills.py

# One skill
python scripts/validate_skills.py skills/go-backend-engineering

# Save local evidence
python scripts/validate_skills.py --json-output .runs/validation.json

# Select an externally installed upstream validator explicitly
python scripts/validate_skills.py --creator-validator /path/to/quick_validate.py
```

Exit code `0` means selected packages passed; `1` means validation found an invalid package; `2` means the validation operation could not complete, such as an unavailable upstream dependency.

### `scripts/package_skills.py`

Packaging validates each selected skill first, then writes a ZIP containing the entire package under its skill-name directory. It checks archive CRC, file count, and every archived file against source bytes, then prints a SHA-256 of the archive. It refuses existing ZIPs and an output location inside the source skill.

```sh
# All packages, using a fresh output directory
python scripts/package_skills.py --output-dir dist/review-1

# One package
python scripts/package_skills.py skills/go-backend-engineering --output-dir dist/go-review-1
```

The default output directory is `dist/`. A repeat run must use a fresh destination if ZIPs with the same names already exist. Archives are ignored build artifacts, not automatically uploaded releases or installed skills.

### Upstream dependency and setup

Use a standard Python 3.11+ development installation with pip/venv, plus Git. CI is configured for Python 3.13. `requirements-dev.txt` pins `PyYAML==6.0.3`.

```sh
python -m venv .venv
```

Activate `.venv` using `.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` on macOS/Linux, then:

```sh
python -m pip install -r requirements-dev.txt
git clone https://github.com/openai/skills.git .tools/openai-skills
git -C .tools/openai-skills checkout 49f948faa9258a0c61caceaf225e179651397431
```

The validator first looks in this ignored upstream checkout, then in the installed `$CODEX_HOME/skills/.system/skill-creator` location, defaulting to `~/.codex`. The upstream tool is an external dependency; it was not copied into the published repository. The pinned validator is a baseline with documented limitations around optional specification fields.

The migration machine had a stripped embedded Python without normal pip/venv support. Verification used an ignored local runtime copy and checksum-verified PyYAML cache. That workaround did not change the original interpreter or global configuration and is not required in a standard development environment.

## 7. Tests and the bug found during review

Run the maintained tooling suite with:

```sh
python -m unittest discover -s tests -v
```

The final migration run completed **24 tests successfully**. These cover valid and invalid skill metadata, missing resources, encoded path escapes, file URIs, incorrect path case, optional UI policy, missing icons, Python syntax without execution, duplicate selections, archive contents and no-overwrite behavior, safe evaluation identifiers, baseline preparation, review sandbox selection, preparation of the entire case corpus, owned-process timeout cleanup, and preserved defect-checker behavior.

One inherited problem was found in the optional checker. It opened a secondary SQLite connection using the connection's transaction context manager without explicitly closing it. Python's [SQLite documentation](https://docs.python.org/3.13/library/sqlite3.html#how-to-use-the-connection-context-manager) distinguishes transaction handling from closing a connection. This could leave a resource open during temporary-directory cleanup on Windows.

A focused regression retained real SQLite connections so garbage collection could not hide the leak. It failed against the inherited behavior. The checker was corrected to close the connection explicitly while retaining transaction-context behavior. The regression and full tooling suite then passed. The deliberately defective application fixtures were not fixed as part of that correction.

Another tooling test verifies that the preserved invoice checker detects a known tenant/object authorization defect. That underlying fixture check is expected to fail; the tooling test passes because it confirms the checker catches the defect. This is evidence about the checker, not a successful skill-driven implementation.

## 8. Optional evaluations and their fixtures

### Case inventory

| Case group | Count | Purpose |
| --- | ---: | --- |
| Positive API design/review/implementation cases | 9 | Small API design, invoice authorization/concurrency, reservations, public migrations, GraphQL, gRPC, webhooks, caching, and asynchronous operations. |
| Negative API activation cases | 4 | CSS work, database-only indexing, a local pure helper, and a documentation typo should not load the API skill. |
| PostgreSQL review | 1 | Review schema/caller behavior, transaction connection ownership, concurrency, tenant isolation, and pooling assumptions. |
| Metadata discovery | 2 | Check availability metadata for the API and PostgreSQL skills without reading files or calling tools. |
| **Total** | **16** | Preparation is covered by the tooling suite. |

Expected activation flags and rubrics are test intentions, not observed successful activation results. During consolidation all cases were prepared; **no model execution, implicit-activation experiment, or before/after model-quality comparison was performed**.

### Fixture contents

| Directory | Files | What they represent |
| --- | --- | --- |
| `evals/fixtures/invoice/` | `PROJECT.md`, `service.py`, `test_existing.py` | Requirements and a synthetic Python/SQLite invoice API with authorization, protected-field, and concurrent-edit risks. Existing tests are deliberately incomplete. |
| `evals/fixtures/reservation/` | `PROJECT.md`, `service.py`, `test_existing.py` | A synthetic reservation workflow exposing duplicate-request and stock-consistency problems. |
| `evals/fixtures/postgresql-review/` | `PROJECT.md`, `schema.sql`, `customer.js` | A synthetic PostgreSQL schema, caller, and incident/proposal for read-only review. Preparation does not require a live PostgreSQL server. |

These nine source files were preserved byte-for-byte. Work on disposable copies when evaluating an implementation; changing the committed defects to make the checker pass would invalidate the evaluation input.

### Runner behavior

```sh
python evals/run.py --list
python evals/run.py --case p02-invoice-edit --label inspection
python evals/run.py --case p02-invoice-edit --condition baseline --label inspection
```

By default, `evals/run.py` only prepares a fresh workspace, prompt, and metadata under `.runs/evals/`. It copies the target skill into workspace `.agents/skills/` for the skill condition, omits that copy for the baseline, and initializes a nested Git repository to bound repository instruction discovery. Existing run directories are not overwritten.

Actual model execution requires an explicit flag and a compatible authenticated Codex CLI:

```sh
python evals/run.py --case p02-invoice-edit --label trial-1 --execute --timeout 300
```

That command can incur model usage. The runner has no fixed model; `--model` is optional. Review/discovery requests use a read-only sandbox; implementation requests use workspace-write. Configuration is passed for that invocation rather than rewriting global files. On timeout/interruption it attempts to stop its owned process group/tree and records exit code `124`.

The runner records execution status, requested condition, the target `SKILL.md` hash, elapsed time, exit status, and token usage only if the CLI supplies it. A prepared case has `executed: false`. Successful process exit is not automatically a behavioral PASS.

Common global copies of the target are disabled for the invocation, but other skills, instructions, tool availability, model variability, and host settings can still confound a baseline. A scope prompt and sandbox are not a guarantee of hidden rubrics, unavailable credentials, or full environment isolation. Use synthetic data and suitable isolation.

### Behavioral implementation checker

After inspecting and trusting a changed disposable artifact:

```sh
python evals/verify_implementation.py invoice .runs/evals/p02-invoice-edit-skill-trial-1/workspace
python evals/verify_implementation.py reservation .runs/evals/p03-reservation-skill-trial-1/workspace
```

This checker imports and executes the artifact's code. It is not a safe loader for hostile code. Its multiprocess SQLite checks widen scheduling windows and provide stress regression evidence; they do not prove every possible interleaving or substitute for PostgreSQL/MySQL-specific testing. Full evaluation details are in [evals/README.md](../evals/README.md).

## 9. Root documents, configuration, and local-only folders

| Item | Role and maintenance rule |
| --- | --- |
| [README.md](../README.md) | Public entry point: philosophy, all actual skills, installation, invocation, validation, prerequisites, support, and licensing. |
| [AGENTS.md](../AGENTS.md) | Stable repository-specific instructions for future coding agents: ownership, skill development, research, verification, and publication hygiene. |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Reproducible development setup, external validator installation, change workflow, commands, and review expectations. |
| [LICENSE](../LICENSE) | MIT terms for original skills, tools, fixtures, and documentation; notices accompany individually installed packages. |
| [requirements-dev.txt](../requirements-dev.txt) | Pinned PyYAML dependency for maintained Python tooling. |
| [.gitattributes](../.gitattributes) | LF normalization for new repository text; imported `skills/**` and `evals/fixtures/**` retain their original bytes. CRLF-aware whitespace checks preserve legitimate original line endings. |
| [.gitignore](../.gitignore) | Excludes dependency caches, runtime copies, generated runs, ZIP output, virtual environments, bytecode, local environment files, and common machine artifacts. |
| `.git/` | Local Git history/configuration. Managed by Git; not a skill package or normal committed source directory. |
| `.tools/` | Ignored local dependencies, including the external upstream checkout and migration verification runtime/cache. Not part of the published collection. |
| `.runs/` | Ignored local validation reports, test logs, and disposable evaluation workspaces/traces. May contain local context; review before sharing. |
| `dist/` | Ignored verified ZIP packages. The migration packages are under `dist/migration/`; they were not uploaded as a GitHub release. |
| `.venv/`, `__pycache__/` | Optional/generated Python environment and cache directories. They may exist locally but do not belong in commits. |

### Historical manifest

`docs/source-manifest.json` records the original snapshot using logical source names such as `user-skills/<name>`. It stores each file's relative path, byte count, SHA-256, and executable status. Absolute personal paths were deliberately omitted from the published record.

This is **historical evidence**, not a manifest to regenerate whenever a skill changes. Later deliberate updates are tracked in Git. Comparing a legitimately updated skill to the old snapshot will show a difference; that does not mean the migration was incorrect.

## 10. Useful existing tooling: retained, adapted, or excluded

| Earlier helper/resource | Decision and reason |
| --- | --- |
| `validate_skill.py` | Adapted into `scripts/validate_skills.py`; removed hardcoded installation and temporary dependency paths, retained supported upstream validation. |
| Two ZIP packaging helpers | Consolidated into `scripts/package_skills.py`; removed session-specific paths/fixed counts and retained integrity checks. |
| Separate discovery/API/PostgreSQL runners | Consolidated into `evals/run.py`; preserved useful cases with explicit execution, no fixed model, and bounded process cleanup. |
| API prompts, rubrics, and synthetic fixtures | Retained as reusable evaluation input, with explicit skill ownership. |
| PostgreSQL review fixture | Retained with a portable review case. |
| Implementation checker | Retained and corrected for argument handling, worker cleanup, selected-test invocation, and secondary connection closure. |
| Windows-specific dependency bootstrap | Excluded from maintained tooling; standard development dependency installation replaces it. |
| OpenAI `.system` and plugin-owned tools | Kept external. They were not relabeled or redistributed as original collection code. |
| Downloaded dependencies, research-page copies, raw outputs, traces, generated patches, and conversations | Excluded from publication because they are dependencies, temporary artifacts, or potentially sensitive context rather than necessary package source. |

No new application framework, scheduler, agent runtime, boilerplate generator, or infrastructure platform was introduced. Useful overlapping helpers were consolidated rather than maintained as parallel systems.

## 11. License and public-content review

MIT was selected with the owner's authorization for original collection content. It permits reuse, modification, and redistribution while requiring retention of the notice, and includes warranty/liability terms. It does not change the licenses of external documentation, tools, or dependencies. The root notice identifies `lofingoindia`; every skill contains a matching notice for individual distribution.

The publication review covered all original skill resources, fixtures, maintained tools, configuration, and documentation. It included targeted scans for recognizable credential/private-key patterns, sensitive URL credentials, personal absolute paths, and private-address candidates, plus review of script assumptions and redistributed content.

No high-confidence secret, private-key, or personal-path candidate was found in the reviewed publication set. No third-party implementation library or upstream validator was vendored. Original skill content was preserved, references point to external technical sources, and fixture data is synthetic.

This was a bounded review. It is not exhaustive copyright clearance, a secret-detection guarantee, or a security certification. Future additions need the same care. In particular, never publish raw evaluation outputs merely because they are generated by a test tool.

## 12. GitHub setup, publication, and CI

The empty local destination was connected to the already-existing GitHub repository. Its established default branch, `main`, was used. The repository was not recreated, its visibility was not changed, and no history replacement or force-push was performed.

The configured remote is:

```text
origin  https://github.com/lofingoindia/codex-engineering-skills.git
```

The consolidation commit contains **177 intended files**. Verification compared all published file paths, blob hashes, and Git file modes against local Git, with no mismatch or extra remote file. README and AGENTS were accessible at the commit. Local `main`, `origin/main`, and the remote branch SHA matched, and the working tree was clean at completion of that publication.

### Configured workflow

`.github/workflows/validate.yml` is configured for pushes to `main`, pull requests, and manual dispatch. It uses Python 3.13 on `ubuntu-latest` and `windows-latest`, installs development dependencies, obtains the pinned external validator, validates all skills, runs the tooling suite, and verifies packaging.

GitHub Actions and the upstream tool are pinned to reviewed commit SHAs. Repository permissions are read-only, checkout credentials are not persisted, and paid/model evaluations are absent from the workflow. These are configuration facts; hosted execution is reported separately.

### Actual hosted result

The first [Actions run](https://github.com/lofingoindia/codex-engineering-skills/actions/runs/41097060738) ended in `startup_failure` with **zero jobs**. The Actions page identified an account-level runner restriction. The existing account restriction must be resolved before hosted execution can be verified; no account settings were changed during this work.

After runner access is restored, run the **Validate skills** workflow on the current `main` and inspect both operating-system jobs. Local Windows checks passed, but hosted Windows and Ubuntu results are not yet established. The workflow should not be described as green until those jobs actually execute successfully.

## 13. How to install and use the collection

The Git repository is the versioned source copy. The existing user-level installations are the working copies Codex already discovers. Editing or pulling the repository does **not** automatically update those installations.

To install one skill through a supported Codex host:

```text
Use $skill-installer to install the skill at
https://github.com/lofingoindia/codex-engineering-skills/tree/main/skills/go-backend-engineering
```

While the repository is private, the installing account needs access. Use supported Git/installer authentication without placing credentials in prompts or committed files. Use an exact commit in place of `main` when reproducibility matters.

The migration host's installer uses `$CODEX_HOME/skills`, normally `~/.codex/skills`. Current Codex documentation also describes `~/.agents/skills` for user-level discovery and `.agents/skills` for project-level discovery. Confirm the installed host's supported path and avoid duplicate same-name installations. The migration did not move the already-working global copies.

For manual installation, copy a complete selected skill folder, including references and license, into the supported directory after checking for an existing destination. The [README](../README.md#installation) includes a collection-copy example that checks all conflicts before copying.

Example invocation:

```text
Use $postgresql-data-engineering to investigate our concurrent order updates.
Inspect our existing schema, callers, and tests before proposing changes.
```

To update an installed skill later: review the repository diff, preserve any local modifications, validate the intended package, and deliberately copy/install the approved revision. Refresh discovery according to the host. This repository does not silently overwrite global installations.

## 14. Where to make future changes

| Desired change | Correct place |
| --- | --- |
| Improve one skill's main reasoning/workflow or activation boundary | That skill's `SKILL.md` |
| Add detail about a technical topic | The relevant file under that skill's `references/` |
| Change a skill's display name/short description | That skill's `agents/openai.yaml` |
| Repair metadata/resource validation | `scripts/validate_skills.py` and focused regressions in `tests/test_tooling.py` |
| Change ZIP behavior | `scripts/package_skills.py` and packaging regressions |
| Add an optional evaluation scenario | `evals/cases.json`, with a synthetic fixture only if needed |
| Change optional runner or checker behavior | The relevant `evals/*.py`, documented limits, and focused tooling tests |
| Add or change hosted checks | `.github/workflows/validate.yml` and contributor instructions |
| Change public overview or installation instructions | `README.md` |
| Change contributor setup/workflow | `CONTRIBUTING.md` |
| Change stable repository-maintenance rules for agents | Root `AGENTS.md` |
| Understand original import provenance | `docs/inventory.md` and the historical manifest; preserve that snapshot |

A normal skill update should inspect the relevant guidance and sources, make the smallest justified change, validate that package, run relevant regressions, and review the diff. Use collection-wide validation for cross-cutting changes. Update catalog/docs when capabilities or commands change. Model evaluations are optional and should be proportional to the decision being tested.

## 15. Evidence boundaries and remaining work

| Established by executed evidence | Not established by this work |
| --- | --- |
| All discovered custom packages were copied, source hashes matched, and global source files were unchanged. | That future source changes will still match the historical migration snapshot. |
| All 17 packages passed the selected structural checks and ZIP integrity/source comparisons. | That every technical claim is correct for every future framework version. |
| The 24 tooling regressions passed, including a before/after cleanup regression and known-defect detection. | That each skill improves agent engineering decisions or avoids every application bug. |
| All 16 optional cases could be prepared without a model invocation. | Successful implicit activation, behavioral case outcomes, causal quality improvements, or measured token/cost savings. |
| The consolidation commit was pushed and its complete remote tree matched local Git. | Successful hosted Windows/Ubuntu execution, which remains blocked before startup. |
| The reviewed publication set had no high-confidence sensitive-content candidate. | Exhaustive legal/security certification or safety of future raw outputs. |

The remaining operational step is to restore hosted runner access and execute the configured workflow. No additional skill rewrite or large evaluation campaign is required to describe the completed migration accurately. The collection remains private until the owner separately authorizes a visibility change.

## 16. Complete supporting-reference index

The following index lists every original reference file by owning skill. Open the relevant topic when needed; an agent should not load all 99 references for one task.

<!-- Reference index generated from the inspected skill folders; not a new runtime dependency. -->

| Skill | Supporting reference files |
| --- | --- |
| `api-design-engineering` | [contracts](../skills/api-design-engineering/references/contracts.md), [protocols](../skills/api-design-engineering/references/protocols.md), [reliability](../skills/api-design-engineering/references/reliability.md), [security](../skills/api-design-engineering/references/security.md), [sources](../skills/api-design-engineering/references/sources.md) |
| `deep-readonly-system-audit` | [evidence-and-report](../skills/deep-readonly-system-audit/references/evidence-and-report.md), [safe-investigation](../skills/deep-readonly-system-audit/references/safe-investigation.md), [sources](../skills/deep-readonly-system-audit/references/sources.md) |
| `distributed-systems-reliability` | [atomicity-and-concurrency](../skills/distributed-systems-reliability/references/atomicity-and-concurrency.md), [delivery-and-contracts](../skills/distributed-systems-reliability/references/delivery-and-contracts.md), [recovery-and-operations](../skills/distributed-systems-reliability/references/recovery-and-operations.md), [sources](../skills/distributed-systems-reliability/references/sources.md) |
| `engineering-research-intelligence` | [agents-and-retrieval](../skills/engineering-research-intelligence/references/agents-and-retrieval.md), [data-and-distributed](../skills/engineering-research-intelligence/references/data-and-distributed.md), [evidence-policy](../skills/engineering-research-intelligence/references/evidence-policy.md), [go-and-mobile](../skills/engineering-research-intelligence/references/go-and-mobile.md), [languages-and-web](../skills/engineering-research-intelligence/references/languages-and-web.md), [production-evidence](../skills/engineering-research-intelligence/references/production-evidence.md), [repository-study](../skills/engineering-research-intelligence/references/repository-study.md) |
| `flutter-app-engineering` | [architecture-lifecycle](../skills/flutter-app-engineering/references/architecture-lifecycle.md), [data-offline](../skills/flutter-app-engineering/references/data-offline.md), [navigation-security](../skills/flutter-app-engineering/references/navigation-security.md), [performance](../skills/flutter-app-engineering/references/performance.md), [platforms-events](../skills/flutter-app-engineering/references/platforms-events.md), [sources](../skills/flutter-app-engineering/references/sources.md), [ux-accessibility](../skills/flutter-app-engineering/references/ux-accessibility.md), [verification-release](../skills/flutter-app-engineering/references/verification-release.md) |
| `go-backend-engineering` | [concurrency-context](../skills/go-backend-engineering/references/concurrency-context.md), [http-streams](../skills/go-backend-engineering/references/http-streams.md), [integrations-jobs](../skills/go-backend-engineering/references/integrations-jobs.md), [language-security](../skills/go-backend-engineering/references/language-security.md), [lifecycle-verification](../skills/go-backend-engineering/references/lifecycle-verification.md), [runtime-performance](../skills/go-backend-engineering/references/runtime-performance.md), [sources](../skills/go-backend-engineering/references/sources.md) |
| `multi-tenant-access-control` | [enforcement-and-data](../skills/multi-tenant-access-control/references/enforcement-and-data.md), [freshness-and-administration](../skills/multi-tenant-access-control/references/freshness-and-administration.md), [policy-and-identity](../skills/multi-tenant-access-control/references/policy-and-identity.md), [sources](../skills/multi-tenant-access-control/references/sources.md) |
| `nextjs-fullstack-engineering` | [data-caching](../skills/nextjs-fullstack-engineering/references/data-caching.md), [navigation-ux](../skills/nextjs-fullstack-engineering/references/navigation-ux.md), [production-verification](../skills/nextjs-fullstack-engineering/references/production-verification.md), [public-performance](../skills/nextjs-fullstack-engineering/references/public-performance.md), [rendering-structure](../skills/nextjs-fullstack-engineering/references/rendering-structure.md), [security-mutations](../skills/nextjs-fullstack-engineering/references/security-mutations.md), [sources](../skills/nextjs-fullstack-engineering/references/sources.md) |
| `nodejs-backend-engineering` | [http-streams](../skills/nodejs-backend-engineering/references/http-streams.md), [integrations-jobs](../skills/nodejs-backend-engineering/references/integrations-jobs.md), [language-security](../skills/nodejs-backend-engineering/references/language-security.md), [lifecycle-diagnostics](../skills/nodejs-backend-engineering/references/lifecycle-diagnostics.md), [runtime-concurrency](../skills/nodejs-backend-engineering/references/runtime-concurrency.md), [sources](../skills/nodejs-backend-engineering/references/sources.md) |
| `postgresql-data-engineering` | [migrations](../skills/postgresql-data-engineering/references/migrations.md), [operations-recovery](../skills/postgresql-data-engineering/references/operations-recovery.md), [queries-indexes](../skills/postgresql-data-engineering/references/queries-indexes.md), [schema-security](../skills/postgresql-data-engineering/references/schema-security.md), [sources](../skills/postgresql-data-engineering/references/sources.md), [transactions-connections](../skills/postgresql-data-engineering/references/transactions-connections.md) |
| `react-vite-dashboard-engineering` | [architecture](../skills/react-vite-dashboard-engineering/references/architecture.md), [auth-routing](../skills/react-vite-dashboard-engineering/references/auth-routing.md), [data](../skills/react-vite-dashboard-engineering/references/data.md), [experience](../skills/react-vite-dashboard-engineering/references/experience.md), [sources](../skills/react-vite-dashboard-engineering/references/sources.md) |
| `real-world-test-engineering` | [flutter-and-dart](../skills/real-world-test-engineering/references/flutter-and-dart.md), [go](../skills/real-world-test-engineering/references/go.md), [javascript-and-web](../skills/real-world-test-engineering/references/javascript-and-web.md), [python](../skills/real-world-test-engineering/references/python.md), [reproducible-integration](../skills/real-world-test-engineering/references/reproducible-integration.md), [scenarios-and-oracles](../skills/real-world-test-engineering/references/scenarios-and-oracles.md), [sources](../skills/real-world-test-engineering/references/sources.md) |
| `redis-production-engineering` | [atomicity-and-rate-limiting](../skills/redis-production-engineering/references/atomicity-and-rate-limiting.md), [caching-and-freshness](../skills/redis-production-engineering/references/caching-and-freshness.md), [capabilities-and-compatibility](../skills/redis-production-engineering/references/capabilities-and-compatibility.md), [infrastructure-and-recovery](../skills/redis-production-engineering/references/infrastructure-and-recovery.md), [messaging-and-processing](../skills/redis-production-engineering/references/messaging-and-processing.md), [sources](../skills/redis-production-engineering/references/sources.md), [tenancy-and-clients](../skills/redis-production-engineering/references/tenancy-and-clients.md) |
| `repository-structure-engineering` | [dart-flutter](../skills/repository-structure-engineering/references/dart-flutter.md), [go](../skills/repository-structure-engineering/references/go.md), [javascript-node](../skills/repository-structure-engineering/references/javascript-node.md), [ownership-and-placement](../skills/repository-structure-engineering/references/ownership-and-placement.md), [polyglot-workspaces](../skills/repository-structure-engineering/references/polyglot-workspaces.md), [safe-restructuring](../skills/repository-structure-engineering/references/safe-restructuring.md), [sources](../skills/repository-structure-engineering/references/sources.md), [web-frameworks](../skills/repository-structure-engineering/references/web-frameworks.md) |
| `saas-security-engineering` | [identity-and-sessions](../skills/saas-security-engineering/references/identity-and-sessions.md), [operations-and-verification](../skills/saas-security-engineering/references/operations-and-verification.md), [sources](../skills/saas-security-engineering/references/sources.md), [untrusted-boundaries](../skills/saas-security-engineering/references/untrusted-boundaries.md) |
| `task-subagent-orchestration` | [delegation-and-integration](../skills/task-subagent-orchestration/references/delegation-and-integration.md), [planning-and-skills](../skills/task-subagent-orchestration/references/planning-and-skills.md), [reporting-and-audits](../skills/task-subagent-orchestration/references/reporting-and-audits.md), [sources](../skills/task-subagent-orchestration/references/sources.md) |
| `universal-database-engineering` | [clickhouse](../skills/universal-database-engineering/references/clickhouse.md), [integrity-workload-and-evolution](../skills/universal-database-engineering/references/integrity-workload-and-evolution.md), [modeling-decisions](../skills/universal-database-engineering/references/modeling-decisions.md), [mongodb](../skills/universal-database-engineering/references/mongodb.md), [mysql-and-mariadb](../skills/universal-database-engineering/references/mysql-and-mariadb.md), [sources](../skills/universal-database-engineering/references/sources.md), [sqlite](../skills/universal-database-engineering/references/sqlite.md) |
