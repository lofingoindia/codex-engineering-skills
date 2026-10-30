# Reproducible asynchronous and integration tests

## Keep the disputed behavior real

Map each claim to the minimum realistic boundary. A service-level test can run application handlers, actual repositories and one local database without deploying the entire product. Keep external payment/email boundaries controlled where the test concerns orchestration; exercise real local transport when sockets, parsing, streaming or disconnect behavior is the subject. An in-process request injector may bypass TLS, routing middleware or serialization; name what it does and does not exercise.

Reuse existing Compose, Testcontainers, service fixtures and configuration. Match relevant engine/client versions, schema/migrations, roles, isolation, extensions, topology and queue/durability settings. A single-node container is not a replica/failover test; a different SQL engine or in-memory fake cannot establish the production engine's guarantees. Check actual application-role behavior where authorization depends on it.

Before mutating setup/cleanup, verify the target and ownership: explicit isolated endpoints, disposable data and scoped credentials. A database name ending in “test” alone is not proof. Do not reset shared/live data or run fault injection against production. Give parallel workers distinct databases/schemas/namespaces/queues/ports or serialize conflicting work; key prefixes alone may not isolate global commands or resource exhaustion. Use dynamic allocated ports and service readiness rather than fixed startup sleeps.

## Control ordering and responsibility

For a race, arrange the relevant operations, wait for each critical read/claim point, then release the competing transition and inspect final state. Promise gates, channels, completers, supported test clocks and existing dependency seams can make this reproducible. Concurrent launch alone does not prove the intended overlap; arbitrary sleeps and repeated stress cannot establish that a particular interleaving occurred. Keep waits bounded and produce useful phase diagnostics so a broken barrier fails rather than hangs.

Do not add production authorization bypasses or a custom scheduler to make a test easy. A small justified seam for an existing clock/adapter can be appropriate. A simulated failure hook can test error handling, but it does not by itself demonstrate process-crash or storage recovery; use an isolated real failure when that is the actual claim.

Test failures on the right side of the effect: before commit, after commit before response/ack, during recovery and after ownership changes, as relevant. Cancellation/timeout does not prove remote work rolled back or stopped. Observe durable outcomes after reconnect/retry, effect counts and stale owners' behavior. Use independent connections/actors for transaction and authorization claims; one transaction or a process-local fake can hide the defect.

For PostgreSQL/MySQL, test actual constraint/isolation behavior and lock-sensitive state transitions with the real engine. Transaction-rollback fixtures do not isolate writes committed by another connection, worker or migration. For Redis, distinguish a controlled application clock from server TTL, atomic scripts, eviction and reconnect behavior. For RabbitMQ, publisher confirms and consumer acknowledgments protect different boundaries; test effect-before-ack/redelivery and duplicate handling with actual compatible broker/client settings when that guarantee matters. Queue-empty or published-message count alone is not successful business processing.

Contract tests validate actual consumer expectations against provider behavior and relevant provider states. A generated schema or mocked successful response is one-sided evidence. Cover meaningful missing/null/type/error/message compatibility without making every incidental field/value rigid. Contract verification does not prove authorization policy, transaction effects, network infrastructure or the full workflow. Reuse existing contracts/provider checks before introducing Pact or a broker service.

## Make isolation and teardown trustworthy

Own every task, server, subscription, connection, temporary path and timer started by the test. Register cleanup after successful acquisition so partial setup failure does not leak earlier resources. Stop intake/cancel work, await owned completion where possible, then close resources in dependency order with a bound. Do not mask the primary failure or silently ignore teardown failures.

Restore mocks, timers, environment, globals, handlers and dependency overrides. Use minimal deterministic fixtures with explicit identities/time zones/order; seeded randomness must remain replayable. Fresh state per generated example is different from fresh state per test function. Avoid shared mutable fixtures or hidden test-order dependencies. Reuse helpers for genuine repeated setup, not a generic test DSL that obscures the behavior.

Fake time is useful for owned application timers, not proof that a real database, network peer or OS clock advanced. Coordinate pending asynchronous work and restore clocks using the installed runner's supported behavior. Bound polling of externally eventual state by a contract-based deadline; polling is an observation mechanism here, not an application freshness architecture. Do not replace a broken synchronization assumption with a larger timeout.

## Diagnose flakes and select checks

Preserve the first failure, seed, test order, relevant logs and environment. Investigate leaked state, unawaited tasks, clock/order assumptions, capacity and real dependency errors. Targeted repetition, shuffled order or parallel execution can diagnose a hypothesis; repeated passing runs do not erase an unexplained failure. If quarantine is necessary, disclose its scope, risk and repair owner instead of presenting the suite as fully verified.

Run the focused regression and affected integration/consumer tests first; broaden for changed interfaces, shared infrastructure or unresolved risk. Confirm the intended tests were collected and executed, with no accidental only/skip/xfail behavior. Keep type/lint/build checks distinct from behavioral tests. Infrastructure failure, unavailable dependency, zero collected tests and a real assertion failure require different reports. Do not mark an unexecuted real-dependency claim PASS because mocks passed.

Sources: [Testcontainers purpose and limits](https://testcontainers.com/getting-started/), [RabbitMQ acknowledgment boundaries](https://www.rabbitmq.com/docs/confirms), [Pact consumer/provider verification](https://docs.pact.io/getting_started/how_pact_works), [flaky-test diagnosis](https://docs.pytest.org/en/stable/explanation/flaky.html), [controlled promise scheduling](https://fast-check.dev/docs/advanced/race-conditions/). Use the installed database/Redis/runtime specialist and target upstream manual for their exact guarantees.
