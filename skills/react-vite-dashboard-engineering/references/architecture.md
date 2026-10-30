# Architecture, performance, and production quality

Choose the smallest structure that keeps the requested feature understandable. Reuse existing project boundaries, scripts, language, and design system. Do not introduce a frontend framework inside the application.

## Components and state ownership

Keep feature-specific behavior near its page/components; share stable behavior when there is meaningful reuse. Compose layout, data ownership, and interaction components rather than adding generic controllers, services, and adapters for every screen. An app-wide provider is appropriate for truly shared concerns, not every local field or open menu. Avoid duplicating server data into multiple stores that then need synchronization.

Derive display values from current props/state; handle user actions in their event/action path. Use Effects to synchronize external systems, with correct dependencies and mirrored cleanup for listeners, subscriptions, timers, observers, and requests. Do not suppress the dependency linter or disable Strict Mode to hide a duplicate-request bug. Development setup/cleanup behavior can expose real lifecycle defects ([unnecessary Effects](https://react.dev/learn/you-might-not-need-an-effect), [useEffect](https://react.dev/reference/react/useEffect)).

Preserve identity intentionally: stable entity keys, page layouts, and state placement prevent accidental remounts. Reset state at real entity/security boundaries, not on every refresh. Avoid conditional Hooks and render-time side effects. Keep data transformations pure and handle actual response variants. Error boundaries isolate rendering failures; they do not automatically catch rejected async requests or event-handler failures. Route/library error handling and action/request error state need their own appropriate paths.

[shadcn/ui](https://ui.shadcn.com/docs) distributes component code you own; inspect the installed component and its primitive/version rather than assuming a catalog example exactly matches it. [Radix](https://www.radix-ui.com/primitives/docs/overview/accessibility) handles many interaction mechanics, but composition can still break accessibility. Reuse existing tokens and primitives; a second component kit often creates more inconsistency than it solves. Preserve JavaScript where suitable instead of forcing a TypeScript migration as part of a page repair.

## Measure the bottleneck

Distinguish server/network time, transfer/parse time, render/commit work, layout/paint, and interaction delay. Compare a representative production build on target devices and data sizes. Development Strict Mode behavior or one desktop Lighthouse score is not the whole production experience.

Use browser performance/network tools and the existing React profiling workflow to locate expensive work ([Profiler](https://react.dev/reference/react/Profiler)). Fix avoidable request loops, waterfalls, payload size, expensive derivations, broad state updates, or unstable identities before blanket memoization. Consider React Compiler and library requirements if installed; `useMemo`/`memo` are performance tools, not business-correctness guarantees.

For a table library, respect its required stable data/column references and actual version ([TanStack Table data](https://tanstack.com/table/latest/docs/guide/data)). A small table rarely needs virtualization. A measured large-list bottleneck may justify it, but evaluate row height, keyboard/focus behavior, screen-reader navigation, selection, and scroll restoration. Move genuinely expensive non-render computation off the main thread only when measured benefit justifies worker lifecycle/serialization complexity. Keep typing responsive; transitions/deferred rendering do not make synchronous heavy work or network requests disappear.

Split heavy, infrequently visited routes or visualization/editor code when startup benefits outweigh navigation overhead. Keep lazy declarations stable and loading/error boundaries useful. Avoid a chain of nested lazy/data waterfalls or splitting every small component. Inspect dependency/import impact before adding a large chart, date, icon, or UI package; preserve necessary locale/time-zone support rather than pruning it blindly.

[Core Web Vitals](https://web.dev/articles/vitals) track LCP, INP, and CLS, with field evaluation at the 75th percentile. [INP](https://web.dev/articles/inp) concerns interaction responsiveness, not just React render duration. Combine these with dashboard-specific route-to-useful-data, request counts, slow-table interactions, layout continuity, and memory/subscription behavior. State the workload and measurement method; do not promise improvements from code appearance alone.

## Vite and deployment behavior

Inspect package/lockfile versions, Node engines, plugins, scripts, aliases, and browser targets before changing tooling. New Vite versions can use a different bundler/configuration surface; an old Rollup recipe is not automatically current. Verify type checking separately: Vite transpiles TypeScript but does not itself establish type correctness ([Vite features](https://vite.dev/guide/features)). Reuse the project's existing package manager and checks; do not upgrade the toolchain for an unrelated UI fix.

Test the production artifact, base path, static assets, route refresh/deep links, and API origins. Development proxy behavior does not configure production CORS or authentication. Ensure SPA fallback does not turn failed API requests into HTML success responses. Verify configuration exposure: `VITE_*` and custom client replacements are public, build-time values are not automatically runtime environment values ([environment guide](https://vite.dev/guide/env-and-mode)). `vite preview` is a local preview, not a production server ([deployment guide](https://vite.dev/guide/static-deploy)).

Plan for a tab running an older release whose lazy chunk has been retired. Use deployment asset retention/cache strategy and a bounded update/reload recovery path; preserve or warn about unsaved work and avoid infinite reload loops. Vite's `vite:preloadError` can help detect dynamic-import failure, but it does not prove that every import failure should reload ([production build](https://vite.dev/guide/build)).

## Normal verification and operational evidence

Use existing tests, not a new evaluation platform. Unit-test consequential pure transformations and component-test visible interaction/error behavior with the current tools. [Testing Library](https://testing-library.com/docs/react-testing-library/intro/) encourages behavior-focused checks; [Vitest](https://vitest.dev/guide/) is an option when compatible, not a mandatory dependency. A simulated DOM cannot prove real layout, browser focus behavior, or production routing.

For affected journeys, use available browser tests or manual inspection with realistic local fixtures: a slow refresh should retain useful same-context content; an older search response should not replace a newer one; a failed submit should preserve the draft; logout during a request should not restore private data. Select the checks that expose the change's actual risk. Use deterministic delays/failures and meaningful request-count assertions, not arbitrary sleeps or a blanket requirement that every dev request happen exactly once.

In [Playwright](https://playwright.dev/docs/best-practices) or the existing equivalent, prefer role/label locators, web-first assertions, and isolated test identities. Inspect a relevant narrow viewport, keyboard/focus path, console errors, and production build. Mocked browser API tests establish client behavior, not backend authorization or distributed correctness. Run the affected lint/type/test/build scripts; broaden only when changes, failures, or unresolved concerns warrant it.

Reuse runtime reporting with route/build correlation, useful error categories, request timing, and failed-chunk/session-loop visibility. Redact credentials and sensitive data. Define rollout/recovery evidence for a consequential migration without adding a monitoring service for a minor fix. Report executed checks and any untested browser/server boundary plainly.
