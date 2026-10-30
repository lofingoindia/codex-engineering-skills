# Production operations and recovery

Start with the affected service, symptoms, time window, baseline, deployment changes and business impact. Collect narrow evidence using existing observability. A database skill should not create a monitoring platform or turn every incident into global configuration tuning.

## Diagnose the constrained resource

| Evidence | Investigate before changing capacity |
| --- | --- |
| High request latency, modest SQL execution time | Pool acquisition, queued work, network, retries or application processing |
| Lock wait / long transaction | Blocker chain, transaction age/owner, pending DDL, idle-in-transaction and application cleanup |
| High execution CPU | Frequent/redundant SQL, row-estimate errors, excessive scans/joins, plan regression, worker concurrency |
| Disk/temp pressure | Scans, sort/hash spill, working set, write rate, maintenance and storage latency |
| WAL/checkpoint pressure | Index/update amplification, transaction/batch shape, archive/replica/slot retention and checkpoint behavior |
| Growing tables/old snapshots | Vacuum progress, dead tuples, long transactions, replication feedback/slots and churn |

Use `pg_stat_activity`, supported wait events, transaction/query age and `pg_locks`/`pg_blocking_pids` to establish current blocking. Row contention often appears as transaction-ID waits rather than an obvious row entry. Do not equate an active backend with active CPU use. Cumulative statistics have reset/sampling/snapshot semantics; gather comparable intervals and use version-appropriate fields. Query text and parameters can contain sensitive data ([activity/statistics](https://www.postgresql.org/docs/18/monitoring-stats.html), [locks](https://www.postgresql.org/docs/18/monitoring-locks.html)).

Use existing `pg_stat_statements` for normalized frequency/cost evidence when installed. Enabling its preload component can require a restart; do not install/restart merely to answer a narrow query if adequate evidence exists. Totals/averages are not latency percentiles, and absence from sampled/reset data does not prove no activity ([extension docs](https://www.postgresql.org/docs/18/pgstatstatements.html)).

Cancel/terminate only within authorized incident scope after identifying the correct blocker and consequences. Termination can roll back a large transaction and leave an application retry storm or uncertain external effect. Observe recovery and protect administrative capacity rather than killing arbitrary sessions.

## Sustainable write and maintenance behavior

Keep autovacuum/autoanalyze effective. MVCC updates create row versions; cleanup needs visibility horizons to advance. Long/idle transactions, prepared transactions, replication feedback and slots can retain needed history. Inspect dead/live tuples, vacuum/analyze recency/progress, transaction/multixact age and workload before changing per-table thresholds/workers. Do not disable autovacuum as a casual performance fix ([routine vacuuming](https://www.postgresql.org/docs/18/routine-vacuuming.html)).

Plain VACUUM normally makes space reusable and maintains visibility; it does not generally shrink files to the operating system. VACUUM FULL rewrites, needs extra space and a disruptive lock. Choose a reclaim/reindex strategy only after estimating space, blocking and the cause of growth. HOT updates depend on page space and the indexed columns/methods affected; lowering fillfactor trades density for update room, not a universal setting ([HOT](https://www.postgresql.org/docs/18/storage-hot.html)).

Bound ingest batches and transactions for throughput, memory, rollback, contention and lag. COPY can improve bulk transfer when the driver, validation/security and target workflow support it; staging plus a deliberate merge can be appropriate. It does not bypass business correctness requirements. Row triggers, constraints, duplicate keys and error/restart behavior still matter ([COPY](https://www.postgresql.org/docs/18/sql-copy.html)).

Do not enlarge work_mem as though it were a per-connection total: multiple plan nodes, hash multipliers, concurrent queries and workers can multiply memory. Match resource tuning to measured pressure and provider limits. Pool/worker concurrency, indexes and hot-row design often matter before hardware or partitioning ([resource settings](https://www.postgresql.org/docs/18/runtime-config-resource.html)).

Keep durability consequences explicit. WAL, checkpoints, synchronous_commit, fsync and storage guarantees serve different roles. Disabling durable acknowledgement or crash-safety controls for throughput changes the loss/corruption risk, not merely speed. Set any accepted tradeoff from the real RPO and verify crash/recovery implications; do not silently weaken durability during optimization ([WAL settings](https://www.postgresql.org/docs/18/runtime-config-wal.html)).

## Replicas and retained WAL

Separate write/flush/replay lag and application read-after-write needs. A successful primary commit does not mean an asynchronous replica can return that row or that failover preserves it. Route consistency-sensitive reads appropriately or use an established explicit catch-up strategy. Synchronous replication has latency/availability tradeoffs; no setting alone creates a complete HA system.

Replication slots and failed archiving can retain WAL until disk exhaustion. Monitor retained bytes, activity, consumer progress and capacity. Retention caps can protect storage by making a lagging consumer unable to catch up; plan resynchronization. Never delete files from pg_wal manually or drop a needed slot as a cosmetic fix. Logical replication also has schema/sequence/DDL/version limitations to verify in the specific integration ([standby/slots](https://www.postgresql.org/docs/18/warm-standby.html)).

## Backups, restoration, and failover

Establish RPO (acceptable lost committed work), RTO (time to restored service), scope and failure threats. Replication is availability infrastructure, not independent protection from accidental deletion, bad application writes, credential compromise or every corruption. Keep suitable protected, retained copies and recoverable credentials/encryption keys outside the same failure boundary.

Choose logical dump/restore for appropriate object/database portability and physical base-backup plus WAL for cluster/PITR needs. `pg_dump` is consistent for one database, not a complete cluster backup of globals or external configuration. Use `pg_restore` for supported archive formats and psql for plain SQL dumps. Plan roles/ownership, extensions, dependencies, sequences, collation and tool/server compatibility. Physical backups need appropriate version/tool compatibility; incremental chains add dependencies, not free recovery ([backup approaches](https://www.postgresql.org/docs/18/backup.html), [pg_dump](https://www.postgresql.org/docs/18/app-pgdump.html), [pg_basebackup](https://www.postgresql.org/docs/18/app-pgbasebackup.html)). Reuse a sound existing provider/backup system; [pgBackRest](https://pgbackrest.org/user-guide.html) is an option, not a mandatory new dependency.

PITR requires a usable base backup and the necessary continuous WAL through the target, with correct timeline/target/inclusivity and recovery configuration. Monitor archive success and completeness, not just backup job exit status. Preserve all required dependencies through retention, plus files/settings not reconstructed by WAL. Before a destructive restore, identify an isolated target, how to stop before the damaging transaction, what legitimate later writes would be lost, and how the application will be validated ([continuous archiving](https://www.postgresql.org/docs/18/continuous-archiving.html)).

Verify manifests/checksums where supported, but `pg_verifybackup` cannot prove a successful usable restore. Rehearse restoration to an isolated cluster, start it, verify the target data/invariants, roles/extensions/access, sequence behavior, and representative application reads/writes; measure recovery duration and actual recovery point. Disable external jobs/destinations in the rehearsal to prevent accidental customer effects. Include key/secret availability and retrieval time in the RTO ([backup verification](https://www.postgresql.org/docs/18/app-pgverifybackup.html)).

Failover requires fencing the old writer, confirming replica state/data-loss risk, promotion/routing/pool recovery, and a plan for the old primary's rejoin. Promotion alone does not prevent split brain. Cross-database workflows and external effects may need reconciliation after recovery. Prepare the concrete plan and commands, respect explicit live authorization, and do not execute failover/restore as a diagnostic experiment. Without an actual drill, report recoverability as unverified.
