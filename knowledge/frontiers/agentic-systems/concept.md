---
id: frontiers/agentic-systems
title: Agentic Systems
band: B5
track: frontiers
tier: T4
bloom_target: apply
prerequisites: [ai-ml/llm-architectures]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-agentic-systems
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0277, S-0278, S-0279, S-0280]
review_after: 2027-02-17
---

# Agentic Systems

## Claims

### Agent loops (perceive / act / reflect)

- The canonical agent loop interleaves reasoning traces with actions: the model emits a thought, calls a tool/action, receives the observation as the next input, and reflects before the next step — ReAct's thought/action/observation alternation, which beat both reasoning-only and action-only baselines. [T1][S-0277]
- Grounding the loop in environment feedback reduces hallucination: on HotpotQA and FEVER, ReAct queried a Wikipedia API for evidence instead of relying on parametric knowledge alone, reducing hallucination and error propagation relative to chain-of-thought, and produced more interpretable trajectories. [T1][S-0277]
- Loop efficacy requires very little supervision: 1-2-shot ReAct prompting reached 71% success on ALFWorld vs 45% for action-only and 37% for imitation learning trained on ~1e5 trajectories, and ~+10 absolute points over IL/RL methods on WebShop. [T1][S-0277]

### Tool use and function calling (T4)

- Production agents are, at their core, "LLMs using tools based on environmental feedback in a loop": the agent emits structured calls to registered tools/functions, and the toolset design (names, schemas, documentation) is the main lever on reliability. [T4][S-0279]
- Workflows vs agents: workflows orchestrate LLMs through predefined code paths; agents let the LLM dynamically direct its own process and tool usage. Practitioner guidance is to start with single calls/workflows and escalate to agents only when tasks are open-ended and steps cannot be pre-specified. [T4][S-0279]
- Tool integration is consolidating around open protocols: Anthropic's 2024 guidance points to its Model Context Protocol (MCP, released Nov 2024) as the standard way to connect models to third-party tools, and major providers adopted MCP through 2025 — a fast-moving, non-consensus area. [T4][S-0279]

### Memory architectures (T4)

- Agent memory is currently built mostly as external, updatable context rather than trainable memory: RAG-style retrieval over a non-parametric index (Lewis et al.) gives the agent access to corpora that change independently of the model, and the index updates without retraining. [T1][S-0278]
- Long-horizon and episodic memory (remembering and reusing outcomes across tasks/sessions) is an open frontier: current practice relies on context engineering (getting relevant information into the window: retrieval, summarization, caching) rather than on a settled memory architecture. [T4][S-0279]

### Multi-agent patterns (T4)

