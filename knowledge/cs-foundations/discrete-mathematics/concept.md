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

# Discrete Mathematics

## Claims

### Sets, relations, functions

- A set is an unordered collection of distinct objects; two sets are equal exactly when they have the same elements (extensionality), and sets are described either by enumeration or by a predicate in set-builder notation [T3][S-0048].
- The empty set contains no elements and is a subset of every set; the power set of an n-element set contains exactly 2^n subsets [T3][S-0048].
- Union, intersection, difference, and complement are the basic set operations, and they satisfy De Morgan's laws: (A ∪ B)^c = A^c ∩ B^c and (A ∩ B)^c = A^c ∪ B^c [T3][S-0048].
- The Cartesian product A × B is the set of ordered pairs (a, b) with a ∈ A and b ∈ B, and |A × B| = |A| · |B| for finite sets [T3][S-0048].
- A binary relation R from A to B is a subset of A × B; on a single set a relation may be reflexive, symmetric, antisymmetric, and/or transitive, each defined by a quantified condition [T3][S-0048].
- An equivalence relation (reflexive, symmetric, transitive) partitions its underlying set into disjoint equivalence classes, with each element in exactly one class; conversely, every partition defines an equivalence relation [T3][S-0048].
- A partial order is a reflexive, antisymmetric, transitive relation; a total order additionally relates every pair of distinct elements [T3][S-0048].
- A function f: A → B is a relation assigning to each a ∈ A exactly one b ∈ B; a function may be injective (one-to-one), surjective (onto), or bijective (both), and f is bijective iff it has an inverse [T3][S-0048].

### Counting and combinatorics

- The product rule: a task with m outcomes followed by a task with n outcomes has m·n combined outcomes; the sum rule: two mutually exclusive tasks have m + n combined outcomes [T3][S-0048].
- The number of ways to choose and order k elements from n distinct elements is P(n, k) = n! / (n − k)!; the number of ways to choose k elements without order is C(n, k) = n! / (k! · (n − k)!) [T3][S-0048].
- The binomial theorem expands (x + y)^n as the sum over k of C(n, k)·x^(n−k)·y^k, and the coefficients satisfy Pascal's identity C(n, k) = C(n − 1, k − 1) + C(n − 1, k) [T3][S-0048].

### Induction and the pigeonhole principle

- Mathematical induction is the proof rule: if a property holds at the base case and, whenever it holds at k it holds at k + 1, then it holds for every natural number; Peano's 1889 axiomatization made induction an explicit axiom of arithmetic [T0][S-0045].
- Strong induction (assuming the property for all values below n) is equivalent in power to ordinary induction, and both are equivalent to the well-ordering principle: every nonempty set of natural numbers has a least element [T3][S-0048].
- The pigeonhole principle: placing n + 1 or more objects into n boxes forces some box to contain at least two objects; more generally, n objects into k boxes force some box to hold at least ⌈n/k⌉ objects [T3][S-0048].
- The pigeonhole principle is the r = 1 case of the finite Ramsey theorem — any coloring of the r-element subsets of a sufficiently large set with k colors contains a monochromatic subset of any prescribed size — which Ramsey proved in full generality in 1930 [T0][S-0049].
- Ramsey theory in graphs: for every pair of integers r, s ≥ 2 there is a number R(r, s) such that every 2-coloring of the edges of the complete graph on R(r, s) vertices contains a monochromatic K_r or K_s; R(2, s) = s, the edge case of the pigeonhole principle [T0][S-0049].

### Graph theory basics

- A graph G = (V, E) consists of a set of vertices and a set of unordered pairs of distinct vertices called edges; the degree sum satisfies the handshake lemma Σ deg(v) = 2|E| [T3][S-0048].
- A tree is a connected acyclic graph, and an n-vertex tree has exactly n − 1 edges; a graph is bipartite iff it contains no odd cycle [T3][S-0048].
- Graphs are represented by adjacency matrices (n² entries for n vertices) or adjacency lists (O(|V| + |E|) total space); the representation choice trades space against access time [T3][S-0048].

### Modular arithmetic

- Congruence: a ≡ b (mod m) iff m divides a − b; congruence is an equivalence relation on the integers whose classes are the residue classes 0, 1, …, m − 1 [T3][S-0048].
- Congruence is compatible with arithmetic: if a ≡ b and c ≡ d (mod m) then a + c ≡ b + d and a·c ≡ b·d (mod m) [T3][S-0048].
- The Chinese remainder theorem: if m1, …, mk are pairwise relatively prime, then the system x ≡ ai (mod mi) has a unique solution modulo the product m1·…·mk [T3][S-0048].
- Fermat's little theorem: if p is prime and p does not divide a, then a^(p−1) ≡ 1 (mod p); this underpins modular exponentiation, primality testing, and public-key cryptography [T3][S-0048].

## Details

- The five pillars of this topic — sets/relations/functions, combinatorics, induction, graphs, and modular arithmetic — are the vocabulary of every later CS theory topic: relations reappear as database schemas, functions as program specifications, induction in algorithm correctness, graphs in networking, and modular arithmetic in cryptography [T3][S-0048].
- Discrete mathematics is "discrete" because it studies countable structures (finite or countably infinite sets) rather than continuous ones — the counting arguments above are exactly the tool that makes algorithmic reasoning possible [T3][S-0048].
- Equivalence classes are the mental model behind modular arithmetic (residue classes), hashing (slots), and quotient constructions: whenever a relation is reflexive, symmetric, and transitive, elements can be treated interchangeably within a class [T3][S-0048].

## Boundaries / common misunderstandings

- A set is not a sequence: {1, 2} and {2, 1} are the same set, and sets contain no duplicates — multisets and ordered tuples are different objects [T3][S-0048].
- A function is not just "an arrow": the formal definition requires a relation in which every domain element maps to exactly one codomain element; a partial function (undefined for some inputs) is not a function in the total sense [T3][S-0048].
- Induction is not proof by example: checking the base case and one or two steps proves nothing; the inductive step must establish P(k) → P(k + 1) for an arbitrary k [T0][S-0045].
- The pigeonhole principle asserts existence, not location: it guarantees some box is crowded but gives no method to find it, and its contrapositive form is the basis of counting lower bounds (e.g., why 2^n subsets cannot fit in n memory cells) [T0][S-0049].
- "a ≡ b (mod m)" is a statement about a − b being divisible by m, not a claim that a and b are equal; the equivalence classes, not individual integers, are the objects of modular arithmetic [T3][S-0048].
- Partial orders are not "incomplete total orders": antisymmetry and transitivity without totality describe genuine hierarchies (subsets, divisibility, prerequisites) where incomparable elements are the norm [T3][S-0048].

## References (evidence records)

- [S-0048] Rosen 2019 — Discrete Mathematics and Its Applications, 8th ed., McGraw-Hill.
- [S-0049] Ramsey 1930 — On a Problem of Formal Logic, PLMS s2-30(1), 264-286.
- [S-0045] Peano 1889 — Arithmetices principia, nova methodo exposita, Fratres Bocca, Turin.
