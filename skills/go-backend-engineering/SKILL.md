---
name: go-backend-engineering
description: Build, review, debug, or improve Go backend services and workers, including concurrency, contexts, HTTP, integrations, resource ownership, security, and production recovery. Use for Go backend engineering decisions; skip unrelated languages, trivial syntax edits, and database-only or API-contract-only work.
---

# Go Backend Engineering

Make the requested service behavior correct, bounded, and recoverable under its actual operating conditions. Preserve sound project conventions and choose the smallest solution that protects the relevant invariant. Explicit user requirements and repository instructions take precedence over these defaults.

## Establish the execution and ownership model

Inspect applicable instructions and trace the affected handler, job, or subscription through its dependencies before proposing architecture. Read the relevant packages, constructors, entrypoint, tests, configuration, and deployment path. Establish:

- The task: feature, focused repair, concurrency/resource bug, integration, review, incident, security, or measured optimization.
- Module/workspace boundaries, `go.mod` language requirement, `toolchain` directive, actual build/deployment Go version, build tags, cgo, and platform constraints.
- Existing router/framework, clients/pools, validation, logging/telemetry, authentication, and test utilities.
- The data/business invariant, tenant boundary, acceptable partial failure, replay semantics, and affected consumers.
- Owners and lifetimes of goroutines, contexts, channels, locks, connections, streams, timers, and durable work.

Keep investigation bounded to the task. Use matching official docs and the selected toolchain's `go doc` or source for uncertain contracts. A newer local compiler does not change a project's minimum language/API requirement. Do not upgrade toolchains, replace frameworks, or change global Go environment settings as incidental cleanup.

## Load only relevant guidance

| Decision or symptom | Reference |
| --- | --- |
| Package boundaries, interfaces, errors, data representation, configuration, security | [Language and security](references/language-security.md) |
| Goroutine ownership, shared state, channels/locks, cancellation, bounded parallelism | [Concurrency and contexts](references/concurrency-context.md) |
| HTTP lifecycle, client reuse, deadlines, large transfers, SSE/WebSockets | [HTTP and streams](references/http-streams.md) |
| Database/Redis/broker clients, transactions, jobs, retry and recovery boundaries | [Integrations and jobs](references/integrations-jobs.md) |
| Scheduler, containers, GC/memory, profiles and measured optimization | [Runtime and performance](references/runtime-performance.md) |
| Startup/shutdown, deployment, observability, focused tests and fault verification | [Lifecycle and verification](references/lifecycle-verification.md) |
| Version-sensitive behavior, authority and research links | [Source and version register](references/sources.md) |

This skill owns Go implementation and application integration. For substantial API-contract or PostgreSQL work, use a relevant specialist skill if available; neither is required. Do not transfer another language's runtime assumptions into Go or duplicate its entire specialist guidance.

## Implement the simplest sufficient mechanism

State the root failure or required invariant and selected approach before editing. Reuse suitable packages and explicit construction; concurrency, channels, interfaces, generic repositories, extra services, and infrastructure must earn their complexity.

For each changed asynchronous boundary, determine who starts, cancels, waits, handles errors, and releases resources, plus what bounds active and waiting work. Context cancellation requests stopping; it does not join goroutines or undo completed effects. Local synchronization does not protect a durable invariant across replicas.

Keep request errors, dependency failures, cancellation, and programming failures distinguishable. Preserve compatibility and safe legitimate workflows. Identify unavoidable contract, data, or deployment migrations rather than introducing them for style. Never weaken authorization, tenant isolation, TLS, or diagnostic access to make a change easier.

## Verify and finish proportionately

Use existing scripts and focused Go checks suited to the changed behavior. Formatting, targeted tests, vet/build, race detection, integration, fuzzing, or profiling answer different questions; do not run them all automatically. Documentation-only work needs normal package validation, not an application scaffold or agent evaluation suite.

Select a realistic failure from the affected path and verify the invariant, completion, and cleanup as well as the result. Use explicit synchronization and disposable dependencies/state instead of sleeps or production disruption. A clean race-detector run only covers executed memory accesses; it does not prove ordering, deadlock freedom, idempotency, or distributed correctness.

Review the diff for leaked or unbounded work, broken ownership, compatibility, redundant abstractions, and unrelated changes. Report what changed, which checks actually ran, the evidence obtained, and genuine limitations. Do not claim performance gains or production reliability from compilation or a happy-path test alone.
