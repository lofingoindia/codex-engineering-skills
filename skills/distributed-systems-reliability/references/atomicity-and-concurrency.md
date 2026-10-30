# Atomicity, duplicate effects, and concurrent ownership

## Protect the actual transition

Start from business state and its owner. A transaction protects operations committed within its database boundary. A database commit and a separate broker publish or external API call are not automatically atomic, regardless of their proximity in code. Avoid solving a local invariant with distributed infrastructure.

Use constraints, conditional updates or suitable transactions/locks to make competing state transitions safe. A read followed by an unguarded write can oversell stock or execute a terminal action twice. Choose the database/runtime mechanism matching the existing service; retries of serialization failures must repeat the relevant transaction safely, not duplicate unprotected external calls.

## Idempotency and durable intent

For a retriable operation, define key scope, canonical request identity, allowed reuse, result/status storage, concurrent in-progress behavior and retention. Reusing a key with different intent must not silently execute another action. Authorize a caller before returning a previously stored private result. A disabled submit button or process-local set cannot protect multiple processes and restarts.

For a consumer updating its own database, record deduplication and the protected business effect in the same transaction where possible. Marking an event “done” before its effect loses work; recording it afterward in a separate transaction leaves a duplicate window. Concurrent consumers need an atomic claim/unique constraint, not check-then-insert. An inbox record cannot make a separate external side effect atomic.

When committed database state must produce a durable event, an outbox can store state and publication intent in the same transaction. A relay/CDC process sends committed intents and records progress. A crash after publish but before progress recording can republish, so downstream idempotency is still needed. Preserve the required per-entity order and bound outbox growth/lag.

Reuse existing durable jobs, CDC or outbox mechanisms. A wake-up event can reduce latency, while durable intent remains discoverable after a lost notification. Do not add polling where an existing event-driven handoff already meets the guarantee; an appropriate bounded outbox/reconciliation mechanism is a deliberate correctness decision, not blanket polling of application data.

## External effects and unknown outcomes

If a payment/email/provider call times out, determine whether it committed before retrying. Use the provider's supported idempotency key/status lookup and retention behavior where available, binding the same business operation to the same provider request. Do not generate a fresh key on every transport attempt.

Without suitable atomicity or provider idempotency, exactly-once external effects may be unattainable. Store durable intent and observable outcome, reconcile using provider/business identifiers, and expose an honest pending/unknown state. Do not mark unknown as failed and initiate another charge blindly.

Compensation is another business action, can fail, and may not reverse the original action perfectly. Use sagas only when cross-service workflows actually need explicit coordinated states/compensations. Define recovery and reconciliation for failed compensation rather than treating it as database rollback. Distributed transactions require supported participants and operational justification; they are not the default alternative.

## Leases and fencing

Lease expiry or heartbeat loss does not prove an old worker stopped. A paused worker can resume after another owner takes over. Use an ownership/version token checked by the protected state transition, or fencing tokens enforced by the target resource where required. A token passed through logs but ignored by the write target provides no fencing.

Release a lock only if the caller still owns it; do not unconditionally delete another worker's lease. Understand failover, clock/time assumptions and renewal behavior of the installed mechanism. Prefer a local atomic transition when it suffices; do not introduce a distributed lock service to guard one database row.

Partition outages force tradeoffs between accepting work and preserving a strict shared invariant. State what can remain available under degraded conditions and what must defer/reject. Preserve durable recovery paths and explicit ownership rather than letting two sides assume exclusive authority.
