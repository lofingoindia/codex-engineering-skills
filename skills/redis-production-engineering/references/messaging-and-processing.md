# Messaging and processing

## Select the delivery responsibility

Decide whether an event is an ephemeral wake-up/UI hint, replayable history, competing work, or durable business intent. Keep an existing RabbitMQ/queue workflow if its routing, acknowledgments, recovery and operational model fit. Redis deployment alone is not a migration rationale. Lists/sorted sets can implement simple work/delay mechanisms, but removal-before-processing, reservation, retries and crash recovery still need ownership. Reuse a suitable queue library rather than rebuilding it casually.

## Pub/Sub is a first-class ephemeral transport

`PUBLISH` reaches currently subscribed clients; disconnected subscribers miss messages. Delivery is at-most-once, not a durable queue or business acknowledgment. A publish count is not successful downstream processing. Define reconciliation after reconnect when missed hints matter: refresh authoritative state or resume a supported durable cursor. A notification alone cannot record an accepted payment, job or permission revocation.

Scope channels by environment/application/validated tenant and apply channel ACLs plus backend authorization. Pub/Sub crosses logical database numbers. Do not allow an untrusted browser to select arbitrary Redis channels; authorize SSE/WebSocket subscriptions and outgoing data. Subscription cleanup on logout, tenant switch and disconnect must remove old listeners and pending deliveries. Revalidate long-lived connections when permissions change.

Use connection ownership supported by the installed client/protocol; a dedicated subscription connection is often appropriate. RESP2 subscribed connections have command restrictions; RESP3 capabilities do not imply a particular client can multiplex safely. Bound application buffers, fan-out and per-subscriber work; decide whether slow consumers disconnect, drop ephemeral updates or recover via replay. Monitor output-buffer pressure and reconnect storms.

Ordinary Cluster Pub/Sub propagates across the cluster; sharded Pub/Sub (7.0+) confines propagation to a shard using channel slots and compatible clients. Do not interchange `PUBLISH`/`SUBSCRIBE` with `SPUBLISH`/`SSUBSCRIBE` without checking routing and library support. Preserve required ordering explicitly across channels, instances and asynchronous handlers; overlapping pattern/exact subscriptions can deliver the same publication more than once to application code. Reconnection does not recover missed history. Keyspace notifications share the lossy transport and expiry event timing is not precise scheduling.

## Streams require processing and retention design

Define stream partitioning, group purpose, startup position and replay/reset ownership. Members of one consumer group share work; separate groups can consume independently. `XREADGROUP ... >` reads new deliveries; abandoned pending entries need an explicit recovery path. `NOACK` changes the responsibility and is unsuitable for work requiring recovery.

An entry enters a group's Pending Entries List on delivery. Acknowledge with `XACK` after the required effect commits. Crash after effect but before acknowledgment permits duplicate work; crash after an early acknowledgment can lose the effect. Use existing durable idempotency/conditional database transitions for the business operation. Redis receipt, producer deduplication and end-to-end exactly-once effects are distinct claims. Database update plus `XADD` has a dual-write gap; preserve durable intent/reconciliation when necessary.

Inspect `XPENDING`, delivery counts, age and lag. Reclaim abandoned work using supported `XCLAIM`/`XAUTOCLAIM` behavior and a justified idle threshold. Claiming transfers Redis ownership but does not stop the former consumer from committing. Bound batch sizes and outstanding work. Resume recovery cursors correctly; completion of one scan does not mean no entries will become reclaimable later. Verify the installed reply shape: Redis 7.0 changed `XAUTOCLAIM` replies to include IDs of removed entries.

Set retention from replay, slow-group recovery and memory budgets. Ordinary trimming/deletion can remove message bodies still referenced by pending entries. `XACK` does not itself delete the body. Newer `XACKDEL`/`XDELEX` and reference-handling modes change group interactions; use only after checking version and every group's retention needs. A forgotten group can affect acknowledgment-based retention. Consumer cleanup must not discard the only recovery route to pending work.

Bound retries and quarantine poison work with diagnostics and a replay policy. Keep persistence, eviction and failover loss within the accepted delivery guarantee; Streams stored in an evictable cache are not reliably durable merely because they have IDs.

Producer idempotency in 8.6+ uses stable producer/message identities within bounded time/count tracking. Capacity eviction or changing idempotency configuration can remove deduplication history. Content-derived IDs can merge two intentional identical messages. Do not replace consumer/business idempotency with this feature.

## Evidence to select

Derive tests around disconnect/reconcile, crash before/after effect and acknowledgment, overlapping reclaim, poison work and retention racing a slow group. Verify actual business effects and recoverable messages, not just `XADD` success. Sources: [Pub/Sub semantics](https://redis.io/docs/latest/develop/pubsub/), [keyspace notifications](https://redis.io/docs/latest/develop/pubsub/keyspace-notifications/), [Streams](https://redis.io/docs/latest/develop/data-types/streams/), [XAUTOCLAIM](https://redis.io/docs/latest/commands/xautoclaim/), [XACKDEL](https://redis.io/docs/latest/commands/xackdel/), [producer idempotency](https://redis.io/docs/latest/develop/data-types/streams/idempotency/).
