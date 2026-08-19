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
status: draft
schema-version: 1
owner: l1-llm-architectures
reviewed-by: []
updated: 2026-08-18
sources: [S-0269, S-0273, S-0274, S-0278]
review_after: 2027-02-17
---

# LLM Architectures

## Claims

### Transformer architecture

- The transformer replaced recurrent sequence models with a pure-attention architecture: it removes recurrence entirely so all tokens are processed in parallel, while keeping dot-product attention as the mechanism for modeling context. [T1][S-0269]
- Scaled dot-product attention: the output is a weighted sum of values, with weights computed as softmax(QK^T / sqrt(d_k)) — queries, keys and values are linear projections of the input, and dividing by sqrt(d_k) counteracts dot products that grow large with dimension. [T1][S-0269]
- Multi-head attention runs h parallel attention layers (h=8 in the original model, with d_k = d_v = d_model/h), letting the model attend to different representation subspaces, at a total computational cost similar to single-head attention. [T1][S-0269]
- Because every position attends to every other position, full self-attention cost grows quadratically with sequence length (O(n^2) per layer) — the key complexity constraint behind later efficiency work. [T1][S-0269]
- The original transformer is an encoder-decoder stack; the decoder uses masked self-attention so each position attends only to positions up to itself, preserving the autoregressive property required for generation. [T1][S-0269]

### Pretraining objectives

- The dominant pretraining objective for modern LLMs is causal next-token prediction on a decoder-only transformer: the compute-optimal exemplar Chinchilla is an autoregressive transformer trained for next-token prediction, and the InstructGPT family follows the same base recipe (pretrained GPT-3, then post-trained). [T1][S-0273][S-0274]
- The original encoder-decoder transformer also supports masked/bi-directional attention (encoder) and sequence-to-sequence tasks; the causal, decoder-only variant is what the current frontier LLM family standardized on. [T1][S-0269]

### Scaling laws (T1, volatile in part)

- Compute-optimal scaling (Hoffmann et al., 2022): for a fixed compute budget, model parameters and training tokens should be scaled at equal rates — doubling the model means doubling the training data. [T1][S-0273]
- Rule of thumb: ~20 training tokens per parameter at the compute-optimal point; Chinchilla (70B params, 1.4T tokens) matched or beat much larger, undertrained models (Gopher 280B, GPT-3 175B, Jurassic-1 178B, Megatron-Turing NLG 530B) at the same compute budget. [T1][S-0273]
- This corrected the earlier Kaplan et al. (2020) guidance, which held that parameter count should grow faster than data volume — most pre-2022 frontier models were undertrained by the revised standard. [T1][S-0273]
- Scaling guidance is itself volatile at the frontier: the quantitative recipe changed within ~2 years (2020 -> 2022), and later work (e.g., inference-aware "beyond Chinchilla-optimal" analysis, 2024) argues production models should be overtrained relative to the 20:1 ratio — treat any published ratio as dated guidance. [T4][S-0273]

### RLHF and instruction following

- RLHF as introduced by InstructGPT has three stages: supervised fine-tuning on human demonstrations, training a reward model on human pairwise preference rankings, and optimizing the policy with PPO against that reward model. [T1][S-0274]
- Human raters preferred outputs from the 1.3B-parameter InstructGPT over the 175B GPT-3, and preferred the 175B InstructGPT over 175B GPT-3 about 85% of the time — instruction-following via human feedback dominated raw scale on this dimension. [T1][S-0274]
- RLHF measurably improved safety-relevant behavior: InstructGPT produced truthful/informative answers roughly twice as often as GPT-3, hallucination dropped from 41% to 21% on summarization/closed-domain QA, toxic outputs decreased, at the cost of only small regressions on public NLP benchmarks (the "alignment tax"). [T1][S-0274]

### Context windows and RAG

