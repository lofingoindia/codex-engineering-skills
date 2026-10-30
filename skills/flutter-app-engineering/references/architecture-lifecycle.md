# Architecture, Dart, and lifecycle ownership

Use for structure, state, repeated initialization, disposed-state errors, or retained resources. Inspect the actual state library/version and scopes before selecting a fix.

## Preserve useful boundaries

Flutter's recommended UI/data separation and MVVM/repositories are adaptable guidance, not a mandatory file hierarchy. Keep features cohesive; separate substantial data/business logic from rendering and give each shared fact one authoritative owner. Preserve sound Bloc, Riverpod, Provider, native Listenable or other existing designs. Do not introduce parallel state systems or a new domain/use-case layer without real reuse/complexity.

Local focus, expansion and temporary form state usually belong near their widgets. Server data, session identity, durable pending work and derived display values have different lifetimes. Avoid copying one server entity into several independently mutable stores. Feature-first, layer-first and hybrid organization can all work; choose clear ownership and incremental changes over boilerplate.

Follow Dart null safety, error/stack propagation and existing analyzer conventions. Validate external data rather than using casts or null assertions to disguise schema errors. Preserve serialized null/absent/zero values, numeric and temporal semantics. Keep generated files generated through the established tool/version; do not edit them or add code generation for a tiny model without benefit.

## Distinguish rebuild from identity/lifetime

Widgets describe configuration, elements preserve identity/state in the tree, and render objects perform layout/paint. A rebuild can reuse the same state; a changed key/type or removed subtree can create a fresh owner. Trace the actual identity/provider/router change before attributing a request to rendering.

Create owned controllers/listeners outside repeated build work. Initialize once per appropriate owner; use dependency/update hooks when inputs genuinely change. `didChangeDependencies` can run repeatedly, while `didUpdateWidget` can introduce a new resource ID. A boolean “already loaded” guard can suppress necessary tenant/filter updates as easily as it prevents duplication.

For FutureBuilder, obtain/reuse the relevant Future before build, replacing it when its actual key changes. Constructing a new Future during build restarts work on rebuild; even an already-completed replacement can produce a waiting frame. Do not add a global cache or artificial delay to hide this lifecycle mismatch.

Use stable keys for real identity/reordering; avoid random/UniqueKeys to force refresh. Keeping a tab alive retains more than scroll position, including listeners and potentially private data. Choose retention intentionally, and reset identity-sensitive owners when the account/resource changes.

## Own resources explicitly

The creator/provider owns disposal unless its contract transfers ownership. Do not dispose a borrowed controller, HTTP client or shared state object. Provider creation versus `.value`, BlocProvider-created versus borrowed blocs, and Riverpod auto-dispose/keep-alive/recomputation have different contracts. Read the installed API rather than assuming a route pop always destroys state or an exposed value is automatically closed.

Cancel timers/subscriptions, remove listeners and dispose owned controllers. Stream cancellation can have asynchronous cleanup; await it where the owning abstraction supports that, or deliberately manage completion/errors outside synchronous widget dispose. Widget disposal is not a guaranteed last chance to persist critical work when the OS kills the process.

## Async safety needs more than mounted

Await/return Futures or deliberately supervise detached work and its errors. `unawaited` documents intent; it does not catch exceptions. Keep `setState` callbacks synchronous and small. Async stream listeners do not inherently serialize event processing; choose ordering/concurrency through supported stream/state APIs when effects can overlap.

After an async gap, check the relevant context's validity before UI/navigation. Also verify that the result still belongs to the current query, resource, route and identity generation. A mounted screen can now represent a different account, and a valid context can navigate the wrong active stack. Prefer cancellation/result invalidation and correct ownership over merely suppressing “setState after dispose.”

`Future.timeout` stops waiting but lets source work continue. Future combinators do not automatically cancel siblings. Use supported transport/operation cancellation and handle partial completion according to the workflow. Keep CPU-heavy synchronous work off hot UI paths; adding async syntax alone does not move it to another isolate.
