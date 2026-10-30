# Authoritative source and version register

Researched 2026-10-30. This skill is original decision guidance, not a copy of the linked manuals. Consult documentation matching the deployed Node.js, framework, client, OS, and provider before relying on an API/default. Current documentation links move; check history and release notes rather than assuming every documented capability is available in an older LTS.

## Skill engineering

| Authority | Applied decision |
| --- | --- |
| Locally installed `skill-creator/SKILL.md`, metadata reference, initializer, and validator | Precise activation, compact entrypoint, conditional references, supported user-level installation and normal validation |
| [OpenAI GPT-6 Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), [Skills guide](https://developers.openai.com/api/docs/guides/tools-skills) | Outcome and decision boundaries rather than exhaustive recipes; detail loaded only for the task |
| [Agent Skills specification](https://agentskills.io/specification), [Codex discovery](https://learn.chatgpt.com/docs/build-skills) | Portable name/description manifest; host-specific UI metadata remains optional |
| [OpenAI skill evaluation guidance](https://developers.openai.com/blog/eval-skills) | Distinguish static validation from observed engineering behavior. This installation uses normal checks as requested, without agent evaluations or benchmark claims |

The API and PostgreSQL skills complement this skill's implementation/runtime scope. They are optional and are not tool or runtime dependencies.

## Versions and authority

[Node.js releases](https://nodejs.org/en/about/previous-releases) and the [Release Working Group schedule](https://github.com/nodejs/Release/blob/main/schedule.json) were checked. At research time, 26 was Active LTS, 24 and 22 were Maintenance LTS, and 27 was Alpha. The local authoring runtime was 24.22.1. These are dated observations, not permanent pins or instructions to upgrade unrelated projects. The published release policy is changing from the earlier odd/even cadence; recheck the schedule instead of hard-coding that rule.

Node.js implementation/API documentation governs runtime behavior; libuv and V8 describe underlying components. Framework and driver documentation governs their abstractions. OWASP recommendations are risk guidance, not Node.js API guarantees. Examples and tuning recommendations require workload/deployment judgment.

## Runtime, language, and diagnostics

| Official source | Retained consequence |
| --- | --- |
| [Don't block the event loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop), [event loop and nextTick](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick), [libuv design](https://docs.libuv.org/en/v1.x/design.html) | Separate JS, OS I/O, and shared worker-pool contention; avoid starvation and timer-order assumptions |
| [Worker threads, 24.x](https://nodejs.org/docs/latest-v24.x/api/worker_threads.html), [Abort APIs](https://nodejs.org/api/globals.html#class-abortcontroller) | CPU offloading has scheduling/ownership costs; cancellation is cooperative and API/version dependent |
| [Async context](https://nodejs.org/api/async_context.html), [performance hooks, 24.x](https://nodejs.org/docs/latest-v24.x/api/perf_hooks.html) | Scoped correlation, context-loss diagnosis, event-loop evidence and correct units |
| [Native TypeScript, 24.x](https://nodejs.org/docs/latest-v24.x/api/typescript.html), [Node packages](https://nodejs.org/api/packages.html), [TypeScript module reference](https://www.typescriptlang.org/docs/handbook/modules/reference.html) | Type stripping is not checking or tsconfig transformation; match build/module behavior to deployment |
| [Understanding memory](https://nodejs.org/en/learn/diagnostics/memory/understanding-and-tuning-memory), [heap snapshots](https://nodejs.org/en/learn/diagnostics/memory/using-heap-snapshot), [diagnostic reports](https://nodejs.org/api/report.html) | Separate heap/RSS/external retention, avoid speculative tuning, account for diagnostic pauses, memory and secrets |
| [V8 GC architecture](https://v8.dev/blog/trash-talk) | Background/concurrent GC explains why a process has more threads than its JS event loop; this older architecture article is not a current tuning recipe |
| [Process, 24.x](https://nodejs.org/docs/latest-v24.x/api/process.html), [test runner, 24.x](https://nodejs.org/docs/latest-v24.x/api/test.html) | Fatal-state and exit-hook limits; built-in test support is an option when it fits existing tests |
| [OpenTelemetry Node.js](https://opentelemetry.io/docs/languages/js/getting-started/nodejs/) | Instrumentation loading differs by module path; reuse the provider and control data exposure/cardinality |

Material version examples: native type stripping became stable in 24.12; `AbortSignal.any` was added in 20.3/18.17; HTTP idle-connection shutdown changed in 19. These illustrate why capability checks matter. Some current docs served 26.x during research, so newer methods/options must not be assumed on local 24.x. Do not import newer convenience APIs merely to satisfy this skill.

## HTTP, framework, and integration semantics

| Official source | Retained consequence |
| --- | --- |
| [HTTP API](https://nodejs.org/api/http.html) | Distinct timeout/lifecycle events, disconnect versus completion, shutdown and upgraded-connection limitations |
| [Streams](https://nodejs.org/api/stream.html), [backpressure](https://nodejs.org/en/learn/modules/backpressuring-in-streams) | Buffer thresholds, writable flow control, error/cleanup ownership, HTTP pipeline destruction |
| [Undici upstream](https://github.com/nodejs/undici), [Undici documentation](https://undici.nodejs.org/) | Fetch dispatcher ownership, consume/cancel bodies, Node-specific lifecycle rather than browser GC assumptions |
| [Express error handling](https://expressjs.com/en/guide/error-handling/), [Fastify server lifecycle](https://fastify.dev/docs/latest/Reference/Server/) | Use installed-framework behavior rather than a universal async wrapper or custom shutdown manager |
| [ws upstream](https://github.com/websockets/ws) | Authentication, heartbeat/cleanup and compression/buffering considerations; not a durable delivery protocol |
| [node-postgres transactions](https://node-postgres.com/features/transactions) | A transaction owns one client; pooled independent calls do not form a transaction |
| [node-redis connections](https://redis.io/docs/latest/develop/clients/nodejs/connect/) | Error events, reconnect/offline behavior and lifecycle must match installed client semantics |
| [RabbitMQ confirmations](https://www.rabbitmq.com/docs/confirms), [consumer prefetch](https://www.rabbitmq.com/docs/consumer-prefetch) | Publisher confirmation and consumer acknowledgement cover different boundaries; redelivery and bounded consumption remain application concerns |

The broker/client examples teach boundaries rather than prescribe those products. Apply the existing queue, ORM, cache, or cloud client's documented semantics.

## Security and supply chain

| Official source | Retained consequence |
| --- | --- |
| [Node.js security](https://nodejs.org/en/learn/getting-started/security-best-practices), [permission model](https://nodejs.org/api/permissions.html) | Runtime/resource hardening and parser boundaries; permissions are not a hostile-code sandbox |
| [OWASP Node.js cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html) | Validate trust boundaries, bound expensive work, handle errors/context safely, and protect sensitive execution |
| [SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html), [command injection](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html), [prototype pollution](https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html), [CSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | Destination/redirect validation, argument-level injection, safe object handling, and cookie-authentication defenses need separate controls |
| [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/), [npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit/) | Lock-consistent installation still has lifecycle-script risk; audit output requires reviewed compatible remediation |

## Resolve competing approaches by requirement

- Worker threads, chunking, and durable jobs solve different CPU/lifetime problems; async syntax alone solves none of them.
- Abort, deadline, retry, and rollback protect different boundaries. Combine only what the operation requires, within one budget and replay policy.
- Direct modules and framework facilities are preferable until measured complexity justifies additional layers or infrastructure.
- Readiness, graceful drain, forced termination, and crash recovery are complementary. None can guarantee a process always finishes its work.
- Built-ins and established libraries both have value. Match capability, version, maintenance, and project conventions instead of mandating a package or a dependency-free rewrite.
