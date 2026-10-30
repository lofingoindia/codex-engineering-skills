---
name: real-world-test-engineering
description: Discover realistic failure cases and write, run, or improve behavior-focused unit, component, integration, and contract tests. Use for meaningful application verification, regression fixes, concurrency risks, or weak/flaky tests; skip trivial documentation edits and standalone AI-agent evaluations.
---

# Real-World Test Engineering

Build the smallest sufficient suite that distinguishes correct behavior from plausible defects. Test counts, line coverage, successful compilation and a green runner are not proof of meaningful correctness. Strengthen code-level confidence before expensive acceptance testing while identifying what still needs a real browser, device, service or deployment.

## Establish expected behavior first

Inspect the request, relevant instructions, callers/consumers, implementation, state transitions, existing tests, fixtures and CI commands. Establish actual runtime/framework/driver versions and test environments. Expand only along relevant dependencies. Reuse the project's runner, helpers and isolated services; do not migrate frameworks or add testing infrastructure by default.

Define the intended user/workflow outcome, compatibility requirements, business/security invariants and the observable evidence that would establish them. Existing code/tests can be wrong; do not copy their current result into the oracle. Resolve material ambiguity from contracts and domain evidence before encoding a disputed expectation. For read-only requests, assess evidence and propose checks without changing the application or executing mutating tests; preserve the authorized report-only boundary.

## Discover the failures that matter

Trace where input, ownership, state or responsibility changes. Ask what happens if the user repeats an action, another actor changes state, work completes out of order, or a dependency fails before versus after committing an effect. Combine only risks supported by the actual workflow. Rank by impact, likelihood, exposure and uncertainty, not by checklist length.

For each important scenario, identify the precondition, action/interleaving, expected response/final state, prohibited effect and the test boundary that can observe them. A small fix can use one focused regression; substantial work may warrant a compact scenario summary. Do not generate a formal matrix for every utility.

Use [scenario discovery and oracles](references/scenarios-and-oracles.md) for counterexamples, property/stateful/fuzz testing and selective mutation testing. These techniques are options, not requirements for every change.

## Choose a boundary that can prove the claim

Use unit tests for isolated decisions, component/widget tests for framework interactions, and integration tests for actual adapters and service behavior. Keep the behavior under test real. A mocked repository cannot prove transaction isolation, a mocked Redis clock cannot prove server expiry, and a mocked broker cannot prove redelivery. Mock external boundaries when their real behavior is outside the claim. Schema/consumer mocks need provider verification when interoperability is claimed.

| Current uncertainty | Conditional reference |
| --- | --- |
| Oracles, meaningful assertions, advanced discovery or regression sensitivity | [Scenarios and oracles](references/scenarios-and-oracles.md) |
| Async ordering, concurrency, real dependencies, contracts, fixtures or flakes | [Reproducible integration](references/reproducible-integration.md) |
| TypeScript/Node.js, React or Next.js | [JavaScript and web](references/javascript-and-web.md) |
| Go handlers, goroutines, race detection or fuzzing | [Go](references/go.md) |
| Python fixtures, async behavior or generated tests | [Python](references/python.md) |
| Dart/Flutter state, widgets and platform boundaries | [Flutter and Dart](references/flutter-and-dart.md) |
| Authoritative evidence, version caveats or source examples | [Research index](references/sources.md) |

Load only relevant detail. Use available research/specialist skills for consequential engine, runtime or security uncertainty. This skill owns test quality and confidence, not a new E2E framework, security audit or model-provider evaluation system. Companion skills are optional and must honor the same scope.

## Prove, fix and verify

Before a defect fix, establish a failing regression when feasible. Confirm it reaches the intended condition and fails for the defect, not broken setup/imports. For new behavior, define expectations independently before implementation. If a test passes unexpectedly, inspect its path, awaited work, doubles and assertions; do not assume the suspected defect is absent.

Correct the cause, retain the regression and run the focused tests plus justified neighboring/integration checks. Assert actual response, durable state, allowed/forbidden effects and recovery as relevant. Do not weaken assertions, suppress failures, add production bypasses or accept arbitrary sleeps to obtain green results. Stop broadening/repeating successful checks without a new reason. Normal validation is appropriate for documentation/skill-only work; a behavioral evaluation campaign is not the default.

For every substantial task report in main chat: **scenarios and edge cases → tests added/improved → bugs/root causes/corrections → commands and actual results → remaining verification gaps → PASS / PARTIAL / FAIL / BLOCKED**. Distinguish passed, failed, skipped and unexecuted checks. State what the evidence establishes and which browser/device/proxy/provider/performance risks remain; never claim code-level tests eliminate all real-environment verification.
