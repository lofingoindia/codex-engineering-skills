# Freshness, administration, and focused verification

## Define revocation precisely

State what must stop after a membership/permission change: new reads, writes, subscriptions, queued user work or downloads. Define allowable propagation delay and treatment of already-running operations. Immediate revocation across disconnected services and pre-issued capabilities cannot be assumed from deleting one membership row.

JWT claims and cached policy decisions are snapshots. Choose expiry, policy/session versions, invalidation events or authoritative checks according to risk and existing architecture. High-impact changes may need stronger freshness; that does not imply a database lookup for every low-risk operation. An invalidation event can be lost or delayed, so define the bounding expiry or reconciliation mechanism when needed.

OpenFGA's documented default can use cached decisions; its higher-consistency option bypasses that cache. It does not automatically make a separate business database transaction atomic with the policy decision. Inspect actual engine/storage guarantees rather than inferring them from an option name. Apply equivalent reasoning to replicated OPA data/bundles or another installed policy system.

When a decision service fails, return an appropriate unavailable/unknown outcome without granting access. Existing bounded, previously validated read permissions may be usable only where explicitly allowed by the product's security/freshness model. Never use stale grants for arbitrary privileged operations merely to keep a screen green.

## Handle concurrent policy changes

Check-then-write can race membership removal, ownership transfer or resource reassignment. Use an atomic conditional change, appropriate transaction/locking, or supported version checks at the owning state boundary when the invariant requires it. A remote authorization request alone cannot lock unrelated database state.

Define and preserve administrative invariants such as preventing removal of the last owner, limiting assignable privileges, and forbidding ownership transfer to an ineligible account. Two concurrent valid-looking demotions can violate a last-owner rule unless it is protected atomically. Do not add distributed locks if a local transaction or conditional update is sufficient.

Invitations should bind tenant, intended identity, permitted role/scope, expiry and single acceptance. Validate verified identity and current inviter/acceptance policy; a stale invitation must not silently restore privileges after revocation. Removal/reassignment should update relevant service accounts, sessions, caches and subscriptions according to the defined model, without deleting unrelated tenant memberships.

Keep original actor, effective subject, tenant, target, policy/action and result in appropriate protected audit history for privilege changes and impersonation. Redact credentials and sensitive attributes. Do not log private data from a denied resource as part of explaining the denial.

## Verify the actual matrix, not a fictional universal one

For implementation work, choose representative principals/resources from the inspected model and verify both intended grants and denials. Follow the changed workflow beyond the HTTP response to data state and downstream outputs.

| Risk under change | Useful test focus |
| --- | --- |
| Tenant-qualified lookup | Same actor with different memberships; resource and related IDs from another tenant; legitimate same-tenant access |
| Field/bulk operation | Mixed authorized/unauthorized items and protected fields; no partial leak outside the documented result contract |
| Cache/search/export | Warm a response under one scope, then access under another; check counts, files and account-switch behavior |
| Revocation/role change | Old session/decision cache and queued or subscribed work after the relevant freshness bound |
| Concurrent administration | Simultaneous demotions/transfers/invite acceptance with final owner/membership invariants checked |
| RLS/pooling | Real application role; absent/incorrect context; pooled reuse and mutations, not only owner-role SELECT tests |

These are selections for real changes, not instructions to create a large evaluation harness. Use authorized isolated fixtures and existing tests. For read-only review, inspect reachable enforcement, schema/policies, test definitions and safe available evidence; describe runtime/concurrency validation separately instead of changing roles or test data.

Report the established guarantee and its limits: an isolated helper test does not prove every API, storage path or worker is covered. Record uncovered entrypoints, stale-data windows and unavailable infrastructure accurately. Avoid false claims of immediate revocation or perfect isolation, and avoid broad denials that break legitimate tenant administration.
