---
id: ai-ml/neural-networks
title: Neural Networks
band: B4
track: ai-ml
tier: T1
bloom_target: apply
prerequisites: [ai-ml/supervised-learning]
related: [cs-foundations/probability-statistics]
recommended: []
status: draft
schema-version: 1
owner: l1-neural-networks
reviewed-by: []
updated: 2026-08-18
sources: [S-0257, S-0267, S-0268, S-0269]
---

# Neural Networks — validation

## Formative (practice)

### Q1
- Q: Define ReLU and explain, in one or two sentences, why saturating activations like sigmoid slow gradient-based training.
- bloom: remember
- bank: formative
- A: ReLU(z) = max(0, z): a piecewise-linear, unbounded activation with unit slope on the positive region. Sigmoid/tanh saturate — their derivative σ′(z) = σ(z)(1−σ(z)) approaches zero when |z| is large — so error signals multiplied through saturated units shrink, and learning slows or stalls (a local cause of vanishing gradients).
- evidence: [S-0268]
- topic: ai-ml/neural-networks

### Q2
- Q: In your own words, what does backpropagation compute, and how is it an application of the chain rule rather than a new learning rule?
- bloom: understand
- bank: formative
- A: It computes the gradient of the loss with respect to every weight in the network. The forward pass records activations; the chain rule lets you factor the gradient into local Jacobians — an error signal δ_l propagates from the output layer backward through the transposed weight matrices, multiplied by the activation derivative at each layer (δ_l = (W_{l+1}ᵀ δ_{l+1}) ⊙ σ′(z_l)). Any differentiable computation graph can be differentiated this way; backpropagation is just that applied to networks.
- evidence: [S-0267]
- topic: ai-ml/neural-networks

### Q3
- Q: Your MLP's loss goes to NaN by epoch 10. List the three most likely causes in order and the standard fix for each.
- bloom: apply
- bank: formative
- A: (1) Learning rate too large — the updates overshoot into diverging losses; fix: reduce η or add a schedule/adaptive optimizer. (2) Exploding gradients — error signals multiplying through layers with large spectral norm; fix: gradient clipping, weight initialization with smaller scale, normalization layers. (3) Unstable loss/numerics — e.g., log(0) in the loss or unbounded activations; fix: add a small epsilon in logs, use logits-based loss (softmax-cross-entropy fused), or switch activations (ReLU over saturating ones).
- evidence: [S-0268]
- topic: ai-ml/neural-networks

## Summative (mastery checkpoint)

### Q4
- Q: Hand-compute one backpropagation update for the two-layer net from the teaching example with a different start: x=1, y=1, w1=0.2, w2=0.5, sigmoid activations, MSE loss, η=0.5. Give forward activations, both deltas, both gradients, and the updated weights.
- bloom: apply
- bank: summative
- A: Forward: z1 = 0.2, h = σ(0.2) ≈ 0.5498; z2 = w2·h = 0.5·0.5498 = 0.2749, ŷ = σ(0.2749) ≈ 0.5683; L = ½(ŷ−1)² ≈ 0.0932. Output delta: δ_out = (ŷ−1)·ŷ(1−ŷ) = (−0.4317)(0.5683)(0.4317) ≈ −0.1059. Hidden delta: δ_h = w2·δ_out·h(1−h) = 0.5·(−0.1059)·(0.5498·0.4502≈0.2475) ≈ −0.0131. Gradients: ∂L/∂w2 = δ_out·h ≈ −0.0582; ∂L/∂w1 = δ_h·x ≈ −0.0131. Update: w2 ← 0.5 − 0.5·(−0.0582) = 0.5291; w1 ← 0.2 − 0.5·(−0.0131) = 0.2066. The output moves toward 1, so loss falls next epoch.
- evidence: [S-0267][S-0268]
- topic: ai-ml/neural-networks

### Q5
- Q: Training: loss 0.01 and still falling; validation loss starts rising at epoch 8. Meanwhile layer-1 gradients are ≈1e-6. Diagnose both problems and prescribe fixes.
- bloom: analyze
- bank: summative
- A: Validation rising while train falls = overfitting: the network's capacity is memorizing the training set (the resubstitution/held-out gap); fixes: early stopping at epoch ~8, dropout, weight decay, more data/augmentation, or less capacity. Layer-1 gradients ≈1e-6 = vanishing gradients in the first layer: error signals shrink as they propagate backward through the network (the product of Jacobians); fixes: ReLU instead of sigmoid/tanh, better initialization (e.g., variance-preserving scale), batch/layer normalization, residual connections. Both are structural and can compound: with tiny gradients the first layers stop learning and the model leans on later layers — fix initialization and normalization first, then address overfitting.
- evidence: [S-0257][S-0268]
- topic: ai-ml/neural-networks

