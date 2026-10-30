# Policy, identities, and resource ownership

## Establish a decision vocabulary

Describe decisions using subject, action, resource, tenant and applicable context. Find the source of truth for each value and which service owns the final enforcement. Distinguish authentication identity from active tenant membership, role assignment, resource relationships and platform privileges. Do not derive a global role from a role in one organization.

Determine the actual hierarchy: a workspace/store may belong to a tenant, a resource to a workspace, and a user to several tenants. Model only relationships that exist. Explicitly identify globally shared/public resources and any intentionally cross-tenant collaboration rather than assuming every row uses the same ownership rule.

| Model | Appropriate use and cost |
| --- | --- |
| RBAC | Stable job roles with clear tenant-scoped permissions; avoid role explosion for every resource combination |
| ABAC | Decisions depend on trusted attributes such as ownership, resource state or environment; define attribute authority and freshness |
| ReBAC | Sharing, groups, nested ownership or collaboration needs explicit relationships; bound traversal and understand consistency |
| Hybrid | A role grants a capability while ownership/relationship/state limits the affected resources; keep the combined semantics explicit |

These are reasoning options, not package requirements. Existing SQL and application checks can express an appropriate small policy. A separate engine is justified by concrete reuse, complexity or policy governance requirements, and adds distribution, availability and debugging costs.

## Preserve coherent policy semantics

Default to no grant when the relevant policy is absent or does not match. Define inheritance and exceptions explicitly; owner/admin does not automatically mean unrestricted platform access. Review combined allow/deny behavior and unsupported actions, not merely the happy-path role table. If an engine returns undefined/errors, the caller must not interpret that as allow.

For an external policy service, inspect the actual request inputs, deployed model/policy version, data replication, decision API, error semantics and caller enforcement. Centralizing a decision does not make all APIs enforce it, synchronize its data with business records, or eliminate the need to review resource ownership. Prevent subject/resource ID collisions across tenants in the model namespace.

Keep a simple permission vocabulary tied to business actions. Avoid spreading unrelated role-name string comparisons across handlers, but do not create a policy abstraction framework to hide a small clear conditional. Reuse the project's current helper/policy layer when it expresses the invariant correctly.

## Actor, subject, and service scopes

Tenant administrators can manage only their authorized tenant, assignable roles and resource scope. Validate who can invite, grant, revoke, transfer or impersonate; possessing an admin UI does not grant every permission a payload requests. Prevent escalation through custom-role creation, bulk assignment, inherited roles or changing the target tenant of a membership.

Separate platform superadmin/support privileges from tenant roles. Define the real supported operations, tenant selection, accountability and any required step-up/approval using existing product controls. For impersonation/delegation, preserve both original actor and effective subject, bounded scope, expiry and audit context; do not silently replace the actor with an unrestricted user token.

Service accounts and workers need scoped authority appropriate to the workflow. Avoid accepting an arbitrary tenant header on a trusted service credential. Derive scope from authenticated workload identity, validated message provenance and owned business records. A producer's assertion that it was authorized is not perpetual authority for every downstream action.

Avoid exposing excessive private identity/permission data through list-users or policy APIs. Authorization configuration itself needs access control and versioned change handling. Keep human-readable decision reasons useful to operators without revealing another tenant's resources to an unauthorized caller.
