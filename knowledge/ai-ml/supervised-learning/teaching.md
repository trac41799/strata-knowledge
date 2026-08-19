---
id: ai-ml/supervised-learning
title: Supervised Learning
band: B4
track: ai-ml
tier: T1
bloom_target: apply
prerequisites: [ai-ml/ml-fundamentals]
related: [ai-ml/neural-networks]
recommended: []
status: draft
schema-version: 1
owner: l1-supervised-learning
reviewed-by: []
updated: 2026-08-18
sources: [S-0257, S-0259, S-0262, S-0263, S-0264, S-0268]
---

# Supervised Learning — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: state the L1/L2 penalty forms, the max-margin idea of SVMs, and the bagging-vs-boosting distinction. [T0][S-0268][S-0264][S-0262][S-0263]
- **understand**: explain why bagging reduces variance, boosting reduces bias, and why regularization strength must be chosen on validation data. [T1][S-0262][S-0263][S-0257]
- **apply**: select a family/protocol/metrics for a tabular problem, run gradient descent on a small loss by hand, and interpret train/validation curves. [T0][S-0268][T1][S-0257] **bloom_target**
- **analyze**: decompose train/validation gaps and ensemble behavior in terms of bias-variance; audit a model-selection story for resubstitution bias. [T1][S-0257][S-0262]
- **evaluate**: judge claims like "random forests never overfit" or "more regularization is always safer" against the evidence. [T1][S-0262][S-0257]

## Worked example — gradient descent on a small loss, then the bias-variance lesson

1. **Setup.** Minimize L(w) = (w−3)² starting at w=5, η=0.1. The gradient is ∇L = 2(w−3) = 4 at w=5; the update w ← w − η∇L gives w = 5 − 0.4 = 4.6. [T0][S-0268]
2. **Iterate.** Step 2: ∇=3.2 → w = 4.28; step 3: ∇=2.56 → w ≈ 4.02. The losses 4, 2.56, 1.64, 1.05 fall monotonically; w approaches 3. With η=1 the update at w=5 overshoots to 1 and the iterates oscillate 5↔1; η>1 diverges. Learning rate = stability boundary. [T0][S-0268]
3. **Add a regularizer.** Minimize L_λ(w) = (w−3)² + λw² instead. The optimum is w* = 3/(1+λ): λ=0 → w*=3 (unregularized), λ=1 → w*=1.5, λ=5 → w*=0.5. The penalty pulls the optimum toward zero — that is the bias — in exchange for variance reduction, which is why ridge λ is chosen on validation/CV, never on train error. [T1][S-0257]
4. **Make it a model-selection story.** Add two families to the comparison: a random forest (averages many trees; error converges as trees grow — the variance-reduction of bagging) and gradient boosting (fits trees to residuals stagewise — the bias-reduction of boosting). Select among ridge λ, RF, GBM with ten-fold stratified CV; report once on the untouched test set. [T1][S-0262][S-0263][S-0257]
5. **Metrics on an imbalanced target.** If the class ratio is 5:95, the PRC baseline P/(P+N) sits at 0.05 and ROC can flatter; report precision/recall at the operating threshold. [T1][S-0259]

## Elaboration prompts

- Gradient descent is the ancestor of every optimizer in this and later topics: trace what changes as you go from full-batch to mini-batch estimates (the estimator stays unbiased in expectation). [T0][S-0268]
- Walk through the bias-variance decomposition as λ grows from 0 to ∞: which term rises, which falls, and why the sum's minimum is not at either extreme. [T1][S-0257]
- Breiman's forest and Friedman's boosting are both "many trees", yet one reduces variance and the other reduces bias. What exactly differs — resampling vs residuals, parallel vs sequential? [T1][S-0262][S-0263]
- L1 zeroes coefficients, L2 does not. Sketch why (the geometry of the |w| penalty touching an axis in weight space) and name the practical consequence for feature selection. [T3][S-0268]
- A model has AUC 0.99 but PRC 0.03 on fraud data. Reconstruct what the alert stream looks like and what metric the operator should optimize. [T1][S-0259]

## Common misconceptions

1. **"Deep learning beats everything."** On tabular or small data, tuned tree ensembles and linear models are often as good or better with far less data and compute; deep learning is not a panacea. [T3][S-0262][S-0263]
2. **"Random forests never overfit."** They do not overfit as the number of trees grows (error converges), but tree depth/complexity still overfits — tune those on validation data. [T1][S-0262][S-0257]
3. **"More regularization is always safer."** Regularization trades bias for variance; too much underfits — that is why strength is a hyperparameter chosen by CV, not a moral good. [T1][S-0257]
4. **"Training accuracy selects models."** Resubstitution is optimistically biased; selection happens on validation/CV scores and the final number comes from the untouched test set. [T1][S-0257]
5. **"Accuracy is the metric."** On imbalanced classes accuracy hides failure; precision/recall and PRC expose it, and ROC can look deceptively good. [T1][S-0259]

## Feynman targets

Explain in plain language a non-engineer could follow:

- Why a student graded on the exact homework they practiced scores high without understanding — training accuracy is the same illusion; the validation set is the "different exam."
- Why averaging many slightly-wrong independent guesses (a forest) is more reliable than one careful guess (a single tree), and why a team of learners that each fix the others' remaining mistakes (boosting) ends up strong.
- Why "of every 100 alerts we fire, how many are real?" and "of every 100 real frauds, how many do we catch?" are two different questions, and why answering only "how often are we right overall?" hides a useless fraud detector.

## Interleaving hooks

- **ai-ml/ml-fundamentals (prerequisite)**: every protocol here inherits its discipline — split hygiene, leakage checks (learn-predict separation), and PRC/ROC literacy are assumed; this topic adds the families and algorithms those protocols select among.
- **ai-ml/neural-networks (related)**: the loss + gradient-descent machinery developed here (convex losses, η stability, regularization) is exactly what backpropagation and deep-net training dynamics build on; ensembles vs deep nets is a recurring bias-variance comparison.
- **cs-foundations/probability-statistics (via ml-fundamentals)**: expectations and variance are the raw material of the bias-variance decomposition; the unbiasedness of the mini-batch gradient estimator is an expectation argument.
