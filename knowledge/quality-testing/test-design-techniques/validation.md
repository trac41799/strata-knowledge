---
id: quality-testing/test-design-techniques
title: Test Design Techniques
band: B4
track: quality-testing
tier: T1
bloom_target: apply
prerequisites: [quality-testing/software-testing-basics]
related: [quality-testing/test-automation, quality-testing/code-review, quality-testing/quality-models]
recommended: [quality-testing/test-automation]
status: draft
schema-version: 1
owner: l1-test-design-techniques
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0208, S-0212, S-0213, S-0214]
---

# Test Design Techniques — validation

## Formative (practice)

- Q: What is equivalence partitioning, and why does it reduce the number of test cases needed?
- bloom: remember
- bank: formative
- A: It divides the input domain into equivalence classes — sets of values the implementation is expected to treat alike — and tests one representative from each class (valid and invalid) instead of every value.
- evidence: [S-0017]
- topic: quality-testing/test-design-techniques

- Q: Why do defects tend to cluster at boundaries of ranges and conditions?
- bloom: understand
- bank: formative
- A: Implementations typically compare with relational operators at boundaries (off-by-one in conditions and loops); values at or immediately around the boundary exercise the code's edge decisions, so boundary value analysis adds boundary points to each equivalence class.
- evidence: [S-0017]
- topic: quality-testing/test-design-techniques

- Q: A function `validateAge(age)` accepts ages 18–65 inclusive and rejects everything else. Derive the equivalence classes and the boundary-value test inputs.
- bloom: apply
- bank: formative
- A: Classes: valid [18,65]; invalid below (<18); invalid above (>65); non-numeric input as an additional class. Boundary tests: 17 (below-valid), 18 (valid lower), 65 (valid upper), 66 (above-valid); representatives 25 (valid interior), 0 (invalid interior).
- evidence: [S-0017]
- topic: quality-testing/test-design-techniques

- Q: A login feature has two conditions — "valid user exists" and "password correct" — and actions "grant access" and "reject". Build the decision table and state the test cases.
- bloom: apply
- bank: formative
- A: Four rules: (valid user=T, password=T) → grant; (T,F) → reject; (F,T) → reject; (F,F) → reject. One test per rule covers the table; the "reject" rules disambiguate which condition failed in the oracle.
- evidence: [S-0017]
- topic: quality-testing/test-design-techniques

- Q: A screen has 3 parameters with 3 values each (27 combinations). Using the NIST interaction data, justify testing only pairwise combinations and bound what is left uncovered.
- bloom: apply
- bank: formative
- A: NIST found 65–97% of failures across six domains triggered by one- or two-variable interactions, so a covering array of all pairs (roughly 9–12 rows) captures the dominant failure space. Residual risk: defects needing 3+ interacting variables are missed; 4- to 6-way coverage would raise capture to 96–100% at higher cost.
- evidence: [S-0212]
- topic: quality-testing/test-design-techniques

## Summative (mastery checkpoint)

- Q: Given `if (a > 0 && b > 0) { X } else { Y }`, design the minimal set of tests that achieves 100% branch coverage, and state what condition coverage additionally demands.
- bloom: apply
- bank: summative
- A: Two tests achieve branch coverage: (a>0, b>0) → X; (a<=0 or b<=0) → Y. Condition coverage additionally requires each atomic condition's truth values: a>0 true and false, b>0 true and false — e.g., (T,T), (F,T), (T,F) — three tests.
- evidence: [S-0017]
- topic: quality-testing/test-design-techniques

- Q: Your suite reaches 100% branch coverage yet a defect ships to production. Explain why this outcome is expected rather than surprising, citing the evidence.
- bloom: analyze
- bank: summative
- A: Coverage is weakly correlated with fault-detection effectiveness once suite size is controlled; coverage says which code ran, not which behavior was asserted. The suite may lack oracles or assert trivial properties (e.g., getters), so 100% coverage is necessary but not sufficient.
- evidence: [S-0208]
- topic: quality-testing/test-design-techniques

- Q: Your team proposes replacing statement-coverage targets with a 100% mutation score. Give a reasoned evaluation of the proposal, including costs and mitigations.
- bloom: evaluate
- bank: summative
- A: Mutation score is among the most effective adequacy criteria and empirically approximates real-fault detection difficulty, so it is a stronger quality gate. But it is computationally expensive, and equivalent mutants cannot be killed, so 100% is typically unreachable or noisy; mitigate with selective mutation, weak mutation, sampling, and equivalent-mutant detection, and keep coverage as a complement.
- evidence: [S-0214][S-0213]
- topic: quality-testing/test-design-techniques

## Review (spaced repetition — interleaved with prerequisites)

- Q: Why can testing demonstrate the presence of defects but never prove their absence?
- bloom: understand
- bank: review
- A: Testing executes a finite, carefully selected subset of an infinite execution domain; passing the subset certifies behavior only on those cases — the oracle verdicts do not generalize to all possible executions.
- evidence: [S-0017]
- topic: quality-testing/software-testing-basics

- Q: What is an oracle, and why does a test without one produce no test result?
- bloom: remember
- bank: review
- A: An oracle is the means of deciding whether observed behavior is acceptable (specification, reference system, or expected result). Without it, executing the program is observation, not verification — there is no pass/fail verdict.
- evidence: [S-0017]
- topic: quality-testing/software-testing-basics

- Q: Legacy code has no tests and you must change it. What entry point does the seams model give you, and which kind of test do you write first?
- bloom: apply
- bank: review
- A: A seam is a place to alter behavior without editing in that place, with an enabling point for choosing behavior; write characterization tests through the seams to lock in current behavior before changing it.
- evidence: [S-0139]
- topic: quality-testing/software-testing-basics
