---
name: postgresql-data-engineering
description: Design, review, troubleshoot, or improve PostgreSQL schemas, queries, transactions, migrations, pooling, security, and production recovery. Use for PostgreSQL engineering decisions; skip unrelated backend work and trivial SQL or text edits.
---

# PostgreSQL Data Engineering

Preserve the application's data invariants, tenant boundaries, durability, and recoverability while solving the requested problem with the least necessary complexity. Explicit user requirements and repository instructions take precedence over this skill's recommendations.

## Establish the decision context

Identify the task: modeling, query diagnosis, concurrency repair, migration review, integration/pooling, incident response, or recovery planning. Follow a targeted issue through its actual application/worker transaction and generated SQL; do not expand every SQL change into a full database audit.

Inspect relevant instructions, schema and migrations, constraints/indexes, query plans, driver/ORM transaction APIs, pool settings, consumers, tests, and deployment topology. Establish the server major/minor version, extensions, provider restrictions, driver and pooler versions. Use authorized metadata or configuration; do not expose credentials while collecting evidence. Check whether reads reach a primary or replica and which role really executes them.

For consequential decisions, state the business invariant, observed failure/evidence, chosen mechanism, and main tradeoff. Establish relevant workload/skew, contention, latency, data size, availability and recovery requirements. Infer from evidence and ask only for unresolved facts that materially affect correctness, authorization, or operational impact. Keep independent work moving while answers are pending.

Reuse sound schema, drivers, migration tools, observability, and application boundaries. Do not prescribe RLS, SERIALIZABLE, PgBouncer, partitioning, sharding, Redis, new extensions, or microservices without evidence of a benefit that justifies their costs. A slow request can be a pool or application problem rather than a database configuration problem.

## Read the guidance relevant to the task

| Decision | Reference |
| --- | --- |
| Data modeling, types, constraints, tenant relationships, roles/RLS/functions | [Schema and security](references/schema-security.md) |
| MVCC, invariants under concurrency, retries, job claiming, driver ownership and pool state | [Transactions and connections](references/transactions-connections.md) |
| Slow SQL, plans/statistics, index design, measured read/write costs | [Queries and indexes](references/queries-indexes.md) |
| DDL/backfills, mixed application versions, concurrent indexes, upgrades/recovery of migrations | [Migrations](references/migrations.md) |
| Incidents, vacuum/storage/WAL, replicas, backup/restore and failover | [Operations and recovery](references/operations-recovery.md) |
| Source authority, version differences, disputed or evolving behavior | [Source register](references/sources.md) |

Load only the relevant references. Verify significant or unfamiliar PostgreSQL, driver, pooler, and provider behavior against the installed version's official manual/release notes. These references are a dated synthesis; current/development docs do not establish support on an older production server. Disclose missing runtime or research access rather than inventing behavior or execution evidence.

## Keep guarantees and side effects explicit

Separate statement atomicity, multi-statement isolation, committed local effects, external effects, replica visibility, and recoverability. A transaction wrapper does not prove correct connection ownership or prevent every race. An acknowledged commit, lost connection, or timed-out request has different implications for retry safety. Never infer an external payment/message was rolled back by PostgreSQL.

Treat proposed SQL, plans, and live execution as different deliverables. EXPLAIN ANALYZE executes SQL, including functions and triggers; rollback does not undo every side effect. Use disposable/appropriate environments for experiments. Keep live investigation bounded and read-only unless changes are authorized. Destructive DDL, irreversible backfills, disruptive maintenance, restore and failover require explicit authorized scope and a concrete recovery path; skill invocation alone does not authorize them. Prepare reviewable commands and impact before seeking any missing approval; preserve authorization already given.

Own PostgreSQL guarantees and their application integration. Coordinate API behavior or cross-service workflow changes explicitly; use complementary engineering skills only when that work is in scope, without depending on them.

## Verify the actual invariant

Implement the focused change through affected schema, SQL, integration, migration and operational documentation. For reviews, lead with actionable findings tied to evidence, impact and a practical correction. Preserve data and supported consumers; do not break them for naming or stylistic consistency.

Use normal project checks and focused PostgreSQL tests appropriate to the risk. Exercise real independent connections for a concurrency claim, the actual runtime role for RLS, representative distributions for plans, migration interruption/lock impact when relevant, and an isolated restore for recoverability. Inspect durable state and effect counts, not only returned rows or success codes. Mocks, SQL parsing, SQLite, and one sequential request cannot prove PostgreSQL isolation, planner behavior, or recovery.

Compare before/after correctness, latency/resource use, and compatibility where affected. Stop expanding tests once meaningful checks pass unless a new change, failure, or unresolved risk warrants more. Report what changed, why, executed evidence, rollout/recovery implications, and genuine limitations. Proposed checks and plausible SQL are not executed tests or proof of production readiness.
