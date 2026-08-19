---
id: quality-testing/code-review
title: Code Review
band: B4
track: quality-testing
tier: T1
bloom_target: apply
prerequisites: [quality-testing/software-testing-basics]
related: []
recommended: []
status: draft
schema-version: 1
owner: l1-code-review
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0222, S-0223, S-0224]
---

# Code Review — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — Recite the Fagan inspection stages and roles, and the pre-commit vs commit-then-review process models. (evidence: S-0223, S-0224)
- understand — Explain why review is static verification (no execution), why it complements rather than replaces testing, and why defect-finding is only one of its documented outcomes. (evidence: S-0017, S-0222)
- apply — Run a review session on a small change: prepare against a checklist, produce findings, classify each finding as review-findable or test-findable, and structure the diff for velocity. (evidence: S-0223, S-0224) — **bloom_target**
- analyze — Diagnose a review pipeline (intervals, diff sizes, defect data) against the empirical convergence findings and identify which practice norm is violated. (evidence: S-0224)
- evaluate — Judge claims like "reviews are obsolete / reviews are free / bigger reviews are better" against the evidence for purposes, costs, and velocity. (evidence: S-0222, S-0223, S-0224)

## Worked example — a simulated review session

Scenario: review of a 14-line change: `def fee(order): rate = 0.05; if order.international: rate = 0.10; return order.base * rate`, comment "fee formula per ticket 4421", no test added.

1. **Prepare (individually, against a checklist).** Per the Fagan pattern: planning and preparation precede the meeting. The reviewer studies the diff, reads ticket 4421, and checks the change against checklist items: behavior vs stated intent; branch coverage of the decision; robustness of inputs; test presence. Preparation is where most findings are born — the meeting (or tool thread) verifies, not discovers.
2. **Find and classify defects.** Reading the code, not running it: (a) formula-vs-ticket mismatch — review-findable, only if the reviewer checks the source of truth; (b) no test for the 0.05/0.10 branches — this is the defect class review *requests*: tests are dynamic and lock in behavior; (c) `order.base` assumed present — review-findable robustness issue. Each comment is classified by which mechanism would catch it (review vs test), matching the claim that review and testing verify different things.
3. **Run the exchange.** Reviewer posts findings; author replies; the thread resolves the ticket question (this is where knowledge transfer happens — the author learns the fee policy context, the reviewer learns the module's conventions). The session is a learning outcome even if the code were defect-free.
4. **Check velocity.** 14 lines, one pass, hours not days: the session matches the convergent practice — small unit, quick turnaround, pre-commit — rather than the ~10-day inspection interval that throttled formal review.

The reusable moves: prepare against a checklist; classify each finding by detection mechanism; treat the exchange as learning, not just defect extraction; keep the unit small.

## Worked example (mini) — velocity arithmetic

A team reviews 2,000-LOC diffs and completes ~4 reviews/week; median interval is 11 days, approximating formal-inspection lag. Evidence-based target: diffs of a few hundred LOC, first response within hours, completion on the order of a day (14.7–19.8 h medians in the studied Microsoft projects). The diagnosis is structural (unit size + response norms), not effort — review velocity is the unit cost of the practice.

## Elaboration prompts

- Why does preparation (individual study before the meeting/thread) matter more in Fagan's process than in casual review, and what modern tool feature corresponds to it? (evidence: S-0223)
- The measured outcome "knowledge transfer" is not visible in the defect list — how would you instrument a team to see it, as Rigby & Bird did? (evidence: S-0224)
- A reviewer's comment "this should be a test, not a comment" — which mechanism boundary is the reviewer enforcing, and when is the reviewer wrong? (evidence: S-0017)
- Pre-commit review blocks merges; commit-then-review doesn't — under what conditions would a team rationally choose each, given the convergence evidence? (evidence: S-0224)
- The Fagan data shows 10x–25x cost escalation for late defects. Trace how a *velocity-driven* review process still captures that benefit (i.e., which defects are caught before system testing). (evidence: S-0223)
- In the worked example, the reviewer read a ticket to judge intent. Which prerequisite concept (verification vs validation, oracle) does that action map onto? (evidence: S-0017)

## Common misconceptions

1. **"Code review is just about finding bugs."** Defect-finding is the main *motivation*, but knowledge transfer, team awareness, and alternative solutions are measured outcomes; review is a learning channel (66–150% more files known). (evidence: S-0222, S-0224)
2. **"Reviews can replace tests."** Review never executes the code; runtime-only defects (races, timing, resource exhaustion) are invisible to it. Tests and review are complementary mechanisms (SWEBOK static vs dynamic). (evidence: S-0017)
3. **"A bigger diff gets a bigger review."** Practice converged on small, quick reviews; the rigidity and multi-day intervals of formal inspection are what limited adoption. (evidence: S-0224)
4. **"Modern code review is just Fagan inspection in software."** Modern review dropped the meeting ceremony, roles, and checklists as defaults; it trades formality for speed and scale, though it descends from inspection. (evidence: S-0224, S-0223)
5. **"Review is free — it costs nothing."** Review consumes real developer time (a documented challenge); its economic case is catching defects early (10x–25x cost escalation later) plus knowledge transfer, not zero cost. (evidence: S-0222, S-0223)
6. **"If tests pass, the review's job is done."** A green suite certifies conformance to oracles; review is the mechanism that checks intent against spec (verification vs validation) — a passing suite does not validate the requirement. (evidence: S-0017)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why a friend reading your essay can catch arguments you cannot — and why running the essay through a spell-checker can't replace that reader. (grade against the purposes/knowledge-transfer claims: S-0222, S-0224)
2. Why two engineers reading code for 30 minutes cost something, and when that cost is worth paying (grade against the cost-escalation and velocity claims: S-0223, S-0224).
3. Why "it compiled and the tests passed" is not the same as "a human who knows the domain said this is right" (grade against static-vs-dynamic and verification-vs-validation claims: S-0017).

## Interleaving hooks

- **quality-testing/software-testing-basics (prerequisite):** review is the static complement to the oracle-based dynamic tests of the prerequisite pack — R1/R2 in validation.md interleave coverage and characterization-test evidence; ask which defect classes each mechanism owns.
- **quality-testing/test-design-techniques (related):** the branch analysis a reviewer demands (decision coverage of `international`) is the input-selection vocabulary from that pack — a review comment "cover both branches" translates directly into equivalence classes.
- **quality-testing/test-automation (related):** review gates are enforced by the same CI/automation machinery that runs tests — the velocity norm (pre-commit, hours-to-a-day) is a pipeline design decision there.
- **quality-testing/quality-models (related):** review's contribution to maintainability (analysability, modifiability) and quality-in-use is distinct from its defect-removal role — a review improves the code's maintainability even when it changes no behavior.
