---
id: quality-testing/test-automation
title: Test Automation
band: B4
track: quality-testing
tier: T1
bloom_target: apply
prerequisites: [quality-testing/test-design-techniques]
related: [operations/devops-pipeline, quality-testing/performance-engineering, quality-testing/code-review]
recommended: [operations/devops-pipeline]
status: draft
schema-version: 1
owner: l1-test-automation
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0207, S-0217, S-0218, S-0219, S-0220]
---

# Test Automation — validation

## Formative (practice)

- Q: What is the definition of a flaky test?
- bloom: remember
- bank: formative
- A: A test that passes and fails on the same code — its outcome depends on conditions other than the code under test (timing, concurrency, ordering, environment).
- evidence: [S-0217]
- topic: quality-testing/test-automation

- Q: Why does the test automation pyramid put UI tests at the top (fewest) and unit tests at the base (most)?
- bloom: understand
- bank: formative
- A: Unit tests are fast, cheap, and stable, giving the fastest feedback per unit of effort; UI tests are brittle, expensive to write, and slow, so they are reserved for the few flows that genuinely need end-to-end coverage.
- evidence: [S-0207]
- topic: quality-testing/test-automation

- Q: A login test fails intermittently on CI only. It waits a fixed 500ms for a redirect, shares a database record with another test, and runs in random order. Map each suspected cause to a documented flaky root-cause class and propose the fix.
- bloom: apply
- bank: formative
- A: Fixed 500ms wait → asynchronous-wait root cause (largest class, ~45%); fix with an explicit wait-for-condition (poll until element/promise resolves). Shared record → test-order/state dependency (~12%); fix by isolating per-test data. Random order exposes ordering sensitivity → fix by isolation, not by pinning order.
- evidence: [S-0217]
- topic: quality-testing/test-automation

- Q: Place each test on the pyramid: (a) API contract test for the payment endpoint, (b) Selenium click-through of checkout, (c) pure function test for fee calculation. Justify each placement.
- bloom: apply
- bank: formative
- A: (c) at the base — pure, fast, stable; (a) in the middle — service layer that pins the contract; (b) at the top — one or few end-to-end flows, accepted as brittle and slow.
- evidence: [S-0207]
- topic: quality-testing/test-automation

## Summative (mastery checkpoint)

- Q: Google reports ~1.5% of ~4.2M tests flaky in a given week. Compute the expected number of flaky tests per week and interpret what the 84% statistic adds about their impact.
- bloom: apply
- bank: summative
- A: 0.015 × 4.2M ≈ 63,000 tests flaky in a week. The 84% figure means flaky tests were involved in most transitions from stable-passing to failing — i.e., flakiness is the dominant source of false red signals in CI, which is why rerun infrastructure exists.
- evidence: [S-0218]
- topic: quality-testing/test-automation

- Q: After a refactor, a snapshot test fails. Walk through your decision process between reviewing the diff, updating with the flag, and deleting the test.
- bloom: analyze
- bank: summative
- A: Treat the snapshot like code: inspect the diff and decide whether the output change is intended (refactor preserved behavior → update) or a regression (fix the code, do not update). Bulk `-u` is only acceptable after per-diff review; if the snapshot asserts nothing useful, delete it. Updating without review masks regressions.
- evidence: [S-0220]
- topic: quality-testing/test-automation

- Q: Draft a flaky-test management policy for a CI system: how do you detect, triage, and resolve flakiness, and when is rerunning legitimate? Defend your choices with the evidence.
- bloom: evaluate
- bank: summative
- A: Detect via stability tracking (pass/fail history per test); triage by labeling suspected flaky tests and quarantining them; resolve by root-causing (async waits, concurrency, ordering) rather than permanent reruns, since reruns mask root causes (4.56% of failures at Google were flaky) and cost compute (2–16%). A bounded automatic rerun with labeling is defensible as a triage tool; it is not a fix.
- evidence: [S-0219][S-0218]
- topic: quality-testing/test-automation

## Review (spaced repetition — interleaved with prerequisites)

- Q: Why does pairwise testing need so few test cases, and what residual risk does it accept?
- bloom: understand
- bank: review
- A: 65–97% of failures are triggered by one- or two-variable interactions, so covering all pairs captures the dominant failure space; the residual risk is defects requiring three or more interacting variables.
- evidence: [S-0212]
- topic: quality-testing/test-design-techniques

- Q: What is an oracle and why is it required for an automated test to be a test?
- bloom: remember
- bank: review
- A: The oracle decides whether observed behavior is acceptable; without an encoded pass/fail verdict, automated execution produces observations, not test results.
- evidence: [S-0017]
- topic: quality-testing/software-testing-basics

- Q: Your team's suite has 100% statement coverage. What must you check before believing the suite is effective?
- bloom: analyze
- bank: review
- A: Coverage correlates only low-to-moderately with fault-detection effectiveness once suite size is controlled; verify the assertions and oracles are substantive and use stronger criteria or mutation as a complement.
- evidence: [S-0208]
- topic: quality-testing/test-design-techniques
