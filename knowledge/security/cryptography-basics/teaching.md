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
status: published
schema-version: 1
owner: l1-cryptography-basics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0017, S-0019, S-0232, S-0233, S-0234]
---

# Cryptography Basics — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: name AES's block and key sizes, the STRIDE-of-crypto primitives (symmetric, asymmetric, hash, MAC, key exchange, mode), and the NIST-approved families (AES; SHA-2/SHA-3; HMAC; GCM). [T2][S-0232][S-0234]
- **understand**: explain what each primitive provides and — crucially — what it does not (encryption ≠ authentication; DH ≠ authentication; hash ≠ encryption). [T3][S-0233]
- **apply**: given a security requirement, select the correct primitive or combination and trace its execution (mode-of-operation trace, DH exchange with concrete numbers). [T0][S-0233][S-0234] **bloom_target**
- **analyze**: diagnose flawed designs — missing MAC, nonce reuse, hash output too short, secrecy-of-algorithm thinking — against the claims in this pack. [T3][S-0233]

## Worked example — AES-128-GCM: the full lifecycle of one message

Setup: a client and server share a 128-bit key K. The client sends plaintext P = "TRANSFER 1000 USD" with associated data AAD = the header "req/42".

1. **Encrypt (sender).** The client picks a fresh nonce N (96 bits, typical for GCM). AES-CTR-style encryption under K with a counter derived from N turns P into ciphertext C. Simultaneously, GCM's GHASH polynomial authenticator — keyed by K — digests AAD and C into a 128-bit tag T. The client transmits (N, C, T) — N is not secret, only unique per K. [S-0234]
2. **Verify (receiver).** The server recomputes GHASH over the received AAD and C using K and N and compares the result to T. A mismatch → reject the message: it was modified in transit, or was not produced by a party holding K. Only if the tag verifies does the server decrypt C. [S-0234]
3. **Why this order and why GCM.** Verification before decryption closes padding-oracle-style channels; providing integrity and confidentiality in one mode removes the classic encrypt-without-authenticate failure. Reusing N with the same K breaks both confidentiality and forgery-resistance — which is why NIST requires unique nonces per key. [S-0234][S-0233]

Mini DH trace (same numbers as `concept.md` Details): p=23, g=5, a=6, b=15 → exchanged 8 and 19 → shared secret 2 on both sides. The lesson: the wire carries only public values; the algebra identity (g^a)^b = g^(ab) = (g^b)^a does the work, and the discrete-log assumption does the protecting. [S-0233]

## Elaboration prompts

- Why is "encrypt the data" an incomplete answer to "make the data secure"? Trace what an attacker can still do to AES-CBC ciphertext without the key. [T3][S-0233]
- GCM needs a unique nonce per key — what exactly breaks on nonce reuse, and why do "random enough" nonces still fail at scale? [T2][S-0234]
- If DH's security is only an assumption, why is it used everywhere anyway — and where does the assumption actually live (group choice, key size)? [T0][S-0233]
- Kerckhoffs's principle says the algorithm may be public — does that mean publishing an algorithm makes it secure? What does publication add beyond scrutiny? [T3][S-0233]
- Why does HMAC exist when we already have hashes? What does the key add that a bare SHA-256 digest cannot provide? [T2][S-0234][S-0233]

## Common misconceptions

1. **"Encryption = security."** Encryption gives confidentiality only. Without a MAC or AEAD, ciphertext can be modified undetected; without authenticated peers, it does not tell you who sent it. [T3][S-0233]
2. **"A hash is encryption you can't reverse."** Hashes are keyless, one-way integrity checks; they hide nothing and authenticate nothing. Password storage, checksums, and deduplication each use hashes differently. [T3][S-0233]
3. **"Diffie-Hellman secures the channel."** DH produces a shared secret — and nothing else. No authentication means man-in-the-middle; no encryption means the secret is not yet used for anything. [T3][S-0233]
4. **"128 bits of hash output is 128 bits of security."** For collision resistance the birthday bound halves the effective strength: 2^64 work. Output width must be ~2× the target level. [T3][S-0233]
5. **"Keeping the algorithm secret adds security."** Kerckhoffs's principle: security must reside in the key. Secret algorithms are un-reviewed and collapse when leaked. [T3][S-0233]
6. **"I can write my own AES."** "Don't roll your own crypto" covers both algorithm design and implementation: subtle side channels and parameter mistakes survive unit tests; use reviewed libraries and validated modules. [T3][S-0233]

## Feynman targets

Explain in plain language a non-engineer could follow:

- Why locking a letter in a box (encryption) is different from putting a tamper-evident seal on it (authentication), and why you usually need both.
- How two people who never shared a password can still agree on one in front of everyone (Diffie-Hellman) — and why the math is exact while the safety is only "we believe".
- Why "we keep the recipe secret" is a bad way to make an unbreakable safe, and why published recipes with public locks are the industry standard.

## Interleaving hooks

- **cs-foundations/logic-and-proof (prerequisite)**: distinguish theorems (the DH algebra identity) from assumptions (DLP hardness) — a proof-review reflex that applies to every security claim.
- **cs-foundations/probability-statistics (prerequisite)**: the birthday bound is pure probability; digest widths and key-entropy decisions are quantitative, not aesthetic.
- **security/authentication-authorization (next topic, recommended)**: authentication protocols (password hashing, challenge-response, TLS handshake) are where these primitives are composed — watch for the encrypt-vs-authenticate confusion reappearing there.
- **frontiers/post-quantum-cryptography (related, T4)**: Shor's algorithm threatens RSA/ECC/DH; the transition to lattice/hash-based schemes is why today's "approved" lists have expiry dates.
