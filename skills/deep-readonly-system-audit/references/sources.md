# Audit sources and limits

Research checked **2026-10-30**. These references inform evidence-driven investigation; they do not grant permission for active security tests, fixes or infrastructure changes.

- [OWASP secure code review](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html): source-to-sink tracing, business logic, configuration, reachable paths and manual analysis beyond scanners.
- [OWASP threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html): assets, data flows, trust boundaries and risk-based selection. The audit should map the real architecture rather than impose a fixed chain.
- [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/): versioned test methodology and coverage vocabulary. The consulted project page lists 4.2 as released and 5.0 as in development; latest development content is not an automatic stable baseline. Active testing requires its own permitted environment/scope.
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/): additional review methodology context. The project is described as a lab project; prefer applicable current framework documentation and the current review cheat sheet for specific behavior.
- [NIST SSDF](https://csrc.nist.gov/projects/ssdf): risk-based development/review and evidence practices; SP 800-218 version 1.1 is identified as final on the consulted page. It is not a checklist proving readiness or a certification for this audit.
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html): ANALYZE actually executes the supplied statement and permits its side effects. A harmless-sounding diagnostic is not necessarily read-only.
- [PostgreSQL transaction access mode](https://www.postgresql.org/docs/current/sql-set-transaction.html): read-only restrictions have defined scope and exceptions; they are not a guarantee of zero external/resource effects. The consulted current docs identify PostgreSQL 18.
- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/): consumer-group reads/claims and acknowledgments change progress/ownership. Do not classify all queue inspection as read-only by command name.
- [OWASP logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html): sensitive data, provenance, coverage and purpose of evidence. Sampled operational traces and complete audit history are different guarantees.

PROVEN / STRONGLY SUPPORTED / HYPOTHESIS / UNVERIFIED are this skill's explicit reporting convention requested for these audits, not labels claimed to be standardized by the sources. Strict report-only writing and continuous checkpoints implement the user's audit boundary; third-party references cannot relax it.

The installed skill-creator/UI guidance, [Agent Skills specification](https://agentskills.io/specification), [OpenAI skills guide](https://developers.openai.com/api/docs/guides/tools-skills) and [Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) inform concise discovery and conditional references. [Evaluation guidance](https://developers.openai.com/blog/eval-skills) distinguishes actual behavioral evidence from a valid manifest. No audit-mode non-mutation result is established merely by validating this skill package.
