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
status: draft
schema-version: 1
owner: l1-garbage-collection
reviewed-by: []
updated: 2026-08-18
sources: [S-0026, S-0027, S-0028]
---

# Garbage Collection — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **apply** — trace a full mark-sweep collection on a small heap: identify roots, propagate the mark, determine which objects the sweep reclaims, and predict the resulting fragmentation ([S-0028]).
- **apply** — trace a generational nursery scavenge with a remembered set: compute survivors, promotions, and deaths, and update the remembered set after copying ([S-0026], [S-0028]).
- **understand** — explain why plain reference counting leaks reference cycles and what machinery fixes it, on a concrete self-referential example ([S-0028]).
- **understand** — distinguish stop-the-world, incremental, and concurrent collectors, and state what low-pause collectors (C4, ZGC) trade away ([S-0028]).
- **analyze** — choose among mark-sweep / mark-compact / copying / generational designs given constraints on space, fragmentation, pause time, and allocation rate ([S-0028]).
- **evaluate** — assess the claim "GC is slower than manual memory management" against the measured time-space tradeoff, identifying the memory-headroom condition under which each side wins ([S-0027]).

## Worked example 1 — tracing mark-sweep on a small heap

Heap of 10 objects, edges as follows:

| Object | Points to | Object | Points to |
|---|---|---|---|
| A | B | F | (int) |
| B | D | G | H |
| C | D, E | H | (int) |
| D | (int) | I | B |
| E | F | J | (int) |

Roots: `GLOBAL1 → A`, `stack → C`, `stack → G`.

**Step 1 — mark.** Worklist starts at the roots: {A, C, G}.

1. Pop A → mark A → follow A→B, push B. 2. Pop B → mark B → follow B→D, push D. 3. Pop D → mark D (no outgoing pointers). 4. Pop C → mark C → follow C→D (already marked) and C→E, push E. 5. Pop E → mark E → follow E→F, push F. 6. Pop F → mark F. 7. Pop G → mark G → follow G→H, push H. 8. Pop H → mark H.

Marked: **{A, B, C, D, E, F, G, H}**. Note: I points at B but I itself is never reached — edges from unmarked objects are not followed.

**Step 2 — sweep.** Scan the heap linearly; reclaim every unmarked block: **I and J**.

**Observations.** (1) `I→B` did not save I: reachability is one-directional from the roots. (2) No object moved — A..H keep their addresses, so the freed I and J leave holes; with variable-sized objects this is exactly how fragmentation accumulates. (3) Total work = mark (∝ reachable graph) + sweep (∝ whole heap): mark-sweep always pays a full-heap scan ([S-0028]).

## Worked example 2 — a generational nursery scavenge

State before collection:

- Nursery: `n1, n2, n3, n4, n5, n6, n7` (nursery = from-space; to-space empty).
- Old generation: `o1, o2`.
- Edges: `n1→n2`, `n2→n3`, `o1→n4`, `n4→n5`, `o2→o1`.
- Roots: `stack → n1`, `stack → o2`. Remembered set: **{o1}** (o1 was recorded by the write barrier when `o1→n4` was stored).
- Tenuring threshold: 2 scavenges; `n1` has survived one scavenge already.

**Step 1 — find the roots of this collection.** A nursery-only collection never scans the old generation: roots = mutator roots that point into the nursery (`n1`) **plus** the remembered set (`o1`, because `o1→n4` reaches the nursery).

**Step 2 — copy survivors.** Trace from {n1, o1}:

- From n1: n2, then n3 → survivors **n1, n2, n3**.
- From o1: n4, then n5 → survivors **n4, n5**.
- n6 and n7 have no incoming references from roots ∪ remembered set → **dead**.

