# Evidence quality, provenance, and research limits

## Classify what a source establishes

| Evidence | What it supports; what it does not |
| --- | --- |
| Adopted specification | Requirements within the stated protocol/profile/version; not automatic implementation conformance |
| Official public API documentation | Supported behavior for its version/edition/environment; inspect compatibility and deprecations |
| Pinned source implementation | Observed behavior of that ref and path; not necessarily a stable public contract or installed release |
| Upstream/local tests | Behavior asserted under their setup; distinguish reading from execution and coverage from completeness |
| Issues and PRs | Reports, rationale and changes with specific lifecycle state; neither a universal bug nor automatic released fix |
| First-party production case study | A team's observations under its historical workload, topology and constraints; not your benchmark result |
| Research paper | Evidence under its methods/datasets/assumptions; not a guarantee on this product's users or corpus |
| Educational example/curated collection/opinion | Discovery and possible explanations; follow original evidence before a material decision |

Evaluate relevance, version fit and direct support rather than counting domains. Multiple summaries of one article are not independent confirmation. A recent marketing post is not necessarily stronger than an older applicable specification. Check publication and event dates, stable versus draft status, and documented limitations.

## Resolve a disagreement

First compare versions, configuration, workload, isolation/durability guarantees, platforms and measurement definitions. Two different conditions can make apparently conflicting observations both true. For actual library behavior, inspect the target ref and relevant tests; for a supported contract, consult release documentation/maintainer clarification. For performance, a local measurement may still be required.

Separate observed fact from the inference that it improves this codebase. Compare the current system with the candidate on correctness as well as speed/cost. Fewer queries, files, tools or tokens do not automatically mean a better outcome. If the sources cannot settle a load-bearing fact, state the uncertainty and the focused check that would resolve it.

Avoid fabricating precision: do not invent throughput, release versions, supported options, license permissions or exploitability from a general article. Cite the exact page/section or commit/file near the supported claim, noting an inference where relevant. Search snippets and inaccessible URLs do not count as read evidence.

## Keep the source index maintainable

The domain indexes were assembled on **2026-10-30**. Selected official documentation and primary articles were checked in this session or preceding skill research; inspected implementation examples have commit permalinks. Other listed sources remain discovery seeds, not audited recommendations. Recheck all suitability/maintenance/license facts when actually adopting them. Do not pin a future project to a snapshot simply because it appears here.

Useful sources were recovered from earlier attachment excerpts covering PostgreSQL/backend case studies and custom agent/MCP engineering. The complete original 51-resource collection and both full original research documents were not independently located. Their project-specific instructions are not universal rules; retained sources were checked independently where used.

Known discovery corrections: mini-swe-agent's root `LICENSE` fetch returned 404; its manifest identified `LICENSE.md`, which was read as MIT. A current LangGraph durable-execution URL redirected to persistence documentation; follow the active documentation and actual checkpoint/replay semantics rather than assuming an old URL defines an API. Anthropic's 2024 agent article now explicitly notes that tooling has evolved. These are reasons to verify, not to reject the broader engineering lessons.

No repository code or tests were executed while assembling this index, and no production-workload or with/without-skill result is implied. Source inspection is distinct from behavioral skill evaluation.

## Skill-design provenance

The installed skill-creator and UI metadata guidance, [Agent Skills specification](https://agentskills.io/specification), [OpenAI skills guide](https://developers.openai.com/api/docs/guides/tools-skills), and [GPT-6 Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) support conditional loading and precise activation. [Evaluation guidance](https://developers.openai.com/blog/eval-skills) distinguishes structural validation from improved agent behavior. This skill adds no required research service, script or companion skill.
