# Database, cache, broker, and durable-work integration

Use when a Go path owns pooled resources, transactions, external effects, jobs or subscriptions. Check the installed client's concurrency, cancellation, retry and close semantics before using a familiar pattern.

## Database ownership and driver distinctions

`sql.DB` is a concurrency-safe pool handle, not one transaction/connection. Reuse it and verify connectivity appropriately when startup requires it; opening a handle need not establish a connection. Inspect native driver pools such as pgxpool instead of putting a second custom pool around them.

Account for pool capacity across replicas, worker groups, deployments and administrative clients. Observe acquisition waits, in-use/idle connections, timeouts and `DB.Stats`/driver metrics before increasing limits. Nested acquisitions while holding all pool capacity can deadlock the application. Tune max-open/idle/lifetime settings to workload and server capacity, not universal numbers.

| Resource | Required ownership decision |
| --- | --- |
| Rows/query result | Close on early exit; check Scan and iteration errors, including Rows.Err after the loop. Do not assume an empty result means a successful query |
| Transaction | Keep all statements on its Tx/connection, arrange rollback on error/early return, check Commit, then release according to the driver |
| Dedicated connection/prepared statement | Close/release the acquired object at its documented lifetime; do not retain request-owned state globally |
| Pooled session/tenant settings | Bind to the correct transaction or reset safely before reuse; another caller must not inherit identity or settings |

Do not mix DB/pool calls into an intended transaction or hold transactions open around unrelated network waits. Parameterization and backend constraints remain necessary even with an ORM. Concurrent use of a pool is different from concurrent use of a connection/Tx; pgx connections are not a general shared concurrent client.

`database/sql.BeginTx` ties context cancellation to automatic rollback and Commit failure. pgx/pgxpool Begin contexts affect beginning the transaction and do not provide the same automatic rollback. Explicitly finalize native transactions. After cancellation, cleanup may need a separate bounded context or driver disposal path; do not assume a canceled context can complete rollback. Read the installed driver's contract.

A failed connection, cancellation or uncertain commit can leave an ambiguous business result. Do not blindly re-execute writes. Protect durable invariants with transaction/constraint/operation identity and inspect authoritative status. PostgreSQL isolation, schema/index and migration decisions belong to the actual database semantics; local Go synchronization cannot replace them.

## Redis, caches, and other clients

Reuse established clients and verify their concurrency and lifecycle rules. Bound pool acquisition, command time, retries and outstanding work. A method accepting Context may only honor it at one phase: for example, documented AMQP publish variants can check cancellation before starting while not interrupting in-flight I/O. Never infer cancellation from a method name.

Inspect automatic retries/reconnect, command replay and backoff before adding application retries. A timed-out Redis increment, publish or external side effect may already have happened. Reconnection must not duplicate consumers/subscriptions or retain stale channels. Broker confirmations and cache operations do not create an atomic business transaction across services.

For a cache, define tenant/user/permission key scope, value schema, freshness, invalidation, capacity and outage behavior. An in-process map differs from fleet-shared state. Concurrent miss deduplication must not combine callers with different authorization or let one canceled caller improperly control all others. Bound refresh/fall-through so a cache outage cannot flood the database. TTL alone does not establish revocation or distributed lock safety.

For gRPC, propagate appropriate deadlines and inspect supported retry/connection behavior. For object storage, handle streaming completion, cancellation and multipart abort according to the actual client. These are client boundaries, not reasons to introduce a universal integration wrapper.

## Jobs and delivery guarantees

A goroutine, channel, timer or detached context is not durable work storage. Use the existing durable job boundary when work must survive a request/process; a simple supervised in-process task is sufficient when loss/restart semantics allow it.

For a changed job, trace durable input, stable identity, claim/lease, business effect, acknowledgement and recovery point. Acknowledge after the required durable effect, not merely after launching a goroutine. If the effect commits and the acknowledgement is lost, safe redelivery still needs durable idempotency. In-memory ID sets and check-then-act code are insufficient under crashes/concurrent workers.

Publisher confirms, consumer acknowledgements, message persistence and application effect commits protect different boundaries. Do not claim exactly-once processing from any one. Use a justified existing outbox/coordination pattern for database-plus-broker effects that cannot tolerate a dual-write gap; do not add one to every notification.

Bound worker concurrency, prefetch, queued bytes, retry attempts/age and downstream pressure. Classify permanent failures; poison messages need visible terminal/dead-letter handling and controlled replay using original identity. Avoid immediate infinite requeue loops.

Leases can expire while an original worker is still running. Cancellation is cooperative and cannot prove exclusive execution; use actual durable safeguards/fencing when required. Preserve committed checkpoints and do not report progress as completed durable work prematurely.

On shutdown, stop new claims, then finish/checkpoint/release active work under the available budget. Do not acknowledge interrupted work as successful or close required clients before workers finish. Verify the affected acquisition/finalization, retry/redelivery or identity boundary with isolated state rather than introducing another queue/client framework.
