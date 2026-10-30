# Delivery, ordering, and event contracts

## Separate acceptance from completion

For every handoff, determine whether success means local buffering, broker acceptance, replicated persistence, consumer delivery, transaction commit or completed business action. Delivery guarantees apply within documented boundaries and failure assumptions, not indefinitely under every retention, disk-loss or operator-deletion event.

| Mechanism | Relevant guarantee and limit |
| --- | --- |
| Synchronous HTTP/RPC | A reply can be lost after commit; timeout leaves an uncertain outcome unless the protocol provides an authoritative status/idempotency path |
| Redis Pub/Sub | Ephemeral at-most-once fan-out; disconnected subscribers miss messages and cannot replay them |
| Redis Streams | Retained stream plus consumer-group progress; durable outcomes still depend on persistence/replication, retention, reclaim and application commit behavior |
| RabbitMQ | Confirms and acknowledgments cover different handoffs; queue type, durability, publication mode, routing and client behavior determine safety |
| Kafka | Partitioned retained log with producer/transaction/offset guarantees in their actual configuration; external effects need their own coordination |
| SSE/WebSocket | A live transport, not a durable business ledger; reconnect/replay requires application support and authoritative state |

Use the mechanism already suited to the product. An ephemeral UI invalidation can refetch authoritative state; a payment or order job cannot rely on an offline subscriber receiving a notification.

## RabbitMQ

Publisher confirms acknowledge broker-side handling, not consumer completion. An unroutable publication can still receive a confirm; verify required routing using supported mandatory/return handling or the intended alternate routing design. Treat a missing confirm as uncertain and republish safely with stable event identity if appropriate.

Inspect durable queues, persistent messages, queue type/replication and confirmation requirements together. A durable queue alone does not make every publication durable. Broker/channel recovery must restore intended topology and consumers using the actual client's semantics.

Consumer acknowledgments should follow the protected durable effect or durable handoff that transfers responsibility. A crash after commit but before acknowledgment permits redelivery, so effects must tolerate it. Acknowledging before commit can lose work. Delivery tags are channel-scoped; do not acknowledge old deliveries on a recreated channel. Bulk/multiple acknowledgments must not cover unfinished concurrent work.

Bound in-flight deliveries using appropriate prefetch/concurrency. Requeueing an immediately failing message forever can create a hot loop. Inspect rejection/dead-letter behavior and the destination's safety guarantees; a DLQ is neither automatic successful processing nor necessarily a lossless transfer under every configuration.

## Redis Streams and Kafka

For Streams, inspect the consumer group's pending state, acknowledgment point, reclaim policy and lag. Reclaiming an old pending item does not prove the previous worker stopped; duplicate ownership still needs safe effects. Acknowledgment does not delete the stream entry, and trimming/retention can remove data needed by delayed or recovering consumers. Do not assume replay history survives the selected Redis persistence/failover configuration.

For Kafka, distinguish producer retry deduplication from application-level request deduplication. Transactions can coordinate applicable Kafka writes and offsets; they do not atomically commit an arbitrary external database or payment call. Inspect auto/manual offset commits, rebalances, isolation settings and client version. Committing past unfinished concurrent records can skip work on restart.

Ordering is scoped: partitions, keys, channels and consumer concurrency matter. Broker FIFO does not prove effects complete in order after retries or redelivery. Use per-entity versions/sequence checks, commutative operations, conditional transitions or an explicit gap/replay policy where order matters. Do not rely on wall-clock timestamps as a global causal order.

## Contracts and identity

Define stable event identity, producer/source, type/schema version, owning tenant/resource and required payload. Keep event identity stable across delivery retries; distinguish an attempt ID from the original operation. Deduplication scope must include the intended consumer and identity namespace, not just a guessed globally unique string.

CloudEvents can standardize an envelope but does not guarantee delivery or authorize its payload. Preserve producer/consumer compatibility during rolling upgrades; allow expected additive fields, handle unsupported versions deliberately, and keep generation/schema ownership reproducible where used. Trace/correlation metadata is diagnostic input, not authorization evidence. Avoid unnecessary sensitive payloads and retain enough authoritative state for recovery.
