# JavaScript, TypeScript, Python, and web research

Use the section matching the active runtime/framework. These are source-selection prompts, not implementation rules or a reason to introduce a listed framework.

## Authoritative entrypoints

| Area | Start here; investigate when relevant |
| --- | --- |
| TypeScript | [Documentation](https://www.typescriptlang.org/docs/) and [module reference](https://www.typescriptlang.org/docs/handbook/modules/reference.html): compiler/version, resolution host, emitted specifiers, exports and type/runtime differences |
| Node.js | [Learn](https://nodejs.org/learn) and [API reference](https://nodejs.org/api/): runtime release, event loop, streams, cancellation, package loading and actual client-library behavior |
| Python | [Official docs](https://docs.python.org/3/) and [packaging guide](https://packaging.python.org/): selected interpreter/environment, concurrency, dependency/backend versions and deployment model |
| React | [React docs](https://react.dev/): state ownership, identity/lifetime, Effects and supported integration behavior rather than folder templates |
| Next.js | [Next.js docs](https://nextjs.org/docs): installed version/router/bundler, cache scope, server/client boundary, invalidation and deployment; latest docs can differ from older installations |
| Vite | [Vite guide](https://vite.dev/guide/): build/dev differences, linked packages, aliases, environment exposure and asset resolution |

Select a version in the official documentation rather than assuming a floating URL matches the app. During this research `/3/` showed Python 3.15.2; it is not an instruction to upgrade. For example, [TaskGroup documentation](https://docs.python.org/3/library/asyncio-task.html) identifies its introduction in 3.11 and subsequent behavior changes. Read the target version before using a recently documented method.

## Repository seeds

- [Next.js](https://github.com/vercel/next.js): inspect relevant runtime implementation, integration tests and linked regressions. Its checked default branch was `canary`, so do not treat a search result there as a released stable API.
- [Twenty](https://github.com/twentyhq/twenty): product-scale feature, permission and package interactions; inspect actual owners, tests and licensing before borrowing. Studying its NestJS implementation does not justify migrating an Express app.
- [Bulletproof React](https://github.com/alan2207/bulletproof-react): an opinionated example for feature locality and integration tradeoffs, not React's prescribed structure.
- [Node best practices](https://github.com/goldbergyoni/nodebestpractices): community guidance and links to explanations; verify claims against current Node/framework behavior and this service's needs.
- [FastAPI](https://github.com/fastapi/fastapi): dependency/request lifecycle, validation and regression tests where FastAPI is actually relevant. Do not impose its abstractions on another Python stack.

Other than the pinned examples below, these are discovery entries, not complete repository quality audits.

## Examples actually inspected

- [Next dedupe implementation, pinned ref](https://github.com/vercel/next.js/blob/65e4a5eda25e9cda5b1c21e05e5bbb225aece3ee/packages/next/src/server/lib/dedupe-fetch.ts) contains request-shape/lifetime conditions and points to [PR 73274](https://github.com/vercel/next.js/pull/73274). The PR describes a response-cloning workaround and was merged. Inspect the installed release and actual request path before generalizing this to all caching or copying the workaround.
- [FastAPI generator-dependency implementation](https://github.com/fastapi/fastapi/blob/79cab5bed28b24d92c185d236feb33f5783dfeb3/fastapi/dependencies/utils.py) and [context-variable regression test](https://github.com/fastapi/fastapi/blob/79cab5bed28b24d92c185d236feb33f5783dfeb3/tests/test_dependency_contextvars.py) show why lifecycle claims should be traced through implementation and a narrowly asserted test. These files were read, not executed.

Both repositories had recent commit evidence when inspected; that does not establish compatibility, absence of defects or suitability for another application. Use the installed framework's public API as the contract and internal source as supporting evidence.
