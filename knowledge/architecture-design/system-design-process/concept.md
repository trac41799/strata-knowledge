---
id: architecture-design/system-design-process
title: System Design Process
band: B5
track: architecture-design
tier: T2
bloom_target: analyze
prerequisites: [architecture-design/architectural-styles, engineering-process/requirements-engineering]
related: [engineering-process/software-lifecycle, quality-testing/quality-models]
recommended: [quality-testing/quality-models]
status: published
schema-version: 1
owner: l1-system-design-process
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0018, S-0019, S-0020, S-0021, S-0152, S-0153, S-0154]
---

# System Design Process

## Claims

### Requirements → architecture → design

- SWEBOK v4 organizes the development pipeline into distinct Knowledge Areas — Requirements, Architecture, Design, Construction — where the Architecture KA covers the system's fundamental structure and the Design KA covers detailed design; requirements are the input that architecture and design elaborate. [T2][S-0017]
- ISO/IEC/IEEE 12207:2017 defines architecture definition and design definition as distinct lifecycle technical processes: architecture definition transforms requirements into candidate architectures and selects among them; design definition transforms the architecture into detailed design suitable for construction (claims citing S-0020 are dated to the 2017 edition). [T2][S-0020]
- The three activities iterate: requirements, architecture, and design are applied iteratively and refined as implementation and operation reveal problems — they are not a single sequential pass. [T2][S-0017][S-0020]
- CS2023's Software Engineering KA includes architectural design and design-process competencies — designing in the context of requirements, with iterative refinement — among the core software development knowledge units. [T2][S-0018]

### Architecture description (ISO/IEC/IEEE 42010)

- ISO/IEC/IEEE 42010:2022 defines architecture description as the standard concept: an architecture description is a work product used to express an architecture, and the standard specifies the concepts — stakeholder, concern, view, viewpoint, correspondence — and their relationships. [T2][S-0021]
- In 42010, a viewpoint specifies the conventions for constructing, using, and analyzing views to address a set of related concerns; a view is a work product expressing the architecture of a system from the perspective of the system concerns addressed by that viewpoint. [T2][S-0021]
- The reason for viewpoints is stakeholder communication: different stakeholders (end users, developers, operators, acquirers) have different concerns, and no single view addresses them all; multiple viewpoints, with correspondences between their views, are what make an architecture description usable. [T2][S-0021]
- 42010 generalizes architecture frameworks: a framework (e.g., Kruchten's 4+1, TOGAF, DoDAF) is a set of conventions for building an architecture description within a community or domain — a set of viewpoints and rules for their use. [T2][S-0021]
- Kruchten's 4+1 view model (1995) is the canonical worked example: logical, process, development, and physical views plus scenarios (the "+1"), each addressing the concerns of a stakeholder group, show how a single architecture is described by multiple concurrent views. [T3][S-0153]
- Documenting an architecture means recording decisions and their rationale, not just diagrams: Perry & Wolf define a software architecture as a set of architectural elements (processing, data, connecting) with a particular form, explicated by rationale — the rationale captures the motivation for the choice of style, elements, and form. [T3][S-0154]

### Tradeoff analysis and architecture evaluation

- Architectural decisions trade quality attributes against one another; ISO/IEC 25010:2023 supplies the vocabulary — nine product quality characteristics — for stating what is being traded, and its performance-efficiency characteristic decomposes into time behaviour, resource utilization, and capacity. [T2][S-0019]
- ATAM (Architecture Tradeoff Analysis Method, SEI, 2000) evaluates an architecture against its quality-attribute goals — e.g., performance or modifiability — using stakeholder-driven scenarios; it reveals how well the architecture satisfies those goals and provides insight into the tradeoffs involved. [T3][S-0152]
- ATAM's outputs are sensitivity points (decisions where a slight change makes a significant difference in a quality attribute), tradeoff points (decisions affecting more than one quality attribute), and risks/non-risks; the method surfaces these while the architecture can still be changed, rather than after implementation locks them in. [T3][S-0152]
- ATAM analyzes quality attributes, not functional correctness: whether the architecture can meet its quality requirements is the evaluation target, while functional correctness is established by verification and testing. [T3][S-0152]
- Architecture evaluation is a stakeholder activity: ATAM brings together managers, developers, maintainers, testers, reusers, end users, and customers to elicit business drivers and prioritize the quality-attribute goals (utility tree) the architecture must satisfy. [T3][S-0152]

### Capacity and scale

- ISO 25010:2023 defines capacity as a subcharacteristic of performance efficiency, giving requirements language for scale: a capacity requirement states how much of a resource the system must handle (throughput, data volume, users). [T2][S-0019]
- Scale is decided during architecture definition: the 12207 architecture definition process establishes candidate architectures and assesses them against the requirements — including capacity and performance requirements — before one is selected; scaling properties follow from structural decisions (where state lives, what can replicate), not from tuning. [T2][S-0020]

## Details

Design process loop: requirements (FRs + quality requirements) → architecture
definition (candidate structures + style selection) → evaluation against quality
goals (tradeoff analysis, scenarios) → detailed design → construction — with
feedback from each step revising the earlier ones. The architecture description
(views + decisions + rationale) is the durable output of the architecture stage;
evaluation is what keeps the process honest.

## Boundaries / common misunderstandings

- "A diagram is the architecture": the architecture description — views, models, decisions, rationale — is a representation of the architecture, not the architecture itself; 42010 distinguishes the two. [T2][S-0021]
- "One view is enough": a single view cannot address all stakeholders' concerns; 42010's viewpoint/view/correspondence machinery exists precisely because multiple views are required. [T2][S-0021]
- "Evaluation tests functional correctness": ATAM evaluates quality attributes; functional correctness is established by verification and testing. [T3][S-0152]
- "Design is one upfront phase": requirements, architecture, and design iterate, and refinement continues as implementation and operation feed new information back. [T2][S-0017]
- "Scalability is a tuning problem": whether a system can scale follows from structural decisions made during architecture definition, so capacity must be evaluated as a requirement then, per 12207 architecture definition and ISO 25010's capacity subcharacteristic. [T2][S-0020][S-0019]

## References (evidence records)

- S-0017 SWEBOK v4.0 (Requirements/Architecture/Design KAs; iterative design) — T2
- S-0018 CS2023 (Software Engineering KA: architectural design competencies) — T2
- S-0019 ISO/IEC 25010:2023 (product quality characteristics; performance efficiency: time behaviour, resource utilization, capacity) — T2
- S-0020 ISO/IEC/IEEE 12207:2017 (technical processes: architecture definition, design definition; 2017 edition) — T2
- S-0021 ISO/IEC/IEEE 42010:2022 (architecture description: viewpoints, views, concerns, correspondences, frameworks) — T2
- S-0152 Kazman, Klein & Clements 2000, CMU/SEI-2000-TR-004 — ATAM — T3
- S-0153 Kruchten 1995, IEEE Software 12(6) — 4+1 view model — T3
- S-0154 Perry & Wolf 1992, SIGSOFT SEN 17(4) — architecture = {elements, form, rationale} — T3
