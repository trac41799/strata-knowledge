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
status: published
schema-version: 1
owner: l1-zero-knowledge-proofs
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0292, S-0293, S-0294, S-0233]
review_after: 2027-02-17
---

# Zero-Knowledge Proofs

## Claims

### Definition and formal properties

- A zero-knowledge (ZK) proof is an interactive protocol in which a prover convinces a verifier that a statement is true while revealing nothing beyond the statement's truth: Goldwasser, Micali and Rackoff formalized this as a protocol whose verifier-view can be simulated without the witness, i.e., "knowledge complexity" zero. [T0][S-0292]
- The three defining properties are completeness (an honest prover holding a valid witness convinces the honest verifier with overwhelming probability), soundness (no prover can convince the verifier of a false statement except with negligible probability), and zero-knowledge (the verifier's view is simulatable — it learns nothing it could not have computed alone). [T0][S-0292]
- The original ZK protocols proved membership in number-theoretic languages (e.g., quadratic residuosity) — the first "prove knowledge of a secret without revealing it" constructions. [T0][S-0292]

### Interactive vs non-interactive proofs

- The Fiat-Shamir transform converts a public-coin interactive proof into a non-interactive one by replacing the verifier's random challenges with a hash of the transcript (message and commitments) — the basis of practical identification, signatures, and later proof systems. [T0][S-0293]
- Fiat-Shamir's motivating application was identification: a user proves knowledge of a secret without transmitting it, proven secure against known/chosen-message attacks assuming factoring is hard, at a small fraction (as little as a quarter) of RSA's modular multiplications in typical implementations. [T0][S-0293]

### SNARKs and polynomial commitments

- A zk-SNARK is a succinct non-interactive argument of knowledge; PLONK (2019) constructed one with fully succinct verification and an updatable, universal structured reference string (SRS), removing the per-circuit trusted-setup obstacle that earlier pairing-based SNARKs carried. [T1][S-0294]
- PLONK-style systems express the computation as polynomials evaluated over a subgroup (Lagrange basis), commit to them with KZG-style polynomial commitments (constant-size group-element commitments), and verify with a few pairing equations independent of circuit size. [T1][S-0294]
- Proving dominates cost: PLONK's prover uses roughly 7.5-20x fewer group exponentiations than the fully-succinct mode of its predecessor Sonic (depending on circuit structure), while verification stays cheap and the proof stays constant-size. [T1][S-0294]

### Frontier status

- Proving-system design is a fast-moving frontier: PLONK (2019) is one point in an active sequence (circuit-specific pairing SNARKs -> universal/updatable SRS -> transparent hash-based systems -> recursive composition), and no single proving system is consensus as of 2026-08-18; current-state claims (exact production stacks, benchmark rankings) are UNVERIFIED in this pack. [T4][S-0294]

### ZK as a fundamental primitive

- Zero-knowledge is a standard primitive of modern cryptography, presented with formal definitions and security proofs in standard textbooks alongside encryption and signatures. [T3][S-0233]

## Details

Mental model: ZK = verifiability without disclosure. The prover holds a witness; the protocol proves a statement about it; zero-knowledge means the verifier's view is simulatable. Interactive proofs become non-interactive via Fiat-Shamir (hash the transcript). Modern proving systems (SNARKs/STARKs) arithmetize the computation, commit to the resulting polynomials (KZG-style for pairing-based systems), and produce short proofs with cheap verification at the price of heavy prover computation; the trust anchor moved from per-circuit ceremonies to universal, updatable SRSs.

## Boundaries / common misunderstandings

- "ZK proofs are encryption" — ZK proves properties about hidden data; it does not hide data by itself. Encryption hides content; ZK is about verifiability without disclosure, per GMR's knowledge-complexity definition. [T0][S-0292]
- "Soundness is absolute" — soundness is probabilistic: a cheating prover succeeds with negligible (not zero) probability; in non-interactive Fiat-Shamir proofs the analysis treats the hash as an unpredictable function (random-oracle style), and real-world instantiation failures are documented (see volatility notes — UNVERIFIED here). [T0][S-0293]
- "All SNARKs need a trusted setup" — pairing-based SNARKs use an SRS, but PLONK's is universal and updatable (no per-circuit ceremony); transparent, setup-free hash-based systems also exist (STARK-style — see volatility notes, UNVERIFIED here). [T1][S-0294]
- "Zero-knowledge means no information is transmitted" — information does flow (the transcript); zero-knowledge means the transcript yields nothing beyond the statement's truth (simulatability). [T0][S-0292]
- "ZK is too slow to be useful" — proving is expensive, but verification is fast and proofs are tiny; the asymmetry is the design point: prove once, verify everywhere. [T1][S-0294]

## Volatility notes

- Dated 2026-08-18; review at 2027-02-17 or earlier if a cited source shifts.
- STARKs: the foundational realization (Ben-Sasson, Bentov, Horesh & Riabzev 2018, IACR ePrint 2018/046 — web-verified: first transparent ZK-STARK, hash-based, with exponential verification speedup and post-quantum candidates) is NOT recorded in this pack — all STARK claims are UNVERIFIED here; add an S-record at next review.
- Groth16 (Groth 2016, EUROCRYPT, DOI 10.1007/978-3-662-49896-5_11 — web-verified: 3-element pairing-based proofs, per-circuit SRS) and the KZG commitment paper (Kate, Zaverucha & Goldberg 2010, ASIACRYPT, DOI 10.1007/978-3-642-17373-8_11 — web-verified) are verified documents but not recorded in this pack; claims beyond what PLONK supports are UNVERIFIED here.
- Fiat-Shamir failures: the transform is unsound for some protocols (attacks documented since Goldwasser & Kalai 2003) and deployed systems suffered real weak-Fiat-Shamir vulnerabilities — UNVERIFIED in this pack (no record yet).
- zk-rollups (web-verified as of 2026-08-18): production ZK rollups (zkSync Era, Starknet, Scroll, Polygon zkEVM, Linea) run centralized sequencers and permissioned prover networks; prover cost remains a real operating line item; privacy-preserving identity (selective-disclosure credentials) is an active, non-consensus area — all UNVERIFIED here (no record; practitioner sources: Alchemy ZK-rollup guide 2025; Eco ZK-rollup guide 2026).
- Proving-cost figures: only the relative figure stated in the PLONK paper (vs Sonic) is claimed here; absolute ms/byte numbers move with hardware and implementation and are NOT claimed.
- "ZK ≠ encryption" is a teaching frame; its formal content is GMR's knowledge-complexity definition [S-0292].

## References (evidence records)

- S-0292 — Goldwasser, Micali & Rackoff (1989), "The Knowledge Complexity of Interactive Proof Systems", SIAM J. Comput. 18(1):186-208, DOI 10.1137/0218012. Definition of ZK and its properties.
- S-0293 — Fiat & Shamir (1987), "How to Prove Yourself: Practical Solutions to Identification and Signature Problems", CRYPTO '86, LNCS 263:186-194, DOI 10.1007/3-540-47721-7_12. Fiat-Shamir transform; identification and signatures.
- S-0294 — Gabizon, Williamson & Ciobotaru (2019), "PLONK", IACR ePrint 2019/953. Universal updatable SRS; KZG polynomial commitments; prover cost.
- S-0233 — Katz & Lindell (2020), "Introduction to Modern Cryptography" 3rd ed. (reused additively from security/cryptography-basics).
