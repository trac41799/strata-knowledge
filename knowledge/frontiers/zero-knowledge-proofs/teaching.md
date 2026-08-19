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

# Zero-Knowledge Proofs — teaching

## Learning objectives (Bloom)

At the end of this topic the learner can (understand level; target = understand):

- State the formal definition of a zero-knowledge proof (GMR) and explain each of the three properties — completeness, soundness, zero-knowledge — in terms of what it protects.
- Explain the simulator criterion: "the verifier learns nothing" = the verifier's view can be produced without the witness.
- Describe the Fiat-Shamir transform: when it applies (public-coin protocols), what it replaces (verifier challenges with a hash of the transcript), and what it produces (non-interactive proofs/signatures).
- Explain at a high level how a modern SNARK works: arithmetization -> polynomials -> commitments -> evaluation proofs, and what the universal updatable SRS changed.
- Explain what ZK is NOT: not encryption, not absolute soundness, not a trust-free setup by default.
- Recognize which ZK claims are settled (formal theory, T0) vs volatile (proving-system landscape, applications — T4).

## Worked example

Worked example — the Fiat-Shamir identification protocol, traced step by step (the original "prove you know the secret without saying it").

Setup: the prover knows the factorization of n = 35 (= 5 x 7) and keeps a secret square root s = 4 of the public value v = s^2 mod 35 = 16. Anyone can know n and v; only the prover knows s.

Round (interactive):
1. Commit: prover picks random r = 11, sends x = r^2 mod 35 = 121 mod 35 = 16. (A random "blind" — it hides what the response will be.)
2. Challenge: verifier flips a coin, sends c = 1.
3. Response: prover sends y = r·s^c mod 35 = 11·4 = 44 ≡ 9 (mod 35).
4. Verify: check y^2 ≡ x·v^c (mod 35). Left: 9^2 = 81 ≡ 11. Right: 16·16 = 256 ≡ 11. Match -> verifier accepts.

Why sound: if the prover does not know s, answering c = 1 requires a square root of x·v; answering c = 0 requires a square root of x. One commitment x can satisfy only one of the two honestly, so a cheater is caught with probability 1/2 per round; k rounds -> (1/2)^k. (Repeat rounds to reach the required confidence.)

Why zero-knowledge: the simulator — who does NOT know s — picks c = 1 and y = 9 first, then sets x = y^2·v^-1 mod 35 = 81·11 mod 35 = 16 (v^-1 = 11 mod 35). The transcript (16, 1, 9) is distributionally identical to the real round above. Verifier learned nothing it could not simulate.

Non-interactive version (Fiat-Shamir): the challenge becomes c = H(x, m) — the hash of the commitment (and message m for signatures). One message, no interaction; security now rests on the hash behaving like an unpredictable function (see volatility notes for the caveat).

Contrast: the whole protocol transmits only numbers anyone could produce; the "secret" never leaves the prover. That is the essence of ZK.

## Elaboration prompts

- "In the trace, what exactly does the verifier gain that it did not have before the protocol? Re-derive the simulator to check."
- "Why must the commitment x be sent BEFORE the challenge c? What attack becomes possible if the prover could choose x after seeing c?"
- "Where does the random oracle enter the Fiat-Shamir story, and what breaks conceptually if the hash is not unpredictable?"
- "PLONK replaced per-circuit trusted setups with a universal updatable SRS. What does 'updatable' buy you in trust terms, and where does the trust move to instead?"
- "Why is the cost profile of ZK systems asymmetric (heavy prover, light verifier), and which real systems exploit exactly that asymmetry?"

## Common misconceptions

- "ZK proofs encrypt the answer." No — they prove a property of hidden data. The formal claim is about the verifier's knowledge (simulatable view), not about hiding a payload; encryption and ZK are complementary, not the same thing.
- "Soundness means it is impossible to cheat." Soundness is probabilistic: cheating is possible with negligible probability, which is tuned via rounds/security parameter. And in Fiat-Shamir form, soundness is only as good as the hash's unpredictability — real implementations have been broken (weak Fiat-Shamir).
- "A SNARK proof of X proves X is 'computationally checked'". A proof proves a statement about a computation (e.g., "this circuit was evaluated with this witness") — but the circuit itself encodes the claim, and bugs in arithmetization or the proving stack have produced unsound systems. The proof is only as good as the system that produces it.
- "Zero-knowledge requires no setup at all." Pairing-based SNARKs use an SRS; PLONK's is universal and updatable, but there is still a bootstrapping trust question — only transparent (hash-based) systems are setup-free, and they are a different (T4, UNVERIFIED-here) family.

## Feynman targets

- "Explain to a friend why showing you can open a locked box without revealing the key is a zero-knowledge proof — and what the verifier could still learn."
- "Explain 'the simulator' as: anything the verifier sees, a coin-flipping magician could have prepared backstage without the secret."
- "Explain Fiat-Shamir as: instead of the verifier choosing a challenge, the transcript itself chooses one, by hashing — like a quiz where the questions are generated from your own earlier answers."

## Interleaving hooks

- From security/cryptography-basics (prerequisite): ZK sits on the primitives you already know — hash functions (one-wayness/collision resistance underpin Fiat-Shamir and Merkle-style commitments), modular arithmetic/factoring (RSA hardness underlies the identification trace), and Kerckhoffs's principle (protocols are public; witnesses are secret). Re-derive the FS trace from those.
- From security/authentication-authorization: FS identification is the ancestor of challenge-response authentication — connect the c=0/1 challenge to challenge-response login protocols.
- Into frontiers practice: the "narrow scope + dated claims + re-review" discipline used here (formal core vs volatile landscape) is the same pattern used in the agentic-systems and post-quantum frontier packs.

## How to keep this current

- Re-review at review_after (2027-02-17) or earlier: verify (1) the proving-system landscape (SNARK vs STARK families, recursive proofs, new systems), (2) zk-rollup production state (prover networks, decentralization, benchmark numbers), (3) application areas (privacy-preserving identity standards, ZK in AI/verifiable ML), (4) known Fiat-Shamir/implementation vulnerabilities.
- Priority additions for next review (currently UNVERIFIED here, records needed): S-record for the STARK paper (ePrint 2018/046), S-record for Groth16 (DOI 10.1007/978-3-662-49896-5_11), S-record for KZG (DOI 10.1007/978-3-642-17373-8_11), and a record for a current zk-rollup survey.
- Process: propose changes as a PR (draft -> CI -> L2 review -> human gate); never silently rewrite published content.
