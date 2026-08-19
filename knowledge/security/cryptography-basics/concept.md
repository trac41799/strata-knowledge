---
id: security/cryptography-basics
title: Cryptography Basics
band: B2
track: security
tier: T2
bloom_target: apply
prerequisites: [cs-foundations/probability-statistics, cs-foundations/logic-and-proof]
related: [frontiers/post-quantum-cryptography, security/threat-modeling]
recommended: [security/authentication-authorization]
status: draft
schema-version: 1
owner: l1-cryptography-basics
reviewed-by: []
updated: 2026-08-18
sources: [S-0017, S-0019, S-0232, S-0233, S-0234]
---

# Cryptography Basics

## Claims

### Security goals and standards standing

- ISO/IEC 25010:2023 defines Security as a product quality characteristic whose subcharacteristics include Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity, and Resistance — the goals cryptographic mechanisms serve. [T2][S-0019]
- SWEBOK v4.0 treats security as a first-class, lifecycle-integrated software engineering concern via its new Software Security knowledge area. [T2][S-0017]

### Symmetric encryption (AES)

- AES is the NIST-approved symmetric block cipher: it processes 128-bit blocks with 128, 192, or 256-bit keys (FIPS 197; the 2023 update made no technical changes). [T2][S-0232]
- In symmetric encryption one shared secret key performs both encryption and decryption, and confidentiality depends entirely on keeping that key secret. [T3][S-0233]

### Asymmetric (public-key) cryptography

- Asymmetric cryptography gives each party a key pair — a public key and a private key — so two parties need not share one secret; it is orders of magnitude slower than symmetric encryption and in practice is used for key establishment and digital signatures, not bulk data. [T3][S-0233]
- RSA is a public-key scheme built on a trapdoor function from modular exponentiation; "textbook RSA" (direct exponentiation without padding) is not a secure encryption scheme, which is why RSA-OAEP (RFC 8017) applies randomized padding before encryption. [T3][S-0233]
- Elliptic-curve cryptography implements the same public-key primitives on elliptic-curve groups, achieving comparable security levels with much shorter keys than RSA. [T3][S-0233]
- The security of RSA and elliptic-curve cryptography rests on computational assumptions — integer factorization and the discrete-logarithm problem respectively — that are believed hard but not proven hard. [T3][S-0233]

### Hash functions (SHA-2/SHA-3)

- SHA-2 (FIPS 180-4) and SHA-3 (FIPS 202) are the NIST-approved hash function families; NIST guidance permits only approved algorithms for protecting sensitive information. [T2][S-0234]
- A cryptographic hash must satisfy collision resistance: it is computationally infeasible to find two distinct inputs with the same output. [T3][S-0233]
- Because of the birthday bound (a collision is expected after roughly 2^(n/2) evaluations of an n-bit hash), collision resistance requires an output at least twice the target security level — e.g., SHA-256 for 128-bit security. [T3][S-0233]

### MACs and HMAC

- HMAC (FIPS 198-1) is the NIST-approved keyed-hash message authentication code, and NIST guidance names HMAC among the approved message-authentication mechanisms. [T2][S-0234]
- A MAC is a secret-keyed checksum that provides both integrity (data not modified) and authenticity (data from a party sharing the key); encryption alone provides neither. [T3][S-0233]

### Key exchange (Diffie-Hellman)

- Diffie-Hellman key exchange works on an algebraic identity: in a group with generator g, (g^a)^b = g^(ab) = (g^b)^a, so two parties who exchange only public values g^a and g^b compute the same secret g^ab without transmitting it. [T3][S-0233]
- DH's security is an assumption, not a theorem: it presumes computing discrete logarithms (or the CDH problem) is hard; the algebra above is exact, but the adversary model is a computational assumption. [T3][S-0233]
- Plain Diffie-Hellman authenticates nobody: an active attacker can mount a man-in-the-middle attack, so in practice DH is combined with authentication (e.g., signatures or certificates). [T3][S-0233]

