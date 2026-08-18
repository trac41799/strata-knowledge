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
sources: [S-0039, S-0103, S-0104, S-0132, S-0133, S-0134]
---

# Parallel Programming

## Claims

### Hardware taxonomy and parallelism models

- Flynn's taxonomy classifies parallel hardware by instruction-stream and data-stream multiplicity: SISD (single instruction, single data), SIMD (one instruction stream over multiple data items — vector units, SIMD extensions, GPUs), MIMD (multiple instruction and data streams — multicore and multiprocessor systems); most real machines are hybrids of the categories [T3][S-0134].
- Computer architecture distinguishes data-level parallelism (DLP: one operation applied to many data items, exploited by vector/SIMD/GPU hardware) from thread-level parallelism (TLP: many threads of control, exploited by multicore/multiprocessors) [T3][S-0134].
- Data parallelism splits the data across workers and applies the same operation to each chunk; task parallelism splits the work into different tasks executed by different workers; the two strategies compose (e.g., a data-parallel stage inside a task-parallel pipeline) [T3][S-0134].
- GPUs are many-core, SIMD-style (SIMT) accelerators: thousands of threads execute in lockstep groups (warps) and map naturally onto data-parallel kernels; divergent control flow within a warp serializes, because threads that branch differently execute one path at a time [T3][S-0134].

### Speedup laws

- Amdahl's law: if a fraction s of a fixed-size workload is inherently serial, the maximum speedup with N processors is 1 / (s + (1-s)/N), which approaches the bound 1/s as N grows [T0][S-0132].
- Amdahl's law assumes a fixed problem size: s is the serial fraction of the single-processor run and does not shrink when processors are added [T0][S-0132].
- For a fixed-size problem with serial fraction s, the Amdahl bound is exact — no schedule of the parallel fraction can beat 1 / (s + (1-s)/N) [T0][S-0132].
- Gustafson's law (scaled speedup): if the problem size scales so that total execution time stays fixed, and s is the serial fraction of the scaled run, speedup is s + N(1-s), which grows with N rather than saturating at 1/s [T0][S-0133].
- Amdahl's law (fixed-size) and Gustafson's law (fixed-time) answer different questions: the first bounds speedup for a fixed workload, the second for a workload that grows with the machine; applying one where the other's assumption holds is a category error [T0][S-0133].

### Races and synchronization

- A data race occurs when two threads access the same memory location without synchronization and at least one access is a write; in the C language standard this is undefined behavior [T2][S-0103].
- Because data races are undefined behavior in C/C++, compilers may assume programs are race-free and transform code accordingly; Wang et al. (2013) found real production systems (including the Linux kernel and PostgreSQL) whose correctness silently depended on such undefined behavior, with crash and security consequences [T1][S-0104].
- Locks provide mutual exclusion: a thread holds the lock while updating shared state inside a critical section, serializing concurrent updates; spin locks, the hardware-level form (a lock variable polled with atomics), are a classic topic in the architecture literature [T3][S-0134].
- The C standard exposes a per-type lock-free property for atomic types (atomic_is_lock_free): implementations may implement some atomic operations with locks, and programs can query which; lock-free atomic operations make progress without blocking on a lock [T2][S-0103].
- False sharing: two threads write different variables that happen to occupy the same cache line; the coherence protocol treats the line as shared, so each write invalidates the other core's copy, generating cache-miss traffic with no real data sharing — an empirically measured artifact of shared-memory multiprocessors and standard coverage in the architecture literature [T1][S-0039][S-0134].

## Details

- Parallel performance on shared-memory machines is bounded by synchronization and coherence traffic as well as by the serial fraction; the coherence machinery behind shared writes is covered by hardware/cache-coherence [T3][S-0134].
- GPU kernels are written as data-parallel functions over thousands of threads; the programmer maps work to thread blocks, and the hardware schedules warps onto SIMD lanes [T3][S-0134].

## Boundaries / common misunderstandings

- Amdahl's law is not a universal "parallelism is hopeless" bound: it applies to fixed-size problems only; under fixed-time scaling (Gustafson's law) speedup grows with N, which is why near-linear speedups occur in practice despite nonzero serial fractions [T0][S-0133].
- SIMD is not a synonym for GPUs: SIMD instruction-set extensions (x86 SSE/AVX, ARM NEON) and GPU SIMT cores are different implementations of data-level parallelism [T3][S-0134].
- A data race is not merely "an intermittent bug that might bite": in C it is undefined behavior, so after a race the program has no defined meaning and the compiler may silently drop or reorder the racing operations [T2][S-0103].
- Lock-free is a per-operation/per-type property in the C standard, not a blanket guarantee for a data structure; a lock-free atomic does not mean "no thread ever waits" [T2][S-0103].
- Parallel programming is not distributed programming: parallel threads share memory and one failure domain on a single machine; distributed systems span machines with message passing and partial failure, where the hard problems are coordination and fault tolerance, not speedup — see systems-software/distributed-systems-basics [T3][S-0134].

## References (evidence records)

- [S-0132] Amdahl 1967 — Validity of the Single Processor Approach (AFIPS SICC '67).
- [S-0133] Gustafson 1988 — Reevaluating Amdahl's Law (CACM 31(5)).
- [S-0134] Hennessy & Patterson 2017 — Computer Architecture: A Quantitative Approach (6th ed.).
- [S-0039] Torrellas, Lam & Hennessy 1994 — False Sharing and Spatial Locality (IEEE TC), cited on one claim.
- [S-0103] ISO/IEC 9899:2018 (C17) — memory model, data races, atomics, cited on claims.
- [S-0104] Wang et al. 2013 — Towards Optimization-Safe Systems (SOSP '13), cited on one claim.
