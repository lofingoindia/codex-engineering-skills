# HTTP, network clients, streams, and real-time connections

Use for Go HTTP runtime behavior and resource safety. Preserve existing router/framework and API contracts; Go handler conventions do not automatically apply to a framework with a different lifecycle.

## Match limits to the actual operation

Inspect the server, client, proxy and protocol path. Header read, body reception, response writes, keep-alive idle time, dependency connection acquisition and application completion are different deadlines. Header limits do not limit body size. Configure relevant bounds from real operations; a universal short WriteTimeout can break SSE/downloads, while an unbounded upload can exhaust resources.

Use the request context for request-owned operations. Cancellation does not undo a write or force arbitrary handler code to return. A timeout wrapper is not a complete resource policy: standard TimeoutHandler does not support streaming/hijacking interfaces and is unsuitable for some long-lived responses. Verify request-body, application, and network termination separately.

## Handlers and middleware

Validate method, content type, bounded body and domain input as required by the existing contract. `MaxBytesReader` provides an incoming body limit; a `LimitReader` that merely truncates can make oversized input look like a complete smaller document. Do not trust Content-Length as the only size control. Bound decompressed size/work separately when compressed input is accepted.

For a single JSON document, handle malformed/trailing input and validate the resulting values; strict unknown-field behavior must be an intentional compatibility choice. Decoder revisions differ on duplicate keys, name matching and number handling. Decoding into a struct is not authorization or full domain validation.

Set response headers/status before committing the body, and handle write/encode errors according to phase. Do not write a second JSON error after starting a stream. ResponseWriter belongs to the active handler lifetime; do not continue writing from a detached goroutine after ServeHTTP returns or assume concurrent use is safe. Reuse framework middleware instead of adding a competing chain. Wrappers must preserve supported flushing/hijacking behavior or expose appropriate unwrapping for ResponseController.

Authentication, resource/tenant authorization, trusted proxy handling and request limits need correct middleware/data-boundary placement. Recover at an established safe request boundary where appropriate; recovery does not roll back partial effects, cover other goroutines, or make corrupted shared state safe.

## Outbound clients and connection reuse

Reuse configured clients/transports at their intended scope and avoid mutating their configuration while in use. Zero-value Client is usable but has no overall timeout. Client.Timeout includes response-body reads; phase-specific transport settings cover different portions of the exchange. Outgoing request contexts can bind acquisition, transfer and body consumption to the owner.

Inspect HTTP status separately from the Go error. Close response bodies on successful Do calls, including error-status responses. Consume expected bounded bodies to EOF for reuse when appropriate; for unwanted/oversized bodies, use bounded cleanup and close rather than draining an attacker-controlled stream indefinitely. Do not depend on version-specific automatic draining to conceal missing ownership.

Tune active connection capacity separately from idle keep-alive capacity, accounting for HTTP/2 multiplexing and proxy behavior. More connections do not fix downstream saturation. Preserve TLS verification and inspect redirects, proxy settings, DNS/dial restrictions and credentials for SSRF-sensitive requests.

Retry only replay-safe classified failures within one remaining time/attempt budget. A replayable request body is not proof that the business operation is idempotent. Client/transport, middleware and upstream retries may multiply attempts; inspect existing behavior before adding another layer. Ambiguous write outcomes require stable identity/status recovery.

## Streams, files, and buffers

Use `io` streaming when size warrants it; small bounded payloads do not require a pipeline framework. Handle `n > 0` data before a Read error and propagate copy/write/close failures that affect the outcome. `io.Copy` does not add context cancellation, a size limit, or persistence by itself. A wrapper that checks context before Read cannot interrupt an already blocked underlying read.

Bound both bytes and retained buffers/parallel operations. A streaming parser that accumulates an entire object is not memory-bounded. Close relevant endpoints/unblock producers on failure. Buffers borrowed from readers or pools must not be retained after reuse without a safe copy/ownership transfer. Do not publish a completed file/object after a partial transfer; clean temporary artifacts and perform required validation/commit steps.

## SSE and WebSockets

Retain existing event-driven architecture. Authorize upgrade/subscription and each sensitive operation/event scope, including session expiry and tenant changes where relevant. Use the installed WebSocket library's read/write concurrency and context rules; different clients permit different concurrent operations. Ensure control-frame/read loops, deadlines/heartbeats and cleanup fit that library.

Bound per-connection outbound queues, payloads and subscription counts. Slow consumers need an explicit policy such as backpressure, disposable-update coalescing, resynchronization or disconnect. Keep SSE flushing/proxy buffering and long-lived timeout behavior correct. A socket reconnect or heartbeat does not guarantee replay/durable delivery.

Track connection/subscription goroutines through shutdown. Server.Shutdown does not wait for hijacked WebSockets; SSE remains an active HTTP handler and may need explicit termination to finish draining. Do not add Redis fan-out or polling unless the actual topology/product requires it.
