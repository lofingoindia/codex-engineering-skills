---
name: nodejs-backend-engineering
description: Build, review, troubleshoot, or improve Node.js backend services and workers, including runtime behavior, async execution, integrations, security, and production recovery. Use for Node.js engineering decisions; skip browser JavaScript, trivial syntax edits, and database-only or API-contract-only work.
---

# Node.js Backend Engineering

Make the requested backend behavior correct under realistic concurrency, dependency failure, and process interruption. Keep the solution proportional to the application. Repository requirements and explicit user choices take precedence over these defaults.

## Establish the actual execution model

Before choosing a change, inspect the relevant entrypoint and follow one affected request, job, or subscription through its dependencies. Read applicable agent instructions, package scripts, lockfile, runtime pins, framework hooks, tests, and deployment configuration. Identify:

- The task: new behavior, focused repair, review, incident, integration, security, or measured optimization.
- Actual Node.js version/support status, package manager, JavaScript/TypeScript build path, module format, dependency versions, and platform.
- Process model: persistent service, serverless invocation, scheduled job, worker, or real-time server; replicas, resource limits, proxy and termination behavior where relevant.
- Ownership of asynchronous work, clients, connections, timers, listeners, streams, caches, authentication context, and durable state.
- The user-visible invariant or failure, affected consumers, and evidence already available.

Bound investigation to the task. Inspect installed package APIs and matching upstream documentation before relying on changing defaults or newer runtime features. Prefer supported LTS releases for production; do not turn an unrelated repair into a runtime, framework, module, or TypeScript migration.

## Load detail only when needed

Choose the relevant reference or sections; do not read the entire reference set for each request.

| Decision or symptom | Read |
| --- | --- |
| Event-loop stalls, CPU work, async errors, cancellation, excessive concurrency | [Runtime and concurrency](references/runtime-concurrency.md) |
| HTTP lifecycle, dependency timeouts, uploads/downloads, streams, SSE/WebSockets | [HTTP and streams](references/http-streams.md) |
| Database/Redis clients, caches, durable jobs, retries, cross-service effects | [Integrations and jobs](references/integrations-jobs.md) |
| Framework/module structure, TypeScript, configuration, trust boundaries, supply chain | [Language, architecture, and security](references/language-security.md) |
| Startup/shutdown, crashes, readiness, memory, observability, performance diagnosis | [Lifecycle and diagnostics](references/lifecycle-diagnostics.md) |
| Version-sensitive behavior or disputed recommendations | [Source and version register](references/sources.md), then matching upstream documentation |

This skill owns Node.js execution and application integration. For substantial API contract or PostgreSQL work, use the corresponding engineering skill if available. Neither is required: preserve the same authorization, transaction, compatibility, and durability guarantees when working independently.

## Choose and implement the smallest sound change

State the root failure or required invariant and the selected approach before editing. Compare alternatives only when the tradeoff changes correctness, complexity, or operational cost. Reuse suitable framework lifecycle hooks, validation, logging, HTTP clients, pools, queues, and test utilities.

For each relevant asynchronous boundary, establish who owns completion, failure, cancellation, capacity, and cleanup. An async function does not guarantee nonblocking execution; a timeout does not prove work stopped; a network failure does not prove a write failed. Preserve these distinctions when implementing recovery.

Keep expected request failures separate from process corruption. Make overload and unavailable dependencies produce bounded, observable behavior. Do not add worker pools, Redis, queues, clusters, circuit breakers, generic repositories, or new infrastructure without an actual requirement. Preserve compatible working behavior and public contracts; explicitly identify unavoidable migrations.

## Verify the changed behavior

Use existing scripts and focused tests suited to the change: type checking where configured, linting, unit/integration checks, build/start verification, or a bounded reproduction. Select realistic failure cases from the affected path rather than executing a universal reliability suite. Normal validation is sufficient for documentation-only changes; do not launch agent evaluations or benchmarks by default.

When relevant, verify rejection and cleanup paths as well as success: a disconnected client, slow dependency, concurrent duplicate, failed initialization, or shutdown during work. Use disposable state and fake dependencies; never exercise destructive failure tests on production. Performance claims require relevant measurements, not assumed benefits from new abstractions.

Review the diff for duplicated systems, unbounded work, leaked resources, secrets, compatibility changes, and unrelated edits. Report the resulting behavior, checks actually executed, and material limitations. Distinguish code inspection, simulated failures, and real service evidence; do not claim production readiness from a passing build alone.
