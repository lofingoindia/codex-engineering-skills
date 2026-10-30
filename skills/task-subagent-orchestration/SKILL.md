---
name: task-subagent-orchestration
description: Scope engineering work, plan cohesive tasks, select skills, and coordinate useful subagent delegation through verification and integration. Use for substantial planning or coordination, including audits, or when deciding whether decomposition is needed; keep small coherent changes direct.
---

# Task and Subagent Orchestration

Act as the lead responsible for the user's complete outcome. Plan and delegate only when that improves correctness, elapsed time or context use after coordination costs. This skill coordinates existing engineering capabilities; it does not define a new scheduler, agent runtime or project-management framework.

## Understand before dividing

Inspect the request, prior decisions, applicable instructions, relevant architecture/current code, callers, dependencies, invariants and existing verification. Read only what the change needs; expand when evidence reveals a wider boundary. Do not invent a plan from a generic feature template or trust stale documents over current implementation.

A contained coherent change can stay with one owner, without a task table, agents or broad research. Directly implement and verify it proportionately. For meaningful dependencies, uncertainty, ownership or verification boundaries, use a formal plan. Scope is a judgment about outcomes and risk, not file/line counts or a required number of tasks.

## Formal plans and research

Before task-based implementation, present this readable table in the **main chat**, with concise rows derived from the investigation:

| Task | Objective & Scope | Dependencies | Skills | Research Focus | Owner | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

Give each task an ID, cohesive behavioral outcome, owner, boundaries, prerequisites and completion criteria. [Planning and skill selection](references/planning-and-skills.md) covers the task contract and scope decisions. Keep all requested work represented without turning it into microtasks.

For **every substantive task in a formal plan, use `engineering-research-intelligence`**: read/apply its available instructions, identify the task's technical uncertainty, check applicable version-matched upstream evidence against current code, and record concise conclusions. Reuse still-current, directly applicable research; mandatory use does not require rereading the skill or repeating searches. If unavailable, perform equivalent targeted research and disclose the fallback; never claim it was invoked.

Inspect actual available skill descriptions and choose only relevant specialists. Show them in the table and handoff. Do not assume a testing or technology skill exists or load all skills because they are installed.

## Delegate useful independent work proactively

For a formal plan, examine the **whole remaining plan** for worthwhile parallel work, including upcoming tasks. When permitted, tools are available and ownership/resources are safe, delegate ready independent implementation or investigation early. Subagents can write and test within assigned scope; they are not restricted to research. Do not wait for the lead to reach an independent task merely to preserve serial order.

Keep dependent mutations behind resolved prerequisites. Early read-only investigation can proceed without guessing an unfinished contract. Use [delegation and integration](references/delegation-and-integration.md) for the decision, handoff and ownership rules. Check actual context, filesystem/worktree, permission and lifecycle behavior; do not assume isolation. If delegation is unavailable, forbidden or uneconomic, execute lead-owned and state that accurately.

## Execute, integrate, and report

Each owner follows investigation, focused research, planning, relevant edge cases/tests, implementation, failure correction and verification within its assigned task. Choose/add meaningful tests for changed behavior; use normal validation for documentation/configuration where appropriate. Do not silently batch unrelated tasks or repeat successful checks without a reason.

The lead reviews actual changes and evidence, resolves interface/resource conflicts, and verifies the relevant integrated behavior. A subagent's self-reported PASS is not integrated proof. Publish a main-chat completion report **before marking that task complete and before assigning its owner another task**:

**Findings → Changes → Tests & Evidence → Pending Issues → Status: PASS / PARTIAL / FAIL / BLOCKED.**

State pending integration explicitly. Update task status, then release dependent work only when its prerequisites are satisfied. Reassess and explain significant changes to task boundaries, order, ownership or necessary scope; do not follow an obsolete plan. Continue until the requested outcome is handled or a genuine blocker remains.

## Read-only audits

Explicit read-only scope governs every owner and specialist. No agent may fix code or mutate the audited environment. For substantial audits, apply available `deep-readonly-system-audit` guidance; otherwise preserve its equivalent boundary: one authorized Markdown report, updated alongside meaningful investigation segments and before major transitions/compaction. The report is the sole writable artifact unless the user authorizes others. Assign one report writer to prevent concurrent overwrites. See [reporting and audits](references/reporting-and-audits.md).

Use [sources](references/sources.md) for upstream rationale and limitations. Report actual delegation, checks and outcomes; do not invent agents, measurements, activation results or end-to-end success.
