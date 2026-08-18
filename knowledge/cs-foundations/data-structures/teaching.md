---
id: cs-foundations/data-structures
title: Data Structures
band: B3
track: cs-foundations
tier: T0
bloom_target: apply
prerequisites: [cs-foundations/logic-and-proof]
related: [cs-foundations/algorithms]
recommended: []
status: published
schema-version: 1
owner: l1-data-structures
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0053, S-0054, S-0055]
---

# Data Structures — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — State the operation costs of arrays, linked lists, stacks, queues, BSTs, heaps, and hash tables in worst-case/expected/amortized terms. (evidence: S-0055)
- understand — Explain why dynamic arrays are O(1) amortized, why universal hashing removes the input-distribution assumption, and why load factor — not table size — governs hash performance. (evidence: S-0053, S-0054)
- apply — Choose a structure for a stated operation mix, trace heap insert/extract and BST insert, and compute load factors, probe counts, and amortized totals. (evidence: S-0055, S-0053) — **bloom_target**
- analyze — Given a performance claim, identify which mode (worst/expected/amortized) is being asserted and whether the data distribution or operation sequence invalidates it. (evidence: S-0054, S-0053)
- evaluate — Compare candidate structures on asymptotic cost, memory layout, and worst-case guarantees for a concrete application scenario. (evidence: S-0055)

## Worked example

### Part A — Analyzing a dynamic array, formally (amortized analysis)

**Setup.** A dynamic array starts empty with capacity 1. Append doubles the capacity when full, copying all elements.

**Question.** What is the amortized cost of an append over a sequence of n appends?

**Analysis (accounting method).** Charge each append 3 units of work:
- 1 unit for the immediate write of the new element;
- 2 units saved as "credit" on the element just written.

When a resize at capacity C happens, the array holds C elements, each carrying 2 credits — 2C units — exactly the cost of copying C elements into the new array. Every copy is therefore paid for by credits accumulated at earlier appends, never by the resize itself.

**Bound.** Total charge over n appends is 3n; total real work (writes + copies) ≤ 3n, so amortized cost per append is O(1), while the worst single append is O(n) — the two statements coexist because amortization is a sequence bound, as Tarjan (1985) formalized: each element is copied only O(log n) times under doubling, and n appends move O(n) total elements.

**Why the doubling matters.** With +1 growth (capacity increases by one), n appends copy 1 + 2 + … + (n − 1) = O(n²) elements — O(n) per append. The geometric ratio is what converts worst-case O(n) into amortized O(1). This is the same arithmetic that makes hash-table doubling (rehashing) amortized O(1).

### Part B — Choosing a structure with the cost table

**Scenario.** A spell-checker needs: (1) fast membership test "is this word known?", (2) millions of words, (3) no ordering requirement. A competitor needs: (1) ordered iteration, (2) predecessor/successor queries.

**Analysis.** (1) Hash table: expected O(1) lookup with chaining at α ≈ 1, or with universal hashing without trusting the dictionary's distribution (Carter–Wegman). (2) Balanced BST: O(log n) ordered operations — a hash table cannot answer "next word after 'quixotic'" without an O(n) scan, because it preserves no order.

**Key mental model:** hash = expected O(1) unordered membership; BST = O(log n) ordered operations; amortization = sequence-average accounting; and every "O(1)" hash claim carries an implicit distribution or randomness assumption.

## Elaboration prompts

- Derive the expected 1/(1 − α) probes for open addressing from the geometric series — where exactly does the load factor enter the sum? (evidence: S-0055)
- Why is 3 units of charge in the accounting example exactly enough, and what would break with a charge of 2? Relate the surplus to the potential method. (evidence: S-0053)
- Universal hashing randomizes the function but the guarantee is about collisions, not the hash values themselves — trace why "any two keys collide with probability ≤ 1/m" implies expected O(1 + α) search. (evidence: S-0054)
- A BST and a sorted array both answer "is key k present?" — lay out the full tradeoff (build cost, search cost, insert/delete cost, locality) and find the crossover point for your use case. (evidence: S-0055)
- Why must a heap be complete to achieve O(log n) bounds, and what breaks if the tree is allowed to be arbitrary? (evidence: S-0055)

## Common misconceptions

1. **"A hash table is always O(1)."** The claim is expected O(1) under uniform or universal hashing and bounded load factor; worst case (all keys colliding) is O(n) per lookup, and adversarial inputs defeat any fixed hash function — the reason universal families exist. (evidence: S-0054)
2. **"Linked lists beat arrays because insertion is O(1)."** Only with a pointer to the position; random access is O(n), each node costs an allocation, and contiguous arrays win on cache locality. The correct reading is a tradeoff, not a ranking. (evidence: S-0055)
3. **"Balanced trees are always better than plain BSTs."** Balance buys a Θ(log n) worst case at the cost of rebalancing complexity and constant factors; a plain BST with random insertions is near-optimal in practice. The height bound, not "tree-ness," is what delivers O(log n). (evidence: S-0055)
4. **"Amortized O(1) means every operation takes ~1 unit."** Amortization bounds sequence averages; individual operations may be expensive (resizes, rehashes). Confusing amortized with per-operation worst case produces wrong latency reasoning in real-time systems. (evidence: S-0053)
5. **"A heap is a sorted array."** Only the root-to-leaves ordering constraints hold; extracting all elements in sorted order costs O(n log n) — the very reason heapsort's bound is O(n log n), not O(n). (evidence: S-0055)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why a phone-book (array) lets you jump to entry 500 instantly but a chain of post-it notes (linked list) forces you to walk, while cutting a post-it chain in the middle is free — grade against the access-vs-splice claims. (evidence: S-0055)
2. Why a bus that doubles its seats when full runs a smooth average service even though some single rides trigger a huge refit — grade against the amortized-analysis claims. (evidence: S-0053)
3. Why a dictionary cannot be the same thing as a sorted phone book: one answers "is this word known?" in one step on average, the other "what comes after?" in log steps — and why neither is "better" without the question — grade against the hash-vs-tree claims. (evidence: S-0055, S-0054)

## Interleaving hooks

- **cs-foundations/logic-and-proof (prerequisite):** every complexity claim is a quantified statement (∃c, n0) and every correctness proof is induction — rehearse contraposition and induction before the formal complexity material (R1–R2 in validation.md).
- **cs-foundations/discrete-mathematics (recommended):** the pigeonhole principle explains why collisions are unavoidable (n > m), and counting arguments are the vocabulary of amortized totals — revisit after finishing that pack.
- **cs-foundations/algorithms (related):** sorting lower bounds and graph algorithms consume exactly the cost table built here (heaps → Dijkstra, BST → ordered maps, hash → dedup).
- **systems-software/virtual-memory (later):** array contiguity is what makes cache lines and page locality real — the "constant factors" hand-waved in asymptotic analysis are the difference between memory-hierarchy-friendly and hostile layouts.
