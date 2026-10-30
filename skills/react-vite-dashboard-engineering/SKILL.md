---
name: react-vite-dashboard-engineering
description: Build, review, or repair React + Vite dashboards, including loading UX, API fetching, authentication, routing, accessibility, and performance. Use for dashboard or admin application engineering; skip unrelated React widgets, backend API design, and trivial copy or style edits.
---

# React + Vite Dashboard Engineering

Deliver a coherent user journey whose visual, network, permission, and state behavior agree. Match the rigor to the requested change and its consequences. Explicit user instructions and repository requirements take precedence over the defaults here.

## Establish the actual change

Distinguish new dashboard/feature work from a targeted repair, review, or performance investigation. Inspect the affected page and its journey through routes, session initialization, requests, cache/state, mutations, and rendered feedback. Check relevant project instructions, package/lockfile versions, scripts, existing components/styles, API contracts, and tests. Read what the change needs; do not map the entire application for a small bug.

Confirm React + Vite and the installed router mode, data layer, UI primitives, and authentication model before using their APIs. Preserve working JavaScript or TypeScript conventions. Reuse sound clients, query providers, components, validation, and test tools. A new state library, fetching wrapper, design system, router mode, abstraction, or framework migration needs a concrete benefit and a proportionate integration cost.

Explain a nontrivial change in terms of the root cause, the user-visible result, and the smallest approach that preserves correctness. Infer requirements from project evidence; ask only for missing facts that change security, compatibility, or the intended workflow. Keep unrelated useful work moving while answers are pending.

## Read detail when relevant

| Current problem | Reference |
| --- | --- |
| Loading, empty/error states, forms/tables/charts, visual consistency, keyboard/focus | [Experience and accessibility](references/experience.md) |
| Request ownership, duplicate fetching, cache freshness/isolation, races, mutations, real-time data | [Data and state](references/data.md) |
| Session bootstrap, login/logout, protected routes, permissions, tenant changes, browser security | [Authentication and routing](references/auth-routing.md) |
| Components/Effects, render or bundle performance, deployment, normal testing and monitoring | [Architecture and production quality](references/architecture.md) |
| Standard status, current versions, or a contested recommendation | [Authoritative sources](references/sources.md) |

Start with the directly relevant reference; load others when the task crosses their boundary. Verify unfamiliar/version-sensitive APIs and significant security or architectural decisions against installed versions and official docs. These references are a dated synthesis, not permanent version pins. Disclose unavailable research or project evidence rather than asserting it was verified.

## Preserve the important boundaries

- Frontend routes and hidden controls improve UX; the backend must independently authorize data and operations. Never present a frontend-only fix as complete backend enforcement.
- A user's identity/tenant context governs requests, caches, subscriptions, and async completions. Logout or switching context must not allow previous work to repopulate sensitive state.
- Give server data one intentional owner. Avoid duplicate fetching systems, redundant invalidation/refetch paths, and automatic polling. Reuse supported event updates when real-time freshness is needed; add neither polling nor sockets for data that needs neither.
- Keep the shell and unaffected content stable. Represent initial loading, refreshing, genuine empty results, denied access, failures, and uncertain mutation outcomes accurately. Retain previous data only when it belongs to the current security context and is not misleading.
- A cancelled request or interrupted UI does not prove a server mutation stopped. Prevent accidental resubmission and reconcile uncertain outcomes using the existing API contract.

Own browser-side behavior and API consumption. When a task also changes backend contract, authorization, or distributed reliability, coordinate that work explicitly; use `api-design-engineering` if available and relevant. This skill has no dependency on it.

## Complete and verify the journey

Implement the focused change through affected UI, data, routes, and tests. For reviews, give actionable findings with file/behavior evidence, impact, and a practical correction. For new dashboard work, establish a consistent shell, hierarchy, and reusable interaction states without turning every component into a generic framework.

Use normal project checks appropriate to the change: relevant unit/component tests, type/lint checks, and production build. For changed interactions, inspect the running app when available, including a relevant narrow viewport and keyboard path. Exercise the actual failure risk, such as out-of-order search, background refresh, a failed save, or logout during a request. Assert visible outcomes and important request counts/state boundaries; do not build a benchmark suite for an ordinary fix.

After meaningful checks pass, finish the authorized work. Report changes/findings, what actually ran, compatibility and deployment implications, and genuine limitations. Keep proposed checks separate from executed evidence; a successful build does not demonstrate browser behavior or backend security.
