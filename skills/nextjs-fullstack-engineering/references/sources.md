# Source and compatibility register

Researched 2026-10-30. These references support original engineering synthesis, not a copied Next.js handbook. Prefer the installed package's relevant documentation over a moving current or canary page. Runtime/API behavior, normative standards, accessibility techniques, and opinionated workflow recommendations have different authority.

## Version and documentation policy

The [published `next` package](https://registry.npmjs.org/next/latest) and current docs reported **16.4.3**. The [support policy](https://nextjs.org/support-policy) listed 16.x Active LTS and 15.x Maintenance LTS, with 15's security maintenance extended through 2027-01-31. These are dated observations, not permanent version pins. Inspect resolved dependencies, lockfile, Node.js/React compatibility, feature flags, deployment adapter and advisories for every version-sensitive change.

The [AI agents guide](https://nextjs.org/docs/app/guides/ai-agents) documents bundled `node_modules/next/dist/docs/` from 16.2 and managed documentation instructions from 16.3. Locate the actual installed package in monorepos. Respect existing managed `AGENTS.md` blocks and version-indexed `.next-docs` instructions; do not recreate that integration or copy the docs into this skill. An unavailable bundled page can be researched in matching official docs without installing unrelated tooling.

The [16 migration guide](https://nextjs.org/docs/app/guides/upgrading/version-16) and [15 migration guide](https://nextjs.org/docs/app/guides/upgrading/version-15) document changing request APIs, cache defaults and tooling. Current recommended new-app Cache Components/Partial Prefetching defaults are not evidence that an existing app uses them. Cache Components needs its supported Node.js runtime; old segment options and experimental PPR flags are not interchangeable with the new model.

## First-party specialized workflows

Inspected upstream `SKILL.md` files on Vercel's **canary** branch. They can change independently of a stable project's installed framework. Recheck their current prerequisites before invoking; none was installed or copied during this skill's creation.

| Official skill | Use and observed compatibility boundary |
| --- | --- |
| [next-dev-loop](https://github.com/vercel/next.js/blob/canary/skills/next-dev-loop/SKILL.md) | Runtime framework/browser cross-checks. Inspected version requires Next.js 16.3+, Turbopack, running dev server and agent-browser 0.31.1+; discover actual MCP tools rather than invent names |
| [next-cache-components-adoption](https://github.com/vercel/next.js/blob/canary/skills/next-cache-components-adoption/SKILL.md) | An intentional App Router Cache Components migration, with configuration/error guidance and verification. Inspected workflow requires 16.3+ and a runnable app; it does not migrate Pages routes |
| [next-cache-components-optimizer](https://github.com/vercel/next.js/blob/canary/skills/next-cache-components-optimizer/SKILL.md) | A named static-shell/initial or client-navigation UI goal with supported instant-test coverage. Requires 16.3+ and Cache Components already adopted |
| [next-partial-prefetching-adoption](https://github.com/vercel/next.js/blob/canary/skills/next-partial-prefetching-adoption/SKILL.md) | Intentional Partial Prefetching adoption preserving required prefetched UI. Inspected prerequisites include 16.3+, working Cache Components and production-like verification |
| [next-bundle-optimizer](https://github.com/vercel/next.js/blob/canary/skills/next-bundle-optimizer/SKILL.md) | Audit/fix initial browser bundle work using supported analyzer artifacts; inspect installed CLI support and requested scope before running |

This skill selects and complements those workflows; it does not provide competing migration recipes, testing rigs, or analyzer utilities. For an ordinary fix on an incompatible stack, continue using available docs/project tools without pretending the specialized workflow ran. Preserve explicit workflow boundaries when a user actually invokes one.

## Rendering, routing, and data correctness

| Official sources | Retained judgment |
| --- | --- |
| [Project structure](https://nextjs.org/docs/app/getting-started/project-structure), [layouts/pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages), [server/client components](https://nextjs.org/docs/app/getting-started/server-and-client-components) | Router/file/module boundaries and composition; no universal folder tree or client-only dashboard |
| [Linking/navigation](https://nextjs.org/docs/app/getting-started/linking-and-navigating), [templates](https://nextjs.org/docs/app/api-reference/file-conventions/template), [preserving UI state](https://nextjs.org/docs/app/guides/preserving-ui-state) | Different render/remount/retained-Activity behavior; decide intentional resets and verify identity transitions |
| [Prefetching](https://nextjs.org/docs/app/guides/prefetching), [Partial Prefetching adoption](https://nextjs.org/docs/app/guides/adopting-partial-prefetching), [router API](https://nextjs.org/docs/app/api-reference/functions/use-router) | Prefetch versus actual navigation, safe programmatic URLs, refresh versus server invalidation |
| [Fetching](https://nextjs.org/docs/app/getting-started/fetching-data), [fetch reference](https://nextjs.org/docs/app/api-reference/functions/fetch), [backend-for-frontend](https://nextjs.org/docs/app/guides/backend-for-frontend) | Diagnose actual owners/waterfalls; server-to-source reads, deliberate BFF boundaries, no automatic Action read transport |
| [Caching](https://nextjs.org/docs/app/getting-started/caching), [Cache Components config](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents), [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache), [previous model](https://nextjs.org/docs/app/guides/caching-without-cache-components) | Model/host-specific scope and lifetime; request API constraints, keys, runtime storage and version-sensitive defaults |
| [Revalidating](https://nextjs.org/docs/app/getting-started/revalidating), [revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag), [updateTag](https://nextjs.org/docs/app/api-reference/functions/updateTag), [revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath) | Distinguish stale-while-revalidate, immediate expiry, path scope, caller context and read-your-own-writes |
| [React cache](https://react.dev/reference/react/cache), [StrictMode](https://react.dev/reference/react/StrictMode), [Suspense](https://react.dev/reference/react/Suspense), [transitions](https://react.dev/reference/react/useTransition) | Request memoization is not persistence; development checks are not production counts; suspension and transitions have specific integration/ordering limits |
| [Pages getServerSideProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-server-side-props), [getStaticProps](https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props), [Pages navigation](https://nextjs.org/docs/pages/building-your-application/routing/linking-and-navigating) | Keep Pages rendering/data/navigation semantics intact; server-fetched props are browser-visible |

## Security, experience, and public performance

| Official sources | Retained judgment |
| --- | --- |
| [Authentication](https://nextjs.org/docs/app/guides/authentication), [data security](https://nextjs.org/docs/app/guides/data-security), [mutating data](https://nextjs.org/docs/app/getting-started/mutating-data), [redirect](https://nextjs.org/docs/app/api-reference/functions/redirect) | Live authorization at data/action boundaries, minimal exposure, session ownership, actual mutation success and framework control flow |
| [CSP](https://nextjs.org/docs/app/guides/content-security-policy), [environment variables](https://nextjs.org/docs/app/guides/environment-variables) | Security controls must match rendering; public build-time values are not runtime secrets |
| [Errors](https://nextjs.org/docs/app/getting-started/error-handling), [not-found behavior](https://nextjs.org/docs/app/api-reference/file-conventions/not-found), [metadata](https://nextjs.org/docs/app/getting-started/metadata-and-og-images), [JSON-LD](https://nextjs.org/docs/app/guides/json-ld) | Distinct failure states; streaming/status limitations, technical SEO and safe structured data without ranking promises |
| [Image](https://nextjs.org/docs/app/api-reference/components/image), [fonts](https://nextjs.org/docs/app/getting-started/fonts), [lazy loading](https://nextjs.org/docs/app/guides/lazy-loading), [React Compiler](https://react.dev/learn/react-compiler/introduction), [Web Vitals](https://web.dev/articles/vitals) | Correct assets and boundaries before speculative memoization/lazy loading; field and lab evidence serve different purposes |
| [WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/), [APG modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), [Radix accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility), [shadcn/ui](https://ui.shadcn.com/docs) | WCAG supplies criteria; APG and libraries guide implementation. Composition still requires labels, focus, usable states and manual checks |

Consult [Next.js advisories](https://github.com/vercel/next.js/security/advisories) and [React advisories](https://github.com/react/react/security/advisories) for the installed dependency graph. Examples reviewed: [nested cache/root-param leakage](https://github.com/vercel/next.js/security/advisories/GHSA-h694-7cp9-m8p3), and [image optimizer/upstream library RCE](https://github.com/vercel/next.js/security/advisories/GHSA-2464-fhr4-w9xw). These demonstrate why key design and patched transitive dependencies both matter; they are not an exhaustive or permanent safe-version list.

## Operations, tests, and skill authoring

| Authority | Retained decision |
| --- | --- |
| [Self-hosting](https://nextjs.org/docs/app/guides/self-hosting), [CDNs](https://nextjs.org/docs/app/guides/cdn-caching), [static export](https://nextjs.org/docs/app/guides/static-exports), [instrumentation](https://nextjs.org/docs/app/guides/instrumentation) | Verify hosting capabilities, skew, separate cache-handler interfaces, external cache variants/invalidation, streaming and runtime-specific telemetry |
| [Testing overview](https://nextjs.org/docs/app/guides/testing), [Next/Playwright](https://nextjs.org/docs/app/guides/testing/playwright), [Next/Vitest](https://nextjs.org/docs/app/guides/testing/vitest), [Playwright practices](https://playwright.dev/docs/best-practices), [Testing Library principles](https://testing-library.com/docs/guiding-principles/) | Match tests to runtime boundaries; observable user behavior, isolation and production-mode evidence when relevant. Unit tooling does not universally support async RSC |
| Bundled local `skill-creator/SKILL.md`, UI metadata guide, initializer and validator | Supported installation, precise description, compact workflow and conditional references; no unnecessary scripts/templates |
| [OpenAI Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), [Skills guide](https://developers.openai.com/api/docs/guides/tools-skills), [Agent Skills specification](https://agentskills.io/specification) | Outcomes and decision boundaries, progressive disclosure, portable metadata and proportional work |
| [OpenAI skill evaluations](https://developers.openai.com/blog/eval-skills) | Static package checks do not prove improved agent behavior. This creation used normal verification as requested, without evaluations or benchmarks |

When recommendations conflict, resolve them with the project's router, version, data visibility, freshness, state ownership and deployment constraints. Newer caching, client querying, request-time rendering, and static delivery each fit different boundaries; none is a universal winner.
