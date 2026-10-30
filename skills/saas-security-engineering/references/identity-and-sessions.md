# Identity, sessions, and credential lifecycle

## Reuse the actual identity model

Inspect browser, native mobile and service clients separately. Determine the identity provider, session store or token verifier, trusted issuer/audience, proxy/TLS configuration, recovery flow and credential ownership. OAuth delegates authorization; OpenID Connect adds identity semantics. An ID token is not a general API access token.

For OAuth, use supported authorization-code and PKCE flows appropriate to the client, exact registered redirect handling and the provider's transaction binding/state/nonce protections. Native apps are public clients; an embedded client secret is not confidential. Prefer the external user agent and verified callbacks for native flows. Do not migrate a sound provider or introduce a BFF merely as generic hardening.

Validate tokens using the adopted profile: signature, permitted algorithms and key source, issuer, audience, lifetime and required claims. Decoding a JWT is not verification. Do not let attacker-controlled key URLs or algorithm choices define trust. Handle legitimate signing-key rotation and bounded clock skew without accepting arbitrary stale tokens. Restrict access-token scopes and intended resource servers.

## Sessions and storage

For browser sessions, use appropriate `Secure`, `HttpOnly`, cookie host/domain/path scope and an explicit SameSite policy. Choose SameSite for actual login and cross-site workflows; Strict everywhere can break legitimate flows. HttpOnly reduces token reading through script but does not prevent injected script from making authenticated requests. Cookie paths and CORS do not enforce authorization.

Cookie-authenticated state changes need an appropriate CSRF strategy using supported framework protections, validated tokens and/or suitable origin/Fetch Metadata controls with understood fallbacks. SameSite is defense in depth, not a universal replacement. Never make state-changing GETs a shortcut.

Do not store persistent bearer credentials in script-readable browser storage merely for convenience. Assess existing token architecture and XSS exposure before changing it; memory-only storage also has tradeoffs. Native clients should use supported platform-backed storage and consider backups, logs, screenshots and device compromise. App obfuscation cannot protect a privileged embedded server secret.

Rotate session identifiers after authentication or privilege-sensitive transitions; invalidate prior state as required. Define idle/absolute expiry, logout and revocation, not merely client redirects. Clear identity-scoped caches and reject late responses that could restore an old account after logout/switching. Unavailable session verification is not the same as a proven invalid session.

## Refresh, recovery, and account takeover

Follow RFC 9700's applicable refresh-token protections. Public clients need replay detection through rotation or sender constraints where refresh tokens are issued. Coordinate concurrent refreshes so legitimate tabs/requests do not race a single-use token; provider-specific replay handling and revocation remain authoritative. Do not indiscriminately retry a rejected refresh or revive credentials after logout.

Use maintained salted password hashing with a cost appropriate to the deployed system. Select password/passkey/MFA policy from actual assurance requirements; prefer phishing-resistant options for high-impact access. Do not add arbitrary composition rules or routine forced password changes unsupported by the adopted policy. Support password managers and usable recovery without weakening identity verification.

Recovery, invitation, email-change and MFA-reset tokens need unpredictable values, purpose/account binding, limited lifetime and safe single-use handling. Protect sensitive changes with appropriate reauthentication and user notification. Avoid enumeration through responses, timing, logs or recovery status while preserving actionable legitimate feedback.

Combine abuse controls across identity, network/device signals and expensive workflow costs. An attacker should not be able to lock out a victim indefinitely through a naïve per-account threshold. Rate limits alone do not address stolen sessions, workflow bypass or recovery abuse. Test the normal path alongside expired, replayed, concurrent and revoked credentials.
