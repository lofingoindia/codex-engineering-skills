# Causal findings and the durable audit report

## Evidence classifications

| Classification | Meaning |
| --- | --- |
| PROVEN | Direct, sufficient evidence establishes the specific issue under the stated conditions; this can be a complete reachable code/configuration proof, without claiming an unexecuted exploit |
| STRONGLY SUPPORTED | Several consistent observations support the issue, but a required runtime/configuration/link remains unconfirmed |
| HYPOTHESIS | A plausible failure mechanism with a clear missing observation or proposed discriminating check |
| UNVERIFIED | Available evidence is insufficient to decide whether the behavior is correct or defective |

Keep severity and confidence separate. A severe potential leak can remain a hypothesis, while a proven cosmetic issue remains low impact. Severity should reflect actual exposure, prerequisites, business impact and existing mitigation. Use the project's established rubric where available; do not invent a numerical readiness score or treat every best-practice deviation as a release blocker.

Separate observed facts, causal inference and proposed correction. Cite exact paths/symbols/lines and revision where available; do not fabricate references. For telemetry, record environment, query/time window, filters, sampling and coverage limits with sanitized identifiers. Source configuration is not necessarily deployed configuration. A scanner result, README claim or test name is not direct proof of runtime behavior.

## Validate and challenge a finding

Connect a realistic trigger to reachable code, missing/incorrect guard, resulting state/effect and customer consequence. Look for the strongest existing safeguard or disconfirming path before finalizing. A vulnerability finding should not omit an upstream permission check; a reliability finding should not omit a durable consumer deduplication step merely because it is in another module.

Distinguish missing code from configuration supplied elsewhere, optional feature from active path, and dead/example code from deployed behavior. Corroborate callers, registration, flags, transactions, schema constraints and consumers. For a concurrency issue, describe a feasible interleaving and the invariant it violates; do not claim that it was reproduced unless it was.

Record what would resolve uncertainty. A narrow isolated integration test, deployment-setting confirmation or provider guarantee is more useful than “test thoroughly.” During the read-only audit, describe such checks rather than executing mutating ones. Existing test success is useful evidence only for what its setup and assertions cover.

Update a finding's classification or withdraw it when new evidence changes the causal chain. Preserve a brief disposition so earlier references are understandable; stable IDs should not silently point to unrelated new issues. Do not duplicate the same root cause into many inflated findings when one finding with multiple affected paths is clearer.

## Maintain one report continuously

Create an initial report before substantive investigation. Keep enough state for another agent/person to resume without the chat. After each meaningful segment, write new evidence and revise the current conclusion, not just append an unstructured transcript. Before a major transition or compaction, reconcile outstanding items and record the next step.

Use sections proportional to the scope:

- Scope, revision/environment, constraints, permitted report path and limitations.
- Architecture/workflow map and the boundaries actually traced.
- Finding inventory with stable IDs, severity, evidence classification and status.
- Detailed causal findings and relevant safeguards.
- Unverified areas, missing evidence and focused validation needs.
- Prioritized remediation direction, readiness limits and current investigation checkpoint.

This is a report outline, not a giant template to fill for every subsystem. Reuse the existing coherent report rather than creating separate copies for each phase. Keep raw secrets, private records and unnecessary payloads out of it; refer to protected sources using sanitized evidence.

A useful finding can be compact while covering:

`ID / title / subsystem / severity / classification → trigger → observed path and safeguards → violated invariant and causal consequence → correction direction → required validation and uncertainty.`

Keep facts and recommendations distinct. Findings remain recommendations in read-only mode regardless of severity or availability of an implementation skill. An urgent suspected incident warrants an explicit evidence-based notification, not self-authorized containment changes.

## Close the audit honestly

Summarize material risk, verified coverage, practical remediation order and genuinely unverified areas. Tie release blockers to supported consequences under the agreed criteria; absence of known findings does not establish universal readiness. Record checks actually executed and their results separately from proposed tests and theoretical analysis.

Reconcile inventory and details, update the checkpoint as complete or interrupted, and document read-only verification and any unexplained changes. State repository/file comparison scope and limits for remote systems. A report is independently useful when it preserves what was learned, why it matters, what remains unknown and the next safe action without relying on transient chat context.
