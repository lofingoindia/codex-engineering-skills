# Next.js, React, and Vite organization

## Next.js file location changes behavior

Establish App Router, Pages Router, or deliberate coexistence, plus the installed Next.js version and bundler. Keep framework entry files recognizable and delegate cohesive implementation when useful. Do not migrate routers as part of organization work.

In App Router:

- Folders form route segments; `page` and `route` entry files expose endpoints. Other implementation files can be colocated without automatically becoming routes.
- `(group)` organizes segments/layouts without adding that name to the URL. `_folder` opts its subtree out of routing; it does not provide code privacy or authorization. Route groups can still create URL collisions or change layout ownership when moved.
- Moving a layout, template, loading/error boundary, parallel slot or intercepted route can change provider lifetime, state preservation, loading scope, and navigation behavior. A URL that looks unchanged does not prove the refactor preserves UX.
- Preserve server/client import graphs. `use client` defines a client module boundary; moving that directive to a broad barrel can pull unrelated dependencies into it. Mark server-only implementations with supported tooling where appropriate and keep client-safe contracts separate. Server Functions remain remotely invocable operations that require authorization, regardless of their folder.

In Pages Router, files under `pages` participate in file-based routing according to configured extensions and special-file conventions; `pages/api` defines API routes. Do not apply App Router's safe-colocation rules to ordinary helper/component files in `pages`. Preserve `_app`, `_document`, route paths, and existing data-loading boundaries.

`src` is optional. Avoid duplicate active roots and moving root configuration or `public` just to make everything live under `src`. Check the version's actual discovery rules for metadata files, proxy/middleware, instrumentation and other special entrypoints before relocating them.

For a shared package, inspect how the selected router and bundler compile it before adding `transpilePackages`; current toolchains can compile some workspace packages automatically. Inspect standalone/file-tracing roots and required runtime assets after moves outside the app root. Compilation and deployment tracing solve different problems.

## React feature and state ownership

Keep a page's components, local hooks, forms and adapters with that feature unless they have a broader stable contract. Use shared UI for genuinely reusable primitives, not a central directory containing every screen component. React specifies behavior and composition, not a universal folder tree.

Put state at the owner whose lifetime and consumers require it. A form draft can stay local; a provider belongs at the narrowest scope that needs the shared instance. Extracting a custom hook shares logic, not automatically state, network deduplication, or a cache. Moving provider placement can reset state, duplicate subscriptions, or retain account-specific state too long. Reuse the application's existing router and server-state system.

Do not create a new `services`, `store`, and `hooks` hierarchy for each small feature. A component and a small adjacent helper may be sufficient. Preserve JS/TS choices and design-system conventions without forcing migrations.

## Vite package and asset boundaries

Inspect source root, aliases, dev-server resolution, linked packages, dependency deduplication, public assets and production build behavior. A sibling package resolving in development may still fail in production or in a separately packed consumer.

Vite treats linked dependencies outside normal `node_modules` resolution as source; its documented handling expects suitable ESM, with optimization options for incompatible packages where needed. Do not cargo-cult optimizer settings or assume development pre-bundling describes production output.

Avoid multiple runtime copies of React introduced by shared packages or links; inspect peer dependencies and actual resolution before adding aliases/dedupe settings. Browser consumers must not import Node-only clients or secret-bearing configuration through a “shared” entrypoint.

Moves can invalidate CSS imports, URL-based assets, `public` URLs, `import.meta.glob` patterns, dynamic imports, tests, and route discovery plugins. Recheck their owning configuration and affected runtime paths. Keep public/client-exposed environment values free of secrets; a repository folder name cannot protect bundled content.
