# Security operations and practical verification

## Secrets and deployment trust

Inspect how secrets enter each process and who can read/use them. Prefer the existing supported secret store, workload identity and least-privilege service credentials. Separate environments and purposes; a database migration role need not be the normal app role. Secure bootstrap credentials as well as downstream secrets.

Plan rotation across issuers, verifiers, caches and consumers with a controlled overlap when needed. Exposure requires assessment, revocation/replacement and removal from accessible artifacts/history according to the incident plan; editing the latest source file alone does not invalidate a leaked secret. Do not print secret values to prove that configuration exists.

Use supported TLS validation and trusted endpoints. Inspect proxy trust, allowed hosts, production/debug flags, management interfaces, process/container capabilities, network exposure and filesystem permissions relevant to the application. Reuse supported deployment mechanisms; do not impose a new platform or certificate-pinning scheme without a matching threat model and operational recovery plan.

## Supply chain and abuse

Inspect the actual resolved versions, lockfiles, transitive paths and reachable use when evaluating advisories. Prefer supported fixes with focused compatibility checks. A scanner finding is a lead; a clean scan does not establish secure business logic. Avoid executing untrusted package scripts or fetching arbitrary tools through an unpinned command during an investigation. Preserve reproducible builds and existing provenance/update practices rather than generating a second dependency system.

Protect resource consumption at its expensive boundaries: input/payload size, pagination, query complexity, upload processing, concurrency, paid-provider calls, storage and queue backlog. Use quotas and admission controls where needed, with actionable errors and appropriate recovery. Do not let retries or CAPTCHA/lockout policies amplify denial of service for legitimate customers.

## Security evidence and incidents

Use existing structured logging for authentication failures, credential lifecycle, privilege-sensitive actions and security-relevant state transitions. Record enough actor, target, tenant, action, outcome and correlation context to investigate without logging passwords, tokens, private keys or unnecessary personal data. Bound and sanitize attacker-supplied log fields. Access control, retention and integrity of audit records matter as much as log creation.

Security events, business audit history and sampled debug traces have different coverage guarantees. Do not claim a complete audit trail from sampled telemetry. Define meaningful alerts and response ownership with the existing system. During an incident, preserve relevant evidence and follow authorized containment/recovery; a security finding does not authorize destructive production actions.

## Choose focused verification

For a real implementation change, derive tests from the missing invariant and its legitimate counterpart. Examples are decision prompts, not a suite to run automatically:

| Changed boundary | Useful evidence |
| --- | --- |
| Session/credential lifecycle | Valid login/recovery works; fixation, expiry, revocation and concurrent refresh cannot restore forbidden access |
| Input/output | Payload reaches the intended validator/encoder; malformed input fails safely and legitimate content remains usable |
| Upload/outbound integration | Allowed file/destination works; relevant traversal, redirect, spoofed type or resource limit is rejected |
| Signed event | Correct signed bytes succeed; tampering/replay cannot duplicate protected business effects |
| Dependency/configuration | Effective deployed version/settings fix the affected path without breaking supported clients |

Use isolated authorized data and inspect test setup/teardown before running it. Do not attack production or perform broad load/credential tests without scope. In explicitly read-only work, tests that write fixtures, contact services, run lifecycle hooks or update caches need a separate authorized environment; inspect evidence instead.

Report trigger and impact, exact inspected code/configuration, existing safeguards, proposed/final correction and what was actually verified. Separate proven behavior, supported risk and unresolved hypotheses. Document a meaningful remaining gap rather than asserting “secure” from a build or regex scan. Keep remediation proportional and preserve legitimate workflows.
