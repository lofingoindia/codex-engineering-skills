# Data ownership, duplicate work, and cache correctness

Use when fetching is slow/redundant, content is stale, or a cache policy is changing. Inspect the installed Next.js/React versions, flags, HTTP client, query library, and deployment before choosing an API.

## Diagnose the operation, not just the browser row count

Follow one reproducible flow from initial load through navigation/mutation. Correlate URL/method, initiator, request identity, browser timing, server trace, and actual backend execution. RSC/prefetch traffic is not the same as a duplicate business write. A component render, Effect setup, HTTP request, and database operation are separate events.

Investigate the evidence for:

- Expected Link prefetches and router-cache reuse; automatic prefetch differs in production.
- Development Strict Mode setup/cleanup, HMR, or development fetch caching.
- Multiple component owners, unstable dependencies/keys, remounts or restored visibility.
- A server read followed by an immediate redundant hydration/client refetch.
- Query retry, focus/reconnect refetch, broad invalidation, or repeated `router.refresh`.

Fix the identified owner/lifetime first. Do not disable Strict Mode or hide duplication behind a global cache. Count relevant backend activity too; fewer browser rows can still cause more server work.

## Keep the mechanisms distinct

| Mechanism | Scope and consequence |
| --- | --- |
| Matching `fetch` memoization in the React server render tree | Can share matching reads during rendering; do not assume it covers arbitrary clients, POSTs, Actions, or Route Handlers |
| React `cache(fn)` | Request/render-scoped sharing for supported RSC use, including errors; reuse one exported wrapper and matching arguments. Recreating wrappers or object identities can defeat sharing |
| Next persistent data/output caching | Reuses across requests according to the active model, key, lifetime, invalidation and host; a separate correctness decision from request memoization |
| Client router/prefetch cache | Retains route payload/UI on navigation; refreshing it does not invalidate every server cache |
| Client query cache | Owned by the installed library/provider; keys, hydration timestamps, retries, stale time and invalidation govern its requests |
| HTTP browser/CDN cache | Governed by headers, variants and cache keys; framework invalidation does not automatically purge every external CDN |

React `cache` is not a process-global memoizer. It does not deduplicate arbitrary Route Handler or Server Action calls outside a React render. Cache Components scopes can isolate React memoization; do not use a memoized session read as a bridge into a shared cache scope.

## Select the architecture already supported

Server Components should normally access an authorized data source/backend directly, rather than HTTP-calling the application's own Route Handler. The latter adds a hop and can fail during prerendering when no server is listening. A browser-facing BFF remains useful for a real credential, aggregation, or trust-boundary requirement.

Keep existing client fetching when interaction, subscriptions, or client-only inputs justify it. Hydrate existing query infrastructure deliberately so it does not immediately repeat a server fetch without a freshness reason. Partition keys by tenant/user/permission scope, filters, pagination, and other response-varying inputs. Never share a request-bound client or query cache globally across server users.

Parallelize independent bounded reads, not every dependency blindly. Preserve cancellation/stale-result protection for rapid filters/navigation and clean up subscriptions. Prefer existing supported event updates where they satisfy freshness; polling, another state library, or Server Actions for routine reads are not default fixes.

## Current Cache Components versus earlier models

Check `cacheComponents` and related flags first. Under Cache Components, use `"use cache"`, explicit suitable `cacheLife`, and tags only for data whose reuse is correct; runtime-sensitive uncached work belongs behind the appropriate streaming boundary. Standard shared cached scopes cannot read request APIs through a helper either. Resolve request context outside and pass approved key inputs, with authorization performed on the live path.

Without Cache Components, follow that version's `fetch` options, route configuration, ISR, and non-fetch caching facilities. Fetch defaults changed across releases; uncached fetch and a fully dynamic route are not universally equivalent. Do not enable the new model, `force-dynamic`, or `no-store` across the app to fix one route.

For any shared private cache, define whose visibility the result represents, keys, lifetime, revocation, and invalidation. Tenant ID alone can be insufficient when users within a tenant have different access. Tags label entries for invalidation; they do not partition the cache key or authorize access. Keep authorization current even when a data result is reused. Prefer uncached sensitive reads when an isolation/freshness guarantee cannot be established. Directive names such as `private` are not substitutes for checking their version-specific scope.

## Mutation-to-read consistency

After a successful durable mutation, update the actual owners that serve the affected UI. Avoid stacking a query invalidation, refresh, and full reload when one targeted path suffices.

- `updateTag` is for immediate expiry/read-your-own-writes from Server Actions in supported versions; it is not available in Route Handlers.
- `revalidateTag(tag, 'max')` permits stale-while-revalidate. For a strict freshness requirement, choose the supported expiry semantics rather than relabeling stale data as updated. Single-argument legacy behavior is deprecated in current docs.
- `revalidatePath` targets page/layout paths. Invocation context affects when refresh happens; a webhook Route Handler marking a path does not instantly redraw every open browser.
- `router.refresh()` requests/merges a new RSC payload while preserving unaffected client state, but does not invalidate persistent server data caches or the query library's independent cache.

Server mutation success and refresh failure are different outcomes: never repeat the write merely because the subsequent read failed. Coordinate browser/query caches, backend cache, and CDN only when they actually participate. For multi-instance hosting, inspect invalidation propagation rather than assuming process-local entries are shared.

Verify freshness and isolation after navigation, mutation, and identity changes. A request-count improvement fails if it shows another user's data or hides a committed update.