- RAG pairs parametric memory (the generator's weights) with non-parametric memory (an external, updatable document index): Lewis et al. retrieve top-k passages with a DPR bi-encoder and condition a BART generator on them. [T1][S-0278]
- On open-domain QA (Natural Questions, WebQuestions, CuratedTrec), RAG set state-of-the-art exact match, beating closed-book generative models (T5-11B) and extractive retrieval systems (REALM, DPR) — grounding in retrieved text competes with purely parametric knowledge. [T1][S-0278]
- Because the index is decoupled from the parameters, the non-parametric memory can be updated (new documents, deletions) without retraining the generator — the practical advantage that made RAG the standard grounding pattern. [T1][S-0278]

## Details

The pipeline that produced today's LLMs: pretrain a decoder-only transformer with causal next-token prediction at a compute-optimal (or deliberately overtrained) size, then post-train with instruction data and RLHF-style preference optimization. Attention provides the sequence machinery (with O(n^2) cost as the binding constraint), scaling laws set the data/parameter budget, RLHF shapes behavior, and RAG adds updatable external knowledge that training cannot provide. Each stage is a distinct design decision; "the model" is usually a pipeline, not a single artifact.

## Boundaries / common misunderstandings

- "Attention is memory" — attention weights are computed dynamically from the input at every forward pass; they persist nothing across calls. The persistent knowledge is the parametric memory in the weights, which is exactly what RAG's non-parametric index complements. [T1][S-0278][S-0269]
- "Bigger is always better" — at fixed compute, an undertrained large model loses to a compute-optimal smaller one (Chinchilla 70B beats Gopher 280B and GPT-3 175B); scale is only useful when data scales with it. [T1][S-0273]
- "A long context window makes the model's knowledge updatable" — parametric knowledge is frozen at training time; new facts and corpora enter via retrieval (or retraining/fine-tuning), not by sending text in the prompt. [T1][S-0278]
- "RLHF adds new knowledge" — RLHF is behavior shaping on a fixed base model (same architecture, fine-tuned on human preference data); it does not add pretraining knowledge. [T1][S-0274]
- "The transformer is parallel, so generation is parallel" — parallelism is a training-time property (no recurrence); autoregressive generation still emits tokens one at a time. [T1][S-0269]

## Volatility notes

- Dated 2026-08-18; review at 2027-02-17 or earlier if a cited source shifts.
- Context windows grew rapidly in 2024-2025: from ~128k tokens (GPT-4 Turbo era) to 1M+ tokens in production (Gemini 1.5 Pro, Feb 2024, with 10M tested in research; 2M in some deployments) — verified via Google's announcement and the Gemini 1.5 technical report; exact window sizes change with every release and are NOT covered by a record in this pack.
- Post-training moved beyond RLHF as described here: since 2024-2025, labs combine SFT with RL-style reasoning training (e.g., DeepSeek-R1, Jan 2025, verified) and other recipes; the frontier mix is unsettled — UNVERIFIED in this pack (no record yet).
- Production practice deliberately overtrains models past the Chinchilla ratio (inference-aware scaling, e.g., 2024 "Beyond Chinchilla-Optimal" analyses; Llama-3-era ratios ~10x the 20:1 rule) — verified via secondary sources; not yet recorded in this pack.
- Quantization basics (4-bit/8-bit post-training quantization for deployment, e.g., GPTQ/AWQ/QLoRA-style methods) was DROPPED from this revision: it is established practice but no verified record slot was available — UNVERIFIED in this pack; add with a record at next review.
- Frontier safety/alignment practice (evals-based safety cases, responsible scaling policies, red-teaming) is volatile and not standardized — UNVERIFIED in this pack; the settled part (RLHF reduces measured harm) is covered above at T1.

## References (evidence records)

- S-0269 — Vaswani et al. (2017) — the transformer: self-attention, multi-head attention, parallelization, autoregressive decoding.
- S-0273 — Hoffmann et al. (2022) — compute-optimal scaling laws; 20 tokens/param; Chinchilla validation; correction of Kaplan et al. (2020).
- S-0274 — Ouyang et al. (2022) — InstructGPT RLHF: SFT, reward model, PPO; human preference results; alignment tax.
- S-0278 — Lewis et al. (2020) — RAG: parametric + non-parametric memory; DPR + BART; SOTA open-domain QA.
