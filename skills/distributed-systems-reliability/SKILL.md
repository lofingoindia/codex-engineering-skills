---
name: distributed-systems-reliability
description: Design, review, or repair business workflows spanning services, databases, queues, workers, and external effects. Use for partial failures, delivery guarantees, idempotency, concurrency, or recovery; skip local-only implementation and routine broker setup without a reliability decision.
---

# Distributed Systems Reliability

Preserve the actual business invariant across process, network and durable-system boundaries. Use existing runtime, database, broker and observability capabilities; do not introduce microservices, queues, sagas or distributed locks without a demonstrated need. Companion engineering skills are optional, not dependencies.

## Reconstruct the workflow

Identify whether the request is new design, a focused defect, incident investigation or read-only review. Honor explicit read-only instructions even when a fix is apparent. Inspect actual entrypoints, persisted state, transactions, broker/client versions, acknowledgment and retry settings, workers, external providers and deployment lifecycle.

State the durable business outcome and what must never happen: lost accepted work, double charge, negative inventory, unauthorized processing or an invalid state transition. Trace who accepts responsibility at each step and what survives a crash. Include the user's visible completion/uncertainty state; a successful publish or HTTP response may represent only acceptance.

For relevant boundaries, consider failure before and after the state change, lost replies/acknowledgments, duplicate execution, reordered events, delayed workers and dependency outages. Distinguish a known failure from unknown completion. Timeouts bound waiting; cancellation does not prove a remote action stopped or rolled back.

## Load the relevant reference

| Decision | Reference |
| --- | --- |
| RabbitMQ/Redis/Kafka delivery, acknowledgments, ordering or event contracts | [delivery-and-contracts](references/delivery-and-contracts.md) |
| Database/message atomicity, duplicate effects, leases or competing workers | [atomicity-and-concurrency](references/atomicity-and-concurrency.md) |
| Retries, overload, reconnects, poison work, shutdown and observation | [recovery-and-operations](references/recovery-and-operations.md) |
| Upstream guarantees, specification scope or version caveats | [sources](references/sources.md) |

## Choose the smallest sufficient guarantee

Keep a local operation in a local transaction when that protects the invariant. For work spanning systems, identify the gap between durable intent, delivery and committed effects. Use existing idempotency, conditional state transitions, outbox/inbox or reconciliation where the gap requires them. Do not claim end-to-end exactly-once effects from a broker feature alone.

Document the scope and conditions of the guarantee: persistence/replication, message retention, deduplication lifetime, retry policy, ownership and external-provider capabilities. At-least-once delivery allows duplicates and is still bounded by loss/retention/failure assumptions. A lease, timestamp or in-memory flag is not automatically durable exclusive ownership.

Give each retry path a clear owner, finite budget and safe stopping/recovery condition. Preserve tenant/authorization context and compatibility of event contracts. Prefer existing events over redundant polling; use durable discovery/reconciliation only where the workflow actually needs it. In-memory notifications can wake work but cannot be its sole record when crash survival is required.

## Verify final state and recovery

For real implementation changes, derive focused isolated tests from the identified uncertainty windows. Check durable outcomes after duplicate requests, a relevant crash/redelivery or competing transition, not only a sent message or successful response. Use existing test infrastructure; fault injection against production is outside normal verification.

Read-only reviews use available safe evidence and record the isolated runtime test still needed. Report the failure chain, selected guarantee and its scope, actual test results, operational detection/recovery, and unresolved durability or compatibility limits. Do not assert measured throughput, failover correctness or recovery success without execution evidence.
