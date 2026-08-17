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

# Garbage Collection — validation

## Formative (practice)

### F1 — remember: the generational hypothesis
- Q: State the generational hypothesis and name the 1984 study that first quantified it empirically.
- bloom: remember
- bank: formative
- A: "Most objects die young" — young objects become garbage quickly while objects that survive for a while tend to persist. Ungar (1984) measured object lifetimes in Berkeley Smalltalk, motivating generation scavenging.
- evidence: [S-0026]
- topic: programming/garbage-collection

### F2 — understand: reachability as liveness
- Q: Why does a garbage collector use reachability from roots as its definition of "live", instead of "will be used again"?
- bloom: understand
- bank: formative
- A: The collector cannot predict future use. Reachability is a sound, conservative approximation: everything reachable is kept (never a use-after-free of live data), and only provably unreachable objects are reclaimed. The cost of the approximation is that reachable-but-unused objects are retained (leak via reachability).
- evidence: [S-0028]
- topic: programming/garbage-collection

### F3 — understand: the reference-counting cycle problem
- Q: Two objects A and B reference each other (A→B, B→A) and no root reaches either. Under plain reference counting, what are their counts and what happens to them? Why?
- bloom: understand
- bank: formative
- A: Each has count ≥ 1 (each is referenced by the other), so neither ever reaches zero and neither is freed — a leak, even though the pair is unreachable. Pure reference counting only reacts to individual decrements; it cannot detect that a subgraph is globally unreachable without extra cycle-detection machinery (e.g., trial deletion).
- evidence: [S-0028]
- topic: programming/garbage-collection

### F4 — apply: trace mark-sweep on a small heap
- Q: Heap: A→B, B→D, C→D and C→E, E→F, G→H, I→B, and J is an int. Roots: GLOBAL1→A, stack→C, stack→G. Trace a full mark-sweep: which objects are marked, which are reclaimed, and what does the heap look like after the sweep?
- bloom: apply
- bank: formative
- A: Mark from the roots propagates: A,B,D (via A→B→D), C,E,F (via C→E→F), G,H. I and J are never reached — I is garbage even though it points at the live object B (marking only follows edges from marked objects). Sweep reclaims I and J; live objects keep their addresses, so the freed slots are holes in the heap (fragmentation if objects were variable-sized).
- evidence: [S-0028]
- topic: programming/garbage-collection

### F5 — understand: why nursery collections need a remembered set
- Q: A collector wants to collect only the nursery. A young object n4 is referenced only by an old object o1. Why must the collector treat o1 as a root, and how is that made cheap?
- bloom: understand
- bank: formative
- A: Without treating o1→n4 as a root, n4 would appear unreachable and be wrongly reclaimed while still referenced. A write barrier records every store of a young pointer into an old object, adding the old object to a remembered set; the nursery collection then scans roots + remembered set instead of the whole old generation.
- evidence: [S-0026, S-0028]
- topic: programming/garbage-collection

## Summative (mastery checkpoint)

### S1 — apply: trace a generational scavenge
- Q: Nursery: n1..n7. Old: o1, o2. Edges: n1→n2, n2→n3, o1→n4, n4→n5. Roots: stack→n1, stack→o2, o2→o1. Remembered set: {o1}. n1 has already survived one scavenge; the tenuring threshold is 2. Trace a nursery scavenge: which objects die, which are copied to to-space, which are promoted, and what happens to the remembered set?
- bloom: apply
- bank: summative
- A: Roots for this collection = stack (n1, o2) + remembered set ({o1}→n4). Marking: n1→n2→n3 and n4→n5; so n1..n5 survive, n6 and n7 are dead and their nursery space is reclaimed wholesale. Copy: n2,n3,n4,n5 copied to to-space (first survival); n1 (second survival, threshold 2) is promoted to the old generation. Remembered set: o1 still points at n4, now at its new location (forwarding pointers during the copy) — the entry stays, so the next scavenge still finds n4. From/to spaces swap; allocation resumes by bump pointer in the empty space.
- evidence: [S-0026, S-0028]
- topic: programming/garbage-collection

