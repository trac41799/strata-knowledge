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

# Cryptography Basics — validation

## Formative (practice)

### Q1
- Q: State the block size and the three key sizes of AES as specified by FIPS 197.
- bloom: remember
- bank: formative
- A: AES processes 128-bit blocks with 128, 192, or 256-bit keys (AES-128/192/256); the numeric suffix is the key length, the block size is always 128 bits.
- evidence: [S-0232]
- topic: security/cryptography-basics

### Q2
- Q: Why does encrypting a message not protect it against modification? What does a MAC or an AEAD mode add that encryption alone cannot?
- bloom: understand
- bank: formative
- A: Encryption provides confidentiality only: it hides content but an attacker can still flip bits or reorder blocks in the ciphertext, producing a different plaintext on decryption with no error. A MAC (or an AEAD mode such as GCM) adds a keyed authentication tag that makes any modification detectable; a tag mismatch means the data was changed or was not produced by a key holder, so it is rejected.
- evidence: [S-0233][S-0234]
- topic: security/cryptography-basics

### Q3
- Q: Your service must (a) encrypt bulk user data with integrity and authenticity protection, (b) distribute an initial secret to each client over an unauthenticated channel, and (c) detect accidental corruption of a public hash table. Pick the primitive class for each: symmetric AEAD, public-key exchange, or hash. Justify in one line each.
- bloom: apply
- bank: formative
- A: (a) Symmetric AEAD — AES-GCM gives confidentiality plus integrity/authenticity in one operation with a unique nonce per key. (b) Public-key key exchange — DH (with authentication added) lets client and server establish a shared secret without pre-shared material. (c) Hash — keyless one-way digests detect corruption; collision resistance makes deliberate forgery infeasible.
- evidence: [S-0232][S-0233][S-0234]
- topic: security/cryptography-basics

## Summative (mastery checkpoint)

### Q4
- Q: Alice and Bob use Diffie-Hellman with public group parameters p=23, g=5. Alice's private value is a=6, Bob's is b=15. Compute the public values exchanged and the shared secret both derive.
- bloom: apply
- bank: summative
- A: A = 5^6 mod 23 = 8; B = 5^15 mod 23 = 19. Alice computes 19^6 mod 23 = 2; Bob computes 8^15 mod 23 = 2. Shared secret = 2. This works because (g^a)^b = g^(ab) = (g^b)^a; an eavesdropper sees only 5, 23, 8, 19 and would need a discrete log (or CDH) to recover the secret — assumed hard in real-sized groups.
- evidence: [S-0233]
- topic: security/cryptography-basics

### Q5
- Q: A proposal uses a 128-bit digest hash "because 128 bits of entropy is enough for security." Analyze whether 128-bit output can provide 128-bit collision resistance, and if not, what output size is needed.
- bloom: analyze
- bank: summative
- A: No. By the birthday bound, a collision in an n-bit hash is expected after roughly 2^(n/2) evaluations: 2^64 work for 128 bits, far below 128-bit security. Collision resistance therefore needs an output of about twice the target security level — e.g., SHA-256 for 128-bit collision resistance. 128-bit outputs may suffice for other properties (e.g., preimage resistance) but not for collisions.
- evidence: [S-0233]
- topic: security/cryptography-basics

### Q6
- Q: A vendor argues: "Our cipher is unbreakable because the algorithm is secret, so we do not publish it." Evaluate this claim against Kerckhoffs's principle and the practice of public review.
- bloom: evaluate
- bank: summative
- A: The claim inverts Kerckhoffs's principle: a sound cryptosystem must remain secure when everything except the key is public. Security-by-secrecy of the algorithm fails completely if the algorithm leaks, and hidden algorithms never receive the public cryptanalytic review that finds design flaws; standardized, published algorithms are the basis for trusting a design. Secrecy of the key, not of the algorithm, is what provides security.
- evidence: [S-0233]
- topic: security/cryptography-basics

## Review (spaced repetition — interleaved with prerequisites)

### Q7
- Q: You receive ciphertext whose decryption produced gibberish. Can you conclude an attacker tampered with it if the system used (a) plain CBC encryption and (b) GCM? Why the difference?
- bloom: understand
- bank: review
- A: (a) No — CBC provides no integrity mechanism, so gibberish could be tampering, corruption, or a wrong key; you cannot distinguish modification from other causes. (b) Yes — GCM authenticates: a tag mismatch proves the ciphertext was modified or produced by an entity lacking the key, and the data must be rejected.
- evidence: [S-0234][S-0233]
- topic: security/cryptography-basics

### Q8
- Q: Classify the logical status of these two statements about Diffie-Hellman: "the shared secret is equal for both parties" and "an eavesdropper cannot recover the secret." For the second, is it a theorem, an assumption, or a conjecture? (Logic & proof interleave.)
- bloom: apply
- bank: review
- A: The first is a theorem of group algebra: (g^a)^b = g^(ab) = (g^b)^a, provable from the laws of exponentiation. The second is an assumption (the discrete-log/CDH hardness assumption): believed hard, not proven hard, and a proof or disproof would change the field. A security argument that treats the second as proven commits the fallacy of treating an unproven premise as established.
- evidence: [S-0044][S-0233]
- topic: cs-foundations/logic-and-proof

### Q9
- Q: An n-bit hash is evaluated n times per second. Using the birthday bound, estimate the number of hash outputs needed for a ~50% collision chance in a 64-bit hash, and compare the same estimate for a 256-bit hash. (Probability & statistics interleave.)
- bloom: apply
- bank: review
- A: Collision probability reaches ~50% after about 1.18 × 2^(n/2) outputs: ≈ 2^32 (≈4.3 billion) for a 64-bit hash — minutes at the given rate — versus ≈ 2^128 for a 256-bit hash, which is computationally infeasible. The n^2-style birthday scaling is why digest width must be twice the target security level.
- evidence: [S-0233]
- topic: cs-foundations/probability-statistics
