---
id: ai-ml/llm-architectures
title: LLM Architectures
band: B5
track: ai-ml
tier: T4
bloom_target: understand
prerequisites: [ai-ml/neural-networks]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-llm-architectures
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0269, S-0273, S-0274, S-0278]
review_after: 2027-02-17
---

# LLM Architectures — teaching

## Learning objectives (Bloom)

At the end of this topic the learner can (understand level; target = understand):

- Describe how the transformer computes context (scaled dot-product attention, multi-head, masked decoder attention) and why removing recurrence changed training.
- Explain the compute-optimal scaling recipe (equal scaling, ~20 tokens/param) and what Chinchilla demonstrated about undertrained models.
- Sequence the InstructGPT RLHF pipeline and interpret its human-preference results, including the alignment tax.
- Distinguish parametric from non-parametric memory and explain when/why RAG is used.
- State what is settled (T1) versus volatile (T4) in this pack, and where to look for change.

## Worked example

Worked example 1 — a hand-computed attention step. Suppose d_k=2, one query q = [1, 2], two keys K = [[1, 2], [2, 1]], values V = [[0.3, 0.7], [0.8, 0.2]], scale = sqrt(2) ~ 1.414.

1. Dot products: q.K1 = 1*1 + 2*2 = 5; q.K2 = 1*2 + 2*1 = 4.
2. Scale: 5/1.414 ~ 3.54; 4/1.414 ~ 2.83.
3. Softmax: exp(3.54) ~ 34.5, exp(2.83) ~ 16.9; sum ~ 51.4; weights ~ 0.67 and 0.33.
4. Weighted sum of values: 0.67*[0.3, 0.7] + 0.33*[0.8, 0.2] = [0.20 + 0.26, 0.47 + 0.07] ~ [0.46, 0.54].

The output for position 1 is a convex combination of the values — context mixed by compatibility of query and key. Without the sqrt(2) scaling the logits (5, 4) would be larger and softmax saturates (weight 0.73/0.27 — already less contrast); at realistic d_k=64 the un-scaled dot products grow with dimension and push softmax into saturated, low-gradient territory.

Worked example 2 — a compute-optimal budget. A team can afford 1e21 FLOPs (roughly Gopher's budget). Using Hoffmann-style equal scaling, the compute-optimal point was ~70B parameters with 1.4T tokens (~20 tokens/param). The team's older plan (280B params, 300B tokens) is the same compute but off-curve: Chinchilla-style training predicts — and empirically delivered — better downstream performance, because the loss is minimized at the equal-scaling frontier, not by the larger model.

## Elaboration prompts

- "Why does scaling by sqrt(d_k) matter for gradient flow through softmax? Trace what happens to the logits at large d_k."
- "Chinchilla corrected Kaplan et al. What assumptions had to break for the earlier result to be wrong? What assumption might break for Chinchilla next?"
- "Why does instruction-following benefit more from RLHF than from scale? What does the 1.3B-beats-175B result imply about where capability actually lives?"
- "RAG retrieves before generating. Where does retrieved text 'enter' the model, and why does that avoid retraining?"
- "If a model already has a 1M-token context window, is RAG obsolete? Argue both sides using the parametric/non-parametric distinction."

## Common misconceptions

- "Attention is a memory store." Attention weights are recomputed per forward pass from the input; nothing persists. Persistent knowledge lives in weights (parametric memory); external knowledge lives in an index (non-parametric memory) — see the Boundaries section of concept.md.
- "Scale is a free lunch." At fixed compute, bigger is only better if data grows with it; undertrained large models lose to compute-optimal smaller ones (Chinchilla vs Gopher/GPT-3).
- "Context window = updatable knowledge." Prompts do not update the model; new facts require retrieval, fine-tuning, or retraining.
- "RLHF teaches new facts." It reshapes behavior (helpfulness, truthfulness, refusal) on a fixed base model; knowledge comes from pretraining.
- "More data alone fixes everything." Data must be matched to capacity at the compute-optimal point; adding only data (or only parameters) moves off the frontier.

## Feynman targets

- "Explain scaled dot-product attention to a friend without formulas, then with the formula — and say which parts you had to hand-wave."
- "Explain why a 70B model beat a 175B model at the same compute budget, in three sentences."
- "Explain the difference between what a model 'knows' (parametric) and what RAG lets it 'access' (non-parametric), with a library metaphor."

## Interleaving hooks

- From ai-ml/neural-networks (prerequisite): transformers are neural networks whose architecture replaced recurrence with attention — revisit backprop/optimization as the shared training machinery, and bias-variance as the frame for scaling allocation.
- Into frontiers/agentic-systems (next topic): an agent is an LLM plus tools in a loop — the RLHF-shaped instruction-following and the RAG-style retrieval machinery here become the agent's substrate.

## How to keep this current

- Re-review at review_after (2027-02-17) or earlier if a cited claim shifts: verify (1) scaling-law ratios and any revision of equal-scaling guidance, (2) frontier context-window sizes, (3) post-training recipes (RLHF vs RL-style reasoning training), (4) RAG vs long-context economics, (5) safety-practice standardization. Add records for quantization and for 2025-2026 post-training/safety sources (currently UNVERIFIED in this pack).
- Process: propose changes as a PR (draft -> CI -> L2 review -> human gate); never silently rewrite published content.
