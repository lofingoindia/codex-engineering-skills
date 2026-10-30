# Data, requests, and state

Trace one user interaction from URL/input through request ownership, response interpretation, cache identity, and visible result. Count requests and explain their causes before changing architecture. Reuse a suitable existing router/data library or small client; a project using fetch does not automatically need Axios, TanStack Query, Redux, or a new wrapper.

## One intentional owner

Separate server state from local interaction state (open dialog, draft, selection) and shareable navigation state (filters, sort, page). Derive rather than copy values unnecessarily. Use the URL for navigable/shareable state when appropriate, with validation, back/forward behavior, and no credentials or sensitive drafts in it.

Determine whether data belongs to a route loader, an existing query cache, or a component. A router loader and a query library can cooperate by sharing one fetch/cache path; independently fetching in both the loader and component creates duplication. Preserve the installed [router mode](https://reactrouter.com/start/modes): declarative routing does not automatically provide data-router pending/action APIs. For a few local requests, a clear Effect with cleanup may be sufficient; for substantial shared server state, compare the existing data layer's capabilities before adding one ([React Effects](https://react.dev/reference/react/useEffect), [TanStack Query overview](https://tanstack.com/query/latest/docs/framework/react/overview)).

Start independent reads in parallel when their authorization/context is established; do not create a parent-to-child waterfall just because components mount in sequence. Prefetch likely next navigation using existing support when the benefit justifies bytes, cost, and freshness risk. Do not prefetch privileged or expensive data speculatively.

## Request identity and freshness

An identity describes everything that changes the result: resource, verified user/tenant/security context as appropriate, filters, sort, page/cursor, and representation. Do not include raw credentials in keys, logs, or URLs. Enable private queries only after the required context is resolved. A key scopes cached results; it does not authorize the backend request ([query keys](https://tanstack.com/query/latest/docs/framework/react/guides/query-keys)).

If using TanStack Query, inspect the installed version and actual defaults: cached data is normally stale immediately; stale queries may refetch on mount, focus, and reconnect. Freshness (`staleTime`) is separate from inactive retention (`gcTime` in v5). Set policy from how stale the user can safely be, rather than disabling all refetching or setting an arbitrary universal TTL. Investigate provider/client recreation, changing keys, manual Effects, router revalidation, and retry behavior when request counts look excessive ([important defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)). Other libraries have different semantics.

Keep cached data visible on a same-context refresh where useful. Previous-page placeholders can help pagination, but must be labeled accurately and must not cross account/tenant/permission boundaries. A security-context change requires disposal or isolation of old queries, persisted caches, derived stores, subscriptions, and sensitive selections/drafts. Prevent late results from repopulating cleared state: cancel old work where supported and verify context/generation before committing its data, errors, navigation, or mutation callbacks. Clearing a cache alone does not establish this invariant.

## Cancellation, races, and errors

Rapid searches and filter changes can complete out of order. Pass the owner's [AbortSignal](https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation) through the actual HTTP client, clean up on context/unmount changes, and use the library's ordering guarantees or a request/context identity guard. Treat deliberate cancellation as cancellation, rather than showing an error toast. A stale request's `finally` must not clear a newer request's pending state. Debounce only when the interaction benefits; deferred rendering is not network debouncing ([useDeferredValue](https://react.dev/reference/react/useDeferredValue)).

Normalize expected failures through the existing client: network/timeout, HTTP status, API error envelope, parsing/shape failure, and abort differ. `fetch` resolves for 4xx/5xx responses, so inspect status; handle empty/204 responses without blindly parsing JSON, and do not treat a login HTML page as valid API data. Validate critical response assumptions and render safely; do not turn malformed responses into empty success ([MDN fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)).

Use bounded, context-aware read retries for transient failure. Avoid retrying invalid input or denied access, and coordinate query, client, router, and refresh retries. A mutation retry requires safe server semantics and the same operation identity when supported. Aborting a request does not roll back a server effect ([router race conditions](https://reactrouter.com/explanation/race-conditions)). Show an unknown outcome honestly and reconcile before resubmitting a payment, destructive action, or other consequential mutation.

## Mutations and consistency

Guard duplicate submission at the action owner, including keyboard paths. Reconcile confirmed server responses into the appropriate detail/list/summary state or invalidate the affected scoped queries; select one intentional strategy, rather than combining broad invalidation, manual refetch, navigation reload, and polling. Router actions may already revalidate loaders. Await freshness work when the workflow actually promises current data before proceeding, rather than marking every background refresh as a blocking save ([invalidation guidance](https://tanstack.com/query/latest/docs/framework/react/guides/invalidations-from-mutations)).

Optimism fits predictable, reversible changes where failure can be explained and reconciled. Prefer confirmed outcomes for high-impact, authorization-sensitive, or server-computed transitions. For optimistic work, account for in-flight reads overwriting the prediction, pending identity, server IDs, sorting/totals, and rollback. A whole-cache snapshot rollback can erase a newer successful concurrent mutation; serialize per entity, use targeted/version-aware reconciliation, or choose a simpler pessimistic flow. Handle success and failure only in the initiating security context ([optimistic updates](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates)).

## Large and changing datasets

Match server pagination/filtering/sorting to actual API semantics. Do not sort only the current page while claiming a globally sorted dataset. Reset or reconcile page/selection when filters change; define whether bulk selection means this page, explicit IDs, or all matching records. Bound data and rendering separately: virtualization reduces DOM work, not download volume or backend query cost.

Use existing event/subscription support for genuine real-time needs, with tenant/permission-safe scope, cleanup, event identity, reconnection/gap handling, and reconciliation. Prefer neither automatic polling nor a new socket platform for ordinary freshness. If polling is explicitly required or best supported for a bounded operation, justify interval, stop/backoff/visibility behavior, and deduplication. Notifications can invalidate/refetch authoritative data; an event payload need not become a second independent state store.
