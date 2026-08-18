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

# Professional Ethics

## Claims

### Codes of ethics

- The current ACM Code of Ethics and Professional Conduct was adopted by the ACM Council on June 22, 2018; it is structured as a preamble plus four sections — General Ethical Principles, Professional Responsibilities, Professional Leadership Principles, and Compliance with the Code. [T2][S-0078]
- The IEEE Code of Ethics (IEEE Policies §7.8, incorporating revisions through June 2020) commits members to ten tenets under three commitments: uphold the highest standards of integrity; treat all persons fairly and with respect; and strive to ensure the code is upheld by colleagues and co-workers. [T2][S-0079]
- SWEBOK v4 treats Professional Practice as a Knowledge Area, covering professionalism (accreditation, certification, licensing, ethics codes) and legal issues (patents, copyrights, trade secrets, liability, data privacy). [T2][S-0017]
- Both codes frame ethics as a personal commitment of members rather than a legal statute: ACM requires commitment to ethical conduct of every member, SIG member, and award recipient, and IEEE members "commit ourselves to the highest ethical and professional conduct." [T2][S-0078][S-0079]

### Core obligations

- ACM Section 1 (general ethical principles) obliges computing professionals to contribute to society and human well-being, avoid harm, be honest and trustworthy, be fair and not discriminate, respect the work behind new ideas and creative works, respect privacy, and honor confidentiality. [T2][S-0078]
- ACM Section 2 (professional responsibilities) obliges professionals to strive for quality in processes and products, maintain competence, know and respect rules, accept and provide professional review, evaluate systems comprehensively including risk analysis, perform work only in areas of competence, and design systems that are robustly and usably secure. [T2][S-0078]
- ACM Section 3 (leadership principles) requires that the public good be the central concern of professional computing work, and calls on leaders to articulate social responsibilities and take special care with systems integrated into society's infrastructure. [T2][S-0078]
- IEEE tenet 1 requires members to hold paramount the safety, health, and welfare of the public, to strive for ethical design and sustainable development, to protect the privacy of others, and to disclose promptly factors that might endanger the public or the environment. [T2][S-0079]
- IEEE tenets also require: avoiding and disclosing real or perceived conflicts of interest (tenet 3); rejecting bribery and unlawful conduct (tenet 4); honest claims and estimates with proper credit to others' contributions (tenet 5); and maintaining technical competence, undertaking tasks only when qualified or after disclosing limitations (tenet 6). [T2][S-0079]
- Confidentiality and privacy are distinct obligations: ACM 1.7 protects entrusted information (confidentiality), ACM 1.6 protects personal data (privacy), and IEEE tenet 1 requires protecting the privacy of others. [T2][S-0078][S-0079]
- Intellectual property obligations are explicit in the codes: ACM 1.5 requires respect for the work required to produce new ideas, inventions, creative works, and computing artifacts; SWEBOK's Professional Practice KA covers patents, copyrights, trade secrets, and liability. [T2][S-0078][S-0017]

### Safety-critical responsibility

- ISO/IEC 25010:2023 defines Safety as a product quality characteristic (avoidance of harm to people and the environment); engineers of safety-critical software therefore have a corresponding professional duty to analyze, specify, and disclose risks (ACM 2.5 comprehensive evaluation including risk analysis; IEEE tenet 1). [T2][S-0019][S-0078][S-0079]
- The Therac-25 (1985–1987) is the canonical safety-critical case: a radiation therapy machine massively overdosed patients at least six times, causing severe injury or death, primarily because of software errors combined with the manufacturer's failure to follow proper software engineering practices. [T3][S-0080]
- The Therac-25's predecessor (Therac-20) retained independent protective circuits and mechanical interlocks, while the Therac-25 placed more safety responsibility on software — replacing hardware safety mechanisms with software control was a central factor in the accidents. [T3][S-0080]
- The Leveson & Turner (1993) investigation found organizational factors — failure to reproduce faults, initial blame of hardware and operators, inadequate testing — contributed as much as the code defects themselves; overconfidence in software safety was an important factor. [T3][S-0080]

### Whistleblowing and compliance

- ACM Section 4 obliges professionals who recognize breaches of the Code to take action to resolve the ethical issue, including, when reasonable, expressing concern to the person(s) thought to be violating the Code; violations are treated as inconsistent with ACM membership. [T2][S-0078]
- The IEEE code explicitly prohibits retaliation against individuals reporting a violation and requires supporting colleagues in following the code (tenet 10). [T2][S-0079]

## Details

Codes are decision aids, not checklists: identify the facts, the affected
stakeholders, the applicable principles (ACM sections 1–3; IEEE tenets),
then weigh and act, then review. Cases like Therac-25 show that ethical
responsibility is systemic — requirements, verification, organizational
culture, and reporting channels all carry it. When in doubt about a
provision's current wording, consult the live code text (both codes are
revisioned; ACM 2018, IEEE 2020).

## Boundaries / common misunderstandings

- Ethics codes are not laws, and enforcement is limited to membership consequences (ACM: violations inconsistent with membership) — they guide professional judgment and complement, rather than replace, legal and organizational requirements. [T2][S-0078]
- "I just write code" does not shrink responsibility: ACM 2.5 requires comprehensive evaluation of systems and their impacts, including risk analysis, for all who build them. [T2][S-0078]
- Following a manager's instruction does not settle an ethical question: the codes bind the individual professional (ACM 2.5, 3.1) to evaluate impacts and keep the public good central. [T2][S-0078]
- The Therac-25 is not a story about incompetent engineers: it is a system-level failure (requirements, design, verification, organization, regulation) — which is exactly why individual diligence alone cannot guarantee safety. [T3][S-0080]
- Confidentiality is not the same as privacy, and neither is the same as security: the obligations target entrusted information, personal data, and system robustness respectively (ACM 1.6, 1.7, 2.9). [T2][S-0078]
- Codes change: the ACM code was rewritten in 2018 and the IEEE code last revised in 2020 — always check the current version before citing a clause. [T2][S-0078][S-0079]

## References (evidence records)

- S-0017 — SWEBOK v4.0 (IEEE CS, 2024) — Professional Practice KA (professionalism, legal issues).
- S-0019 — ISO/IEC 25010:2023 — Safety as a product quality characteristic.
- S-0078 — ACM Code of Ethics and Professional Conduct (2018).
- S-0079 — IEEE Code of Ethics (rev. 2020).
- S-0080 — Leveson & Turner (1993) — An Investigation of the Therac-25 Accidents.
