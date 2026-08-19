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
status: draft
schema-version: 1
owner: l1-ml-fundamentals
reviewed-by: []
updated: 2026-08-18
sources: [S-0018, S-0257, S-0258, S-0259]
---

# ML Fundamentals

## Claims

### ML problem framing

- CS2023's Artificial Intelligence knowledge area includes a Machine Learning knowledge unit designated KA-core (required content for all majors), spanning the core learning paradigms. [T2][S-0018]
- The curriculum distinguishes three paradigms: supervised learning (learning from labeled examples to predict outputs), unsupervised learning (finding structure in unlabeled data), and reinforcement learning (an agent learning from interaction with an environment through evaluative feedback). [T2][S-0018]

### Train/test/validation split

- Training error is an optimistically biased estimate of generalization error: the model is fitted to the training data, so its score there is not independent — the resubstitution bias that Kohavi's large-scale study measures across real-world datasets. [T1][S-0257]
- In Kohavi's experiment (over half a million runs of C4.5 and Naive-Bayes), ten-fold stratified cross-validation was the best model-selection method among those studied — better balanced than leave-one-out and than bootstrap variants. [T1][S-0257]

### Overfitting and bias-variance

- Overfitting is the regime where a model fits the training data far better than it generalizes; the empirical signature is the systematic gap between resubstitution and cross-validated accuracy that Kohavi quantifies. [T1][S-0257]
- A model that wins on training error can lose on generalization — model selection must be performed on held-out (validation) or cross-validated scores, never on training fit alone. [T1][S-0257]

### Evaluation metrics

- Precision = TP/(TP+FP): the fraction of positive predictions that are actually positive (equivalent to positive predictive value). [T1][S-0259]
- Recall = TP/(TP+FN): the fraction of actual positives that are predicted positive (equivalent to sensitivity / true positive rate). [T1][S-0259]
- The ROC curve plots true positive rate against false positive rate over all decision thresholds; AUC summarizes it as a single number, with 0.5 = random and 1.0 = perfect. [T1][S-0259]
- In precision-recall space the baseline of a random classifier is P/(P+N) — it shifts with class distribution — whereas the ROC diagonal baseline does not; the two plots are one-to-one but answer different questions. [T1][S-0259]

### Data quality and leakage

- Data leakage — information not legitimately available at prediction time entering the training process, via features or via training samples — can produce near-perfect cross-validated performance while the deployed model fails. [T1][S-0258]
- Because training and test splits share the leaked information, ordinary cross-validation validates the leak rather than the model — which is why Kaufman et al. prescribe structural prevention ("learn-predict separation": include a feature only if it is legitimate for inferring the target) instead of post-hoc detection. [T1][S-0258]

### Model evaluation pitfalls

- Pitfall: choosing the model that scores best on the training set — resubstitution-based selection systematically overstates expected accuracy. [T1][S-0257]
- Pitfall: reporting accuracy on imbalanced data — simulations and a literature re-analysis show ROC plots can look deceptively good while precision among positive predictions is poor; precision-recall plots expose it. [T1][S-0259]
- Pitfall: feature-level leakage (using information that only exists because the target was observed, e.g., target-derived statistics or future information) — it inflates evaluation without any error message. [T1][S-0258]

## Details

The evaluation loop: split data (train / validation / test) before any data-dependent computation → fit on train → select hyperparameters and models on validation (or k-fold CV) → report once on test. The bias-variance decomposition — expected squared loss = noise + bias² + variance — is the mechanism behind overfitting: flexible models reduce bias but raise variance; the generalization optimum sits between the two, which is why training error alone is a poor selector. Leakage breaks the loop silently: it inserts prediction-time-illegitimate information into training, so every downstream score is a confidence in the wrong model.

## Boundaries / common misunderstandings

- "More data is always better / fixes models" — data volume does not fix leakage, biased sampling, or label noise; a large contaminated dataset yields a confidently wrong model. [T1][S-0258]
- "Leakage is rare, just peeking at the test set" — leakage via features and samples is common and silent; it invalidates evaluation with no error message. [T1][S-0258]
- "High training accuracy means a good model" — resubstitution is optimistically biased; only held-out or cross-validated estimates count. [T1][S-0257]
- "Accuracy is the right metric for every problem" — on imbalanced classes accuracy can stay high while the model is useless; precision/recall or PRC tell the real story. [T1][S-0259]
- "More complex models are always better" — complexity trades bias for variance; past the optimum, generalization degrades even as training error falls, so selection must use validation/CV scores. [T1][S-0257]

## References (evidence records)

- S-0018 — CS2023 (ACM/IEEE-CS/AAAI, 2024) — AI KA: Machine Learning knowledge unit (KA-core), three paradigms.
- S-0257 — Kohavi (1995) — large-scale study of CV/bootstrap; resubstitution bias; 10-fold stratified CV for model selection.
- S-0258 — Kaufman, Rosset, Perlich & Stitelman (2012) — leakage formulation, detection, avoidance; learn-predict separation.
- S-0259 — Saito & Rehmsmeier (2015) — confusion-matrix metrics, ROC/AUC, PRC baselines; imbalance findings.
