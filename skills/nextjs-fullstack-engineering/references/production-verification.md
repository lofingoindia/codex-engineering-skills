# Deployment, diagnosis, and proportional verification

Use for production failures, hosting decisions, cache/deployment coordination, or choosing checks for an application change. Keep the existing provider and tools unless a requirement justifies replacing them.

## Verify capabilities before choosing a deployment

Inspect the actual output mode, adapter, runtime, package scripts, proxy/CDN, filesystem, and resource/request limits. Do not assume Vercel, serverless, Edge, or an indefinitely running Node.js process. Current Cache Components requires the supported Node.js model; inspect compatibility instead of adding an Edge route config from an older tutorial.

Static export cannot supply a request-time server for session-bound rendering, Server Actions, dynamic request APIs, or runtime ISR. Static supported outputs still work; choose from actual feature requirements, including external backend support and image optimization. A deployment mode that builds successfully can still omit required runtime behavior.

Build-time and runtime values differ. `NEXT_PUBLIC_*` values are public and normally inlined during build; changing a container's environment later does not rewrite the browser bundle. Preserve the project's supported runtime configuration path and build reproducibility. Ensure secrets are absent from public artifacts and diagnostics.

Streaming must work through the complete proxy/load-balancer path. Buffering or time limits can remove the benefit or terminate a long response. Validate the deployed path when making streaming claims; a local development stream is insufficient evidence.

## Multi-instance and rolling deployment correctness

For multiple instances, identify cache storage and invalidation coordination, consistent build/artifact identity, assets, and Server Action compatibility. A process-local cache or tag update is not automatically fleet-wide. Use established platform facilities or a justified maintained cache handler; do not create a distributed cache for every app.

Legacy persistent-cache handlers and Cache Components `cacheHandlers` are different interfaces. Check which one owns the affected entries. A custom store must preserve supported serialization, bounds/TTL, errors, and tag semantics, not simply JSON-stringify arbitrary internal cache objects.

An external CDN adds independent variant keys, TTLs, and purging. Preserve required RSC/HTML and prefetch distinctions for the installed routing model; do not strip `_rsc`, relevant headers, or query variation blindly. Never force public cache headers on identity-dependent responses. Framework revalidation alone may leave an external cached copy stale.

Rolling deploys can mix old client assets, RSC payloads, and Server Action references with a new server. Follow the deployment's skew/asset-retention and action-key guidance. Consistent encryption keys where needed are not a substitute for compatible builds and authorization. Test an affected old-tab/navigation scenario when changing deployment behavior; do not introduce a forced reload on every routine navigation.

For work after a response, verify the runtime's supported lifecycle. An `after` callback is not a durable job queue or guaranteed recovery after a crash. Use the existing durable worker boundary for required business effects. Reuse Next.js/server lifecycle facilities; low-level runtime, database, and broker details belong to their actual owners.

## Production diagnosis

Scope an incident by route, identity class, deployment version, time window, and hard versus soft navigation. Correlate browser network/console, server errors, backend activity, traces, and cache behavior. Observe before labeling an issue a rendering bug, authorization failure, or stale cache.

Reuse existing instrumentation/logging. Where appropriate, `instrumentation` initializes instance-level integrations and must respect runtime-specific imports. Separate server, client, and dependency failures; retain safe correlation and redact tokens/private data. Avoid raw URL/user identifiers as unbounded metric labels and duplicate telemetry providers.

Consult current Next.js/React/transitive advisories and supported release policy for exposure/upgrades. Do not declare the newest major mandatory for a small unrelated change; do not dismiss a relevant patched security issue as style. Run the actual lint/type scripts: build and lint responsibilities change across framework versions.

## Pick checks from the changed user flow

Use existing tests and tools. Pure data/validation logic can have unit tests; interactive components suit user-visible component tests; async RSC, server/client integration, cache/navigation, and auth transitions often need browser/integration evidence. Check the installed test tool's support instead of treating a mocked Server Component as proof of real RSC behavior.

Choose a small meaningful failure/sequence for the task: hard reload plus back/forward after changing routing; rapid filters with an out-of-order response; logout then return to a preserved page; mutation committed but refresh failed; or public metadata/cache after a content update. Do not turn these examples into a mandatory universal suite.

For request optimizations, compare browser initiators and relevant backend executions, including data freshness. For public delivery, inspect actual HTML/metadata and critical assets. For interactions, check keyboard/focus and a relevant mobile layout. Use isolated state, deterministic network controls, semantic locators, and assertions on settled outcomes instead of arbitrary sleeps. Avoid shared real credentials and destructive production tests.

Use a compatible installed `next-dev-loop` for framework/browser cross-checks when its prerequisites are satisfied. Otherwise use available project diagnostics and browser tools without claiming that official workflow ran. Production-mode checks matter for prefetch, static output, hydration and caches; they are not required for every text edit. Run a build/start or focused test only when it adds relevant confidence.

Report the commands and observations actually obtained. Distinguish static inspection, mocked behavior, development runtime, production build, and deployed evidence. Normal skill-package validation does not establish automatic activation quality or better agent decisions; do not claim evaluations, browser results, or performance measurements that were not executed.
