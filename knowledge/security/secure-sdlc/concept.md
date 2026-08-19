---
id: security/secure-sdlc
title: Secure SDLC
band: B5
track: security
tier: T2
bloom_target: apply
prerequisites: [security/threat-modeling, engineering-process/requirements-engineering]
related: [security/web-security, security/authentication-authorization, security/cryptography-basics]
recommended: []
status: draft
schema-version: 1
owner: l1-secure-sdlc
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0020, S-0252, S-0253, S-0254]
---

# Secure SDLC

## Claims

### Security in the lifecycle

- SWEBOK v4.0's Software Security knowledge area integrates security considerations throughout the software development lifecycle rather than treating security as a separate phase at the end. [T2][S-0017]
- ISO/IEC/IEEE 12207:2017 organizes the lifecycle into process groups — agreement, organizational project-enabling, technical management, and technical (requirements, implementation, verification, validation, operation, maintenance) — providing the process framework into which security activities are embedded; the standard does not itself supply the security practices. [T2][S-0020]
- The NIST Secure Software Development Framework (SSDF, SP 800-218 v1.1) organizes secure development into four practice groups — Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW), Respond to Vulnerabilities (RV) — whose outcome-based tasks can be integrated into any SDLC model. [T2][S-0252]

### Security requirements

- Security requirements are stated and verifiable requirements like any other (see `engineering-process/requirements-engineering`), but they are derived from adversarial analysis — threat models, abuse cases, compliance obligations — rather than from stakeholder needs alone. [T2][S-0017]
- SSDF's Prepare-the-Organization group opens with defining security requirements for development (PO.1), and v1.1 adds documenting them (PO.1.2) and tracking security requirements, risks, and design decisions (PW.1.2). [T2][S-0252]

### Threat-modeling integration

- Threat modeling is the design-time engine of a secure SDLC: SWEBOK places it among software security fundamentals, and SSDF's Produce group expects designs that meet security requirements and mitigate security risks before implementation. [T2][S-0017][S-0252]
- The threat model feeds downstream gates: OWASP SAMM's Requirements-driven Testing practice turns threats into misuse/abuse test cases, so design findings become testable obligations. [T3][S-0253]

### Secure coding practices

- OWASP SAMM places secure development across five business functions — Governance, Design, Implementation, Verification, Operations — with fifteen practices at maturity levels 0–3, making coding standards (Policy & Compliance), secure build, and defect management explicit, ratable activities rather than folklore. [T3][S-0253]

### Security testing

- SAMM's Security Testing practice pairs an automated baseline stream (tool-based scanning, integrated into build and deploy — the SAST/DAST families in OWASP terminology) with a manual deep-understanding stream (expert and penetration testing), because automation finds common weaknesses early while experts find what tools miss. [T3][S-0253]

### Security review gates

- SSDF's outcome-based practices act as lifecycle review gates: security requirements review, design/risk review, code review, and vulnerability testing of executable code are explicit checkpoints with auditable outcomes. [T2][S-0252]
- SAMM operationalizes gates as maturity levels — from ad-hoc activity (level 1) to "integrated into the build and deploy process" (level 3) — so a review gate is a defined, measurable activity, not a wall to pass. [T3][S-0253]

### Vulnerability management

- SSDF's Respond-to-Vulnerabilities group requires gathering and investigating credible reports, confirming them by analysis/testing, prioritizing remediation, and fixing and communicating — vulnerability management is an explicit lifecycle process, and its stated purpose includes reducing the impact of undetected or unaddressed vulnerabilities. [T2][S-0252]
- The CVE program (run by MITRE, sponsored by CISA) assigns shared identifiers — CVE records — through CVE Numbering Authorities (CNAs: vendors, open-source projects, coordination centers), giving the vulnerability-management ecosystem a common name for each disclosed issue. [T3][S-0254]
- A CVE record identifies and describes a disclosed vulnerability; remediation (fix, patch, advisory) is tracked separately by the affected parties — an identifier is not a fix. [T3][S-0254]

### Shift-left vs defense-in-depth

- "Shift-left" — moving security activities (requirements, threat modeling, static analysis) earlier in the lifecycle — is embodied by frameworks that span the whole cycle: SAMM's five business functions from governance to operations, and SSDF's four groups from pre-development preparation to post-release response. [T3][S-0253]
- Defense-in-depth complements shift-left: because even the best lifecycle leaves residual risk — SSDF's own terms: "undetected or unaddressed vulnerabilities" — programs add layered, independent controls so that exploiting any single flaw does not compromise the system. [T2][S-0252]

## Details

Secure SDLC pipeline: security requirements (adversarial derivation) → threat modeling at design (from `security/threat-modeling`) → secure coding standards + SAST in the build → code review and DAST/security testing before release → post-release response (CVE triage, coordinated disclosure, patching). SSDF provides the practice map (PO/PS/PW/RV), SAMM provides the maturity yardstick per practice, SWEBOK and ISO 12207 provide the lifecycle frame. The framework's own guidance is explicit that adoption is risk-based — cost, feasibility, and automatability weigh in — and that it is not a compliance checklist.

## Boundaries / common misunderstandings

- "Security is a phase at the end of development" — SWEBOK v4 integrates security throughout the lifecycle; a secure SDLC places requirements, design, implementation, verification, and response activities in every phase. [T2][S-0017]
- "A secure SDLC replaces threat modeling or security testing" — the SDLC is the host; threat modeling and testing are activities inside it (SAMM: 15 practices; SSDF: 4 groups). [T3][S-0253]
- "Running SAST/DAST scanners means we do security testing" — SAMM's Security Testing practice pairs automation with manual expert testing; scanners find known patterns, experts find business-logic flaws. [T3][S-0253]
- "SSDF/SAMM compliance makes software secure" — the frameworks are explicitly not checklists; they are outcome-based guides for reducing risk, and maturity assessment measures the process, not the product's assurance. [T2][S-0252]
- "A CVE ID means it is fixed" — the identifier marks a publicly disclosed vulnerability; remediation is a separate process that usually lags. [T3][S-0254]
- "Every security practice is worth adopting" — SSDF says to weigh cost, feasibility, applicability, and automatability when choosing practices; over-instrumenting adds complexity without proportional risk reduction. [T2][S-0252]

## References (evidence records)

- S-0017 — SWEBOK v4.0 (IEEE CS, 2024) — Software Security KA: security integrated throughout the lifecycle.
- S-0020 — ISO/IEC/IEEE 12207:2017 — lifecycle process groups (technical processes host security activities).
- S-0252 — NIST SP 800-218 v1.1 (2022) — SSDF: PO/PS/PW/RV groups, outcome-based tasks, risk-based adoption.
- S-0253 — OWASP SAMM v2 (2020) — 5 business functions, 15 practices, maturity levels; Security Testing practice.
- S-0254 — CVE Program (MITRE/CISA) — shared vulnerability identifiers via CNAs; record ≠ fix.
