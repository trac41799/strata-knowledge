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

# Data Structures — validation

Item anatomy: `Q` · `bloom` · `bank` · `A` · `evidence` · `topic`.

## Formative (practice)

### F1. Operation vocabulary
- Q: Which structure gives O(1) read of the k-th element: an array or a singly linked list? Which gives O(1) insertion after a known node?
- bloom: remember
- bank: formative
- A: Arrays give O(1) random access via base-address arithmetic (A[i] = base + i·size); linked lists need O(k) pointer traversal. Linked lists give O(1) insertion after a known node (splice one pointer); arrays shift O(n) elements.
- evidence: [S-0055]
- topic: cs-foundations/data-structures

### F2. BST worst case
- Q: Keys 1, 2, 3, …, n are inserted into an initially empty BST in increasing order. What shape does the tree take, and what is the cost of searching for key n?
- bloom: apply
- bank: formative
- A: Each new key becomes the right child of the previous one — a chain (degenerate tree) of height n − 1. Searching costs O(h) = O(n): the BST is asymptotically a linked list. This is why balanced BSTs rebalance.
- evidence: [S-0055]
- topic: cs-foundations/data-structures

### F3. Load factor arithmetic
- Q: A hash table with chaining has m = 10 slots and currently holds n = 25 keys. Compute α and the expected search cost under uniform hashing. What would you do to restore constant-time behavior?
- bloom: apply
- bank: formative
- A: α = n/m = 2.5; expected search is O(1 + α) = 3.5 probes. Restore α ≈ 1 by resizing: allocate ~25–50 slots and rehash every key (expected O(n) total, O(1) amortized with doubling).
- evidence: [S-0055]
- topic: cs-foundations/data-structures

### F4. Amortized accounting
- Q: A dynamic array starts at capacity 1 and doubles when full. Give the total number of element copies for 8 appends, and the amortized cost per append.
- bloom: analyze
- bank: formative
- A: Copies happen at growth: 0 (1st), 1 (2nd), 2 (4th), 4 (8th) — total 7 copies for 8 appends. Amortized cost = (8 writes + 7 copies)/8 < 2 per append = O(1). Doubling geometric growth makes each element copied O(log n) times, total O(n) over n appends.
- evidence: [S-0053]
- topic: cs-foundations/data-structures

## Summative (mastery checkpoint)

### S1. Choosing a structure
- Q: You need a buffer where items are appended at one end and consumed at the other, never inspected in the middle, and memory must stay contiguous. Which structure, and why? Give operation costs.
- bloom: evaluate
- bank: summative
- A: A circular array (ring buffer) implementing a FIFO queue: enqueue and dequeue each O(1) with head/tail indices modulo capacity, contiguous memory, and no node allocation. A linked list would also give O(1) enqueue/dequeue but breaks contiguity; a stack is wrong because consumption is FIFO.
- evidence: [S-0055]
- topic: cs-foundations/data-structures

### S2. Heap operation trace
- Q: Show the array contents of a min-heap [3, 7, 9, 12, 15] after insert(1) and then extract-min. State the cost of each operation and why.
- bloom: apply
- bank: summative
- A: Insert 1 at position 5 → [3, 7, 9, 12, 15, 1], then sift up: swap with parent 9, then parent 3 → [1, 7, 3, 12, 15, 9]. Extract-min: remove 1, move the last element 9 to the root → [9, 7, 3, 12, 15], then sift down swapping with the smaller child: 9 swaps with 3 → [3, 7, 9, 12, 15]; children of 9 (12, 15) are larger, stop. Each operation walks one root-to-leaf path: O(log n).
- evidence: [S-0055]
- topic: cs-foundations/data-structures

### S3. Open addressing probes
- Q: An open-addressing table with linear probing has load factor α = 0.9. Estimate the expected number of probes for an unsuccessful search and explain the practical consequence.
- bloom: analyze
- bank: summative
- A: Expected unsuccessful search ≈ 1/(1 − α) = 1/0.1 = 10 probes, vs ~1.1 probes at α = 0.1. The 1/(1 − α) bound shows probe count grows steeply as α → 1: keeping α under ~0.7 (with rehashing) is the standard operating rule; at α ≈ 1 linear probing degenerates toward long cluster scans.
- evidence: [S-0055]
- topic: cs-foundations/data-structures

### S4. Universal hashing reasoning
- Q: An adversary supplies the keys. Why does a fixed hash function fail, and why does choosing h randomly from a universal family restore the expected O(1) guarantee?
- bloom: analyze
- bank: summative
- A: With a fixed h, the adversary can select n keys that all collide (worst case O(n) per op). Universal hashing randomizes h after (or independently of) the key choice: for any two distinct keys, at most |H|/m functions collide, so the expected number of collisions stays bounded regardless of the input — the Carter–Wegman input-independence theorem. The adversary cannot adapt to a function chosen at random.
- evidence: [S-0054]
- topic: cs-foundations/data-structures

## Review (spaced repetition — interleaved with prerequisites)

### R1. Contraposition (from logic-and-proof)
- Q: State the contrapositive of "if the heap property holds at the root after sift-down, then the tree is a valid heap." Why is the contrapositive the form used in induction-based heap proofs?
- bloom: understand
- bank: review
- A: Contrapositive: "if the tree is not a valid heap, then the heap property failed at the root after sift-down." Contraposition (P → Q iff ¬Q → ¬P) is used when it is easier to assume the conclusion fails and derive the failure of the hypothesis — the standard structure of correctness arguments for sift-down and rebalancing.
- evidence: [S-0055]
- topic: cs-foundations/data-structures

### R2. Induction template (from logic-and-proof)
- Q: Prove by induction that a binary tree with n nodes has exactly n − 1 edges, and name the two obligations.
- bloom: apply
- bank: review
- A: Base n = 1: one node, zero edges ✓. Step: any n-node tree has a leaf; remove it and its edge, leaving an (n−1)-node tree with (n−2) edges by hypothesis; re-adding the leaf gives (n−1) edges. Obligations: base case and P(k) → P(k + 1) for arbitrary k. The same induction pattern proves heap sift-down terminates in O(log n) steps.
- evidence: [S-0055]
- topic: cs-foundations/data-structures

### R3. Quantified claim check (from logic-and-proof)
- Q: A colleague claims "for every hash function h, there exists an input where h runs in O(n) time per lookup." Is that a true quantified statement, and does it contradict universal hashing?
- bloom: analyze
- bank: review
- A: The statement is true — for any fixed h an adversarial input exists (worst case). It does not contradict universal hashing: universal hashing randomizes the function choice, so the statement "there exists a bad input for h" no longer applies to a function drawn at random after the input is fixed — quantifier order is exactly what changes: ∃h vs ∀h, and expected vs worst case.
- evidence: [S-0054]
- topic: cs-foundations/data-structures

### R4. Pigeonhole in hashing (interleaved with discrete-mathematics)
- Q: 101 keys are placed into 100 slots. What does the pigeonhole principle force, and how does load-factor-based sizing (α ≈ 1) relate to it?
- bloom: analyze
- bank: review
- A: Some slot receives at least ⌈101/100⌉ = 2 keys — collisions are unavoidable once n > m. Hashing cannot eliminate collisions, only make them rare (expected): keeping α = n/m bounded makes the expected number of collisions per slot constant, which is the pigeonhole principle read in reverse — sizing the table is choosing how many collisions to accept.
- evidence: [S-0055][S-0054]
- topic: cs-foundations/data-structures
