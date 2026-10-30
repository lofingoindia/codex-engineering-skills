# Atomicity, ownership and rate limiting

## Use the narrowest atomic mechanism

Prefer an existing command for a Redis-local state change: conditional set, increment or a data-structure operation. Pipelining reduces round trips; it provides neither isolation nor rollback. Bound pipeline count/bytes and inspect individual command errors, including uncertain partial completion after a disconnect.

`MULTI`/`EXEC` executes queued commands without interleaving; runtime command errors do not roll back earlier effects or prevent all remaining commands from running. Check every result. Use `WATCH` when optimistic read/modify/write is appropriate, with bounded conflict retries. It is connection state: isolate the connection for the full watch/read/exec lifecycle rather than sharing it with unrelated concurrent requests. A rejected/conflicted transaction and an unknown outcome after a lost reply are different cases.

Lua/Functions can implement a short Redis-local decision and mutation atomically with respect to other commands. Validate inputs, key types and conditions before writes; runtime errors do not provide SQL rollback. Keep work bounded: long scripts/functions block other command execution. Declare accessed keys correctly, pass data as arguments, and verify same-slot requirements in Cluster. Do not interpolate user input into script source or build one new script per request.

Check deployment/reload behavior: EVAL script caches can be missing after restart, failover or eviction; handle `NOSCRIPT` using supported client facilities without blindly duplicating effects. Functions (7.0+) are persisted/replicated library artifacts but still require deliberate versioning and provisioning across relevant shards. They do not make cross-database/external operations transactional. Do not build a custom scripting framework for a single counter.

## Leases and idempotency have finite scope

A single-instance lease typically needs an unguessable owner token and atomic acquire-with-expiry; release/renew only when that token still matches. Redis 8.4+ conditional commands can replace a small compare/delete script when supported. Plain `DEL` can delete a successor's lease. Failover can lose an acquired lock, and a paused owner can outlive its expiry.

For critical effects, use authoritative conditional/transactional safeguards or fencing accepted and checked by the protected resource. A monotonically increasing token only works with a trustworthy non-regressing issuer and enforcement on every relevant effect; `INCR` in a lossy Redis deployment alone does not establish that. Do not claim exclusive business execution from a lease or a multi-node locking recipe without establishing its failure assumptions.

An idempotency record needs a stable operation identity scoped to tenant/actor, request-payload conflict handling, processing/completion distinction, result semantics and a retention/recovery policy. A `SET NX` claim expiring during an external effect can allow a duplicate. When Redis and the durable effect cannot commit together, use existing authoritative operation state and reconciliation. Expiry, eviction and failover are part of the guarantee.

## Choose quota semantics from the workload

| Mechanism | Useful fit and tradeoff |
| --- | --- |
| Fixed window | Cheap counter; boundary bursts may approach two windows' allowance |
| Sliding log/window | Finer rolling behavior; exact event logs cost memory proportional to admitted traffic; approximations have error |
| Token bucket | Explicit sustained rate plus burst budget |
| Leaky bucket/GCRA | Smooth admission or virtual scheduling; decide rejection versus actual queued shaping |
| Concurrency lease | Bounds in-flight work, not requests per interval; crash/expiry recovery can permit overlap |

Use existing proven implementation if suitable. Make admission, consumption and expiry updates one atomic Redis-local operation where required. `INCR` followed separately by `EXPIRE` can leave an immortal counter after a crash. Define whether rejected requests consume quota and how retries/unknown completion affect charging. If multiple keys/limits require all-or-nothing admission, establish the atomic boundary and Cluster placement rather than assuming a pipeline provides it.

Use validated user/API-key/tenant identities and only trusted proxy information. Shared NAT/mobile IPs need fair limits, not arbitrary bans. Combine endpoint/resource-cost and tenant budgets only when justified; distinguish rate, paid quota and active concurrency. Bound identity length/cardinality, counter lifetime and sliding-history storage so attackers cannot turn the limiter into a memory attack.

Define clock source, units, rollback/skew handling, burst and plan-change behavior. Derive retry timing from actual limiter state; do not give a made-up `Retry-After`. Choose fail-open, bounded local fallback or denial per endpoint's risk; a local fallback is not a global quota. Balance legitimate user access, abuse protection and dependency overload.

## Evidence to select

Check boundary bursts, simultaneous multi-instance admission, missing expiry, quota-change/retry ambiguity and a lease owner paused past renewal. Assert admission/effect counts and fairness, not only script return values. Sources: [transactions](https://redis.io/docs/latest/develop/using-commands/transactions/), [pipelining](https://redis.io/docs/latest/develop/using-commands/pipelining/), [Lua](https://redis.io/docs/latest/develop/programmability/eval-intro/), [Functions](https://redis.io/docs/latest/interact/programmability/functions-intro/), [rate limiting](https://redis.io/docs/latest/develop/use-cases/rate-limiter/), [conditional deletion](https://redis.io/docs/latest/commands/delex/).
