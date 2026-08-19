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

# LLM Architectures — validation

## Formative (practice)

### Q1
- Q: Write the scaled dot-product attention formula and name the three inputs. What is the scaling factor and why is it there?
- bloom: remember
- bank: formative
- A: Attention = softmax(QK^T / sqrt(d_k))V, over queries Q, keys K, values V (linear projections of the input). The sqrt(d_k) scaling counteracts dot products that grow large with dimension, which would push softmax into very small gradients.
- evidence: [S-0269]
- topic: ai-ml/llm-architectures

### Q2
- Q: Why did replacing recurrence with attention change how transformers are trained, and what did it cost?
- bloom: understand
- bank: formative
- A: Removing recurrence lets all tokens be processed in parallel during training (a recurrent step serializes on the previous hidden state). The cost: full self-attention is O(n^2) per layer in sequence length, so very long sequences become the binding constraint.
- evidence: [S-0269]
- topic: ai-ml/llm-architectures

### Q3
- Q: State the compute-optimal rule of thumb from Hoffmann et al. and what Chinchilla demonstrated with it.
- bloom: understand
- bank: formative
- A: At the compute-optimal point, training data should scale at the same rate as parameters — roughly 20 tokens per parameter. Chinchilla (70B params, 1.4T tokens) matched or beat larger undertrained models (Gopher 280B, GPT-3 175B, MT-NLG 530B) at the same compute budget, showing earlier models were undertrained.
- evidence: [S-0273]
- topic: ai-ml/llm-architectures

### Q4
- Q: List the three stages of RLHF as introduced by InstructGPT.
- bloom: remember
- bank: formative
- A: (1) Supervised fine-tuning on human demonstrations; (2) training a reward model on human rankings of model outputs; (3) optimizing the policy with PPO against the reward model (with a small pretraining-data mix).
- evidence: [S-0274]
- topic: ai-ml/llm-architectures

## Summative (mastery checkpoint)

### Q5
- Q: Explain the parametric vs non-parametric memory distinction in RAG, and why the non-parametric side can change without retraining.
- bloom: understand
- bank: summative
- A: Parametric memory = the generator's weights (knowledge learned at training). Non-parametric memory = the external document index (DPR-encoded passages), queried at inference. They are decoupled: updating the index changes what is retrieved without touching the weights, so facts can be added/removed without retraining — the advantage of RAG over purely parametric systems.
- evidence: [S-0278]
- topic: ai-ml/llm-architectures

### Q6
- Q: Human raters preferred a 1.3B-parameter InstructGPT over the 175B GPT-3. Explain what this shows about scale versus post-training, and the role of the "alignment tax".
- bloom: understand
- bank: summative
- A: Post-training (instruction + preference optimization) shaped a small model to follow instructions well enough to beat a 100x larger base model on human preference. Scale alone is not instruction-following; the base model provides knowledge/capability, RLHF shapes behavior — with a measured cost: small regressions on standard NLP benchmarks (the alignment tax).
- evidence: [S-0274]
- topic: ai-ml/llm-architectures

### Q7
- Q: A team has a fixed compute budget and must choose between a 175B-parameter model trained on 300B tokens and a 70B model trained on 1.4T tokens. Which is expected to perform better on downstream tasks, and why?
- bloom: apply
- bank: summative
- A: The 70B/1.4T model (Chinchilla-style, ~20 tokens/param). At fixed compute, loss is minimized at the equal-scaling frontier; the 175B model is undertrained by the Hoffmann et al. standard, and Chinchilla empirically outperformed exactly such larger models (Gopher 280B, GPT-3 175B) downstream.
- evidence: [S-0273]
- topic: ai-ml/llm-architectures

### Q8
- Q: Why is "scaling-law guidance" treated as volatile rather than as a fixed law? Trace the documented revision and what may change next.
- bloom: analyze
- bank: summative
- A: The recipe changed materially within two years: Kaplan et al. (2020) said parameters should grow faster than data; Hoffmann et al. (2022) showed equal scaling is compute-optimal and that pre-2022 models were undertrained. Later work adds further corrections (inference-aware/overtrained deployment ratios). Each revision was quantitative guidance fitted to a regime, not a physical law — re-verify ratios against the current frontier before using them.
- evidence: [S-0273]
- topic: ai-ml/llm-architectures

## Review (spaced repetition — interleaved with prerequisites)

### Q9
- Q: An MLP and a transformer both train with gradient descent on a loss. What architectural machinery did the transformer add on top of the neural-network stack, and what training property did it change? (Neural networks interleave.)
- bloom: understand
- bank: review
- A: The transformer added attention (weighted context mixing across positions, with softmax(QK^T/sqrt(d_k))V) plus residual connections and layer norm on top of feed-forward blocks; it removed recurrence/convolution, so training parallelizes across positions instead of unrolling the sequence through time. The optimizer and backprop machinery are shared with ordinary neural networks.
- evidence: [S-0269]
- topic: ai-ml/neural-networks

### Q10
- Q: In neural-network terms, what is the difference between "underfitting" and the Chinchilla finding that 2020-era frontier models were undertrained?
- bloom: understand
- bank: review
- A: Underfitting classically means the model's capacity is insufficient for the task; Chinchilla's point is different: at a fixed compute budget, the capacity was too large relative to the data — a 175-280B model on ~300B tokens sits off the compute-optimal curve, and the same compute spent on 70B params + 1.4T tokens fits the data better (lower loss, better downstream scores). It is an allocation problem (params vs data), not simply model capacity.
- evidence: [S-0273]
- topic: ai-ml/neural-networks

### Q11
- Q: A neural network that memorizes the training set generalizes poorly. What is the LLM-scale analogue of the capacity/data balance, and which lever did Hoffmann et al. show was mis-set in 2020-2022 models?
- bloom: analyze
- bank: review
- A: The analogue is the parameter/token balance: too many parameters for the data is a memorization-adjacent regime (and economically wasteful at frontier scale). Hoffmann et al. showed the field was over-allocating to parameters and under-allocating to data (undertrained models), and that equal scaling is compute-optimal — the same bias-variance tradeoff, relocated to the training-budget plane.
- evidence: [S-0273]
- topic: ai-ml/neural-networks
