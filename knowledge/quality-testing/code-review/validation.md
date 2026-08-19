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

# Code Review — validation

Item anatomy: `- Q:` `- bloom:` `- bank:` `- A:` `- evidence:` `- topic:`.

## Formative (practice)

### F1. The Fagan process
- Q: Name the six stages of the Fagan inspection process and the defined roles that operate it.
- bloom: remember
- bank: formative
- A: Stages: planning, overview, preparation, inspection meeting, rework, follow-up. Roles: moderator (leads process, verifies follow-up), author, reader (walks through the artifact), recorder (logs defects), and inspectors (all participants hunt defects). Preparation is individual study against checklists and standards; the meeting itself is for finding defects.
- evidence: [S-0223]
- topic: quality-testing/code-review

### F2. Static vs dynamic
- Q: A change passes human review but the test suite has no coverage of it. What class of defects can review still have missed, and why can't review catch them?
- bloom: understand
- bank: formative
- A: Runtime-only defects: timing/race conditions, concurrency, resource exhaustion, performance degradation, and behavior that depends on execution environment. Review is static — people read the code without executing it — so only defects visible by reading are in scope; dynamic verification (tests) is the complementary mechanism.
- evidence: [S-0017]
- topic: quality-testing/code-review

### F3. Pre-commit vs post-commit
- Q: Contrast the pre-commit and commit-then-review process models, and state which one the large corporate projects in the evidence converged on.
- bloom: understand
- bank: formative
- A: Pre-commit review happens before the change is integrated (tool-mediated, gating); commit-then-review reviews after check-in, as in traditional open-source development (Linux, Apache). The corporate projects studied (AMD, Microsoft Bing/Office/SQL, Google-led) converged on pre-commit review that starts before commit, is picked up within hours, and completes with a median interval of roughly a day.
- evidence: [S-0224]
- topic: quality-testing/code-review

### F4. Structuring a review for velocity
- Q: A team's review queue is backed up: diffs average 3,000 LOC and median time-to-review is 6 days. Apply the evidence about review velocity and size to prescribe a concrete change and state the reasoning.
- bloom: apply
- bank: formative
- A: Shrink the review unit: contemporary practice converged on small diffs reviewed within hours-to-a-day (median ~1 day in the studied projects), whereas inspection-scale intervals of ~10 days are exactly what limited adoption. Split 3,000-LOC diffs into small reviewable changes, make first response a norm within hours, and keep pre-commit review for every change. The reasoning: review velocity is the unit cost — small, frequent, quick reviews keep pace with development; large reviews recreate the rigidity that throttled formal inspection.
- evidence: [S-0224]
- topic: quality-testing/code-review

## Summative (mastery checkpoint)

### S1. Simulated review session
- Q: You are the reviewer on this change. `def fee(order): rate = 0.05; if order.international: rate = 0.10; return order.base * rate` — the author claims it charges 5% domestic / 10% international, changed `rate` from 0.03 to 0.05, added no test, and left a comment "fee formula per ticket 4421". Run the review: produce the comments you would post, and classify each finding by what mechanism would have caught it (review vs test).
- bloom: apply
- bank: summative
- A: Findings: (1) correctness-by-assertion: the author's stated behavior (5%/10%) matches the code — but the comment references a ticket; a reviewer should verify the formula against the ticket, because review can catch spec-vs-code mismatch only if the reviewer checks the source of truth; (2) no test: the 5%/10% branch logic is exactly the defect class that review can argue about but only tests lock in — request a unit test with oracles for both branches (decision coverage); (3) naming/robustness: `order.base * rate` assumes `base` exists — reviewer flags null/type handling as a review finding. Classify: comment/spec mismatch = review-findable; branch regression = test-findable (review can request it); robustness = review-findable. This mirrors the evidence: defect-finding is the motivation, but knowledge transfer (ticket context, conventions) happens in the same session.
- evidence: [S-0222][S-0223]
- topic: quality-testing/code-review

