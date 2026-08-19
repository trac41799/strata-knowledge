---
id: security/threat-modeling
title: Threat Modeling
band: B5
track: security
tier: T2
bloom_target: apply
prerequisites: [architecture-design/architectural-styles, systems-software/networking-basics]
related: [security/cryptography-basics, security/web-security]
recommended: [security/secure-sdlc]
status: published
schema-version: 1
owner: l1-threat-modeling
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0237, S-0238, S-0239]
---

# Threat Modeling

## Claims

### Purpose and standing

- SWEBOK v4.0's Software Security knowledge area covers threat modeling among security fundamentals and integrates security considerations throughout the software development lifecycle rather than treating security as an afterthought. [T2][S-0017]
- ISO/IEC 25010:2023 defines the security goals a threat model protects: Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity (and Resistance) as subcharacteristics of the Security quality characteristic. [T2][S-0019]
- Threat modeling is a structured technique for identifying and enumerating the threats a system design is exposed to, as the first step of proactive security analysis — before implementation, so that mitigations are designed in rather than bolted on. [T3][S-0237]
- Threat, vulnerability, and attack are distinct: a threat is a potential occurrence with an undesirable effect on system resources, a vulnerability is a characteristic that makes a threat possible, and an attack is an action that exploits vulnerabilities to enact a threat. [T3][S-0237]

### STRIDE

- STRIDE (Kohnfelder & Garg, 1999) classifies threats into six categories: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, and Elevation of privilege. [T3][S-0237]
- Each STRIDE category maps to the security property it violates: Spoofing→Authentication, Tampering→Integrity, Repudiation→Non-repudiation, Information disclosure→Confidentiality, Denial of service→Availability, Elevation of privilege→Authorization. [T3][S-0237]
- STRIDE is applied against a model of the design during the design phase: threats are identified based on the design of the product, which makes enumeration systematic instead of ad hoc brainstorming. [T3][S-0237]
- A system is only as secure as its weakest link: sophisticated multi-step attacks chain small compromises, so threat analysis focuses on finding and improving the weakest links. [T3][S-0237]

### Attack trees

- An attack tree (Schneier, 1999) models an attack goal as the tree root and decomposes it into sub-goals: OR nodes are alternative ways to reach the parent goal, AND nodes are steps that must all be taken; leaves are concrete attacker actions. [T3][S-0238]
- Attack trees support quantitative reasoning: assigning values such as cost, skill, or probability to leaf nodes lets analysts compute the cheapest or most likely path to the root goal and compare mitigations. [T3][S-0238]

### Risk and decision-making

- Threat analysis includes deciding which threats to address: threats that are not mitigated must at minimum be identified and explicitly rationalized rather than ignored. [T3][S-0237]

### The model as a living artifact

- Because security is integrated throughout the lifecycle (SWEBOK v4.0), a threat model is a living artifact: it is created at design time and re-examined whenever the design, deployment, or adversary landscape changes — not a one-time diagram. [T2][S-0017]

### MITRE ATT&CK

- MITRE ATT&CK is a globally accessible knowledge base of adversary tactics and techniques based on real-world observations, organized as a matrix (e.g., the Enterprise matrix: 14 tactics from Reconnaissance to Impact). [T3][S-0239]
- ATT&CK complements design-centric methods such as STRIDE: it grounds threat enumeration in observed adversary behavior, supporting detection coverage analysis, red-team planning, and defensive control selection. [T3][S-0239]

## Details

Data flow diagram (DFD) practice — the working vehicle for STRIDE-style analysis: the system is drawn as external entities, processes, data stores, and data flows, with trust boundaries drawn wherever the trust level changes (e.g., around the server tier, or where data enters from the Internet). Each element is then examined for each applicable STRIDE category ("STRIDE per element"), and each identified threat is assessed for whether it can realistically occur and how damaging it would be (likelihood × impact), with mitigations chosen for the high-risk ones and the rest explicitly accepted or documented.

Relationship to other disciplines: threat modeling sits between architecture (the DFD is a data-flow view of the architecture — see `architecture-design/architectural-styles`) and security testing (threats become test cases and security requirements — see `security/secure-sdlc`).

## Boundaries / common misunderstandings

- "Threat modeling is a one-time diagram drawn at kickoff" — the model is a living artifact; it must be re-examined as the design, deployment, and threat landscape evolve, because mitigations only protect the design they were derived from. [T2][S-0017]
- "A vulnerability scanner or pentest replaces threat modeling" — scanners and pentests find implementation weaknesses in existing code; threat modeling finds design-level threats before code exists, which is why it is positioned at the design phase. [T3][S-0237]
- "More mitigations is always better" — every mitigation has a cost and can add attack surface; the model exists to rank threats by risk so effort goes where it matters and the rest is rationalized. [T3][S-0237]
- "Threat modeling is only about hackers" — STRIDE's repudiation and tampering categories cover insiders and accidental causes too; a threat is "any potential occurrence, malicious or otherwise, that can have an undesirable effect". [T3][S-0237]
- "STRIDE and ATT&CK are the same thing" — STRIDE is a design-time taxonomy of what can go wrong in a proposed design; ATT&CK is an observation-based catalog of how real adversaries operate. They complement, not replace, each other. [T3][S-0237][S-0239]

## References (evidence records)

- S-0017 — SWEBOK v4.0 (IEEE CS, 2024) — Software Security KA: threat modeling among security fundamentals; lifecycle integration.
- S-0019 — ISO/IEC 25010:2023 — Security quality characteristic and subcharacteristics.
- S-0237 — Kohnfelder & Garg (1999), "The Threats to Our Products" — STRIDE model, definitions, design-phase process.
- S-0238 — Schneier (1999), "Attack Trees" (Dr. Dobb's Journal) — AND/OR attack tree modeling and analysis.
- S-0239 — MITRE ATT&CK — adversary tactics/techniques knowledge base.
