# Recovery, overload, and operational evidence

## Retry only with a safety argument

Choose a deadline from user/business needs and dependency behavior. Budget connection, request, processing and retry time across the call chain. Do not give every nested layer an independent full timeout. Propagate cancellation where supported while recognizing that remote work can continue after local cancellation.

Classify transient failures, permanent rejection and uncertain completion. Retry only when the effect is safe or protected, using bounded attempts/time, backoff and jitter, and provider retry signals where applicable. Select one retry owner across SDK, handler and job layers; multiplication can overwhelm a failing dependency. Authentication/validation failures do not become transient merely because a retry library supports them.

Stop with a meaningful pending, failed or reconciliation state when the budget is exhausted. Store durable next-attempt state for work that must survive restarts. A circuit breaker can help a demonstrated repeated dependency failure, but adds states and recovery behavior; reuse an existing mechanism instead of adding one to every integration.

## Backlog, overload, and poison work

Bound admission, in-flight work, concurrency, memory and connections to downstream capacity. More consumers can worsen database/remote-service overload. Consider fair scheduling or scoped quotas when one tenant can starve others, without building a scheduler framework for a small worker.

Observe age of oldest work and end-to-end completion latency, not only queue depth. Distinguish a surge, stalled consumers, dependency saturation and a poison-message loop before scaling. Backpressure and load shedding should preserve accepted durable work or make rejection explicit; silently dropping accepted work violates a different guarantee.

Classify poison payload/version failures, quarantine with enough diagnostic context, and protect sensitive data. Define who can inspect, repair and redrive work, how replay is bounded and how duplicates/obsolete permissions are handled. A DLQ without monitoring and an accountable redrive path is only deferred loss. Avoid automatic endless DLQ-to-main-queue cycling.

## Reconnect, shutdown, and deployment

Reconnect with bounded backoff/jitter, restore supported subscriptions/topology and account for gaps. Socket reconnection is not business recovery. Use replay/resume IDs or refetch authoritative state when supported; explicitly handle unavailable/expired history.

On shutdown, stop accepting/claiming new work, signal readiness appropriately, and drain/cancel in-flight work within the actual deployment deadline. Commit/ack only completed protected work, allowing safe redelivery of unfinished work. Process termination can skip cleanup, so safety cannot depend solely on a shutdown hook. Avoid acknowledging all pending deliveries to make shutdown faster.

Rolling deploys can mix producer/consumer versions. Check contract compatibility, queue/retention changes, worker ownership, retry behavior and rollback paths. Configuration changes can alter durability or delivery even when application code is unchanged. Do not mutate production brokers or kill processes merely to validate a review.

## Observe completion and correctness

Reuse existing OpenTelemetry/logging/metrics. Propagate correlation and trace context through supported message carriers, using appropriate span/link relationships for batches and delayed work. Honor installed semantic-convention versions; messaging conventions can be development status and should not trigger gratuitous instrumentation churn.

Track publication failures/returns/confirms as appropriate, unacknowledged/pending work, redeliveries, retries, dead-letter/redrive counts, processing latency, dependency errors and business completion. Protect labels from unbounded IDs/cardinality and payloads from credential/tenant leakage. Sampled traces cannot establish that an unsampled failure never occurred.

Use reconciliation/consistency checks for the invariant where needed: accepted versus completed operations, intent versus external outcome, or stale pending work. A healthy broker and successful delivery metric do not prove orders were fulfilled exactly once.

## Focus verification on the identified gap

For implementation, choose isolated tests that cross a relevant commit/ack/ownership window. Check final business state after duplicate delivery, lost reply, restart, competing owners, reordered updates or a dependency recovery selected from the actual workflow. Inspect setup/teardown and use disposable infrastructure where required. Normal local tests are sufficient when they establish the changed invariant; do not demand a broad chaos campaign for every edit.

For read-only investigation, inspect code, configuration, existing tests and safe telemetry; report unexecuted crash/failover assumptions. Do not convert a thought experiment into a claimed test. State the guarantee, retention/failure assumptions, evidence, unresolved limits and practical recovery owner.
