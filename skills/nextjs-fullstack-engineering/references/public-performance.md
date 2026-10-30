# Public delivery, technical SEO, and measured performance

Use for websites, storefronts, content delivery, assets, or actual rendering/bundle bottlenecks. Private dashboards can benefit from asset/performance guidance without becoming indexable public pages.

## Public content and crawlability

Choose prerendering, appropriate ISR/caching, or request-time rendering from content freshness, personalization, scale, and deployment support. Keep meaningful public content available in the intended server output rather than moving it behind unnecessary browser fetching. Separate reusable content from account/cart widgets and sensitive transactions.

For App Router, use static metadata or `generateMetadata` and file conventions where supported. Pages Router uses its own head/document conventions. Check titles/descriptions, canonical URLs, robots policy, sitemap inclusion, OG images, and relevant locale alternatives against the real public URL and environment. Avoid indexing staging, private dashboards, preview content, or duplicate filter permutations unintentionally. Robots/noindex directives do not protect private resources.

Ensure metadata and body represent the same content. Share a suitable request-scoped read when metadata and the page need the same record; do not separately fetch the entire entity twice by default. Streaming metadata and crawler-specific handling vary by version. Inspect actual output and the relevant bot/share-preview behavior rather than assuming every response's head is identical.

Use structured data only when it accurately describes visible content and meets the consumer's requirements. Serialize JSON-LD safely: `JSON.stringify` alone does not stop a string from terminating a script element. Use the approved safe serializer/escaping and validate output. Rich snippets or ranking improvements are not guaranteed by valid markup.

Handle missing content with the framework's supported not-found path. Verify status and robots behavior before and after streaming; once headers are sent, not-found UI can accompany a 200 response. Do not report a universal 404 guarantee or solve crawlability with a cosmetic empty page.

## Images, fonts, and scripts

Use existing asset tooling when suitable. With `next/image`, provide intrinsic dimensions or a correctly constrained fill container, meaningful alt/decorative handling, and accurate responsive `sizes`. Restrict remote patterns to needed sources and understand that the default optimizer does not forward authentication headers. Do not expose private signed resources through an indiscriminate shared image cache.

Choose eager/high-priority/preload behavior for the actual critical image, using supported properties. Do not lazy-load the LCP image or preload the whole gallery. Current versions deprecate older `priority` behavior in favor of clearer controls; check the installed API before editing. Keep SVG/optimizer security controls and patched image dependencies; do not enable dangerous image options to bypass a configuration problem.

Use `next/font` or the established font system with only needed families, weights, and subsets. Apply it at the appropriate layout scope to avoid repeated instances and layout shifts. Account for build-time font retrieval/offline build requirements rather than adding broad network exceptions silently.

Audit third-party scripts by purpose, consent requirements, load timing, main-thread cost, and failure behavior. Choose the supported script strategy for the need. Defer genuinely noncritical code without breaking keyboard flows, critical content, analytics correctness, or CSP.

## Establish the actual bottleneck

| Symptom | Useful evidence before choosing a fix |
| --- | --- |
| Slow first content/LCP | Server/dependency latency, discovery and download of the LCP resource, render-blocking work, hydration/main-thread contention |
| Slow input/INP | Long tasks, expensive handlers, rendering/commit work, large tables/charts, third-party scripts |
| Layout shifts/CLS | Missing dimensions, unstable fallbacks, fonts, inserted alerts/content |
| Slow navigation | Blocking server reads, waterfalls, prefetch/cache behavior, loading boundaries, client refetch and hydration |
| Large initial JS | Client boundary imports, duplicated dependencies, shared providers, expensive libraries, actual analyzer output |

Core Web Vitals are LCP, INP, and CLS; use field distributions when available and lab traces to diagnose. TTFB and route/backend timings remain useful but are not replacements for those metrics. Separate cold/warm/cache-hit scenarios, devices, and network conditions. Do not optimize solely for one Lighthouse score or claim a gain without comparable evidence.

First reduce unnecessary client graph/data, repeated effects, misplaced state, and genuine waterfalls. A rerender alone is not a defect. Use React profiling to identify expensive repeated work before adding `memo`/`useMemo`/`useCallback`. React Compiler availability/configuration matters; it does not fix network ownership or authorization.

Dynamic imports can defer an expensive optional interaction, but indiscriminate lazy loading introduces more waits. Browser-only `ssr: false` has placement/version restrictions and removes server output. Verify supported splitting behavior rather than assuming every dynamic import shrinks initial client work. Use virtualization for evidenced large-list costs while preserving semantics, focus, and navigation.

When a compatible official bundle or static-shell optimizer is available and matches the request, use its workflow rather than implementing a competing analyzer. Otherwise use existing profiling/build tools and state the evidence limit. Preserve content, freshness, and accessible interactions while optimizing.
