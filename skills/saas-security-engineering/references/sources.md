# Sources and applicability

Research checked **2026-10-30**. Consult current official documentation matching installed frameworks, identity providers and protocol profiles. These sources support focused decisions; loading all of them is unnecessary.

## Verification frameworks and identity standards

- [OWASP ASVS](https://asvs.owasp.org/): published 5.0.0 baseline observed; select applicable verification requirements and version identifiers, not an unqualified compliance claim.
- [NIST SP 800-63-4 final](https://csrc.nist.gov/pubs/sp/800/63/4/final) and [SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html): identity assurance, authenticators, recovery and usable credential policy. Normative requirements apply within their adopted scope, not automatically to every SaaS product.
- [OAuth security BCP, RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700): current applicable protections beyond original OAuth 2.0, including refresh-token replay protection.
- [OpenID Connect Core 1.0, errata set 2](https://openid.net/specs/openid-connect-core-1_0.html): identity/token roles and validation requirements.
- [JWT BCP, RFC 8725](https://datatracker.ietf.org/doc/html/rfc8725): algorithm, key, audience and token-confusion risks; a token profile still determines required validation.
- [OWASP MASVS](https://mas.owasp.org/MASVS/): native storage, platform and network boundaries; client hardening cannot replace backend authorization.

## Application guidance

- [Threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html), [authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html), and [session management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html): risk/context selection and credential lifecycle. Cookie strictness and assurance controls need workflow-aware tradeoffs.
- [CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [SSRF](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html), and [file uploads](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html): trusted-destination versus arbitrary-URL cases, browser ambient credentials, content processing and layered controls.
- [OWASP API Security](https://owasp.org/www-project-api-security/): the published Top 10 2023 highlights object/property/function authorization, consumption and sensitive workflow abuse. A risk list is not a complete verification standard.
- [Secrets management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html), [logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), and [secure code review](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html): lifecycle, safe evidence and source-to-sink/business-flow review.
- [AI agent security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html): untrusted context, scoped tools and high-impact action boundaries; these are application controls, not a prompt-only defense.
- [NIST SSDF](https://csrc.nist.gov/projects/ssdf): risk-based secure development; the consulted page identifies SP 800-218 version 1.1 as final. Verify publication status before adopting a revision.

## Skill engineering

The installed skill-creator and UI metadata guidance, [Agent Skills specification](https://agentskills.io/specification), [OpenAI skills guide](https://developers.openai.com/api/docs/guides/tools-skills), and [GPT-6 Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) informed discovery, concise routing and proportional instruction scope. [Evaluation guidance](https://developers.openai.com/blog/eval-skills) distinguishes structural validity from behavioral evidence; no evaluation results follow merely from citing it.
