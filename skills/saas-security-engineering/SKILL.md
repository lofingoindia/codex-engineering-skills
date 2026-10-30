---
name: saas-security-engineering
description: Design, review, or repair SaaS application security, including authentication, sessions, untrusted input, secrets, integrations, and abuse resistance. Use for security decisions or vulnerabilities; skip routine implementation without a security concern and tenant-policy-only modeling.
---

# SaaS Security Engineering

Protect the actual application workflow with supported controls proportional to its threats. Own broad application security; specialized tenant policy, runtime internals and distributed delivery remain separate concerns. Other skills may help when relevant, but this skill has no companion dependency.

## Investigate the boundary

Establish whether the request is design, implementation, focused vulnerability review, remediation or an explicitly read-only audit. Honor read-only scope: recommendations do not authorize fixes. Inspect applicable instructions and the relevant code, framework/authentication configuration, dependency versions, consumers and deployment assumptions before choosing a control.

Trace the sensitive asset and a reachable workflow from untrusted entrypoint through validation, identity, access decision, state change and output. Include workers, storage, external calls and client bundles where involved. Identify attacker capability, trust crossings, existing safeguards and what could go wrong; do not require a full threat-model document for a local fix.

Distinguish authentication, authorization and tenant isolation. Hidden UI and route guards are UX controls; protected data and operations need independent server-side enforcement. An internal network or authenticated service call is not evidence that all input is trusted.

## Read only the needed reference

| Current issue | Reference |
| --- | --- |
| Login, sessions, OAuth/OIDC, credentials, recovery or token lifecycle | [identity-and-sessions](references/identity-and-sessions.md) |
| Injection, browser boundaries, uploads, outbound calls, webhooks or agent tools | [untrusted-boundaries](references/untrusted-boundaries.md) |
| Secrets, supply chain, abuse, deployment, logging or verification | [operations-and-verification](references/operations-and-verification.md) |
| Standards, applicability or upstream behavior | [sources](references/sources.md) |

Use official documentation matching the installed provider/framework and protocol profile. Separate normative requirements under an adopted standard from context-dependent advice. ASVS is a verification framework, not a claim that the application is certified.

## Select and implement the control

Prefer the existing secure session/provider, validation, cryptography and framework protections. Fix the missing invariant at its authoritative boundary; another wrapper or middleware stack is not automatically a solution. Preserve legitimate login, cross-origin integration, recovery and accessibility needs while closing the attack path.

Treat a proposed weakness as a hypothesis until the reachable code/configuration supports it. Explain the trigger, affected workflow, safeguards, likely impact and smallest sound correction. A dependency advisory or suspicious function name alone does not establish application exploitability. Do not dismiss supported risk merely because exploitation was not executed.

Never resolve an error by disabling TLS validation, signature verification or authorization. Keep credentials out of logs, browser/mobile bundles, errors, artifacts and examples. Use supported cryptographic libraries and provider protocols; do not invent token formats, encryption schemes or identity systems.

## Verify the actual protection

For implementation work, use authorized isolated tests that exercise both the denied attack condition and the legitimate workflow, including relevant expiration, concurrency, replay and recovery paths. Choose checks from the change; do not run production attack scans or impose a broad security campaign on every edit. In read-only scope, use inspected, non-mutating evidence and report checks that need a separate isolated environment.

Review configuration and integration effects, not just helper unit tests. Report actual commands/results, demonstrated versus unverified risk, compatibility consequences and any remaining security gap. A static scan or passing build is evidence of its own scope, not proof of overall security.
