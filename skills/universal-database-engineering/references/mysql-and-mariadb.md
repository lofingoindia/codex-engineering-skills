# MySQL and MariaDB: verify the actual engine

These are related products, not interchangeable releases of one engine. Establish server/version/provider, table storage engine, SQL mode, charset/collation, driver and effective session settings before choosing behavior. The MySQL 8.4 links below are a versioned research baseline, not a requirement to deploy 8.4 or evidence about every other release. Follow the target manual and release notes.

## Model for integrity and storage

For InnoDB, the primary key determines clustering and is included in secondary indexes. A very wide or frequently changing key can multiply storage/write costs. Balance that against actual business and tenant identity; do not migrate a sound key scheme merely to mandate integer IDs.

Check foreign-key support, compatible column types/collations and index requirements for the actual storage engine. InnoDB can create required referencing indexes; PostgreSQL behavior differs. Prefer a properly supported primary/unique parent key; do not rely on nonstandard nonunique referenced-key behavior across products/versions. Tenant-qualified uniqueness/references may protect a meaningful relationship invariant. Inspect actual indexes before adding duplicates.

Validate SQL mode and constraint enforcement rather than assuming invalid values are rejected uniformly. Required fields, defaults, CHECK behavior and NULL uniqueness semantics need target-version tests. Text collation can equate values the application considers different. Foreign-key/check bypass settings and bulk imports need a deliberate validation path; reenabling checks is not automatically proof all historical rows were revalidated.

MySQL native binary JSON and MariaDB's documented JSON-as-LONGTEXT representation differ. Compare supported validation, expression/generated-column indexing, query plans and update costs before placing core searchable facts in JSON. Do not treat MySQL functional/partial-index techniques or PostgreSQL operators as portable MariaDB syntax. Generated values and their indexability are version-dependent.

## Concurrency and access paths

InnoDB's documented default REPEATABLE READ does not establish the actual session configuration or PostgreSQL-equivalent semantics. Nonlocking consistent reads and locking reads can observe different views. Index search shape affects record/gap/next-key locks, so a broad scan can lock far more than the intended business row. Diagnose actual waits/plans and lock ordering before raising isolation or adding broad locks.

Use constraints and conditional writes for the intended state transition, with bounded whole-transaction retries when needed. Verify deadlock versus lock-timeout rollback scope and driver behavior. `ON DUPLICATE KEY UPDATE` is driven by applicable unique indexes; additional unique keys can change which conflict is encountered. `REPLACE` has deletion/reinsertion semantics rather than being a harmless update. Check affected rows, triggers, cascades and idempotency before substituting these operations.

Use actual EXPLAIN/runtime evidence, representative parameters and target-version statistics. Composite/covering/expression indexes have specific capabilities. Account for secondary-index PK storage, write/log pressure and replication. Do not infer a need for sharding or another engine from query count alone.

## Migration and recovery

Consult the exact operation's INSTANT/INPLACE/COPY and locking support; INPLACE can rebuild a table, and online work can still wait on/acquire metadata locks. Specify supported algorithm/lock constraints when appropriate so an unacceptable fallback does not occur silently. Include long transactions, temporary disk, log volume and replica lag in the plan. Do not disable integrity checks merely to obtain a faster DDL algorithm.

MySQL atomic DDL concerns a statement's crash consistency, not SQL transaction rollback of arbitrary DDL. DDL can implicitly commit surrounding work. MariaDB has its own supported atomic/online operations and version boundaries. The migration runner cannot make these behaviors identical. Shadow-table tools have cutover, key, trigger/foreign-key and replication assumptions; use the existing tool only when the target operation needs it.

Validate representative legacy values and old/new writes, not only an empty database. Preserve binlog/backup continuity and a compatible recovery/rollback path. Provider HA/replicas are not independent backups; make recoverability claims only after appropriate restore evidence.

Sources: [InnoDB locking/isolation](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html), [clustered/secondary index model](https://dev.mysql.com/doc/refman/8.4/en/converting-tables-to-innodb.html), [online DDL matrix](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html), [atomic DDL](https://dev.mysql.com/doc/refman/8.4/en/atomic-ddl.html), [implicit commits](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html), [MariaDB constraints](https://mariadb.com/docs/server/reference/sql-statements/data-definition/constraint), [MariaDB JSON](https://mariadb.com/docs/server/reference/data-types/string-data-types/json), [compatibility matrix](https://mariadb.com/docs/server/server-management/install-and-upgrade-mariadb/migrating-to-mariadb/moving-from-mysql/mysql-to-mariadb-compatibility-matrix).
