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

# Post-Quantum Cryptography — validation

## Formative (practice)

### Q1
- Q: What problem does Shor's algorithm solve, in what time, and on what kind of machine?
- bloom: remember
- bank: formative
- A: Integer factorization and discrete logarithms, in polynomial time on a quantum computer (polynomial quantum steps plus polynomial classical post-processing) — the two problems that RSA and Diffie-Hellman/elliptic-curve cryptography depend on.
- evidence: [S-0287]
- topic: frontiers/post-quantum-cryptography

### Q2
- Q: Why does Shor's algorithm threaten RSA but not symmetric encryption the same way? What is the structural difference?
- bloom: understand
- bank: formative
- A: RSA's security is a computational assumption about a specific number-theoretic problem (factoring) that Shor solves in polynomial time — the assumption itself collapses. Symmetric security is about key search, where quantum search gives only a quadratic speedup (Grover — UNVERIFIED as a record in this pack), so larger keys restore the margin. The asymmetry is structural: Shor kills the assumption; search speedup only changes the constant.
- evidence: [S-0287]
- topic: frontiers/post-quantum-cryptography

### Q3
- Q: Name the three NIST post-quantum standards published in August 2024 and the family of each.
- bloom: remember
- bank: formative
- A: FIPS 203 ML-KEM (from CRYSTALS-Kyber, lattice-based/MLWE) for key establishment; FIPS 204 ML-DSA (from CRYSTALS-Dilithium, lattice-based) for signatures; FIPS 205 SLH-DSA (from SPHINCS+, stateless hash-based) for signatures.
- evidence: [S-0288]
- topic: frontiers/post-quantum-cryptography

### Q4
- Q: What is MLWE, and why is it the security foundation of ML-KEM?
- bloom: understand
- bank: formative
- A: Module Learning with Errors: recovering a secret from noisy module-lattice equations. ML-KEM's security is related to its computational difficulty, and NIST judges the problem hard even for adversaries with a quantum computer. It replaces factoring/discrete logarithms as the assumption family for key establishment.
- evidence: [S-0288]
- topic: frontiers/post-quantum-cryptography

## Summative (mastery checkpoint)

### Q5
- Q: Explain harvest-now-decrypt-later and why it makes migration urgent specifically for confidentiality — and what it does NOT justify.
- bloom: understand
- bank: summative
- A: Adversaries record encrypted data today and decrypt it once a quantum computer exists; data with long confidentiality lifetimes (backups, health records, long-term secrets) is at risk now, so NIST treats HNDL as an urgency driver for encryption/key exchange and urges PQC or hybrid deployment as soon as practical. It does not by itself justify dropping signature-migration planning — signatures face a different, long-term forgery question.
- evidence: [S-0291]
- topic: frontiers/post-quantum-cryptography

### Q6
- Q: Prioritize migration for a system with: (a) TLS with RSA-2048 + ECDHE, (b) firmware signed with ECDSA, (c) 10-year encrypted backups wrapped with RSA, (d) short-lived session tokens. Order and justify.
- bloom: apply
- bank: summative
- A: (c) backups first — long-lived confidentiality is the prime HNDL target: move to ML-KEM key wrapping, hybrid initially. Then (a) TLS — bulk of traffic, adopt hybrid ECDHE + ML-KEM (the RFC 9794 practice). Then (b) firmware signatures — migrate to ML-DSA/SLH-DSA when the ecosystem supports it. (d) session tokens last — short-lived value cannot be harvested, but they must still be tracked for the 2030/2035 transition deadlines. Rationale: NIST IR 8547's urgency ordering is confidentiality first, with all quantum-vulnerable public-key algorithms facing the proposed deadlines.
- evidence: [S-0291][S-0288]
- topic: frontiers/post-quantum-cryptography

### Q7
- Q: A CISO says: "No quantum computer exists, so we can wait until 2030." Evaluate this using the transition report's own logic.
- bloom: evaluate
- bank: summative
- A: The premise is correct as of today (no cryptographically relevant quantum computer — UNVERIFIED as a cited claim here), but the conclusion ignores three things the report emphasizes: HNDL means the cost of waiting is incurred today by recording adversaries; migration is a multi-year engineering program (inventory, protocols, certificates, agility) that must start well before the deadlines; and hybrid deployments provide quantum protection without betting on the timeline. Verdict: the reasoning about the present is sound; the decision it supports is not.
- evidence: [S-0291]
- topic: frontiers/post-quantum-cryptography

### Q8
- Q: Compare classical, PQC, and hybrid key establishment for a TLS service along: threat model, performance/interoperability, migration risk.
- bloom: analyze
- bank: summative
- A: Classical (ECDHE): efficient and interoperable, but its confidentiality promise dies with a cryptographically relevant quantum computer — HNDL exposure. PQC (ML-KEM): quantum-resistant per NIST, but larger keys/ciphertexts (ML-KEM-768 public key ~1,184 bytes vs 32 for X25519 — verified sizes, no record here), newer implementation base, and a single-algorithm bet. Hybrid (ECDHE + ML-KEM): security if either component holds, negotiated with legacy peers, larger handshakes; NIST IR 8547 endorses hybrid for the transition. Migration risk is lowest with hybrid, which is why it is the de facto deployment pattern.
- evidence: [S-0291][S-0288]
- topic: frontiers/post-quantum-cryptography

## Review (spaced repetition — interleaved with prerequisites)

### Q9
- Q: RSA and ECC rely on which hardness assumptions, and which part of Shor's algorithm is the threat to each?
- bloom: understand
- bank: review
- A: RSA rests on integer factoring (public-key encryption RSA-OAEP; NIST-approved RSA key establishment); ECC and Diffie-Hellman rest on the discrete logarithm problem (ECDLP). Shor's period-finding algorithm solves both factoring and discrete logarithms in polynomial time — the same quantum core covers both — so the entire classical asymmetric assumption family falls together.
- evidence: [S-0233][S-0234][S-0287]
- topic: security/cryptography-basics

### Q10
- Q: Why is AES-256 considered safe against search-based attacks today, and how should you reason about its quantum status?
- bloom: apply
- bank: review
- A: Classically, exhaustive key search over 2^256 keys is infeasible. Quantum search (Grover) would reduce the search to ~2^128 — still infeasible, which is why symmetric schemes survive with margin (the Grover factor is UNVERIFIED as a record in this pack). The reasoning pattern is the same as in classical security analysis: estimate the best known attack under the assumed adversary model; for symmetric crypto the quantum model changes the constant, for public-key crypto it removes the assumption.
- evidence: [S-0234][S-0287]
- topic: security/cryptography-basics
