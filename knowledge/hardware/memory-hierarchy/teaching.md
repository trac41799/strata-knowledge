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

# Memory Hierarchy — teaching

## Learning objectives (Bloom)

- **Remember** — state the AMAT model, the 2^index = size/(block × associativity) formula, and the SRAM/DRAM/flash/disk technology tiers.
- **Understand** — explain temporal and spatial locality and why the working-set model is the empirical basis of caching.
- **Apply** (target) — compute sets/index/tag/offset for a given cache, compute AMAT for multi-level hierarchies, and choose a technology for a storage role.
- **Analyze** — classify misses with the 3C model and map each class to its remedy; diagnose why a strided workload thrashes any cache.
- **Evaluate** — judge design tradeoffs (block size, associativity, capacity) for a stated workload and budget.

## Worked example 1 — cache hit/miss analysis

A 16 KB, 4-way set-associative cache with 64-byte lines, 32-bit addresses.

1. Geometry: sets = 16 KB / (64 B × 4) = 64; index bits = 6; offset bits = 6; tag bits = 32 − 12 = 20.
2. Address 0x0001FF40: binary ...0001 1111 1111 0100 0000 → offset = 0x40 (64, the first byte of a fresh line); index = bits 6..11 = 0x1F (31); tag = bits 12..31 = 0x1FF. The line lives in set 31, any of 4 ways, verified by tag 0x1FF.
3. A loop streaming a 32 KB array (twice the cache) sequentially: every line is a first touch (compulsory), then the second pass finds the working set exceeds capacity → capacity misses. Classify, do not guess: 3C says compulsory first, then capacity — no conflict here (fully sequential).
4. AMAT for this machine with L2: L1 miss rate 5% (L2 hit 20 cycles, 80% of L1 misses), memory 200 cycles (20% of L2 misses): AMAT = 1 + 0.05 × (20 + 0.20 × 200) = 1 + 0.05 × 60 = 4 cycles. The 1% of accesses that reach memory contribute 2 cycles — half the average.

## Worked example 2 — locality in a real loop

`for (i=0; i<N; i++) sum += a[i];` with 4-byte ints, 64-byte lines, N large:

- Each line holds 16 ints: one compulsory miss per 16 iterations, then hits (spatial locality), then next line.
- Stripe it: `for (i=0; i<N; i+=16)` — every access lands in a different line region of the same few sets → conflict thrash at small sizes; and each line is used once → compulsory-dominated.
- Same instruction count, wildly different memory behavior: locality is authored by the programmer.

## Elaboration prompts

- Why is the miss penalty term multiplied by miss rate in AMAT, and why does a 1% memory miss rate still dominate average time when the penalty is 200 cycles?
- Trace why a row-buffer-friendly access order (row-major over column-major) can make DRAM behave 2-10x faster without any cache change.
- If bandwidth grows faster than latency, why do wide lines, pipelined L2, and hardware prefetchers follow as design moves?
- Where exactly does the working-set model break down — what programs would you distrust it for, and why?
- Your workload has 40% compulsory misses. Which of the three AMAT levers still works, and which is wasted engineering?

## Common misconceptions

1. **"Main memory is slow."** DRAM is tens of nanoseconds in absolute terms. The problem is the 100-200 cycle gap to the CPU clock; a memory access is slow only relative to the processor. (S-0063)
2. **"Bigger cache / bigger blocks are always better."** Larger caches cost hit time and money; larger blocks buy spatial locality at the price of miss penalty and conflict misses. Both are measured tradeoffs. (S-0063)
3. **"The hierarchy is a hardware detail; programmers cannot influence it."** Locality is a property of the program: data layout, traversal order, padding, and blocking are the programmer's cache controls. (S-0065)
4. **"There is one 'the cache'."** Real systems have 2-3 levels with different sizes, associativities, and write policies; AMAT composes them level by level. (S-0063)
5. **"SRAM is 'fast memory' and DRAM is 'slow memory'."** Both are volatile; the real differences are cell structure (6T vs 1T1C), refresh, density, and cost per bit — SRAM happens to be fast because it is a latch, DRAM dense because it is a capacitor. (S-0064)

## Feynman targets

- Explain to a novice why "the computer has 32 GB of RAM" and "the CPU has a 16 KB cache" are answers to different questions, using the pyramid of levels.
- Explain in ≤3 sentences why a program that reads an array once can still benefit from a cache.
- Explain why doubling cache size does not halve misses, in terms of working sets and phases.
- Explain the difference between latency and bandwidth of memory using a courier vs a pipeline analogy that stays accurate about AMAT.

## Interleaving hooks

- **hardware/isa-basics** (prerequisite of next topics) — instruction fetch is itself a sequential access stream; the PC's spatial locality is what makes a small instruction cache effective, and immediate/fixed-width encodings change the fetch pattern.
- **hardware/cache-coherence** — multiprocessor systems add a coherence layer over this hierarchy; larger blocks' spatial-locality win turns into false-sharing traffic when cores share lines.
- **systems-software/virtual-memory** — the working-set model (S-0065) reappears as the paging policy theory; the TLB is a cache for page-table entries, and its misses are handled by the same 3C reasoning one level up.
- **hardware/storage-devices** (upcoming) — disk/SSD internals extend the same hierarchy reasoning below DRAM.
