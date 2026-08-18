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

# Software Maintenance — teaching

## Learning objectives (Bloom)

After this pack the learner can:

- **remember** — name the four maintenance types and the origin of the technical debt metaphor (F1, F3).
- **understand** — explain why most maintenance is not bug fixing, what Lehman's laws claim and about which class of programs (F2, F4, F5).
- **apply (bloom_target)** — classify real change requests into the four types; allocate maintenance investment from a workload mix.
- **analyze** — decompose a technical debt situation into principal, interest, and repayment conditions; interpret a system's evolution data through Lehman's laws.
- **evaluate (stretch)** — judge cost doctrines ("fix when it breaks") against the evidence.

## Worked example — maintenance-type classification

The Acme Ledger system receives these change requests. Classify each and justify:

| # | Request | Type | Why |
|---|---|---|---|
| 1 | "App crashes when a transaction has no description" | Corrective | Residual fault — behavior violates specification |
| 2 | "Support Windows Server 2025" | Adaptive | Environment change (OS upgrade) |
| 3 | "Add CSV export for auditors" | Perfective | New user-facing enhancement |
| 4 | "Refactor duplicate validation logic" | Preventive | Latent structural risk removed before it causes failure (also the restructuring family of perfective) |
| 5 | "Fix rounding error for 3-decimal currencies" | Corrective | Defect in implemented logic |
| 6 | "Update tax tables for new EU directive" | Adaptive | Regulatory environment change |
| 7 | "Speed up month-end close by 40%" | Perfective | Performance improvement |
| 8 | "Add health checks to catch silent DB degradation" | Preventive | Detect latent faults before they manifest |

Worked reasoning: the type depends on *why* the change exists, not what it touches. Bug-ish wording (3, 7) hides perfective work; platform wording (2, 6) marks adaptive; the two most valuable-to-misclassify are 4 and 8 — no reported fault is being fixed, so they are not corrective.

## Worked example 2 — reading evolution data with Lehman's laws

A team plots LOC and module count per release over 6 years: steady growth of ~8%/year, rising module coupling, and a long tail of fix releases after each major version. Lehman's lens: steady growth matches continuing growth; rising coupling matches increasing complexity (unmanaged); the fix-release tail after majors matches continuing change (requirements move between releases). The laws do not doom the system — they name the work: manage complexity deliberately, or the cost of the next enhancement grows.

## Elaboration prompts

- The survey says ~55% of maintenance requests are new requirements. If a company's backlog is 80% bugs, which of the two data points should make you question the other?
- Corrective vs adaptive can be ambiguous (a crash caused by an OS upgrade). What question settles the classification?
- Cunningham's metaphor has principal and interest. Which parts of a real codebase play each role — and what is "repayment" exactly?
- Lehman's "conservation of familiarity": why do huge releases fail even when they are technically sound? What does that imply for release planning?
- Preventive maintenance is usually the smallest budget line. What evidence in this pack argues for raising it — and what argues against?
- Why does program understanding precede safe change? How would you measure "understandability" to justify a refactor?

## Common misconceptions

1. **"Maintenance means fixing bugs."** The survey data says the reverse: the majority of requests and effort are perfective/adaptive. Calling all maintenance "bug fixing" mis-sizes teams and budgets.
2. **"Technical debt is just sloppy code."** The metaphor is about *deliberate or accumulated shortcuts whose interest is paid on every future change* — including hard-won knowledge that has not been consolidated into the code; and a little debt can be a rational accelerator if repaid promptly.
3. **"Lehman's laws are a license for fatalism"** ("software always rots, so why fight it?"). The laws describe empirical regularities in large E-type systems — and the complexity law explicitly describes the *work* (maintenance/reduction) as part of evolution; the whole point of maintenance practice is to do that work.
4. **"Preventive maintenance is testing you tack on at the end."** It is a distinct maintenance type — proactive detection and correction of latent faults — and belongs to a maintenance program, not to final testing.
5. **"Maintenance is the cheap phase after the real work."** It commonly exceeds half of lifecycle costs; the leverage is design-for-maintainability and early verification, not treating maintenance as an afterthought.

## Feynman targets

- Explain to a finance-minded manager (in under 2 minutes): why the maintenance budget is mostly *not* repair, and what "technical debt" means with principal/interest language.
- Explain to a junior dev: the four maintenance types, with one real example of each from this pack.
- Explain to a skeptical architect: what Lehman's laws claim, about which class of systems, and why they are regularities rather than inevitabilities.
- Explain to yourself: why "over half of lifecycle cost" and "~55% of requests are enhancements" belong together in one mental model of maintenance.

## Interleaving hooks

- **engineering-process/software-lifecycle (prerequisite):** maintenance is the technical process that runs after delivery — the same 12207 spine, the same 100x late-defect economics, now applied to changes on a live system.
- **engineering-process/requirements-engineering:** perfective maintenance is requirements evolution arriving post-delivery; classifying an MR correctly is half the requirements analysis.
- **quality-testing:** corrective and preventive maintenance depend on defect detection (testing, monitoring); regression verification gates every change.
- **operations/incident-response (forward link):** corrective maintenance supplies the fixes that incident postmortems demand; preventive maintenance is where incident prevention shows up in the codebase.
