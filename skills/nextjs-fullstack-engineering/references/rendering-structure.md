# Rendering, boundaries, and project structure

Use for architecture, rendering, hydration, or organization decisions. First identify the router and installed configuration; classify individual routes rather than declaring the whole application static, dynamic, or client-rendered.

## Choose from the actual user and data needs

| Surface | Reasonable starting decision, subject to project evidence |
| --- | --- |
| Public article, docs, company or product content | Prerender/cache reusable content where freshness permits; retain crawlable content and minimal browser work |
| Storefront with personalized cart/pricing | Separate reusable catalog content from identity-dependent UI; recheck authoritative prices/availability at the business transaction |
| Private operational dashboard | Authenticate and authorize sensitive reads; choose request-time server reads, existing client server-state ownership, or a deliberate combination |
| Hybrid website and SaaS | Share appropriate primitives while keeping public delivery policy separate from session-dependent areas |

Not every public page can be static; not every dashboard must be a client-only SPA. Choose boundaries from interactivity, sensitivity, freshness, cost, and deployment support. Avoid hoisting a session/database await into a public root layout if only a small user menu needs it. Never stream sensitive child content before its own authorization completes.

## App Router execution and server/client boundaries

Server Components execute on the server and contribute an RSC payload. Client Components provide interaction and browser capabilities; they can also be prerendered into initial HTML and then hydrated. `"use client"` identifies a module-graph boundary, not an instruction to skip all server rendering.

Keep the interactive island small enough to avoid shipping unnecessary imports/data, but do not fragment simple UI into excessive wrappers. Pass only needed serializable values. A Server Component can compose server-rendered children into a client wrapper; importing a server-only data module into the client graph is different and unsafe. Use supported `server-only` boundaries for sensitive modules.

Place providers at the scope that needs their state. Do not move an entire page/layout into the client graph just to add one provider, event handler, or browser widget. Conversely, preserve a sound client query architecture for highly interactive data instead of rewriting every interaction as a server render.

Keep rendering pure with respect to business effects. Renders may repeat and prefetches may execute code before a click. Creating records, logout, sending email, and analytics that assume a committed navigation need explicit lifecycle ownership.

## Streaming and hydration

Use a meaningful Suspense boundary around the work that may suspend. Awaiting the slow read in a parent before returning that boundary still blocks the parent. Start independent authorized work in parallel where it avoids a real waterfall; preserve ordering when one result or authorization is a prerequisite.

With Cache Components enabled, static/cached UI can form a shell while uncached runtime work streams. Follow that version's validation/fix guidance. Do not translate every old route-config option into the new model or silence blocking warnings with caching that violates freshness. A Suspense boundary alone does not make synchronous work dynamic or catch a fetch performed in an Effect.

Hydration requires compatible initial server/browser output. Investigate browser-only reads during render, time/random/locale differences, invalid HTML nesting, extensions, and data snapshots before suppressing warnings. Use a narrowly scoped client-only rendering path only for a genuine browser-only dependency; it can delay meaningful content and is not a universal hydration repair.

## Pages Router and incremental compatibility

Keep Pages Router APIs on Pages routes: `getStaticProps`/`getStaticPaths` and ISR for suitable public content, `getServerSideProps` for request-time props, API Routes for HTTP boundaries, and `next/router` for its navigation behavior. Returned props are exposed to the browser, even though fetching runs on the server. Avoid an internal HTTP hop to an API Route when the server function can safely access the source directly.

Do not transplant App Router `loading`, RSC, metadata exports, or cache directives into Pages routes. Hybrid projects can migrate incrementally, but routing/identity and shared provider behavior need deliberate handling. A task on one route does not authorize converting the entire router.

## Organization that earns its complexity

Reuse root or `src` placement, feature boundaries, aliases, tests, and style conventions. Keep route files understandable; colocate feature-specific UI and separate server-only access where it reduces exposure or repeated logic. An existing external API layer can already be the correct data boundary; a new repository/DAL class hierarchy is not required.

Route groups organize URLs/layouts without adding a URL segment; private folders can mark non-routable implementation. Do not create multiple root layouts, parallel/intercepting routes, monorepo packages, or generic shared utilities without a concrete need. Make import/build compatibility part of a focused structural change.
