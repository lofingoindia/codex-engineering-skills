# Caching and freshness

## Define what a hit means

Trace every writer, including imports, workers and administrative paths. Decide which database/source owns truth, the cache identity, freshness budget and safe fallback. Include tenant, representation/schema version and relevant authorization, locale, filters or other response variants. Shared raw data may have a different cache identity from a permission-filtered response; authorize each request appropriately.

Use cache-aside when requested reads justify it; read-through/write-through describe ownership, not stronger cross-system transactions. Write-behind can lose accepted changes and reorder writes without durable intent, ordering and recovery; do not use it as an incidental database optimization. Use explicit TTLs where expiry is intended, validated units and bounded jitter that respects maximum staleness. Audit overwrites that remove expiry, including `SET` without a TTL/`KEEPTTL`; not every Redis responsibility should expire.

## Distinguish confirmed absence from failure

For a repeatedly requested nonexistent product, short-lived negative caching may reduce repeated database work. Store an unambiguous miss sentinel only after an authoritative, authorized lookup confirms absence. Redis miss/expiry, malformed input, permission denial, database timeout and backend failure are different outcomes. A tenant-hidden record is not necessarily globally nonexistent. Bound entry size, lifetime and admission; validate identifiers before expensive work.

Unique random identifiers bypass repeated-key hits and can fill Redis with negative entries. Select admission limits, tenant/actor quotas or existing abuse controls based on observed traffic; negative caching alone is insufficient. A Bloom filter is optional and introduces maintenance/rebuild requirements and false positives; a stale filter can incorrectly reject newly created records. Never treat an approximate structure as proof of current authorized existence.

Creation must invalidate/update relevant negative entries as well as ordinary cached reads. Define the remaining stale-negative window if invalidation fails. Bounded TTL can be sufficient for a catalog; permissions, inventory reservations or financial decisions may require an authoritative path.

## Reason about interleavings

Deletion after a database write does not prevent stale population:

1. Reader loads old database value, then pauses.
2. Writer commits the new value and deletes the cache key.
3. Reader resumes and fills Redis with the old value.

First establish the actual stale interval and whether it is acceptable. TTL starts at cache population, so it alone does not bound the age of an old database snapshot or a delayed fill; account for read age, in-flight lifetime and refresh/invalidation behavior. If the required bound is not met, evaluate existing version/generation validation, an authoritative conditional transition, or a durable change/invalidation mechanism. A version in the cached payload alone cannot reject a stale fill when the newer key has been deleted. Generation/CAS schemes need a defined version authority, writer coverage and protection against expiry, eviction or reset making an old generation valid again. `SET NX` alone does not repair this race. Fixed delayed double-deletes are timing heuristics, not a general proof.

Database commit plus Redis mutation is a dual write: either side can fail independently. Reuse an existing outbox/change feed and reconciliation if the freshness guarantee requires durable invalidation. Handle duplicates and ordering so an older event cannot replace newer state. Pub/Sub/keyspace notifications can accelerate refresh but cannot be the sole reliable record. Redis expiry notifications are not an exact business scheduler.

## Control rebuild pressure

Coalesce misses within an application instance where useful; multiple instances still need an appropriate fleet-wide policy. TTL jitter, bounded refresh concurrency and selectively coordinated regeneration can protect hot keys. A regeneration lease may expire mid-fill, so apply the same stale-writer reasoning. Bound waiting; do not let lock contention create a request backlog.

Permit stale-while-revalidate or stale-on-error only for suitable data with an explicit freshness bound and a refresh owner. Never serve stale permissions or financial state as authority. During cache loss, bound database fallback concurrency and rate; automatic bypass can overload the database. Measure fallback load and recovery, not only hit ratio. Warm only a justified working set.

L1/client-side caches need entry/byte limits, tracked invalidations and a reconnect/uncertainty flush policy. An invalidation can arrive before an in-flight fill; use the client's supported race handling. Confirm that the installed client implements tracking, not merely the `CLIENT TRACKING` command.

## Evidence to select

Exercise the identified stale-fill or negative-entry creation window, concurrent rebuilds, failed invalidation and bounded cold-cache fallback in isolated application tests when changing behavior. Check values, authorization and database pressure. Guidance: [cache-aside](https://redis.io/docs/latest/develop/use-cases/cache-aside/), [consistency tradeoffs](https://redis.io/blog/cache-consistency-strategies/), [SET expiry semantics](https://redis.io/docs/latest/commands/set/), [client-side caching races and disconnects](https://redis.io/docs/latest/develop/reference/client-side-caching/).
