# Untrusted input, output, and integrations

## Trace sources to sensitive sinks

Find actual parsing, normalization, transformations and execution paths. Validate structure, sizes, ranges and business state at the owning boundary; do not confuse a TypeScript type with runtime validation. Allow only fields a caller may set. Derive privileged fields, tenant ownership, prices and workflow transitions from authoritative state rather than mass-assigning a payload.

Use parameterized SQL and appropriate ORM APIs; identifiers, sort expressions and raw fragments still need controlled selection. Keep untrusted input out of shell command strings, unsafe template evaluation and object deserialization capable of executing code. Use constrained argument APIs and parser formats appropriate to the actual input. Escaping one context does not make input safe in all others.

## Browser and HTTP boundaries

Render text through the framework's normal escaping. Rich HTML requires a maintained sanitizer and a deliberate allowed-content policy; raw HTML, URL schemes, SVG and DOM sinks need context-specific review. CSP can reduce impact but does not repair an injection sink. Avoid disabling sanitization to make user content render.

CORS controls browser access to responses, not who may call the API. Use explicit allowed origins and credentials behavior appropriate to the product, not permissive reflection. Preserve CSRF protections for ambient credentials. Validate postMessage origins and intended recipients where used. Review redirect targets using structured same-origin/allowlist rules rather than substring checks.

Where reverse proxies/CDNs and HTTP servers disagree on message framing, request smuggling is an infrastructure/parser compatibility problem. Inspect supported server/proxy settings and advisories; do not implement a second custom HTTP parser or trust client-supplied forwarding headers. Bind trusted proxy configuration to the real network topology.

## Files and outbound requests

Uploads require authentication/authorization, permitted types verified beyond a client MIME label, bounded sizes/counts/decompression, safe server-generated names and controlled storage/retrieval. Prevent traversal and unintended overwrite. Check canonical paths and symlinks at the actual filesystem boundary. Keep active uploaded content away from privileged application origins/execution paths; use safe download headers and processing/scanning appropriate to risk. A malicious file can exhaust resources before storage, during transformation, or at download.

For outbound fetches, distinguish known destinations from a legitimate arbitrary-URL product. Reuse a maintained URL parser and restrict schemes, ports, credentials and destinations appropriately. Account for redirects, DNS changes/rebinding, IPv4/IPv6, loopback/private/link-local and cloud metadata endpoints at resolution/connection time, not just a hostname regex. Supported egress controls can strengthen application checks. Preserve allowed webhook or remote-image workflows while protecting internal networks. Bound response sizes, time and decompression; treat external responses as untrusted input.

## Webhooks, realtime, and agent tools

Verify webhook signatures over the provider-specified bytes and metadata before trusting the event. Validate signed freshness/replay conditions where the protocol provides them; use a durable event/business deduplication strategy for repeated legitimate deliveries. Key rotation and retries must remain usable. A valid signature does not authorize arbitrary resource IDs or prove a payment/workflow is complete; verify relevant business state and account binding.

Authorize WebSocket/SSE establishment and subscribed resources, not just the initial login screen. Review origin/session validation, message limits and revocation behavior. Client-selected channels are not permission grants.

For AI/MCP integrations, retrieved documents, tool results and prompt text are untrusted data. They cannot grant privileges or choose tenant scope. Enforce principal/resource/action authorization outside model reasoning, constrain tool credentials and outputs, and independently validate high-impact actions using existing approval/product rules. Bound tool loops, output sizes and cost. Do not treat prompt wording as a substitute for application access control or add an unrelated agent framework.
