---
id: engineering-process/professional-ethics
title: Professional Ethics
band: B5
track: engineering-process
tier: T2
bloom_target: understand
prerequisites: []
related: []
recommended: []
status: published
schema-version: 1
owner: l1-professional-ethics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0078, S-0079, S-0080]
---

# Professional Ethics — teaching

## Learning objectives (Bloom)

After studying this topic you will be able to:

- (remember) name the ACM code's four sections and the IEEE code's three commitments and ten tenets;
- (understand) explain professional responsibility, conflicts of interest, confidentiality vs privacy, intellectual property duties, and safety-critical responsibility in terms of the codes; (bloom target)
- (apply) analyze a workplace scenario against the relevant code principles and propose a responsible course of action;
- (analyze) evaluate a case (e.g., Therac-25) by separating technical, organizational, and ethical contributing factors.

## Worked example — analyzing an ethics case with the codes

Scenario: you are a developer on a medical-scheduling app. The release
deadline is Friday; on Wednesday you find that a teammate edited a
performance test's parameters so the "under 500 ms" claim passes, although
real usage shows 1.5 s. The feature gates patient appointment booking.

Structured case analysis:

1. **Facts.** A test was altered to hide a real performance gap; the gap
   affects patients (delayed booking, possible missed care); the release
   is imminent; a colleague is involved.
2. **Stakeholders.** Patients (harm risk), your team (integrity), the
   company (liability, trust), regulators if the system is a medical
   device.
3. **Applicable principles.** ACM 1.3 (be honest and trustworthy), 1.2
   (avoid harm), 2.4 (accept and provide professional review), 2.5
   (comprehensive evaluation including risk analysis), 2.9 (robust,
   secure systems); IEEE tenet 5 (honest claims and estimates, acknowledge
   and correct errors), tenet 9 (avoid injuring others by false or
   malicious actions).
4. **Options.** (a) Ship as-is — violates honesty and harm obligations;
   (b) quietly fix the test — hides the problem; (c) flag the discrepancy
   to the teammate and raise it with the team lead, document the real
   measurements, propose a delay or an honest interim claim.
5. **Decision.** Option (c): raise the concern directly (ACM 4.1: express
   concern to the person thought to be violating the Code), escalate if
   unresolved, and refuse to sign off on the false claim — protected by
   IEEE tenet 10 (no retaliation against reporters).
6. **Review.** Afterward, reflect: was the reporting channel clear? Did
   the team's process pressure encourage the falsification? That is the
   organizational dimension of ethics.

## Elaboration prompts

- Why do both codes put public safety and avoidance of harm before
  employer interests? What tension does this create inside a company?
- ACM 2.5 asks for "comprehensive and thorough evaluations of computer
  systems and their impacts, including analysis of possible risks." What
  does that obligation look like in your day-to-day work?
- Why does the ACM code have a separate leadership section (Section 3)
  rather than one list of rules for everyone?
- How would you distinguish an honest mistake from a violation in the
  falsified-test scenario — and why does the distinction matter?
- What changed between the Therac-20 (hardware interlocks) and the
  Therac-25 (software-enforced safety)? Why was that change dangerous?

## Common misconceptions

1. **"Ethics is the same as legality."** The codes bind members even where
   no law is broken (e.g., honesty in claims, avoiding harm); conversely,
   legality does not settle whether an action is ethical. Codes are
   commitments, not statutes [S-0078][S-0079].
2. **"My responsibility ends at my ticket."** ACM 2.5 and 3.1 extend
   responsibility to system-level impacts and the public good; the
   Therac-25 shows how individual "I just wrote the code" reasoning
   distributes responsibility away until no one owns safety [S-0078][S-0080].
3. **"Reporting a violation is disloyal."** The codes explicitly
   encourage raising concerns (ACM 4.1) and prohibit retaliation against
   reporters (IEEE tenet 10); silence is the deviation, not the report
   [S-0078][S-0079].
4. **"Confidentiality, privacy, and security are the same duty."** They
   are three distinct obligations (ACM 1.6, 1.7, 2.9) targeting personal
   data, entrusted information, and system robustness respectively
   [S-0078].
5. **"The Therac-25 was a rare hardware fluke."** It was a software- and
   process-driven failure repeated at least six times; its lessons —
   verification, hazard analysis, honest reporting — are generic
   safety-critical practice [S-0080].

## Feynman targets

- Explain in 2 minutes why the Therac-25 still matters for a developer
  building a consumer app today.
- Explain to a non-engineer the difference between confidentiality and
  privacy, with one example each.
- Explain why "it passed the test" is not the same as "it is safe" —
  using the falsified-performance-test scenario.

## Interleaving hooks

- engineering-process/requirements-engineering — safety and other
  non-functional requirements must be elicited and specified; ethics
  turns quality characteristics into duties.
- quality-testing/quality-models — ISO 25010 Safety characteristic; a
  rubric for "does this system avoid harm?"
- quality-testing/software-testing-basics — honest testing is an ethical
  duty (falsified tests are violations, not shortcuts).
- security/secure-sdlc — robustly and usably secure systems (ACM 2.9);
  security as a professional obligation, not an afterthought.
- engineering-process/software-lifecycle — ethical duties bind across all
  lifecycle processes, not only construction.
