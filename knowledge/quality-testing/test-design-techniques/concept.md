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
status: published
schema-version: 1
owner: l1-test-design-techniques
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0208, S-0212, S-0213, S-0214]
---

# Test Design Techniques

## Claims

- Test design techniques are systematic procedures for selecting test cases from the potentially infinite execution domain of a program, aiming at effective defect finding with minimal redundant cases [T2][S-0017].
- Equivalence partitioning divides the input domain into equivalence classes — sets of values the implementation is expected to treat alike — and selects one representative from each class, including invalid classes, as test input [T2][S-0017].
- Boundary value analysis tests values at and immediately around the boundaries of equivalence classes and valid ranges, because defects cluster at boundaries of conditions, ranges, and loops [T2][S-0017].
- Decision tables capture condition–action logic as rules (combinations of conditions mapped to actions); each rule is exercised by at least one test case, giving systematic coverage of specifications rich in such logic [T2][S-0017].
- State-transition testing models the system as states and event-triggered transitions and derives tests that exercise states, transitions, and transition pairs; it applies wherever behavior is specified as a state model [T2][S-0017].
- In NIST's analysis of naturally occurring failures across medical-device, browser, server, NASA, and network-security systems, 65–97% of failures were triggered by one- or two-variable interactions, and 4- to 6-way interaction coverage reached 96–100% of failures [T1][S-0212].
- No studied domain in the NIST failure analysis required more than six interacting variables, so n-way combinatorial testing with small n acts as pseudo-exhaustive testing: it covers the observed failure-triggering interaction space without exhaustive combination enumeration [T1][S-0212].
- White-box (structural) criteria use program internals: statement coverage executes every statement, branch/decision coverage exercises both outcomes of every decision, and condition coverage tests each atomic condition for both truth values [T2][S-0017].
- Mutation testing seeds artificial defects (mutants) into the program and uses the percentage of mutants killed by the suite (mutation score) as a test adequacy criterion [T1][S-0214].
- In a controlled experiment, the difficulty of detecting mutants was statistically similar to that of detecting real faults (SPACE program), supporting mutation score as a proxy for real fault detection when comparing testing techniques [T1][S-0213].
- Mutation-based adequacy is among the most effective yet most computationally expensive criteria; cost is managed through selective mutation, weak mutation, mutant sampling, and equivalent-mutant detection [T1][S-0214].
- Coverage-based adequacy has limits: statement, decision, and modified-condition coverage each correlate only low-to-moderately with a suite's fault-detection effectiveness once suite size is controlled, so high coverage is necessary but not sufficient for suite quality [T1][S-0208].

## Details

- Techniques are complementary views of the artifact — specification-based (partitioning, boundaries, tables, state models) versus structure-based (coverage criteria) — and combining them is the norm rather than an either/or choice [T2][S-0017].
- Technique selection follows the available artifact and the dominant failure risk: decision tables for condition-rich requirements, state-transition for stateful behavior, pairwise when parameter interactions explode, mutation for adequacy assessment [T2][S-0017].
- The NIST interaction data is the empirical basis for the "interaction rule" behind pairwise testing: interactions of a few parameters cause most failures, so covering all 2-way (or n-way) combinations is a cost-effective substitute for full combination testing [T1][S-0212].

## Boundaries / common misunderstandings

- "Coverage is a guarantee": coverage measures which code ran, not what behavior was asserted; a suite can reach 100% statement or branch coverage while asserting almost nothing, and correlation with effectiveness is weak once suite size is controlled [T1][S-0208].
- "Equivalence partitioning means testing every value in the class": a class is represented by one value; but classes must be derived from the specification, so the quality of the result depends on the quality of that analysis [T2][S-0017].
- "Pairwise testing is exhaustive": it covers all two-variable interactions, not all combinations — defects requiring three or more interacting variables escape 2-way coverage; the NIST data bounds the residual risk, it does not eliminate it [T1][S-0212].
- "A 100% mutation score proves correctness": mutants are proxies for real faults, and equivalent mutants (behaviorally identical to the original) cannot be killed, so mutation score is an adequacy signal, not a correctness proof [T1][S-0213].
- "Mutation testing is a black-box technique": it is an adequacy criterion evaluated on the suite, and its cost (compilation and execution of each mutant) is prohibitive without the documented cost-reduction strategies [T1][S-0214].

## References (evidence records)

- [S-0017] IEEE Computer Society 2024 — SWEBOK v4.0, Software Testing KA (technique families: EP/BVA, decision tables, state-transition, structural coverage).
- [S-0208] Inozemtseva & Holmes 2014 — Coverage Is Not Strongly Correlated with Test Suite Effectiveness (ICSE'14).
- [S-0212] Kuhn, Wallace & Gallo 2004 — Software Fault Interactions and Implications for Software Testing (NIST; TSE).
- [S-0213] Andrews, Briand & Labiche 2005 — Is Mutation an Appropriate Tool for Testing Experiments? (ICSE'05).
- [S-0214] Papadakis et al. 2018 — Mutation Testing Advances: An Analysis and Survey (Advances in Computers).
