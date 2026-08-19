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

# Secure SDLC — validation

## Formative (practice)

### Q1
- Q: Name the four SSDF practice groups and give one concrete task from each.
- bloom: remember
- bank: formative
- A: Prepare the Organization (PO) — e.g., define security requirements for development (PO.1); Protect the Software (PS) — e.g., protect code from unauthorized access and tampering; Produce Well-Secured Software (PW) — e.g., review and analyze code, test executable code; Respond to Vulnerabilities (RV) — e.g., gather and investigate credible vulnerability reports, analyze and fix confirmed ones.
- evidence: [S-0252]
- topic: security/secure-sdlc

### Q2
- Q: A team plans to "do security after the beta release". Why does SWEBOK v4's framing make this a flawed plan, and what process does ISO 12207 provide instead?
- bloom: understand
- bank: formative
- A: SWEBOK v4's Software Security KA integrates security throughout the lifecycle — requirements, design, implementation, verification, response — so a post-release security pass can fix implementation bugs but not design-level threats. ISO 12207 provides the process framework (agreement, organizational, technical management, technical processes) into which security activities must be embedded at each point, since the standard itself supplies no security practices.
- evidence: [S-0017][S-0020]
- topic: security/secure-sdlc

### Q3
- Q: Your team is adding a file-upload feature (HTTPS in, object store out). Place at least four security activities into SSDF groups and SAMM business functions, and name the lifecycle phase each belongs to.
- bloom: apply
- bank: formative
- A: (1) Security requirements for the upload feature (e.g., size limits, content-type checks, per-user authorization) — SSDF PO.1, SAMM Design/Security Requirements — requirements phase. (2) Threat model of the upload flow (tampering, DoS, path traversal) — SSDF PW design tasks, SAMM Design/Threat Assessment — design phase. (3) SAST + code review of the upload handler in CI — SSDF PW (code review), SAMM Implementation/Secure Build — implementation phase. (4) DAST/pen-testing of the running endpoint before release — SAMM Verification/Security Testing, SSDF PW vulnerability testing — verification phase. (5) A CVE-triage path if a dependency in the upload path is disclosed — SSDF RV, SAMM Operations/Incident Management — operations phase.
- evidence: [S-0252][S-0253]
- topic: security/secure-sdlc

## Summative (mastery checkpoint)

### Q4
- Q: Given the SDLC stages requirements → design → build → test → release → operations, assign each activity to its stage and state the two biggest gaps for a team that "only runs SAST at release time": security requirements review; threat modeling; SAST; DAST; code review; CVE triage; incident runbook.
- bloom: apply
- bank: summative
- A: Security requirements review — requirements; threat modeling — design; SAST and code review — build (per change, in CI); DAST and penetration testing — test (and pre-release); CVE triage and incident runbook — operations (RV and SAMM Incident Management). Gaps: (1) no design-phase threat modeling means design-level threats (repudiation, business logic) are never examined; (2) release-time-only SAST gives no per-change feedback loop, so findings arrive after the design is baked in — the "shift-left" that SSDF/SAMM structure around is absent.
- evidence: [S-0252][S-0253]
- topic: security/secure-sdlc

### Q5
- Q: A payment service was built with full lifecycle security, yet a zero-day in a crypto library is exploited in production. Analyze how shift-left and defense-in-depth each address (or fail to address) this scenario.
- bloom: analyze
- bank: summative
- A: Shift-left reduced the number and severity of vulnerabilities introduced by the team's own code, but it cannot eliminate third-party or unknown (zero-day) flaws — that is residual risk. Defense-in-depth is the complementary layer: independent controls (network segmentation, least privilege, monitoring, WAF rules, runtime detection) mean the exploited library does not directly reach sensitive data. The lesson: shift-left optimizes what you build; defense-in-depth bounds the blast radius of what you cannot predict — SSDF's RV group exists precisely because "undetected or unaddressed vulnerabilities" remain.
- evidence: [S-0252]
- topic: security/secure-sdlc

### Q6
- Q: An AppSec lead reports: "We run SAST in CI, every finding gets a CVE ID, and our SAMM assessment is level 3 in Security Testing — the program is done." Evaluate this claim against SSDF/SAMM coverage.
- bloom: evaluate
- bank: summative
- A: The claim covers only part of the program: SAST-in-CI is one stream of one practice (SAMM Security Testing, stream A); CVE IDs are identifiers, not remediation, and issuing them does not fix or triage anything (SSDF RV is about analysis, prioritization, fixing, communicating). Missing: security requirements review (PO.1), threat modeling at design, code review, manual/deep testing, defect management, incident management, and the governance function (strategy, policy, training). A level-3 Security Testing practice with absent Design/Implementation practices is a lopsided program — SAMM assesses 15 practices, not one.
- evidence: [S-0253][S-0254]
- topic: security/secure-sdlc

## Review (spaced repetition — interleaved with prerequisites)

### Q7
- Q: A threat model found "information disclosure via credential sniffing on an unencrypted login flow". Which lifecycle activities (per SSDF) should consume this finding, and at which phase does the mitigation first appear? (Threat modeling interleave.)
- bloom: apply
- bank: review
- A: The finding becomes a security requirement (SSDF PO.1 — "login must use TLS"), a design obligation (PW design tasks — encryption of the flow), a test case (SAMM Requirements-driven Testing / misuse testing — "login without TLS must fail"), and a code-review focus area; the mitigation first appears at design time when the flow is specified, and is verified at build/test. One finding threads through requirements → design → test, which is why the threat model feeds the SDLC rather than sitting beside it.
- evidence: [S-0237][S-0252]
- topic: security/threat-modeling

### Q8
- Q: You must write a security requirement for "no SSRF from the file-import endpoint". State which 29148 characteristics make it a good requirement and how it differs from a functional requirement. (Requirements engineering interleave.)
- bloom: apply
- bank: review
- A: It must be unambiguous (single interpretation of what URLs are allowed), verifiable (a test or analysis can demonstrate it — e.g., deny-list/allow-list checks with a test case), implementation-free (state the constraint, not the library), and traceable to its source (the threat model). It differs from a functional requirement ("the endpoint accepts CSV files") because it constrains how a capability behaves under adversarial conditions rather than stating a capability itself — an NFR derived from analysis, per SWEBOK and 29148.
- evidence: [S-0073][S-0017]
- topic: engineering-process/requirements-engineering

### Q9
- Q: A dependency you ship is disclosed as CVE-2026-1234. What does the identifier tell you, what does it not tell you, and which SSDF activities now apply? (Vulnerability management.)
- bloom: analyze
- bank: review
- A: The CVE record tells you a public identifier and description of the vulnerability exist; it does not tell you whether your usage is affected, exploitability in your context, or how to fix it (that lives in vendor advisories/patches). SSDF RV applies: gather and investigate the report (RV.1), analyze/confirm impact in your product (RV.2), then fix, verify, and communicate (RV.3) — and if the root cause pattern recurs, feed it back into coding standards and review gates.
- evidence: [S-0254][S-0252]
- topic: security/secure-sdlc
