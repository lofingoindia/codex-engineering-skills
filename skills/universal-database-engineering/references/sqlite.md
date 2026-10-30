# SQLite: embedded relational design

Use SQLite when its embedded ownership, write workload, deployment and recovery model fit. Do not add a client-server database just to resemble a SaaS reference architecture. Conversely, verify actual multi-process/multi-host access and durability needs rather than assuming a local test proves every deployment is suitable.

## Verify the runtime and model

Inspect the library version actually linked into the application/driver, compile options, filesystem, journal/synchronous settings and connection setup. The installed command-line executable can use a different SQLite version. Foreign-key declarations alone do not prove enforcement: configure and verify `PRAGMA foreign_keys` on each application connection, outside an already active transaction, using the actual driver/pool lifecycle. Check existing data with the appropriate validation tools when changing enforcement.

Validate parent-key uniqueness/collation and composite-reference/null semantics. Choose child indexes from actual lookup/delete/check costs rather than assuming all declarations create them. SQLite's flexible typing and historical primary-key/null quirks differ from conventional server SQL. Inspect actual DDL and use appropriate NOT NULL/CHECK/STRICT behavior where justified. STRICT tables require SQLite 3.37.0+ and have supported-type restrictions; they do not make every SQL type portable. Define date/time, Boolean and exact-money representations explicitly.

Choose rowid, INTEGER PRIMARY KEY or WITHOUT ROWID from key/access needs. Do not add AUTOINCREMENT simply to obtain automatic IDs; establish whether its stronger reuse semantics are required and account for cost. Use the current planner and representative data to evaluate multi-column/covering/partial/expression indexes rather than importing another engine's syntax or cost model.

## Own concurrency and files

WAL allows concurrent readers and a writer, but still only one writer at a time per database. Keep write transactions focused, bound busy handling and diagnose contention before increasing connection pools. A deferred read transaction may fail when upgrading to write after its snapshot becomes stale; select a supported transaction mode and whole-operation retry policy from the invariant. `BEGIN IMMEDIATE` is useful in some read-then-write workflows, not a universal setting.

Long readers can impede checkpoints and grow WAL. Monitor checkpoint/WAL behavior and disk capacity. WAL's shared-memory coordination normally requires processes on the same host; do not place a standard WAL database on a network filesystem and assume normal distributed access. Verify provider-specific alternatives separately.

The WAL contains committed data that may not yet be in the main file. Copying only a live `.db` file can lose relevant state; use supported backup/snapshot procedures and verify restoration. Synchronization settings trade durability for speed, not just latency. Protect files and backups with appropriate OS/application permissions; do not assume built-in server roles or encryption from another engine exist here.

The official WAL page reviewed on 2026-10-30 documents a WAL-reset corruption fix in 3.51.3 and selected earlier backports (including 3.44.6 and 3.50.7). Check the actual runtime's release notes/fix status; “WAL enabled” is not sufficient version evidence. Do not repeatedly fault-test a live database to demonstrate this issue.

## Evolve and verify proportionately

Check the actual version's ALTER TABLE support and rebuild requirements. Use supported table-rebuild steps when necessary, preserving constraints, indexes, triggers, foreign-key relationships and data. A generic ORM migration may not preserve everything automatically. Validate existing data and representative application behavior after migration, and use appropriate integrity/foreign-key checks without claiming they prove every business invariant.

For concurrency claims use independent real connections and the application's actual transaction mode; separate in-memory databases or mocks can hide contention. Keep file/journal/backup handling consistent with the tested deployment. Sources: [foreign keys](https://www.sqlite.org/foreignkeys.html), [isolation](https://www.sqlite.org/isolation.html), [WAL and fix history](https://www.sqlite.org/wal.html), [STRICT tables](https://www.sqlite.org/stricttables.html), [query planner](https://www.sqlite.org/queryplanner.html), [database documentation index](https://www.sqlite.org/docs.html).
