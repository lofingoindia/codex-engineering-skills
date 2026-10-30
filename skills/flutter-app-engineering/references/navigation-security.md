# Navigation, sessions, and client security

Use for routing/deep links, auth restoration, account/tenant switching, sensitive local state or another client trust boundary. Preserve a sound router and authentication system.

## Choose the existing navigation model deliberately

Simple Navigator flows and declarative routers serve different requirements. Reuse the current stack; do not install go_router or convert every route to fix one pop/redirect. For new advanced deep-link/nested navigation, consult current Router/package guidance. Named-route limitations can justify an intentional migration, not an unrelated rewrite.

Trace root/nested navigator identity, page keys, tab branches, route observers, and state/provider scope. Recreating the app router during ordinary rebuilds can reset the stack. Preserve form drafts, tab and scroll state where users expect it; reset state when account/resource identity actually changes. Retention, in-memory restoration and recovery after process death are different guarantees.

Handle Android back/predictive-back and iOS gestures through supported router/widget APIs. Dirty-form protection should guard meaningful unsaved work without trapping navigation. After awaiting, ensure context, route, resource and session still match before popping/pushing or showing a modal. Prevent duplicate taps/listeners from pushing duplicate routes.

## Auth initialization and identity transitions

Represent session restoration explicitly before deciding private/public navigation. Avoid private-content flashes, redirect loops and repeated session initialization. Preserve a validated intended destination through login and discard it when invalid/unauthorized. Do not conflate an unreachable auth service with a successfully unauthenticated session without an intentional recovery policy.

Routing and hidden widgets do not authorize data. The backend independently enforces user, tenant, object and operation permission; client permission UI improves usability. Server responses remain authoritative even if local permissions looked valid.

On logout, revocation or account/tenant switch, cancel/reject old-identity work and clear/recreate affected providers, caches, database views, drafts, sockets, push registrations and back-stack state as appropriate. Use identity-scoped keys and live authorization, not one global mutable tenant field. A late refresh/result must not restore the old account or show private content to the next user.

Choose secure token/session handling within the existing model. Coordinate refresh through one owner and handle expiration without infinite replay. Native OAuth should use a suitable maintained flow with an external user-agent and PKCE according to current standards/provider guidance; validate callback state and redirect binding. Embedded client secrets cannot be kept secret by a mobile binary.

## Deep links and notifications are input

Validate URI scheme, host, path, parameters and intended resource before navigation. Prefer correctly associated App Links/Universal Links for supported flows; verify actual Android/iOS association and app configuration. Flutter built-in and plugin deep-link handlers can conflict, so inspect both before registering another listener.

Handle cold, warm and already-authenticated entry consistently. Queue a validated navigation intent until router/session initialization is ready, consume it once, and recheck resource access. A notification payload or link ID is not proof that the current account may view/act on it. Avoid arbitrary external redirects, token leakage in URLs and duplicate tap processing.

## Protect sensitive local data and boundaries

No server secret belongs in Dart source, assets or compile-time environment values. Obfuscation hides some names, not credentials or business authorization. Keep tokens/private payloads out of logs, crash reports, analytics, clipboard and unnecessary screenshots/app-switcher previews where the threat model requires it.

Use an appropriate maintained platform-backed secure store for sensitive credentials. Android Keystore manages cryptographic keys; iOS Keychain stores small secrets with access policies. Inspect the plugin's actual encryption/accessibility, locked-device, biometric, backup/restore and migration behavior. Secure storage is not a guarantee against every compromised-device or runtime attack, and is not a bulk encrypted database by default.

Keep TLS verification and current dependencies. Certificate pinning, root checks and anti-tamper measures require a threat model, rotation/recovery plan and legitimate-network considerations; do not add brittle restrictions by default. Local biometric success may gate local key access but is not a replacement for backend authorization or session policy.

Minimize permissions/third-party data collection. Evaluate native capabilities, private files, external intents, WebViews and SDK data exposure when they intersect the feature. Apply OWASP MASVS/MASTG criteria relevant to the risk without turning every UI change into a full mobile audit.

For a security/navigation repair, verify the legitimate flow plus an affected denied, expired, wrong-account or malformed-link case. Never weaken authorization/TLS or regenerate credentials/signing keys to make a check pass.
