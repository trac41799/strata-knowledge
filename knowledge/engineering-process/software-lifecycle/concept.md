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

# Software Lifecycle

## Claims

- A software life cycle is the entire span of activities from concept through disposal of a software product; life cycle models structure that span into stages with defined purposes, outputs, and transition criteria [T2][S-0020].
- ISO/IEC/IEEE 12207:2017 organizes software engineering into 30 processes in 4 categories — Agreement (2), Organizational Project-Enabling (6), Technical Management (8), Technical (14) — covering acquisition and supply, organizational support, project management, and the technical engineering spine [T2][S-0020].
- ISO 12207 is lifecycle-model-neutral: it does not mandate a particular model (waterfall, iterative, agile, etc.); it defines the processes any model must enact, and requires each project to select a model within which those processes run [T2][S-0020].
- The waterfall model sequences stages — requirements, design, implementation, verification, operation — with each stage completed before the next and feedback between stages; Royce (1970) documented this scheme and its risks [T3][S-0083].
- Royce's 1970 paper, later credited as the origin of the "waterfall," actually argued the sequential scheme was risky and recommended feedback, iteration between stages, and building a pilot version before full construction — the rigid one-pass reading was a later simplification, not Royce's recommendation [T3][S-0083].
- Iterative and incremental development (IID) is not a modern invention: documented IID projects and methods date back to the mid-1950s, decades before the agile movement [T3][S-0085].
- IID approaches share one aim — avoiding a single-pass, sequential, document-driven, gated-step process and building through repeated cycles with feedback — but vary from significant up-front specification with time-boxed increments to strongly evolutionary, feedback-driven development [T3][S-0085].
- The spiral model (Boehm 1986) is risk-driven: each cycle performs objective setting, risk assessment and reduction (e.g., prototyping), development and verification, and planning of the next cycle, making the lifecycle an iterative refinement governed by the project's dominant risks [T3][S-0084].
- Boehm positioned the spiral for large, complex projects where risk is the dominant driver, combining features of the waterfall with evolutionary prototyping [T3][S-0084].
- Phase-gate models make stage boundaries explicit — a stage completes with its documentation and review before the next begins, buying commitment and control at the cost of late feedback; iterative models run the same engineering activities repeatedly to shorten feedback loops [T3][S-0085][S-0084].
- Early defect removal is a major economic driver of lifecycle structure: finding and fixing a defect after delivery costs about 100x more than during requirements/design on large systems (about 5x on smaller ones), favoring lifecycles that verify and validate early [T3][S-0075].
- Tailoring is built into ISO 12207: the Life Cycle Model Management process requires projects to select a life cycle model and tailor the standard's processes to project needs, so an enacted process set is a tailored subset of the 30 processes, not the full set [T2][S-0020].
- Process-improvement frameworks are orthogonal to lifecycle models: CMMI V3.0 defines 31 practice areas across 8 domains to assess and improve organizational capability and does not prescribe a specific lifecycle model [T2][S-0022].
- ISO 25010:2023 added Safety as a ninth product quality characteristic, with subcharacteristics operational constraint, risk identification, fail-safe, hazard warning, and safe integration, making safety requirements specifiable and evaluable like other quality attributes [T2][S-0019].
- ISO 12207 defines Verification and Validation as distinct technical processes, so safety-critical lifecycles can pair each development level with explicit verification and validation activity that demonstrates requirements — including safety requirements — are satisfied [T2][S-0020].
- The Therac-25 accidents (1985–1987) are the canonical case study of lifecycle failure in a safety-critical system: software was reused from the Therac-20 without re-verification in the new context, safety interlocks that had been independent hardware circuits were moved into software, and reported faults were not reproduced or investigated before redeployment [T3][S-0080].

## Details

- The ISO 12207 technical spine: business or mission analysis, stakeholder needs and requirements, system/software requirements definition, architecture, design, implementation, integration, verification, transition, validation, operation, maintenance, disposal — with agreement, organizational, and technical management processes wrapping it [T2][S-0020].
- The spiral's risk-reduction repertoire is broad — prototyping for requirements risk, simulation for performance risk, incremental delivery for schedule risk — and each cycle picks the techniques matching its own risks [T3][S-0084].

## Boundaries / common misunderstandings

- "ISO 12207 is a lifecycle model like waterfall or agile": it is a process framework; model choice and tailoring are explicitly delegated to the organization [T2][S-0020].
- "The waterfall is what Royce recommended": his paper described the sequential scheme but argued for iteration and a pilot version; the rigid waterfall was a later simplification [T3][S-0083].
- "Iterative/incremental is just agile rebranded": IID predates agile by decades; agile methods are one family of IID practice, not its origin [T3][S-0085].
- "The spiral model is prototyping": prototyping is one risk-reduction technique inside the spiral; the defining feature is risk-driven iteration [T3][S-0084].
- "Safety-critical software just needs more testing": Therac-25 shows failures rooted in lifecycle decisions — reuse without re-verification, interlock design, fault response — and the standards response is dedicated verification/validation processes plus safety as an evaluated quality characteristic, not merely additional test effort [T2][S-0020][S-0080].

## References (evidence records)

- [S-0020] ISO/IEC/IEEE 12207:2017 — Software life cycle processes (standard).
- [S-0019] ISO/IEC 25010:2023 — Product quality model, Safety characteristic (standard).
- [S-0022] CMMI V3.0 — Capability Maturity Model Integration (standard).
- [S-0083] Royce 1970 — Managing the Development of Large Software Systems (WESCON).
- [S-0084] Boehm 1986 — A Spiral Model of Software Development and Enhancement (SIGSOFT SEN 11(4)).
- [S-0085] Larman & Basili 2003 — Iterative and Incremental Development: A Brief History (IEEE Computer 36(6)).
- [S-0075] Boehm & Basili 2001 — Software Defect Reduction Top 10 List (IEEE Computer 34(1)).
- [S-0080] Leveson & Turner 1993 — An Investigation of the Therac-25 Accidents (IEEE Computer 26(7)).
