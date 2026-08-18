---
id: systems-software/parallel-programming
title: Parallel Programming
band: B3
track: systems-software
tier: T0
bloom_target: apply
prerequisites: [programming/concurrency-primitives, hardware/cache-coherence]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-parallel-programming
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0132, S-0133, S-0134]
---

# Parallel Programming — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — State Flynn's taxonomy, the DLP/TLP distinction, and the definitions of data race, false sharing, and lock-free atomic operations. (evidence: S-0134, S-0103)
- understand — Explain Amdahl's vs Gustafson's law, why coherence turns false sharing into traffic, and why data races are undefined behavior in C. (evidence: S-0132, S-0133, S-0039, S-0103)
- apply — Compute speedups with measured serial/parallel fractions under both laws, and size a parallelization decision from the numbers. (evidence: S-0132, S-0133) — **bloom_target**
- analyze — Given a poorly scaling parallel program (locks, false sharing, divergence), identify the bottleneck mechanism and design a discriminating experiment. (evidence: S-0039, S-0134)

## Worked example — Amdahl with measured fractions, then Gustafson

You run a video-transcoding pipeline on one core and profile it: 40 s total — 36 s in a parallelizable per-frame stage, 4 s in a serial setup/merge stage. Measured fractions: s = 4/40 = 0.10, p = 36/40 = 0.90.

**Amdahl (fixed-size, the 40 s workload):**
- N = 8 cores: speedup = 1 / (0.10 + 0.90/8) = 1 / (0.10 + 0.1125) = 1 / 0.2125 ≈ 4.7.
- N = 32 cores: speedup = 1 / (0.10 + 0.90/32) = 1 / (0.10 + 0.028125) = 1 / 0.128125 ≈ 7.8.
- N → ∞: speedup → 1/0.10 = 10. The serial 4 s caps the fixed-size pipeline at 10×, and the gains shrink fast: N=16 gives 1/(0.1+0.05625) ≈ 6.4, N=32 gives 7.8 — the last doubling of cores buys only ~1.4×. Lesson: adding cores past the knee of the curve is waste for a fixed workload.

**Gustafson (scaled, time fixed):**
- Now let the problem grow so the parallel stage fills more of the same wall-clock time, serial stage still 4 s in the scaled run: scaled speedup at N = 8: s + N(1-s) = 0.10 + 8·0.90 = 7.3 — versus Amdahl's 4.7 for the same N. The 7.3 means: with 8 cores you can process 7.3× the frames in the same time.

**Decision reading:** for a batch service with a backlog (scaled workload), Gustafson's number governs — adding cores scales throughput nearly linearly. For a latency-bound fixed job (e.g., one render), Amdahl's number governs — optimize the serial stage (the 4 s) first; at s = 0.10, cutting the serial stage in half raises the bound from 10× to 20×.

Key mental model: **measure s on the actual run; Amdahl bounds the fixed-size case (1/s), Gustafson the scaled case (s + N(1-s)); before optimizing parallelism, know which case you're in.**

## Worked example (mini) — race to UB

Two threads share `int counter = 0;` and each runs `counter++` 1000 times, unsynchronized, in C. The standard's model: the two increment sequences are loads/stores to one location, overlapping without a happens-before edge → data race → undefined behavior. Expected "2000" is not guaranteed; observed results may be 1000–2000 or anything the (optimizing) compiler produces after assuming the race away. Fix: an atomic increment (lock-free or not) or a mutex — a defined happens-before edge.

## Elaboration prompts

- Derive Amdahl's bound from "serial part s runs once, parallel part p runs in p/N": why is the formula exact rather than heuristic? (evidence: S-0132)
- The same measured fractions gave 4.7 (Amdahl) and 7.3 (Gustafson) at N = 8. Which number should a product team use to decide whether a batch pipeline should grow? (evidence: S-0133)
- Why does false sharing appear in *shared-memory* systems but not in message-passing ones — what role does the cache-line granularity of coherence play? (evidence: S-0039, S-0134)
- The C standard says a race is undefined behavior. What would change if it were merely "unspecified which value you read"? (evidence: S-0103, S-0104)
- A GPU kernel with divergence runs both branches for the whole warp. How does this change the advice for writing data-parallel kernels? (evidence: S-0134)

## Common misconceptions

1. **"Amdahl's law proves parallelism is hopeless."** It proves a bound for *fixed-size* problems; Gustafson's law — scaling the problem with the machine — grows with N, and real batch workloads scale. Amdahl's pessimism is a property of its fixed-size assumption, not of parallelism. (evidence: S-0132, S-0133)
2. **"A data race is an intermittent bug that mostly works."** In C/C++ a race is undefined behavior: the program's meaning is gone, and compilers routinely exploit race-freedom when optimizing — Wang et al. found kernel and database code silently depending on it. (evidence: S-0103, S-0104)
3. **"Adding threads always speeds things up."** Speedup is bounded by the serial fraction and degraded by synchronization, coherence traffic, and false sharing; the parallelization decision must be made from measured fractions, not thread count. (evidence: S-0132, S-0039)
4. **"SIMD is only about GPUs."** SIMD instruction-set extensions (SSE/AVX/NEON) and GPU SIMT cores are different hardware for the same idea (data-level parallelism); auto-vectorization of a loop is SIMD without any GPU. (evidence: S-0134)
5. **"Lock-free means nobody waits."** The C standard's lock-free property is per-atomic-type and means the atomic operation itself does not block on a lock — it says nothing about whole-structure progress or other threads' waiting. (evidence: S-0103)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why "40 s of work on 8 cooks" is not "5 s of wall time", using the serial recipe steps — grade against the Amdahl claims. (evidence: S-0132)
2. Why writing a bigger batch of cookies in the same time with more ovens behaves differently than baking one fixed batch faster — grade against the Gustafson claims. (evidence: S-0133)
3. Why two neighbors updating their own halves of a shared whiteboard cause a traffic jam at the eraser — grade against the false-sharing claims. (evidence: S-0039)

## Interleaving hooks

- **hardware/cache-coherence (prerequisite):** false sharing and coherence traffic are the memory-system half of parallel performance — rehearse MSI/MESI invalidation when diagnosing a slow parallel loop (R1, R2 in validation.md).
- **programming/memory-model-and-pointers (prerequisite):** the C memory model's data-race rule is the language half — happens-before, UB, and the optimizer (R3, R4 in validation.md).
- **programming/concurrency-primitives (prerequisite):** threads, mutexes, and atomics are the building blocks this topic reasons about; revisit after studying speedup to separate "program is correct" from "program is fast".
- **systems-software/distributed-systems-basics (cross-track):** parallel (shared memory, one failure domain) vs distributed (message passing, partial failure) — compare the speedup laws here with the failure vocabulary of distributed systems.
