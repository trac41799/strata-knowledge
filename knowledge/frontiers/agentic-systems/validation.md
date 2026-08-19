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
status: draft
schema-version: 1
owner: l1-agentic-systems
reviewed-by: []
updated: 2026-08-18
sources: [S-0277, S-0278, S-0279, S-0280]
review_after: 2027-02-17
---

# Agentic Systems — validation

## Formative (practice)

### Q1
- Q: Name the three phases of the ReAct loop and what each produces.
- bloom: remember
- bank: formative
- A: Thought (reasoning trace about the current state and next step), Action (a tool call / environment action), Observation (the result of the action, fed back as the next input). The alternation is what distinguishes the loop from a single call.
- evidence: [S-0277]
- topic: frontiers/agentic-systems

### Q2
- Q: ReAct reduced hallucination on HotpotQA/FEVER. What mechanism did it add, and why does that reduce hallucination relative to chain-of-thought?
- bloom: understand
- bank: formative
- A: It added interaction with a Wikipedia API: the model performs search/lookup actions and conditions the next step on the retrieved observations. Grounding in external evidence replaces reliance on parametric knowledge alone, so answers are checked against retrieved content instead of generated from memory — and error propagation is caught earlier because each step observes the environment.
- evidence: [S-0277]
- topic: frontiers/agentic-systems

### Q3
- Q: Distinguish a workflow from an agent per Anthropic's 2024 guidance.
- bloom: understand
- bank: formative
- A: A workflow orchestrates LLMs and tools through predefined code paths (the steps are fixed by the developer); an agent lets the LLM dynamically direct its own process and tool usage, deciding steps as it goes. Workflows give predictability for well-defined tasks; agents are for open-ended tasks where steps cannot be pre-specified.
- evidence: [S-0279]
- topic: frontiers/agentic-systems

### Q4
- Q: What does SWE-bench measure, and what does the model have to produce to score?
- bloom: remember
- bank: formative
- A: It measures whether an agent can resolve real GitHub issues: given a codebase and an issue description, the model must produce code changes such that the held-out tests pass — full task resolution across 2,294 instances from 12 Python repos.
- evidence: [S-0280]
- topic: frontiers/agentic-systems

## Summative (mastery checkpoint)

### Q5
- Q: Design the minimal loop for an agent that answers customer questions from a company knowledge base. Specify: the tools, the loop structure, and two reliability mechanisms.
- bloom: apply
- bank: summative
- A: Loop: user question -> thought (which tool, what query) -> action (retrieve(query) over the knowledge index; optionally lookup/expand) -> observation (top passages) -> answer. Tools: one retrieval tool (RAG-style index over company docs — the non-parametric memory can be updated as docs change without retraining). Reliability: (1) ground-truth per step — base the final answer only on retrieved passages, citing them; (2) checkpoint/scope — require human approval before any irreversible action (e.g., writes), and a stopping condition (max steps).
- evidence: [S-0278][S-0277][S-0279]
- topic: frontiers/agentic-systems

### Q6
- Q: Your task: generate a weekly report from three fixed internal data sources, where the extraction steps never change. Choose workflow or agent, justify, and sketch the implementation choice (framework vs direct calls).
- bloom: apply
- bank: summative
- A: Workflow — the steps are fixed and predictable, so predefined code paths give consistency and lower cost; an agent adds latency and failure modes without benefit. Implement as direct LLM API calls (retrieval + in-context examples are usually enough), using a framework only if it genuinely reduces boilerplate; per guidance, start direct and keep the underlying code understandable.
- evidence: [S-0279]
- topic: frontiers/agentic-systems

### Q7
- Q: Compare RAG-style retrieval memory with a hypothetical trainable memory for an agent, on: update latency, cost, and behavior risk. Which is the current practice and why?
- bloom: analyze
- bank: summative
- A: Retrieval memory: updates are index-side (new documents available immediately, no retraining — decoupled non-parametric memory), cost is per-query retrieval + generation, and there is no risk of the model's weights drifting from training data. Trainable memory: updates require fine-tuning runs (slow, expensive) and risk catastrophic forgetting/capability shifts. Current practice is retrieval/context engineering precisely because it is fast, cheap and reversible; trainable persistent memory is open research.
- evidence: [S-0278]
- topic: frontiers/agentic-systems

### Q8
- Q: You must evaluate a coding agent before deploying it. Design an evaluation plan: benchmark, its known limitations, and what you would additionally measure for production.
- bloom: evaluate
- bank: summative
- A: Use a task-level, execution-based benchmark (SWE-bench-style: real issue + codebase + held-out tests) as the capability measure. Known limitations: curated task distribution, no operational properties, saturation/contamination risk — a high pass rate does not imply production reliability. Additionally measure: latency and cost per task, tool failure/retry rates, behavior under prompt-injection attempts, and human-checkpoint compliance, using a shadow/eval harness on real tasks.
- evidence: [S-0280]
- topic: frontiers/agentic-systems

### Q9
- Q: A multi-step coding task can change several files, and you cannot predict which ones. Select a multi-agent/workflow pattern and justify it; then state the two main failure modes you must engineer against.
- bloom: analyze
- bank: summative
- A: Orchestrator-workers: a central LLM dynamically decomposes the task and delegates file-specific subtasks to worker LLMs, then synthesizes results — appropriate because subtask structure is unpredictable. Main failure modes: (1) compounding small errors over many turns (workers diverge, wrong edits accepted) — mitigate with ground-truth per step (run tests, diff review) and human checkpoints; (2) integration conflicts when synthesizing workers' outputs — mitigate by having the orchestrator verify the merged state against tests before completion.
- evidence: [S-0279]
- topic: frontiers/agentic-systems

## Review (spaced repetition — interleaved with prerequisites)

### Q10
- Q: An agent's loop is built on instruction-following and grounding. From the LLM side: which two mechanisms covered in llm-architectures directly supply these, and how does each fail when used alone? (LLM architectures interleave.)
- bloom: understand
- bank: review
- A: (1) RLHF/instruction tuning supplies instruction-following (InstructGPT's preference optimization made models follow instructions; 1.3B beat 175B base on this dimension) — alone it still hallucinates because knowledge is parametric. (2) RAG supplies grounding: retrieved text conditions generation (non-parametric memory), reducing reliance on parametric knowledge — alone it lacks the multi-step loop. The agent loop (ReAct) combines them: instruction-following for action selection, retrieval/tools for ground truth.
- evidence: [S-0274][S-0278]
- topic: ai-ml/llm-architectures

### Q11
- Q: A transformer has O(n^2) attention cost in sequence length. How does that constraint show up in agent design, and which agentic pattern exists partly to work around it?
- bloom: apply
- bank: review
- A: Agents accumulate trajectory history (thoughts, tool results, observations), which grows the context window and therefore attention cost per step. Working around it: context engineering — summarization, caching, and retrieval of only relevant history (the "memory as context" pattern) instead of replaying everything; and keeping per-step contexts small (orchestrator-workers each handle only their subtask's context).
- evidence: [S-0272][S-0279]
- topic: ai-ml/llm-architectures
