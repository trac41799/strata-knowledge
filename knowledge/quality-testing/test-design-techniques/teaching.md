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

# Test Design Techniques — teaching

## Learning objectives (Bloom)

By the end of this topic, the learner can:

- remember: name the specification-based (EP, BVA, decision tables, state-transition, pairwise) and structure-based (statement/branch/condition coverage, mutation) technique families.
- understand: explain why boundary values and few-variable interactions concentrate defects.
- apply (target): derive test cases from an input domain, a decision table, a state model, and a parameter set; compute coverage criteria for a small program.
- analyze: interpret coverage and mutation-score numbers as adequacy signals with documented limits.
- evaluate: choose a technique mix for a given artifact and risk profile.

## Worked example — partition + BVA on a real function

Specification: `bookingFee(days)` returns 10 for 1–3 days, 25 for 4–10 days, and an error otherwise.

1. **Partition first.** Classes from the spec: valid 1–3, valid 4–10, invalid 0, invalid negative, invalid non-numeric. Note the two valid classes have different behavior — merging them into "valid 1–10" would silently accept one expected-result branch untested.
2. **Then boundaries.** For each class, test the boundary points: 1, 3, 4, 10, plus one interior value per class (2, 7) and one value past each boundary (0, 11). Add a non-numeric representative.
3. **Oracle.** Expected results come from the spec: 10, 10, 25, 25; errors for 0, 11, "x". Now every test is decidable — a test without an oracle is an observation, not a test.
4. **Why not test every value?** 1–10 are 10 values plus invalids; the chosen set (9 cases) covers all boundary decisions. Defects cluster at boundaries, so interior values add little.

## Worked example — pairwise instead of exhaustive

A config dialog has 4 parameters (browser × OS × region × auth) with 3 values each = 81 combinations. Exhaustive testing of the UI is slow and brittle. Using pairwise, build a covering array of all 2-way combinations (≈ 9–13 rows) — the NIST data says 65–97% of failures are triggered by 1–2 variable interactions, so the array covers the dominant failure space at a fraction of the cost. Remember what is sacrificed: a 3-way interaction bug would need 3-way (or higher) coverage to be guaranteed found.

## Elaboration prompts

- Why do boundary conditions and loops concentrate defects — what does the implementation actually do at `<=` vs `<`?
- Your decision table has two rules with identical actions. Should you merge them? What does merging cost you in defect diagnosis?
- When is pairwise coverage the wrong answer, and what does the 96–100% figure for 4- to 6-way coverage imply about the cost of more rows?
- Why is mutation score "among the most effective yet most expensive" — where does the cost come from?
- If coverage correlates weakly with effectiveness, what should your team's coverage target actually be used for?

## Common misconceptions

- "100% coverage means no bugs." Coverage is necessary, not sufficient; it measures which code ran, not what was asserted. A suite of logic-free getter tests can hit 100% statement coverage while detecting nothing (S-0208).
- "Equivalence partitioning = test one value per input field." The class boundaries come from the specification's behavior, not from the input widget; two valid classes with different expected behavior must both be tested (S-0017).
- "Pairwise testing covers everything." It covers all two-variable interactions; failures needing three or more interacting variables escape it (S-0212).
- "Mutation score measures real faults directly." Mutants are a proxy with statistically similar difficulty, and equivalent mutants can never be killed — score 100% is a goal, not a correctness proof (S-0213).
- "State-transition testing is only for code with explicit state machines." It applies to any behavior specified as states/events — protocols, workflows, UI flows — even when the code has no visible state machine (S-0017).

## Feynman targets

Explain to a non-tester, without jargon: (1) why testing one representative per equivalence class is enough; (2) why pairwise testing exists (the "defects come in pairs" intuition); (3) what mutation testing is and why it is expensive; (4) why coverage is a floor, not a ceiling.

## Interleaving hooks

- From software-testing-basics: the oracle concept underpins every technique here — re-derive the oracle for the decision-table example.
- Forward to test-automation: which of these techniques produce the tests you will automate, and which automate badly (e.g., manual state-transition exploration)?
- Forward to code-review: coverage and mutation numbers are review inputs, not review substitutes.
- From quality-models: map each technique to the ISO 25010 characteristic it protects (correctness → EP/BVA; robustness → invalid classes).