### Q6
- Q: A colleague claims: "Transformers made CNNs and RNNs obsolete — we should use attention for everything." Evaluate the claim against the evidence.
- bloom: evaluate
- bank: summative
- A: Incorrect. The transformer's self-attention (all-pairs, parallelizable) replaced recurrence for sequence modeling and became the foundation of modern LLMs (Vaswani et al.), but architecture choice is about matching inductive bias to data: CNNs encode translation equivariance, which remains efficient and data-economical for images; RNNs/state models handle streaming or long-context settings cheaply. Attention is O(n²) in sequence length, needs more data to compensate for its weaker structural priors, and on small datasets the bias-leaner architectures win. "One architecture for everything" confuses current dominance with universal optimality.
- evidence: [S-0269][S-0268]
- topic: ai-ml/neural-networks

### Q7
- Q: Write the chain-rule product that makes gradients vanish in a deep network, and state which two design choices counteract each factor.
- bloom: analyze
- bank: summative
- A: The error signal reaching layer l is a product of per-layer factors: δ_l ∝ (∏_{k=l}^{L} W_kᵀ σ′(z_k)) · (ŷ−y). Each factor has magnitude ≈ ‖W_k‖·‖σ′(z_k)‖; with many layers, products below 1 decay exponentially (vanish) and products above 1 grow exponentially (explode). Counteract ‖W‖ by normalized initialization and normalization layers (keep layer maps near-isometric) and counterbalance σ′ by choosing non-saturating activations (ReLU's derivative is 1 on the positive region instead of →0 for large |z|) — plus residual connections that let the gradient bypass layers entirely.
- evidence: [S-0268]
- topic: ai-ml/neural-networks

## Review (spaced repetition — interleaved with prerequisites)

### Q8
- Q: Your deep fraud model scores 99.9% on 10-fold CV but fails in production. Enumerate the checks you run before trusting any CV number on a deep pipeline.
- bloom: evaluate
- bank: review
- A: (1) Leakage audit — normalization/standardization fit on the full dataset before splitting, duplicated rows across folds, target-derived or future features; leaked deep models show exactly this near-perfect signature (Kaufman). (2) Metric fit — on imbalanced fraud data, report PRC/precision-recall at the operating threshold, not accuracy or ROC (Saito & Rehmsmeier). (3) Selection honesty — CV used for tuning is itself optimistic; the final number must come from a test set touched once (Kohavi). A 99.9% CV score on fraud is a red flag that one of these three is broken, not a reason to celebrate.
- evidence: [S-0258][S-0259][S-0257]
- topic: ai-ml/ml-fundamentals

### Q9
- Q: For a binary classifier, the sigmoid output ŷ = σ(z) is interpreted as P(y=1|x). Express the cross-entropy loss as the negative log-likelihood of a Bernoulli random variable, and state the chain-rule factor that connects the output-layer delta to (ŷ−y). (Probability & statistics interleave.)
- bloom: understand
- bank: review
- A: Cross-entropy L = −[y log ŷ + (1−y) log(1−ŷ)] is exactly −log P(y|x) for y ~ Bernoulli(ŷ), i.e., maximum-likelihood estimation under a Bernoulli model. The chain rule gives ∂L/∂z = (∂L/∂ŷ)·(dŷ/dz) = (ŷ−y)/(ŷ(1−ŷ)) · ŷ(1−ŷ) = ŷ−y: the sigmoid's derivative cancels the log-likelihood's denominator, so the output-layer delta is simply (ŷ−y) — the cleanest demonstration of why cross-entropy pairs with sigmoid, and why probabilities (not raw scores) are the natural output of a classifier.
- evidence: [S-0268][S-0259]
- topic: cs-foundations/probability-statistics

### Q10
- Q: You average five neural nets and beat every single net. Connect this to the bias-variance material from supervised learning: which term does averaging reduce, and which property of the five nets makes the averaging work?
- bloom: analyze
- bank: review
- A: Averaging reduces variance: each net's error has an independent component (different initialization/data randomness), and averaging cancels the independent parts while leaving bias unchanged — the same mechanism as bagging forests, where the generalization error converges as learners are added (Breiman's result for forests; Kohavi's framework for the train/validation gap). The gains depend on decorrelation: five nets trained identically with one seed collapse into one net and averaging buys nothing; diversity (seeds, subsets, architectures) is what makes the ensemble work.
- evidence: [S-0257][S-0262]
- topic: ai-ml/supervised-learning
