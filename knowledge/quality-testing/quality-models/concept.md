---
id: quality-testing/quality-models
title: Quality Models
band: B5
track: quality-testing
tier: T2
bloom_target: understand
prerequisites: [engineering-process/requirements-engineering]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-quality-models
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0019, S-0108, S-0109, S-0110]
---

# Quality Models

## Claims

- A quality model is a structured scheme for specifying and evaluating quality: it decomposes quality into characteristics and subcharacteristics that provide a shared vocabulary, with associated measures making them assessable [T2][S-0019][S-0110].
- ISO/IEC 25010:2023 defines the product quality model with 9 characteristics — functional suitability, performance efficiency, compatibility, interaction capability, security, safety, reliability, maintainability, flexibility — each decomposed into subcharacteristics [T2][S-0019].
- The 2023 edition restructured the 2011 model: Safety was added as a ninth characteristic, Usability was renamed Interaction Capability, and Portability became Flexibility; subcharacteristics such as inclusivity, resistance, and scalability were added [T2][S-0019].
- Reliability decomposes into faultlessness, fault tolerance, availability, and recoverability; security into confidentiality, integrity, non-repudiation, accountability, authenticity, and resistance; maintainability into modularity, reusability, analysability, modifiability, and testability [T2][S-0019].
- ISO 25010 distinguishes two complementary views: product quality (static and dynamic properties of the product itself) and quality in use (the outcome when the product is used by specific users to achieve specific goals in specific contexts of use) [T2][S-0019][S-0110].
- The quality-in-use model has 5 characteristics: effectiveness, efficiency, satisfaction, freedom from risk, and context coverage [T2][S-0019].
- Product quality makes quality in use possible but does not guarantee it: outcomes depend on the context of use, so quality in use must be measured where the product is used — or, before release, in a test environment designed and used exclusively by the intended users for their goals and contexts [T2][S-0110].
- SQuaRE measurement (ISO 25020:2019) distinguishes quality measures on internal properties (static attributes of the product — architecture, structure, code), quality measures on external properties (dynamic behavior of the executing product), and quality-in-use measures (outcomes in context) [T2][S-0110].
- The measurement framework (ISO 25020:2019) bridges quality models and evaluation: it governs how measures are developed and selected, including quality measure elements, reliability and validity checks, and documentation of measures [T2][S-0110].
- In SQuaRE, quality requirements are specified in terms of the quality model's characteristics and subcharacteristics; each requirement is then linked to quality measures, and evaluation checks the measured values — giving traceability from requirement to metric to verdict [T2][S-0019][S-0110].
- McCall et al. (1977) defined 11 quality factors under three perspectives — product operation (correctness, reliability, efficiency, integrity, usability), product revision (maintainability, flexibility, testability), and product transition (portability, reusability, interoperability) — and linked each factor to criteria and metrics [T3][S-0108].
- Boehm et al. (1978) defined a hierarchical model: top-level characteristics (as-is utility, maintainability, portability) decomposed into second-level attributes and finally into primitive source-code characteristics, anchoring quality in measurable code properties [T3][S-0109].
- The historical models established the pattern — characteristics to subcharacteristics to metrics — that ISO 9126 and then SQuaRE (ISO 25010) standardized; McCall and Boehm remain the canonical precursors of modern quality models [T2][S-0019][S-0108][S-0109].
- Because ISO 25010:2023 includes safety and security as product quality characteristics, safety and security requirements are specified, measured, and evaluated through the same model as all other quality characteristics [T2][S-0019].

## Details

- SQuaRE is organized into divisions with distinct roles: quality models (2501n), quality measurement (2502n, including the 25020 measurement framework), evaluation (2503n), and quality requirements (2504n) — together forming a specification-measurement-evaluation chain around the quality model [T2][S-0019][S-0110].
- The ISO 25010 safety subcharacteristics (operational constraint, risk identification, fail-safe, hazard warning, safe integration) give a concrete vocabulary for specifying safety requirements and their verification [T2][S-0019].

## Boundaries / common misunderstandings

- "A quality model is a scoring checklist": it supports specifying requirements, choosing measures, and evaluating quality through the lifecycle; a single composite score is neither its purpose nor defined by it [T2][S-0019][S-0110].
- "Quality in use = user satisfaction": satisfaction is one of five quality-in-use characteristics; effectiveness, efficiency, freedom from risk, and context coverage are separate dimensions that must be measured independently [T2][S-0019].
- "Internal metrics prove the product is good": measures on internal or external properties indicate quality in use only indirectly; outcomes must be measured in the context of use [T2][S-0110].
- "McCall and Boehm are modern alternatives to ISO": they are historical precursors; the current codified model is ISO 25010, with the historical models retained for lineage and vocabulary [T2][S-0019][S-0108][S-0109].
- "A quality model resolves trade-offs between characteristics": it names the dimensions (e.g., security vs interaction capability); resolving conflicts between characteristics remains a per-project engineering decision [T2][S-0019].

## References (evidence records)

- [S-0019] ISO/IEC 25010:2023 — Product quality model (standard).
- [S-0110] ISO/IEC 25020:2019 — SQuaRE quality measurement framework (standard).
- [S-0108] McCall, Richards & Walters 1977 — Factors in Software Quality (RADC-TR-77-369).
- [S-0109] Boehm, Brown, Kaspar, Lipow, MacLeod & Merritt 1978 — Characteristics of Software Quality (North-Holland).
