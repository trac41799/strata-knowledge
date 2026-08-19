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

# Test Automation — teaching

## Learning objectives (Bloom)

By the end of this topic, the learner can:

- remember: define a flaky test and name the documented root-cause classes with their prevalence.
- understand: explain the pyramid rationale and why the three layers differ in speed, cost, and brittleness.
- apply (target): place tests in the pyramid, fix a flaky test, and decide whether to update a snapshot.
- analyze: interpret flakiness statistics (prevalence, share of failures, compute cost) as signals for CI policy.
- evaluate: design a flaky-test triage and management policy for a CI system.

## Worked example — diagnose a flaky test

Symptom: `checkout_test` fails on CI roughly one run in five, always in the "order confirmation visible" assertion; it passes locally and on retry.

1. **Rule out code change:** the test passes and fails on identical code — that is the definition of a flaky test (S-0217).
2. **Hypothesize against the root-cause classes:** async waits (~45%) — the test sleeps a fixed 800ms for the confirmation; concurrency (~20%) — the suite runs shards in parallel, and the test writes a shared `orders` fixture; order dependency (~12%) — the suite order is randomized.
3. **Instrument:** run the test alone 20 times (passes — rules out pure code), then with neighbors in parallel (fails — points to shared state), then with the fixed sleep reduced to 50ms and an explicit wait-for-condition (fails more often — confirms timing is marginal).
4. **Fix:** replace the fixed sleep with an explicit wait for the confirmation element (dominant root-cause class); move the shared fixture to per-test isolation. Both fixes target documented root causes (S-0217).
5. **Verify:** 100 consecutive CI runs green; monitor the test's pass history for recurrence instead of relying on reruns (S-0219).

## Worked example — snapshot or not?

Your team snapshots a rendered settings page. After a refactor the snapshot fails. Worked decision: open the committed `.snap` diff in review; the change is a whitespace/naming change → intentional → update via `-u` with the reviewed diff; if the diff shows a real behavior change the team didn't intend → the test caught a regression, fix the code. Bulk `-u` without review is the documented failure mode (S-0220).

## Elaboration prompts

- Why is a fixed sleep the single most common flaky-test cause, and what makes wait-for-condition strictly better?
- Your CI reruns failed tests once. Where exactly does that policy help, and where does it hurt (S-0218/S-0219)?
- The pyramid is a heuristic — what cost signals should override it for your product?
- Why does test data belong to the test design artifact rather than to a shared environment (S-0017)?
- When is a snapshot the right tool, and when is it a liability?

## Common misconceptions

- "Rerunning a flaky test fixes it." Rerun is triage; 84% of stable→failing transitions at Google involved flaky tests, and masking them delays real fixes (S-0218).
- "Flakiness is rare." At Google scale, ~16% of tests were flaky at some point, and 4.56% of 1.6M failures in 15 months were flaky (S-0218, S-0219).
- "Snapshot tests assert behavior." They assert equality against an artifact; a snapshot with a weak name and a bulk update is a silent change approval machine (S-0220).
- "Automating everything means more confidence." UI-everywhere suites are the slowest and most brittle — the pyramid's top exists to be thin (S-0207).
- "Test order/shared state is a testing detail." Order dependency and shared mutable state are documented flaky root causes; isolation is a fix, not a preference (S-0217).

## Feynman targets

Explain to a non-tester: (1) what makes a test flaky and why "it passed on rerun" is bad news, not good; (2) why you want many small fast tests and few slow end-to-end ones; (3) what a snapshot test actually checks; (4) why test data must be controlled.

## Interleaving hooks

- From test-design-techniques: automate the EP/BVA and pairwise cases from that pack — which techniques map to which pyramid layer?
- From software-testing-basics: every automated test still needs an oracle — find the oracles in the worked example.
- Forward to devops-pipeline: where the suite runs in CI, how flakiness gates merges, and what result distillation does at scale.
- From code-review: snapshots and flaky-fix PRs are review surfaces; coverage and mutation numbers are inputs to review, not substitutes for it.