### S2 — analyze: choose a collector family
- Q: A service allocates huge numbers of short-lived objects, keeps a small long-lived set, and suffers OOM-like failures when a large buffer cannot be allocated despite ample total free memory. Which design (mark-sweep, mark-compact, copying, generational) addresses each symptom, and what does it cost?
- bloom: analyze
- bank: summative
- A: High allocation of short-lived objects → the generational hypothesis applies: a generational design with a small nursery collects frequently and cheaply. Large-buffer failure despite free memory = fragmentation → need compaction: mark-compact or copying (or a generational collector with a compacting old generation). Costs: mark-compact pays compaction proportional to the live set; copying needs ~2x space; a plain mark-sweep fixes neither symptom. No design avoids the fundamental space-time tradeoff.
- evidence: [S-0028]
- topic: programming/garbage-collection

### S3 — analyze: interpret the Hertz & Berger tradeoff
- Q: A benchmark runs the same program under malloc/free and under a generational tracing collector with (a) 5x, (b) 3x, (c) 2x the minimal memory. What does each configuration predict, and why does the curve collapse so steeply?
- bloom: analyze
- bank: summative
- A: (a) ~parity (GC can slightly win), (b) ~17% slower, (c) ~70% slower; with physical-memory scarcity, paging makes GC an order of magnitude slower. The curve collapses because smaller heaps force more frequent collections, and each collection's cost is dominated by heap/live-set size; below the working-set threshold, the GC's extra memory traffic spills to disk (page faults), which is orders of magnitude more expensive than CPU work. Lesson: GC's competitive zone is memory-abundant, and its failure mode is memory pressure.
- evidence: [S-0027]
- topic: programming/garbage-collection

### S4 — evaluate: is "GC is slow" true?
- Q: A developer argues: "Garbage collection is inherently slower than manual memory management, so latency-critical code must use manual management everywhere." Evaluate this claim using the measured evidence.
- bloom: evaluate
- bank: summative
- A: The claim is partially correct but not "inherently": Hertz & Berger measured parity (even slight wins) at 5x memory headroom, with degradation only as headroom shrinks to 3x/2x and collapse under paging. The truth is a time-space tradeoff plus a workload factor: allocation rate, live-set size, and reference-mutation rate decide which design wins. Manual management eliminates GC's memory overhead but reintroduces dangling-pointer/double-free/leak bugs and per-allocation costs. Verdict: choose by workload and memory budget, not by a blanket rule.
- evidence: [S-0027]
- topic: programming/garbage-collection

## Review (spaced repetition — interleaved with prerequisites)

### R1 — remember (memory-model-and-pointers): what the roots are
- Q: A GC language program has globals, a heap, and a call stack. Which of these hold values the collector must scan as roots, and why aren't heap-internal references roots?
- bloom: remember
- bank: review
- A: Globals/statics, plus stack slots and registers of running threads: they are the only entry points into the heap not reachable through other heap objects. Heap-internal references are found by tracing from those roots — marking only follows edges from already-reachable objects, so scanning the heap as roots would be wrong (and would keep everything alive).
- evidence: [S-0028]
- topic: programming/memory-model-and-pointers

### R2 — apply (memory-model-and-pointers): what GC actually prevents
- Q: Classify: (a) forgetting to free a buffer, (b) freeing an object then dereferencing it, (c) freeing the same object twice. In a program under a tracing GC, which classes are impossible, and what leak-like failure remains possible?
- bloom: apply
- bank: review
- A: (a) leak, (b) dangling pointer / use-after-free, (c) double free. Tracing GC makes (b) and (c) impossible for heap objects (reclaimed objects are unreachable, so no code can hold a valid pointer to them) and removes (a) for unreachable objects. The remaining failure is a leak via unintended reachability — an object kept alive by a root you forgot to drop (cache, listener, static) — which GC cannot detect because the object is, by definition, reachable.
- evidence: [S-0028]
- topic: programming/memory-model-and-pointers

### R3 — understand (garbage-collection): why tracing dominates throughput runtimes
- Q: Given that reference counting reclaims memory immediately and needs no tracing pauses, why do throughput-oriented runtimes (JVM, Go, .NET) use tracing collectors instead?
- bloom: understand
- bank: review
- A: Reference counting pays a cost on every pointer store — even for objects that die young and would never be traced — and cannot reclaim cycles without extra machinery, which is hard to make concurrent and cheap. Tracing's amortized cost is proportional to the live set at collection time, which generational design concentrates in a small nursery; Ungar's 8-fold reclaim-time reduction over reference counting is the classic empirical demonstration. Determinism wins only in niches (CPython, Swift ARC, shared_ptr).
- evidence: [S-0026, S-0028]
- topic: programming/garbage-collection
