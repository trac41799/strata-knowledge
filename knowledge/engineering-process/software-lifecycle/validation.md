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

# Software Lifecycle — validation

Item anatomy: `- Q` · `- bloom` · `- bank` · `- A` · `- evidence` · `- topic`.

## Formative (practice)

### F1. ISO 12207 structure
- Q: How many processes does ISO/IEC/IEEE 12207:2017 define, and what are the four process categories with their process counts?
- bloom: remember
- bank: formative
- A: 30 processes in 4 categories: Agreement (2: acquisition, supply), Organizational Project-Enabling (6), Technical Management (8), Technical (14).
- evidence: [S-0020]
- topic: engineering-process/software-lifecycle

### F2. Model neutrality
- Q: A team says "ISO 12207 forces you to work waterfall." Explain why that claim is wrong, using what the standard actually requires.
- bloom: understand
- bank: formative
- A: 12207 defines processes (what activities must exist), not a model (how stages are arranged). It is lifecycle-model-neutral: waterfall, iterative, incremental, and agile all enact the same processes. The standard requires each project to select a life cycle model and tailor the processes to fit it, so the model is the organization's choice.
- evidence: [S-0020]
- topic: engineering-process/software-lifecycle

### F3. Model selection for a fixed-requirements product
- Q: An avionics vendor must build a flight-control subsystem whose requirements are frozen and externally audited for traceability. Propose a lifecycle model and say which ISO 12207 processes carry the audit burden.
- bloom: apply
- bank: formative
- A: Choose a sequential, phase-gated arrangement (waterfall or a V arrangement) because requirements are stable, changes are costly, and traceability is audited; the Verification and Validation processes plus Configuration Management and Quality Assurance carry the audit burden, since each development level is paired with an explicit verification activity and a baseline is maintained.
- evidence: [S-0020][S-0075]
- topic: engineering-process/software-lifecycle

### F4. What Royce actually said
- Q: The waterfall is often attributed to Royce (1970) as a recommended rigid process. What did the paper actually argue?
- bloom: understand
- bank: formative
- A: Royce documented the sequential scheme but argued it was risky: he recommended feedback between stages, iteration, and building a pilot version before full construction. The rigid one-pass "waterfall" reading was a later simplification, not his recommendation.
- evidence: [S-0083]
- topic: engineering-process/software-lifecycle

## Summative (mastery checkpoint)

### S1. Select and lay out a lifecycle
- Q: A startup must build an ML-powered recommendation service: requirements are highly uncertain, users must react early, and the team is small. Select a lifecycle model, justify it against the alternatives, and list which ISO 12207 processes you would tailor out or lighten and why.
- bloom: apply
- bank: summative
- A: Select iterative and incremental development: uncertain requirements make one-pass sequential phases wasteful because feedback arrives too late; IID shortens feedback loops by repeating analysis/design/implementation/verification in cycles (the aim all IID approaches share). Tailor the enacted process set from the 30 ISO 12207 processes: keep stakeholder needs, requirements definition, design, implementation, integration, verification, validation, risk and project management; lighten heavyweight agreement/information-management artifacts until the product stabilizes. Guardrail: record and validate each iteration's outcomes so early defect removal (100x cost gap) is actually realized.
- evidence: [S-0085][S-0020][S-0075]
- topic: engineering-process/software-lifecycle

### S2. Diagnose Therac-25 through the lifecycle lens
- Q: The Therac-25 overdosed patients because of software errors. Identify the lifecycle failures documented by the investigation and map each to an ISO 12207 process or an ISO 25010 safety subcharacteristic.
- bloom: analyze
- bank: summative
- A: Failures include: reuse of Therac-20 software without re-verification in the new hardware context (missing Validation/Verification of the change); relying on software for interlocks previously implemented as independent hardware (missing fail-safe design — ISO 25010 safe-integration/fail-safe; design decisions without risk analysis); inadequate testing and failure to reproduce reported faults before redeployment (weak Verification process, Configuration Management absent on fault records). The lesson: safety-critical lifecycles must pair each development level with explicit verification/validation and treat safety as an evaluated quality characteristic, not an afterthought.
- evidence: [S-0080][S-0020][S-0019]
- topic: engineering-process/software-lifecycle

### S3. Evaluate a process doctrine
- Q: "All projects should use phase gates." "All projects should be continuous." Evaluate both doctrines using the evidence: defect-cost data, the documented history of IID, and the spiral model's rationale.
- bloom: evaluate
- bank: summative
- A: Both doctrines overgeneralize. Phase gates buy commitment and control but delay feedback — fatal when requirements are uncertain. IID has half a century of documented practice and shortens feedback loops, but its cost is coordination and rework discipline. The spiral model shows the synthesis: choose cycle structure and risk-reduction techniques per dominant risk. Defect-cost evidence (100x late-fix premium) argues for early verification in any model, not for a particular one. Selection is contingent on requirements stability, risk profile, and feedback cost — a fixed doctrine ignores exactly the variables that matter.
- evidence: [S-0075][S-0085][S-0084]
- topic: engineering-process/software-lifecycle

## Review (spaced repetition — interleaved with prerequisites)

### R1. Requirement types (from requirements-engineering)
- Q: Distinguish a functional requirement from a non-functional requirement and give one example of each.
- bloom: remember
- bank: review
- A: A functional requirement states a behavior the system must exhibit ("the system shall cancel an order when the user confirms"); a non-functional requirement states a constraint or quality property ("the system shall be available 99.9% of the time", "responses shall complete within 200 ms"). NFRs are the bridge to quality models and to lifecycle verification planning.
- evidence: [S-0020]
- topic: engineering-process/requirements-engineering

### R2. Tailoring recap
- Q: In ISO 12207, what does "tailoring" mean, and why is it required rather than optional?
- bloom: understand
- bank: review
- A: Tailoring is selecting and adapting the standard's 30 processes to the project's characteristics (size, criticality, domain, contract) within the Life Cycle Model Management process. It is required because no project enacts the full standard unchanged — a tailored subset is the project's actual process set, and it must still satisfy the process purposes that apply.
- evidence: [S-0020]
- topic: engineering-process/software-lifecycle

### R3. From NFR to lifecycle decision (from requirements-engineering)
- Q: A client specifies an availability NFR of 99.9% for a payment service. Which lifecycle decisions follow, and why?
- bloom: apply
- bank: review
- A: The NFR must be verifiable: the lifecycle needs explicit verification and validation activities (fault-injection/recovery tests for the reliability characteristic, performance testing), a risk-management process (the spiral's risk-driven cycle fits such dependability-critical systems), and traceability so the requirement is demonstrated, not asserted. If requirements are still moving, an iterative model keeps re-verification cheap; if frozen, phase-gated verification suffices.
- evidence: [S-0020][S-0019][S-0075]
- topic: engineering-process/requirements-engineering
