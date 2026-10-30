# Planning and skill selection

## Choose the mode from observed work

One coherent fix with understood behavior and a local verification boundary can remain a direct change even if several files are touched. A short change can warrant a formal plan when it crosses a sensitive contract or has an uncertain prerequisite. Do not turn technology names or repository size into automatic decomposition.

For moderate work, separate outcomes with real prerequisites and verification needs. For broad work, represent the complete requested scope, the dependency chain that determines completion, independent workstreams and an integration owner. Avoid a long speculative backlog before inspecting relevant code. Prefer investigation that resolves a concrete planning uncertainty.

When uncertainty prevents an implementation-ready boundary, create a bounded discovery outcome first: the decision and evidence needed to release implementation. Do not pretend a guessed API/schema is already agreed. Conversely, do not gate independent work on unrelated discovery merely because it appears earlier in the table.

## The task contract

Each formal task should be independently understandable. Keep the chat row compact and supply necessary detail in its handoff/context:

- ID/title, actual objective and expected user/system behavior.
- In-scope responsibilities and exclusions; owning subsystem and affected paths discovered so far.
- Dependencies, unresolved assumptions, stable contracts and relevant version/configuration constraints.
- Business/security/reliability/compatibility invariants that must survive.
- Existing skills to use, mandatory research-intelligence usage and the focused technical uncertainty.
- Owner, allowed mutation/resource boundary and any required integration coordination.
- Appropriate tests/evidence and definition of done, including relevant failure/allowed paths.

Keep tasks cohesive: “make this worker transition idempotent” can be an outcome; “edit imports,” “add a folder,” and “write a helper” usually are implementation steps. Pure research, analysis or review tasks finish with evidence/decisions rather than invented application changes or tests.

Include integration as an explicit task or owner responsibility when there is a real cross-task boundary. Do not create a ceremonial integration task for every localized fix. A task table is communication in chat, not a reason to add permanent YAML plans, a tracker service or duplicate repository documentation.

## Match skills to the decision

Inspect the active environment's installed metadata. Apply `engineering-research-intelligence` to each substantive formal task, then only specialists whose responsibilities are involved. Reading/applying a skill is different from merely putting its name in a table. Pass an available name/path to a subagent when needed, without assuming its context or filesystem matches the lead.

For example, a tenant leak in a Go endpoint may need tenant-access and Go guidance; an API-contract change may also need API guidance. A database-only task does not automatically need all backend skills. A dashboard's local state fix does not automatically need a database/security audit. These are selection examples, not fixed skill bundles or a hardcoded installed-skill inventory.

If a specialist is absent, use relevant official guidance and available capabilities. Missing a convenient specialist is not automatically a blocker. If research intelligence is absent, disclose equivalent targeted research and its limits rather than falsely claiming invocation. Do not install new skills/tools or change global configuration just to satisfy a table entry.

Reuse evidence across tasks only when the claim, version, configuration and applicability still match. Record what carries over and what remains task-specific. “Research completed elsewhere” without a relevant conclusion is not sufficient; neither is repeating the same searches for every row.

## Revise the plan rather than defend it

When discovery reveals a missing prerequisite, unnecessary task, shared file/resource, new in-scope risk or safer parallel boundary, update affected rows and notify owners. Pause affected mutations until scope/contracts are clear; independent work can continue. Preserve task IDs/dispositions where useful so earlier reports remain understandable.

Merge or remove tasks that no longer have a purpose. Add work needed for the authorized result's correctness, not speculative features or an architectural expansion. For a genuine external/input blocker, report what is missing and continue useful independent work where possible. The plan is current working state, not an immutable promise to execute a template.
