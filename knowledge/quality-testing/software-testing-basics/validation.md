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
status: draft
schema-version: 1
owner: l1-software-testing-basics
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0139, S-0207, S-0208, S-0209]
---

# Software Testing Basics — validation

Item anatomy: `- Q:` `- bloom:` `- bank:` `- A:` `- evidence:` `- topic:`.

## Formative (practice)

### F1. Test levels recall
- Q: Name the four test levels of SWEBOK, and state what each one targets as the system under test.
- bloom: remember
- bank: formative
- A: (1) Unit — the smallest testable units (functions, classes, modules) in isolation. (2) Integration — interactions between units, using stubs/drivers for components not yet built. (3) System — the complete system against its requirements. (4) Acceptance — formal check that the system satisfies user needs.
- evidence: [S-0017]
- topic: quality-testing/software-testing-basics

### F2. The oracle problem
- Q: A developer runs the program with some inputs and "eyeballs" the output. Why does this not produce a test result, and what is the missing component?
- bloom: understand
- bank: formative
- A: A test needs an oracle — a decidable criterion for judging whether observed behavior is acceptable. Eyeballing is observation, not verification: no pass/fail decision is made against a specification, reference system, or expected results, so executing the program yields no test outcome.
- evidence: [S-0017]
- topic: quality-testing/software-testing-basics

### F3. Statement vs decision coverage
- Q: Distinguish statement coverage from decision coverage: what does each measure, and which one would a "100% statement coverage" target leave unexamined?
- bloom: understand
- bank: formative
- A: Statement coverage measures which statements were executed; decision (branch) coverage measures which Boolean outcomes (true/false of each decision) were taken. 100% statement coverage can be achieved while a branch of an if-statement never executes, so decision coverage is the stricter adequacy criterion of the two.
- evidence: [S-0017]
- topic: quality-testing/software-testing-basics

### F4. Pyramid investment decision
- Q: A team's automated suite is 70% end-to-end UI tests; full runs take hours, flake weekly, and only diagnose failures slowly. Apply the test automation pyramid to prescribe a target shape and state the reasoning.
- bloom: apply
- bank: formative
- A: Rebalance toward the pyramid: a large base of fast, cheap unit tests; fewer service/integration tests; the fewest UI tests at the top. UI tests are brittle, expensive to write, and time-consuming, so the top should shrink; unit tests fail fastest and localize failures best. The pyramid is an investment heuristic — not a fixed ratio — so the target is an inverted-versus-current shape with the business-critical end-to-end flows kept at the top.
- evidence: [S-0207]
- topic: quality-testing/software-testing-basics

## Summative (mastery checkpoint)

### S1. Unit test with a stub
- Q: Function `apply_discount(order)` must charge 10% off when `order.loyalty_ok()` returns true. `loyalty_ok()` talks to a not-yet-built loyalty service. Write the minimal unit test structure for `apply_discount` (what you substitute, what you assert, what the oracle is), and name the kind of component you substitute.
- bloom: apply
- bank: summative
- A: Substitute the dependency with a test double — a stub returning true (and a second case returning false). Assert the expected price for each case against hand-computed expected results, which serve as the oracle. The stub isolates the unit from the missing service, exercising `apply_discount` in isolation; the two stubbed cases give decision coverage of the discount branch.
- evidence: [S-0017]
- topic: quality-testing/software-testing-basics

### S2. Coverage is not effectiveness
- Q: A suite reports 100% statement coverage; mutation testing scores it at 12% (mutants killed). Explain the mechanism behind the gap, and describe what the suite likely contains.
- bloom: analyze
- bank: summative
- A: Coverage records which code ran, not what behavior was asserted. A suite can execute every statement while its assertions check almost nothing — e.g., getter tests, type-checks, or weak assertions — so mutations alter behavior without any test noticing. The T1 evidence (Inozemtseva & Holmes) shows coverage correlates only low-to-moderately with fault-detection once suite size is controlled; stronger criteria add little. The fix is assertion strength and mutation/inspection feedback, not a higher coverage target.
- evidence: [S-0208]
- topic: quality-testing/software-testing-basics

### S3. Evaluating a quality claim about TDD
- Q: A vendor claims "TDD measurably improves software quality" and cites a practitioner book. Classify this claim by evidence type, state what would be needed to upgrade it, and say what TDD is actually established to be.
- bloom: evaluate
- bank: summative
- A: The claim as sourced is a practice claim (T3): the red–green–refactor discipline is well documented, but the book's quality claims rest on practitioner experience, and no verified controlled study was found establishing "TDD improves quality" — so that causal form is not empirically established. Upgrading would require RCT/quasi-experimental or large-N observational evidence with confounders controlled. What TDD is established to be is a development and design discipline — write a small failing test, make it pass minimally, refactor — not a proven quality lever.
- evidence: [S-0209]
- topic: quality-testing/software-testing-basics

### S4. Verification vs validation
- Q: A payments module passes every test in its suite, and each test's oracle is derived from the written specification. A requirement review later discovers the specification mis-states the fee formula. Classify what the suite achieved and what it failed to achieve.
- bloom: analyze
- bank: summative
- A: The suite achieved verification — conformance to the specification as written, with every oracle satisfied. It failed validation — fitness for the real user need — because the oracles encoded the wrong requirement. This is the presence-of-defects limit: passing oracles certifies conformance to the oracle, not correctness against the unstated requirement.
- evidence: [S-0017]
- topic: quality-testing/software-testing-basics

## Review (spaced repetition — interleaved with prerequisites)

### R1. Purity meets testability (from programming-paradigms)
- Q: A codebase uses heavily impure functions (randomness, globals, wall-clock time). Why does this make unit testing harder, and which paradigm property would make the tests deterministic without mocks?
- bloom: apply
- bank: review
- A: Impure functions depend on hidden state, so outcomes vary between runs and tests must mock or reset the world to be repeatable. Pure functions — output depends only on input, no observable side effects — give referential transparency: deterministic, order-independent, trivially testable without setup, teardown, or doubles. This is why functional idioms are favored for data pipelines and concurrency, and it shows the testability consequences of the paradigm split.
- evidence: [S-0098]
- topic: programming/programming-paradigms

### R2. Evidence about quality levers (from programming-paradigms)
- Q: Your team plans to rewrite a service in a "better" paradigm, citing quality gains, and separately mandates 95% statement coverage. Evaluate both moves against the T1 evidence you know.
- bloom: evaluate
- bank: review
- A: Both levers are weaker than claimed. The large-N evidence (Ray et al.) shows language/paradigm choice has a significant but modest association with defect rates once size, age, team, and domain are controlled — no "objectively better paradigm." And the coverage evidence (Inozemtseva & Holmes) shows coverage correlates only low-to-moderately with effectiveness once suite size is controlled. Both moves should be justified by concrete project-specific mechanisms (team fit, assertion strength), not by a universal ranking.
- evidence: [S-0099][S-0208]
- topic: programming/programming-paradigms

### R3. Presence of defects (this topic)
- Q: A legacy module has no tests. A developer adds a characterization test that locks in current behavior — even behavior the team suspects is wrong. Does the module now have "correctness"? Why is the characterization test still the right entry point?
- bloom: analyze
- bank: review
- A: No — the test demonstrates the presence (or absence) of the behaviors it asserts, not their correctness; a green characterization suite certifies conformance to today's behavior, which may be a bug. It is still the right entry point because code without tests cannot be changed safely: the characterization test pins the current contract, exposes the seams, and makes subsequent correction a deliberate, reviewable change instead of a silent regression.
- evidence: [S-0139]
- topic: quality-testing/software-testing-basics
