# Diagnostics, proportional tests, and release reliability

Use for choosing evidence, debugging production failures, plugin/build changes or preparing an authorized release. Reuse project tests, CI, diagnostics and release infrastructure.

## Diagnose across boundaries

Reproduce a bounded journey and identify app version/flavor, OS/device, account class, lifecycle state and network conditions. Correlate UI/state transitions, requests/backend activity, logs and platform errors. Separate rendering/state bugs, backend failures, malformed data, native-plugin exceptions, memory pressure and notification/lifecycle issues before restructuring unrelated screens.

Reuse FlutterError.onError, PlatformDispatcher error handling and existing crash reporting according to their actual coverage. Awaited errors, framework callbacks, unhandled async errors, other isolates and native crashes are different paths. Do not assume one zone/error hook catches them all or double-report errors through competing handlers. Preserve useful stacks and redact tokens, payloads, identifiers and screenshots according to privacy policy. `debugPrint` is not a guarantee that sensitive logs disappear in release builds.

Hot reload retains state and does not replay every initialization path. Verify a restart/cold start when changing bootstrap or ownership. Production tree shaking, native setup and permissions can differ from debug. A fix visible after hot reload is not proof that a fresh installation works.

## Choose the smallest meaningful checks

| Changed boundary | Appropriate evidence |
| --- | --- |
| Dart logic/serialization/controller | Focused unit tests, static analysis and existing lint/format conventions |
| Widget/interaction state | Widget tests with controlled dependencies and assertions on pending, data, failure and actions |
| Layout/design | Relevant dimensions, keyboard/text scaling, semantics, and golden checks when useful |
| Request/lifecycle ownership | Request counts plus keyed/stale-result, cancellation and cleanup assertions |
| Router/auth/offline/native integration | Relevant integration/device flow, isolated storage/accounts and controlled failure |
| Frame/memory claim | Representative profile/release-mode device evidence with comparable conditions |
| Native dependencies/release config | Actual supported build and targeted install/start check where infrastructure permits |

Use existing compatible upstream testing/analysis skills when they fit; do not create another harness or migrate test libraries to repair one feature. Use Dart/Flutter MCP diagnostics/symbol/runtime tools when connected, discovering actual capability names and prerequisites. Fall back to SDK/DevTools/project tools without claiming MCP/device observations that were unavailable.

Mocked plugins and widget tests do not prove native permissions, push delivery, process restoration, secure-storage backup, screen-reader interaction or OS background behavior. Use real/emulated platform checks for the affected guarantee. iOS builds require the appropriate macOS/Xcode environment; Windows analysis cannot establish iOS release success.

Avoid arbitrary sleeps. Advance controlled time/network responses and assert the intended state. `pumpAndSettle` can time out on infinite loading/shimmer animations; use bounded deliberate pumps/conditions instead of waiting minutes or removing necessary UI. Do not mutate unrelated production state or use real secrets for failure testing.

Pick a small sequence from the actual workflow: navigate away before a response; switch account while refresh runs; retry an upload with uncertain completion; restart with pending local work; or open a notification while session initialization is incomplete. Verify resources, durable outcomes and user feedback, not merely that a widget appears once. Do not turn examples into an exhaustive suite for every edit.

## Preserve build and release integrity

Inspect SDK pins/bundled Dart, application lockfile, plugin native versions, Gradle/JDK/Android SDK, Xcode/CocoaPods or other established native dependency path, deployment targets, identifiers and flavors. Keep application dependency resolution reproducible. Review migrations and compatible fixes rather than blanket upgrades or dependency overrides that hide conflicts.

Validate environment/API endpoints, manifests/entitlements, permission text, native capabilities, privacy disclosures and supported devices against the actual release. Bundled configuration is readable by app users; server secrets must stay on the backend. Check data/schema upgrades and old backend/client compatibility when the change crosses release versions.

Reuse Android signing/upload and Apple signing/provisioning arrangements. Do not regenerate keys, change bundle/application identity, enable invasive capabilities or publish a release as routine verification. Protect signing material and retain matching Dart/native symbols for crash diagnosis, especially when obfuscation/split-debug-info is used.

Use existing staged rollout/TestFlight/internal distribution and monitoring when release work is authorized. Mobile rollback is constrained by store/device update behavior; an old binary can remain active. Do not assume instant rollback, downgrade-safe local storage or a server change that only supports the newest app. Keep a concrete recovery/hotfix path proportionate to the change.

Report exact checks, devices/build modes and outcomes. Distinguish code review, mocks, widget tests, emulator/device interaction, profile measurements and store/deployed evidence. Normal validation of this skill does not prove improved agent behavior or production app reliability. Do not add agent evaluations, benchmark campaigns or release builds for documentation-only skill creation.
