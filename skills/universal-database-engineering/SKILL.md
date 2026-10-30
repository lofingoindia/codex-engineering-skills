---
name: universal-database-engineering
description: Design or evolve data models, schemas, constraints, and workload-driven database architecture across relational, embedded, document, and analytical engines. Use for substantive database modeling, integrity, query/index tradeoffs, or schema evolution; skip unrelated backend work and trivial SQL edits.
---

# Universal Database Engineering

Optimize the logical model for business correctness and clarity, then optimize storage and access using evidence. The goal is neither fewer tables nor maximum normalization/indexing. Preserve a suitable existing schema, engine, driver and migration system. Do not introduce another database or copy a company's architecture merely because its workload appears similar.

## Understand the fact before choosing storage

Identify the request: new model, existing feature, query/concurrency problem, migration, architecture decision or read-only review. Inspect applicable instructions and the relevant schema/models, migrations, constraints, generated queries, readers/writers, background jobs, tests and deployment. Follow actual dependencies rather than exploring the whole repository. A simple column change does not require a multi-engine architecture review.

Establish the actual engine/version, storage engine/extensions, provider restrictions, driver/ORM, transaction and connection ownership, isolation/consistency settings and primary/replica paths. Separate configured, installed and deployed behavior. Do not assume MySQL equals MariaDB, SQLite tests prove PostgreSQL behavior, or SQL terminology implies identical guarantees. Research consequential uncertainty against the target release, using available research guidance without loading unrelated domains.

For the affected data, establish its grain (what one record means), identity, owner/tenant, lifecycle, cardinality, invariants, history/retention and access patterns. Ask only for missing business facts that materially change correctness or the model. Find whether existing structures already own the fact before proposing a table, collection or column.

## Make the modeling decision explicit

Compare reuse, extension, separation, embedding/reference, computation or deliberate materialization only where plausible. Choose from ownership, dependencies, lifecycle, atomic boundaries, growth and query costs. A separate table needs a distinct entity, relationship, lifecycle or other concrete benefit; keeping everything together needs equally sound boundaries.

For a proposed stored fact, explain who writes it, what identifies it, why it belongs there, how invalid states are prevented and how consumers access it. Distinguish a historical snapshot from an accidental duplicate of current data. Denormalized/derived values need an authoritative source, maintenance/rebuild path and acceptable lag. Avoid speculative counters, status fields, timestamps, JSON escape hatches or generic entity frameworks.

## Load only relevant detail

| Decision or engine | Reference |
| --- | --- |
| Table/collection boundaries, columns, relationships and tenant invariants | [Modeling decisions](references/modeling-decisions.md) |
| Concurrency, query/index costs, migration and production architecture | [Integrity, workload and evolution](references/integrity-workload-and-evolution.md) |
| MySQL or MariaDB | [MySQL and MariaDB distinctions](references/mysql-and-mariadb.md) |
| Embedded SQLite | [SQLite](references/sqlite.md) |
| MongoDB documents | [MongoDB](references/mongodb.md) |
| ClickHouse analytics | [ClickHouse](references/clickhouse.md) |
| Source authority, case studies or deeper upstream research | [Research index](references/sources.md) |

For deep PostgreSQL work, use available `postgresql-data-engineering` guidance and versioned upstream documentation instead of duplicating its full handbook. If unavailable, apply this workflow and research the actual engine directly. Redis, authorization, distributed workflows, runtime integration, audits and task coordination may warrant installed companion skills; none should activate automatically just because a database is involved.

## Implement and verify the real outcome

Keep changes focused and compatible with affected consumers. Use established migrations and authorized environments. Explicit read-only scope prohibits fixes or mutating experiments. Destructive DDL, irreversible data changes, backfills and operational actions require actual authorization; preserve authorization already given and prepare concrete impact/recovery details before asking for anything missing.

Derive focused tests from business invariants and actual race/failure windows. Check stored state, relationship/tenant validity, concurrent effects, old/new consumer compatibility and relevant resource costs. Plans, mocks, empty-database migration success and compilation cannot establish production concurrency or recovery. Some profiling commands execute statements; verify engine-specific effects before running them.

Use proportional verification and stop after meaningful checks pass unless a change or unresolved risk warrants more. Normal validation is sufficient for a skill-only change; do not launch benchmark/agent-evaluation infrastructure by default. Report the model decision, evidence, implementation, actual tests, compatibility/rollout implications and remaining uncertainty. Do not claim measured gains or successful restore/failover without execution.