- The standard multi-agent decomposition pattern is orchestrator-workers: a central LLM dynamically breaks a task into subtasks, delegates them to worker LLMs, and synthesizes their results — suited to tasks whose subtask structure cannot be predicted (e.g., multi-file coding changes). [T4][S-0279]
- The other documented patterns are parallelization (sectioning: independent subtasks in parallel; voting: several prompts on the same task with a threshold) and evaluator-optimizer loops (an LLM critic iterates on a generator's output) — all variants of "workflows" rather than free-running agents. [T4][S-0279]

### Evals for agents (T4)

- Task-level, execution-based benchmarks are the dominant evaluation method for coding agents: SWE-bench provides 2,294 real GitHub issue->PR instances across 12 Python repos, and requires the agent to edit the codebase so held-out tests pass — full task resolution, not single-edit scoring. [T1][S-0280]
- At release, frontier models resolved only a small fraction of SWE-bench (e.g., Claude 2: 1.96%): the authors concluded models handle only the simplest tasks and that earlier static benchmarks had become saturated, motivating execution-based task evaluation. [T1][S-0280]
- Agent-evaluation practice is volatile: benchmark saturation, contamination, and the gap between benchmark scores and deployed reliability are live concerns, and no single standard governs agent evaluation as of 2025-2026. [T4][S-0280]

### Agent frameworks (T4 practice)

- Frameworks reduce plumbing for standard patterns (calling models, defining/parsing tools, chaining), but add abstraction that can obscure prompts and responses and tempt over-complexity; guidance (Anthropic, 2024) is to start with direct API calls and use frameworks only when they clearly reduce complexity. [T4][S-0279]
- The framework landscape is churning: examples from late 2024 include Claude Agent SDK, Strands Agents SDK by AWS, Rivet and Vellum — expect this list to be stale quickly. [T4][S-0279]

### Reliability and safety of agents (T4)

- Ground truth per step is the primary reliability mechanism: agents should obtain environment feedback (tool results, code execution) at each step to assess progress, and pause for human feedback at checkpoints or when blocked. [T4][S-0279]
- Error compounding and autonomy risk: small errors compound over many turns, so deployment guidance is to trust agent decision-making only in appropriately limited environments, and to include stopping conditions (e.g., max steps) — free-running autonomy is not the default. [T4][S-0279]

## Details

A useful mental model: an agent = LLM + tools + a loop. The loop is the ReAct cycle (thought -> action -> observation); the tools are the agent's interface to the world (functions, APIs, retrieval); reliability comes from grounding each step in real feedback, human checkpoints, and narrow scopes. "Agents" in the frontier sense are the small minority of systems where the LLM decides the steps; most production "agentic" systems are workflows with predefined paths. Evaluation remains the weakest link: task-level execution benchmarks (SWE-bench style) are the current best practice for coding agents but are saturating, and operational properties (latency, cost, security, injection resistance) are not captured by them.

## Boundaries / common misunderstandings

- "An agent is an API call" — a single LLM call is not an agent; an agent is the loop (model + tools + environment feedback), which is what changes the failure modes and the engineering work. [T4][S-0279]
- "Autonomy means no oversight" — production agents still use checkpoints, human approval, ground-truth feedback and stopping conditions; autonomy is scoped, not total. [T4][S-0279]
- "RAG is agent memory" — retrieval gives access to external corpora (non-parametric memory); episodic memory across tasks and persistent goals is a different, unresolved problem. [T1][S-0278]
- "Multi-agent is automatically better" — orchestrator-workers helps when subtasks are unpredictable; adding agents to a simple pipeline adds cost, latency and failure modes. [T4][S-0279]
- "Benchmark pass rate = production reliability" — SWE-bench measures task resolution in a controlled execution environment; it does not measure operational properties (latency, cost, tool failure, security). [T1][S-0280]

## Volatility notes

- Dated 2026-08-18; review at 2027-02-17 or earlier if a cited source shifts.
- Function-calling APIs became a standard model capability in 2023-2024, and MCP (Nov 2024, adopted by OpenAI and others in 2025 — verified) is consolidating tool integration; both the protocol versions and the provider landscape are expected to keep moving.
- Agent evals are a moving target: SWE-bench-derived benchmarks have largely saturated by 2025-2026, and task-level suites for non-coding agents (e.g., tau-bench-style conversational benchmarks) are recent — UNVERIFIED in this pack (no record yet).
- Indirect prompt injection and other agent-specific attack surfaces are documented since 2023 but this pack carries no record for them yet — UNVERIFIED here; add at next review.
- Post-training shifts (RL-style reasoning training, 2024-2025, e.g., DeepSeek-R1, Jan 2025 — verified) change what base models agents are built on; the interaction with loop design is unsettled.
- Framework names (LangGraph, CrewAI, AutoGen, Claude Agent SDK, and successors) churn quickly; treat any framework claim as a snapshot.

## References (evidence records)

- S-0277 — Yao et al. (2023) — ReAct: thought/action/observation loops; grounding; ALFWorld/WebShop results.
- S-0278 — Lewis et al. (2020) — RAG: parametric + non-parametric memory; updatable index (shared with ai-ml/llm-architectures).
- S-0279 — Anthropic (2024) — Building Effective Agents: loops, tool use, workflows vs agents, orchestrator-workers, frameworks, reliability guidance.
- S-0280 — Jimenez et al. (2024) — SWE-bench: task-level execution-based agent evaluation; saturation motivation.
