# Language, architecture, and security boundaries

Use for module/build behavior, framework organization, configuration, application hardening, or dependency risk. Preserve the existing stack unless a concrete requirement justifies changing it.

## Keep architecture and language choices practical

Trace the actual feature before adding layers. Separate transport/framework handling, business rules, and external effects only as much as reuse, testing, or complexity warrants. A small service may need straightforward modules rather than controllers/services/repositories/DI for every operation. Avoid parallel validation, configuration, HTTP, logging, or error systems.

Respect framework lifecycle and error propagation. Express 4, Express 5, Fastify, Nest, Hono, and custom servers differ; inspect the installed version's Promise, hook, context, and shutdown semantics. Errors from timers/EventEmitters do not necessarily reach an HTTP error handler. Do not send a response and continue mutating state unintentionally. Preserve causal errors internally while returning the established safe public error shape.

Check `package.json` scripts, `type`, `exports`, file extensions, loader, build output, and deployment entrypoint. CommonJS and ESM interoperation is version-sensitive. Avoid an application-wide module conversion to fix one import. Verify emitted specifiers and assets work when starting the built artifact, not just under a development runner.

TypeScript types disappear at runtime. Validate untrusted inputs and dependency responses at the relevant boundary using the existing validation system. Node.js native TypeScript stripping is version-dependent, does not type-check, and does not apply `tsconfig` transformations or path aliases. Non-erasable syntax or the project's build needs may require its existing compiler/transpiler. Do not replace a working build pipeline merely because native execution exists.

Validate required configuration at startup and distinguish absent, empty, malformed, and explicitly disabled values. Avoid coercion bugs such as treating the string `"false"` as a disabled feature. Keep test configuration local; do not modify global environment or import-time singletons unnecessarily. Public browser configuration and server secrets require different handling.

## Protect actual trust boundaries

Authentication establishes identity; authorization must enforce the operation, resource, and tenant on the server. Never trust a tenant ID, role, forwarded address, queue payload, or internal-looking request solely because it arrived through a familiar code path. AsyncLocalStorage can carry validated context for convenience but is not an authorization mechanism.

Reuse a sound authentication/session system. Verify credential scope, expiry/revocation, audience/issuer as applicable, and safe forwarding. Cookie authentication needs its applicable CSRF defenses; CORS is not access control. A shared service key does not automatically provide object-level authorization. Never log tokens, cookies, connection strings, or private payloads as diagnostic context.

Apply defenses to the input's eventual use:

| Boundary | Engineering consequence |
| --- | --- |
| Request/query/body parsing | Bound byte size, nesting, field count, decompressed size, and expensive validation work where relevant; validate domain values as well as syntax |
| SQL and other query languages | Use supported parameterization; allowlist structural identifiers/operators that cannot be bound as values |
| Object merging/dynamic keys | Avoid unsafe recursive merges and assignment of attacker-controlled prototype keys; use allowlisted fields and appropriate dictionary structures |
| Process execution | Prefer argument-array APIs without a shell; validate executable, options, paths, and argument interpretation. Shell-free execution does not prevent argument injection |
| File paths/uploads | Resolve against an allowed root and consider separators, symlinks, races, and permissions; a naive string prefix is insufficient |
| Outbound URLs | Restrict destinations/protocols and re-evaluate redirects, resolved addresses, and credential forwarding; use network controls where warranted |
| Regex, JSON, compression, serialization | Large/adversarial work can block the event loop even inside an async handler; use limits and safer algorithms rather than relying on a timer to interrupt synchronous work |

Inspect HTTP proxy/parser agreement and trusted-proxy configuration. Do not enable permissive/insecure parsing to work around malformed requests; request smuggling crosses server/proxy boundaries. Scope public error messages while preserving useful internal correlation.

Node.js's permission model can restrict trusted code's accidental resource access. It is not a sandbox against malicious dependencies/code, and capabilities differ by version. Worker threads likewise share a process trust boundary. Use OS/container isolation and least privilege when hostile execution is part of the product. Keep the runtime inspector and diagnostic endpoints off public interfaces.

## Supply chain and runtime updates

Use the repository's package manager and committed lockfile. For npm CI, `npm ci` enforces manifest/lock consistency; it may still execute package lifecycle scripts. Review script permissions and provenance according to project policy. Disabling every install script blindly can break native dependencies; determine what is required in an isolated build context.

Triage advisories against installed versions, exposure, and supported fixes. An audit with no findings is not a security guarantee; `audit fix --force` can introduce incompatible upgrades. Prefer a focused reviewed update with relevant checks over regenerating the whole dependency tree. Check runtime/security support and framework/driver compatibility before upgrades, including native add-ons and container base images.

For a security repair, verify the exploit boundary and legitimate workflow in focused tests. Do not turn ordinary backend work into an unsolicited full audit or impose a new authentication platform without need.
