---
name: redis-production-engineering
description: Design, implement, troubleshoot, optimize, or operate Redis-backed applications and infrastructure, including caching, messaging, atomic state, tenant isolation, and recovery. Use for Redis-specific engineering decisions; skip unrelated backend work and trivial command edits.
---

# Redis Production Engineering

Make Redis's actual guarantees fit the application's responsibility. Preserve sound clients, utilities, topology and authoritative storage. Redis is more than a cache, but its presence does not justify replacing a database, RabbitMQ, an existing queue or another working mechanism.

## Reconstruct the responsibility

Identify the task: new capability/infrastructure, focused repair, performance investigation, operational change or read-only audit. Inspect applicable instructions and only the relevant producers, consumers, key builders, database writes, client configuration, deployment and tests. Expand when a real dependency appears. Honor read-only scope across tools and companion skills.

Establish configured, installed and deployed server/client versions, distribution/edition, enabled capabilities, RESP mode and topology. Record what remains unknown. A managed service or Redis-compatible product may differ from Redis Open Source. Check version-matched command history, client APIs, release notes and relevant source/tests before selecting newer behavior. Do not upgrade merely to use a convenient command.

For each affected responsibility, identify the authoritative state, validated tenant/actor, allowed staleness/loss, retention, atomic boundary, cardinality, peak load and recovery objective. Determine behavior on timeout, unknown completion, eviction, restart and failover. Disposable cache, session/revocation state, work queues and coordination may require different resource and durability policies; logical databases do not isolate security or capacity.

## Load only the needed guidance

| Current decision | Conditional reference |
| --- | --- |
| Freshness, repeated misses, stampedes, invalidation or L1 caching | [Caching and freshness](references/caching-and-freshness.md) |
| Pub/Sub, real-time fan-out, Streams, consumer groups or queue choice | [Messaging and processing](references/messaging-and-processing.md) |
| Atomic updates, Lua/Functions, leases, idempotency or quotas | [Atomicity and rate limiting](references/atomicity-and-rate-limiting.md) |
| Key design, ACLs, tenant isolation, client retries or connections | [Tenancy and clients](references/tenancy-and-clients.md) |
| Linux/containers/managed service, topology, memory, recovery or diagnosis | [Infrastructure and recovery](references/infrastructure-and-recovery.md) |
| Data-structure selection, advanced features or compatibility | [Capabilities and compatibility](references/capabilities-and-compatibility.md) |
| Upstream evidence, source observations or further targeted research | [Research index](references/sources.md) |

Do not load all references for a localized problem. Reuse existing research when applicable; investigate consequential uncertainty with available `engineering-research-intelligence` guidance. Complement database, runtime, authorization, security or distributed-workflow skills only when their boundary is involved; they are not prerequisites. Use orchestration/audit skills when the actual scope calls for them, without weakening user restrictions.

## Protect the actual invariant

Choose the smallest mechanism that satisfies the workload. Redis-local atomicity does not cover database transactions or external effects. Pipelining is not a transaction; transactions and scripts are not SQL rollback. A timeout does not establish that a command failed, a lease does not stop its former owner, Pub/Sub is not durable delivery, and replication is not strong consistency. Cache hit rate and `PING` do not establish business correctness.

Explain the chosen failure policy per responsibility. Reuse existing reconciliation, idempotency and authoritative checks where necessary; do not add a scripting framework, Cluster, Sentinel, locks, polling or a second client system without a concrete benefit. Keep tenant and permission context intact through reads, events, caches and recovery.

## Verify proportionately and report

Derive failure scenarios from the real call path: pause between the authoritative read/write and Redis update, lose the reply after execution, or let ownership/authorization change while work remains in flight. Select relevant isolated tests and assert final application state and user-visible recovery, not only command success. Normal documentation/configuration validation is sufficient for a skill-only change; do not create a benchmark or agent-evaluation campaign by default.

For operational changes, verify effective configuration and recovery behavior in an authorized environment. Never infer restore, failover, security or throughput success from research alone. Avoid destructive production experiments. Report the local finding, compatibility/guarantee limits, selected change, actual checks, application impact and remaining uncertainty. Do not claim tests or measurements that were not executed.
