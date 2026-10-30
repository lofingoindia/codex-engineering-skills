# Idiomatic implementation and security boundaries

Use for package design, errors, representation, configuration, module changes, or an actual security boundary. Inspect existing conventions and the project's minimum Go version first.

## Structure around real responsibilities

Prefer cohesive packages, explicit construction and visible dependency direction. Reuse established application layers when they work; a small handler/service does not require a generic repository, DI container, interface for every type, or universal `cmd/internal/pkg` tree. `internal` enforces an import boundary; folder names alone do not establish architectural quality.

Define small interfaces where a consumer actually needs an interchangeable behavior. Accept existing useful abstractions such as `io.Reader`; do not wrap the whole driver or framework just for hypothetical tests. Generics should remove meaningful repeated logic while keeping semantics understandable. Preserve APIs and package import paths during focused repairs.

Classify errors through supported `errors.Is`/`errors.As`, wrapping, or suitable newer typed helpers when the minimum version permits. Preserve meaningful causes without exposing low-level credentials/private data. Wrapping makes a cause inspectable to callers, so consider API compatibility. Avoid error-string matching, logging and returning the same failure at every layer, or panic for ordinary validation/dependency errors. Watch typed-nil interfaces and variable shadowing that hides a failure.

Choose receiver/value/pointer semantics from identity, mutation and copying cost. Do not copy synchronization-bearing structs after use. A copied slice/map or shallow clone can still alias mutable data. Preserve nil/empty, omitted/zero, numeric precision and time/JSON representations when consumers distinguish them. A stylistic change can be an API break.

Validate required configuration in owned startup code and distinguish absent, malformed and intentionally disabled values. Keep shared mutable package globals and import-time side effects to what the architecture actually needs. Avoid process exits inside reusable packages; let the owner perform cleanup and choose termination.

## Protect trust and tenant boundaries

Enforce authorization at sensitive server reads/mutations, independently of UI checks. Authenticate callers, then validate current resource/tenant/operation permission. Context values may carry verified identity but are not proof that a caller-supplied tenant ID is authorized. Shared caches, deduplication keys, pooled session settings and logs must respect visibility and revocation requirements.

Reuse sound session/token middleware and backend policies. Secure cookies need applicable CSRF controls; CORS is not authorization. Supported standard-library cross-origin protection can help where its contract fits, but does not authenticate non-browser callers or make state-changing GETs safe. Validate redirect destinations, trusted proxy/address handling, token scope/lifetime and credential forwarding for the existing deployment.

Apply defenses at the eventual use of input:

| Boundary | Relevant Go-side decision |
| --- | --- |
| SQL | Use driver-supported parameters; allowlist structural identifiers/operators that cannot be parameters |
| JSON/parsers | Bound input/work, validate domain values and expected document structure. Unknown fields, duplicate keys, case matching, trailing values and numeric conversions depend on decoder/version/contract |
| Files/uploads/archives | Restrict to intended destinations and consider symlinks, TOCTOU, platform names and permissions. Lexical cleaning or string prefixes alone are insufficient. Use supported traversal-resistant APIs such as `os.Root` when appropriate, with documented platform/security limits |
| Commands | `exec.Command` does not invoke a shell by default; retain argument-array execution and validate executable/options/paths. Argument injection and subprocess descendants still need consideration |
| Outbound networking | Validate destination, resolved address, redirects, protocols and credential scope. SSRF protection needs a coherent dial/redirect/network policy, not merely a URL regex |
| TLS/randomness/templates | Keep certificate verification; use established cryptographic APIs and `crypto/rand` for security material. Preserve context-appropriate escaping rather than marking untrusted template content safe |

Use size/time/concurrency limits against resource exhaustion without breaking legitimate streaming/uploads. Never expose debug/pprof endpoints or sensitive reports unintentionally. Prefer least privilege; `unsafe`, cgo or runtime internals require a demonstrated need and do not provide an isolation boundary.

## Modules and current tooling

Inspect `go.mod`, `go.sum`, workspace replacements, vendoring, build tags, tool dependencies and CI image/toolchain. The `go` directive and selected toolchain have different roles; auto toolchain selection can download a compiler. Keep changes scoped and reproducible, and review generated module diffs rather than casually tidying/upgrading the whole graph.

Module hashes/checksum verification detect integrity changes, not malicious logic or known vulnerabilities. Respect private-module proxy/checksum settings without disabling verification globally or exposing private names/credentials. Use available `govulncheck` for relevant security/dependency work and triage reachable known findings against the actual build; a clean result is not proof of complete security. Machine-readable scan modes can exit successfully despite findings; inspect the mode and report rather than relying on the exit code alone.

Current JSON v2 and newer language/library APIs have compatibility/default differences. Preserve a working v1 encoding contract unless a deliberate change justifies migration; do not copy experimental examples or a newer API into an older minimum-version project. Verify the denied case and legitimate workflow for an actual security change.
