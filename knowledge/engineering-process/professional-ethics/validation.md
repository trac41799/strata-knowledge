---
id: engineering-process/professional-ethics
title: Professional Ethics
band: B5
track: engineering-process
tier: T2
bloom_target: understand
prerequisites: []
related: []
recommended: []
status: published
schema-version: 1
owner: l1-professional-ethics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0078, S-0079, S-0080]
---

# Professional Ethics — validation

## Formative (practice)

- Q: Which body adopted a new Code of Ethics and Professional Conduct on June 22, 2018, and what are its four sections?
- bloom: remember
- bank: formative
- A: The ACM Council. Sections: 1 General Ethical Principles; 2 Professional Responsibilities; 3 Professional Leadership Principles; 4 Compliance with the Code.
- evidence: [S-0078]
- topic: engineering-process/professional-ethics

- Q: Explain the difference between confidentiality (ACM 1.7) and privacy (ACM 1.6).
- bloom: understand
- bank: formative
- A: Confidentiality protects information entrusted to you by others; privacy protects personal data about individuals. A system can respect privacy (not collecting personal data) yet leak confidential business data — the obligations are separate.
- evidence: [S-0078]
- topic: engineering-process/professional-ethics

- Q: What does IEEE tenet 1 require regarding public safety, and what must members disclose promptly?
- bloom: understand
- bank: formative
- A: Members must hold paramount the safety, health, and welfare of the public, strive for ethical design and sustainable development, protect the privacy of others, and disclose promptly factors that might endanger the public or the environment.
- evidence: [S-0079]
- topic: engineering-process/professional-ethics

- Q: Why is the Therac-25 considered a case about organizations and processes, not just software bugs?
- bloom: understand
- bank: formative
- A: The investigation found multiple contributing factors beyond the code defects: removal of hardware interlocks in favor of software-enforced safety, inadequate testing, failure to reproduce and properly report faults, initial blame of hardware and operators, and overconfidence in software safety.
- evidence: [S-0080]
- topic: engineering-process/professional-ethics

## Summative (mastery checkpoint)

- Q: A colleague proposes shipping a feature that can cause financial harm to users in edge cases, to meet a deadline. Map the obligations that apply under ACM Sections 1 and 2.
- bloom: understand
- bank: summative
- A: Section 1: avoid harm (1.2), be honest and trustworthy (1.3), contribute to society and human well-being (1.1). Section 2: strive for quality (2.1), give comprehensive evaluations including risk analysis (2.5), design robustly and securely (2.9), accept and provide professional review (2.4). Shipping known-harmful software conflicts with each of these.
- evidence: [S-0078]
- topic: engineering-process/professional-ethics

- Q: You are asked to add analytics that record users' browsing history "for internal insight" without telling users. Identify the code principles that apply and a responsible course of action.
- bloom: apply
- bank: summative
- A: ACM 1.6 (respect privacy), 1.3 (be honest and trustworthy), 1.1 (contribute to society/well-being), 2.5 (evaluate impacts including risks). Responsible action: disclose the data collection, obtain informed consent, minimize collection to what is needed, document the decision — and refuse or escalate if disclosure is impossible.
- evidence: [S-0078]
- topic: engineering-process/professional-ethics

- Q: A vendor offers your team a "success fee" to choose their library. Analyze the conflict-of-interest and reporting obligations that apply.
- bloom: analyze
- bank: summative
- A: IEEE tenet 3: avoid real or perceived conflicts of interest and disclose them to affected parties; tenet 4: reject bribery in all forms. ACM 2.3: know and respect existing rules; 1.3: be honest and trustworthy; 4.1: if a breach is recognized, take action to resolve it, including expressing concern. Declining the fee or disclosing it to management/procurement is the responsible course.
- evidence: [S-0079, S-0078]
- topic: engineering-process/professional-ethics

## Review (spaced repetition — interleaved with prerequisites)

- Q: ISO/IEC 25010:2023 lists Safety as a product quality characteristic. Why must safety requirements be specified and verified, and what professional duty does this imply?
- bloom: understand
- bank: review
- A: Safety (avoidance of harm) cannot be assumed from good intentions: it must be a stated, verifiable requirement. The duty to evaluate risks comprehensively (ACM 2.5) and hold public safety paramount (IEEE tenet 1) is what turns the quality characteristic into a professional obligation.
- evidence: [S-0019, S-0078]
- topic: quality-testing/quality-models

- Q: A safety requirement states "the machine shall not deliver more than the prescribed dose." Using the 29148 quality characteristics, explain what makes this requirement verifiable, and why verification matters for ethical responsibility.
- bloom: understand
- bank: review
- A: It is unambiguous and testable if the dose limit and measurement method are defined (e.g., "prescribed dose" bounded by an explicit number and a defined measurement procedure). The Therac-25 case shows what happens when such requirements and their verification are inadequate: harm to people. Verification is a professional duty, not a process nicety.
- evidence: [S-0073, S-0080]
- topic: engineering-process/requirements-engineering

- Q: ACM 2.9 requires designing systems that are robustly and usably secure, and IEEE tenet 1 requires protecting the public. How do these obligations align with building security into the SDLC rather than after the fact?
- bloom: analyze
- bank: review
- A: Security must be a first-class requirement from elicitation onward, because retrofitted security is both less robust and harder to verify — a system-level judgment the codes demand (evaluate systems and their impacts, avoid harm). Retrofitting after incidents repeats the Therac-25 pattern of safety as an afterthought.
- evidence: [S-0078, S-0079, S-0080]
- topic: security/secure-sdlc
