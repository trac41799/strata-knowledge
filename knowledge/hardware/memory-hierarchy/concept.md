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

# Memory Hierarchy

Processors need memory that is fast, large, and cheap — no single technology delivers all three, so systems stack levels of storage (registers → caches → main memory → storage) and rely on programs' locality to make the stack behave like one fast, large memory.

## 1. Locality — the empirical foundation

- Programs do not access memory uniformly: references cluster in time and space — the principle of locality, experimentally validated over a decade of working-set studies [T3][S-0065]
- Temporal locality: an item referenced now is likely to be referenced again soon (loops, stack frames, hot counters) [T3][S-0065]
- Spatial locality: items near a referenced address are likely to be referenced soon (sequential code, arrays, structs) [T3][S-0065]
- Reference behavior is not uniform over time: programs alternate stable phases, each with a small active set, punctuated by transitions [T3][S-0065]
- The working set — the set of pages/lines referenced in the last T units of time — is the standard model of a program's current memory demand [T3][S-0065]
- Working-set-based management is near-optimal among policies without lookahead, which is why locality underwrites every cache level [T3][S-0065]
- Locality is a property of programs and their inputs, not of hardware: adversarial access patterns (strided, random) show almost no locality [T3][S-0065]

## 2. The hierarchy concept

- A memory hierarchy is a series of storage levels — registers, one or more caches, main memory, storage devices — each larger, slower, and cheaper per byte than the level above [T3][S-0063]
- Data moves between adjacent levels in blocks (lines/pages), never byte-by-byte; a hit is served at that level's latency, a miss recurses down [T3][S-0064]
- The design goal: present the speed of the top level with the capacity and cost of the bottom [T3][S-0063]
- The hierarchy exists because fast storage is expensive: SRAM costs far more per bit than DRAM, DRAM more than flash/disk [T3][S-0064]
- CS2023 requires memory-system organization for every CS graduate: AR/Memory Hierarchy is a 6-hour core knowledge unit of the Architecture and Organization KA [T2][S-0018]

## 3. Technology tiers: SRAM, DRAM, flash, disk

- SRAM: ~6-transistor cells, static (no refresh), ~1 ns access, low density, high cost per bit — used for on-chip caches and register files [T3][S-0064]
- DRAM: one-transistor-plus-capacitor cells, must be refreshed periodically, ~tens of ns, high density, cheap per bit — main memory [T3][S-0064]
- SRAM and DRAM are both volatile: contents are lost when power is removed; persistence only exists below main memory [T3][S-0064]
- DRAM chips are organized in banks, rows, and columns with a row buffer; an access activates a row, then reads/writes columns, so access patterns within a row are much cheaper [T3][S-0063]
- Flash (SSDs): non-volatile, latency between DRAM and disk, and now a standard hierarchy level for bulk storage [T3][S-0063]
- Mechanical disks: rotating media with millisecond seek/rotation latencies — the classic bottom level of the hierarchy [T3][S-0063]

## 4. Latency and bandwidth — the numbers

- H&P's worked example (4.0 GHz CPU, Intel Core i7 context): L1 hit latency is 4 cycles; DDR4-2400 DRAM latency is about 40 ns ≈ 160 cycles to the first 16 bytes; the full miss penalty is about 200 cycles [T3][S-0063]
- Main-memory accesses therefore cost on the order of 100-200 processor cycles — misses, not hits, dominate memory performance [T3][S-0063]
- Average memory-access time: AMAT = hit time + miss rate × miss penalty — the standard performance model of a hierarchy [T3][S-0063]
- Three levers follow from AMAT: cut hit time, cut miss rate, or cut miss penalty; different cache optimizations target different levers [T3][S-0063]
- Miss rate understates the problem: misses per instruction = miss rate × memory accesses per instruction, so instruction-heavy code amplifies misses [T3][S-0063]
- Bandwidth and latency are separate resources: nonblocking caches, multiple in-flight misses, and prefetching recover bandwidth even where latency is fixed [T3][S-0063]

## 5. Cache structure: sets, ways, lines

