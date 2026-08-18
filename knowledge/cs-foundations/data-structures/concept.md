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

# Data Structures

## Claims

### Arrays and dynamic arrays

- An array stores n elements in contiguous memory, so A[i] is read or written in O(1) time given the base address and element size [T3][S-0055].
- Insertion or deletion at an arbitrary position of an array costs O(n) because later elements must be shifted; appending past the fixed capacity is impossible without a new allocation [T3][S-0055].
- A dynamic array (e.g., vector, ArrayList) grows by allocating a larger block and copying when full; with doubling growth, a sequence of n appends performs O(n) total element copies, i.e., O(1) amortized time per append [T0][S-0053].
- Amortized analysis bounds the average cost per operation over a sequence, not the worst case of any single operation; Tarjan (1985) formalized it with accounting and potential-function methods [T0][S-0053].

### Linked lists, stacks, queues

- A singly linked list stores nodes holding an element and a pointer to the next node; finding the k-th element costs O(k) (no index arithmetic), while insertion or deletion after a known node costs O(1) [T3][S-0055].
- A stack is the LIFO structure: push, pop, and peek act on one end in O(1); a queue is FIFO: enqueue and dequeue act on opposite ends in O(1) when implemented with a linked list or circular array [T3][S-0055].
- The array-vs-list tradeoff is structural: arrays give O(1) index access and contiguous (cache-friendly) storage but O(n) middle insertion; linked lists give O(1) splice given a pointer but O(n) access and per-node allocation overhead [T3][S-0055].

### Trees: BSTs and heaps

- A binary search tree stores keys with all left-subtree keys less than the node key and all right-subtree keys greater; search, insert, and delete cost O(h), where h is the tree height [T3][S-0055].
- BST height ranges from Θ(log n) for balanced trees to Θ(n) when keys arrive in sorted order and the tree degenerates to a chain — unbalanced BSTs degrade to linear-time operations [T3][S-0055].
- Self-balancing BSTs (the Adelson-Velsky–Landis family and successors) rebalance by rotations after insert and delete, keeping height O(log n) and hence search/insert/delete at O(log n) worst case [T3][S-0055].
- A binary heap is a complete binary tree in which each node's key is ≤ (min-heap) or ≥ (max-heap) its children's keys; it is stored compactly in an array with children of position i at 2i+1 and 2i+2 [T3][S-0055].
- Heap insert and extract-min/max cost O(log n) (sift-up/sift-down along one root-to-leaf path), and building a heap from n elements costs O(n) when sift-down starts at the deepest internal level [T3][S-0055].
- A binary heap implements the priority-queue operations — insert O(log n), extract-min O(log n), peek O(1) — and is the engine of heapsort, which sorts in place in O(n log n) worst case [T3][S-0055].

### Hash tables

- A hash table stores n keys in a table of m slots, mapping each key by h(key) mod m; the load factor α = n/m governs performance [T3][S-0055].
- With chaining, colliding keys share a slot's list and, under uniform hashing, search costs expected O(1 + α) — constant time while α is kept bounded (e.g., α ≈ 1) [T3][S-0055].
- With open addressing, collisions are resolved by probing within the table (linear, quadratic, or double hashing); the expected number of probes is ~1/(1 − α) for unsuccessful search and ~(1/α)·ln(1/(1 − α)) for successful search, so performance collapses as α approaches 1 [T3][S-0055].
- Universal hashing makes the guarantee input-independent: choosing the hash function at random from a universal family bounds expected collisions for any key distribution; Carter & Wegman (1979) proved expected linear total time for storage and retrieval [T0][S-0054].
- Hash tables resize by rehashing when α crosses a threshold; with doubling, expected O(1) operations are preserved amortized — the same accounting as dynamic arrays [T0][S-0053][S-0055].

### Complexity of operations (formal)

- Asymptotic notation: f ∈ O(g) iff there exist c > 0 and n0 with f(n) ≤ c·g(n) for all n ≥ n0; Ω and Θ define lower and tight bounds, abstracting away constant factors and machine speed [T3][S-0055].
- Operation costs are stated as worst-case, expected, or amortized, and the three differ: BST search is O(n) worst case, hash search is O(1) expected under uniform/universal hashing, and dynamic-array append is O(1) amortized [T0][S-0053][S-0055].
- Comparison-based sorting needs Ω(n log n) comparisons in the worst case (decision-tree lower bound), and heapsort meets it with O(n log n) — optimal among comparison sorts [T3][S-0055].

## Details

- Data structures are not chosen in isolation: the operation mix (lookup-heavy vs update-heavy vs ordered iteration) determines which structure is correct, and the complexity claims above are the formal basis for that choice [T3][S-0055].
- Contiguity matters on real hardware: arrays and heaps exploit cache locality that pointer-chasing lists lose, so constant factors and memory layout distinguish structures that are asymptotically equal [T3][S-0055].
- The three analysis modes compose: a hash table with doubling is O(1) amortized expected — the guarantees stack because each one is stated precisely about a different axis (sequence-average vs randomness) [T0][S-0053][S-0054].

## Boundaries / common misunderstandings

- "O(1) average" is not "O(1) worst case": a hash table's constant time is expected (over the hash function or input distribution); a single pathological key set can still cost O(n) for one lookup [T0][S-0054].
- A linked list is not faster than an array in general: random access is O(n) and every node is a separate allocation; the O(1) insert/delete advantage applies only when the position is already known [T3][S-0055].
- Trees are not inherently O(log n): the guarantee is a bound on height; an unbalanced BST inserted in sorted order is a linked list in disguise with O(n) operations [T3][S-0055].
- A heap is not a sorted structure: only the root satisfies the heap property globally; extracting all elements in order costs O(n log n) — that is precisely why heapsort is not linear [T3][S-0055].
- Load factor is a ratio, not a count: performance is governed by α = n/m, so a 1000-element table with 1000 slots (α = 1) behaves like a 10-element table with 10 slots; keeping m proportional to n via rehashing is what preserves O(1) [T3][S-0055].
- "Amortized O(1)" does not mean every operation is fast: a single dynamic-array append can cost O(n) during a resize; the bound is on the total work of a sequence, per Tarjan's formalization [T0][S-0053].

## References (evidence records)

- [S-0053] Tarjan 1985 — Amortized Computational Complexity, SIAM J. Algebraic Discrete Methods 6(2), 306-318.
- [S-0054] Carter & Wegman 1979 — Universal Classes of Hash Functions, JCSS 18(2), 143-154.
- [S-0055] Knuth 1998 — The Art of Computer Programming, Vol. 3: Sorting and Searching, 2nd ed., Addison-Wesley.
