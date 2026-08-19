---
id: frontiers/post-quantum-cryptography
title: Post-Quantum Cryptography
band: B2
track: frontiers
tier: T4
bloom_target: understand
prerequisites: [security/cryptography-basics]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-post-quantum-cryptography
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0287, S-0288, S-0291]
review_after: 2027-02-17
---

# Post-Quantum Cryptography — teaching

## Learning objectives (Bloom)

At the end of this topic the learner can (understand level; target = understand):

- Explain what Shor's algorithm does, why it breaks RSA/ECC/DH, and why it does not break symmetric cryptography the same way.
- Describe the NIST PQC standards (FIPS 203/204/205), what ML-KEM is, and the role of the MLWE assumption family.
- Explain harvest-now-decrypt-later and why it drives confidentiality-migration urgency.
- Explain hybrid schemes and why they are the endorsed transitional practice.
- Judge migration claims ("we can wait until 2030") using the NIST transition report's logic, and identify what is settled vs volatile in the field.

## Worked example

Worked example — migrate an encrypted-backup service to post-quantum, reasoned step by step.

Goal: protect 10-year encrypted backups that are currently wrapped with RSA-2048.

1. Inventory and classify by HNDL exposure. Backups have a 10-year confidentiality lifetime; an adversary can record them today and decrypt them after a quantum computer arrives — prime harvest-now-decrypt-later exposure. Short-lived data (session keys) would not be in this class.
2. Choose the algorithm. The NIST-standardized key-encapsulation mechanism is ML-KEM (FIPS 203); for key wrapping of stored data, encapsulate a data-encryption key with ML-KEM and wrap the ciphertext with it (a KEM-DEM style construction). For the transition, use hybrid: wrap with both RSA (legacy read compatibility) and ML-KEM, so security holds if either survives — NIST IR 8547 endorses hybrid during the transition.
3. Handle the operational deltas. ML-KEM-768 public keys are ~1,184 bytes vs 32 for X25519 / ~256 for RSA-2048 — storage schema, key-management tooling, and backup-format fields must accommodate larger artifacts; new implementations need validation (FIPS 140-3-style) before production.
4. Schedule against the timeline. The NIST IR 8547 draft proposes disallowing quantum-vulnerable algorithms by 2035 and deprecating RSA-2048/ECC P-256 for new deployments by 2030 — plan the cutover so new backups are hybrid or PQC-only before 2030, and legacy-restore path retires before 2035.
5. Build in agility. Key the whole design to an algorithm identifier (like TLS cipher suites) so a future standard (e.g., the additional signature schemes in progress) can be adopted without re-architecting — crypto agility, per the transition report's approach.

Contrast: for firmware signatures (no HNDL exposure, but long-lived forgery risk), the same exercise points to ML-DSA/SLH-DSA, but with less urgency for the confidentiality reason — signatures are not harvestable the way ciphertext is.

## Elaboration prompts

- "Why does period-finding break both factoring and discrete logarithms — what is the shared structure?"
- "ML-KEM's security is 'believed', not proven: how is that different from RSA's status, and why does it matter for engineering decisions?"
- "Why is the 2035 date in IR 8547 a proposal, and what would change it?"
- "If a cryptographically relevant quantum computer were announced tomorrow, what would break immediately, and what would still work (and why)?"
- "Hybrid is endorsed for the transition — what would make a permanent hybrid strategy the wrong choice?"

## Common misconceptions

- "Post-quantum cryptography runs on quantum computers." The standardized FIPS algorithms are mathematics running on ordinary hardware; only the adversary model is quantum. PQC is also not QKD — different technology entirely.
- "A quantum computer breaks all cryptography." Shor breaks the factoring/DLP public-key family (RSA, ECC, DH); symmetric encryption and hashes only face a quadratic search speedup (Grover — UNVERIFIED as a record in this pack), so AES-256 and SHA-2/3 keep their margins.
- "PQC migration is a library swap." Key sizes, handshake sizes, certificate formats, and key-management workflows change materially; NIST's transition report treats migration as a phased engineering program with deadlines.
- "Only governments need to migrate." HNDL exposes any long-lived confidentiality data regardless of owner — the report's urgency framing applies to every organization with data worth harvesting.
- "Hybrid means twice the security." Hybrid gives security if at least one component holds (defense against breaking of either), not a doubled security level against an adversary who breaks neither; it is a transition-risk tool, not a strength multiplier.

## Feynman targets

- "Explain Shor's algorithm as: break the lock by finding the repeating pattern inside the number, then use the pattern to get the factors."
- "Explain HNDL as: the enemy is recording your vault conversations today, betting on a machine that can open the recordings later."
- "Explain hybrid as: belt and suspenders — the belt is the old lock, the suspenders are the new lock; if either breaks, you are still secure."
- "Explain the 2030/2035 proposal as: 'no new buildings with old locks after 2030; all old locks replaced by 2035' — with the caveat that it is still a draft."

## Interleaving hooks

- From security/cryptography-basics (prerequisite): the security definitions do not change — IND-CCA for KEMs, unforgeability for signatures — only the hardness assumptions (factoring/DLP -> MLWE) and the mechanism families do; re-derive the PQC story from the classical definitions.
- From security/cryptography-basics: the NIST mechanism-approval pattern (SP 800-175B surveying approved mechanisms) is the same pattern the FIPS 203/204/205 standards follow — standardization precedes adoption.
- Into frontiers practice: implementation bugs in new PQC code are a formal-verification problem (frontiers/formal-verification-scale): new, subtle math code is exactly where machine-checked correctness earns its keep.

## How to keep this current

- Re-review at review_after (2027-02-17) or earlier: verify (1) NIST IR 8547 final status and whether the 2030/2035 dates moved, (2) the additional signature scheme standardization (FN-DSA status), (3) new NIST guidance (e.g., SP 800-227 KEM recommendations, final Sept 2025), (4) real-world deployment milestones (hybrid TLS groups, Chrome/Firefox/Cloudflare/Apple — currently verified-but-unrecorded in this pack), (5) quantum hardware milestones (any cryptographically relevant quantum computer claims — currently UNVERIFIED here), (6) Regev/Grover records to add.
- Process: propose changes as a PR (draft -> CI -> L2 review -> human gate); never silently rewrite published content.
