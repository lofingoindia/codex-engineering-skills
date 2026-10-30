# Main-chat reporting, completion, and audits

## Report task outcomes where the user can see them

Every formal task gets a main-chat completion report before it is marked complete and before its owner starts another assignment. A subagent's final message to the lead, a tool log, a repository file or a tracker update does not substitute for this report. The lead can keep working on independent work while another task runs, but must review and publish its result before reassignment.

Use concise parallel fields:

**Findings → Changes → Tests & Evidence → Pending Issues → Status.**

Completion status is **PASS / PARTIAL / FAIL / BLOCKED**. A plan can additionally distinguish pending/active work without presenting it as completed. PASS means the task's actual completion criteria have been accepted with relevant evidence. PARTIAL identifies delivered work with outstanding requirements/integration; FAIL records a failed outcome; BLOCKED identifies a real prerequisite/input/environment dependency preventing completion. Do not relabel a failed check as PASS merely to advance the plan.

For an analysis-only task, evidence can be inspected source/configuration and a supported decision; do not invent a code change or executed test. For implementation, identify the changed behavior and actual checks. Distinguish reading tests, executing them, task-local success, integrated success and deployment verification. If a local result is sound but integration remains pending, state both.

Keep the task table accurate after meaningful status/scope changes. Explain new dependencies, removed work or owner changes briefly. Avoid repeatedly pasting a large unchanged table or recounting every tool call. Significant outcomes and unresolved risk should remain visible in chat, with detailed evidence in an authorized existing artifact when needed.

## Finish the whole requested scope

Before final completion, reconcile every requested outcome with accepted work, relevant combined verification and any genuine remaining limitation. Check that no agent is still making conflicting changes, no required work was orphaned and no partial task is hidden behind another owner's PASS. Do not stop at a useful first subset and ask whether to do the remaining authorized work.

Report actual use of subagents and verification scope. Do not estimate token savings, elapsed-time improvement, test coverage or superiority to a single agent as measured facts without instrumentation and a comparable baseline. More active agents is not a success metric. Do not create an evaluation service or benchmark campaign merely to justify coordination.

## Keep audits strictly read-only

For substantial read-only audits, apply `deep-readonly-system-audit` if available; if absent, maintain the same user-required boundary and disclose the fallback. Resolve one authorized Markdown report destination, initialize/update it before substantive investigation and preserve findings after each meaningful segment and before major transitions/compaction. Reuse stable finding IDs and checkpoint the investigation.

The audited source, configuration, databases, services and infrastructure remain unchanged by every agent. The report is the sole writable artifact unless explicitly authorized otherwise. Do not create scratch scripts, worktrees, caches, test outputs, alternate reports or runtime fixtures under an assumed audit exception. Existing independently readable environments may be used only within scope; a test/build or apparent GET is not inherently non-mutating.

Assign the lead or one designated owner as the sole report writer. Other audit agents send sanitized evidence, exact references, scope and uncertainties after meaningful segments rather than waiting until their entire assignment ends; the writer updates the primary report promptly. Pause investigation if discoveries cannot be preserved safely. Do not let two agents overwrite the report or defer its creation until the final response.

Use the established evidence classifications: PROVEN, STRONGLY SUPPORTED, HYPOTHESIS and UNVERIFIED. Preserve confidence separately from severity; a proposed correction remains a recommendation. No specialist skill, severe finding or subagent delegation grants permission to apply a fix.

Read-only instructions are behavioral constraints, not a new sandbox. Inspect actual inherited tools/permissions and choose safe read capabilities. Verify non-mutation through appropriate available baselines/status/content evidence without creating unauthorized artifacts or causing changes to collect evidence. Report exactly what was checked and what could not be independently verified, especially remote resources. A source diff alone cannot establish that a live database was untouched.
