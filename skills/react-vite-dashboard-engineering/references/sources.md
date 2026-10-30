# Authoritative sources and applicability

Researched 2026-10-30. These are primary sources used to form original, task-oriented guidance. Versions are dated research observations, not mandated dependencies. Check installed packages, stable versus experimental APIs, provider behavior, and actual deployment support when applying the skill.

## Skill design

| Source | Retained decision |
| --- | --- |
| Bundled `skill-creator/SKILL.md` and metadata/validation tooling, inspected locally | Precise activation, short root workflow, on-demand references, no unnecessary runtime scripts |
| [OpenAI GPT-6 Astra skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Outcome-focused instructions and clear boundaries; avoid bloated recipes and incidental rules |
| [OpenAI Skills guide](https://developers.openai.com/api/docs/guides/tools-skills), [Agent Skills specification](https://agentskills.io/specification) | Required name/description and progressive loading; no connector/API upload needed for a local user skill |
| [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills) | Current docs list user `~/.agents/skills`; bundled creator uses `~/.codex/skills`. This host's fresh session verified discovery from the latter, avoiding duplicate installations |
| [OpenAI skill evaluation guidance](https://developers.openai.com/blog/eval-skills) | Valid Markdown alone is not behavior evidence. Honor the user's requested validation scope; normal checks and truthful limits rather than an unsolicited large evaluation suite |

## React and build toolchain

| Source | Status / useful boundary |
| --- | --- |
| [React versions](https://react.dev/versions) | Official current docs identify React 19.3, released 2026-09-09; use project-version guidance for older apps |
| [Suspense](https://react.dev/reference/react/Suspense) | Library behavior: supported suspending resources, not ordinary Effect fetching; experimental options are not a safe general default |
| [useTransition](https://react.dev/reference/react/useTransition), [useDeferredValue](https://react.dev/reference/react/useDeferredValue) | Rendering priority/continuity; neither automatically solves out-of-order async work or eliminates network requests |
| [You might not need an Effect](https://react.dev/learn/you-might-not-need-an-effect), [useEffect](https://react.dev/reference/react/useEffect) | React engineering guidance and lifecycle semantics; derive values, handle actions directly, clean up external synchronization |
| [Profiler](https://react.dev/reference/react/Profiler) | Measurement API; not a mandate to instrument every component |
| [Vite guide](https://vite.dev/guide/), [8.1 release](https://vite.dev/blog/announcing-vite8-1) | Current guide and 2026-06-23 release; versioned Node/plugin/browser compatibility matters, experimental bundled dev mode is optional |
| [Vite features](https://vite.dev/guide/features), [environment/modes](https://vite.dev/guide/env-and-mode) | TypeScript transpilation versus checking; client configuration exposure and build-time replacement |
| [Vite build](https://vite.dev/guide/build), [static deployment](https://vite.dev/guide/static-deploy) | Production artifact, base/assets, chunk failure recovery; preview is not production hosting |

## Routing and API consumption

| Source | Status / useful boundary |
| --- | --- |
| React Router [modes](https://reactrouter.com/start/modes), [state management](https://reactrouter.com/explanation/state-management), [race conditions](https://reactrouter.com/explanation/race-conditions) | Current docs show 8.5.1 alongside older supported-version docs. Declarative/Data/Framework modes expose different capabilities; UI cancellation does not roll back a server mutation |
| TanStack Query [overview](https://tanstack.com/query/latest/docs/framework/react/overview), [defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults), [keys](https://tanstack.com/query/latest/docs/framework/react/guides/query-keys) | Current docs identify v5. Optional server-state architecture; freshness and retention differ, query identity includes result-changing inputs |
| Query [cancellation](https://tanstack.com/query/latest/docs/framework/react/guides/query-cancellation), [invalidation](https://tanstack.com/query/latest/docs/framework/react/guides/invalidations-from-mutations), [optimism](https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates) | Library semantics, not universal patterns. Cancellation needs client signal consumption; choose appropriate completion and concurrent rollback behavior |
| [TanStack Table data](https://tanstack.com/table/latest/docs/guide/data) | Current docs identify v9; inspect actual adapter/version and stable-reference requirements. A headless table does not supply the finished UX or accessibility |
| [MDN Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch), [BroadcastChannel](https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API) | Browser platform documentation; HTTP errors need interpretation, tab messages are signals rather than server authority |

## Security and accessibility

| Source | Publication status / use |
| --- | --- |
| [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700) | OAuth Security BCP 240 (January 2025); current secure OAuth practices and grant/redirect/token constraints |
| [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017.html) | Browser OAuth BCP 212 (August 2026), published successor to the browser-app draft; compare BFF, token-mediating and browser-only threats, rather than treating it as an unpublished proposal |
| [OWASP API Security](https://api-security.owasp.org/) | Backend permission threat model complements browser checks; current project lists 2023 API Top 10 |
| OWASP [HTML5/storage](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html), [sessions](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [DOM XSS](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html) | Security engineering guidance; script-accessible storage, lifecycle, browser credentials, safe rendering, and usable defenses |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [quick reference](https://www.w3.org/WAI/WCAG22/quickref/) | W3C Recommendation (current dated recommendation 2024-12-12); normative success criteria. Techniques/quickref are supporting guidance |
| APG [dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), [table](https://www.w3.org/WAI/ARIA/apg/patterns/table/), [grid](https://www.w3.org/WAI/ARIA/apg/patterns/grid/) | W3C practical, non-normative interaction patterns; correct roles include keyboard/focus behavior |
| [Reduced motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) | Browser preference documentation; reduce nonessential motion without hiding meaningful state changes |

## Design, measurement, and normal testing

| Source | Retained judgment |
| --- | --- |
| [shadcn/ui](https://ui.shadcn.com/docs), [Radix accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility) | Optional code/primitives; preserve existing systems, labels and composition. Neither automatically proves final-app conformance |
| [Carbon loading](https://www.carbondesignsystem.com/building-blocks/core/patterns/loading) | Design-system recommendation updated 2026-08-11; structured skeletons, local indicators and progressive rendering; no universal artificial delays |
| [GOV.UK error summary](https://design-system.service.gov.uk/components/error-summary/) | Tested design-system form pattern; adapt summary/focus and field errors to form complexity rather than importing an entire visual system |
| [Web Vitals](https://web.dev/articles/vitals), [INP](https://web.dev/articles/inp) | Browser performance engineering guidance: LCP/INP/CLS and field percentiles, complemented by dashboard route/data interactions |
| [Playwright practices](https://playwright.dev/docs/best-practices), [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) | Official testing guidance: user-visible outcomes, isolation, accessible locators, appropriate browser coverage; avoid implementation-only snapshots |
| [Vitest guide](https://vitest.dev/guide/), [migration](https://vitest.dev/guide/migration/) | Official runner docs; verify Node/Vite/DOM environment and installed-version requirements before adopting or updating |

## Context-dependent choices

- **Fetching:** a router's data flow, query cache, or a small Effect can fit different projects. Select one intentional ownership path and reuse it.
- **Freshness:** manual/navigation refresh, cache revalidation, and existing event delivery have different costs. Polling and new sockets require actual need.
- **Authentication:** cookies/BFF reduce browser token exposure but retain CSRF/XSS considerations; browser OAuth has different constraints. Preserve a sound model and investigate real weaknesses.
- **Loading and motion:** choose local feedback from task shape and actual latency, not a universal skeleton/spinner/Suspense policy.
- **Performance and accessibility:** optimize measured bottlenecks while preserving keyboard semantics, focus, data correctness, and legitimate workflows.
