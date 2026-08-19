---
id: frontiers/zero-knowledge-proofs
title: Zero-Knowledge Proofs
band: B5
track: frontiers
tier: T4
bloom_target: understand
prerequisites: [security/cryptography-basics]
related: []
recommended: []
status: draft
schema-version: 1
owner: l1-zero-knowledge-proofs
reviewed-by: []
updated: 2026-08-18
sources: [S-0292, S-0293, S-0294, S-0233]
review_after: 2027-02-17
---

# Zero-Knowledge Proofs — validation

## Formative (practice)

### Q1
- Q: Name the three formal properties every zero-knowledge proof system must have, and state what each one protects against.
- bloom: remember
- bank: formative
- A: (1) Completeness — an honest prover with a valid witness convinces the honest verifier with overwhelming probability (protects the honest user from being rejected). (2) Soundness — no prover can convince the verifier of a false statement except with negligible probability (protects the verifier from lies). (3) Zero-knowledge — the verifier's view is simulatable without the witness, so it learns nothing beyond the statement's truth (protects the prover's secret).
- evidence: [S-0292]
- topic: frontiers/zero-knowledge-proofs

### Q2
- Q: In GMR's definition, what exactly does "zero-knowledge" mean, and what is the standard proof technique to demonstrate it?
- bloom: understand
- bank: formative
- A: It means the protocol's knowledge complexity is zero: there exists a simulator that, given only the statement (no witness), produces a transcript with the same distribution as real protocol transcripts — so whatever the verifier sees, it could have produced by itself. Demonstrating ZK = constructing/arguing such a simulator.
- evidence: [S-0292]
- topic: frontiers/zero-knowledge-proofs

### Q3
- Q: Why does the Fiat-Shamir transform require the interactive protocol to be public-coin (verifier only sends random challenges, no private coins)?
- bloom: understand
- bank: formative
- A: Because the transform replaces the verifier with a deterministic hash of the transcript — there is no private verifier state left to simulate. Only public-coin challenges can be reproduced by hashing the protocol so far; if the verifier used private coins, the hash could not stand in for them and the resulting non-interactive proof would not be sound.
- evidence: [S-0293]
- topic: frontiers/zero-knowledge-proofs

### Q4
- Q: What is a universal updatable SRS, and which obstacle of earlier SNARKs does it remove?
- bloom: remember
- bank: formative
- A: A structured reference string that is shared across all circuits (universal) and can be contributed to securely by many parties (updatable). It removes the per-circuit trusted setup: earlier pairing-based SNARKs needed a new (and ceremony-dependent) SRS for each circuit, which PLONK's universal updatable SRS eliminates.
- evidence: [S-0294]
- topic: frontiers/zero-knowledge-proofs

## Summative (mastery checkpoint)

### Q5
- Q: A colleague says "a ZK proof is just encryption of the answer". Where exactly does this mental model break, per the formal definition?
- bloom: understand
- bank: summative
- A: Encryption hides data but says nothing about it; ZK proves that a statement about hidden data holds, without disclosing the data (witness). The formal content is knowledge complexity zero: the verifier's view is simulatable, so it gains no knowledge beyond the statement's truth. A ciphertext is not a proof; a ZK transcript is not an encrypted message — the two are complementary primitives, and ZK can be built on top of encrypted/committed values.
- evidence: [S-0292]
- topic: frontiers/zero-knowledge-proofs

### Q6
- Q: Trace the Fiat-Shamir identification protocol for n=35, secret s=4, public v=s^2 mod n, prover random r=11. Show the commitment, one challenge c=1 and the response, and the verification check. Then explain how a simulator reproduces this transcript without s.
- bloom: apply
- bank: summative
- A: v = 16 (mod 35). Commit: x = r^2 mod 35 = 121 mod 35 = 16. Challenge c=1. Response: y = r·s^c = 11·4 = 44 ≡ 9 (mod 35). Verify: y^2 ≡ x·v^c (mod n) -> 9^2 = 81 ≡ 11, and x·v = 16·16 = 256 ≡ 11 (mod 35). Equal. Simulator: pick c=1 and y=9, set x = y^2·v^-1 mod 35 (v^-1 = 11, so x = 81·11 ≡ 16) — transcript (16, 1, 9), distributionally identical to the real one, without ever knowing s.
- evidence: [S-0293]
- topic: frontiers/zero-knowledge-proofs

### Q7
- Q: Soundness is probabilistic, not absolute. What does this imply for deploying a ZK protocol, and how does Fiat-Shamir change the soundness story in the non-interactive setting?
- bloom: understand
- bank: summative
- A: A malicious prover can cheat with some probability, so protocols repeat rounds (each round halves the cheating probability) or use a large enough security parameter to push the bound below negligible. In the non-interactive setting the challenge is derived from a hash of the transcript instead of a fresh verifier coin, so soundness rests on the hash behaving as an unpredictable (random-oracle-like) function — and known counterexamples show the transform is not sound for every protocol (see volatility notes).
- evidence: [S-0293]
- topic: frontiers/zero-knowledge-proofs

### Q8
- Q: Compare the trust model of a circuit-specific pairing-based SNARK (Groth16-style) with PLONK's universal updatable SRS. What deployment problem does the latter solve, and what remains the dominant cost?
- bloom: analyze
- bank: summative
- A: Circuit-specific: each new circuit needs its own trusted setup (ceremony); a broken setup breaks soundness for that circuit. PLONK: one universal, updatable SRS serves all circuits, and updates can be contributed by many parties so no single party must be trusted. Deployment consequence: setup becomes a one-time bootstrapping problem instead of per-circuit ceremonies. Dominant cost remains the prover: PLONK reported ~7.5-20x fewer group exponentiations than Sonic's fully-succinct mode, but proving still dwarfs the (cheap, constant-size) verification.
- evidence: [S-0294]
- topic: frontiers/zero-knowledge-proofs

## Review (spaced repetition — interleaved with prerequisites)

### Q9
- Q: From cryptography-basics: what are the two defining properties of cryptographic hash functions, and why does Fiat-Shamir's soundness depend on them?
- bloom: understand
- bank: review
- A: (1) One-wayness — given h(m), finding m is infeasible. (2) Collision resistance — finding m != m' with h(m)=h(m') is infeasible (per NIST-approved SHA-2/SHA-3 families). Fiat-Shamir replaces the verifier's random challenge with hash(transcript); a prover who could predict or influence the hash output could pre-commit x to pass a chosen challenge, so the transform's soundness is only as strong as the hash's unpredictability.
- evidence: [S-0234][S-0293]
- topic: security/cryptography-basics

