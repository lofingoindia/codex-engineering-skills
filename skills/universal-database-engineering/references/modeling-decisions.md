# Modeling facts, relationships and lifecycle

## Start from the existing business model

Trace the requested workflow through persisted facts and their writers. Describe the affected record's grain: one order, one line, one membership, one reservation or one measurement at a defined time. Identify candidate/business keys as well as physical IDs. A surrogate primary key does not enforce the business uniqueness rule.

Understand functional dependencies: which attributes are determined by the same identity, and under which temporal/tenant scope? Repeating a mutable fact under several owners creates update anomalies unless a deliberate representation requires it. Normalization is a tool to prevent those anomalies, not a target normal-form count. Conversely, splitting co-owned scalar fields into many one-to-one tables can add joins, locks and deployment complexity without protecting a new invariant.

Do not assume the ORM's class boundaries, API response shape or a noun in the requirement should each become a table. Check existing columns/relationships and extension points first. Reuse a table when its identity, meaning and lifecycle fit; do not overload an unrelated table merely to avoid a justified new entity.

## Compare only plausible shapes

| Decision | Evidence that can justify it | Cost to make explicit |
| --- | --- | --- |
| Extend existing record | Same identity/owner/lifecycle; bounded scalar or structured attribute | Width, write contention, validation and compatibility |
| Separate child/entity | Independent identity/lifecycle, repeated children, distinct retention/security or independent access | Referential integrity, joins, deletion and transaction scope |
| Junction/association | Actual many-to-many relationship, possibly its own attributes/lifecycle | Scoped uniqueness, valid endpoints and high-degree access |
| Embed/document/JSON | Co-accessed bounded aggregate with suitable update/validation semantics | Growth, indexing, independent updates and cross-record constraints |
| Reference related data | Shared independent fact, unbounded children or separate lifecycle | Lookup cost, integrity and visibility across updates |
| Store historical snapshot | Business meaning is “as agreed/observed then” | Immutable provenance, correction policy and privacy/retention |
| Store aggregate/read model | Measured repeated computation cost or required consistent aggregate | Update atomicity/lag, duplicate handling, rebuild and drift detection |

An order line's agreed unit price and a product's current price are different facts. Replacing the historical price with a live join can corrupt business meaning; duplicating the current product name into every mutable representation can instead create drift. Decide from semantics, not resemblance of values.

Membership roles often depend on both user and tenant, rather than the user globally. A status enum may be sufficient for a small fixed lifecycle; a lookup table is justified when values have independent metadata, permissions or ownership. A large number of nullable fields is evidence to investigate subtype/optional data, not automatic proof of a required split. A JSON field is not a substitute for known core relationships merely because it avoids a migration. EAV/polymorphic designs need a real extensibility requirement and an honest constraint/query tradeoff.

## Define the stored value precisely

Choose types from the value's domain, bounds, precision, comparison and supported engine behavior. Define unknown/absent/not-applicable semantics explicitly; an empty string or zero default can silently invent a fact. Nullability and defaults must preserve actual business meaning and mixed-version writes. A `CHECK` expression is not necessarily a not-null rule.

For money, choose exact decimal or bounded integer units with currency and rounding rules appropriate to the product; do not assume all currencies have two fractional digits or that every runtime preserves database numeric precision. For temporal data, distinguish an instant, local calendar date, recurring local time and recorded/valid time. Normalize representation intentionally and preserve a relevant time-zone identity for future local-time scheduling. Verify engine/driver conversion, precision and daylight-saving behavior where relevant.

Choose identifier strategy from uniqueness scope, generation ownership, ordering, exposure and index/storage cost. Preserve compatible existing IDs unless a real weakness justifies change. Composite versus surrogate keys is a tradeoff, not a style rule. Treat text length, encoding, collation/case equivalence and canonicalization as part of identity and uniqueness, not merely display. Bound large objects and consider existing object storage with an explicit metadata/deletion lifecycle when it fits.

State fields, timestamps, flags and counters must represent distinct facts. Several writable indicators of the same state need a synchronization rule or consolidation. Generated values can avoid duplicated writable truth when supported and suitable; do not use them to hide expensive work or version-specific restrictions.

## Enforce relationships and lifecycle

Use supported primary/unique/foreign-key/check/validation mechanisms for invariants they actually express. Application prechecks alone cannot establish concurrent uniqueness. A row-level check cannot generally prove an aggregate across changing rows. Define insert, update, delete, restore and reparent behavior; cascading deletion is a business choice, not boilerplate. Soft deletion changes uniqueness, visibility, retention and relationship semantics and does not automatically satisfy erasure requirements.

For tenant-owned relationships, prevent a child in tenant A referencing tenant B's parent. A foreign key on a globally unique parent ID alone does not couple the child's tenant to that parent's tenant. Where appropriate, use a tenant-qualified reference to a supported unique parent key plus required nullability; the extra constraint/index may protect a real invariant despite apparent overlap. Global/shared resources need their explicitly different policy. Constraints do not replace read authorization.

Audit/history records need defined actor, ordering/identity, time semantics, integrity and correction/retention behavior. Do not introduce event sourcing for every history requirement. If derived or duplicated data is necessary, identify the authoritative writer and correctness boundary, then define rebuild and reconciliation before treating it as maintained truth.

For an actual change, verify the relevant invalid as well as valid state, deletion/restore path and competing writer. Compare model alternatives using the real queries and lifecycle, without rewriting working structures for aesthetics. Sources: [data-store models](https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/understand-data-store-models), [OLTP reasoning](https://learn.microsoft.com/en-us/azure/architecture/data-guide/relational-data/online-transaction-processing/), [constraint semantics example](https://www.postgresql.org/docs/current/ddl-constraints.html), [document modeling](https://www.mongodb.com/docs/manual/data-modeling/).
