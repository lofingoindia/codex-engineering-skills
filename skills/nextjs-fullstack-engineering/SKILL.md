---
name: nextjs-fullstack-engineering
description: Build, review, debug, or optimize Next.js public websites and authenticated SaaS applications, including rendering, routing, data fetching, caching, security, UX, and deployment. Use for meaningful Next.js engineering; skip non-Next.js React work, trivial copy edits, and standalone backend or database tasks.
---

# Next.js Full-Stack Engineering

Deliver the requested behavior with correct data ownership, useful UI, and evidence appropriate to its risk. Public content and private workflows can share a project without sharing one rendering or caching policy. Preserve sound architecture and keep changes proportional to the task.

## Establish the project and route context

Read applicable instructions, including managed Next.js guidance in `AGENTS.md`. Locate the actual application directory and inspect the lockfile, resolved Next.js/React versions, package scripts, `next.config.*`, route tree, relevant consumers, authentication, data clients, and tests. Determine:

- The requested outcome: new feature, focused repair, review, migration, incident, or measured optimization.
- App Router, Pages Router, or both; JavaScript/TypeScript; runtime and deployment adapter/provider.
- The affected route's audience: anonymous public content, personalized public experience, authenticated workspace, or a combination.
- Data sensitivity, tenant/resource ownership, freshness and mutation requirements; current cache and state owners.
- The affected initial load, client navigation, background refresh, or mutation path, including relevant production evidence.

Resolve documentation from the app's installed Next.js package. When available, read only relevant files under `node_modules/next/dist/docs/`; honor an existing version-matched `.next-docs` index too. Otherwise consult matching official version documentation. Check current security advisories when the task involves exposure or upgrades. Do not apply canary behavior, current-site defaults, or a new cache model to an older project by assumption.

## Read only the relevant reference

| Task or decision | Reference |
| --- | --- |
| Server/client boundaries, rendering strategy, App/Pages compatibility, project organization | [Rendering and structure](references/rendering-structure.md) |
| Duplicate requests, fetching ownership, cache scope/freshness, invalidation | [Data and caching](references/data-caching.md) |
| Sessions, tenant isolation, Server Actions, Route Handlers, mutation correctness | [Security and mutations](references/security-mutations.md) |
| Layouts, preserved state, remounts, loading/recovery, dashboard interactions | [Navigation and UX](references/navigation-ux.md) |
| Public content, SEO, images/fonts/scripts, bundles, rendering performance | [Public delivery and performance](references/public-performance.md) |
| Deployment constraints, production diagnosis, focused tests and verification | [Production and verification](references/production-verification.md) |
| Current versions, authoritative sources, specialized Vercel skill selection | [Source and compatibility register](references/sources.md) |

Vercel's specialized skills own supported development-loop, cache-adoption, partial-prefetching, and optimization workflows. Use an installed compatible workflow when it fits; read its prerequisites and preserve the user's scope. Do not recreate its recipes, install optional tooling automatically, or require a framework migration for ordinary work. If unavailable, use relevant official docs and existing project tools, stating what could not be verified.

This skill owns Next.js decisions across public sites and dashboards. Existing API, Node.js, PostgreSQL, and UI skills can help with genuinely separate specialist work; none is required. Do not apply Vite configuration or assume a browser-only architecture merely because dashboard components use React.

## Make a focused engineering change

Before editing, state the root failure or required invariant and the simplest suitable approach. Trace the affected data and interaction across browser, Next.js, backend, and cache boundaries. Reuse existing components, clients, auth, validation, state libraries, and conventions. Avoid parallel systems or a universal folder tree.

Place client interactivity where needed; retain server-only secrets and authorization. A layout redirect or hidden button cannot protect an endpoint. Cache scope must preserve user/tenant isolation and revocation requirements. Keep render paths free of business mutations: prefetching and repeated renders must be safe.

For performance work, establish which request, render, or dependency is expensive. Reduce redundant work without losing freshness, input, navigation state, or authorization. Do not disable Strict Mode, blanket-memoize, add unscoped shared caching, or add proxies/infrastructure to conceal a symptom.

## Verify and finish

Run existing focused checks suited to the change. Browser/network evidence is necessary for claims about navigation, request counts, hydration, or interactions; production-mode checks matter when development behavior differs. Select realistic failure cases from the actual flow. Do not impose an exhaustive suite, agent evaluations, or benchmarks on every task.

Review the diff for compatibility, cache/data exposure, broken state transitions, duplicate systems, and unrelated edits. Report changes, checks actually executed, observed outcomes, and genuine limitations. A successful build establishes build compatibility, not correct authorization, browser behavior, or production performance.
