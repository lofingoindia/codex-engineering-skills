# Authoritative source and version register

Checked 2026-10-30. Guidance is original engineering synthesis, not copied manuals. Prefer the deployed server/driver/pooler/provider version's documentation; use these links as entry points and recheck release notes, current security fixes and feature support when a decision depends on them.

## Skill authoring and boundaries

| Source | Retained decision |
| --- | --- |
| Bundled `skill-creator/SKILL.md`, metadata reference, initializer and validator (inspected locally) | Precise triggers, compact workflow, progressive disclosure, no unnecessary runtime scripts |
| [OpenAI GPT-6 Astra skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Favor clear outcome/decision boundaries over exhaustive recipes and bloated root context |
| [OpenAI Skills guide](https://developers.openai.com/api/docs/guides/tools-skills), [Agent Skills specification](https://agentskills.io/specification) | Portable name/description manifest and on-demand resources; optional UI metadata is host-specific |
| [Codex discovery](https://learn.chatgpt.com/docs/build-skills), [skill evaluations](https://developers.openai.com/blog/eval-skills) | Verify actual host discovery and observable behavior; metadata validation alone is not proof of technical correctness. Keep validation proportional |

The installed API skill covers consumer contract and distributed API behavior; this skill owns PostgreSQL primitives, data guarantees, integration and operations. Complementary skills are optional, not runtime dependencies.

## Version policy

[Version policy](https://www.postgresql.org/support/versioning/) and [manual index](https://www.postgresql.org/docs/) listed PostgreSQL 18 / 18.6 as current stable and PostgreSQL 19 as RC during research; supported majors were 14–18, with 14 nearing its listed 2026-11-12 end of support. These are dated observations, not permanent pins or a requirement to upgrade every project now. PostgreSQL is the implementation authority; its extensions and operational recommendations are not all generic SQL guarantees.

Material version distinctions: [15 constraints](https://www.postgresql.org/docs/15/ddl-constraints.html) document NULLS NOT DISTINCT; [18 release notes](https://www.postgresql.org/docs/18/release-18.html) describe B-tree skip scans and native uuidv7. [18 ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html) includes newer not-null/NOT VALID capabilities. Check the older server manual before applying them. Driver docs can default to a development build; do not infer deployed library support from an unpinned page.

## Schema, access and transaction semantics

| Official source | Applied judgment |
| --- | --- |
| [Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html), [date/time](https://www.postgresql.org/docs/18/datatype-datetime.html), [UUID functions](https://www.postgresql.org/docs/18/functions-uuid.html) | Database-enforced relationships and domain rules; NULL/default, precision, temporal and generator-version semantics |
| [Partitioning](https://www.postgresql.org/docs/18/ddl-partitioning.html) | Pruning/retention benefits versus partition management, constraint and lock limitations; not a default scaling step |
| [Row security](https://www.postgresql.org/docs/18/ddl-rowsecurity.html), [schemas](https://www.postgresql.org/docs/18/ddl-schemas.html), [function security](https://www.postgresql.org/docs/18/sql-createfunction.html), [TLS](https://www.postgresql.org/docs/18/ssl-tcp.html) | Runtime-role/owner bypass, actual schema privileges, safe privileged resolution and secure connections; RLS is optional and context-dependent |
| [Concurrency overview](https://www.postgresql.org/docs/18/mvcc.html), [isolation](https://www.postgresql.org/docs/18/transaction-iso.html), [locking](https://www.postgresql.org/docs/18/explicit-locking.html) | Statement versus transaction snapshots, write skew, atomic predicates, ordered locks and coordination; SERIALIZABLE is not universal |
| [Serialization failure handling](https://www.postgresql.org/docs/18/mvcc-serialization-failure-handling.html), [INSERT](https://www.postgresql.org/docs/18/sql-insert.html), [SELECT](https://www.postgresql.org/docs/18/sql-select.html) | Whole-transaction retry, upsert/snapshot subtleties, MERGE distinctions and queue-specific SKIP LOCKED behavior |
| [SET](https://www.postgresql.org/docs/18/sql-set.html), [NOTIFY](https://www.postgresql.org/docs/18/sql-notify.html) | Transaction-local context lifetime; notifications do not establish durable replayable delivery |
| [node-postgres transactions](https://node-postgres.com/features/transactions), [Psycopg transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html) | Driver-specific connection ownership, implicit transaction and cleanup examples. Psycopg page served 3.3.7.dev1 during research; verify installed-version docs before relying on changing APIs |
| [PgBouncer features](https://www.pgbouncer.org/features.html), [configuration](https://www.pgbouncer.org/config.html) | Current site lists 1.26.1; pooling modes, session-feature limitations and configured protocol-prepared support. SQL PREPARE and protocol preparation differ |

## Query, migration and operational evidence

| Official source | Applied judgment |
| --- | --- |
| [EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html), [planner statistics](https://www.postgresql.org/docs/18/planner-stats.html), [PREPARE](https://www.postgresql.org/docs/18/sql-prepare.html) | Plans/costs versus actual workload, estimates/skew, custom/generic plans; ANALYZE execution is not side-effect-free |
| [CREATE INDEX](https://www.postgresql.org/docs/18/sql-createindex.html), [multicolumn](https://www.postgresql.org/docs/18/indexes-multicolumn.html), [partial](https://www.postgresql.org/docs/18/indexes-partial.html), [index-only](https://www.postgresql.org/docs/18/indexes-index-only-scans.html) | Match predicates/order/operators, account for write cost/visibility, and handle concurrent-build failure; avoid rigid column-order myths |
| [ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html), [version/upgrade policy](https://www.postgresql.org/support/versioning/) | Lock/scan/rewrite and constraint-version details; choose compatibility and recovery over migration convenience |
| [Statistics/activity](https://www.postgresql.org/docs/18/monitoring-stats.html), [locks](https://www.postgresql.org/docs/18/monitoring-locks.html), [pg_stat_statements](https://www.postgresql.org/docs/18/pgstatstatements.html) | Bounded incident evidence, appropriate views/columns, collection/reset limits and extension startup requirements |
| [Routine vacuuming](https://www.postgresql.org/docs/18/routine-vacuuming.html), [HOT](https://www.postgresql.org/docs/18/storage-hot.html), [resources](https://www.postgresql.org/docs/18/runtime-config-resource.html), [COPY](https://www.postgresql.org/docs/18/sql-copy.html), [WAL](https://www.postgresql.org/docs/18/runtime-config-wal.html) | MVCC/storage maintenance, effective autovacuum, write amplification, multiplied memory, bounded ingest and explicit durability tradeoffs |
| [Backup approaches](https://www.postgresql.org/docs/18/backup.html), [pg_dump](https://www.postgresql.org/docs/18/app-pgdump.html), [pg_basebackup](https://www.postgresql.org/docs/18/app-pgbasebackup.html), [pg_verifybackup](https://www.postgresql.org/docs/18/app-pgverifybackup.html) | Logical/physical scope, compatibility and integrity verification; an actual restore/app check remains necessary |
| [Continuous archiving/PITR](https://www.postgresql.org/docs/18/continuous-archiving.html), [standby/replication slots](https://www.postgresql.org/docs/18/warm-standby.html) | Base plus WAL/timeline/recovery dependencies, RPO/RTO, lag/retention and failover consequences; replication is not a backup substitute |
| [pgBackRest upstream guide](https://pgbackrest.org/user-guide.html) | Established backup/retention/encryption/restore tooling when it fits the existing system; its Linux examples are not cross-platform installation instructions |

## Resolve competing recommendations by evidence

- Atomic predicates/constraints, explicit locking and serializable execution protect different invariants with different contention/retry costs. Select the simplest sufficient mechanism.
- App pool sizing and PgBouncer solve different connection-ownership/concurrency problems; raising maximum connections is not a general cure.
- Indexes, batching, denormalization and partitioning trade read cost against writes, storage and maintenance. Measure the actual workload instead of adopting universal recipes.
- Concurrent index builds and phased constraints reduce some blocking at extra complexity/cost. Small offline changes may not need them; large online changes need interruption/recovery planning.
- Logical, physical, incremental and provider backups have different scope and dependencies. A restore drill and measured recovery point/time are stronger evidence than green job status.
