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
status: published
schema-version: 1
owner: l1-code-review
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0222, S-0223, S-0224]
---

# Code Review

## Claims

- SWEBOK v4 covers review-based verification — code reviews, design reviews, and inspection techniques — in its Software Quality knowledge area, while its Testing KA covers dynamic verification of the executing system; the two are complementary verification routes [T2][S-0017].
- A review is static: people examine a work product without executing it, so review complements but cannot replace testing — defects that only manifest at runtime (timing, concurrency, resource use) are outside review's scope [T2][S-0017].
- Fagan's 1976 inspection method structured review into a formal process — planning, overview, preparation, inspection meeting, rework, follow-up — with defined roles (moderator, author, reader, recorder, inspectors) and checklists of common defects used to focus preparation [T1][S-0223].
- In the IBM environment Fagan reported, inspections improved programming quality and productivity — gains of 20% or more — and participating in inspections was itself reported as a learning mechanism for designers and programmers [T1][S-0223].
- Fagan reported defect-cost escalation: errors detected during system testing cost about 10 times more to fix than errors caught during construction, and 10–25 times more when found after release — the classic economic argument for early verification [T1][S-0223].
- Contemporary ("modern") review converged across large projects at Google, Microsoft, and AMD on a lightweight, tool-mediated practice: review starts before the change is committed, first responses arrive within hours, and median completion intervals are on the order of hours to a day (14.7–19.8 h in the Microsoft projects studied) [T1][S-0224].
- The rigidity of formal, meeting-based inspection limited its adoption and efficiency: Lucent inspection intervals had a median of about 10 days, versus hours-to-a-day in contemporary practice [T1][S-0224].
- Defect-finding remains the main stated motivation for review, but the measured outcomes are broader — knowledge transfer, team awareness, and alternative or better solutions — so review is not only defect-finding [T1][S-0222].
- Peer review measurably spreads codebase knowledge: measured participation in review increased the number of distinct files a developer knows by 66–150% depending on the project [T1][S-0224].
- Open-source projects (Apache, Linux, KDE) have traditionally reviewed after commit (commit-then-review), while the corporate projects studied (AMD, Microsoft, Google-led) converged on pre-commit review [T1][S-0224].
- Review consumes real developer time: the survey found review effort is a documented challenge, and the speed of lightweight tool-mediated review exists partly in response to that cost [T1][S-0222].

## Details

- The Fagan process separated preparation (individual study against checklists and standards) from the meeting (defect discovery), so that meeting time is spent finding defects, not reading the artifact — the origin of "review preparation" in modern tooling [T1][S-0223].
- Review velocity is the unit cost of the practice: at ~1-day median intervals reviews keep pace with development, whereas inspection-scale intervals (days to weeks) throttled how much could be reviewed [T1][S-0224].
- Review serves learning independent of defect removal: even a defect-free change transfers knowledge of the codebase, APIs, and conventions from reviewer to author and back [T1][S-0222][S-0224].

## Boundaries / common misunderstandings

- "Code review is only defect-finding": knowledge transfer is a documented benefit — developers report it as a valued outcome, and it is measurable (66–150% more files known after review participation) [T1][S-0222][S-0224].
- "Reviews replace tests (or tests replace reviews)": review examines code without executing it; a reviewed-but-untested change can still fail at runtime, and a green test suite cannot transfer a reviewer's knowledge to the author — the mechanisms verify different things [T2][S-0017].
- "Bigger reviews catch more": contemporary practice converged on small, quick reviews; the multi-day/week intervals of formal inspection are what limited its adoption, not a lack of rigor [T1][S-0224].
- "Modern review is Fagan inspection in a tool": contemporary review dropped the meeting structure and roles; it is the descendant of inspection that traded formality for speed and scale [T1][S-0224].
- "Review is free": review time is a real cost developers report; the value proposition is catching defects and transferring knowledge before the 10x–25x cost escalation of later detection [T1][S-0223][S-0222].

## References (evidence records)

- [S-0017] IEEE Computer Society 2024 — SWEBOK v4.0 (Software Quality KA: reviews and inspections; Testing KA: dynamic verification).
- [S-0222] Bacchelli & Bird 2013 — Expectations, Outcomes, and Challenges of Modern Code Review (ICSE'13).
- [S-0223] Fagan 1976 — Design and Code Inspections to Reduce Errors in Program Development (IBM Systems Journal).
- [S-0224] Rigby & Bird 2013 — Convergent Contemporary Software Peer Review Practices (ESEC/FSE'13).
