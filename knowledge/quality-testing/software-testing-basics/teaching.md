---
id: quality-testing/software-testing-basics
title: Software Testing Basics
band: B4
track: quality-testing
tier: T1
bloom_target: apply
prerequisites: [programming/programming-paradigms]
related: [quality-testing/test-design-techniques, quality-testing/test-automation, quality-testing/code-review, quality-testing/quality-models]
recommended: []
status: published
schema-version: 1
owner: l1-software-testing-basics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0139, S-0207, S-0208, S-0209]
---

# Software Testing Basics — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — Enumerate the four test levels (unit, integration, system, acceptance) and the core components of a test: oracle, inputs, and expected outcome. (evidence: S-0017)
- understand — Explain why testing can demonstrate the presence of defects but not their absence, why an oracle is required for a test to exist, and what each coverage criterion (statement, decision) measures. (evidence: S-0017)
- apply — Choose test levels, doubles, and investment shape for a given component and suite; construct a unit test with a stub and a decidable oracle. (evidence: S-0017, S-0207) — **bloom_target**
- analyze — Given a suite report (coverage, mutations, flaky e2e), diagnose what the suite does and does not establish, and identify the violated testing principle. (evidence: S-0208, S-0207)
- evaluate — Classify quality claims (e.g., "TDD improves quality", "100% coverage = safe") by evidence type and state what would be needed to upgrade them. (evidence: S-0209, S-0208)

## Worked example — from requirement to unit test with a stub

Scenario: a shipping module with function `shipment_cost(order)` that adds a 5% handling fee if the order is international. The `order.is_international()` method calls a not-yet-built geo-service.

1. **Identify the unit and its boundary.** The unit is `shipment_cost`; the missing geo-service is the boundary. We do not need the service to test the fee logic — we substitute it.
2. **Write the failing test first (red).** `order` is a real object with a stubbed `is_international()` (a test double returning true in one test, false in another). Expected values are computed by hand: base 100.00 → international → 105.00; base 100.00 → domestic → 100.00. These hand-computed values are the **oracle**: the test fails or passes against a decidable expectation, not by eyeballing output.
3. **Make it pass with the simplest change (green), then refactor.** Duplicate fee logic is extracted into one constant.
4. **Check what was actually verified.** The two stubbed cases give decision coverage of the fee branch, but they assert nothing about the geo-service, address lookups, or the real-world fee policy — the suite verifies conformance to the fee formula as specified, not that the formula is the right business rule (verification ≠ validation).

The trace shows the four reusable moves: isolate the unit (double), fix the oracle (hand-computed expectation), cover both decision outcomes, and then audit what remains unverified.

## Worked example (mini) — the 100% coverage trap

A suite for a `Customer` class reports 100% statement coverage. Inspection shows tests of the form `customer.set_name("x"); assertEquals("x", customer.getName())` plus constructor calls — every line executes, no logic is asserted, and a mutation that deletes the validation branch in `set_name` kills nothing. Coverage measured *which code ran*; it never measured *what behavior was pinned*. This is the Inozemtseva & Holmes finding in miniature: coverage is necessary but not sufficient, and stronger criteria (decision, condition) only help if assertions have teeth.

## Elaboration prompts

- Why does a test without an oracle produce no information at all, rather than weak information? (evidence: S-0017)
- The pyramid says *fewer* UI tests — under what concrete conditions would a team rationally violate the shape (e.g., a three-screen app with no unit-testable logic)? (evidence: S-0207)
- If coverage is weakly correlated with effectiveness, what should a team measure or inspect instead, and why is coverage still worth reporting? (evidence: S-0208)
- TDD's red–green–refactor loop is a *design* discipline — where exactly does the design input enter the loop, and what breaks if refactor is skipped? (evidence: S-0209)
- In the worked example, the stub made the test deterministic — which paradigm property from the prerequisite pack is doing that work, and when does that property fail (e.g., time-dependent oracles)? (evidence: S-0017, S-0098)
- A characterization test pins buggy behavior as the new contract — trace how the team still corrects the bug without losing the safety the test provides. (evidence: S-0139)

## Common misconceptions

1. **"100% coverage means no bugs."** Coverage says which code ran, not what was asserted; a suite can execute every statement while asserting almost nothing. The T1 evidence shows low-to-moderate correlation with effectiveness once suite size is controlled. (evidence: S-0208)
2. **"More end-to-end tests = more confidence."** An e2e-heavy suite is slow, brittle, and diagnoses poorly; the pyramid is an investment heuristic, not a ratio dogma. (evidence: S-0207)
3. **"TDD is just writing the tests first."** Skipping refactor collapses the discipline into ordering trivia; the loop — failing test, minimal pass, refactor — is the claimed mechanism, and TDD does not replace test design or test levels. (evidence: S-0209)
4. **"A green suite proves the software is correct."** Testing shows the presence of defects, not their absence; passing oracles certify conformance to the oracle (verification), not to the unstated real requirement (validation). (evidence: S-0017)
5. **"TDD measurably improves quality — a book proved it."** The quality claims are practitioner experience (T3); no verified controlled study was found establishing the causal claim, so it must be presented as practice, not established fact. (evidence: S-0209)
6. **"Running the program and looking at the output is a test."** Without an oracle, execution is observation, not verification; the pass/fail decision must be decidable and preferably automated. (evidence: S-0017)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why a doctor-style "I ran it, it worked" claim is weaker than a test with a written expected result — grade against the oracle claims. (evidence: S-0017)
2. Why covering 100% of the roads in a city says nothing about whether the addresses are correct — grade against the coverage-claims. (evidence: S-0208)
3. Why a shop that checks every parcel against the order form still ships wrong items when the order form itself is wrong — grade against the verification/validation claims. (evidence: S-0017)

## Interleaving hooks

- **programming/programming-paradigms (prerequisite):** purity gives deterministic, mock-free tests (R1 in validation.md); the paradigm-effect evidence disciplines quality claims about language choice (R2 in validation.md).
- **quality-testing/test-design-techniques (related):** this pack supplies the oracle and coverage vocabulary; the next pack adds how to choose inputs (equivalence partitioning, boundary analysis) — revisit the S1 stub test and ask which input classes it covers.
- **quality-testing/test-automation (related):** the pyramid's unit/service/UI layers become concrete harness decisions (frameworks, CI, flake management) — the investment heuristic here is the cost model there.
- **quality-testing/code-review (related):** automated tests and human review detect different defect classes — ask which finding types each catches, and why a characterization test complements, not replaces, review.
- **quality-testing/quality-models (related):** verification/validation maps onto ISO 25010 characteristics — a green suite argues functional correctness only, not performance, usability, or security.
