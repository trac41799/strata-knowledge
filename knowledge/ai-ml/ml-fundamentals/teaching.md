---
id: ai-ml/ml-fundamentals
title: ML Fundamentals
band: B4
track: ai-ml
tier: T1
bloom_target: apply
prerequisites: [cs-foundations/probability-statistics]
related: [ai-ml/supervised-learning, ai-ml/neural-networks]
recommended: []
status: published
schema-version: 1
owner: l1-ml-fundamentals
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0018, S-0257, S-0258, S-0259]
---

# ML Fundamentals — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: state the three learning paradigms, the precision/recall formulas, and what AUC values 0.5 and 1.0 mean. [T0][S-0259]
- **understand**: explain why training error is optimistically biased, why leakage is silent, and why PRC baselines move with class distribution. [T1][S-0257][S-0258][S-0259]
- **apply**: choose a split/CV protocol, compute precision/recall/AUC-interpretation from a confusion matrix, and audit a pipeline for leakage. [T1][S-0257][S-0258][S-0259] **bloom_target**
- **analyze**: classify pipeline findings as feature- vs sample-level leakage and reason about what each evaluation metric can and cannot reveal. [T1][S-0258][S-0259]

## Worked example — overfitting demonstration + metric computation

Setup: regression on 15 points sampled from y = sin(2πx) + noise; fit polynomials of degree 1, 3, and 9 with least squares; 10 points for training, 5 held out.

1. **Fit and score.** Degree 1: train MSE 0.31, test MSE 0.47. Degree 3: train 0.09, test 0.12. Degree 9: train 0.02, test 0.58. The degree-9 polynomial interpolates the training noise — training error keeps falling while test error rises. This is the empirical overfitting signature; selecting on training fit alone picks the worst model. [S-0257]
2. **Why.** The bias-variance decomposition, expected squared loss = noise + bias² + variance, predicts it: degree 1 has high bias (can't represent the curve), degree 9 has high variance (wiggles follow the noise); degree 3 sits at the optimum. Complexity trades bias for variance. [S-0257]
3. **Choose the model properly.** Ten-fold stratified CV over degrees 1..9 selects degree 3 (lowest CV error); the untouched test set, scored once, confirms. [S-0257]
4. **Metric computation on the selected classifier.** Suppose at the chosen threshold on a 200-row test set: TP=40, FP=10, FN=5, TN=145. Precision = 40/50 = 0.80; recall = 40/45 = 0.889; accuracy = 0.925. If the production class ratio is 1:99 instead of 45:155, accuracy transfers poorly — the PRC baseline P/(P+N) shifts, so report precision/recall and the operating threshold. [S-0259]
5. **Leakage check.** Before trusting any of it: was normalization fit on train only? Any duplicated rows across splits? Any feature that only exists because the target was observed? A positive answer invalidates every number above. [S-0258]

## Elaboration prompts

- Resubstitution bias: the model was fitted to the data it is scored on. Why is "fitting well" on train actively misleading for selection, and which score does Kohavi's study say to trust instead? [T1][S-0257]
- The bias-variance decomposition is an identity under squared loss: noise + bias² + variance. Walk through what happens to each term as model complexity grows — and why the minimum of their sum is not at the complexity that minimizes training error. [S-0257]
- PRC baselines move with P/(P+N); ROC baselines do not. What does that difference imply for comparing models across datasets with different class ratios? [T1][S-0259]
- Kaufman et al. propose "learn-predict separation" — asking whether each feature is legitimate for inferring the target. Apply that question to a time-series feature, an ID column, and a leaky campaign flag. [T1][S-0258]
- "More data" is the first instinct when a model underperforms. Given the evidence, what should be the first three checks before adding data? [T1][S-0258]

## Common misconceptions

1. **"High training accuracy means a good model."** Resubstitution is optimistically biased; the model was fitted to those examples. Held-out or cross-validated estimates are the only trustworthy ones. [T1][S-0257]
2. **"Leakage is just peeking at the test set."** Leakage arrives through features and samples and is silent — near-perfect CV scores with no error message. Prevention must be structural (learn-predict separation). [T1][S-0258]
3. **"More data fixes everything."** Volume does not fix leakage, biased sampling, or label noise; a larger contaminated dataset is a more confidently wrong model. [T1][S-0258]
4. **"Accuracy is the universal metric."** On imbalanced classes accuracy hides failure; precision/recall and PRC expose it (ROC can look deceptively good). [T1][S-0259]
5. **"Bigger models are better models."** Complexity trades bias for variance; past the optimum, generalization degrades even as training error falls. [T1][S-0257]

## Feynman targets

Explain in plain language a non-engineer could follow:

- Why grading a student on the exact homework they were trained on is meaningless — the test must be a different exam, and choosing the model on the training score is like choosing an answer key by how well it fits the questions it was made for.
- Why a fraud detector claiming 98% accuracy can still be useless when fraud is 1 in 1000 — and why you must ask "of the alerts we fire, how many are real?" (precision) and "of the real fraud, how much do we catch?" (recall).
- Why "the exam paper was leaked to the students" explains suspiciously perfect scores — and why more students (more data) makes a leaked exam look even more convincing, not less.

## Interleaving hooks

- **cs-foundations/probability-statistics (prerequisite)**: precision and recall are conditional probabilities; Bayes' theorem explains why precision depends on class priors while recall does not; expectation/variance are the raw material of the bias-variance decomposition.
- **ai-ml/supervised-learning and ai-ml/neural-networks (related)**: every concrete algorithm inherits this topic's discipline — supervised methods are fit on train, tuned on validation, and judged by the metrics defined here; neural networks make the overfitting curve sharper and leakage more expensive.
- **data/relational-model (related)**: joins and ETL are where feature-level leakage is born (target-derived aggregates), so data engineering knowledge is the practical guardrail for learn-predict separation.
