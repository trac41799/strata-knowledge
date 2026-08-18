---
id: cs-foundations/discrete-mathematics
title: Discrete Mathematics
band: B3
track: cs-foundations
tier: T0
bloom_target: apply
prerequisites: [cs-foundations/logic-and-proof]
related: [cs-foundations/logic-and-proof]
recommended: []
status: published
schema-version: 1
owner: l1-discrete-mathematics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0048, S-0049, S-0045]
---

# Discrete Mathematics — validation

Item anatomy: `Q` · `bloom` · `bank` · `A` · `evidence` · `topic`.

## Formative (practice)

### F1. Equivalence relation check
- Q: The relation R on integers defined by aRb iff a − b is divisible by 3: is R reflexive, symmetric, transitive? What does that make R, and what are its classes?
- bloom: remember
- bank: formative
- A: R is reflexive (a − a = 0 is divisible by 3), symmetric (if 3 | (a − b) then 3 | (b − a)), and transitive (if 3 | (a − b) and 3 | (b − c) then 3 | (a − c)). R is an equivalence relation; its classes are the residue classes 0, 1, 2 mod 3 — this is the congruence relation a ≡ b (mod 3).
- evidence: [S-0048]
- topic: cs-foundations/discrete-mathematics

### F2. Pigeonhole computation
- Q: 366 students take an exam; each is assigned one of 12 grade levels. What does the pigeonhole principle force about grade levels, and what is the exact bound?
- bloom: apply
- bank: formative
- A: 366 objects into 12 boxes forces some box to hold at least ⌈366/12⌉ = ⌈30.5⌉ = 31 students — at least 31 students share a grade level. The principle guarantees existence of the crowded box but does not identify it.
- evidence: [S-0049]
- topic: cs-foundations/discrete-mathematics

### F3. Counting choices
- Q: A password is 4 distinct lowercase letters followed by one digit. Count the number of passwords. Which rule(s) did you use?
- bloom: apply
- bank: formative
- A: P(26, 4) = 26·25·24·23 = 358,800 letter arrangements, times 10 digits, by the product rule: 3,588,000 passwords. Counting ordered choices of distinct objects uses permutations; independent later choices multiply.
- evidence: [S-0048]
- topic: cs-foundations/discrete-mathematics

### F4. Induction gap
- Q: A classmate "proves" 2^n ≥ n² for all n ≥ 1 by checking n = 1, 2, 3, 4 and declaring it true. What is the flaw, and what would a correct inductive proof need?
- bloom: analyze
- bank: formative
- A: Checking finitely many cases is not a proof: induction requires (1) a base case and (2) a proof that P(k) → P(k + 1) for arbitrary k, so the property is inherited indefinitely. Note also the claim is false for n = 3 (8 < 9) — a good demonstration that examples cannot certify claims.
- evidence: [S-0045]
- topic: cs-foundations/discrete-mathematics

## Summative (mastery checkpoint)

### S1. Functions by relation properties
- Q: A relation R ⊆ A × B with |A| = 5, |B| = 7 is a function f: A → B. How many distinct functions exist? How many are injective? Give the formula and the numbers.
- bloom: apply
- bank: summative
- A: Each of the 5 domain elements picks one of 7 codomain elements: 7^5 = 16,807 functions. Injective functions choose 5 distinct codomain elements and order them: P(7, 5) = 7·6·5·4·3 = 2,520. No surjection exists since 5 < 7 — a function into a larger codomain cannot be onto.
- evidence: [S-0048]
- topic: cs-foundations/discrete-mathematics

### S2. Equivalence classes and partitions
- Q: Prove: if R is an equivalence relation on A, then the equivalence classes of R partition A (every element is in exactly one class).
- bloom: analyze
- bank: summative
- A: Reflexivity puts every a ∈ A in its own class [a], so classes cover A. If two classes [a] and [b] share an element c, then aRc and bRc; by symmetry cRa, and by transitivity bRa, and again by transitivity aRb — hence [a] = [b]. Overlapping classes are therefore identical, so classes are disjoint and cover A: a partition. This is the theorem that makes residue classes and hash-bucket reasoning possible.
- evidence: [S-0048]
- topic: cs-foundations/discrete-mathematics

