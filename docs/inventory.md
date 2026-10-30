# Migration inventory and provenance

Snapshot date: **2026-10-30**. Source discovery inspected the actual user-level Codex skill root and skill-creation workspace. System skills and plugin-owned skills were excluded. There were **17 custom engineering skills**, **133 source files**, and **681,508 bytes**; all were text (`.md`/`.yaml`), with no bundled executable scripts or symlinks. All 17 had `SKILL.md`, `agents/openai.yaml`, and supporting references. No discovered custom package was missing or incomplete.

The source of each entry is `user-skills/<name>` in the existing user-level installation. This logical notation deliberately avoids personal absolute paths. [source-manifest.json](source-manifest.json) records every original relative path, byte count, executable status, and SHA-256 digest.

| Skill | Original files | References |
| --- | ---: | ---: |
| api-design-engineering | 7 | 5 |
| deep-readonly-system-audit | 5 | 3 |
| distributed-systems-reliability | 6 | 4 |
| engineering-research-intelligence | 9 | 7 |
| flutter-app-engineering | 10 | 8 |
| go-backend-engineering | 9 | 7 |
| multi-tenant-access-control | 6 | 4 |
| nextjs-fullstack-engineering | 9 | 7 |
| nodejs-backend-engineering | 8 | 6 |
| postgresql-data-engineering | 8 | 6 |
| react-vite-dashboard-engineering | 7 | 5 |
| real-world-test-engineering | 9 | 7 |
| redis-production-engineering | 9 | 7 |
| repository-structure-engineering | 10 | 8 |
| saas-security-engineering | 6 | 4 |
| task-subagent-orchestration | 6 | 4 |
| universal-database-engineering | 9 | 7 |

## Preservation decisions

All original 133 skill files were copied byte-for-byte into `skills/`. Global installations were not moved or edited. The only additional file in each copied package is an MIT `LICENSE`, added for independently redistributed packages with the owner's authorization. There was no skill behavior or metadata rewrite. The original hash manifest remains a historical snapshot; future intentional changes belong in Git history.

Git attributes disable text conversion for imported skill files and evaluation fixtures, preserving existing bytes on Windows and Linux. New repository tooling/docs use LF normalization. No executable permission bit was present to preserve on the imported text resources. New Python entry points are documented using `python`, so they do not require Unix executable bits.

## Reusable custom tooling

| Original workspace resource | Repository treatment |
| --- | --- |
| `work/validate_skill.py` | Adapted to `scripts/validate_skills.py`; calls the external upstream validator and checks package resources/UI/syntax. Removed hardcoded installation and temporary dependency paths. |
| `work/package_verified_skill.py`, `work/package_skills.py` | Consolidated into `scripts/package_skills.py`; validates, retains all files, checks bytes/ZIP integrity, refuses overwrite. Removed fixed counts and session paths. |
| `work/run_discovery.py`, `work/final_discovery.py` | Discovery capability represented by two optional cases in `evals/cases.json` and the consolidated runner. No fixed model or automatic paid run. |
| `outputs/evaluation-suite/run.py`, `outputs/postgresql-checks/run.py` | Consolidated into `evals/run.py`; preparation by default, explicit execution, bounded timeout cleanup, per-invocation skill configuration. Removed broad sandbox access and personal paths. |
| `outputs/evaluation-suite/cases.json` and synthetic fixtures | Preserved 13 API prompts/rubrics and six fixture files; added explicit skill ownership in the case data. |
| `outputs/postgresql-checks/fixture` | Preserved three synthetic review files; added one portable review case. |
| `outputs/evaluation-suite/verify_implementation.py` | Preserved semantic checks; added command validation, single-check selection, cleanup of owned worker processes, and explicit secondary SQLite connection closure. |
| `work/prepare_validation.py` | Not retained: a session-specific Windows wheel bootstrap. Standard development dependencies replace it. |

`tests/test_tooling.py` adds focused regressions for the maintained tools. `.github/workflows/validate.yml` runs structural validation, tooling tests, and packaging on Windows and Ubuntu, without model evaluations.

Excluded artifacts include `.system`/plugin tools, downloaded reference copies, third-party dependency libraries, raw agent outputs, research/evaluation logs, generated application patches, caches, temporary data, and pasted conversations. External OpenAI tools and PyYAML are dependencies, not vendored source. Useful original evaluation cases were retained; most other skills have no reusable automated behavioral evaluation assets in the installed packages. No missing assets or successful behavioral results are invented.

## Standards and dependencies

- [Agent Skills specification](https://agentskills.io/specification): portable `SKILL.md` metadata and package layout.
- [Codex skill guidance](https://learn.chatgpt.com/docs/build-skills): host discovery and progressive disclosure. Discovery roots vary with the installed host/installer; see the README.
- [OpenAI skill-creator validator at the CI pin](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/quick_validate.py): reused externally, not copied.
- [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference) and [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode): checked against the installed `codex exec --help` for optional runner flags.
- [Git attributes](https://git-scm.com/docs/gitattributes): imported-byte preservation.
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use): SHA-pinned actions, limited permissions, no privileged PR trigger or persistent checkout credentials.
- [MIT terms](https://opensource.org/license/mit): owner-authorized permissive redistribution of original content. Linked third-party documentation and dependencies retain their own terms.

Each skill's own reference files retain its engineering source index. This migration does not revalidate every external technical claim or link against future releases.
