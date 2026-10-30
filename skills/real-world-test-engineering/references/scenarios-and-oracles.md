# Discovering scenarios and trustworthy oracles

## Find counterexamples from the real workflow

Start with one representative allowed operation and trace identity, input normalization, reads, decisions, writes, external effects and visible completion. Mark the boundaries where knowledge becomes stale or responsibility transfers. Turn an observed uncertainty into a concrete sequence, not an abstract “handles errors” test.

For a search UI, control two pending responses and complete the newer search before the older one; assert the visible result remains associated with the active query. For a retried mutation, distinguish rejection before processing from a lost reply after commit; assert the recovery contract and durable effect count. For a tenant-owned relation, use valid records in two tenants with deliberately overlapping business IDs; assert a permitted operation and the forbidden association's lack of effects. These illustrate the method, not a required suite for every feature.

Follow the actual lifecycle: creation, repeated use, mutation, deletion/revocation and recovery. Boundaries can be numeric, cardinality, encoding, time, identity, ordering or resource ownership. Choose equivalence classes and near-boundary values that distinguish plausible bugs, including meaningful combinations. Do not enumerate the Cartesian product of every input and failure. Include the relevant legitimate workflow so “deny everything” or “never complete” cannot masquerade as a fix.

For significant work, a short scenario record can contain setup, trigger/interleaving, expected outcome, prohibited effects, chosen test level and why it matters. Reuse an existing bug report/contract instead of creating another tracker. Change the scenarios when implementation evidence changes the hypothesis.

## Define an independent oracle

Derive expected results from the user's contract, business rule, accepted specification, independently calculated fixture or simpler reference model. Do not import the production helper to calculate the expected value when that helper is the suspected source of error. A model that repeats the same algorithm and assumptions can share the defect.

Observe the public outcome appropriate to the abstraction. An HTTP test can require status, payload, headers, stored state and relevant side effects. A permission denial may need unchanged records, no queued work and no private fields, not only a 403. A worker test needs committed business effects and recoverability, not just acknowledgment calls. Verify related state rather than asserting an entire unrelated database dump.

Negative assertions need the right observation point: an immediate “no event” check before background work runs is weak. Wait for a known completion/drain/barrier or an explicitly bounded observation window suitable to the contract. A finite window does not prove an effect will never happen. Query durable state through an appropriate fresh connection/session when a stale ORM identity map or uncommitted fixture could mislead the assertion.

Mock call assertions can establish a real interaction contract, retry budget or absence of a duplicate request. Pair them with outcome/integration evidence when the claim is business correctness. Private method names, incidental data structures and arbitrary call order are usually fragile oracles. Internal invariants are appropriate when they are the actual subject, such as a lock owner or serializer contract. Small reviewed snapshots may protect a stable representation; blindly accepting a huge snapshot can preserve the bug.

Expected-error tests must fail if the operation unexpectedly succeeds. Await rejection/exception assertions and ensure catch branches do not silently disappear. Seed valid preconditions so a test cannot pass on an unrelated authentication/validation failure. Use diagnostic assertions to establish the intended path without tightly encoding the implementation.

## Choose stronger techniques when they pay off

| Technique | Useful question | Important limit |
| --- | --- | --- |
| Example/boundary tests | Which concrete input or lifecycle boundary exposes this defect? | More near-identical examples add little confidence |
| Property-based tests | Which invariant or relation should hold across a meaningful generated domain? | Generators/preconditions and the oracle can be wrong; avoid filtering away the interesting cases |
| Metamorphic/differential checks | Which transformation or independent implementation should preserve a specified relation? | Round trips can share bugs; two engines may legitimately differ |
| Stateful/model-based tests | Which action sequence violates an invariant although single actions pass? | Use a simpler independent model and reset state per generated run |
| Fuzzing | Which malformed/edge inputs crash, hang or violate a domain property? | No crash alone does not prove semantic correctness; bound time/memory and preserve failures |
| Controlled scheduling/fault injection | Which interleaving or failure window breaks the workflow? | Only controlled paths are covered; real engine/protocol behavior may need separate integration tests |
| Mutation/fault sensitivity | Would this oracle catch a plausible wrong implementation? | Equivalent mutants, invalid builds and harness failures are not evidence of a missing meaningful assertion |

Use existing fast-check, Hypothesis, native Go fuzzing or suitable project facilities instead of installing a framework for a trivial function. Generate valid states directly where possible, then introduce relevant invalid transitions deliberately. Preserve the minimal failing input/sequence, seed/replay path, tool version and environment needed to reproduce it. Keep sensitive production data out of test corpora and logs.

For a regression, running the same test against the pre-fix implementation is often sufficient sensitivity evidence. Selective mutation can help critical logic when an oracle remains uncertain, but do it in isolated authorized code with changes restored; do not alter unrelated dirty work. Confirm a failure comes from the assertion/behavior, not a syntax error, generic startup failure or unrelated timeout. Do not chase 100% coverage/mutation scores at the expense of clarity or add tests for equivalent mutants.

Sources: [Testing Library principles](https://testing-library.com/docs/guiding-principles/), [fast-check](https://fast-check.dev/docs/introduction/), [Hypothesis state machines](https://hypothesis.readthedocs.io/en/latest/stateful.html), [mutation outcomes](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/), [equivalent mutants](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/), [OWASP testing guide](https://owasp.org/projects/web-security-testing-guide).
