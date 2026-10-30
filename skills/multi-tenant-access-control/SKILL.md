---
name: multi-tenant-access-control
description: Design, implement, or review tenant isolation and authorization across SaaS resources, roles, memberships, workers, caches, and administrative workflows. Use for access decisions or cross-tenant risks; skip authentication-only work and ordinary features with unchanged access boundaries.
---

# Multi-Tenant Access Control

Make every access decision consistent with the application's real subject, tenant, resource and action model. Preserve isolation across the entire workflow without imposing a policy service or a universal role hierarchy. This skill is independently usable; other engineering skills are optional for their implementation specialties.

## Establish the actual authorization model

Distinguish policy design, endpoint/query implementation, tenant-leak investigation, permission lifecycle and read-only review. Inspect applicable instructions, identity/membership schemas, existing policy helpers, routes, data ownership, workers, caches, storage and relevant versions. Trace the requested workflow; do not redesign all permissions for a local defect. During an explicitly read-only audit, keep all corrections as recommendations.

Define the trusted principal, acting tenant, requested action, resource owner and relevant context. A user's membership/role can differ across tenants. A client-selected tenant ID is a request to select a scope, not evidence of authority. Bind it to authoritative membership, service scope and actual resource ownership. A valid session or unguessable resource ID is insufficient.

Identify the invariant and its freshness requirement: who may read, change, delegate, export or subscribe to which data, and when revocation must take effect. Include legitimate allowed operations so a fix does not simply deny all work.

## Select relevant detail

| Uncertainty | Reference |
| --- | --- |
| Ownership, RBAC/ABAC/ReBAC, policy evaluation and service/admin identities | [policy-and-identity](references/policy-and-identity.md) |
| APIs, queries, PostgreSQL RLS, caches, files, search, workers and subscriptions | [enforcement-and-data](references/enforcement-and-data.md) |
| Revocation, concurrent membership changes, invitations and verification | [freshness-and-administration](references/freshness-and-administration.md) |
| Standards, product behavior and consistency tradeoffs | [sources](references/sources.md) |

## Enforce where authority exists

Reuse supported policy mechanisms and repository conventions. Keep decision semantics coherent while enforcing them at every protected entrypoint and data boundary. Frontend visibility can guide UX but cannot enforce backend authorization. Internal jobs and admin routes are not implicit exceptions.

Prefer deny-by-default with explicit grants and bounded scope. Distinguish a policy deny from an unavailable/unknown decision; do not convert dependency failure into permission. Any use of cached decisions must satisfy the defined freshness and risk model. Do not force a live database read on every low-risk request when the existing secure model meets that requirement.

Scope both selected resources and associated IDs, fields, counts and side effects. Preserve tenant ownership when linking or moving records. Avoid filtering after pagination or returning private fields and hiding them only in the client. Carry trusted, validated context through async processing without treating old role claims as indefinitely authoritative.

Choose a local policy model, database constraints/RLS, or an external policy engine from demonstrated relationship complexity, consistency, ownership and operational needs. Do not introduce OpenFGA, OPA or Zanzibar-style infrastructure merely because the app has several roles. Do not replace a working model for stylistic uniformity.

## Verify access and lifecycle

For implementation, derive focused allowed/denied cases from the actual model: different tenants and roles, tampered related IDs, bulk paths, field restrictions, revoked actors and the relevant async/cache path. Verify server/data behavior and resulting state, not only a hidden button or an HTTP status. Exercise relevant concurrent policy transitions when correctness depends on them.

Use isolated authorized data and existing tests. Read-only work must not mutate memberships, policy stores or databases to demonstrate a hypothesis; record the necessary separate validation. Report inspected enforcement paths, test evidence, freshness guarantees, remaining bypasses/uncertainty and compatibility impact without claiming complete isolation from a helper test alone.