### Modes of operation (GCM)

- A block cipher encrypts only single fixed-size blocks; a mode of operation extends it to messages of arbitrary length, and NIST approves specific modes (SP 800-38A: ECB, CBC, CFB, OFB, CTR). [T2][S-0234]
- GCM (SP 800-38D) is the NIST-approved authenticated-encryption mode: one operation provides both confidentiality and integrity/authenticity (AEAD), using a unique IV/nonce per key. [T2][S-0234]

### Principles

- Kerckhoffs's principle (1883): a cryptosystem should remain secure when everything about it except the key is public knowledge — security must reside in the key, never in the secrecy of the algorithm. [T3][S-0233]
- Do not design your own cryptosystems: use standardized, widely reviewed algorithms and validated implementations; custom schemes almost always contain fatal flaws that publication and review would expose. [T3][S-0233]

## Details

Mode-of-operation trace (AES-128-GCM): with key K and unique nonce N, plaintext P (and optionally associated data AAD) produces ciphertext C plus an authentication tag T. The receiver recomputes the tag from K, N, C, and AAD; a mismatch means the ciphertext was modified or was not produced by a holder of the key, so it is rejected. Tag verification happens before any use of the decrypted data. GCM's security requires that N never be reused with the same K — NIST mandates unique nonces per key.

Key-exchange trace (Diffie-Hellman, small group p=23, g=5): Alice picks private a=6, sends A = 5^6 mod 23 = 8; Bob picks private b=15, sends B = 5^15 mod 23 = 19. Alice computes 19^6 mod 23 = 2; Bob computes 8^15 mod 23 = 2 — the shared secret. An eavesdropper sees only p, g, 8, 19, which are useless unless the discrete log (or CDH) is feasible in this group — which is why real systems use groups where it is believed hard.

Quantum threat pointer: a large-scale quantum computer running Shor's algorithm would break RSA and elliptic-curve cryptography (and DH), driving the ongoing transition to post-quantum algorithms. See `frontiers/post-quantum-cryptography` (T4, volatile — check its review date).

## Boundaries / common misunderstandings

- "Encryption provides confidentiality and that is enough" — encryption hides content but does not detect modification: ciphertext can be altered undetectably, so integrity/authenticity requires a MAC or an AEAD mode like GCM. [T3][S-0233]
- "A hash function is encryption" — hashes are one-way and keyless; nobody decrypts a hash. Hashes prove integrity of stored/transmitted data, never secrecy. [T3][S-0233]
- "Collision resistance means no two inputs can share an output" — it means finding such a pair is computationally infeasible, not impossible; the birthday bound quantifies the effort. [T3][S-0233]
- "Diffie-Hellman provides secure communication" — DH only establishes a shared secret; without authentication it is vulnerable to man-in-the-middle, and the secret alone encrypts nothing. [T3][S-0233]
- "Keeping the algorithm secret makes the system more secure" — this inverts Kerckhoffs's principle: public algorithms get public review, and security that relies on secrecy of the algorithm fails the moment the algorithm leaks. [T3][S-0233]
- "Longer keys always mean a more secure design" — key length is one parameter; a broken mode, reused nonce, or missing authentication defeats any key size. [T3][S-0233]

## References (evidence records)

- S-0017 — SWEBOK v4.0 (IEEE CS, 2024) — security as first-class lifecycle-integrated SE knowledge.
- S-0019 — ISO/IEC 25010:2023 — Security quality characteristic and subcharacteristics.
- S-0232 — NIST FIPS 197 (2001; 2023 editorial update) — AES symmetric block cipher.
- S-0233 — Katz & Lindell, Introduction to Modern Cryptography, 3rd ed. (2020) — RSA/OAEP, ECC, hashes and collision resistance, HMAC, DH, Kerckhoffs, practice rules.
- S-0234 — NIST SP 800-175B Rev. 1 (2020) — approved mechanisms: SHA-2/SHA-3, HMAC, modes (incl. GCM).
