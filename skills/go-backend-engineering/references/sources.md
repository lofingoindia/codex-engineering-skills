# Authoritative source and version register

Researched 2026-10-30. Guidance is original engineering synthesis; linked manuals remain the implementation authority. Recheck the target project's selected Go version, language requirement, libraries, build tags, platform and deployment before relying on changing APIs/defaults. Do not load this entire register for an ordinary local fix.

## Versions and authority

The [official download feed](https://go.dev/dl/?mode=json) listed **Go 1.27.3** as stable; local read-only `go version` also returned 1.27.3 on windows/amd64. The [release policy/history](https://go.dev/doc/devel/release) supports a release until two newer major releases exist, making 1.26 and 1.27 the supported families at research time. These observations are dated, not a requirement to upgrade every repository now.

[Toolchain selection](https://go.dev/doc/toolchain) distinguishes a module's minimum/language `go` directive, suggested `toolchain`, workspace requirements and auto selection. Inspect the actual build image/toolchain too. The [Go compatibility promise](https://go.dev/doc/go1compat) does not freeze runtime details, performance, security fixes or undefined/incorrect behavior.

Useful version distinctions:

- [Go 1.24](https://go.dev/doc/go1.24): traversal-resistant `os.Root` and benchmark `B.Loop` APIs require a compatible toolchain; inspect their exact scope before using them.
- [Go 1.25](https://go.dev/doc/go1.25): `WaitGroup.Go`, stable `testing/synctest`, and container-aware GOMAXPROCS are relevant examples. GOMAXPROCS defaults also depend on language compatibility settings/overrides.
- [Go 1.27](https://go.dev/doc/go1.27): JSON v2 is available without the earlier experimental-only model; v1 remains supported with preserved behavior. `goroutineleak` profiling becomes generally available but detects only a subset of leaks. The old `asynctimerchan` compatibility option is removed. Do not import these assumptions into an older service.

Language specification/memory-model requirements are stronger authority than style preferences. Runtime implementation documents explain the current implementation, not an application scheduling guarantee. Effective Go explicitly notes that it predates modules/generics and is not actively updated; use it for enduring idioms alongside current contracts.

## Language, concurrency, and runtime

| Official source | Retained engineering consequence |
| --- | --- |
| [Specification](https://go.dev/ref/spec), [memory model](https://go.dev/ref/mem) | Value/aliasing and channel semantics, synchronization/publication; race freedom does not establish a business invariant |
| [Effective Go](https://go.dev/doc/effective_go), [Code Review Comments](https://go.dev/wiki/CodeReviewComments), [module organization](https://go.dev/doc/modules/layout), [errors](https://pkg.go.dev/errors) | Explicit readable implementation, consumer-driven interfaces, appropriate packages/errors; no universal layout or class hierarchy |
| [Context](https://pkg.go.dev/context), [pipelines/cancellation](https://go.dev/blog/pipelines), [sync](https://pkg.go.dev/sync), [errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup) | Owned cancellation/completion, sender/closure responsibilities, temporary pooling, group context and bounded-submission caveats |
| [Runtime API](https://pkg.go.dev/runtime), [container-aware GOMAXPROCS](https://go.dev/blog/container-aware-gomaxprocs), installed `src/runtime/HACKING.md` | G/M/P model, CPU versus goroutine/thread counts, quota/affinity and override behavior; avoid scheduler assumptions as correctness mechanisms |
| [GC guide](https://go.dev/doc/gc-guide), [memory target API](https://pkg.go.dev/runtime/debug#SetMemoryLimit), [diagnostics](https://go.dev/doc/diagnostics) | Retained versus allocated memory, CPU/heap tradeoffs, soft memory target versus RSS and evidence-led diagnosis |
| [pprof](https://pkg.go.dev/runtime/pprof), [execution trace](https://pkg.go.dev/runtime/trace), [HTTP pprof](https://pkg.go.dev/net/http/pprof) | Choose profiles by question, protect diagnostic data and verify DefaultServeMux exposure |

Critical contracts were also read with the installed toolchain's `go doc`, including Context/WithoutCancel/AfterFunc, WaitGroup.Go, GOMAXPROCS, Pool, Reader/Copy, Timer.Stop and error classification. This grounds current behavior; future application work must select that application's version.

## Network, data, and external effects

| Official source | Retained engineering consequence |
| --- | --- |
| [net/http](https://pkg.go.dev/net/http), [io](https://pkg.go.dev/io), [os/signal](https://pkg.go.dev/os/signal) | Separate time/size/lifetime boundaries, client reuse and body ownership, partial I/O, response lifetime, finite shutdown and signal cleanup |
| [JSON v1](https://pkg.go.dev/encoding/json), [JSON v2](https://pkg.go.dev/encoding/json/v2) | Decoding defaults and representation changes can affect security and compatibility; do not silently migrate existing contracts |
| [Managing connections](https://go.dev/doc/database/manage-connections), [cancellation](https://go.dev/doc/database/cancel-operations), [transactions](https://go.dev/doc/database/execute-transactions), [database/sql](https://pkg.go.dev/database/sql) | Reused pool handles, acquisition pressure, Rows/error/transaction lifetime and supported cancellation |
| [pgx](https://pkg.go.dev/github.com/jackc/pgx/v5), [pgxpool](https://pkg.go.dev/github.com/jackc/pgx/v5/pgxpool) | Native connection concurrency, explicit transaction finalization and cancellation differences from database/sql |
| [go-redis guide](https://redis.io/docs/latest/develop/clients/go/), [go-redis upstream](https://github.com/redis/go-redis) | Reused client/pool ownership, version-specific retry/deadline behavior and consistent cache scope |
| [AMQP Go client](https://pkg.go.dev/github.com/rabbitmq/amqp091-go), [upstream project](https://github.com/rabbitmq/amqp091-go), [RabbitMQ confirms/acks](https://www.rabbitmq.com/docs/confirms) | Actual context support, consumer/reconnect/channel lifecycle, publish versus consume guarantees and durable idempotency |
| [gRPC deadlines](https://grpc.io/docs/guides/deadlines/), [coder/websocket contracts](https://pkg.go.dev/github.com/coder/websocket) | Deadline propagation and library-specific connection/concurrency/read-loop behavior; examples do not prescribe these transports/libraries |

Read-only local HTTP docs included Client/Do, Request.Context, Transport, ResponseController, MaxBytesReader, TimeoutHandler, Shutdown/Close and RegisterOnShutdown. Database reads included BeginTx and Rows lifecycle. A Context argument, acknowledged publish or returned HTTP response is not a generic transaction/durability guarantee.

## Security, operations, and normal checks

| Official source | Retained engineering consequence |
| --- | --- |
| [Go security practices](https://go.dev/doc/security/best-practices), [vulnerability management](https://go.dev/doc/security/vuln/), [govulncheck](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck) | Current patched dependencies/toolchain and reachable known-vulnerability triage; no clean-scan claim of complete security |
| [Module integrity/security](https://go.dev/ref/mod#authenticating), [traversal-resistant files](https://go.dev/blog/osroot), [os.Root](https://pkg.go.dev/os#Root), [os/exec](https://pkg.go.dev/os/exec) | Checksums versus code trust, platform-aware filesystem boundaries, shell-free execution versus argument/process-tree risks |
| [Structured logging](https://pkg.go.dev/log/slog), [OpenTelemetry Go](https://opentelemetry.io/docs/languages/go/instrumentation/) | Reuse provider/log ownership, propagate causal context, redact and bound cardinality, finish telemetry within shutdown budget |
| [Testing](https://pkg.go.dev/testing), [httptest](https://pkg.go.dev/net/http/httptest), [race detector](https://go.dev/doc/articles/race_detector) | Choose meaningful assertions/tool support, distinguish handler mocks from network behavior and executed races from other concurrency failures |
| [Fuzzing](https://go.dev/doc/security/fuzz/), [synctest](https://pkg.go.dev/testing/synctest), [testing asynchronous behavior](https://go.dev/blog/testing-time) | Bounded isolated parser/property testing and controlled concurrency; fake-time bubbles are not real external-system tests |

For application work, the API skill can own broader consumer contracts and the PostgreSQL skill can own database isolation/schema/query/operations. These are optional complements, not dependencies. Client examples do not require new Redis, RabbitMQ, WebSocket or observability infrastructure.

## Skill engineering and evidence limits

The bundled local `skill-creator/SKILL.md`, UI metadata reference, initializer and validator were inspected. [OpenAI Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), the [Skills guide](https://developers.openai.com/api/docs/guides/tools-skills), [Agent Skills specification](https://agentskills.io/specification), and [skill evaluation guidance](https://developers.openai.com/blog/eval-skills) informed precise activation, progressive disclosure, proportional work and truthful verification claims. Their official guidance was researched in this conversation.

Creation verification uses normal metadata/link/package checks as requested. No agent evaluations, activation trials, baseline comparisons, application fixture tests or benchmarks were run. The skill advises appropriate Go testing when later modifying real application behavior; static validation of this skill is not evidence of improved agent decisions or production performance.

Resolve competing recommendations using the actual invariant, failure/replay boundary, resource lifetime, load and supported contracts. Channels versus locks, sync versus async work, pooling versus allocation, caching versus direct reads, and graceful drain versus cancellation protect different requirements. None is a universal architectural rule.
