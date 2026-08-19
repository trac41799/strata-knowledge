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

# Supervised Learning — validation

## Formative (practice)

### Q1
- Q: State what L1 (lasso) and L2 (ridge) penalties penalize, and name the property that only L1 has.
- bloom: remember
- bank: formative
- A: Both add a penalty on the coefficient vector to the loss — L2 adds λΣw² (sum of squares), L1 adds λΣ|w| (sum of absolute values). Both shrink coefficients toward zero, but L1 drives some weights exactly to zero, so it performs feature selection; L2 only shrinks.
- evidence: [S-0268]
- topic: ai-ml/supervised-learning

### Q2
- Q: Explain, in one sentence each, why bagging reduces variance and why boosting reduces bias.
- bloom: understand
- bank: formative
- A: Bagging averages predictions of learners trained on independent bootstrap resamples, so the independent error components cancel — variance shrinks while bias is unchanged. Boosting adds learners that fit the residual error of the ensemble so far (gradient descent in function space), so the combined model can represent targets the individual weak learners could not — bias shrinks.
- evidence: [S-0262][S-0263]
- topic: ai-ml/supervised-learning

### Q3
- Q: You must build a churn classifier from 20k tabular rows with 5% positive class. Choose the model family, the selection protocol, and the reported metrics; justify each choice.
- bloom: apply
- bank: formative
- A: Model family: a tree ensemble (random forest or gradient boosting) — the standard default for tabular data, robust with little tuning (Breiman/Friedman). Selection: ten-fold stratified cross-validation to compare a few families and hyperparameter settings — stratified because it preserves the 5% minority ratio per fold (Kohavi). Metrics: precision, recall, and PRC at the operating threshold, not accuracy and not ROC alone — with a 5% base rate, accuracy is dominated by the majority class and ROC can look deceptively good (Saito & Rehmsmeier). Fix selection and reporting before tuning anything.
- evidence: [S-0257][S-0259][S-0262][S-0263]
- topic: ai-ml/supervised-learning

## Summative (mastery checkpoint)

### Q4
- Q: Ridge regression with λ=0 scores train 0.02 / test 0.58; with λ=10 it scores train 0.11 / test 0.19. Explain the numbers with bias-variance and state which model you ship and why.
- bloom: apply
- bank: summative
- A: λ=0 overfits: the model fits the training noise (low bias, high variance), and the gap 0.02 vs 0.58 is the overfitting signature. λ=10 regularizes: it accepts higher bias (train error rises to 0.11) to cut variance (test 0.19). Shipping: the λ=10 model, because its estimate of generalization is far better; λ was chosen on validation/CV error, never on train error (resubstitution is optimistically biased — Kohavi).
- evidence: [S-0257][S-0268]
- topic: ai-ml/supervised-learning

### Q5
- Q: A team reports: random forest wins on training accuracy, gradient boosting wins on validation. Interpret the result and prescribe the selection protocol.
- bloom: analyze
- bank: summative
- A: Training accuracy is the resubstitution score — optimistically biased because both models were fitted to those examples; a win there carries no selection information. Boosting typically fits training data even harder than bagging (it chases residuals), so the RF train-win is unremarkable. The validation comparison is the selection evidence: pick the GBM if it holds up on cross-validated scores, confirm the margin with 10-fold stratified CV, then score the chosen model once on untouched test data. Report the test number as the final estimate, not the validation number used for selection.
- evidence: [S-0257][S-0262][S-0263]
- topic: ai-ml/supervised-learning

### Q6
- Q: A teammate says: "We always use random forests with default parameters; they never overfit." Critically evaluate the claim.
- bloom: evaluate
- bank: summative
- A: Partial: random forests do not overfit as the number of trees grows — Breiman proves the generalization error converges as trees are added. But "defaults never overfit" is false: RF still overfits on noise-dominated data, and per-tree depth/features (max depth, min leaf size, feature subset size) still control the bias-variance tradeoff — deep fully-grown trees on a small dataset still memorize. The no-overfit property concerns forest size, not tree complexity; validate depth/feature choices on held-out data like any other hyperparameter.
- evidence: [S-0262][S-0257]
- topic: ai-ml/supervised-learning

### Q7
- Q: For L(w) = (w−3)² starting at w=5 with η=0.1, compute two gradient-descent steps and show the loss is decreasing.
- bloom: apply
- bank: summative
- A: ∇L = 2(w−3). Step 1: at w=5, ∇=4 → w = 5 − 0.1·4 = 4.6, L=2.56. Step 2: at w=4.6, ∇=3.2 → w = 4.6 − 0.1·3.2 = 4.28, L=1.6384. Loss falls 4 → 2.56 → 1.6384 and w approaches the optimum 3; with η=1 the step at w=5 overshoots by the full distance and the update oscillates between 5 and 1, and η>1 diverges — the instability of too-large learning rates.
- evidence: [S-0268]
- topic: ai-ml/supervised-learning

## Review (spaced repetition — interleaved with prerequisites)

### Q8
- Q: Why did Kohavi's study single out ten-fold stratified cross-validation for model selection, and what does stratification buy you on a dataset with a rare class?
- bloom: understand
- bank: review
- A: Among the methods compared (over half a million runs of C4.5 and Naive-Bayes), ten-fold stratified CV balanced bias and variance best: better than leave-one-out (costly, higher variance) and than bootstrap variants (low variance but biased on some datasets). Stratification preserves the class ratio in every fold, so the rare class is represented in each training fold and each evaluation fold — critical when the positive class is a few percent.
- evidence: [S-0257]
- topic: ai-ml/ml-fundamentals

### Q9
- Q: A fraud model reports AUC 0.98 but PRC area 0.05. What does the gap tell you, and which number should the product owner trust for "how good are our alerts?"
- bloom: apply
- bank: review
- A: AUC 0.98 with near-zero PRC means the ranking is good in aggregate but precision among the top-scored positives is terrible — exactly the deceptive-ROC regime on imbalanced data: with few positives, a drop in recall looks small in ROC space but collapses the PRC. The product owner should trust precision at the operating threshold (and the PRC), because alerts are what get acted on: "of the alerts we fire, how many are real?" The PRC baseline P/(P+N) also shifts with the deployment base rate, so report at the real rate.
- evidence: [S-0259]
- topic: ai-ml/ml-fundamentals

### Q10
- Q: Why does adding trees to a random forest reduce variance without overfitting, while adding depth to a single tree overfits?
- bloom: analyze
- bank: review
- A: Averaging decorrelates: each tree's error has an independent component that cancels across trees, so variance falls as the forest grows and the generalization error converges to a limit (Breiman) — the bagging property, independent of depth. Depth increases a single tree's capacity: the tree memorizes training noise, its error stays correlated with the data (variance grows), and the train/validation gap widens — the bias-variance tradeoff that selection on validation scores (Kohavi) exists to manage.
- evidence: [S-0262][S-0257]
- topic: ai-ml/supervised-learning
