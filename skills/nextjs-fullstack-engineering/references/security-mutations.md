# Sessions, authorization, and mutation correctness

Use when private data, account/tenant transitions, Server Actions, Route Handlers, forms, or another trust boundary is involved. Reuse a sound existing auth/backend architecture.

## Protect the data and operation boundary

Treat Route Handlers, Pages API Routes, and reachable Server Actions as externally callable endpoints. Validate untrusted arguments and verify identity, tenant membership, resource ownership, and operation permission at the actual server access/mutation. A Client Component check, hidden link, layout redirect, Proxy, or middleware alone cannot establish this guarantee.

Layouts may remain mounted and skip rechecking on child navigation. Proxy can provide useful early navigation/session checks, but is not a complete authorization system. Match Proxy versus middleware naming/runtime to the installed version; do not rename files or change authentication architecture as an incidental cleanup.

Keep shared checks in existing server-only access helpers or backend policies, returning minimal authorized data. Client-provided IDs, Action-bound arguments, and closed-over values are not proof of authority. Server Action IDs/encryption reduce exposure but do not replace authorization. Do not rely on unused exports being unreachable as a security control.

Separate reusable public shell UI from request-bound private reads. Each sensitive subtree must wait for its required checks; streaming a placeholder is fine, streaming unauthorized data is not. Request memoization can avoid repeated session reads during rendering without making sessions globally cached.

## Session and identity transitions

Restore session state without flashing private content or creating login/redirect loops. Validate return URLs against the application's permitted destinations. Reuse applicable secure/HttpOnly/SameSite cookie or OAuth behavior; do not move credentials into browser storage for convenience. Preserve CSRF defenses for cookie-authenticated operations. CORS and same-origin routing are not authorization.

On logout, account/tenant switch, expiry, or revocation, invalidate/revoke the relevant server state and discard sensitive client/query/router/provider state as needed. Cancel or ignore old-identity in-flight results and recreate correctly scoped clients/providers when necessary. Consider another tab and back/forward navigation if those affect the flow. A retained layout or hidden Activity page must not restore the previous user's private UI. A key/reset is a UI measure; the backend still independently denies access.

Never put secrets in `NEXT_PUBLIC_*`, rendered HTML, RSC-serialized props, Action return values, URLs, or telemetry. Server execution does not make returned props private. Send only fields the browser needs. A `server-only` import guards the module boundary, while minimal DTOs limit data exposure. Experimental taint APIs can supplement these controls when supported; they are not the baseline security design.

## Choose the existing mutation boundary

Use a Server Action when it fits the same-app form/workflow and deployment. Keep existing backend endpoints for shared/mobile/external consumers or established client architecture. Use Route Handlers for a real HTTP boundary, webhook, protocol, or BFF need. Do not replace all APIs with Actions or use Actions as a general parallel-read transport.

For the affected mutation, establish:

1. Server-side validation and authorization, including current tenant/resource scope.
2. The durable effect/transaction and any concurrency or replay guarantee.
3. Pending UI, duplicate-click behavior, and input preservation.
4. Success/error result, targeted invalidation, and the next navigation/read.

Disabling a button improves UX but cannot make a payment, invitation, or job creation idempotent. Preserve stable operation identity where replay is possible; use backend constraints/transactions rather than a component flag for durable correctness. A timeout or interrupted navigation can leave a committed write. Recover its status instead of retrying as a new operation blindly.

Use supported form Actions, `useActionState`, and `useFormStatus` only where the installed React and component structure support them. Validate on the server even with client validation. Show success after the operation succeeds, or clearly mark an optimistic state with a realistic rollback/reconciliation path. Keep recoverable input/errors close to the form, and prevent an old response from overwriting a newer edit.

Expected validation/conflict failures should become the established typed UI result. Unexpected failures need safe diagnostics and an appropriate boundary. Framework `redirect`/`notFound` use control flow; do not swallow them in broad catches. Place redirects after the appropriate mutation/invalidation path, with safe destinations.

## Additional boundaries when relevant

- Inspect built-in Action origin checks and trusted proxy headers; extend allowed origins narrowly when required. This does not supply CSRF protection for every custom HTTP endpoint.
- Verify webhook signatures against the required raw payload, reject replay where applicable, and keep invalidation callbacks authenticated.
- Bound upload/body sizes, parsing work, downstream deadlines, and expensive operations. Respect deployment limits and durable ownership for work that outlives the request.
- Treat CMS rich text and JSON-LD as untrusted serialization/HTML boundaries. Normal React text escaping does not sanitize `dangerouslySetInnerHTML` or a JSON script payload.
- Fit CSP to the rendering/deployment model: per-request nonces require request-time behavior and can conflict with static delivery. Test legitimate scripts/styles instead of disabling protections globally.

For a security change, verify a denied operation as well as the legitimate workflow using isolated state. Current Next.js/React and relevant transitive security patches matter; consult advisories rather than hard-coding a permanent safe version.
