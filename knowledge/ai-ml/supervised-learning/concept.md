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

# Supervised Learning

## Claims

### Model families

- Linear regression models the target as a linear combination of features and is fit by least squares; logistic regression models the log-odds of the positive class as linear and outputs a probability via the sigmoid — the canonical first-line models when interpretability matters. [T3][S-0268]
- Support vector machines learn the maximum-margin separating hyperplane and extend to nonlinear problems by mapping inputs into a high-dimensional feature space via kernels. [T3][S-0264]
- Decision trees recursively partition the feature space with axis-aligned splits; individual trees are low-bias, high-variance learners, which is why they are the classic base learners for ensembles. [T3][S-0262]
- Tree ensembles — random forests and gradient boosting — are the standard default for tabular data, typically matching or beating neural networks on small-to-medium structured datasets. [T3][S-0262][S-0263]

### Loss functions and gradient descent

- The mean squared error L = (1/n)Σ(y−ŷ)² is the canonical regression loss; cross-entropy L = −(1/n)Σ[y log ŷ + (1−y) log(1−ŷ)] is the canonical classification loss — for linear models both are convex in the parameters. [T3][S-0268]
- Gradient descent minimizes a differentiable loss by iterating w ← w − η∇L(w); with a suitable learning rate η it converges for convex losses, and it is the ancestor of every optimizer used in machine learning. [T3][S-0268]
- Mini-batch (stochastic) gradient descent estimates the gradient from a random subset of data; the estimate is unbiased in expectation, so it converges to the same optimum while cutting per-iteration cost. [T3][S-0268]

### Bias-variance and ensembles

- Expected squared error decomposes into irreducible noise + bias² + variance; model complexity trades bias against variance, so the generalization optimum lies strictly between underfit and overfit. [T1][S-0257]
- Bagging — and random forests, which add random feature subsets per split — reduces variance by averaging many weakly correlated trees: Breiman shows the forest's generalization error converges as trees are added, so more trees do not overfit. [T1][S-0262]
- Boosting fits an additive model stagewise; Friedman derives it as steepest-descent minimization in function space and it primarily reduces bias by combining weak learners. [T1][S-0263]

### Regularization

- L2 (ridge) and L1 (lasso) penalties shrink coefficients toward zero, trading small bias for reduced variance; L1 drives weights exactly to zero and thus acts as feature selection. [T3][S-0268]
- Regularization strength is a hyperparameter: it must be selected on validation or cross-validated scores, never on training error, which is optimistically biased. [T1][S-0257]

### Cross-validation practice

- Ten-fold stratified cross-validation was the best model-selection method in Kohavi's large-scale comparison: use it to choose among model families and hyperparameters, then score the final model once on untouched test data. [T1][S-0257]

### Imbalanced data

- On imbalanced data, accuracy is dominated by the majority class and ROC/AUC can look deceptively good while precision among positive predictions is poor; precision-recall plots expose it. [T1][S-0259]
- Reporting must match the deployment class ratio: precision, recall and the PRC capture the operating point of a classifier, whereas accuracy and AUC hide failure on rare classes. [T1][S-0259]
- Common remedies for imbalance — class-weighted losses, resampling, threshold tuning — bias predictions toward the minority class, so the final classifier must be evaluated with the deployed metric. [T3][S-0268]

## Details

The supervised recipe: pick a family whose inductive bias matches the data (linear/probabilistic for interpretability, trees+ensembles for tabular, kernels for geometry), define a loss, minimize it with (mini-batch) gradient descent, and control complexity with regularization chosen by cross-validation. Bias-variance is the connective tissue: ensembles exploit it (bagging averages away variance, boosting chases away bias), regularization trades a little bias for a lot of variance, and imbalanced targets force the question of which error you care about. Every number produced must survive the discipline inherited from ml-fundamentals: select on held-out data, report on an untouched test set, and never let accuracy stand in for precision/recall.

## Boundaries / common misunderstandings

- "Deep learning beats everything" — on tabular or small data, tuned tree ensembles and linear models are often as good or better with far less data and compute. [T3][S-0262][S-0263]
- "An ensemble is only as good as its members" — averaging many weakly correlated high-variance learners reduces variance (bagging), and boosting builds strong learners from weak ones; the member itself is not the bottleneck. [T1][S-0262][S-0263]
- "More regularization is always safer" — regularization trades bias for variance; too much shrinks the model into underfitting, which is exactly why the strength is chosen on validation data. [T1][S-0257]
- "Logistic regression is just a weak linear classifier" — it is a probabilistic model: the sigmoid on log-odds gives probabilities and interpretable coefficients, which matters when decisions need explanations, not just boundaries. [T3][S-0268]
- "SVMs are obsolete" — the max-margin + kernel combination remains the canonical demonstration that inductive bias buys generalization, and kernel methods still appear across modern methods. [T3][S-0264]
- "Imbalanced data must be resampled" — fix evaluation first (PRC, precision/recall); the remedy depends on whether you need to catch positives (recall) or be precise among alerts (precision). [T1][S-0259]

## References (evidence records)

- S-0257 — Kohavi (1995) — cross-validation vs bootstrap for model selection; resubstitution bias; 10-fold stratified CV.
- S-0259 — Saito & Rehmsmeier (2015) — PRC vs ROC under class imbalance; precision/recall behavior.
- S-0262 — Breiman (2001) — random forests; error converges with tree count; variance reduction via decorrelated trees.
- S-0263 — Friedman (2001) — gradient boosting as function-space steepest descent; stagewise additive models.
- S-0264 — Cortes & Vapnik (1995) — support-vector networks; max-margin; kernel mapping.
- S-0268 — Goodfellow, Bengio & Courville (2016) — textbook: linear models, losses, gradient-based optimization, regularization.
