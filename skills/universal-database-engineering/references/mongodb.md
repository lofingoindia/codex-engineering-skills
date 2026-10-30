# MongoDB: workload-shaped documents

Establish server/driver versions, deployment topology, shard key where applicable, read preference, read/write concerns and session/transaction behavior. A flexible schema still has business invariants and evolving consumers. Do not apply relational normalization levels or assume wire-compatible services reproduce MongoDB server guarantees.

## Choose the aggregate boundary

Embed bounded, co-owned data that is usually accessed/updated together when one-document atomicity and simpler reads help. Reference independently owned/shared entities, unbounded child sets, many-to-many relationships or data with separate update/security/retention needs. A large entity graph is not automatically one aggregate. Evaluate growth, hot-document contention, returned bytes and index fan-out as well as query count.

Documents have a 16 MiB BSON size limit. Unbounded comments, events or history arrays can also create update/index costs well before that limit. Use a justified bounded subset, bucket or referenced collection; do not install a pattern catalog wholesale. Duplication can improve reads, but define which representation owns the fact, propagation lag, corrections and rebuild. A historical snapshot is different from a mutable copied profile.

## Enforce the actual invariant

Single-document writes are atomic; conditional update filters can ensure the expected version/state still matches. Multiple individually atomic updates are not automatically an atomic multi-document workflow. Bulk operations can interleave and fail partially. Use supported transactions where the invariant spans documents, understanding topology, concerns, limits and driver retry semantics. A retried transaction callback must not duplicate external side effects.

Schema validation can enforce relevant field types/ranges and structure. Inspect validation action/level, existing invalid documents and bypass privileges: enabling a validator is not automatic retroactive cleanup. Application models alone do not constrain every writer. MongoDB references are not relational foreign keys; ownership, referential lifecycle and consistency need an explicit application/transaction strategy.

Use appropriately scoped unique indexes for tenant/business identities and verify shard-key limitations on global uniqueness. Unique multikey indexes prevent conflicts across documents, not necessarily duplicate array elements within one document. Distinguish missing/null index entries, partial filters and required fields; do not claim indexing inserts missing fields into the stored document. Collation affects identity comparisons. A tenant field or obscure `_id` alone does not enforce authorization on reads, updates, joins or aggregations.

## Optimize and evolve from evidence

Inspect representative query shapes/parameters, explain output, scanned documents/keys, projection, sort and aggregation stages. Compound indexes need the actual equality/sort/range workload, cardinality and collation. Arrays create multikey indexes with compound/query-bound restrictions and additional write/storage cost. Avoid automatic indexes on every filter or a wildcard index as a substitute for understanding the workload.

Keep document growth, collection/index size, cache/IO pressure, connection budgets, transaction conflicts and replication lag visible. Secondary reads are not automatically fresh after an acknowledged write; match concerns, sessions and read preference to the consistency requirement. Sharding requires a suitable key, routing/locality and hot-spot analysis, not only large document counts.

For schema evolution, define old/new document shapes and reader/writer compatibility. Prefer a bounded compatible change over rewriting the whole collection. Validators, backfills and index builds have separate effects; inspect existing data before tightening rules or adding uniqueness. Make large transformations resumable and protect newer live updates from stale backfill writes. Preserve representative documents and indexes through a supported backup/restore procedure before making recovery claims.

Verify the boundary actually changed: a competing conditional update, invalid/oversized/growing document, duplicate array versus cross-document identity, tenant mismatch or interrupted migration. SQLite or JSON-only mocks cannot establish MongoDB atomicity, index or transaction semantics. Sources: [schema design](https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/), [embedding](https://www.mongodb.com/docs/manual/data-modeling/embedding/), [unbounded arrays](https://www.mongodb.com/docs/manual/data-modeling/design-antipatterns/unbounded-arrays/), [atomicity](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/), [validation](https://www.mongodb.com/docs/manual/core/schema-validation/), [multikey behavior](https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/), [unique indexes](https://www.mongodb.com/docs/manual/core/index-unique/).
