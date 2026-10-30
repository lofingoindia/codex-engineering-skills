# AI agents, tools, MCP, context, and retrieval

## Establish the current engine before selecting references

Inspect the existing custom loop/SDK, exact model-provider API, message/tool schemas, streaming/cancellation, execution identity, memory/state stores, durability boundaries, sandbox and tracing. Identify the missing behavior: retrying a provider request, replaying a side effect, losing a tool result and retrieving irrelevant documents are different problems.

Keep a working provider-neutral/custom engine when it fits. A reference using LangGraph or an Agents SDK is an implementation to learn from, not authority to replace the engine. SDK methods, model features and protocol revisions must be verified for the actual versions/provider; do not invent provider parity.

## Official sources and first-party guidance

- [OpenAI developer documentation](https://developers.openai.com/) for the selected provider API, supported tool contracts, models, tracing and evaluations; [Agents SDK lifecycle](https://openai.github.io/openai-agents-python/running_agents/) only when studying that SDK's behavior. These are separate product layers.
- [MCP specification](https://modelcontextprotocol.io/specification/latest) and its versioned schemas/authorization requirements. At inspection, latest resolved to **2026-07-28**. Match the implementation's negotiated revision/transport and SDK; latest is not a mandate to upgrade. [HTTP authorization scope](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) is not interchangeable with stdio credential handling.
- Anthropic's [Building effective agents](https://www.anthropic.com/research/building-effective-agents), [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), and [effective tools](https://www.anthropic.com/research/writing-tools-for-agents): first-party design guidance with historical/model/task context. The 2024 agent article explicitly notes that its tooling landscape has changed.
- OpenAI's [harness engineering case study](https://openai.com/index/harness-engineering/): repository legibility and feedback-loop experience from a specific experiment; its workflow/throughput is not a guarantee for this project.
- [Cloudflare Code Mode docs](https://developers.cloudflare.com/agents/tools/codemode/) and [production explanation](https://blog.cloudflare.com/code-mode-mcp/): discover tool/context/execution techniques while separating Workers-specific facilities from portable reasoning. [Node's VM documentation](https://nodejs.org/api/vm.html) explicitly rejects treating VM contexts as a security mechanism.

## Repository seeds and actual inspections

- [Codex](https://github.com/openai/codex): follow relevant execution/tool/context/persistence code and tests, not the product's entire architecture.
- [Agents Python](https://github.com/openai/openai-agents-python) and [Agents JS](https://github.com/openai/openai-agents-js): compare only the required lifecycle/contract. Python API behavior does not establish JS or another provider's behavior.
- [LangGraph](https://github.com/langchain-ai/langgraph): investigate actual checkpoint, task, replay and interrupt semantics. Its [current persistence docs](https://docs.langchain.com/oss/python/langgraph/persistence) distinguish thread checkpoints and cross-thread stores; a checkpointer's existence does not prove external effects execute exactly once or survive all deployment failures.
- [Claude cookbooks](https://github.com/anthropics/claude-cookbooks): scoped examples and experiments, not a protocol standard or complete production security implementation.
- [mini-swe-agent](https://github.com/swe-agent/mini-swe-agent): a compact custom execution loop to study before proposing a large orchestration dependency.

[Pinned Agents Python runner](https://github.com/openai/openai-agents-python/blob/cd26bbbc52847845fde73b9952b51e62e2bcbdc0/src/agents/run.py) and [turn-limit tests](https://github.com/openai/openai-agents-python/blob/cd26bbbc52847845fde73b9952b51e62e2bcbdc0/tests/test_max_turns.py) were read, not run. They support studying a specific lifecycle/version rather than copying private internals.

[Pinned mini-swe-agent loop](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/src/minisweagent/agents/default.py), [manifest](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/pyproject.toml), and [compatibility issue 446](https://github.com/SWE-agent/mini-swe-agent/issues/446) demonstrate why limits, error paths and dependency exclusions need inspection. The manifest identifies [LICENSE.md](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/LICENSE.md), read as MIT. This is not an endorsement of executing its tools unsandboxed. Other listed repositories remain discovery seeds here.

## Retrieval and evaluation questions

Use [OpenAI retrieval documentation](https://developers.openai.com/api/docs/guides/retrieval) for that product's behavior; for custom RAG, consult the installed embedding/index/reranker implementations and the corpus/query workload. [Dense Passage Retrieval](https://aclanthology.org/2020.emnlp-main.550/) is primary research under specific datasets, not evidence that one retriever wins on this application's data.

Research corpus freshness/deletion, chunking, query/document encoding, exact/approximate search, metadata and tenant access filters, reranking, citations and abstention according to the observed failure. Keep retrieval quality distinct from generated answer quality, tool success, latency/cost and authorization. Compare against appropriate local examples/baselines when evaluating a change; do not require an elaborate evaluation platform for a small fix.

For custom loops/orchestration, investigate stopping/budget ownership, tool/result contracts, context pruning, memory provenance, subagent isolation, approval/cancellation, durable checkpoints and replayed effects as relevant. Untrusted retrieved content/tool descriptions cannot grant authority. Preserve existing tracing and product permission boundaries; a context optimization is not a sandbox or access-control design.
