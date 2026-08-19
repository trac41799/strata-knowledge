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
status: published
schema-version: 1
owner: l1-secure-sdlc
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0020, S-0252, S-0253, S-0254]
---

# Secure SDLC — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: name the four SSDF groups (PO/PS/PW/RV), SAMM's five business functions, and the role of CVE records and CNAs. [T2][S-0252][S-0253][S-0254]
- **understand**: explain why SWEBOK v4 integrates security throughout the lifecycle and what ISO 12207's process framework provides. [T2][S-0017][S-0020]
- **apply**: map security activities (requirements, threat modeling, SAST/DAST, code review, CVE triage) to lifecycle phases and SSDF/SAMM practices; identify gaps in a team's SDLC. [T2][S-0252][S-0253] **bloom_target**
- **analyze**: compare shift-left with defense-in-depth and SAMM with SSDF as frameworks; reason about residual risk. [T2][S-0252]
- **evaluate**: judge an AppSec program claim against full SSDF/SAMM coverage rather than single practices. [T2][S-0253]

## Worked example — SSDF mapping exercise for an e-commerce API

Setup: "ShopAPI" — team of 6, quarterly releases, one shared staging environment, tickets, no CI security steps. Feature: checkout with payment-card tokenization.

1. **List current activities.** Requirements: "card data must not be stored". Build: code review by one senior dev. Test: unit tests only. Ops: on-call, no incident process.
2. **Map each to SSDF and SAMM.**
   - "Card data must not be stored" → security requirement, SSDF PO.1; SAMM Design/Security Requirements. Gap: it is the only security requirement — no threat model, no abuse cases.
   - Senior-dev code review → SSDF PW code review; SAMM Implementation. Gap: informal, no checklist from threat model, not gated.
   - Unit tests only → SSDF PW vulnerability testing absent; SAMM Verification/Requirements-driven Testing absent — no misuse tests, no DAST.
   - On-call → SSDF RV absent; SAMM Operations/Incident Management absent — no CVE triage path.
3. **Pick the next three moves (risk-based, per SSDF's own guidance).** (a) Write security requirements for checkout from a 30-minute threat model of the payment flow (cheapest, unblocks everything). (b) Add SAST on every PR + a DAST run before release (automates the common weaknesses). (c) Stand up a minimal RV process: subscribe to dependency advisories, triage, patch, communicate. Defer full SAMM level-3 instrumentation until the baseline holds.
4. **Check the gates.** After the change: requirements reviewed against the threat model at design; code review checks the threat-model checklist; SAST/DAST results are release gates; vulnerabilities have an owner and a fix deadline. [S-0252][S-0253]

## Elaboration prompts

- SSDF is explicitly "not a checklist" — what does an outcome-based practice give you that a checklist does not, and what discipline does it demand instead? [T2][S-0252]
- SWEBOK integrates security across the lifecycle; ISO 12207 supplies process groups without security practices. Where exactly does each framework stop, and why do you need both? [T2][S-0017][S-0020]
- SAMM's Security Testing practice pairs automation with manual deep testing. What kinds of flaws would a mature automated baseline still miss, and why are those exactly the ones experts must chase? [T3][S-0253]
- A CVE record "identifies, not fixes". If identifiers are cheap and fixes are expensive, what should a team's vulnerability-management dashboard actually track? [T3][S-0254]
- Shift-left reduces defects; defense-in-depth bounds impact. In which scenarios does each fail alone, and what does SSDF's RV group imply about the failure mode of shift-left? [T2][S-0252]

## Common misconceptions

1. **"Security is a phase at the end."** SWEBOK v4 integrates security throughout the lifecycle; end-of-cycle testing only finds implementation bugs, never design-level threats. [T2][S-0017]
2. **"The secure SDLC replaces threat modeling / testing."** It hosts them: SSDF's four groups and SAMM's five functions are activities *inside* the lifecycle. [T3][S-0253]
3. **"Scanners = security testing."** SAST/DAST find known patterns; SAMM's Security Testing practice explicitly adds manual expert and penetration testing for what tools miss. [T3][S-0253]
4. **"Compliance with SSDF/SAMM = secure product."** Both are risk-reduction guides, explicitly not checklists; maturity measures the process, not the assurance of any particular release. [T2][S-0252]
5. **"CVE ID = fixed."** It is a public identifier for a disclosed vulnerability; remediation happens in separate vendor processes. [T3][S-0254]

## Feynman targets

Explain in plain language a non-engineer could follow:

- Why you check the plumbing of a building *while* it is being designed, not only when the tenants move in — and why a separate "security team at the end" is like hiring an inspector who only visits after move-in day.
- Why a scan of the code and a scan of the running site are two different checks (like checking the recipe vs tasting the cake), and why a human taster is still needed.
- Why "we know the bug's public name (CVE)" is not the same as "the bug is fixed" — like knowing the street name of a pothole versus having it repaired.

## Interleaving hooks

- **security/threat-modeling (prerequisite)**: the threat model is the input that generates security requirements, design obligations, and misuse test cases — the secure SDLC is how a threat model becomes code and gates.
- **engineering-process/requirements-engineering (prerequisite)**: security requirements must satisfy the same quality criteria (unambiguous, verifiable, traceable) as any requirement — adversarial derivation does not exempt them.
- **security/web-security and security/authentication-authorization (related)**: implementation-level weaknesses (injection, broken auth) are the usual findings of the SAST/DAST gates and code reviews this topic schedules.
- **quality-testing/code-review (related)**: review gates in the secure SDLC reuse code-review practice, extended with threat-model-derived checklists.
