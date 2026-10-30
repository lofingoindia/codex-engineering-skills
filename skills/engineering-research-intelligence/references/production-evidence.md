# Production cases and architecture discovery

Use a case study when its failure mechanism can answer the local question. Extract the symptom, workload/topology, evidence, intervention, assumptions and regression/recovery costs. Compare these conditions with the existing codebase before transferring a technique. Company scale and reported improvements are not this project's measurements.

## Selected first-party cases

| Source | Useful investigation direction; applicability limit |
| --- | --- |
| [Amazon: safe idempotent retries](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) | Caller intent, token scope/lifetime, changed parameters and atomic recording; verify the actual provider/business contract rather than copying EC2 retention rules |
| [Stripe: idempotency](https://stripe.com/blog/idempotency) | Unknown completion and safe retries; historical design reasoning must be paired with current API behavior and the local side-effect boundary |
| [Shopify: inventory reservations](https://shopify.engineering/scaling-inventory-reservations) | The reported bottleneck involved connection occupancy and transaction duration, not simply query CPU; investigate actual callers and contention before changing pool limits or database engines |
| [Datadog: Postgres performance](https://www.datadoghq.com/blog/engineering/debugging-postgres-performance/) | A seemingly skipped upsert still caused row-lock/WAL work in the reported case; check engine version, plans, write evidence and concurrency correctness before copying a SQL rewrite |
| [DoorDash: write-heavy inventory](https://careersatdoordash.com/blog/how-doordash-designed-a-successful-write-heavy-scalable-and-reliable-inventory-platform/) | Workload-specific index/write/dependency costs; a JSONB or batching choice is not a default schema rule for another workload/engine |
| [Uber: fulfillment rearchitecture](https://www.uber.com/us/en/blog/fulfillment-platform-rearchitecture/) | Ownership, multi-entity workflows and post-commit work at their scale; do not infer that an ordinary monolith needs their service topology or saga framework |
| [Cloudflare: Code Mode](https://blog.cloudflare.com/code-mode-mcp/) | Tool discovery/context and execution-boundary tradeoffs; their runtime isolation and performance claims do not transfer to a bare Node VM or a different host |

These articles were opened and relevant passages examined during index creation. Their observations are first-party reports, not independently reproduced results. Avoid turning article-specific diagnostics, extension installs or live experiments into automatically authorized commands.

## Educational and curated discovery seeds

- [System Design Primer](https://github.com/donnemartin/system-design-primer): terminology, alternatives and links for framing a question.
- [Awesome Scalability](https://github.com/binhnguyennus/awesome-scalability): a discovery collection; follow the original team publication and verify its date/context.
- [System Design 101](https://github.com/ByteByteGoHq/system-design-101): explanatory diagrams and concepts; inspect actual specifications and implementations before relying on a guarantee.

These collections are not primary authority and were not audited as complete libraries. Use a relevant original case instead of loading every list or repeating its architecture diagram. Other first-party engineering teams and papers may be better evidence for the active problem; the index is deliberately non-exhaustive.

## Translate a reported improvement carefully

Determine what was measured: average/tail latency, throughput, connection occupancy, CPU/I/O, memory, recall, error rate or completed business outcomes. Check correctness, data distribution, concurrency, cache warmth, hardware, durability/isolation settings and comparison conditions. Reducing indexes can reduce writes and harm reads; batching can improve throughput and increase latency or failure scope; larger pools can amplify contention. Let the local bottleneck and required invariant decide.

Record the transferable mechanism, the conditions that differ and the smallest local verification. A case study may justify investigating a connection leak without justifying a database migration. If the current system lacks the reported conditions, retain its sound implementation and explain why the external result does not establish a better alternative.
