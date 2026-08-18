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

# Requirements Engineering

## Claims

### Nature and scope

- Requirements engineering (RE) is the discipline of discovering, eliciting, developing, analyzing, verifying, validating, communicating, documenting, and managing requirements; ISO/IEC/IEEE 29148:2018 defines it as an interdisciplinary function mediating between the acquirer and the developer/supplier domains to establish and maintain the requirements of the system, software, or service of interest. [T2][S-0073]
- SWEBOK v4 devotes a full Knowledge Area to Software Requirements, covering elicitation (sources and techniques), analysis (basic and formal analysis, QoS economics, conflict resolution), specification (natural language, acceptance criteria, model-based), validation (reviews, simulation, prototyping), and management (scrubbing, change control, tracing, prioritization). [T2][S-0017]
- ISO/IEC/IEEE 12207:2017 defines requirements-related technical processes — Stakeholder Needs and Requirements Definition and System/Software Requirements Definition — alongside Verification and Validation processes that check requirements are satisfied. [T2][S-0020]
- RE is not a single upfront phase: the canonical RE roadmap frames it as interleaved activities — elicitation, modelling and analysis, communication and agreement, and evolution — recurring throughout the life cycle; managing change (impact analysis, configuration management) is a fundamental RE activity. [T3][S-0074]
- Requirements problems are "wicked": analysis boundaries are ill-defined, requirements live in organizational contexts, and stakeholder goals conflict — which is why elicitation and negotiation, not just collection, are needed. [T3][S-0074]

### Types of requirements

- A functional requirement states a capability the system shall provide ("shall" behavior); a non-functional requirement constrains qualities or conditions of the solution (performance, security, usability, maintainability, ...). [T2][S-0017]
- ISO/IEC 25010:2023 defines nine product quality characteristics — functional suitability, performance efficiency, compatibility, interaction capability, security, safety, reliability, maintainability, flexibility — giving a vocabulary for stating and verifying quality (non-functional) requirements. [T2][S-0019]

### Elicitation

- Elicitation draws requirements from multiple sources (stakeholders, existing systems, documentation, domain constraints) using techniques such as interviews, facilitated workshops, observation, prototyping, and use cases/scenarios. [T2][S-0017]
- Elicitation techniques fall into four families — traditional (interviews, surveys, group elicitation), observational (ethnography, protocol analysis), model-based (goals, scenarios, use cases), and exploratory (prototyping) — and prototyping is especially suited to high-uncertainty situations needing early stakeholder feedback. [T3][S-0074]
- No single elicitation technique suffices in all contexts: techniques are combined (e.g., a prototype used to provoke discussion in a workshop), and choice depends on the situation and the stakeholders involved. [T3][S-0074]

### Specification

- ISO/IEC/IEEE 29148:2018 defines characteristics of a good individual requirement (necessary, appropriate, implementation-free, unambiguous, complete, singular, feasible, verifiable, correct, conforming) and of a good set of requirements (complete, consistent, feasible, comprehensible). [T2][S-0073]
- Quality criteria make requirements usable downstream: an unambiguous requirement has a single interpretation, and a verifiable requirement has a feasible test or analysis that can demonstrate satisfaction. [T2][S-0073]
- 29148:2018 provides requirements specification templates and content guidance and replaced the classic SRS recommended practice IEEE 830-1998. [T2][S-0073]

### Validation and verification

- Requirements validation checks that the stated requirements capture what stakeholders actually need ("building the right thing") — via reviews, prototyping, and simulation; requirements verification checks that the specification conforms to quality criteria and standards ("building it right"). [T2][S-0017]
- ISO 12207 distinguishes Validation (the product fulfills its intended use) from Verification (the product meets specified requirements); both are defined technical processes. [T2][S-0020]

### Traceability and management

- Traceability links each requirement to its source (backward) and to downstream artifacts — design, code, tests (forward); bidirectional traceability from need to solution is expected by CMMI V3.0 RDM, and traceability is a requirement attribute in 29148:2018 (each requirement should be traceable, distinct from the set-level characteristics above). [T2][S-0022][S-0073]
- Requirements management covers scrubbing, change control, tracing, and prioritization: proposed changes are evaluated for impact (affected requirements, design, code, tests) before approval, then incorporated under configuration control. [T2][S-0017]
- CMMI V3.0's RDM (Requirements Development and Management) is one of the 17 core practice areas, governing eliciting, analyzing, specifying, and managing requirements across all domains. [T2][S-0022]
- 29148:2018 provides guidance for applying requirements engineering and management within the requirements-related processes of ISO/IEC/IEEE 12207 and 15288, applied iteratively and recursively across the life cycle. [T2][S-0073]

### Cost of getting it wrong

- The later a requirements defect is found, the more it costs to fix: Boehm & Basili (2001) report that finding and fixing a problem after delivery is often 100x more expensive than during requirements/design for large systems (roughly 5x for smaller, less critical systems); the direction is consistent across studies, though exact multipliers are contested. [T3][S-0075]

## Details

Requirements engineering process loop: elicit (interviews, workshops,
observation, prototyping, use cases) → analyze (resolve conflicts, detect
omissions, prioritize) → specify (unambiguous, verifiable "shall"
statements with acceptance criteria, per 29148 characteristics) → validate
(reviews, prototyping, simulation against stakeholder needs) → manage
(traceability, change control) — iterating as understanding grows and as
requirements evolve during development and operation.

## Boundaries / common misunderstandings

- "Gathering" requirements is a misnomer: stakeholders rarely articulate their true needs directly, so requirements are elicited, negotiated, and iterated (ill-defined, conflict-prone problems). [T3][S-0074]
- Non-functional requirements are not optional extras or "future work": qualities such as performance, security, and safety are real requirements that must be stated and verified. [T2][S-0019]
- Requirements state what, not how: specifying implementation prematurely (over-constraining the solution) is a classic RE error; design freedom must be preserved. [T2][S-0017]
- Verification is not validation: passing verification says the artifact matches the spec, not that the spec matches the need — both are required. [T2][S-0017][S-0020]
- Traceability is not documentation overhead: it is what makes impact analysis, change control, and completeness checking possible. [T2][S-0022][S-0017]
- A frozen SRS is not the only way to do RE: agile methods treat requirements as evolving backlog items with acceptance criteria; the quality criteria and management discipline still apply. [T3][S-0074]
- The "100x" late-fix multiplier is a large, phase-gated-project finding, not a universal law: smaller and agile contexts see flatter escalation. [T3][S-0075]

## References (evidence records)

- S-0017 — SWEBOK v4.0 (IEEE CS, 2024) — Software Requirements KA and Professional Practice KA.
- S-0019 — ISO/IEC 25010:2023 — product quality model (9 characteristics incl. safety).
- S-0020 — ISO/IEC/IEEE 12207:2017 — lifecycle processes (requirements-related, verification, validation).
- S-0022 — CMMI V3.0 (ISACA, 2023) — RDM core practice area.
- S-0073 — ISO/IEC/IEEE 29148:2018 — requirements engineering standard.
- S-0074 — Nuseibeh & Easterbrook (2000) — Requirements Engineering: A Roadmap.
- S-0075 — Boehm & Basili (2001) — Software Defect Reduction Top 10 List.
