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

# Neural Networks — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: state the perceptron update's linear-separability limit, the sigmoid/ReLU forms, and which architecture (CNN/RNN/transformer) encodes which inductive bias. [T0][S-0267][T3][S-0268][S-0269]
- **understand**: explain backpropagation as the chain rule, why saturating activations slow learning, and why deep/recurrent nets suffer vanishing or exploding gradients. [T0][S-0267][S-0268]
- **apply**: hand-compute forward/backward passes and weight updates on a two-layer net, and diagnose NaN or stalled training from the loss curve. [T0][S-0267][T3][S-0268] **bloom_target**
- **analyze**: decompose train/validation gaps and per-layer gradient magnitudes into their structural causes (capacity vs gradient product). [T1][S-0257][T0][S-0268]
- **evaluate**: judge "use architecture X for everything" claims against inductive-bias and data-availability arguments. [T3][S-0269][S-0268]

## Worked example — backpropagation on a two-layer net

1. **Setup.** Input x=1, target y=0; one hidden unit and one output unit, both sigmoid σ(z)=1/(1+e^−z); MSE loss L = ½(ŷ−y)²; initial weights w1=0.5 (input→hidden), w2=−0.2 (hidden→output); learning rate η=0.5. [T0][S-0267]
2. **Forward pass.** z1 = w1·x = 0.5, h = σ(0.5) = 0.6225; z2 = w2·h = −0.2·0.6225 = −0.1245, ŷ = σ(−0.1245) = 0.4689; L = ½(0.4689)² = 0.1100. [T0][S-0267]
3. **Output delta.** δ_out = (ŷ−y)·σ′(z2) = (0.4689−0)·0.4689·(1−0.4689) = 0.4689·0.2490 = 0.1168. (With cross-entropy loss this factor simplifies to exactly ŷ−y — the pairing that makes probabilities natural outputs.) [T0][S-0268]
4. **Backward pass.** δ_h = w2·δ_out·σ′(z1) = (−0.2)·0.1168·(0.6225·0.3775) = −0.00549. The chain rule factors the gradient layer by layer: the output error, the transposed weight, the local activation derivative. [T0][S-0267]
5. **Gradients and update.** ∂L/∂w2 = δ_out·h = 0.1168·0.6225 = 0.0727; ∂L/∂w1 = δ_h·x = −0.00549. Update: w2 ← −0.2 − 0.5·0.0727 = −0.2363; w1 ← 0.5 − 0.5·(−0.00549) = 0.5027. Recompute: ŷ′ = σ(−0.2363·0.6231) = 0.4633, L′ = 0.1073 < 0.1100 — one gradient step, loss decreased. [T0][S-0267]
6. **Read the numbers.** The hidden gradient is ~100× smaller than the output gradient — a one-layer taste of the vanishing-gradient mechanism; make the net 20 layers of sigmoids and the first-layer deltas underflow. Note the delta at the output is the *mistake* (ŷ−y) modulated by σ′; that is why a saturated output (σ′≈0) stops learning even with a big mistake. [T0][S-0268]
7. **Put it in the supervised loop.** Split first, train on train, watch validation loss every epoch — the moment it rises while train loss falls is the overfitting signature; stop, regularize (dropout, weight decay), or reduce capacity. Score the final model once on untouched test data. [T1][S-0257]

## Elaboration prompts

- Why does the output-layer delta for sigmoid + cross-entropy simplify to (ŷ−y)? Which two derivatives cancel, and what does that tell you about pairing loss with activation? [T0][S-0268]
- XOR: a single perceptron cannot represent it; write the hidden-layer computation that makes it linearly separable. What does the hidden unit "mean" in that example? [T0][S-0267]
- The error signal δ_l = (W_{l+1}ᵀ δ_{l+1}) ⊙ σ′(z_l): walk through which factor contributes to vanishing gradients, which to exploding, and which design choices target each. [T0][S-0268]
- CNNs, RNNs, transformers: name a dataset where each architecture's inductive bias is a *liability*, not an asset — then explain how you would still make it work. [T3][S-0268][S-0269]
- A deep net fits its training labels to 0.1% error. Is that good news or a diagnostic? Connect to resubstitution bias and to the training-dynamics knob (early stopping) that turns the observation into a decision. [T1][S-0257]

## Common misconceptions

1. **"Backpropagation is a mysterious learning rule."** It is the chain rule applied to a differentiable computation graph: forward pass, then error signals backward through transposed weight matrices. Understanding the derivation is what makes training failures debuggable. [T0][S-0267]
2. **"Deep learning is a panacea."** It is data- and compute-hungry; inductive bias and architecture choice matter, and on small or tabular data classical models and ensembles often win. [T3][S-0268][S-0269]
3. **"More layers = better accuracy."** Depth without data, normalization, and good initialization produces vanishing gradients and overfitting — the train/validation gap and the per-layer gradient magnitude are the diagnostics, not the layer count. [T1][S-0257][T3][S-0268]
4. **"Crank the learning rate to train faster."** Too large a rate diverges or oscillates (loss → NaN); too small stalls. Batch size and learning rate interact and are tuned as a pair. [T3][S-0268]
5. **"Dropout is always on / always helps."** It is a training-time regularizer scaled off at inference, and with ample data or strong other regularizers it can hurt. [T3][S-0268]

## Feynman targets

Explain in plain language a non-engineer could follow:

- A network learns by trying, measuring how wrong it is, and working backward layer by layer to see "how much of the mistake was each connection's fault" — like a relay race where the baton-passing error is traced from the last runner back to the first.
- Deep networks are powerful because they build concepts from concepts (edges → parts → objects), but they need enough examples: the network can "memorize the textbook" (overfit) if the exam only has new questions and it never practiced — validation loss is the check.
- Transformers, CNNs and RNNs are three different assumptions about the world: "what's next to what matters" (images), "what came before matters" (sequences), "everything relates to everything" (text) — choose the assumption that matches your data.

## Interleaving hooks

- **ai-ml/supervised-learning (prerequisite)**: backpropagation is gradient descent on the loss functions from supervised learning — the same η stability rule, the same regularization-for-variance logic, the same validation discipline; ensembles vs deep nets is a recurring bias-variance comparison.
- **ai-ml/ml-fundamentals (prerequisite, via supervised-learning)**: the train/validation/test protocol, leakage checks, and PRC-vs-ROC literacy apply unchanged — a deep pipeline leaks just as silently as any other.
- **cs-foundations/probability-statistics (related)**: sigmoid outputs are Bernoulli probabilities; cross-entropy is negative log-likelihood (the (ŷ−y) simplification is a derivatives-of-likelihood argument); the minibatch gradient's unbiasedness is an expectation argument.
