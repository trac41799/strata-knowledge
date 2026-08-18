---
id: engineering-process/requirements-engineering
title: Requirements Engineering
band: B5
track: engineering-process
tier: T2
bloom_target: apply
prerequisites: []
related: []
recommended: []
status: published
schema-version: 1
owner: l1-requirements-engineering
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0020, S-0022, S-0073, S-0074, S-0075]
---

# Requirements Engineering — validation

## Formative (practice)

- Q: List the four families of requirements elicitation techniques identified in the classic RE roadmap, with one example technique each.
- bloom: remember
- bank: formative
- A: Traditional (interviews/surveys, group elicitation); observational (ethnography/participant observation, protocol analysis); model-based (goal-based, scenarios, use cases); exploratory (prototyping).
- evidence: [S-0074]
- topic: engineering-process/requirements-engineering

- Q: A colleague says "requirements are just gathered from users." Explain why this is misleading.
- bloom: understand
- bank: formative
- A: Stakeholders rarely articulate needs directly; requirements are actively elicited and negotiated in organizational contexts that are conflict-prone and dynamic, and they evolve — so "gathering" understates the discovery and agreement work RE requires.
- evidence: [S-0074]
- topic: engineering-process/requirements-engineering

- Q: Distinguish a functional from a non-functional requirement, giving one of each for an online payment gateway.
- bloom: understand
- bank: formative
- A: Functional: a capability the system shall provide, e.g., "the gateway shall authorize a card payment within 10 seconds." Non-functional: a quality/constraint, e.g., availability >= 99.9%, throughput, or PCI-DSS compliance — expressible via quality characteristics such as performance efficiency or security (ISO 25010).
- evidence: [S-0019, S-0017]
- topic: engineering-process/requirements-engineering

- Q: The requirement "The system shall be fast, secure, and user-friendly" fails which 29148 quality characteristics? Rewrite it as verifiable requirements.
- bloom: apply
- bank: formative
- A: It is not verifiable, not unambiguous, and not singular (three qualities in one statement). Rewrite with measurable bounds, e.g., "the checkout shall complete within 2 s (p95)"; "all stored card data shall be encrypted at rest using AES-256"; "a new user shall complete checkout without assistance in at most 3 minutes (usability test)".
- evidence: [S-0073]
- topic: engineering-process/requirements-engineering

## Summative (mastery checkpoint)

- Q: An interview yields: "We need the app to work offline and sync later." Write one functional and one non-functional requirement for the sync capability, each unambiguous and verifiable.
- bloom: apply
- bank: summative
- A: FR: "The app shall queue records created while offline and transmit them to the server when connectivity returns, without user intervention." NFR: "The app shall resume interrupted syncs and shall complete a sync of up to 100 queued records within 60 seconds of connectivity restoration." Both are testable; avoid vague terms like "soon" or "best effort".
- evidence: [S-0073]
- topic: engineering-process/requirements-engineering

- Q: A change request ("add dark mode") arrives mid-project. Walk through the requirements-management activities that must occur before the change is accepted, and explain traceability's role.
- bloom: analyze
- bank: summative
- A: Evaluate impact via traceability (which requirements, design elements, code, and tests are affected); assess cost, schedule, and risk; prioritize against other work; obtain approval through change control; then update the specification, affected artifacts, and tests under configuration control, keeping traceability current.
- evidence: [S-0017, S-0022]
- topic: engineering-process/requirements-engineering

- Q: Your manager cites "fixing a bug after release costs 100x more" to justify a heavy upfront SRS for a small internal tool. Evaluate the argument: what does the evidence support, and what does it not?
- bloom: evaluate
- bank: summative
- A: The direction (late fixes cost more) is well supported, but the 100x figure is a large-system finding; escalation is closer to ~5x for small, less critical systems and the exact multipliers are contested. For a small internal tool, lighter-weight requirements practice (backlog + acceptance criteria) may be justified — the evidence supports early validation, not a specific documentation weight.
- evidence: [S-0075]
- topic: engineering-process/requirements-engineering

## Review (spaced repetition — interleaved with prerequisites)

- Q: In the ISO 12207:2017 lifecycle, which technical processes produce requirements, and how do Verification and Validation relate to them?
- bloom: understand
- bank: review
- A: Stakeholder Needs and Requirements Definition, then System/Software Requirements Definition, produce the requirements; Verification checks the product meets specified requirements; Validation checks it fulfills intended use — both trace back to the requirements.
- evidence: [S-0020]
- topic: engineering-process/software-lifecycle

- Q: Why must acceptance tests be traceable to requirements, and what is the difference between verifying a requirement and validating the product?
- bloom: understand
- bank: review
- A: Traceability ensures every requirement is covered by a test and every test serves a requirement (no orphan work, no untested requirement). Verification: artifact matches spec ("built right"); validation: product meets the real need ("right thing") — the two can disagree when the spec is wrong.
- evidence: [S-0017, S-0020]
- topic: quality-testing/software-testing-basics

- Q: An agile team maintains a backlog of user stories instead of an SRS. How do the 29148 quality criteria and RE management discipline still apply?
- bloom: apply
- bank: review
- A: Each story needs unambiguous, testable acceptance criteria (verifiable, singular); the backlog is a managed, prioritized requirements set with change control; traceability (story → code → tests) still supports impact analysis. RE's quality discipline carries over; only the artifact form and cadence change.
- evidence: [S-0073, S-0074]
- topic: engineering-process/agile-methods
