# Navigation, state preservation, and dependable UX

Use for dashboard shells, route transitions, lost/persisted state, loading/recovery, forms, tables, or interaction polish. Inspect the actual router and Cache Components configuration before assuming what mounts or remains alive.

## Trace identity and lifecycle

Distinguish server execution, browser render/commit, hydration, mount, remount, Effect setup/cleanup, and cache reuse. A rerender is not automatically an API call. A changed key or template can reset state; a retained component can show stale state without making a request.

Shared layouts normally preserve their client state across child transitions. Templates intentionally remount their keyed segment when it changes; higher-level templates do not necessarily remount for deeper navigation, and search parameters alone do not universally remount a template. Keep a stable dashboard shell when only its content changes. Crossing separate root layouts or router families can cause a full document navigation; investigate before replacing links or adding state persistence workarounds.

Current Cache Components navigation can retain page state/DOM using React Activity. Hidden pages may later resume Effects without a fresh state initialization. Do not promise that leaving a page resets forms, dialogs, success messages, subscriptions, or fetched state. Choose what should persist, what should reset on a new resource/submit, and what must disappear on identity changes. Follow installed-version guidance; do not add global stores or use a new router identity API merely because it exists.

Prefer explicit reset at the responsible event or a stable resource-derived key. Do not key the whole shell by pathname or a random value to fix one dialog. Effects/subscriptions need cleanup for unmount and supported hide/show behavior. Restoring a browser history entry and opening a new transaction can require different state semantics.

## Navigation and URL-owned state

Use framework navigation for internal routes where it preserves the intended experience. Keep normal links for genuine external/download/document navigation. Validate programmatic destinations; untrusted navigation URLs can create XSS or open redirects.

Store shareable filters, search, sort, and pagination in the URL when appropriate. Use push versus replace intentionally for browser history, preserve unrelated parameters, validate input, and define scroll behavior. Do not force all local transient UI into the URL. Pages Router shallow routing has its own same-page limitations; App Router navigation is not interchangeable.

Debounce or defer the expensive work only when useful, keep inputs responsive, and cancel/ignore stale results. Transitions schedule UI updates; they do not cancel requests or guarantee the latest mutation wins. Preserve authorization and input correctness during rapid navigation, refresh, and back/forward.

Use prefetch defaults until evidence identifies unnecessary work. Dense link tables may justify scoped hover/disabled behavior, but turning off all prefetch can slow navigation. Partial Prefetching changes shared-shell versus URL-specific work on compatible versions. Route renders must be safe even if prefetched without a visit.

## Loading and recovery are separate states

Place loading/Suspense boundaries at meaningful content units. Retain the shell and useful existing data during local refresh, visibly indicating staleness/pending work where needed. Skeletons should reserve plausible space; use simpler status feedback for short/unpredictable work instead of artificial delays or animation everywhere. Suspense does not detect arbitrary Effect fetching.

| State | Useful behavior |
| --- | --- |
| Initial request/session not resolved | Appropriate pending UI without claiming no data or exposing private content |
| Successful empty collection | Explain what can be created or what happens next |
| Active filters match nothing | Preserve filters and offer a relevant reset/change |
| Forbidden or expired session | Safe access/session recovery, without repeated automatic failures or resource leakage |
| Network/backend failure | Preserve recoverable input/data and offer a bounded safe retry |
| Missing/deleted resource | Resource-specific not-found behavior and a useful navigation path |
| Partial read or background refresh failure | Keep valid sections and identify the affected region |
| Mutation failure or uncertain outcome | Show the actual failure/pending status; do not turn a read retry into a duplicate write |

Use route/component boundaries to isolate unexpected render failures. Event-handler and arbitrary async failures need their own handling; an error boundary does not catch everything. Boundaries do not make upstream headers/status changeable after streaming starts. Retrying must be meaningful and safe rather than an infinite loop.

## Usability and visual consistency

Reuse the design system, including shadcn/Radix if already suitable; do not impose a replacement. Keep hierarchy, typography, spacing, density, and responsive navigation coherent across public and private surfaces. Reserve space for media and asynchronous content. Charts need understandable labels/units and accessible summaries; large tables need usable overflow, sorting, filters, and pagination before virtualization is considered.

Use semantic controls, associated field errors/labels, visible focus, meaningful page titles/headings, and keyboard navigation. Dialogs need appropriate focus entry/containment/return, Escape behavior, and accessible names. Announce asynchronous status without stealing focus or making every refresh intrusive. Respect reduced motion, contrast, zoom, and small screens.

Verify the changed interaction with a relevant failure or rapid sequence, not only a single successful click. Avoid confirmations for harmless reversible actions; protect consequential destructive actions in proportion to their impact.
