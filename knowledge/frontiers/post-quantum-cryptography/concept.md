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

# Post-Quantum Cryptography

## Claims

### The quantum threat (settled foundation)

- Shor's algorithm solves integer factorization and discrete logarithms in polynomial time on a quantum computer (polynomial quantum steps plus polynomial classical post-processing); since RSA rests on factoring and Diffie-Hellman/elliptic-curve cryptography on discrete logarithms, a large-scale fault-tolerant quantum computer would break them. [T0][S-0287]
- The algorithm works by reducing both problems to period-finding, computed with the quantum Fourier transform — the same period-finding core covers factoring and the discrete logarithm problem, so the entire classical public-key assumption family (RSA, ECDH, ECDSA, DSA) falls together. [T0][S-0287]
- The mathematical result is settled (FOCS 1994, journal 1997), but the practical threat depends on hardware: the timeline for a cryptographically relevant quantum computer is the volatile part of this topic, not the algorithm itself. [T0][S-0287]

### NIST standardization (settled consensus)

- On August 13, 2024, NIST published the first finalized post-quantum standards: FIPS 203 (ML-KEM, derived from CRYSTALS-Kyber) for key establishment, and FIPS 204 (ML-DSA, derived from CRYSTALS-Dilithium) and FIPS 205 (SLH-DSA, derived from SPHINCS+) for digital signatures — concluding the standardization process begun with NIST's 2016 call for candidates. [T2][S-0288]
- ML-KEM is a key-encapsulation mechanism with three parameter sets (ML-KEM-512, ML-KEM-768, ML-KEM-1024); its security is related to the computational difficulty of the Module Learning with Errors (MLWE) problem, which NIST judges to be hard even against adversaries with a quantum computer. [T2][S-0288]
- The standardized lattice schemes therefore change the assumption family of public-key cryptography — from factoring/discrete logarithms to learning-with-errors variants — rather than removing assumptions entirely: like RSA's hardness, MLWE hardness is a belief, not a proof. [T2][S-0288]

### Migration: timeline, HNDL, hybrid (volatile, T4)

- NIST's transition report (IR 8547, initial public draft, November 2024) proposes deprecating RSA-2048 and ECC P-256 by 2030 and disallowing quantum-vulnerable public-key algorithms across NIST standards by 2035; as a draft, these dates are proposals that may change. [T4][S-0291]
- Harvest-now-decrypt-later (HNDL) is the urgency driver for confidentiality: adversaries can record encrypted data today and decrypt it once a quantum computer exists, so NIST urges deploying PQC or hybrid protection for long-lived data as soon as practical and accounting for HNDL when setting migration timelines. [T4][S-0291]
- Hybrid schemes — combining a classical and a PQC algorithm so that security holds if either component survives — are the endorsed transitional practice in NIST IR 8547 and the de facto migration pattern in real deployments, rather than a hard cutover to pure PQC. [T4][S-0291]
- Migration is an engineering program, not a flag flip: it spans algorithm inventory, protocol changes, certificates and key management, and algorithm agility, because PQC key sizes and performance differ materially from RSA/ECC. [T4][S-0291]

## Details

A useful mental model: PQC is mathematics-based cryptography that runs on ordinary classical hardware but is designed against adversaries with quantum computers — it changes the hardness assumptions, not the security definitions (IND-CCA for KEMs, existential unforgeability for signatures). The threat splits: Shor breaks public-key (asymmetric) schemes by destroying the factoring/DLP assumptions; symmetric schemes and hashes are only quadratically affected by quantum search, so they survive with adjusted margins — the Grover speedup claim is UNVERIFIED in this pack (no record yet). NIST PQC is not QKD (quantum key distribution, a physics-based key transport): the standardized FIPS algorithms are pure software/math. Size reality check (verified 2026-08, no record): ML-KEM-768 public keys are ~1,184 bytes versus 32 bytes for X25519, which is why TLS handshake sizes and protocol limits matter in deployment.

## Boundaries / common misunderstandings

- "Quantum computers will break all cryptography" — Shor's algorithm breaks factoring/DLP-based public-key crypto (RSA, ECC, DH); symmetric encryption and hashes are not broken the same way (only quadratic quantum search speedup — UNVERIFIED as a cited claim here), which is why the standardized PQC targets are key establishment and signatures. [T0][S-0287]
- "Post-quantum cryptography needs a quantum computer to run" — the standardized schemes run on ordinary classical hardware; only the adversary model is quantum. [T2][S-0288]
- "PQC algorithms are drop-in replacements for RSA/ECC" — key/ciphertext sizes and performance differ materially, so protocols, certificates, and system integration must change; NIST's own transition planning treats this as a phased migration. [T4][S-0291]
- "Only governments and defense need to migrate" — HNDL puts any long-lived confidentiality data (encrypted backups, health records, long-term secrets) at risk of record-now-decrypt-later collection, which is precisely the urgency framing of the NIST transition report. [T4][S-0291]
- "Quantum-safe means assumption-free" — MLWE-based security, like RSA's factoring-based security, rests on a computational assumption; NIST's "believed secure" is a judgment about hardness, not a mathematical proof of impossibility. [T2][S-0288]

## Volatility notes

- Dated 2026-08-18; review at 2027-02-17 or earlier if a cited source shifts.
- The NIST portfolio is still evolving: additional digital signature standardization continues (FN-DSA trajectory — status UNVERIFIED here), SP 800-227 "Recommendations for Key-Encapsulation Mechanisms" went final in September 2025 (verified), and IR 8545 status reports track further rounds; IR 8547 was still a draft as of mid-2026, so the 2030/2035 dates are proposals.
- Real-world hybrid deployment, verified 2026-08 (not yet records in this pack): Chrome 124 (April 2024) enabled hybrid post-quantum TLS by default and later migrated to the standardized X25519MLKEM768 group; Firefox 132 shipped the same group; Cloudflare's edge has supported hybrid KEMs since 2022; RFC 9794 (December 2024) standardizes concatenated hybrid KEMs for TLS 1.3; Apple iMessage deployed the PQ3 hybrid protocol (February 2024).
- Quantum hardware status is the main uncertainty: no cryptographically relevant quantum computer existed as of mid-2026 (UNVERIFIED here); arrival estimates vary widely and are not consensus — revisit at every review.
- Settled results without records in this pack, flagged for the next review: Regev (2005) worst-case-to-average-case reduction for LWE (the conservative-foundation argument) and Grover (1996) quadratic search speedup — UNVERIFIED as citations here.

## References (evidence records)

- S-0287 — Shor (1997) — polynomial-time quantum factoring and discrete logarithms, SIAM J. Computing 26(5).
- S-0288 — NIST (2024) — FIPS 203 ML-KEM standard (with FIPS 204/205 suite context).
- S-0291 — NIST (2024) — IR 8547 transition plan: timelines, HNDL urgency, hybrid endorsement.
