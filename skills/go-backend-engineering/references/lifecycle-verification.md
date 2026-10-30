# Service lifecycle, deployment, observability, and verification

Use for startup/shutdown, recovery, deployment or choosing meaningful checks. Adapt to existing service/framework/supervisor and actual OS/provider constraints rather than adding a lifecycle framework.

## Startup, health and deployment

Validate configuration and initialize required resources through explicit owned startup. Bound waits, surface errors and unwind partial initialization. Publish readiness only after required capabilities work. Do not execute competing migrations in every replica without existing coordination.

Readiness can remove an instance from routing; liveness should not restart every replica merely because a shared dependency is temporarily down. Choose probes and degraded behavior from real service promises, avoiding expensive probe traffic that amplifies an outage. Reuse the supervisor's restart/backoff behavior and keep recovery observable.

Check selected Go/toolchain, GOOS/GOARCH, cgo/native linkage, build tags, CA certificates, DNS/timezone needs, filesystem permissions and runtime config against the production image/host. A Go binary is not universally static or portable across libc/OS architectures. Cross-compiling a binary does not test its runtime integration. Preserve reproducible module/build inputs and scoped rollbacks; do not force Docker, Kubernetes or a new platform.

## Finite graceful shutdown

Identify request, worker, connection and telemetry lifetimes. Use one idempotent owned shutdown path, normally:

1. Signal unready and stop new acceptance/claims, accounting for routing delay.
2. Drain relevant work within the termination budget; then cancel/force according to policy when it cannot finish.
3. Wait for owned workers/connections, close their dependencies after use, and flush necessary telemetry within the remaining budget.
4. Return the intended status through the entrypoint/supervisor.

`http.Server.Shutdown` stops listeners, closes idle connections and waits for active HTTP connections to become idle until its context expires. Serve/ListenAndServe return ErrServerClosed before draining finishes: do not let main return immediately and kill that drain. The server cannot be reused after Shutdown.

Use a shutdown deadline context that is still live, not the already-canceled signal/request context. If cancellation is wired through BaseContext or a shared service context, choose when to cancel it intentionally; canceling every request first can defeat a drain intended to finish writes.

Shutdown does not wait for all background tasks or hijacked connections. RegisterOnShutdown callbacks initiate protocol shutdown but are not completion waits. Track/join required WebSockets, workers, SSE/subscriptions and application goroutines separately. On timeout, forced Close can interrupt ordinary connections but still does not manage hijacked ones. Close pools only after their users finish or are deliberately aborted.

Use `signal.NotifyContext` or existing platform hooks with cleanup; choose supported signals for the real OS. Understand repeated-signal/default behavior and the supervisor's hard deadline. `os.Exit`/fatal logging bypass deferred cleanup, and SIGKILL/crashes bypass graceful hooks. Durable correctness therefore needs transactions/recovery, not a guarantee that shutdown finishes every action.

Recover only at deliberate boundaries. A recover in one goroutine cannot catch a panic in another; some runtime failures are not recoverable. Do not silently swallow programming failures or resume inconsistent shared state. Normal handler errors belong to the request path; preserve safe diagnostics and rely on the existing supervisor when process termination is appropriate.

## Observability that fits the service

Reuse structured logs/slog or existing telemetry and correlation. Track relevant request/dependency latency and errors, pool waits, active/queued work, retries, goroutines, GC and resource pressure. Use bounded-cardinality labels and redact credentials/private data. Context propagation is required for causal traces, not a reason to put arbitrary payloads in context/baggage.

For OpenTelemetry, preserve installed instrumentation/provider ownership, propagate and end spans appropriately, and flush with a bounded live shutdown context. Avoid duplicate middleware/spans and do not register a conflicting global provider over existing automatic instrumentation. Diagnostic data is sampled evidence, not proof that unobserved failures never occur.

## Choose normal checks from the changed invariant

Use the existing module/workspace and scripts. These are options, not an automatic suite:

| Change | Useful verification |
| --- | --- |
| Local implementation/error path | gofmt, focused `go test`, relevant `go vet`/build and regression assertions |
| Shared state/concurrency | Coordinated interleavings and completion assertions; targeted `-race` when platform/cgo/compiler support permits |
| HTTP behavior | httptest handler checks; a real test server when transport, disconnect, streaming or connection reuse matters |
| Transaction/client lifecycle | Disposable integration state or a suitable controlled dependency; observe release/commit/rollback semantics |
| Parser/validation boundary | Seed regression cases and bounded fuzzing when useful; deterministic isolated targets without external side effects |
| Scheduling/timers | Explicit synchronization or supported `testing/synctest`; its fake-time bubble does not make real network/process interactions deterministic |
| Performance claim | Scoped profile/benchmark with comparable workload and correctness checks |

Use repeated/shuffled runs only when investigating order/scheduling sensitivity, recording the seed when relevant. Fuzzing should have a time/resource budget and retained regression corpus; a normal go test executes seeds, not continuous fuzz discovery. Respect tool/platform limits rather than pretending unsupported race/fuzz checks ran. Freshness, durable results, idempotency and tenant isolation need assertions beyond memory race detection.

Discover a small meaningful failure from the actual flow: cancellation while waiting for capacity, a failed scan after resource acquisition, committed work before lost acknowledgement, or a request active during termination. Verify released/settled resources with owned signals/counters; brittle global goroutine counts or arbitrary sleeps do not establish cleanup. Do not call test Fatal/FailNow from an unmanaged worker as a substitute for returning its error to the test owner.

Report exact checks and observed outcomes. Distinguish static review, mocked/isolated behavior, compiled artifacts and deployed evidence. Documentation-only skill creation needs normal validation, not a sample service, agent evaluation, chaos system or benchmark campaign. Passing build/tests does not prove production reliability or complete concurrency correctness.
