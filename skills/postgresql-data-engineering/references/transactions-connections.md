# Transactions, concurrency, and connections

State the invariant before selecting isolation, locks or retries. Trace the whole application/worker unit of work, including its connection, error handling, commit and external effects. A transaction around incorrect logic remains incorrect.

## MVCC and authoritative writes

At READ COMMITTED, ordinary statements obtain new snapshots; two SELECTs in one transaction need not see the same data. PostgreSQL REPEATABLE READ stabilizes the snapshot but can still allow serialization anomalies such as write skew. SERIALIZABLE can reject conflicting executions and requires whole-transaction retry. Read Uncommitted behaves as Read Committed. Sequence allocation is not rolled back and should not implement gapless business numbering ([isolation](https://www.postgresql.org/docs/18/transaction-iso.html)).

For a stock invariant, a validated positive quantity plus an atomic update is often sufficient:

```sql
UPDATE stock
SET available = available - $3
WHERE tenant_id = $1 AND sku = $2 AND available >= $3
RETURNING available;
```

Interpret zero affected rows deliberately; combine the update and reservation record in one owned transaction when both must succeed. A database CHECK can reinforce nonnegative stock. Do not replace an atomic predicate with a read/check/write of a stale absolute value. An optimistic version predicate must be part of the mutation; a prior SELECT alone is insufficient.

For a multi-row invariant, compare suitable constraints, ordered row locks, a stable coordination row, and serializable transactions. Locking existing rows does not lock an absent row or prevent all matching inserts. Use uniqueness/upsert for insert races when appropriate. `ON CONFLICT DO NOTHING` may wait for a conflicting row invisible to its statement snapshot, so a same-statement CTE fallback SELECT can still return nothing; a later READ COMMITTED statement sees a new snapshot. Do not make a no-op UPDATE solely to force RETURNING without evaluating triggers, write/WAL cost and semantics. MERGE is not a concurrency-equivalent replacement for every upsert ([INSERT](https://www.postgresql.org/docs/18/sql-insert.html), [isolation details](https://www.postgresql.org/docs/18/transaction-iso.html)).

## Locks, failures, and workers

Choose the least restrictive correct row/table lock and acquire multiple resources in consistent order. Keep lock-holding transactions short; do not wait for user input or a remote payment while holding row locks without an unavoidable requirement. Diagnose blockers and wait chains before assuming an index or hardware problem. PostgreSQL detects deadlocks, but the application still needs safe recovery. Advisory locks require cooperating users; transaction-level locks release with the transaction, while session locks and pooling have different lifetimes ([explicit locking](https://www.postgresql.org/docs/18/explicit-locking.html)).

`NOWAIT` exposes immediate lock failure; `SKIP LOCKED` is useful for queue-like claiming, not a consistent general read. Claim/update jobs atomically, then commit the durable claim. Define lease/reclaim, attempt limits, ownership/fencing and idempotent completion for crashes or slow workers; SKIP LOCKED alone does not deliver exactly-once processing or guarantee fairness. Avoid a network-length transaction to hold a job lock ([SELECT locking](https://www.postgresql.org/docs/18/sql-select.html)).

After SQL failure, roll back the failed transaction or appropriate savepoint before continuing. A nested ORM transaction may be a savepoint rather than an independent commit. Retry `40001` serialization failure and appropriate `40P01` deadlock failures by restarting the complete transaction, including decisions based on reads, with bounded attempts/time and backoff. A persistent unique violation is not automatically transient. Keep externally visible side effects outside an unsafe replay loop; use existing idempotency/reconciliation/outbox mechanisms as needed ([retry handling](https://www.postgresql.org/docs/18/mvcc-serialization-failure-handling.html)).

On connection loss during COMMIT, distinguish a known abort from an unknown outcome. Reconnect/retry is not proof that the first commit failed. Record logical operation identity under a unique scoped key together with its effect/result where possible. Reject incompatible key reuse and reauthorize result lookup. Durable local commit cannot atomically include an unrelated payment API or broker; an outbox addresses the database/publish gap, while dispatch and consumers still handle duplicates. NOTIFY is a wake-up signal, not a durable replayable queue ([NOTIFY](https://www.postgresql.org/docs/18/sql-notify.html)).

## Ownership and pool compatibility

All statements in one database transaction must use its owned connection. With node-postgres, acquire a client and use that client for BEGIN/work/COMMIT or ROLLBACK; `pool.query` can choose another connection and cannot provide this guarantee ([driver transactions](https://node-postgres.com/features/transactions)). In other drivers/ORMs inspect callback/session ownership, implicit transactions, autocommit and cleanup. A Psycopg SELECT can start a transaction by default; do not leave it idle while performing unrelated work ([Psycopg transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html)). Concurrent tasks sharing a connection also share transaction state; they are not independent transactions.

Return a connection only after commit/rollback and required state reset; discard a broken connection according to the driver. Clean up on exception, cancellation and timeout. Set context and appropriate timeout values transaction-locally inside the explicit protected transaction; `SET LOCAL` outside that transaction does not carry authority into a later one ([SET](https://www.postgresql.org/docs/18/sql-set.html)). Ensure tenant/role/search_path/temp/advisory state cannot leak across borrowers.

PgBouncer session, transaction and statement pooling have different guarantees. Transaction pooling does not preserve general session SET, LISTEN, session advisory locks or arbitrary temp/cursor state; statement pooling cannot support multi-statement transactions. Protocol-level prepared statements can work in current transaction pooling with suitable `max_prepared_statements`; SQL PREPARE/DEALLOCATE remain different. Check installed pooler, driver and config instead of universally disabling preparation ([features](https://www.pgbouncer.org/features.html), [configuration](https://www.pgbouncer.org/config.html)). Use an appropriate direct/session path for operations that require it, rather than weakening isolation for the whole app.

Budget connections across maximum app replicas, workers, reporting, migrations, pooler database/user pools, replication and administrative reserve. Bound acquisition queues/timeouts and transaction duration. Pool exhaustion may reflect slow/blocked work, leaked clients, idle transactions or a retry storm; raising max_connections can worsen resource pressure. Measure acquisition wait separately from SQL time. Size for useful database concurrency and memory, not just incoming request count.
