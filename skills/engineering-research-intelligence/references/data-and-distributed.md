# Databases, messaging, and throughput research

## Match engine, version, client, and workload

Start with server/extension versions, driver/ORM/pooler behavior, schema/indexes, effective transaction/durability settings and the actual query/workflow. Read the relevant SQL, callers, transaction boundaries and workload evidence before searching for an optimization.

| Domain | Authoritative entrypoints |
| --- | --- |
| PostgreSQL | [Versioned documentation](https://www.postgresql.org/docs/), [transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [locking](https://www.postgresql.org/docs/current/explicit-locking.html), [HOT](https://www.postgresql.org/docs/current/storage-hot.html), [EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) |
| MySQL | [Documentation/version selection](https://dev.mysql.com/doc/), [InnoDB 8.4 isolation example](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html); select the actual deployed engine/version, not 8.4 by default |
| Drivers/pooling | [node-postgres transactions](https://node-postgres.com/features/transactions), [pooling](https://node-postgres.com/features/pooling), [PgBouncer features](https://www.pgbouncer.org/features.html); use corresponding official client docs for Go/Python/Dart or another installed stack |
| Redis | [Redis docs](https://redis.io/docs/latest/) and [Streams](https://redis.io/docs/latest/develop/data-types/streams/): persistence, eviction/retention, delivery, client reconnection and version-specific semantics |
| RabbitMQ | [RabbitMQ docs](https://www.rabbitmq.com/docs/) and [confirms/acknowledgments](https://www.rabbitmq.com/docs/confirms): queue type/configuration, routing, persistence, retry/ack ownership and recovery |
| APIs and SaaS boundaries | [IETF HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [OpenAPI specifications](https://spec.openapis.org/oas/), [OWASP guidance](https://cheatsheetseries.owasp.org/), and [tenant isolation](https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html): select the actual contract, identity/tenant model and version |

SQL syntax similarities do not establish equivalent locking, default isolation, upsert, planner or durability behavior. The inspected MySQL 8.4 InnoDB reference describes REPEATABLE READ as default; PostgreSQL's documentation describes its own semantics. Verify actual settings and operations rather than transferring an optimization across engines.

For infrastructure, use official documentation and release notes for the actual cloud/provider, container runtime, orchestrator and observability components. Separate managed-service guarantees from self-hosted configuration and library behavior. Research effective deployment settings and recovery constraints rather than copying a cloud reference stack or adding an orchestrator.

Driver behavior matters: node-postgres explicitly requires one client for a transaction, while a convenience pool query is not a transaction owner. Generalize the question—connection/transaction ownership—not the JavaScript API to another driver. Pool size alone is not evidence of usable concurrency.

## Repository and research seeds

- [PostgreSQL source](https://github.com/postgres/postgres): investigate the relevant engine branch, regression tests and documented rationale when public documentation leaves internals uncertain.
- [MySQL source](https://github.com/mysql/mysql-server): distinguish server/engine/version and test coverage; do not assume PostgreSQL internals explain InnoDB.
- [pgvector](https://github.com/pgvector/pgvector): extension support, operators, exact versus approximate search, filtering, recall, maintenance and workload evidence.
- [CMU database systems](https://15445.courses.cs.cmu.edu/fall2025/) and [MIT distributed systems](https://pdos.csail.mit.edu/6.5840/): educational foundations for reasoning; not deployed product guarantees or universal tuning instructions.

The [pinned pgvector HNSW scan implementation](https://github.com/pgvector/pgvector/blob/44624c1f8d17327943fbe9a62fa96b3fbd59d2b2/src/hnswscan.c) was inspected for snapshot/locking and bounded iterative-scan behavior. That ref had a 2026-10-28 commit and was non-archived when checked. Reading it does not measure recall, validate this app's tenant filters or justify adding an approximate index. The other engine repositories are discovery seeds here, not full source audits.

For high-write problems, select evidence for correctness, contention/deadlocks, connection hold time, write/index/WAL amplification, vacuum/maintenance and recovery, not only query count or average latency. [Production cases](production-evidence.md) can reveal mechanisms worth checking locally. Do not run EXPLAIN ANALYZE, installs or fault injection against an audited/live system under a presumed read-only exception.
