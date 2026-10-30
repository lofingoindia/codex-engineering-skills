# Integrity, measured workload and safe evolution

## Protect transitions under concurrency

State the business invariant before selecting isolation or locks. Two concurrent operations can each validate successfully against an old view and together violate a capacity, balance or membership rule. Trace the complete transition, including all affected rows/documents and external effects, not just one statement. Distinguish statement atomicity, transaction isolation, durable commit, replica visibility and crash recovery.

Choose the narrowest sufficient supported mechanism: constraint, conditional mutation, optimistic version predicate, focused row/aggregate locking or stronger isolation with appropriate retries. Do not assume a transaction wrapper prevents lost updates or write skew. Check affected-row/result semantics and uniqueness conflicts; read-then-insert and read-then-overwrite are not generally safe under contention. An upsert is not a universal idempotency mechanism; verify the engine's conflict target, row locks, trigger behavior and returned state.

Keep the transaction on its owned connection/session. Use a consistent acquisition order where practical, avoid network/user waits while holding locks and bound operation/lock budgets. Deadlock/serialization retries may need the whole transaction with a fresh view; timeouts can abort a statement or a transaction differently by engine. A lost commit reply is unknown completion, not proof of rollback. External charges/messages are not undone by rolling back a database transaction; use existing durable idempotency/outbox/reconciliation where that boundary matters.

## Diagnose real queries and index costs

Capture actual ORM/generated queries, bound-parameter types, result volumes, frequency, tenant skew, data distribution and existing indexes/statistics. Establish whether delay is database execution, lock wait, connection acquisition, network transfer or application processing. A small test fixture cannot establish selectivity or a production plan.

Use the engine's explain/profile facilities with their actual effects understood. `EXPLAIN ANALYZE` can execute statements and functions; rollback does not undo every side effect. Keep live inspection bounded and authorized. Compare estimated and actual rows where safe, scanned versus returned data, sorting/spills, join strategy, CPU/I/O and lock time. Planner cost numbers are not cross-engine milliseconds.

Design an index for a query family and enforcement requirement, considering equality/range predicates, ordering, projection, collation/expression compatibility, cardinality and engine-specific access rules. “Most selective first,” “index every foreign key,” and “every WHERE column needs an index” are not universal prescriptions. Composite, partial, covering, expression and specialized indexes have different support and costs. A constraint's supporting index and an apparently overlapping index may have different semantics; verify before removing either.

Balance reads against index writes, logging/WAL/redo, storage, cache pressure, replication and maintenance. An apparently unchanged upsert can still lock/log. Fix N+1 and wasteful round trips when they matter, but do not replace several efficient queries with a large join that multiplies rows or increases lock duration. Stable keyset pagination may help deep traversal; define tie-breakers and concurrent change semantics rather than claiming it is a snapshot. Keep efficient offset pagination where it fits.

Denormalization/materialization needs measured benefit, source-of-truth ownership, consistency/lag and a rebuild path. Adding a read replica can introduce stale reads; partitioning can complicate uniqueness and retention; sharding adds cross-shard constraints, transactions and rebalancing. First check query shape, indexes, connection use and contention. Introduce analytical isolation or another engine only when these tradeoffs fit actual workloads.

## Evolve with existing consumers and data

Inspect migration history and actual catalog state, all relevant readers/writers, deployed version overlap and representative existing data. Preserve applied migration integrity; use the project's established runner and locking, not a parallel migration system. A runner's transaction option cannot override engine DDL semantics.

Before a structural change, establish supported algorithm, lock/rewrite behavior, scan/validation work, temporary disk/log growth, replication impact and recovery. “Online” does not mean no blocking or resource cost. Additive changes can still break positional inserts, whole-row decoding, defaults, validations or old writers. Narrowing types/collations, changing nullability, adding uniqueness and changing referential actions need explicit existing-data checks.

Use expand/contract when consumer overlap or data transformation requires stages; a small compatible change need not become a rollout framework. For staged changes define which representation is authoritative at each point. Dual writes can diverge; reconcile and verify before switching reads or removing old storage. Retrying a backfill must not overwrite a newer live update. Choose bounded, resumable, idempotent batches where scale requires them, with progress, throttling and interruption recovery. Do not silently swallow failures and mark work complete.

Verify final coverage/values, nulls/duplicates/orphans, required constraints and relevant application behavior, not only migration exit status or equal row counts. Tighten enforcement and remove legacy structures only after prerequisites are established. Data/schema rollback may be incompatible with newer writes; a forward correction or compatible restore can be safer than a destructive down migration. Obtain actual authorization for destructive changes and unapproved backfills; earlier authorization remains valid within scope.

## Keep production guarantees explicit

Budget connections across replicas, application instances, jobs and migration tools. Protect tenant data with validated scope, scoped relationships/uniqueness and the existing authorization model. Apply least-privilege roles, parameterized values and allowlisted dynamic identifiers; protect secrets, sensitive diagnostics and backups. Do not impose RLS or database-per-tenant without a matching need and supported engine.

Observe relevant tail latency, errors, waits/deadlocks, pool queueing, storage/log growth, maintenance, replication lag and migration progress through existing tools. Bound labels/samples. Define retention/archival and deletion propagation across projections, caches and backups. Availability, replication, backups and point-in-time recovery are separate capabilities. Specify RPO/RTO and verify an authorized isolated restore before asserting recoverability; a replica or a successful backup command alone is insufficient.

Sources: [PostgreSQL plan behavior](https://www.postgresql.org/docs/current/using-explain.html), [MySQL online DDL operation matrix](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html), [GitLab backfill practice](https://docs.gitlab.com/development/database/batched_background_migrations/), [case-study applicability](sources.md).
