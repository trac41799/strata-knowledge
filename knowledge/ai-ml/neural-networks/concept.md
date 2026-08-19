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

# Neural Networks

## Claims

### Perceptron and MLP basics

- A perceptron computes a linear threshold function ŷ = sign(w·x + b); it can only represent linearly separable functions, and XOR is the canonical counterexample. [T1][S-0267]
- An MLP composes affine transforms with nonlinear activations; a network with one hidden layer of sufficient width can approximate any continuous function on a compact domain (universal approximation). [T3][S-0268]
- Hidden layers fix the perceptron's limitation: an MLP learns hidden representations that make the problem linearly separable in hidden space — the capability Rumelhart et al. demonstrated with backpropagation, including on XOR. [T1][S-0267]

### Activation functions

- Sigmoid σ(z) = 1/(1+e^−z) and tanh squash activations to a bounded range; ReLU(z) = max(0, z) is unbounded and piecewise linear. [T3][S-0268]
- Saturating activations (sigmoid/tanh) damp gradient flow when pre-activations are large in magnitude; ReLU's unit-slope positive region makes it the standard default for hidden layers in modern networks. [T3][S-0268]

### Backpropagation

- Backpropagation computes the gradient of the loss w.r.t. every weight by the chain rule: a forward pass records activations, then an error signal δ_l = (W_{l+1}ᵀ δ_{l+1}) ⊙ σ′(z_l) propagates backward, giving ∂L/∂W_l = δ_l h_{l−1}ᵀ. [T1][S-0267]
- Backpropagation made learning in networks with hidden layers tractable and is the algorithmic basis of essentially all neural-network training; its 1986 demonstration — including learning XOR and useful hidden representations — opened the modern era of neural networks. [T3][S-0267]

### Gradient problems

- The backward pass multiplies per-layer Jacobians: the error signal scales roughly like the product over layers of ‖W_l‖·‖σ′(z_l)‖, so products below 1 vanish exponentially with depth and products above 1 explode — the vanishing/exploding gradient mechanism. [T3][S-0268]
- Vanishing/exploding gradients are why plain deep or recurrent networks are hard to train; the standard mitigations are ReLU, careful initialization, normalization, residual connections, and gating. [T3][S-0268]
- RNNs reuse the same weight matrix across time steps, so backpropagation-through-time multiplies the same Jacobian repeatedly: long sequences suffer severe vanishing or exploding gradients. [T3][S-0268]

### Architectures overview

- CNNs share weights over local receptive fields — a translation-equivariance inductive bias that made them dominant for images; RNNs process sequences through recurrence and were the classical architecture for text and time series. [T3][S-0268]
- The transformer replaces recurrence and convolution with stacked self-attention, processing all positions in parallel; introduced for machine translation, it became the foundation architecture of modern sequence models and large language models. [T3][S-0269]
- Architecture encodes inductive bias: translation equivariance (CNN), temporal order (RNN), pairwise attention (transformer); matching the bias to the data structure is what makes deep learning work — not scale alone. [T3][S-0268][S-0269]

### Overfitting in deep networks

- Deep networks have enough capacity to fit training labels almost perfectly while generalizing poorly; the widening train/validation gap is the overfitting signature, and validation-loss monitoring during training is mandatory. [T1][S-0257]
- Dropout randomly zeroes hidden units during training — an implicit ensemble of thinned networks — and weight decay (L2) and data augmentation are complementary regularizers. [T3][S-0268]
- Early stopping — halting training when validation error begins to rise — is the cheapest and most widely used regularizer for deep nets. [T3][S-0268]

### Training dynamics

- The learning rate controls step size: too large diverges or oscillates, too small stalls; scheduling the learning rate and using adaptive optimizers are standard practice. [T3][S-0268]
- Mini-batch size trades gradient noise for throughput: larger batches yield lower-variance gradient estimates at higher per-example cost, and batch size interacts with the learning rate — the two must be tuned together. [T3][S-0268]

## Details

Training a network is supervised learning's loop with a differentiable program in the middle: forward pass computes the loss; backpropagation (chain rule) computes its gradient; a gradient-descent variant updates weights; capacity and regularizers set the bias-variance operating point, monitored on validation data. The three architectural families are three answers to "what structure does the data have?" — locality (CNN), order (RNN), pairwise interaction (transformer). The two recurring failure modes are structural: gradients that vanish/explode with depth or time, and capacity that memorizes instead of generalizing.

## Boundaries / common misunderstandings

- "Deep learning is a panacea" — it is data- and compute-hungry; inductive biases and architecture choice matter, and on small or tabular data classical models and ensembles often win. [T3][S-0268][S-0269]
- "Backpropagation is a separate learning rule" — it is the chain rule applied to a differentiable computation graph; the same mechanism generalizes to any differentiable program, and knowing the derivation is how you debug training. [T1][S-0267]
- "More layers always improves accuracy" — depth without data, normalization, and good initialization produces vanishing gradients and overfitting, not better models. [T3][S-0268]
- "Bigger learning rate trains faster" — a rate too large makes the loss diverge or oscillate; the loss curve, not the rate, is the diagnostic. [T3][S-0268]
- "Dropout should always be on" — it is a training-time regularizer (scaled off at inference) and can hurt when data is plentiful or other regularizers already control overfitting. [T3][S-0268]
- "Networks learn features automatically, so preprocessing and discipline don't matter" — representation learning still depends on data quality and bias-variance; a deep net on contaminated or small data fails like any other model. [T1][S-0257]

## References (evidence records)

- S-0257 — Kohavi (1995) — resubstitution bias; the overfitting signature; model selection on held-out/CV scores.
- S-0267 — Rumelhart, Hinton & Williams (1986) — backpropagation; perceptron limitations; hidden representations; XOR.
- S-0268 — Goodfellow, Bengio & Courville (2016) — textbook: MLP/universal approximation, activations, backprop derivation, gradient problems, architectures, regularizers, training dynamics.
- S-0269 — Vaswani et al. (2017) — transformer; self-attention replacing recurrence/convolution; parallel processing of all positions.
