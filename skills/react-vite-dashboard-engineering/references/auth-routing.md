# Authentication, routing, and browser security

Client permission checks guide navigation and interaction. They cannot protect an API from a direct caller. Verify the backend boundary when the task requires it; report any unverified server enforcement rather than claiming the UI secured the system ([OWASP API Security](https://api-security.owasp.org/)).

## Session initialization and routes

Model session state explicitly: unknown/loading, authenticated with context, unauthenticated, and initialization failure are different. A failed session request during an outage is not necessarily a logged-out user. Share/deduplicate bootstrap at the existing owner instead of checking the session independently in every page/widget. Gate sensitive reads/rendering until the identity/tenant context is resolved; avoid protected-content flashes and login redirects while the session is merely unknown.

Use the installed router's supported mechanism and preserve its mode/version. Layout guards do not necessarily sequence parallel loaders; a protected loader/query must depend on the trusted context itself. Distinguish an unauthenticated response from a forbidden operation, and avoid redirect loops involving login/callback/public routes. Client role flags can be stale or modified. The backend must check object, function, field, and tenant permissions regardless of which controls are shown.

Preserve valid deep links through login with a validated return destination. Parse/resolve the destination and constrain origin and allowed app paths; do not trust `returnTo`, scheme-relative URLs, or an arbitrary query parameter passed to navigation. Keep credentials and sensitive data out of URLs. Use replacement navigation appropriately to avoid bouncing back through an auth callback, while preserving ordinary back/forward behavior. Verify direct refresh on a nested route under the actual deployment fallback/base path.

## Reuse the appropriate authentication model

For a suitable same-origin cookie session, reuse server-set Secure/HttpOnly cookies, appropriate SameSite behavior, credentials configuration, and CSRF protection on mutations. JavaScript cannot reliably inspect HttpOnly cookies; use the supported session endpoint/state. HttpOnly prevents direct cookie reading, not all actions by injected scripts. CORS is a browser-origin policy, not authorization or a general replacement for CSRF protection. Do not choose SameSite=Strict without checking legitimate login/navigation/embed flows ([OWASP sessions](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)). Session fixation prevention and server revocation require server lifecycle support; a React route cannot implement them alone.

When OAuth/OIDC is required, use the established provider SDK and current [OAuth Security BCP 9700](https://datatracker.ietf.org/doc/html/rfc9700) plus [browser-app BCP 10017](https://www.rfc-editor.org/rfc/rfc10017.html). Authorization code with PKCE, validated redirects/transaction binding, and correct access-token use matter. A browser cannot keep a client secret; an OIDC ID token is not a general API access token. Compare existing cookie/BFF, token-mediating backend, and browser-only models by threats and deployment constraints. A BFF can keep OAuth tokens out of browser code but does not eliminate XSS or CSRF and need not replace an already sound session architecture.

Do not add localStorage/sessionStorage/IndexedDB persistence for session identifiers or long-lived credentials for convenience; all script-accessible storage is exposed to same-origin XSS. In-memory tokens reduce persistence, not the power of hostile running scripts. Investigate an existing risky token architecture with a concrete migration that preserves login/refresh behavior, rather than a storage-only swap that breaks authentication ([OWASP HTML5 storage](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)).

## Expiration, switching, logout, and multiple tabs

Centralize refresh if the model supports it. Coalesce simultaneous expirations within the relevant owner, bound refresh/replay attempts, and exclude login/refresh/logout endpoints from recursive retry interceptors. Coordinate cross-tab rotation through supported provider behavior where applicable. Refresh success does not justify blindly replaying an unsafe mutation; use the API's actual repeated-effect guarantees.

On logout, revocation, account switch, or tenant change: stop issuing old private work, close scoped subscriptions, clear/isolate sensitive cache and UI state, and prevent old async callbacks from updating the new context. Account-scoped keys and context checks are both useful; a late refresh must not silently restore a logged-out identity. Cover persisted caches, browser/server caching, and form drafts where the app uses them. Do not keep previous tenant data visible merely to smooth a transition.

Invalidate the server session where required and distinguish local cleanup from remote logout success. A network failure during logout does not prove the remote session/token is revoked. Keep the UI private, explain the incomplete remote step where relevant, and provide a bounded recovery path.

Use existing same-origin tab signaling when needed to propagate logout/session changes. Broadcast an invalidation signal rather than credentials or trusted new permission claims; recheck the authoritative session. [BroadcastChannel](https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API) availability/partitioning and lifetime need consideration, and listeners/channels need cleanup. Avoid building a new cross-tab state framework for a single signal.

## Browser trust and private data

React escapes ordinary text, but unsafe HTML/Markdown rendering, DOM sinks, URL schemes, embedded content, and third-party code need their own controls. Render text normally; sanitize intentionally supported rich HTML with an appropriate maintained tool and safe URL policy. CSP/Trusted Types where supported are additional defenses, not substitutes for safe rendering ([OWASP DOM XSS](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)). Never display upstream error HTML or stack traces as trusted markup.

Everything shipped to the client is public configuration/code. [Vite-prefixed environment variables](https://vite.dev/guide/env-and-mode) are bundled; custom define/env-prefix settings can expose more. Keep private API keys and signing secrets on the server. Audit logs/monitoring/source-map handling for tokens, sensitive URL parameters, form contents and tenant data. Service-worker/browser caches must not serve one identity's private response to another. Changing frontend storage does not repair an incorrectly public server/CDN cache.
