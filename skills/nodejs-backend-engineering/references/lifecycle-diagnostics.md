# Process lifecycle, diagnostics, and recovery

Use for startup, termination, production incidents, memory growth, observability, or measured performance work. Adapt to the framework, supervisor/provider, OS, replica count, and actual signal/deadline behavior.

## Startup and health

Validate configuration and initialize required dependencies through owned startup code. Do not expose readiness before required initialization completes. Bound startup waits; clean up earlier resources if later initialization fails. Avoid migrations or destructive initialization in every replica unless the existing coordination model safely supports it.

Readiness means this instance can serve its promised work. Liveness should identify an unrecoverable/stuck instance, rather than restart every replica whenever a shared dependency fails. A startup probe may need different timing. Choose health behavior from actual routing and recovery needs; deep per-probe dependency queries can amplify an outage. Preserve a useful degraded mode when the product allows it.

## Graceful shutdown with a finite budget

Use the framework's supported hooks and one owned, idempotent shutdown path. Avoid installing signal handlers in reusable modules on import. For a persistent service, the relevant ordering is generally:

1. Mark the instance unready and stop accepting/claiming new work, accounting for proxy removal delay.
2. Drain in-flight requests/jobs within the deployment's termination budget; handle idle and upgraded connections explicitly.
3. Close dependencies after their users finish, and flush required telemetry within the remaining time.
4. Set the intended exit status and allow normal exit when possible; enforce a bounded fallback if work cannot settle.

Modern Node.js `server.close()` behavior for idle keep-alive sockets differs from older releases. Force-closing connections can interrupt active requests and does not cover all upgraded connections; follow the matching Node/framework documentation. Track and close WebSockets/SSE, worker threads, timers, and subscriptions where they keep the process alive. Do not close the database pool before draining handlers that still need it.

Handle repeated termination requests without duplicate cleanup. Platform signal support differs, particularly on Windows and serverless runtimes. Do not assume SIGTERM is always delivered. `process.exit()` can truncate pending output; `exit` hooks cannot await asynchronous cleanup, and `beforeExit` is not a general shutdown signal handler. `unref()` means a resource will not keep the process alive, not that its work is durable.

Abrupt termination and machine failure bypass graceful hooks. Correctness must come from transactions, durable ownership, and replay semantics, not shutdown completing every operation. For a long-lived worker, coordinate claim/acknowledgement behavior with its queue. For serverless, follow the provider's invocation and cleanup contract instead of adding a generic signal manager.

An uncaught exception can leave the process in an undefined state. Do not add global handlers that swallow errors and continue service. Preserve minimal safe diagnostics and terminate under the existing supervisor's recovery policy; cleanup at this boundary is not equivalent to ordinary graceful shutdown. Check unhandled-rejection behavior for actual Node flags/version. Expected request failures should already be handled at their owning boundary.

## Diagnose before tuning

Start with a bounded incident window, recent changes, affected operations, and the service's latency/error/resource signals. Distinguish application time from dependency and queue time. Reuse existing telemetry; do not introduce a new monitoring stack to diagnose one endpoint.

| Signal | Interpretation and next evidence |
| --- | --- |
| Event-loop delay/utilization | Correlate with callback duration and CPU profiles. Utilization is not CPU percentage; delay histograms may be in nanoseconds |
| High latency with low CPU | Inspect dependency time, pool acquisition, throttling, retry amplification, and queued work |
| CPU or throughput pressure | Separate JS hot paths, GC, native work, serialization, and logging; profile representative inputs |
| Growing heap versus growing RSS | Inspect V8 heap, external/ArrayBuffer allocations, native memory, and process limits separately |
| Increasing active work/connections | Find stalled requests, unread bodies, lost releases, listeners, timers, subscriptions, and unbounded queues |

Look at distributions and tail latency, not average request time alone. Define a comparable workload and success criterion before optimization. Tune one evidenced bottleneck and verify correctness plus the intended metric. More replicas, a bigger heap, more threads, or a larger pool can amplify pressure elsewhere.

## Memory and diagnostic safety

Differentiate normal warmup/cache growth from sustained retained growth under comparable completed work. Inspect bounded caches, listener/subscription lifetimes, closures, AsyncLocalStorage stores, Buffers retaining large backing allocations, and pending work. Not all RSS is JavaScript heap; raising `--max-old-space-size` does not fix a leak and can exceed container memory once native/external allocations are included.

Use the least disruptive diagnostic that answers the question. A heap snapshot stops the main thread and may require roughly twice the heap memory, risking a crash. Collect only on an appropriate isolated/redundant instance with authorization; protect snapshots, reports, and profiles because they may contain secrets or user data. Do not expose the inspector publicly. Manual GC or arbitrary V8 flags are not routine production cures.

For request/job correlation, scope AsyncLocalStorage with `run` and a small context. Avoid retaining entire requests, response bodies, or credentials. Repair demonstrated context loss with supported APIs rather than spreading global ambient state. Initialize existing OpenTelemetry instrumentation early enough for the actual ESM/CommonJS loading path; duplicate providers/instrumentation can duplicate spans. Use bounded-cardinality metrics, sampling/redaction, and finite export shutdown.

## Proportional verification

Reuse project scripts and test facilities. A focused lifecycle change may need a failed partial startup, repeated shutdown call, or termination while one request/job is active. Assert both completion/recovery semantics and released resources. A module change may need type checking plus starting the built output. A diagnostics-only change may need configuration validation and inspection of redaction/cardinality.

Do not require load tests or chaos infrastructure for every edit. Use profiling or load evidence when the actual task makes a performance/concurrency claim. Record which checks ran, what was simulated, and which deployment/provider behaviors remain unverified.
