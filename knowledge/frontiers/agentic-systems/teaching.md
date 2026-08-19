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

# Agentic Systems — teaching

## Learning objectives (Bloom)

At the end of this topic the learner can (apply level; target = apply):

- Build a minimal agent loop (thought -> action -> observation) around an LLM and one or two tools.
- Decide, for a given task, whether to use a single call, a workflow, or an agent, and justify the choice.
- Add a RAG-style retrieval memory and explain what it does and does not provide.
- Choose and apply the relevant pattern (orchestrator-workers, parallelization, evaluator-optimizer) to a task description.
- Design a basic evaluation plan for an agent and state its limitations; identify the main reliability mechanisms (ground truth per step, checkpoints, stopping conditions).

## Worked example

Worked example — a minimal customer-support agent, built and reasoned through step by step.

Goal: answer "What are our refund rules for a 30-day-old subscription?" from company docs.

1. Choose the form. Steps are not pre-specifiable (questions vary), but the action surface is tiny and reversible (read-only). Verdict: a single agent loop, not a workflow (a workflow would be fine if every question were a fixed pipeline; it is not). No framework — direct API calls are enough.
2. Define tools. One tool: `retrieve(query, k=3)` over the company doc index (RAG-style, non-parametric memory — docs can change without retraining). Keep the tool schema minimal: name, description, JSON args. This is the main reliability lever: a precise description reduces wrong calls.
3. The loop (ReAct-style): user question -> LLM emits {thought: "need refund policy from docs", action: retrieve("refund policy subscription 30 days")} -> tool returns 3 passages -> LLM emits {thought: "the docs say refunds apply within 14 days; 30 days is outside", action: finish(answer with citation)}.
4. Reliability mechanisms: ground truth per step (the answer is conditioned on retrieved passages, not memory); read-only scope (no dangerous actions, so no approval gate needed); stopping condition (max 3 loop iterations, then fallback "ask a human").
5. Failure analysis: if retrieval returns nothing relevant, the agent must say so (grounding prevents confident hallucination); if the question needs account data, the loop terminates into a human handoff rather than guessing.

Contrast: if the task were "generate the same refund letter from a fixed template every time", the answer would be a workflow or even a single call — not an agent.

## Elaboration prompts

- "Where exactly does the observation enter the model's context, and what could go wrong if it does not (stale reasoning)?"
- "What changes in failure mode when you go from one LLM call to a 10-step loop? Which reliability mechanisms exist precisely because of that change?"
- "Orchestrator-workers vs parallelization: both delegate. What is the deciding property of the task?"
- "Why does updating a RAG index not require retraining, and when would that advantage disappear?"
- "What does SWE-bench not measure, and how would you measure the missing part before deployment?"

## Common misconceptions

- "An agent is just an LLM with a system prompt." The system prompt is static; an agent is a loop with tool actions and environment feedback — the loop, not the prompt, is what grounds and extends the model.
- "More autonomy is better." Free-running agents compound small errors over turns; production practice adds checkpoints, scoped tools, ground truth per step, and stopping conditions. Autonomy is a scope decision, not a capability badge.
- "Retrieval = memory solved." RAG gives access to updatable external corpora (non-parametric memory); episodic memory (what this agent did last session) and long-horizon goals remain open problems built on context engineering.
- "Multiple agents are automatically more capable." Uncoordinated agents add cost, latency and integration failures; the documented patterns (orchestrator-workers, parallelization) exist because structure — not count — is what helps.
- "If it passes the benchmark, it is production-ready." Task-level benchmarks measure resolution in controlled environments; operational properties (latency, cost, tool failure, injection resistance) are separate and usually unmeasured.

## Feynman targets

- "Explain the ReAct loop to a friend using a cooking metaphor (recipe -> check the pantry -> adjust)."
- "Explain workflows vs agents as 'a train on fixed rails' vs 'a driver choosing the route'."
- "Explain RAG memory as 'the library next door' vs the model as 'the person who read many books' — and when each is authoritative."

## Interleaving hooks

- From ai-ml/llm-architectures (prerequisite): agents inherit the LLM's properties — instruction-following (RLHF), parametric knowledge (weights), attention's O(n^2) context cost (why agents summarize/cache/retrieve instead of replaying everything), and RAG grounding. Re-derive each agent decision from these.
- Into frontiers practice: the same loop/checkpoint/stopping-condition ideas recur in post-quantum and formal-verification frontier packs as "narrow scope + human gate" — a cross-frontier reliability theme.

## How to keep this current

- Re-review at review_after (2027-02-17) or earlier: verify (1) tool-calling protocol state (MCP versions, provider APIs), (2) agent-eval landscape (new task-level benchmarks; saturation), (3) framework names and guidance, (4) memory approaches (context engineering vs trainable memory progress), (5) security practice (prompt injection mitigations — currently UNVERIFIED in this pack).
- Process: propose changes as a PR (draft -> CI -> L2 review -> human gate); never silently rewrite published content.