### Q10
- Q: From cryptography-basics: in the Fiat-Shamir identification protocol, the prover's response y = r·s^c (mod n) requires a modular square root of v. Which number-theoretic assumption protects v = s^2 mod n, and what breaks if that assumption fails?
- bloom: apply
- bank: review
- A: The RSA/factoring hardness assumption: without knowing the factorization of n, extracting a square root of v mod n (finding s) is infeasible — so only the real prover can answer the c=1 challenge. If factoring n became easy, anyone could compute s, impersonate the prover, and the identification scheme would be worthless.
- evidence: [S-0233][S-0293]
- topic: security/cryptography-basics

### Q11
- Q: From cryptography-basics: Kerckhoffs's principle says security must not depend on the secrecy of the algorithm. Apply it to a ZK protocol: must the protocol itself (commitment, challenge, response rules) be kept secret?
- bloom: evaluate
- bank: review
- A: No. ZK security rests on the witness (a secret number, e.g., a factorization or discrete log), not on the protocol description. In fact the opposite holds: zero-knowledge is defined as the verifier's view being simulatable with the protocol fully public — a simulator knows every rule and still learns nothing. A "secret protocol" would violate the definition and, per Kerckhoffs's principle, would fail catastrophically on disclosure.
- evidence: [S-0233][S-0292]
- topic: security/cryptography-basics
