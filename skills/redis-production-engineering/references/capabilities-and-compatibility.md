# Capability selection and compatibility

## Choose from operations, not feature availability

| Shape/need | Candidate and decision boundary |
| --- | --- |
| Opaque value, token, counter | Strings; validate serialization, numeric precision/range, expiry and conditional-write semantics |
| Field-oriented entity | Hashes or supported JSON; compare partial updates, nesting/query needs, memory encoding and field versus whole-key expiry |
| Ordered push/pop | Lists; destructive removal alone is not reliable job completion |
| Exact membership/set algebra | Sets; bound cardinality and result sizes |
| Score/range/ordered index | Sorted sets; define tie behavior, updates, retention and hot aggregates; delayed scheduling still needs reservation/recovery |
| Replayable event log | Streams; define groups, processing responsibility, retention and persistence |
| Dense flags/packed integers | Bitmaps/bitfields; bound maximum offsets, sparse-allocation surprises, overflow and signedness |
| Approximate distinct/membership | HyperLogLog versus Bloom/Cuckoo filters; different operations/error models, capacity and lifecycle; never substitute for exact authorization |
| Location lookup | Geospatial operations; inspect radius/polygon requirements, units and candidate/result bounds |
| Query/indexed documents | Search/JSON or existing database/search service; account for indexes, update/expiry behavior, ACL/filter semantics and recovery |
| Timestamped metrics | Time series where supported; choose retention, labels, compaction and out-of-order policy |
| Similarity/AI cache | Supported vector Search/vector sets; verify dimensions, metric, filters, recall, memory and freshness, rather than treating similarity as equality |

Check each actual command's complexity, returned size and memory behavior; a compact value can still require expensive scans or large materialized results. Prefer existing relational queries when transactions, joins, durable truth or broad querying dominate. Redis may simplify a bounded leaderboard or ephemeral lookup without needing a new service, but it does not automatically replace PostgreSQL/MySQL.

For semantic caching, scope candidates by validated tenant/access context, model/prompt/embedding versions, knowledge revision and relevant request variants. Enforce authorization before returning a hit. Choose an evaluated acceptance threshold for the task; semantic proximity does not establish that an answer is correct or safe to share. Invalidate changed knowledge/permissions and bound retention. Avoid caching secrets or private agent/tool outputs into a shared public response cache. Temporary agent state requires an explicit loss/replay policy, distinct from a durable execution record.

## Verify the full compatibility chain

Determine server version/patch, edition/provider, enabled built-ins/modules, client version/API, RESP mode, topology and effective ACL. Verify actual command/subcommand/options and reply shape. A server version number alone does not prove a managed service exposes a feature, and a raw-command escape hatch does not prove correct typed decoding or retry behavior. Do not transfer Redis guarantees automatically to a fork or compatible service.

Selected version gates checked on 2026-10-30; these are examples to verify, not an upgrade target:

| Capability | Redis Open Source introduction / caveat |
| --- | --- |
| `XAUTOCLAIM` | 6.2; reply changed in 7.0 to include deleted entry IDs |
| Functions; sharded Pub/Sub | 7.0; provision libraries/shards and compatible subscriptions |
| `WAITAOF` | 7.2; preceding writes on the connection, relevant AOF configuration and returned counts |
| `HEXPIRE` | 7.4; individual hash-field TTL differs from whole-key TTL and can be cleared by field overwrite |
| `XACKDEL`, `XDELEX`, stream reference handling | 8.2; group acknowledgment/deletion semantics must match retention |
| `SET IFEQ`/related conditions and `DELEX` | 8.4; verify missing-key/type/return/TTL semantics and installed client support |
| `XADD IDMP`/`IDMPAUTO` and `XCFGSET` | 8.6; bounded producer deduplication, configuration reset and patch-specific limitations |
| Newer resource-bounding/options | Inspect target release: for example, 8.10 adds `XREAD`/`XREADGROUP` cumulative reply limits; do not send them to older servers |

Use supported older mechanisms when appropriate rather than forcing a version upgrade. Check release notes for fixes/known limitations and security status, not just a feature's introduction. Redis 8.10 GA and 8.12-RC1 appeared in the release index at research time; prerelease availability is not a production recommendation or proof of the current latest release.

Identify licensing for the exact distribution before adopting/copying it. The reviewed Redis policy distinguishes <=7.2 BSD-3-Clause, 7.4 dual RSALv2/SSPLv1 and 8+ RSALv2/SSPLv1/AGPLv3 choices; commercial products differ. Consult actual license/terms when relevant instead of inferring them from the Redis name.

Sources: [data-type comparison](https://redis.io/docs/latest/develop/data-types/compare-data-types/), [command reference/history](https://redis.io/docs/latest/commands/), [feature sets](https://redis.io/docs/latest/develop/whats-new/redis-feature-sets/), [release index](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/release-notes/redisce/), [HEXPIRE](https://redis.io/docs/latest/commands/hexpire/), [SET](https://redis.io/docs/latest/commands/set/), [semantic-cache mechanism](https://redis.io/docs/latest/develop/use-cases/semantic-cache/), [licensing](https://redis.io/legal/licenses/).
