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

# ML Fundamentals — validation

## Formative (practice)

### Q1
- Q: Write the formulas for precision and recall from a confusion matrix, and state what each measures in plain words.
- bloom: remember
- bank: formative
- A: Precision = TP/(TP+FP) — of everything the model called positive, the fraction that was actually positive. Recall = TP/(TP+FN) — of everything actually positive, the fraction the model found. (Precision ≡ PPV; recall ≡ sensitivity ≡ TPR.)
- evidence: [S-0259]
- topic: ai-ml/ml-fundamentals

### Q2
- Q: A model scores 97% accuracy on its training set and 71% on the held-out test set. Explain what happened, using the concept of resubstitution bias.
- bloom: understand
- bank: formative
- A: The training score is not an independent measurement: the model was fitted to those exact examples, so its error there is optimistically biased (resubstitution). The gap (97 vs 71) is the signature of that bias and of overfitting — the model memorized training patterns that do not generalize. The test set, never used for fitting or selection, is the trustworthy number.
- evidence: [S-0257]
- topic: ai-ml/ml-fundamentals

### Q3
- Q: You have 200 labeled records of a rare disease (12 positives) and must pick the better of two classifiers. Choose the evaluation protocol and justify it; state which metrics you would report.
- bloom: apply
- bank: formative
- A: Use stratified ten-fold cross-validation for model selection (Kohavi's finding: best among the methods studied, and stratification preserves the rare-class ratio in every fold). Do not select on training accuracy (resubstitution bias). Report class-specific metrics — precision, recall, and PRC — rather than accuracy, because with 12/200 positives accuracy is dominated by the majority class and can hide a useless classifier.
- evidence: [S-0257][S-0259]
- topic: ai-ml/ml-fundamentals

## Summative (mastery checkpoint)

### Q4
- Q: A classifier on a test set of 200 records produces TP=40, FP=10, FN=5, TN=145. Compute precision, recall, and accuracy; interpret the numbers for a fraud-detection context where negatives dominate in production.
- bloom: apply
- bank: summative
- A: Precision = 40/(40+10) = 0.80; recall = 40/(40+5) = 0.889; accuracy = 185/200 = 0.925. In production the class ratio will be far more imbalanced than 45:155; precision and recall (and the PRC baseline P/(P+N)) depend on the operating class distribution, so the accuracy figure is the least transferable — a 92.5% accuracy is compatible with very different precision/recall tradeoffs, and reporting all three (plus the operating threshold) is required.
- evidence: [S-0259]
- topic: ai-ml/ml-fundamentals

### Q5
- Q: Audit this pipeline for leakage and classify each finding as feature-level or sample-level: (a) min-max normalization fitted on the full dataset before the split; (b) duplicate patient records spanning train and test; (c) a feature "discount status" computed from a future campaign table; (d) hyperparameter tuning with repeated peeks at the test set.
- bloom: analyze
- bank: summative
- A: (a) feature-level leakage — scale statistics are derived from test values, so test information enters training; fix by fitting normalization on the training split only. (b) sample-level leakage — near-duplicates of test rows are learnable; fix by deduplication before splitting. (c) feature-level leakage — the feature encodes information not available at prediction time (a "future"); fix by excluding it (learn-predict separation: is x legitimate for inferring y?). (d) not leakage but evaluation corruption — the test set is no longer untouched; its score becomes an overfit estimate.
- evidence: [S-0258]
- topic: ai-ml/ml-fundamentals

### Q6
- Q: A team reports "98% AUC on 10-fold CV" for fraud detection. Enumerate at least three distinct checks you would run before trusting the number, and justify each from the evidence.
- bloom: evaluate
- bank: summative
- A: (1) Leakage audit — with AUC this high on fraud data, check for target-derived features, duplicates across folds, and preprocessing before the split (Kaufman: leaked models show exactly this near-perfect signature). (2) Metric fit — on imbalanced fraud data, report PRC/precision-recall and the operating threshold; ROC/AUC can look deceptively good (Saito & Rehmsmeier). (3) Selection honesty — CV scores used to tune models are themselves optimistic; the final number must come from a test set touched once (Kohavi: resubstitution and selection-induced optimism). (4) Label quality — verify the ground truth was available at prediction time.
- evidence: [S-0258][S-0259][S-0257]
- topic: ai-ml/ml-fundamentals

## Review (spaced repetition — interleaved with prerequisites)

### Q7
- Q: Precision is often described as "the probability that a prediction is correct given that it is positive". Express precision as a conditional probability and state the Bayes factor you would need to compare two classifiers' precisions. (Probability & statistics interleave.)
- bloom: apply
- bank: review
- A: Precision = P(actual positive | predicted positive) = P(predicted+ | actual+) · P(actual+) / P(predicted+) by Bayes' theorem — i.e., recall (TPR) times the prior base rate divided by the model's positive-prediction rate. Comparing precisions requires the priors/operating conditions, since precision depends on class distribution while recall does not — the mathematical reason PRC baselines shift with P/(P+N).
- evidence: [S-0018][S-0259]
- topic: cs-foundations/probability-statistics

### Q8
- Q: Your team doubles the dataset and re-runs the same pipeline; CV accuracy jumps from 0.78 to 0.97. Argue for or against "more data fixed the model" and name the alternative explanation the evidence supports.
- bloom: analyze
- bank: review
- A: The jump is suspicious, not automatically good: doubling a dataset cannot fix a leaked pipeline — a large contaminated dataset yields a confidently wrong model (Kaufman). If the new data introduced duplicates, target-derived features, or changed preprocessing, the gain may be measurement of the leak. Check: split hygiene (dedupe before split, fit preprocessing on train only), feature legitimacy, then re-estimate on an untouched test set. Data volume helps only when the pipeline is clean.
- evidence: [S-0258]
- topic: ai-ml/ml-fundamentals

### Q9
- Q: Why did Kohavi's study recommend ten-fold stratified cross-validation over leave-one-out and bootstrap for model selection, and what bias does training-set selection introduce that CV corrects?
- bloom: understand
- bank: review
- A: On real-world datasets the ten-fold stratified estimate balanced bias and variance better than leave-one-out (expensive, high variance) and than bootstrap variants (low variance, but biased on some datasets). Training-set (resubstitution) selection is optimistically biased because the model was fitted to the same examples it is scored on; CV scores each fold's model on data it never saw, removing that bias.
- evidence: [S-0257]
- topic: ai-ml/ml-fundamentals
