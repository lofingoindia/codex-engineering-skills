---
name: flutter-app-engineering
description: Build, review, debug, or improve Flutter applications, including Dart implementation, state and widget lifecycles, API efficiency, navigation, secure sessions, smooth UX, native integration, and release reliability. Use for meaningful Flutter app engineering; skip standalone Dart backend/CLI work, unrelated frameworks, and trivial copy edits.
---

# Flutter App Engineering

Improve the requested user workflow and the engineering that supports it. Adapt to the product, supported platforms, existing architecture, and actual failure. Preserve sound conventions; explicit user requirements and repository instructions take precedence over generic recommendations.

## Establish the app and workflow context

Read applicable instructions and trace the affected screen/action through state, data access, backend, persistence, and native integration. Inspect the relevant entrypoint, widget/controller/provider ownership, router, clients, tests, and platform configuration. Determine:

- The task: feature, focused repair, duplicate requests, loading/navigation, security, offline/native lifecycle, review, or measured optimization.
- Flutter/Dart versions and pins, `pubspec.yaml` constraints, lockfile, analyzer rules, generated code and target platforms/flavors.
- Existing state management, dependency scopes, source of server data, storage, auth/session model, and API contracts.
- The affected cold/warm launch, route/tab transition, mutation, background/resume, notification, or restart sequence.
- Data sensitivity, account/tenant scope, freshness, replay/conflict requirements, supported devices, and evidence already available.

Bound investigation to the task. Read installed package APIs, matching Flutter/Dart docs, and relevant OS/plugin requirements before relying on changing behavior. Flutter's bundled Dart version and a standalone Dart installation may differ. Do not upgrade SDKs, change state libraries, add platforms, or restructure the whole app to fix a local problem.

## Load only relevant detail

| Task or decision | Reference |
| --- | --- |
| Dart implementation, widget/element lifecycle, package structure, state/dependency ownership | [Architecture and lifecycle](references/architecture-lifecycle.md) |
| Duplicate requests, client orchestration, mutations, caching, offline persistence/sync | [Data and offline behavior](references/data-offline.md) |
| Routing, auth restoration, deep links, account/tenant transitions, client security | [Navigation and security](references/navigation-security.md) |
| Loading/recovery, forms/lists, adaptive layout, accessibility and localization | [UX and accessibility](references/ux-accessibility.md) |
| Jank, startup, rendering, images, memory, isolates and profiling | [Performance](references/performance.md) |
| Android/iOS lifecycle, permissions, push, real-time and background execution | [Platforms and events](references/platforms-events.md) |
| Diagnostics, focused tests, native/build compatibility and release operations | [Verification and release](references/verification-release.md) |
| Versions, official upstream skills/tooling and authoritative research | [Source and tooling register](references/sources.md) |

Use installed compatible Flutter/Dart/package skills for a genuinely matching specialized workflow, without duplicating their recipes or adopting their examples as universal architecture. Discover actual MCP capabilities when connected; otherwise use existing SDK, DevTools and project tools. Do not install optional plugins, modify agent configuration, or add test-driver hooks automatically.

This skill owns Flutter client behavior and native integration. API/backend/database specialist skills can help at their actual boundaries; none is required. UI permissions are usability measures: the backend must independently authorize sensitive data and operations.

## Make the smallest sound change

State the root problem or required invariant and selected approach before editing. Reuse existing widgets, state owners, HTTP clients, routing, storage, validation and observability. Separate substantial data/business work from rendering without imposing a universal folder tree or layer per simple operation.

For changed async work, identify who starts it, which input/identity it belongs to, how stale results are rejected, and who cancels/disposes resources. A rebuild is not a reason to fetch; mounted is not freshness; a timeout is not cancellation; background execution is not durable delivery.

Represent loading, refresh, empty, filtered-empty, denied, failed and uncertain-mutation states accurately. Preserve useful content and recoverable input. Avoid adding global caches, keep-alives, isolates, polling, shimmer, or a library migration merely to conceal incorrect ownership or state transitions.

## Verify and finish proportionately

Use existing focused checks for the changed behavior: formatting/analyzer, unit/widget tests, integration/device checks, or the relevant build. Choose realistic failure sequences from the actual flow rather than a universal suite. Documentation-only skill work needs normal validation, not an application fixture or agent evaluation campaign.

Claims about reduced requests need network/backend evidence and correct freshness/isolation. Claims about smoothness/performance need relevant interactions and representative profile/release conditions. State clearly when devices, platform toolchains or optional tools were unavailable.

Review the diff for compatibility, resource leaks, stale/private state, duplicate systems and unrelated changes. Report the resulting behavior, checks actually executed, observations, and material limitations; compilation alone does not establish a reliable mobile experience.
