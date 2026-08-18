---
id: engineering-process/software-lifecycle
title: Software Lifecycle
band: B5
track: engineering-process
tier: T2
bloom_target: apply
prerequisites: [engineering-process/requirements-engineering]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-software-lifecycle
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0019, S-0020, S-0022, S-0075, S-0080, S-0083, S-0084, S-0085]
---

# Software Lifecycle — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — State the four ISO 12207 process categories with counts, and name the classic lifecycle models with their originating sources. (evidence: S-0020, S-0083, S-0084)
- understand — Explain why ISO 12207 is lifecycle-model-neutral, why Royce's paper does not endorse a rigid waterfall, and why IID predates agile. (evidence: S-0020, S-0083, S-0085)
- apply — Given a project profile (requirements stability, criticality, risk), select a lifecycle model and a tailored subset of ISO 12207 processes. (evidence: S-0020, S-0085, S-0084) — **bloom_target**
- analyze — Diagnose a failed or risky project by mapping its lifecycle failures to processes (Verification, Validation, Configuration Management) and quality characteristics (ISO 25010 safety). (evidence: S-0080, S-0020, S-0019)
- evaluate — Assess "phase-gate always" vs "continuous always" doctrines against defect-cost, IID-history, and risk-driven evidence. (evidence: S-0075, S-0085, S-0084)

## Worked example

### Part A — Selecting and tailoring a lifecycle for a medical-device companion

Context: a company builds a two-part product: (1) firmware for a continuous glucose monitor (CGM) — safety-critical, requirements audited, changes rare after freeze; (2) a companion mobile app — user-facing, requirements evolving monthly, fast release cadence. One team must plan both lifecycles.

Step 1 — Classify risk and feedback cost. Firmware: failures can harm patients (ISO 25010 safety: fail-safe, hazard warning, safe integration), so every requirement needs a demonstration path; change is expensive (regulatory). App: failure is inconvenience; feedback is cheap and valuable.

Step 2 — Select models. Firmware: phase-gated, V-style arrangement — each development level (requirements → design → implementation) paired with a verification level (validation tests ↔ requirements, integration tests ↔ design, unit tests ↔ implementation), the structure the ISO 12207 Verification and Validation processes are designed to support. App: iterative and incremental — short cycles, stakeholder feedback each iteration, avoiding a single-pass gated-step process (the documented IID pattern since the 1950s).

Step 3 — Tailor ISO 12207 for each. Both projects keep: stakeholder needs, requirements definition, design, implementation, integration, verification, validation, risk management, configuration management, project planning/control, quality assurance. The app lightens: heavyweight information-management artifacts, formal acceptance ceremony. The firmware adds: strict configuration management (baselines for each audited release), a risk-management loop (spiral-style risk assessment at each gate), and safety-specific validation (the Therac-25 lesson: reuse across contexts — here, shared code between app and firmware must be re-verified in each context, never assumed).

Step 4 — Economic check. The 100x late-fix premium means both projects must verify early: firmware does static analysis and design review at the design level; the app runs automated verification inside each iteration rather than saving all testing for release.

### Part B — The spiral's risk-driven cycle applied

A legacy bank migration project: 8 months, 40 services, high integration risk. A pure waterfall is risky (feedback arrives at the end); pure IID without risk planning iterates blindly. The spiral structure: cycle 1 — set objectives and constraints, then risk-assessment: dominant risks are data-integrity during cutover and unknown service dependencies; mitigation: a thin vertical slice migration + simulation of cutover traffic. Cycle 2 — re-assess: remaining risk is parallel-run correctness; mitigation: shadow traffic comparison. Each cycle ends by planning the next, so the lifecycle itself is governed by which risks remain — not by a fixed phase script.

## Elaboration prompts

- Why does ISO 12207 define processes rather than a model — what breaks if a standard mandates one model for all projects? (evidence: S-0020)
- Royce's paper is famous as the waterfall's origin, yet he recommended iteration. Why do you think the simplified reading won, and what does that tell you about citing primary sources? (evidence: S-0083)
- If iterative development has roots in the 1950s, what was actually new about the agile movement's claim? (evidence: S-0085)
- The 100x late-defect-fix claim is cited everywhere, but the exact multiplier is contested. What does the evidence actually support, and how should you phrase the claim? (evidence: S-0075)
- Where exactly did the Therac-25 lifecycle break — which process should have caught each failure, and why didn't it? (evidence: S-0080, S-0020)
- Why is CMMI capability assessment independent of the lifecycle model a project uses? (evidence: S-0022)

## Common misconceptions

1. **"ISO 12207 prescribes waterfall (or prescribes agile)."** It prescribes neither: 30 processes across 4 categories that any model enacts, with model choice and tailoring left to the project. (evidence: S-0020)
2. **"Royce invented the waterfall and recommended it."** He documented the sequential scheme and argued it was risky, recommending feedback, iteration, and a pilot version; the rigid reading came later. (evidence: S-0083)
3. **"Iterative development is a 1990s/2000s agile invention."** Documented IID projects date to the mid-1950s; agile is one family of IID, not its origin. (evidence: S-0085)
4. **"The spiral model is just prototyping."** Prototyping is one risk-reduction technique used inside spiral cycles; the model's defining structure is risk-driven iteration with explicit risk assessment and reduction each cycle. (evidence: S-0084)
5. **"Safety-critical failures are caused by insufficient testing, so test more."** Therac-25's failures were lifecycle decisions — reuse without re-verification, interlocks moved from hardware into software, faults not reproduced before redeployment. Standards answer with dedicated Verification/Validation processes and Safety as an evaluated quality characteristic. (evidence: S-0080, S-0020, S-0019)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why "the plan" of a project is a choice, not a given: the same software can be built in one long pass or in repeated cycles, and the choice depends on how sure you are about what to build. Grade against the model-neutrality and IID claims. (evidence: S-0020, S-0085)
2. Why a project that finds its mistakes late pays much more than one that finds them early — and why every lifecycle model tries to push verification earlier. Grade against the defect-cost claim. (evidence: S-0075)
3. Why a machine that can harm people needs a different workflow than an app: what changes when every requirement must be shown to be satisfied. Grade against the safety and Therac-25 claims. (evidence: S-0019, S-0020, S-0080)

## Interleaving hooks

- **engineering-process/requirements-engineering (prerequisite):** FRs vs NFRs feed model selection — NFR-heavy, stable requirements favor gated models; volatile ones favor IID (R1, R3 in validation.md).
- **quality-testing/quality-models (recommended chain):** ISO 25010 characteristics (esp. safety) are the vocabulary for what lifecycles must verify; revisit after learning the quality model.
- **quality-testing/software-testing-basics (related):** the ISO 12207 Verification and Validation processes are the formal home of test levels and acceptance strategies.
- **engineering-process/process-tailoring (related):** tailoring is the bridge from the 30-process standard to a project's enacted process set — this topic covers the standard side.
- **operations/continuous-integration (related):** CI is IID's verification loop made automatic — map the "feedback within the cycle" claim to pipeline practice.