- A cache is organized as 2^index sets of E ways, each way holding one line (block) of B bytes; capacity = sets × ways × block size [T3][S-0063]
- Cache index size: 2^index = cache size / (block size × set associativity) [T3][S-0063]
- E = 1 is direct-mapped; E = all lines is fully-associative; in between is set-associative — associativity trades hit-time hardware against conflict misses [T3][S-0064]
- The address decomposes into tag | index | block offset: the index selects the set, the tag disambiguates which block lives there, the offset picks the byte [T3][S-0064]
- Larger blocks exploit spatial locality but lengthen miss penalty and can raise conflict misses; block size is a measured design point, not a constant [T3][S-0063]
- Replacement policy (LRU and approximations) decides which line a miss evicts once a set is full [T3][S-0064]
- Write policies: write-through (memory always current) vs write-back (dirty lines written on eviction), plus write-allocate vs no-write-allocate on write misses [T3][S-0064]
- Misses classify as compulsory (first touch), capacity (working set exceeds cache), or conflict (lines fight for a set) — the 3C model, each class with a different remedy [T3][S-0063]

## 6. Hierarchy design principles (Hennessy & Patterson)

- Make the common case fast: the hierarchy spends its engineering on hits and hides miss handling behind them [T3][S-0063]
- Larger caches reduce miss rates but lengthen hit time and raise cost; every level is a point on that tradeoff curve [T3][S-0063]
- The hierarchy is engineered around the latency gap: it is not "fast memory plus slow memory", but a chain of technologies each hiding the next level's latency behind block movement [T3][S-0063]
- Technology trends favor bandwidth over latency (DRAM bandwidth has grown much faster than DRAM latency), pushing wide blocks, pipelined access, and prefetch [T3][S-0063]

## Details — worked-example parameters (H&P 6th ed, Cortex-A8 example)

| Level | Latency | Notes |
|---|---|---|
| L1 (on-chip SRAM) | 4 cycles | pipelined, hit time |
| DRAM (DDR4-2400) | ≈ 40 ns (≈ 160 cy @ 4 GHz) | to first 16 bytes |
| Full miss penalty | ≈ 200 cycles | L3 miss detection + DRAM latency |

These are example values from one documented design (S-0063, Chapter 2), not universal guarantees.

## Boundaries / common misunderstandings

- Tier note: the pack's T2 tier comes from the CS2023 Architecture & Organization
  curriculum anchor [T2][S-0018]; the technical claims themselves are T3 (H&P-derived).
  [T2][S-0018]

- "Main memory is slow" — wrong in absolute terms: DRAM is tens of nanoseconds, fast by any human scale; it is the ~100-200 cycle gap to the CPU clock that makes misses expensive [T3][S-0063]
- The hierarchy is an engineering answer to the cost/latency tradeoff, not a ranking of "good" vs "bad" memories — each level is optimal for its role [T3][S-0064]
- Locality is an empirical regularity, not a guarantee: random or strided access patterns defeat caches, and the hardware is not "broken" when they do [T3][S-0065]
- Bigger blocks are not always better: the spatial-locality win is traded against miss penalty and conflict misses; the optimum is workload-dependent [T3][S-0063]
- Cache capacity is not "how much memory the CPU has": 2^index = capacity/(block × associativity) shows the same capacity can be organized many ways [T3][S-0063]
- SRAM vs DRAM is not "fast vs slow memory" in a vague sense: it is a specific technology tradeoff (transistor count, refresh, density, cost), and both are volatile [T3][S-0064]

## References (evidence records)

- S-0063 — Hennessy & Patterson (2019), Computer Architecture: A Quantitative Approach, 6th ed., Morgan Kaufmann
- S-0064 — Patterson & Hennessy (2021), Computer Organization and Design RISC-V Edition, 2nd ed., Morgan Kaufmann
- S-0065 — Denning (1980), IEEE TSE SE-6(1):64-84 — working sets, locality
- S-0018 — ACM/IEEE-CS/AAAI (2024), CS2023 — AR/Memory Hierarchy core unit