### S2. Diagnosing a slow review pipeline
- Q: A team's review data shows: median time-to-first-response 2 days, median completion 11 days, diffs averaging 2,500 LOC, and reviewers report "reviews are a chore". Diagnose the failure pattern against the empirical evidence and name the mechanism the team should adopt.
- bloom: analyze
- bank: summative
- A: The team has recreated formal-inspection pathology: ~11-day completion approximates the ~10-day Lucent inspection intervals that the evidence shows limited adoption, with the rigidity/effort developers report as a challenge. The convergent alternative is lightweight pre-commit review: small diffs, first response within hours, completion on the order of a day. The fix is process structure (review unit size, response-time norms), not more reviewer effort — velocity is the unit cost of review.
- evidence: [S-0224][S-0222]
- topic: quality-testing/code-review

### S3. Evaluating "reviews are a waste because we have tests"
- Q: An engineering manager proposes abolishing code review: "automated tests catch everything, and review is pure overhead." Evaluate the proposal against the evidence, identifying what review contributes that tests cannot and what tests contribute that review cannot.
- bloom: evaluate
- bank: summative
- A: The proposal fails on both halves. Review contributes: knowledge transfer (measured 66–150% increase in files known), team awareness, alternative solutions, spec-vs-intent checking, and early detection of defects whose fix cost escalates 10x at system testing and 10–25x post-release — none of which tests provide. Tests contribute: execution-based verification of runtime behavior, which static review cannot see. The two are complementary (SWEBOK: static review vs dynamic testing); the empirical question is review *quality and velocity*, not review-vs-tests.
- evidence: [S-0224][S-0223][S-0017]
- topic: quality-testing/code-review

### S4. Choosing a process model
- Q: A safety-critical subsystem (regulatory review required, small team, long-lived artifacts) is considering either Fagan-style formal inspection or tool-based pre-commit review. Analyze the trade-offs each evidence record supports and recommend with justification.
- bloom: analyze
- bank: summative
- A: Formal inspection (Fagan): defined roles, checklists, structured meetings — strong for completeness and auditable records, reported 20%+ productivity gains and large defect-cost avoidance in IBM's environment; but its rigidity and multi-day intervals limit adoption and efficiency (Lucent ~10-day medians). Tool-based review: velocity (hours-to-a-day), lightweight, pre-commit — but less ceremony and auditable structure. Recommendation: tool-based pre-commit review for the ordinary changes (velocity), with formal inspection only for the small set of change-controlled artifacts the regulator requires — i.e., match ceremony to criticality; the evidence supports both but at different points of the cost/rigor curve.
- evidence: [S-0223][S-0224]
- topic: quality-testing/code-review

## Review (spaced repetition — interleaved with prerequisites)

### R1. Coverage vs assertion strength (from software-testing-basics)
- Q: A reviewer asks an author to "raise coverage to 100% before merge" on a change that already passes review. Evaluate the request against the coverage evidence.
- bloom: evaluate
- bank: review
- A: The request targets the wrong lever: coverage correlates only low-to-moderately with a suite's fault-detection effectiveness once suite size is controlled, because coverage measures which code ran, not what was asserted. The reviewer's actual concern — that runtime behavior is unpinned — is better served by strong assertions on the new branch logic (mutants killed, not lines covered). Coverage is necessary, not sufficient.
- evidence: [S-0208]
- topic: quality-testing/software-testing-basics

### R2. Characterization tests meet review (from software-testing-basics)
- Q: A legacy module has no tests. The team pins its behavior with characterization tests, then sends a change to review. What does each mechanism contribute, and what remains unverified?
- bloom: analyze
- bank: review
- A: Characterization tests lock in *current* behavior (safe-change entry point, per the legacy-code evidence) but assert nothing about whether that behavior is correct. Review contributes the judgment the tests lack: whether pinned behavior matches intent (spec/ticket/domain knowledge). Remains unverified: runtime behavior beyond what the oracles assert — the tests certify conformance to today's behavior, and review certifies intent, but neither proves correctness of the underlying requirement.
- evidence: [S-0139][S-0222]
- topic: quality-testing/software-testing-basics

### R3. Reviewing as learning (this topic)
- Q: A junior engineer's change is defect-free and gets merged after a 10-minute review. Why is it still valuable to have performed the review, and what evidence supports that?
- bloom: understand
- bank: review
- A: The review transfers knowledge — codebase, conventions, API usage — from reviewer to author and reviewer to reviewer; developers report knowledge transfer as a valued outcome, and the measured effect is large (66–150% more distinct files known after review participation). A defect-free change is not a wasted review: learning is a documented outcome of the practice, not a side effect.
- evidence: [S-0222][S-0224]
- topic: quality-testing/code-review
