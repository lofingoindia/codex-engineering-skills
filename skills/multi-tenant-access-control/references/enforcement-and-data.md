# End-to-end enforcement and data isolation

## APIs and persistence

Trace every resource lookup and side effect from the entrypoint. Bind requested IDs to the authorized tenant and actual parent resource, including nested paths, association IDs, imports, batch items, GraphQL resolvers and RPC calls. Filtering a top-level list does not secure a detail lookup or mutation. Client-provided ownership fields must not reassign data implicitly.

Apply authorization before pagination, aggregation and serialization. Counts, facets, autocomplete, sorting/search, error differences and related-object expansion can leak data even when the returned rows look scoped. Distinguish field-level read permissions from write permissions; a writable DTO should not include every database column. Preserve the established 403/404 disclosure policy without making errors the only protection.

Tenant-qualified keys, joins and composite foreign-key/uniqueness constraints can prevent cross-tenant associations where the schema requires them. Choose constraints from actual ownership: globally unique IDs do not themselves enforce tenant access. Check that a transaction cannot authorize one record then update another, and that every affected bulk item follows the intended all-or-partial-success contract.

## PostgreSQL RLS where used

Inspect the real database connection role and effective privileges, not just migration DDL. RLS must be enabled on relevant tables. Owners normally bypass it; superusers and BYPASSRLS roles bypass it, and FORCE ROW LEVEL SECURITY does not turn such roles into safe unprivileged application roles. Verify views, privileged functions and their security context as additional access paths.

Understand `USING` for visible/existing rows and `WITH CHECK` for inserted/updated values. Permissive policies combine with OR and restrictive policies with AND; one broad permissive grant can invalidate an intended restriction. RLS does not cover all operations, including TRUNCATE, and referential/uniqueness checks can disclose information through errors. Do not claim a complete authorization policy from one SELECT filter.

Use trusted request context. If tenant context is passed through a session setting, bind it to the transaction and connection that execute the query, verify missing-context behavior, and prevent leakage on pooled connection reuse. Transaction pooling cannot rely on a previous session's SET state. Validate the actual driver's transaction API and pooling mode. An application-controlled tenant setting is not a barrier against arbitrary SQL execution by a compromised application role.

Test RLS with the real non-owner application role, including insert/update and an absent/wrong tenant context; tests run as the migration owner can give misleading results. Keep general query tuning/migrations with the database's own engineering workflow.

## Non-SQL and asynchronous boundaries

- Cache decisions and responses under the complete required scope: tenant, principal or permission/version context, action and resource as applicable. Not every response needs a per-user cache, but its key must reflect every factor that changes authorization. Recheck shared/CDN caches and logout/account switching.
- Search indexes, materialized reports and exports need equivalent scope and deletion/revocation handling. Filtering after retrieval can leak counts, ordering or raw documents. Large asynchronous exports need authorization at appropriate lifecycle points and protected download access.
- Object keys/prefixes are not storage authorization. Bind signed downloads/uploads to permitted objects, methods and lifetime. A previously issued signed URL may remain usable until expiry; if stricter revocation is required, choose a supported design that can enforce it.
- Workers, scheduled tasks and messages need durable trusted tenant/resource identity, scoped credentials, and an explicit delegated-versus-system authority model. Revalidate as required before execution; do not blindly replay obsolete session role claims. Validate event provenance and resource binding.
- WebSocket/SSE channels and notifications need authorized subscription targets, message filtering and membership-change handling. Do not broadcast privately then expect the client to discard unauthorized events.

Trace isolation through each actual path; do not add these systems merely to satisfy the list. Review failure paths, retries and recovery for context loss, including cross-tenant batches or stale caches after account switching.
