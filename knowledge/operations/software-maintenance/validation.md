---
id: operations/software-maintenance
title: Software Maintenance
band: B4
track: operations
tier: T1
bloom_target: apply
prerequisites: [engineering-process/software-lifecycle]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-software-maintenance
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0020, S-0177, S-0178, S-0179]
---

# Software Maintenance — validation

Item anatomy: `- Q` · `- bloom` · `- bank` · `- A` · `- evidence` · `- topic`.

## Formative (practice)

### F1. The four types
- Q: Name and define the four types of software maintenance in SWEBOK v4.
- bloom: remember
- bank: formative
- A: Corrective (fixing defects discovered after delivery), adaptive (adapting to a changed environment), perfective (enhancing attributes/adding value for users), preventive (detecting and correcting latent faults before they manifest).
- evidence: [S-0017]
- topic: operations/software-maintenance

### F2. Corrective vs adaptive
- Q: A bug crashes the app on a newly released OS version. Is that corrective or adaptive maintenance, and why does the boundary matter?
- bloom: understand
- bank: formative
- A: It is adaptive: the fault arises because the environment changed (new OS), not because the software fails its original specification. The boundary matters because the four types carry different planning, review, and release implications — adapting to the environment is an expected, recurring cost.
- evidence: [S-0017]
- topic: operations/software-maintenance

### F3. Debt origin
- Q: Where does the technical debt metaphor come from, and what is the exact trade it describes?
- bloom: remember
- bank: formative
- A: Ward Cunningham, OOPSLA 1992 (The WyCash Portfolio Management System): shipping first-time code is like going into debt — a little debt speeds development so long as it is paid back promptly with a rewrite; unrepaid debt accrues interest (every minute spent on not-quite-right code).
- evidence: [S-0178]
- topic: operations/software-maintenance

### F4. What maintenance really is
- Q: A manager believes 80% of maintenance work is fixing bugs. How do the data contradict this?
- bloom: understand
- bank: formative
- A: The 487-organization Lientz & Swanson survey found about 55% of maintenance requests were new requirements rather than corrections and at least half of maintenance effort was perfective — maintenance is mostly enhancement and adaptation, with bug fixing the minority share.
- evidence: [S-0179]
- topic: operations/software-maintenance

### F5. Scope of Lehman's laws
- Q: Lehman's laws apply to which class of programs, and why not to the others?
- bloom: understand
- bank: formative
- A: They concern E-programs — systems embedded in the real world that must evolve as the world changes. S-programs are fully specified and verifiable (no environmental drift); P-programs are judged against a problem, but E-programs' requirements move with their environment, forcing continuing change.
- evidence: [S-0177]
- topic: operations/software-maintenance

## Summative (mastery checkpoint)

### S1. Classify change requests
- Q: Classify each request into corrective/adaptive/perfective/preventive and justify: (a) crash on login with null password; (b) support for the new company-wide SSO provider; (c) new export-to-PDF feature; (d) rewrite of a module to remove duplicated logic; (e) database migration for a new currency; (f) fix of a rare timeout under load.
- bloom: apply
- bank: summative
- A: (a) corrective — residual fault, software fails its spec; (b) adaptive — environment change (identity provider); (c) perfective — new user-facing enhancement; (d) preventive (or perfective-by-restructuring) — removes latent structural risk before it causes failure; (e) adaptive — regulatory/environmental change; (f) corrective — defect in the implemented behavior. Note (d) is the classic boundary case: restructuring for maintainability is classified preventive/perfective, not corrective, because no reported fault is being fixed.
- evidence: [S-0017]
- topic: operations/software-maintenance

### S2. Spend the maintenance budget
- Q: A product's maintenance workload is 55% enhancements, 30% environment adaptation, 10% corrections, 5% preventive, and maintenance is >50% of lifecycle cost. Where should engineering invest, and what is the risk of underinvesting in preventive work?
- bloom: apply
- bank: summative
- A: The mix says the system's economic value comes from evolution: invest in maintainability (comprehensible code, tests, docs) because most requests change existing code, and in planned preventive/refactoring work because latent faults and structural rot raise the future cost of the dominant enhancement workload. Underinvesting in preventive work converts tomorrow's cheap enhancements into corrective incidents and grows the interest on technical debt.
- evidence: [S-0179][S-0017]
- topic: operations/software-maintenance

### S3. Analyze a debt decision
- Q: A team ships a v2 rewrite in 6 months instead of 3 by cutting tests, then promises "we'll pay the debt back after launch." Analyze this using the debt metaphor: what is the principal, what is the interest, and what conditions make the decision sound or unsound?
- bloom: analyze
- bank: summative
- A: Principal: the missing tests/quality work — a deliberate shortcut. Interest: every future change is slower and riskier (regression escapes, longer verification). The decision is sound only if the debt is repaid promptly (a scheduled rewrite/refactor after launch, as Cunningham's framing requires) and the interest actually accrues within budget; it is unsound when repayment is indefinite ("after launch" never scheduled), because interest compounds and the system becomes unconsolidated — the failure mode Cunningham described as bringing engineering to a standstill.
- evidence: [S-0178]
- topic: operations/software-maintenance

### S4. Evaluate a cost doctrine
- Q: Evaluate: "Preventive maintenance is wasteful — fix problems when they happen." Argue both sides with the evidence, then decide.
- bloom: evaluate
- bank: summative
- A: For: correction is immediate, observable value; preventive work competes with feature work (the dominant maintenance driver per the survey data). Against: preventive maintenance detects latent faults before they manifest, and maintainability/restructuring investment lowers the cost of the dominant perfective workload; SWEBOK treats preventive as a distinct type precisely because reacting is costlier than preempting. Verdict: the doctrine overgeneralizes — skip preventive work only where fault cost is low and the codebase is stable; for long-lived, enhancement-heavy systems it is the lever that keeps the majority workload cheap.
- evidence: [S-0017][S-0179]
- topic: operations/software-maintenance

## Review (spaced repetition — interleaved with prerequisites)

### R1. 12207 structure (from software-lifecycle)
- Q: How many processes does ISO/IEC/IEEE 12207:2017 define, and in which category does the maintenance process sit?
- bloom: remember
- bank: review
- A: 30 processes in 4 categories: Agreement (2), Organizational Project-Enabling (6), Technical Management (8), Technical (14). Maintenance is one of the technical processes (operation/maintenance phase of the life cycle spine).
- evidence: [S-0020]
- topic: engineering-process/software-lifecycle

### R2. Models and maintenance burden (from software-lifecycle)
- Q: Why do iterative/incremental models and phase-gate models differ in how much maintenance-style rework they create downstream?
- bloom: understand
- bank: review
- A: IID shortens feedback loops by repeating analysis/design/implementation/verification in cycles, catching requirement drift before it becomes post-delivery corrective work; phase gates buy commitment and control but delay feedback, moving change cost into the maintenance phase where defects cost far more (about 100x on large systems when found after delivery).
- evidence: [S-0085][S-0075]
- topic: engineering-process/software-lifecycle

### R3. Defect economics into maintenance (from software-lifecycle)
- Q: Defects found after delivery cost about 100x more to fix than during requirements/design. What does that imply for how a team should run its maintenance process?
- bloom: apply
- bank: review
- A: Maintenance change must be treated like development change: analyze before modifying, verify before releasing (regression testing), and keep the cost of change low through maintainability. The 100x premium also argues for design-for-change early — the cheapest maintenance is the change that never needs to be made late.
- evidence: [S-0075]
- topic: engineering-process/software-lifecycle
