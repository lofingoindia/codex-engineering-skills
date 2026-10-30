# Dependency integration, caches, and durable jobs

Use when a Node.js service owns database/Redis clients, jobs, or side effects spanning dependencies. Inspect the installed client's lifecycle and failure semantics; do not assume APIs are interchangeable across libraries or major versions.

## Client and connection ownership

Reuse clients/pools at the scope supported by the deployment. A long-lived process normally should not create a database or Redis connection per request. Serverless reuse and disposal depend on the provider, invocation concurrency, and driver; do not assume an indefinitely running process or close a shared pool after each invocation.

For each relevant dependency, establish acquisition bounds, connect/operation timeouts, failure/reconnect behavior, health signals, and shutdown ownership. Release acquired resources in `finally`, including when decoding or authorization fails. Handle documented client/pool error events as well as returned Promise rejections. Avoid logging credentials or untrusted full responses.

Pool capacity is multiplied by replicas, workers, rollout overlap, and auxiliary clients. Larger pools can move contention into the database. Observe acquisition wait, active/idle clients, timeouts, and downstream capacity before changing limits. Connection acquisition can consume the entire request deadline even when queries themselves are fast.

Use a single checked-out connection for a transaction; for example, node-postgres transactions cannot be implemented by unrelated `pool.query` calls. Roll back and release safely. Do not hold a transaction open while waiting on unrelated remote calls. Tenant/session settings must have the correct lifetime and be reset or transaction-local so a pooled connection cannot leak identity. Parameterization and least-privilege roles remain necessary.

A disconnected query or timed-out commit may have succeeded. Releasing a connection does not cancel a query; aborting an HTTP request does not roll back a database transaction. Inspect driver cancellation/discard rules and preserve a recoverable operation identity when writes have ambiguous outcomes. Defer SQL isolation/index/migration design to the actual database semantics, not a JavaScript mutex.

## Redis and application caches

Treat a cache as an explicit consistency and ownership decision. Define key namespace, user/tenant/authorization scope, value schema, freshness, eviction/invalidation, and failure policy. Never cache private data under a tenant-free or identity-free key when visibility differs. Bound process-local maps and distinguish them from shared state across replicas.

Reuse the existing cache system. Prefer eliminating redundant work before adding another cache. Where concurrent misses matter, use suitable deduplication or bounded refresh behavior; avoid simultaneous retries/refreshes becoming a cache stampede. A cache outage must not produce unlimited database fall-through. Security decisions need a revocation/staleness policy; a stale-while-revalidate display cache is not automatically safe for authorization.

Redis clients may reconnect and queue commands while offline. Inspect queue limits, expiry, retry, and replay behavior for the installed client. A delayed or repeated command may no longer be valid, especially for non-idempotent operations. Do not treat a disconnected client's queue as durable business storage. Redis persistence, failover, and locking guarantees depend on the actual deployment; a TTL lock alone does not prove exclusive execution after lease expiry.

## Durable background work

Choose a durable job only when work must survive the request/process, be scheduled, or be independently retried. Reuse the broker/queue and worker architecture already present. An unawaited Promise, in-memory queue, or timer is insufficient for work that must survive a crash.

For the changed job, identify its durable input, operation identity, claim/lease, side-effect commit, acknowledgement, and recovery point. A broker confirmation and a consumer acknowledgement protect different boundaries. Acknowledge after the required durable business effect, not after merely starting it. If the effect commits and acknowledgement is lost, redelivery must not repeat the effect unsafely.

Idempotency must cover the durable side effect, with appropriate key scope and atomic duplicate handling. An in-memory completed-ID set or a preflight existence check is not a crash-safe concurrent guarantee. Do not promise exactly-once processing from acknowledgements or retries alone. For database-and-broker dual writes, use an existing transactional outbox or justified coordination when losing either side is unacceptable; do not add one for every event by default.

Bound worker concurrency, broker prefetch, queued memory, retry count/age, and downstream load. Back off classified transient failures. Poison jobs need a visible terminal/dead-letter path and an intentional replay procedure. Preserve original operation identity during replay. Do not retry validation or authorization failures indefinitely.

Long CPU callbacks can block lease renewal and cause simultaneous processing by a replacement worker. Lease expiry, cancellation, and shutdown do not guarantee the first worker stopped. Use broker-supported lock handling and durable safeguards/fencing where required by the invariant. Progress reports should reflect committed checkpoints, not imply completion before durable work finishes.

On shutdown, stop claiming work before draining active tasks. Finish, checkpoint, or release/requeue according to actual broker semantics and the remaining termination budget. Detached follow-up work must not be silently abandoned after acknowledgement.

## Evidence to select

For the touched boundary, test a failed acquisition, thrown error after checkout, account/tenant switch, offline command replay, or crash/redelivery between effect and acknowledgement. Use isolated state. Verify the durable outcome and resource release, rather than only counting handler calls. Reuse existing integration tests; a new queue, cache, or simulator is not a prerequisite for an ordinary repair.
