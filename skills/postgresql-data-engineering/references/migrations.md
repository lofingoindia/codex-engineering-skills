# Safe migrations and schema evolution

Migration convenience must not override data preservation or compatibility. Inspect the actual migration framework and transaction wrapping, schema drift, server version, object sizes/dependencies, traffic, replication, available space and deployment order. Preserve existing tooling instead of adding a second migration system.

## Plan observable impact

For consequential DDL or backfill, identify the exact operation, lock mode/wait, scan or rewrite, expected write/WAL/replica/storage cost, old/new application compatibility, interruption state, and recovery action. Distinguish metadata-only work from a full rewrite, but remember both may require disruptive locks. A waiting strong DDL lock can queue otherwise compatible traffic behind it. Use appropriate bounded lock/statement timeouts and stop/retry conditions rather than letting a deploy wait indefinitely.

Generate the SQL and a reviewable execution plan before any missing live authorization. Confirm the target database/schema/role and avoid accidental default connections. Destructive changes, live irreversible backfills and operationally disruptive execution need explicit authorization; local disposable preparation does not require repeated approvals. A successful command on a small development database does not justify a zero-downtime claim.

## Compatible application and data transitions

Use expand/backfill/switch/contract when independent app/worker versions overlap or conversion is substantial. A small coordinated internal change may need less machinery. Renames, dropped columns, changed defaults/types and tighter constraints can break old code, background jobs, generated SQL, CDC or reports. Keep both write/read paths correct during coexistence; identify which path is authoritative and how drift is reconciled.

Backfills should be bounded, resumable and restart-safe, with progress/checkpoints and a predicate that does not overwrite newer user changes. Commit manageable chunks, observe lock contention/WAL/replica lag, and throttle or pause from actual load. Do not hold one huge transaction simply for convenient rollback. A rollback of application code cannot undo all already committed data conversions.

Preflight violations and conversion behavior on representative data: duplicate scoped keys, NULLs, orphans, invalid casts, overflow, collation/time-zone changes and dependent views/functions. Bound heavy validation queries. After switching, verify data invariants and old/new consumers; retire compatibility paths only after usage/deployment evidence supports it. Prefer a data-preserving rollforward where rollback would discard new legitimate writes.

## PostgreSQL-specific DDL choices

Adding a column with a nonvolatile default can avoid rewriting the existing table on supported modern versions; volatile defaults and many type conversions have different costs. Changing a default does not backfill old rows. SET NOT NULL can scan; a validated CHECK proving non-null can allow a scan to be skipped, while a strong lock is still needed. Newer releases add constraint capabilities: verify NOT VALID support for the actual constraint/server rather than applying one recipe universally ([ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html)).

When supported, add an appropriate CHECK/FK constraint NOT VALID to enforce new writes, then validate existing rows separately after repair. NOT VALID is not equivalent to disabling enforcement, and validation still consumes resources and acquires locks. UNIQUE/primary-key creation has different mechanisms. For a large unique constraint, a suitable unique index built concurrently can sometimes be attached as a constraint; partial/expression/partitioned cases have restrictions. Resolve existing duplicates and stop new conflicts deliberately.

CREATE INDEX CONCURRENTLY avoids blocking ordinary writes for the entire build but performs extra work and waits for relevant transactions/snapshots. It cannot run inside a transaction block; check migration-tool nontransactional support, lock/resource limits, partitioned-table restrictions and rollout state. Do not run every small offline index build concurrently just by habit ([CREATE INDEX](https://www.postgresql.org/docs/18/sql-createindex.html)).

A failed concurrent build may leave an invalid index that still incurs update cost. An invalid unique index may continue enforcing uniqueness. Inspect catalog validity/definition before recovery; IF NOT EXISTS can silently preserve a wrong or invalid object. Choose an authorized drop/rebuild or appropriate concurrent reindex based on current state and dependencies. Do not merely rerun a migration name and assume success. An interrupted nontransactional migration needs explicit reconciliation between the schema and the tool's bookkeeping.

For partitioned tables, plan indexes/constraints and attach/detach operations on the deployed version; parent and partition operations have different concurrency/lock restrictions. Validate matching bounds where needed to avoid expensive attach scans. Partition retention actions are destructive data lifecycle operations, not free maintenance.

## Rehearse and recover

Use disposable PostgreSQL with representative size/distribution and concurrent sessions when lock/compatibility claims depend on it. Exercise interruption after a nontransactional step and restart a chunked backfill. Verify catalog state, data invariants, app/worker compatibility, replica effects and recovery commands. Without a runtime, provide the rehearsal and expected invariant as a proposal and label it unexecuted.

For major upgrades, inspect all intervening release notes, extension/driver/provider compatibility, collation changes, replication and upgrade/dump strategy. Minor upgrades have different requirements but still need their release notes. Test the actual upgrade and recovery path; do not infer binary data-directory compatibility or an effortless downgrade from version numbering ([version policy](https://www.postgresql.org/support/versioning/)). Retain usable backups and access/keys, while recognizing that a backup alone does not make every destructive change easy to reverse.
