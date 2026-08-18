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

# Parallel Programming — validation

Item anatomy: `- Q:` `- bloom:` `- bank:` `- A:` `- evidence:` `- topic:`.

## Formative (practice)

### F1. Taxonomy recall
- Q: State Flynn's taxonomy classes and give one hardware example of SIMD and one of MIMD.
- bloom: remember
- bank: formative
- A: SISD (one instruction stream, one data stream — classic single-core CPU), SIMD (one instruction stream, multiple data — vector units, x86 SSE/AVX, GPU cores), MIMD (multiple instruction and data streams — multicore CPUs, multiprocessor systems). GPUs are often called SIMD-style (SIMT) rather than pure SIMD.
- evidence: [S-0134]
- topic: systems-software/parallel-programming

### F2. DLP vs TLP
- Q: Explain the difference between data-level parallelism and thread-level parallelism, and name the hardware each maps to.
- bloom: understand
- bank: formative
- A: DLP applies one operation to many data items simultaneously — exploited by vector units, SIMD extensions, and GPUs. TLP runs many threads of control concurrently — exploited by multicore and multiprocessor systems. A workload can use both: e.g., threads on cores, each thread using SIMD instructions.
- evidence: [S-0134]
- topic: systems-software/parallel-programming

### F3. Amdahl arithmetic
- Q: A workload takes 100 s on one core: 20 s is inherently serial, 80 s is parallelizable. Compute the Amdahl speedup at N = 4 and the asymptotic limit as N -> infinity.
- bloom: apply
- bank: formative
- A: s = 0.2, so speedup(N) = 1 / (0.2 + 0.8/N). At N = 4: 1 / (0.2 + 0.2) = 2.5. As N -> infinity: 1 / 0.2 = 5. Even with unlimited cores, the serial 20% caps speedup at 5.
- evidence: [S-0132]
- topic: systems-software/parallel-programming

### F4. What a data race is
- Q: Define a data race in C, and state what the language standard says about a program that races.
- bloom: understand
- bank: formative
- A: Two threads access the same memory location without synchronization and at least one access is a write. In the C standard this is undefined behavior: the program has no defined meaning after the race, so symptoms (including none) are not part of the language's contract.
- evidence: [S-0103]
- topic: systems-software/parallel-programming

## Summative (mastery checkpoint)

### S1. Measured fractions, both laws
- Q: You profile a 60 s job: the profiler attributes 12 s to a serial stage and 48 s to a stage parallelizable across cores. (a) Compute the Amdahl speedup at N = 8 and N = 32 and the asymptotic bound. (b) Compute the Gustafson scaled speedup at N = 8 for the same fractions. (c) Explain why the two answers differ.
- bloom: apply
- bank: summative
- A: (a) s = 12/60 = 0.2, parallel fraction 0.8. Amdahl N=8: 1/(0.2+0.8/8) = 1/0.3 = 3.33; N=32: 1/(0.2+0.025) = 4.44; bound = 1/0.2 = 5. (b) Gustafson N=8: s + N(1-s) = 0.2 + 8*0.8 = 6.6. (c) Amdahl fixes problem size (serial 12 s is constant), so speedup saturates at 5; Gustafson lets the problem scale so total time stays fixed, so the parallel fraction multiplies with N — the laws answer different questions.
- evidence: [S-0132][S-0133]
- topic: systems-software/parallel-programming

### S2. Diagnosing a slow parallel loop
- Q: Two threads increment disjoint array elements in a tight loop and take locks anyway; performance is much worse than single-threaded. Propose two distinct hypotheses (one memory-system, one synchronization) and design a minimal experiment that distinguishes them.
- bloom: analyze
- bank: summative
- A: Hypothesis A: false sharing — the two elements share a cache line, so each increment invalidates the other core's copy (coherence traffic). Hypothesis B: lock contention — the lock serializes the loop (plus acquire/release overhead). Experiment: (1) remove the lock (elements are disjoint — if speed recovers, contention was the cause); (2) pad elements to separate cache lines (align/pad so each element spans its own line — if speed recovers without the lock, false sharing was the cause). A third check: count cache misses (perf) before and after padding.
- evidence: [S-0039][S-0134]
- topic: systems-software/parallel-programming

### S3. GPU divergence
- Q: A GPU kernel has an if/else whose condition varies per thread within one warp. Explain what the hardware does and why the branch is called divergent.
- bloom: analyze
- bank: summative
- A: The warp executes in lockstep: threads that take the if-branch run while the else-lanes are masked, then the else-lane threads run while the if-lanes are masked — both paths execute serially for the whole warp. Total work = both branches for the warp, not one branch per thread; this is warp divergence, a data-parallel performance hazard.
- evidence: [S-0134]
- topic: systems-software/parallel-programming

## Review (spaced repetition — interleaved with prerequisites)

### R1. Why false sharing generates traffic (from hardware/cache-coherence)
- Q: Thread A writes variable x, thread B writes variable y; x and y sit in the same cache line. Neither thread touches the other's variable — yet the machine generates coherence traffic. Explain the mechanism.
- bloom: understand
- bank: review
- A: Coherence operates at cache-line granularity: the protocol sees one shared line, and every write must invalidate or update all other copies of that line. A's write invalidates B's copy of the line (and vice versa), forcing re-fetches even though no data is truly shared — false sharing, a granularity artifact of coherence.
- evidence: [S-0039]
- topic: hardware/cache-coherence

### R2. Invalidate-based protocols (from hardware/cache-coherence)
- Q: In an invalidate-based coherence protocol (e.g., MSI/MESI), what happens to the copies of a cache line held by other cores when one core writes the line, and what must the writer do before writing?
- bloom: understand
- bank: review
- A: The writer must first acquire exclusive ownership: the protocol sends invalidations to all other holders, which discard their copies and acknowledge; the writer then has the only copy (modified) and can write. Later reads of the line by other cores miss and fetch the updated copy. This is the single-writer-multiple-reader invariant that makes shared-memory parallel programs see coherent data.
- evidence: [S-0040]
- topic: hardware/cache-coherence

### R3. The race boundary in C (from programming/memory-model-and-pointers)
- Q: Two threads read the same variable concurrently: legal or a race? Two threads write different elements of the same array concurrently: legal? State the precise boundary of a data race.
- bloom: understand
- bank: review
- A: Concurrent reads of the same location: no race, legal. Concurrent writes to different elements of the same array: no race (different memory locations), legal. A race requires the same location, at least one write, and no synchronization (happens-before) between the accesses. Anything else (same location, one write, unsynchronized) is undefined behavior in C.
- evidence: [S-0103]
- topic: programming/memory-model-and-pointers

### R4. Races and the optimizer (from programming/memory-model-and-pointers)
- Q: Wang et al. (2013) showed real kernels and databases relying on undefined behavior caused by racing code. Give one concrete way a compiler can change a program that races, and why the optimizer is allowed to.
- bloom: understand
- bank: review
- A: The compiler may assume the program is data-race-free: it can reorder, eliminate, or transform the racing access — e.g., remove a "redundant" load the race makes it believe is unused, or cache a value in a register across the racy write. It is allowed because a race is undefined behavior: the transformed program must only behave correctly for conforming (race-free) executions.
- evidence: [S-0104]
- topic: programming/memory-model-and-pointers
