# Tenant isolation, security and client ownership

## Key identity is part of the application contract

Reuse one suitable key builder. Derive tenant/actor identity from authenticated, authorized application context; never trust an arbitrary request tenant ID merely because it becomes a key prefix. Include the relevant environment/application, purpose, schema version and canonical resource identity. Encode components unambiguously with bounded lengths; prevent separator, glob and `{...}` hash-tag injection when components participate in patterns or placement. Define case/Unicode normalization from actual identifier semantics, not convenience.

Track value format, maximum size, owner, TTL/retention, invalidation writers and any migration overlap for each affected key family. Cache queries and aggregates need the correct tenant/filter/permission variants. Keep user-scoped output distinct when two users in the same tenant have different visibility. Prefixes prevent accidental collision, not unauthorized access.

Logical databases share process resources and administrative scope; they are not a tenant security boundary. Pub/Sub channels ignore database selection. Use separate credentials, instances or service boundaries when the threat, workload policy or noisy-neighbor risk requires actual isolation. Avoid one instance per tenant as an automatic rule. Tenant quotas and bounded cardinality can improve fairness without pretending they isolate failures.

In Cluster, related multi-key operations generally need one slot. Use a deliberate hash tag for the atomic aggregate, encoding environment/application/tenant as needed to avoid unrelated hot spots. Tagging every key with only a tenant ID can put that tenant's entire workload on one shard. Untagged keys may already be adequate. Design for the current topology and real scaling boundary; do not require Cluster for hypothetical growth.

For invalidation/deletion, constrain scope from trusted identity. Prefer known key families or an existing bounded index. `SCAN` is incremental, not a snapshot: it can return duplicates and has weak guarantees for keys changing during iteration; `COUNT` is a hint, and Cluster scans require topology-aware coverage. A scan-and-delete sweep cannot alone prove complete concurrent tenant erasure. Avoid `KEYS` or broad flushes on live shared datasets; `UNLINK` can defer freeing large values but does not make an unbounded sweep free.

## Enforce credentials and application authorization

Keep Redis private to trusted services; never connect untrusted web/mobile clients directly. Restrict exposed container/host ports, require authentication and use verified TLS where applicable, including topology/discovery connections. Protected mode alone is not a network security design. Keep credentials out of logs, command histories, URLs in telemetry and client bundles. Protect persistence/backups as sensitive data too.

Use least-privilege command allowlists, key patterns and separate channel permissions. Key rules do not restrict database-wide operations with no key arguments: `~tenant:* +@all` does not safely confine `FLUSHALL`/`FLUSHDB`/`SWAPDB`. Restrict administrative, scripting/module/configuration and introspection capabilities according to need, with separate operational credentials. Broad command categories can change as capabilities evolve. Verify effective rules and negative access cases using supported tooling.

A shared service Redis credential does not let Redis distinguish that service's end users; backend authorization still owns that boundary. Check long-lived subscriptions, permission caches, indexes/search results and workers too. Revocation needs explicit handling of existing connections and cached authorization. Turning an ACL user `off` denies new authentication but does not by itself disconnect previously authenticated clients; inspect the supported revocation procedure.

## Audit the installed client's failure behavior

Reuse long-lived clients/pools and existing configuration. Set budgets for connect, pool acquisition, commands and total request/retry time separately where supported. Bound connection count, offline queues, pipeline payloads and application concurrency. A huge pool cannot make serialized commands execute faster and can amplify overload. Blocking stream/queue reads, subscriptions and `WATCH` may need dedicated/isolated connections; size from real ownership rather than one connection per request.

Trace every retry layer, automatic resend, offline queue and topology redirection. A command may commit before a lost reply; cancellation/timeout is not rollback. Blindly retrying `INCR`, `LPUSH`, an idempotency claim or a non-idempotent script can duplicate effects. Document whether the client rejects, queues unsent commands or resends uncertain commands, and who reconciles ambiguity. Configure bounded backoff/jitter to avoid reconnect herds. Verify `MOVED`/`ASK`, Sentinel discovery, announced endpoints, replica-read staleness and TLS/auth behavior for the actual topology.

On shutdown stop intake, stop subscriptions/blocking work, drain or release owned work with a bound, then close clients using the installed API. Do not promise all work completed merely because the socket closed. Rotate credentials through a tested overlap/revocation procedure without exposing them.

## Evidence to select

Test tenant A versus B with colliding resource IDs, ambiguous input encoding, revoked access and stale subscription output when these boundaries change. Exercise unknown command completion with the actual library; mocks rarely model resend behavior. Sources: [ACL semantics](https://redis.io/docs/latest/management/security/acl/), [security model](https://redis.io/docs/latest/operate/oss_and_stack/management/security/), [Cluster placement](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/), [SCAN guarantees](https://redis.io/docs/latest/commands/scan/). Client implementation observations and research entrypoints are in the [source index](sources.md).