Survivors are copied to to-space (with forwarding pointers so `o1→n4` can be redirected to n4's new address). First-time survivors `n2..n5` stay young; **n1 survives its second scavenge → promoted to the old generation** (age counter reached the threshold).

**Step 3 — flip and resume.** From/to spaces swap; the dead nursery space (n6, n7, and the vacated survivors' old locations) is reclaimed **wholesale** — no per-object sweep. Allocation resumes with a bump pointer in the now-empty space. The remembered set still contains o1 (still points to n4, now at its new address) — recorded by the same write barrier on future stores ([S-0026], [S-0028]).

**Why the remembered set matters:** without treating o1 as a root, n4/n5 would be declared dead while still reachable from the old generation — a use-after-free bug. The write barrier is what makes the cheap, frequent nursery collection sound.

## Elaboration prompts

- Why is mark-sweep's sweep phase proportional to the *whole heap* while the mark phase is proportional to the *live set* — and what happens to a program with a huge heap and tiny live set? (Think: which design fixes that, and at what cost?)
- Reference counting pays on every pointer store; tracing pays only during collections. For a program that allocates millions of short-lived temporaries, why does tracing win — and for what program shape does RC's immediacy win?
- A remembered set tracks old→young pointers: why is a *write* barrier enough for a generational collector, but a *load* barrier needed by concurrent compacting collectors like C4/ZGC? (Hint: who can move an object while the mutator is running?)
- CPython layers a generational cycle collector on top of reference counting; the JVM uses generational tracing. What workload properties (allocation rate, mutation rate, cycles, pause tolerance) would make you pick each design? ([S-0026], [S-0028])
- Using the Hertz & Berger numbers (5x/3x/2x headroom), what does the pause/throughput curve of a stop-the-world collector do as the heap shrinks, and why does paging turn a 2x slowdown into 10x? ([S-0027])
- A cache keeps a reachable entry for an object nobody uses. Why can no collector reclaim it, and what does the runtime offer instead? (Weak references — a follow-up topic.)

## Common misconceptions

1. **"Reference counting is the opposite of garbage collection."** No — it is one of the two families of GC (automatic reclamation of unreachable storage). The real division is tracing vs reference counting, both GC. [S-0028]
2. **"With GC, memory leaks are impossible."** GC removes leaks of *unreachable* objects only. Leaks via unintended reachability — caches, event listeners, statics holding references — are invisible to the collector. [S-0028]
3. **"Finalizers are destructors."** Destructors (C++ RAII, `using` in C#/Python) run deterministically; finalizers run at unspecified times, possibly never, on a collector thread. Resource cleanup must never depend on finalization. [S-0028]
4. **"GC is inherently slower than manual memory management."** Measured evidence says parity at 5x headroom, ~17% at 3x, ~70% at 2x — the truth is a time-space tradeoff that flips under memory pressure (paging → 10x). [S-0027]
5. **"A tracing collector scans the entire heap on every collection."** Generational collectors routinely collect only the nursery using remembered sets; full-heap collections are rare. That asymmetry is the entire point of the design. [S-0026], [S-0028]
6. **"Stop-the-world pauses are unavoidable; you pick tracing and eat the pauses."** Incremental/concurrent collectors (C4, ZGC, Shenandoah) bound pauses to ~10 ms or less on huge heaps — paying with CPU and memory instead of latency. [S-0028]
7. **"Mark-sweep compacts memory."** Mark-sweep never moves objects — that is precisely why it fragments. Compaction is the job of mark-compact and copying collectors. [S-0028]

## Feynman targets

- "Explain to a non-programmer why 'most objects die young' lets a two-generation collector be faster than a whole-heap collector — in terms of what work gets done how often." ([S-0026])
- "Explain why a pair of objects that reference each other can leak forever under reference counting but not under tracing."
- "Explain what fragmentation is, why a large allocation can fail with plenty of free memory, and why copying collectors never hit that."
- "Explain when 'GC is slower' is true and when it isn't, using memory headroom as the variable." ([S-0027])

## Interleaving hooks

- **programming/memory-model-and-pointers** (prerequisite) — GC roots are exactly the stack slots/globals from that topic; recall why a GC language forbids arbitrary pointer arithmetic (precise roots), and revisit stack vs heap lifetimes: stack objects never need GC at all.
- **systems-software/virtual-memory** — the GC/memory interaction is physical, not just logical: copying collectors improve page locality, and Hertz & Berger's paging results are the fault-latency ladder (fault ≈ 5–6 orders slower than a TLB hit) applied to collector design ([S-0027]).
- **programming/concurrency-primitives** — write barriers and concurrent marking are synchronization between mutator threads and collector threads; concurrent collectors are lock-free-style coordination problems, not just algorithms.
- **programming/compiler-pipeline** — reference-count updates and write barriers are inserted by the compiler at assignment sites; collector design constrains code generation (e.g., precise stack maps of roots).

If the learner places as **novice**, start with Worked example 1 and Feynman target 1 before any quiz; if **competent**, start with a prediction task ("which collector leaks/fragments/pauses?"), then use the misconceptions list as a self-check.
