# Protocols and integrations

Use this reference when the communication style or an integration is actually in scope. Do not migrate a working interface merely because another protocol offers attractive features.

## Choosing a boundary

| Candidate | Useful when | Costs and constraints to establish |
| --- | --- | --- |
| In-process call | Components share a deployment and trust boundary | Preserve useful module boundaries; adding a network hop adds failure modes |
| HTTP resource/command API | Broad web/mobile/third-party compatibility, ordinary request/response | Latency/round trips, supported media/contracts, cache and retry semantics |
| GraphQL | Consumers need varied graph-shaped projections and schema tooling | Resolver cost, authorization at every path, client cache/schema evolution, partial errors |
| gRPC | Controlled clients need typed RPC/code generation or streaming | HTTP/2/proxy support, browser/gRPC-Web constraints, deadlines, generated-client lifecycle |
| Durable event/queue | Producer and consumer need independent timing or reliable asynchronous delivery | Delivery/ordering semantics, lag, deduplication, replay, schema evolution, operations |
| Webhook | Notify an independently operated consumer | Signatures, retries, duplicates, receiver outages, SSRF and secret rotation |
| SSE / WebSocket | One-way server updates / bidirectional interactive sessions | Connection/proxy limits, backpressure, auth lifetime, reconnect and resume semantics |

Compare only plausible options for the actual consumers and workload. Decide who owns state and consistency before deciding transport. A small application can keep one deployment and its current HTTP stack. Service separation should follow ownership, independent scaling/deployment, or trust requirements that justify distributed failure handling. A gateway can centralize edge concerns when warranted; it does not replace object authorization inside a service.

## GraphQL

Use the [released specification](https://spec.graphql.org/) supported by the implementation, rather than assuming the working draft is deployed. Define nullability for real failure behavior: errors at non-null fields propagate to the nearest nullable parent and may null the entire data result. Account for data-plus-errors in clients; HTTP status alone cannot establish operation success. Verify the chosen HTTP transport/library behavior separately from the core GraphQL spec.

Authorize the underlying data/action, including nested fields, node lookup, aliases, batches, and mutations. Limit complexity/cost, depth, breadth/aliases, list sizes, batch count, execution time, and concurrent expensive work. An HTTP request-rate limit alone cannot bound one expensive query. Scope batching/DataLoader caches to request and identity as appropriate to prevent leaks. Persisted operations are useful for controlled consumers when justified; blanket disabling introspection does not enforce permissions and can damage legitimate developer tooling ([GraphQL security](https://graphql.org/learn/security/)).

Evolve the schema with supported consumer usage evidence and deprecation. Check added required inputs, changed output nullability and enums, generated clients, persisted queries, and cache identity behavior. Serial mutation execution within one request is not a cross-request transaction or an exactly-once guarantee.

## gRPC and Protobuf

Set realistic deadlines; gRPC clients do not have a useful finite deadline automatically. Propagation behavior varies by language. Server application work must cooperate with cancellation ([deadlines](https://grpc.io/docs/guides/deadlines/)). Configure retry only for operations with safe repeated effects, considering transparent retries, status policies, throttling and deadlines. Response commitment constrains library retry behavior; client cancellation or DEADLINE_EXCEEDED does not prove an application effect did not commit ([retry guide](https://grpc.io/docs/guides/retry/)).

For Protobuf evolution, preserve field numbers, reserve removed numbers/names, examine presence/default/enum behavior, and verify the actual language/runtime. Binary wire compatibility does not guarantee ProtoJSON, generated-source, or semantic compatibility; review transcoders and clients. Reuse channels with appropriate pool/connection and message-size limits; streaming requires flow control and application-level bounded buffering ([Protobuf evolution](https://protobuf.dev/programming-guides/proto3/#updating)).

## Webhooks, events, and live connections

For incoming webhooks, verify the provider's signature over the exact received bytes before acting, using its library and replay-window rules. Map verified provider/account identity to the tenant rather than trusting a tenant field. Support rotation and bounded parsing. Persist receipt/work durably before acknowledging success when later processing is promised; do not merely spawn an in-memory task. Atomically deduplicate delivery with the business effect, handle out-of-order events, and reconcile missing/current state where appropriate. Provider event IDs identify deliveries/events; distinct events may still describe the same business effect. Do not infer ordering from a coarse timestamp ([Stripe webhooks](https://docs.stripe.com/webhooks)).

For outgoing delivery, define event identity/schema, signing format and timestamp, secret rotation, ordering scope, bounded retries/backoff, timeout, retention and replay/dead-letter recovery. Authenticate destination changes and apply SSRF-safe egress. Deliveries can duplicate after a receiver commits but its acknowledgement is lost. Document at-least-once behavior or the actual bounded guarantee rather than promising universal exactly-once processing.

For events, decide who owns schema evolution and which historical versions consumers must replay. Make deduplication retention fit the redelivery/replay horizon. Reauthorize async data access if permissions can change; do not leak sensitive payloads to an unauthorized subscriber through a stale subscription.

For SSE/WebSocket or streaming RPC, define resume tokens/sequence and retention, gap behavior, heartbeat/reconnect, bounded buffers and slow-consumer handling. Verify infrastructure idle timeouts and connection limits. Revalidate long-lived authorization at an appropriate point and handle expiry/revocation. Choose SSE for a one-way need when its deployment support suffices; bidirectionality is a reason for WebSocket, not a default requirement.