### S3. CRT construction
- Q: Find all integers x satisfying x ≡ 2 (mod 3) and x ≡ 3 (mod 5). Justify why the answer is unique modulo 15.
- bloom: apply
- bank: summative
- A: Candidates 2, 5, 8, 11, 14, … (mod 15) with x ≡ 2 (mod 3): 2 mod 3 = 2; 5 mod 3 = 2; 8 mod 3 = 2; 11 mod 3 = 2; 14 mod 3 = 2. Check mod 5: 5 mod 5 = 0, 8 mod 5 = 3 ✓. So x ≡ 8 (mod 15). Since 3 and 5 are relatively prime, the Chinese remainder theorem guarantees exactly one class modulo 3·5 = 15; 8 + 15k for any integer k.
- evidence: [S-0048]
- topic: cs-foundations/discrete-mathematics

### S4. Ramsey-style reasoning
- Q: Every graph on 6 vertices contains either a triangle or an independent set of size 3. Justify this with pigeonhole-style counting (this is R(3, 3) = 6).
- bloom: analyze
- bank: summative
- A: Fix any vertex v and color each of its 5 edges red (v adjacent) or blue (v non-adjacent); by pigeonhole, at least 3 of the other vertices share the same color with v. Case red: if any two of those 3 are adjacent to each other, they form a triangle with v; if none are, those 3 form an independent set of size 3. Case blue: if any two of those 3 are non-adjacent to each other, they form an independent set with v; if none are (all pairwise adjacent), those 3 form a triangle. Either way, a triangle or an independent set of size 3 exists, so R(3,3) ≤ 6 (and K5 shows R(3,3) > 5).
- evidence: [S-0049]
- topic: cs-foundations/discrete-mathematics

## Review (spaced repetition — interleaved with prerequisites)

### R1. Truth table criterion (from logic-and-proof)
- Q: Without building the full table: is P → Q logically equivalent to ¬P ∨ Q? State the equivalence you are invoking.
- bloom: understand
- bank: review
- A: Yes — material implication is defined so P → Q is false only when P is true and Q is false, which is exactly when ¬P ∨ Q is false; they have identical truth tables. This equivalence is how conditional proofs get translated into disjunctions.
- evidence: [S-0048]
- topic: cs-foundations/discrete-mathematics

### R2. Proof by contradiction (from logic-and-proof)
- Q: Prove that √2 is irrational by contradiction, then re-express the same argument as a conditional proof. What assumption does each style start from?
- bloom: analyze
- bank: review
- A: Assume √2 = a/b in lowest terms; then 2b² = a², so a² is even, hence a even, a = 2k, so 2b² = 4k² and b² = 2k², making b even — contradicting lowest terms. As a conditional proof: "if √2 is rational then …" deriving a contradiction, i.e., ¬(√2 rational). Contradiction proves a negative by assuming the positive; conditional proof derives an implication directly.
- evidence: [S-0048]
- topic: cs-foundations/discrete-mathematics

### R3. Quantifier order (from logic-and-proof)
- Q: Compare ∀x ∃y R(x, y) with ∃y ∀x R(x, y) over a finite domain. Which implies the other, and why?
- bloom: analyze
- bank: review
- A: ∃y ∀x R(x, y) ⇒ ∀x ∃y R(x, y) (one fixed witness y works for every x), but not conversely: "everyone has a mother" does not imply "someone is everyone's mother." Quantifier order is not interchangeable — the standard test for reading nested quantifiers left to right.
- evidence: [S-0048]
- topic: cs-foundations/discrete-mathematics

### R4. Induction as a proof rule (interleaved)
- Q: Prove by induction that 1 + 2 + … + n = n(n+1)/2, and state where each of the two induction obligations appears.
- bloom: apply
- bank: review
- A: Base: n = 1 gives 1 = 1·2/2 ✓. Inductive step: assume the formula for n = k; then 1 + … + k + (k+1) = k(k+1)/2 + (k+1) = (k+1)(k+2)/2, the formula for k + 1. By the induction axiom both obligations (base case and P(k) → P(k+1)) together certify every n.
- evidence: [S-0045]
- topic: cs-foundations/discrete-mathematics
