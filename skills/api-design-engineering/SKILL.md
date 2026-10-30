---
name: api-design-engineering
description: Design, review, implement, or troubleshoot API contracts and service communication, including authorization, compatibility, and reliability. Use for endpoint or integration engineering; skip backend work that does not affect an API boundary.
---

# API Design & Engineering

Deliver a contract consumers can use correctly and an implementation whose security, consistency, and failure behavior match that contract. Scale the work to the requested change and its consequences. Explicit user requirements take precedence over this skill's defaults.

## Establish the decision context

Identify whether the request is a new design, extension, review, targeted repair, performance investigation, migration, or communication-style decision. For a repair, follow the failing request through the affected layers; do not turn it into a general redesign.

Inspect the relevant instructions, routes/resolvers/RPC definitions, schemas, middleware, authorization, data operations, tests, and actual consumers. Check dependency and tool versions before relying on framework behavior. Read enough to establish the boundary, rather than surveying the whole repository by default. With no repository, give a concrete design using stated assumptions; do not invent existing components.

Establish the facts that affect the decision: consumer ownership and upgrade control (including mobile/offline clients), trust and tenant boundaries, sensitive side effects, consistency needs, expected workload, latency budget, and deployment constraints. Infer from evidence where possible; ask only for unresolved facts that materially change correctness or compatibility. Continue independent work while those answers are pending.

For nontrivial decisions, briefly state the root problem, the required invariant, and the selected approach with its main tradeoff. Distinguish observed facts, assumptions, and proposed behavior. Prefer a sound existing pattern. A new protocol, gateway, version, queue, cache, service, middleware layer, or dependency needs a concrete benefit that outweighs its operating and migration costs.

## Load only useful guidance

Choose references by the question being answered; do not read the entire bundle for every endpoint.

| Current decision | Read |
| --- | --- |
| HTTP methods, schemas, errors, lists, OpenAPI, consumer compatibility, deprecation | [Contracts and evolution](references/contracts.md) |
| Identity, permissions, tenant isolation, credentials, browser boundaries, untrusted input or destinations | [Security boundaries](references/security.md) |
| Duplicate effects, races, dependency failures, async acceptance, latency, caching, operational verification | [Reliability and performance](references/reliability.md) |
| Choosing communication style; GraphQL, gRPC, webhooks, events, streaming | [Protocols and integrations](references/protocols.md) |
| Verifying a standard, version, draft status, or a disputed recommendation | [Source register](references/sources.md) |

Before a major architecture/security/reliability decision or use of unfamiliar or evolving technology, verify the applicable official specification and the installed implementation's documentation. Follow the relevant links, check status/errata and tooling support, and research the uncertain point instead of conducting a broad survey every time. The references are a dated synthesis, not a substitute for current project evidence. If browsing is unavailable, disclose what remains unverified and avoid asserting a current version or draft as settled fact.

## Make the contract and implementation agree

For the affected operation, settle the observable behavior: inputs and limits, identity and permissions, outputs and errors, state transition, and retry/concurrency behavior. Include only dimensions that matter to this task. Preserve names, response shapes, status behavior, defaults, and client expectations unless changing them is necessary; an aesthetic preference is not a migration justification.

Use existing handlers, validators, persistence primitives, instrumentation, and test tools where they satisfy the invariants. Enforce access and tenant scope on every data path, including batches, async results, and caches. Put duplicate prevention and concurrent-state protection at the authoritative shared boundary; a process-local check or a transaction alone does not establish either guarantee. A timeout or cancellation does not prove a remote mutation failed.

For a design request, produce an implementable contract and explain consequential failure cases. For an implementation request, carry the focused change through the relevant contract, code, consumers/docs, and verification within the authorized scope. For a review, lead with actionable findings tied to code/contract evidence, impact, and a practical correction; distinguish confirmed defects from questions.

## Verify the consumer outcome

Choose tests from the actual risks. Alongside the ordinary request, exercise relevant permission boundaries, malformed/oversized inputs, duplicate or concurrent requests, lost responses, dependency failures, and older consumers. Use real database semantics for concurrency claims where practical; mock success does not prove atomicity. Verify negative cases leave no unauthorized side effects. Check a failed mutation's state as well as its status code.

Run the project's relevant tests, contract/schema checks, client generation/type checks, and builds when affected. Measure performance claims against a representative workload. Prefer focused regression coverage and existing tools over building a new validation framework. Contract validation cannot establish authorization or distributed-system correctness.

Finish the authorized work once meaningful checks pass; expand testing when a failure, new change, or unresolved risk warrants it. Report the decision, changes or findings, compatibility/rollout implications, executed evidence, and genuine residual uncertainty. Keep proposed tests distinct from tests actually run. For a public or independently deployed consumer change, include a viable migration and recovery path before calling it ready.
