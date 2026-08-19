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

# Software Testing Basics

## Claims

- Software testing is the dynamic verification of a program's behavior on a finite set of carefully selected test cases from a potentially infinite execution domain; it can demonstrate the presence of defects but cannot prove their absence [T2][S-0017].
- SWEBOK organizes testing into test levels — unit (component), integration, system, and acceptance testing — each targeting a different scope of the system under test [T2][S-0017].
- Unit testing exercises the smallest testable units (functions, classes, modules) in isolation from the rest of the system [T2][S-0017].
- Integration testing verifies interactions between units; stubs and drivers substitute for components not yet built or not available, isolating each side of the interaction [T2][S-0017].
- System testing evaluates the complete system against its requirements, and acceptance testing formally checks that the system satisfies user needs [T2][S-0017].
- The test automation pyramid (Cohn) prescribes many fast unit tests at the base, fewer service/integration tests in the middle, and the fewest user-interface (end-to-end) tests at the top, because UI tests are brittle, expensive to write, and time-consuming [T3][S-0207].
- Every test needs an oracle — a means of deciding whether observed behavior is acceptable; the oracle problem is addressed by checking against a specification, a reference system, or expected results [T2][S-0017].
- Coverage-based test criteria (statement, decision/branch, condition) measure which parts of the code a suite exercised and give test-adequacy targets such as "100% statement coverage" [T2][S-0017].
- Coverage correlates only low-to-moderately with a suite's fault-detection effectiveness once suite size is controlled, and stronger criteria add little predictive insight — coverage is necessary but not sufficient for suite quality [T1][S-0208].
- Test-driven development (Beck) follows red–green–refactor: write a small failing test, make it pass with the simplest change, then remove duplication; it is a development and design discipline, not merely a testing technique [T3][S-0209].
- TDD's quality benefits rest on practitioner experience: this pack found no verified controlled study establishing "TDD improves quality", so claims of that form are practice claims, not empirically established [T3][S-0209].
- Feathers defines legacy code as code without tests; adding tests (e.g., characterization tests written through seams) is the entry point for changing such code safely [T3][S-0139].
- Testing serves both verification (conformance to a specification) and validation (fitness for user needs); a suite that passes its oracles still does not prove the software meets the real requirement [T2][S-0017].
- Test doubles — stubs and drivers — replace real dependencies so the unit under test can be exercised before those dependencies exist or are stable [T2][S-0017].

## Details

- Test level scope progression: unit tests fail fastest and localize failures best; system tests approximate real usage but make failure diagnosis harder; the pyramid is the standard investment heuristic between these extremes [T3][S-0207].
- An oracle is the difference between a test and an observation: without a way to judge acceptability, executing the program produces no test result — the effort is useless (SWEBOK) [T2][S-0017].

## Boundaries / common misunderstandings

- 100% coverage is not bug-free: coverage measures which code ran, not what behavior was asserted — a suite can cover every statement while asserting almost nothing (e.g., logic-free getter tests) [T1][S-0208].
- More end-to-end tests do not mean more confidence: an e2e-heavy suite is slow, brittle, and diagnoses poorly; the pyramid is a heuristic for test investment, not a fixed-ratio dogma [T3][S-0207].
- TDD is not "tests first, same code": skipping the refactor step collapses the discipline into ordering trivia; the loop — failing test, minimal pass, refactor — is the claimed mechanism, and TDD does not replace test design or test levels [T3][S-0209].
- A green suite does not prove correctness: testing shows the presence of defects, not their absence, and passing oracles only certifies conformance to the oracle, not to the unstated requirement [T2][S-0017].
- A test without an oracle is not a test: executing code and eyeballing output is observation, not verification; the pass/fail decision must be decidable and preferably automated [T2][S-0017].

## References (evidence records)

- [S-0017] IEEE Computer Society 2024 — SWEBOK v4.0, Software Testing KA (test levels, oracle problem, limitations of testing).
- [S-0139] Feathers 2004 — Working Effectively with Legacy Code (Prentice Hall).
- [S-0207] Cohn 2009 — Succeeding with Agile (test automation pyramid).
- [S-0208] Inozemtseva & Holmes 2014 — Coverage Is Not Strongly Correlated with Test Suite Effectiveness (ICSE'14).
- [S-0209] Beck 2002 — Test-Driven Development: By Example (Addison-Wesley).
