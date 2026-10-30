# ClickHouse: analytical facts and physical order

Establish version/provider, table engine, replicated/distributed topology, ingestion path and effective settings. ClickHouse is suited to analytical scans/aggregations; do not move authoritative OLTP balances, relationships or reservations into it merely because dashboard queries are slow. An analytical projection adds ingestion, lag, correction and operational responsibilities that may outweigh its benefit for a small workload.

## Model the analytical meaning

Define fact grain, event versus ingestion time, identity, measures, dimensions, updates/deletions and retention. Decide whether queries need current attributes or attributes as observed at event time. Denormalization can reduce repeated joins, but mutable dimension copies require a deliberate refresh/correction policy. Keep joins when they meet latency/resource needs; current versions' join capabilities and algorithms evolve.

Choose ORDER BY from real filtering, locality and compression needs. The primary index is sparse and selects granules; it is not a relational unique constraint. ORDER BY and PRIMARY KEY have related but distinct roles, so do not equate them blindly or append an ID and assume uniqueness enforcement. Read pruning/bytes and actual query behavior matter more than a borrowed key-column count.

Partition mainly for lifecycle/data management and justified pruning. Excessively granular/high-cardinality partitions produce too many parts and impede merging. Do not partition by every tenant/user by default. Balance ingestion batches, part counts, merge backlog, storage amplification and accepted visibility latency. Check acknowledgment/deduplication behavior of the actual synchronous/asynchronous ingestion path before treating a successful client response as an end-to-end guarantee.

## Replacement and materialization are not OLTP constraints

ReplacingMergeTree replacement uses the sorting key and optional version semantics during merging; it does not enforce immediate unique rows. Duplicate/old/deleted versions may affect ordinary reads before reconciliation. Define a correct supported query-time strategy such as FINAL or version-aware aggregation when required, then measure its cost. Parts merge within partitions; keep identity/version placement compatible with the correction strategy rather than assuming future merges will repair arbitrary cross-partition updates.

Insertion retry deduplication has scope, window and configuration conditions. It does not establish exactly-once business ingestion or replace stable source identity/versioning. Preserve the source-of-truth record and reconciliation when CDC/events can duplicate, arrive late or be reordered. Keep deletion markers and cleanup/replay behavior compatible so an old replay cannot resurrect deleted data.

Incremental materialized views process newly inserted blocks into a target table. They do not automatically recompute all historical results when source rows are updated/deleted or a joined dimension changes. Aggregate-state targets must be merged/read with the right semantics. Backfill and live ingestion need a boundary that avoids gaps or double counting. Refreshable views, projections and denormalized targets have different behavior and costs; choose only for the actual query requirement.

## Verify production consequences

Inspect plans, rows/bytes/granules read, query memory/spill, insert latency, part/merge backlog, mutation progress and replica/ingestion lag. Batching, compression, projections, skipping indexes and key changes need workload evidence. Do not routinely force expensive full merges to conceal an incorrect model.

For changes, check existing sorting/partition/schema constraints, rewrite needs and mixed-ingestion compatibility. Validate query results before and after late/duplicate events, replacements/deletes and materialized-view backfills when relevant. Test correctness before comparing speed. Enforce tenant scope in authenticated queries, supported policies and ingestion; a tenant sorting column is not access control. Verify backup/restore with the actual replicated/distributed storage and provider capabilities instead of treating replication as backup.

Sources: [ordering/primary keys](https://clickhouse.com/docs/concepts/best-practices/choosing-a-primary-key), [partitioning](https://clickhouse.com/docs/concepts/best-practices/partitioning-keys), [ReplacingMergeTree](https://clickhouse.com/docs/reference/engines/table-engines/mergetree-family/replacingmergetree), [incremental materialized views](https://clickhouse.com/docs/concepts/features/materialized-views/incremental-materialized-view), [documentation](https://clickhouse.com/docs/).
