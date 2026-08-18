---
id: hardware/memory-hierarchy
title: Memory Hierarchy
band: B1
track: hardware
tier: T2
bloom_target: apply
prerequisites: []
related: []
recommended: []
status: published
schema-version: 1
owner: l1-memory-hierarchy
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0063, S-0064, S-0065, S-0018]
---

# Memory Hierarchy — validation

Format: `Q` / `bloom` / `bank` / `A` / `evidence` (spec §7). Banks: formative
(practice), summative (mastery, ≥80% at bloom_target), review (spaced,
interleaved with prerequisites).

## Formative (practice)

- Q: Which field of a 32-bit address does the cache use to select the set, and which field disambiguates the block in that set?
- bloom: remember
- bank: formative
- A: The index field selects the set (2^index sets); the tag field disambiguates which block occupies the set. The block offset selects the byte within the line.
- distractors: Tag selects the set, index disambiguates / offset selects the set / index selects the byte within the line.
- evidence: [S-0063]
- topic: hardware/memory-hierarchy

- Q: A loop iterates over a small array that fits entirely in the cache, repeatedly hitting the same lines. Which locality principle explains the hits?
- bloom: understand
- bank: formative
- A: Temporal locality: recently referenced items are likely to be referenced again soon, so the same lines keep hitting. (A sequential scan also exercises spatial locality, but the repeated-loop effect is temporal.)
- distractors: Spatial locality, because the array is contiguous / No locality, loops are control flow / It is a capacity effect.
- evidence: [S-0065]
- topic: hardware/memory-hierarchy

- Q: Why must DRAM be refreshed periodically while SRAM is not?
- bloom: understand
- bank: formative
- A: DRAM stores a bit as charge on a capacitor (one transistor per cell) that leaks and must be recharged (refreshed) on a schedule; SRAM uses a ~6-transistor latch that holds its state statically without refresh.
- distractors: SRAM is faster so it does not need refresh / DRAM is cheaper, so it tolerates refresh / Both require refresh, SRAM just does it faster.
- evidence: [S-0064]
- topic: hardware/memory-hierarchy

- Q: State the average memory-access time model in one line and name its three terms.
- bloom: remember
- bank: formative
- A: AMAT = hit time + miss rate × miss penalty. The three levers on memory performance are hit time, miss rate, and miss penalty.
- distractors: AMAT = hit time × miss rate + miss penalty / AMAT = miss rate / hit time / AMAT has no penalty term on modern caches.
- evidence: [S-0063]
- topic: hardware/memory-hierarchy

## Summative (mastery checkpoint)

- Q: A 16 KB cache has 64-byte blocks and 4-way set associativity, with 32-bit addresses. Compute: (a) number of sets, (b) index bits, (c) block-offset bits, (d) tag bits. Where does a given 32-bit address go?
- bloom: apply
- bank: summative
- A: (a) sets = 16 KB / (64 B × 4) = 16384/256 = 64 sets; (b) index = log2(64) = 6 bits; (c) offset = log2(64) = 6 bits; (d) tag = 32 − 6 − 6 = 20 bits. An address maps to set = index bits (bits 6-11), where it may occupy any of the 4 ways whose tag matches bits 12-31.
- distractors: 32 sets, 5 index bits / tag = 16 bits / the offset is 5 bits for 64-byte blocks.
- evidence: [S-0063]
- topic: hardware/memory-hierarchy

- Q: A two-level hierarchy: L1 hit 1 cycle, miss rate 5%, L2 hit 20 cycles, and misses from L2 (20% of L2 accesses) go to main memory at 200 cycles. Compute AMAT and the contribution of the L1 miss path.
- bloom: apply
- bank: summative
- A: AMAT = 1 + 0.05 × (20 + 0.20 × 200) = 1 + 0.05 × (20 + 40) = 1 + 3 = 4 cycles. The L1 miss path contributes 3 of 4 cycles: L2 hits (0.05×20 = 1) plus L2-miss-to-memory (0.05×0.20×200 = 2).
- distractors: AMAT = 1 + 0.05×200 = 11 / AMAT = 20 + 0.2×200 = 60 / AMAT = 1 + 0.05×20×200 = 201.
- evidence: [S-0063]
- topic: hardware/memory-hierarchy

- Q: Classify each miss stream (3C model) and propose the cheapest remedy: (1) first access to a file being read once; (2) a working set twice the cache size, streamed repeatedly; (3) two arrays that happen to map to the same set.
- bloom: analyze
- bank: summative
- A: (1) compulsory — unavoidable, only prefetching helps. (2) capacity — the cache is too small for the working set; increase cache size or restructure the loop. (3) conflict — raise associativity (or pad/offset one array) so both can coexist in the sets they need.
- distractors: (1) is a conflict miss / (2) is compulsory because data is large / (3) is capacity because the set is full.
- evidence: [S-0063]
- topic: hardware/memory-hierarchy

- Q: You must pick the technology for (a) an 8 MB on-chip cache, (b) 32 GB main memory, (c) 1 TB bulk storage. Choose and justify each.
- bloom: apply
- bank: summative
- A: (a) SRAM: ~1 ns access and no refresh, but low density and high cost per bit — only on-chip sizes are feasible. (b) DRAM: tens of ns, high density, cheap per bit, volatile — the main-memory sweet spot. (c) Flash (SSD): non-volatile, between DRAM and disk in latency/cost — bulk storage; mechanical disk remains for archival/very high capacity.
- distractors: (a) DRAM, it is denser / (b) SRAM, it is fastest / (c) DRAM, it is cheapest per bit.
- evidence: [S-0063, S-0064]
- topic: hardware/memory-hierarchy

## Review (spaced repetition — interleaved with prerequisites)

- Q: A code stream with no locality (e.g., a linked list scattered across memory) is processed through a cache. Which miss class dominates, and which cache optimization will NOT help it?
- bloom: understand
- bank: review
- A: Compulsory misses dominate (every line is a first touch). No cache parameter fixes compulsory misses — larger blocks, associativity, and capacity only help once lines are revisited (temporal/spatial locality present); prefetching is the only remedy, and only when access is predictable.
- distractors: Conflict misses; raising associativity fixes it / Capacity misses; any bigger cache fixes it / No misses occur, caches always help.
- evidence: [S-0063, S-0065]
- topic: hardware/memory-hierarchy

- Q: Why does the working-set model predict that a program's miss rate is not a single number, but a function of cache size?
- bloom: analyze
- bank: review
- A: A program's active data changes over phases: each phase has a working set (pages/lines referenced in the last T). If the cache holds the current working set, the program hits; if it is smaller, capacity misses recur in every phase. So miss rate vs cache size is a step-like curve, one step per phase's working-set size.
- distractors: Miss rate is fixed by the ISA / The working set is the whole program / Miss rate depends only on block size.
- evidence: [S-0065]
- topic: hardware/memory-hierarchy

- Q: A single memory access stream hits L1 95% of the time, L2 4%, and main memory 1%. Roughly what fraction of the AVERAGE time does the 1% of memory accesses contribute if L1=1 cycle, L2=10 cycles, memory=200 cycles?
- bloom: apply
- bank: review
- A: AMAT = 1 + 0.05×(10 + 0.20×200) = 1 + 0.05×50 = 3.5 cycles; the memory path contributes 0.01×200 = 2 cycles — over half the average time from 1% of accesses. This is why miss penalty (not just miss rate) is a primary design lever.
- distractors: 1% contributes ~1% of the time / 200 cycles dominate so L2 is irrelevant / memory contributes 0.05×200 = 10 cycles.
- evidence: [S-0063]
- topic: hardware/memory-hierarchy
