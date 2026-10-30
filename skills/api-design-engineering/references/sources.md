# Authoritative sources and decision record

Checked 2026-10-30. This is a source map and original engineering synthesis, not copied standards text. Recheck the linked authority, errata, implementation versions, and tool support when a decision depends on them. The dated versions below are research evidence, not permanent version pins.

## Skill engineering

| Source | Status / retained decision |
| --- | --- |
| Bundled `skill-creator/SKILL.md` (inspected locally) | Local authoring workflow used; use bundled validation, precise scope, progressive disclosure, independent forward testing |
| [GPT-6 Astra skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | OpenAI model guidance, 2026-09-11; concise activation and outcome-focused instructions rather than exhaustive recipes |
| [Skills API guide](https://developers.openai.com/api/docs/guides/tools-skills) | OpenAI product docs; name/description discovery, on-demand body/resources; hosted upload is separate from local installation |
| [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills) | Current product docs list user `~/.agents/skills`; local creator defaults to `~/.codex/skills`. Verify actual host discovery; keep one installation |
| [Agent Skills specification](https://agentskills.io/specification) | Open format; folder/name agreement, required nonempty name/description, relative resources; optional host metadata is not a portable requirement |
| [Skill eval guidance](https://developers.openai.com/blog/eval-skills) | OpenAI engineering guidance; explicit/implicit/negative cases, captured traces, artifact and rubric checks. Check installed CLI flags rather than copying old examples |

The creator entry records authoring provenance, not a runtime dependency; this skill requires no other skill or external connector.

## Specifications and security baselines

| Source | Publication status / application |
| --- | --- |
| [OpenAPI publication index](https://spec.openapis.org/oas/) and [3.2.1](https://spec.openapis.org/oas/v3.2.1.html) | OAI specification; latest listed 3.2.1 (2026-09-10), also 3.1.2 and 3.0.4. Use the project's supported dialect/toolchain |
| [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) | Internet Standard HTTP semantics; replaces the older split semantics/conditional RFCs including 7231/7232 |
| [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html) | Internet Standard caching; replaces 7234 |
| [RFC 5789](https://www.rfc-editor.org/rfc/rfc5789.html), [7396](https://www.rfc-editor.org/rfc/rfc7396.html), [6902](https://www.rfc-editor.org/rfc/rfc6902.html) | Standards Track PATCH, Merge Patch (supersedes 7386), JSON Patch; define actual patch media/atomicity semantics |
| [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) | Standards Track Problem Details; supersedes 7807, does not mandate replacement of all existing error formats |
| [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html) | Standards Track additional codes including 428/429; rate metadata is a separate contract |
| [RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html), [RFC 8594](https://www.rfc-editor.org/rfc/rfc8594.html) | Standards Track Deprecation versus Informational Sunset; different lifecycle meanings and date syntax |
| [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700) | OAuth Security BCP 240, January 2025; updates 6749/6750/6819; authentication/authorization still require application checks |
| [OIDC Core 1.0, errata set 2](https://openid.net/specs/openid-connect-core-1_0.html) | OpenID Final specification; authentication and ID token validation |
| [OAuth 2.1](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) | Active Internet-Draft -16, updated 2026-09-02; do not describe as a final RFC |
| [Idempotency-Key](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/) | Active Internet-Draft -08, updated 2026-10-22; deployed conventions can differ |
| [RateLimit fields](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/) | Active Internet-Draft -11, updated 2026-05-23; distinguish proposal from vendor X-RateLimit conventions and Retry-After |
| [GraphQL versions](https://spec.graphql.org/) / [September 2025](https://spec.graphql.org/September2025/) | Latest listed release September 2025; 2026 working draft is prerelease. Core execution is distinct from HTTP transport |
| [OpenTelemetry HTTP](https://opentelemetry.io/docs/specs/semconv/http/) / [spans](https://opentelemetry.io/docs/specs/semconv/http/http-spans/) | Project semantic conventions, site 1.44.0; stability varies by attribute and instrumentation |

## Production guidance: apply by context

| Primary source | Retained judgment |
| --- | --- |
| Google [AIP-136](https://google.aip.dev/136), [134](https://google.aip.dev/134), [151](https://google.aip.dev/151), [158](https://google.aip.dev/158), [180](https://google.aip.dev/180) | Approved Google guidance: purposeful actions, field-mask update patterns, observable long-running work, page-token behavior, source/wire/semantic compatibility; Google-specific syntax is optional elsewhere |
| Azure [design](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design), [implementation](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-implementation) | Engineering recommendations across resource design, version alternatives, bounded work, request processing and operations; examples do not mandate Azure or .NET |
| [Zalando API/event guidelines](https://opensource.zalando.com/restful-api-guidelines/) | Organization rules: useful consistency and evolution guidance; its MUST casing, media-versioning, null and batch conventions are not universal standards |
| Stripe [idempotency](https://docs.stripe.com/api/idempotent_requests), [webhooks](https://docs.stripe.com/webhooks) | Provider-specific contracts: v1/v2 idempotency differs; raw-body signatures, duplicate/unordered delivery and recovery |
| [OWASP API Top 10](https://api-security.owasp.org/), [2023 risks](https://api-security.owasp.org/editions/2023/en/0x11-t10/) | Latest edition listed by the project is 2023; threat taxonomy, not a normative API protocol or exhaustive security assessment |
| OWASP [REST security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html), [authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [SSRF](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | Security engineering guidance; choose controls for the actual browser/trust/egress boundary and preserve legitimate workflows |
| AWS [timeouts/retries](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), [transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) | Production engineering patterns; avoid retry amplification and uncertain duplicate effects, address dual writes only when durable cross-system propagation is required |
| [PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | Database implementation docs, current stable page 18 during research; illustrates why a transaction is not enough. Use installed database/version docs in actual projects |
| GraphQL [security](https://graphql.org/learn/security/) | Project operational guidance: query cost/breadth/batching, authorization and practical introspection policy |
| gRPC [deadlines](https://grpc.io/docs/guides/deadlines/), [retries](https://grpc.io/docs/guides/retry/), [Protobuf evolution](https://protobuf.dev/programming-guides/proto3/#updating) | Official implementation guidance; language/runtime and binary/JSON distinctions matter |

## Resolve conflicting advice

- **Casing, actions, envelopes, batch status:** preserve sound local contracts; use consumer ergonomics and operation semantics to choose. Do not import all of Google's or Zalando's rules.
- **Versioning:** Azure presents several approaches; Zalando prefers media negotiation. Choose for upgrade control, routing, cache variation, and support burden; compatible evolution may need no new version.
- **Null/update rules:** a company's absent/null convention cannot override the semantics of a selected patch media type. Document domain meaning and use an appropriate representation.
- **Contract-first versus generated contracts:** choose for coordination and existing tooling, then verify drift and actual clients either way.
- **Newest versus supported:** specification publication and production tool support are separate facts. Preserve a supported earlier version unless an upgrade benefit justifies migration.
- **Security versus compatibility:** preserve legitimate access patterns while closing authorization defects; never retain a vulnerability solely because a client exploited it.
