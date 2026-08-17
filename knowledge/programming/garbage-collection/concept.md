---
id: programming/garbage-collection
title: Garbage Collection
band: B3
track: programming
tier: T1
bloom_target: apply
prerequisites: [programming/memory-model-and-pointers]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-garbage-collection
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0026, S-0027, S-0028]
---

# Garbage Collection

## Claims

### Why GC exists

- Manual memory management (`malloc`/`free`, `new`/`delete`) has three canonical error classes — forgetting to free (memory leak), freeing too early (dangling pointer / use-after-free), and freeing twice (double free) — and garbage collection exists to make these impossible by automating reclamation. [T3][S-0028]
- GC delivers software-engineering benefits (memory-safety errors removed, no manual ownership protocol) at a measurable performance cost that depends on collector design and heap sizing — it is a time-space tradeoff, not a free lunch. [T1][S-0027]

### Reachability & GC roots

- A collector defines liveness as reachability: an object is live iff it is reachable from a set of roots — global/static variables, stack slots, and registers of running threads; anything unreachable from the roots is garbage and reclaimable. [T3][S-0028]
- Reachability is a conservative proxy for "will be used again": a reachable-but-never-used object (e.g., an entry kept alive by a cache you forgot to evict) cannot be reclaimed, because the collector cannot predict future use. [T3][S-0028]
- Collectors must know which stack slots and registers hold pointers; imprecise (conservative) collectors treat every bit pattern as a potential pointer, retaining some garbage, while precise collectors need language/compiler support (no arbitrary pointer arithmetic). [T3][S-0028]

### Tracing vs reference counting

- Garbage collection has two families — tracing collectors (mark-sweep and descendants) and reference counting — and reference counting IS a form of GC, not an alternative to it. [T3][S-0028]
- Reference counting keeps a per-object count of incoming references: stores increment the target's count, dead stores decrement it, and an object is freed when its count reaches zero; the cost is paid on every pointer mutation, regardless of whether the object ever becomes garbage. [T3][S-0028]
- Plain reference counting cannot reclaim cyclic garbage: objects in a reference cycle hold non-zero counts while being unreachable, so they leak unless the collector adds cycle-detection machinery (e.g., trial deletion) that a tracing collector does not need. [T3][S-0028]
- Empirical comparison: in Berkeley Smalltalk, replacing reference counting with generational scavenging cut time spent reclaiming storage 8-fold (13% → 1.5% of run time), and the system ran 1.7x faster once the collector's compaction removed an indirection table. [T1][S-0026]

### Mark-sweep, mark-compact, copying

- Mark-sweep works in two phases: mark traces the reachable object graph from the roots, then sweep scans the heap linearly and reclaims every unmarked object; it never moves objects, so it does not fix fragmentation. [T3][S-0028]
- Mark-compact adds a compaction pass that slides survivors into a contiguous block, eliminating fragmentation without extra space — at a cost proportional to the live set. [T3][S-0028]
- Copying (semi-space / scavenging) collectors divide the heap into from-space and to-space, copy survivors to to-space each collection, then flip roles: allocation is a bump pointer, collection cost is proportional to live (not dead) data, and compaction is intrinsic — at the price of roughly 2x address space. [T3][S-0028]
- Fragmentation: repeated allocate/free of varying sizes scatters free memory into small chunks, so a large allocation can fail while total free space is ample; copying and compacting collectors avoid this by design. [T3][S-0028]

### Generational collection

- The generational hypothesis — "most objects die young" — is an empirical regularity first quantified by Ungar (1984): Smalltalk object-lifetime measurements showed young objects die quickly while old objects persist. [T1][S-0026]
- Generational collectors exploit the hypothesis: a small young generation (nursery) is collected frequently, survivors are promoted to an old generation collected rarely, so most garbage is reclaimed by cheap nursery collections and total collection cost drops. [T3][S-0028]
- A nursery-only collection must treat old-to-young pointers as roots: a write barrier records such stores into a remembered set so the collector never scans the whole old generation. [T3][S-0028]

### Stop-the-world vs concurrent collection

- Tracing collectors traditionally stop the world: the mutator is suspended for the whole collection, so pause time grows with the live set; generational design keeps pauses short and frequent by collecting only the nursery. [T3][S-0028]
- Incremental and concurrent collectors interleave collection with program execution using read/write barriers; low-latency collectors such as C4 (Tene, Iyengar & Wolf, ISMM 2011) and ZGC/Shenandoah (OpenJDK) target pause times of roughly 10 ms or less even on very large heaps, paying extra CPU and memory for latency. [T3][S-0028]

### Performance & pause-time tradeoffs

- Hertz & Berger (2005) quantified the time-space tradeoff: with 5x the memory explicit management requires, a generational tracing collector matches or slightly beats `malloc`/`free`; with 3x it runs ~17% slower; with 2x, ~70% slower; and when physical memory is scarce, paging makes it an order of magnitude slower. [T1][S-0027]
- Generational tracing collectors add up to ~50% space overhead and 5–10% runtime overhead versus explicit memory management when memory is not scarce. [T1][S-0027]

### Tracing vs reference counting in practice

- Tracing wins in throughput-oriented runtimes: its amortized cost is proportional to the live set at collection time, whereas reference counting pays a per-store cost on every pointer mutation — including mutations of objects that die young before any collection. [T3][S-0028]
- Reference counting retains niches needing immediate, deterministic reclamation (CPython, Swift ARC, C++ `shared_ptr`): no collection pauses, but cycles require separate handling (CPython adds a cycle collector; Swift relies on weak references). [T3][S-0028]

## Boundaries / common misunderstandings

- Reference counting is NOT the opposite of garbage collection — it is one of the two families of GC (automatic reclamation of unreachable storage). [T3][S-0028]
- Finalizers are not destructors: finalization runs asynchronously, at unspecified times, possibly never, so resource cleanup must use deterministic constructs (e.g., `using`/RAII), not finalizers. [T3][S-0028]
- GC does not make memory leaks impossible: leaks via unintended reachability (caches, event listeners, statics holding references) persist; GC only eliminates leaks of unreachable objects. [T3][S-0028]
- "GC is slow" is workload- and configuration-dependent, not inherent: with adequate memory headroom it matches manual management; the collapse happens when memory is scarce. [T1][S-0027]

## References (evidence records)

- S-0026 — Ungar (1984), SIGPLAN Notices 19(5):157–167: generational hypothesis measurements; scavenging vs reference counting (13% → 1.5%, 1.7x). (T1)
- S-0027 — Hertz & Berger (2005), OOPSLA, 313–326: GC vs explicit memory management time-space tradeoff. (T1)
- S-0028 — Jones, Hosking & Moss (2023), The Garbage Collection Handbook, 2nd ed., CRC Press: practice-level consensus on collector algorithms. (T3)
