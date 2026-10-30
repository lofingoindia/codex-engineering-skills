# Safe investigation and the read-only boundary

## Define scope and environmental authority

Establish the requested subsystem/repository, inspected revision, local versus deployed environment, available evidence, and known exclusions. If source cannot establish effective deployed configuration, mark that uncertainty rather than assuming development defaults apply. Prioritize financial correctness, tenant boundaries, accepted durable work, recovery and high-impact exposure based on this system's workflows.

Use the authorized primary Markdown report as durable investigation state. Do not write an additional scratch file, downloaded artifact, fixture, screenshot or result dump unless separately authorized. The report exception does not permit code/config edits, even when a file's name contains “audit.” If reporting itself is unavailable, state the limitation and resolve the destination before conducting an unrecorded deep audit.

## Inspect effects before running anything

Commands that sound observational may write files, alter runtime state, install tools or contact a live dependency. Inspect scripts, lifecycle hooks and settings, not merely the command label. When behavior remains uncertain, choose inspection or record a proposed isolated check.

| Capability | Safer audit use and hidden effects to consider |
| --- | --- |
| File search/read | Read specific source/configuration without executing modules; avoid exposing secrets and unrelated personal data |
| Git inspection | Use non-mutating status/diff/history operations with optional index-refresh writes disabled where relevant; no checkout, reset, clean, fetch or generated baseline file |
| Tests/builds/analyzers | Read existing results and test definitions first; running can write caches, snapshots, coverage, generated code or test data and invoke network/setup hooks |
| Dependency inspection | Read installed manifests/lockfiles/advisories safely; install, update, audit-fix and tool-on-demand commands can mutate or execute third-party code |
| Database queries | Use inspected, bounded, least-privilege read access where available; SELECT can call functions with effects and EXPLAIN ANALYZE executes the statement |
| Database “read-only” mode | Useful restriction, not proof of no temporary writes, external effects or resource impact; rollback cannot undo every side effect |
| Broker/Redis tools | Inspect safe metadata/metrics; consuming, claiming, acknowledging, retrying or redriving changes state even when a command is called “read” |
| HTTP/browser requests | Inspect endpoint behavior, account and scope; GET/page opening can trigger business writes, sessions, tracking or background actions |
| Cloud/observability APIs | Use known read capabilities and bounded windows/pagination; avoid restarts, deployment, scans and configuration mutations |

Do not make harmless investigation impossible through a hypothetical zero-effect standard: ordinary read telemetry may produce access logs or operating-system activity. The constraint is no intentional target mutation or extra writable artifact. Distinguish understood incidental read effects from application side effects, and report the actual verification scope.

Avoid broad expensive database reads or production traffic generation merely to gather evidence. Use limits, time bounds and existing operational samples. Read-only access can still impair availability or expose private information. Do not request or dump production credentials to complete an audit.

## Trace complete workflows

Select a few consequential flows and expand where evidence points:

- Entry/input to authentication, resource/tenant/field authorization and the actual data query/output.
- Mutation to transaction/constraint, durable intent, event delivery, worker effect and user-visible completion.
- Timeout/partial failure to retry ownership, duplicates, recovery state and operational detection.
- Deployment configuration to runtime permissions, discovered paths, readiness/shutdown and rollback/compatibility assumptions.

Use direct callers, integration adapters, schema/policy definitions, consumer code, tests and telemetry to connect the chain. Do not infer a distributed transaction from an `await`, authorization from a helper's existence, durability from a queue name, or production readiness from healthy process metrics. Inspect fallback/admin/bulk/background paths as the workflow warrants, without requiring every application to have them.

## Verify non-mutation within an honest scope

At the start and finish, use appropriate read-only repository/file evidence to identify pre-existing and new changes. Record baseline identifiers and results in memory/the primary report rather than a new artifact. For local source, status/diff plus scoped content fingerprints can strengthen evidence; Git status alone excludes some ignored/untracked content. Account for the report itself if it is inside the tree.

Concurrent user edits are not automatically agent mutations; disclose them and avoid overwriting or “cleaning” the workspace. A source diff does not verify a remote database, cloud service or runtime configuration. State which resources were checked, which capabilities were used and what could not be independently compared.

If an unexpected mutation occurs, stop that action path, record it and assess its scope. Do not conceal it, rerun with broader permissions or perform an unauthorized rollback that may overwrite user changes. Preserve evidence and explain the bounded next step.
