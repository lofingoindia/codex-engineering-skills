# Native lifecycle, permissions, push, and real-time work

Use when behavior crosses Flutter's process/widget lifetime into Android/iOS services, plugins, notifications, platform channels or persistent connections. Inspect target OS versions, capabilities and installed plugin contracts.

## App lifetime is controlled by the platform

Use the existing lifecycle owner with AppLifecycleListener/WidgetsBindingObserver where supported. Flutter lifecycle names are not exact native lifecycle equivalents; states can be synthesized, skipped, or absent on abrupt termination. Persist required state at its business boundary rather than waiting for dispose/paused/detached.

On resume, reconcile stale session/data/subscriptions according to freshness requirements. Debounce/coalesce overlapping resume/navigation refreshes at the appropriate owner. Pause unnecessary sensors, rendering, timers and connections when hidden, but preserve an explicitly required background capability through its supported native mechanism.

An isolate, timer or socket does not grant indefinite background execution. Android persistent scheduled work, foreground/user-visible work and iOS scheduled/continued work or background transfers have distinct eligibility, budgets and platform policy. Select the supported existing plugin/API for the actual operation. Handle expiration/cancellation and persist/checkpoint work so a later run can recover safely.

Do not use generic periodic work as a substitute for continuous courier tracking or claim identical Android/iOS guarantees. Background location, uploads, media and notification extensions each need their specific platform requirements. Do not add native code or a work scheduler when the app only needs a normal foreground request.

## Permissions and plugins

Request only necessary permissions in context, explain the user benefit, and preserve a usable denied/restricted state. Handle temporary, approximate/limited, permanently denied and later revoked permissions as supported by the OS/plugin. Returning from settings or resuming may change capabilities; do not repeatedly prompt or assume one launch-time grant is permanent.

Inspect manifests/Info.plist, entitlements, usage descriptions, background modes and privacy declarations together with plugin versions and native build requirements. A Dart method existing does not prove configuration or OS support. Dispose plugin handles/event streams and interpret PlatformException versus network/business failures appropriately.

## Push and notification navigation

Reuse the existing provider/plugin and establish one owner for registration and listeners. If using FCM, handle foreground receipt, background receipt, terminated launch intent and notification-open events according to current FlutterFire/platform behavior. Background entry points may require top-level registration, initialization and tree-shaking annotations; they cannot freely manipulate a live widget tree. Verify installed requirements instead of pasting old setup code.

Keep background handlers bounded and acknowledge/complete platform work as required. Delivery, timing and execution can be delayed, duplicated, throttled or prevented by OS/user conditions. A push is not a durable command queue or proof that a business operation succeeded.

Manage device-token refresh/staleness and server registration under the current user/device identity. On logout/switch, remove or update the old association and related subscriptions as required; avoid repeated registration on every widget rebuild. Notification permission denial must preserve appropriate non-push behavior.

Treat payloads as untrusted hints. Fetch/authorize the relevant resource and validate a deferred navigation intent after session/router readiness. Deduplicate receipt/tap handling by suitable event identity; an initial message and an open callback must not blindly push the same route twice. Keep private data out of lock-screen payloads unless product/privacy requirements allow it.

## Real-time connection ownership

Reuse supported WebSocket/SSE architecture where it meets freshness needs. Define authentication/expiry, tenant subscription, retry/backoff, heartbeat, bounded outbound/inbound queues and terminal failure. Reconnect must not duplicate listeners or replay a non-idempotent action accidentally.

Sequence/version/cursor or snapshot reconciliation is needed when gaps affect correctness; sockets and push do not create event durability. Refresh from an authoritative source after relevant gaps/resume. Coalesce disposable updates only when the business semantics permit it. Do not automatically introduce polling or new pub/sub infrastructure.

Close/pause connections at the actual owner/session/lifecycle boundary and cancel retry timers when no longer needed. A user navigating away or logging out should not leave an obsolete socket updating private state. Platform suspension/kill and ordinary connection cancellation are different failure paths.

For a native/event change, choose an affected cold/warm intent, permission denial, resume/reconnect, duplicate event or interrupted-work path to verify on supported infrastructure. A desktop widget test cannot prove native notification, background or permission behavior.
