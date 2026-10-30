# Networking, duplicate work, cache correctness, and offline behavior

Use for client integration, repeated calls, stale results, mutation recovery or local synchronization. Reuse the installed client and data/state architecture.

## Trace the actual request lifecycle

Reproduce one relevant journey and correlate endpoint/method, caller, request key, timing, retries and backend execution. Distinguish rebuilds/listener notifications from HTTP attempts and business effects. Investigate the evidence for new Futures during build, recreated state owners, dependency/route updates, multiple consumers, duplicate listeners, overlapping search/pages, resume refreshes, and auth/retry behavior.

Assign one owner to the read/result at the appropriate scope. Deduplicate only equivalent work, keyed by response-varying inputs and user/tenant/visibility. One canceled consumer must not accidentally invalidate another's required shared request. Keep legitimate refresh/freshness behavior; a lower count is not a success if data is stale or private data crosses accounts.

Do not add another HTTP wrapper, global cache, blanket keep-alive, or full state-library migration to conceal duplicate ownership. Measure before/after requests under comparable navigation and freshness conditions.

## Client and operation lifetimes

Reuse a suitable HTTP/Dio client and close it at its actual owner's lifetime. Understand platform adapters, TLS, redirects and cancellation support. A Future timeout does not stop the underlying request; use the installed client's supported abort/cancel mechanism and bound body consumption too. Canceling one screen should not close a shared client used by the whole app.

Normalize transport, timeout, cancellation, HTTP, decoding, validation, authentication and permission failures into the existing error/state model. Check the operation's documented success/body contract, including no-content responses; do not hard-code an example's 200/201 list or JSON-decode every success. Validate untrusted fields and sizes. Do not turn malformed data or server failure into an empty collection.

For concurrent 401s, coordinate refresh using the existing session owner, bound retries, exclude refresh itself from recursive interception, and replay only safe operations. Do not let an old-account refresh revive a logged-out session. A queued interceptor alone does not establish business idempotency or solve all refresh races.

Retry classified transient failures with bounded attempts/total budget/backoff, respecting existing client/server policy. A timeout/disconnect after an order/payment/upload can mean the server committed. Recover by stable operation identity/status rather than blindly creating another action. Disabled submit UI is not a backend replay guarantee.

Bound parallelism, payloads, files, decoded memory and queued work proportionately. Keep independent reads parallel when it helps without causing a dependency flood. Stream large transfers when supported, handling progress and partial-file cleanup; do not buffer entire media objects merely to update a progress indicator.

## Search, pages, and mutation consistency

Cancel or reject obsolete query generations when filters change quickly. Use all response-varying parameters in keys; a mounted result target can still be obsolete. Reset pagination for a new filter, avoid overlapping load-more requests, merge/deduplicate by stable item identity and honor the server's cursor/order semantics. Stable scrolling must not mix two result sets.

After a confirmed mutation, update/invalidate the state/cache that actually feeds the UI. Avoid combining unconditional navigation refresh, provider invalidation, manual refetch and event refresh if they repeat the same work. Optimistic changes need rollback/reconciliation and must not silently overwrite a concurrent update. Mutation success followed by read failure is a refresh problem, not permission to repeat the write.

## Select the necessary offline guarantee

| Product need | Proportionate behavior |
| --- | --- |
| Online-only operation | Explain unavailability, preserve recoverable input and offer a safe retry/status check |
| Offline reads | Bounded scoped local cache with freshness/version metadata and clear stale/offline presentation |
| Offline writes genuinely required | Durable account-scoped pending operations, stable IDs, retry/expiry/conflict policy, and visible queued/failed/synced outcomes |

A connectivity indicator is a hint, not proof of backend reachability. Captive portals, DNS, TLS and service failures need actual request handling. An app does not need an offline-write engine merely because a network error is possible.

When offline writes are required, persist the operation before acknowledging it as queued; bind it to the intended identity and resource version. Define restart recovery, ordering, deduplication and conflict resolution with the backend. Do not automatically replay old-user work under a new account, report queued as server-confirmed, or promise exactly-once execution from a local request table.

Use existing storage/repository facilities and migration practices. Choose encryption, backup/restore policy, retention/eviction and deletion from data sensitivity. Preferences are suitable for small noncritical settings, not automatically for secrets or a durable transaction queue. Test interrupted writes/migrations when touching them; a future OS lifecycle callback is not a reliable persistence strategy.

Use server events/push as freshness signals where supported, with reconciliation after gaps/resume. Polling, sockets and timers are not automatically required. A cache invalidation/event is not a durable command acknowledgement.
