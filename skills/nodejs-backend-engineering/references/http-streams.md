# HTTP lifecycle, streams, and real-time work

Use for service/client requests, proxy interactions, large payloads, uploads, or persistent connections. Preserve existing HTTP clients, framework hooks, and API contracts where sound.

## Separate the timeout boundaries

Read the installed framework, Node.js, client, and proxy settings. Header/body reception, inactive sockets, application execution, outgoing connection acquisition, upstream headers/body, and keep-alive reuse are different lifetimes. A socket inactivity timeout does not establish an end-to-end application deadline. Node's `request.setTimeout` emits a timeout event; it does not abort the request by itself.

Choose budgets from the user operation and deployment limits. Include retries, queue waits, and response consumption; propagate the remaining budget. Add real cancellation or disposal to a timeout. A low global setting can break legitimate uploads or slow clients; a high global setting can retain scarce resources during abuse. Bound relevant sizes and concurrency as well as time.

Inspect disconnect semantics before wiring cancellation. An incoming request's `close` can follow normal body completion; do not abort every handler on that event. Use framework-supported signals or lifecycle events with completion flags. Response `finish` indicates output handed off for transmission, not client receipt. Prevent double sends and writes after a response has ended; once headers or a streamed body are committed, a fresh JSON error may be impossible.

## Outgoing requests

- Reuse an appropriate owned client/dispatcher and connection pool. Native `fetch` uses Undici; configuring `http.Agent` does not configure that fetch pool. Check bundled versus separately installed Undici versions before using its options.
- `fetch` resolves for HTTP errors. Inspect status and validate the bounded response before treating it as success. Consume or cancel unused bodies to release connection resources; do not depend on garbage collection.
- Keep body-reading and streaming within the operation's deadline. Receiving headers is not completion. Avoid unrestricted `text`, `json`, or `arrayBuffer` calls for untrusted or large responses.
- Retry only classified transient failures within a bounded total budget and the operation's replay semantics. Use backoff/jitter and applicable server retry guidance. Avoid retries at every layer. An interrupted mutation can already have committed; recover through a stable operation identity/status rather than a fresh duplicate action.
- Configure redirects, credentials, TLS verification, and trusted proxy behavior deliberately. User-controlled outgoing URLs require SSRF defenses across redirects and address resolution, not merely a hostname regex. Do not disable TLS validation to fix integration failures.

## Streams and large transfers

Prefer existing streaming APIs for large transfers. Respect `write()` returning false and resume on `drain` with close/error handling. Async `data` listeners are not awaited by EventEmitter, so they can silently create unlimited concurrent writes or transformations.

Use `stream.pipeline`/its Promise API when its destruction and cleanup semantics fit the boundary; propagate cancellation. Plain `pipe` does not provide the same complete error handling. Pipeline may destroy an HTTP socket on failure, preventing a later error response. Validate preconditions before committing output and choose an error strategy appropriate to the stream phase.

`highWaterMark` is a backpressure threshold, not a process memory ceiling. Object mode counts objects; large objects, transform buffers, concurrent streams, and downstream queues still multiply memory. Node streams and Web Streams have different APIs; use supported adapters rather than assuming interchangeability.

Bound compressed and expanded bytes, file count, parsing complexity, temporary disk use, and concurrent transformations where applicable. Streaming bytes through a parser does not make a parser that accumulates the entire document bounded. Use allowlisted file destinations/names and safe temporary-file handling; clean up interrupted partial transfers. Publish a completed file/object only after the required validation and durability steps. Preserve the existing upload protocol rather than inventing one.

## SSE and WebSockets

Use only when the product and backend support long-lived updates. Integrate upgrade/subscription authorization, allowed origins where relevant, tenant filtering, expiry/revocation, and subscription cleanup. A connection authenticated once does not guarantee authorization forever.

Account for proxy buffering, idle limits, heartbeats, reconnect behavior, maximum payloads, and per-client outbound buffers. Slow clients need a defined policy: backpressure, coalescing disposable updates, resynchronization, or disconnection. Never allow an unbounded subscriber queue. Bound compression cost; do not enable it solely because it is available.

Sockets and heartbeats do not establish durable delivery. Sequence/resume or snapshot reconciliation is needed when missing updates affects correctness. Reconnection must not multiply listeners or duplicate business actions. Multiple replicas require an existing appropriate fan-out/state strategy; do not introduce a broker for a single-process feature without need.

## Focused verification

For the affected path, choose a slow or malformed body, disconnect during an upload, upstream error with an unread body, retry after ambiguous write completion, or a slow subscriber. Verify cleanup and bounded work. A happy-path HTTP response does not prove connection reuse, cancellation, or shutdown correctness.
