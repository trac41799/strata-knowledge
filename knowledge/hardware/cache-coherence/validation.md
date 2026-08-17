---
id: hardware/cache-coherence
title: Cache Coherence
band: B1
track: hardware
tier: T0
bloom_target: analyze
prerequisites: [hardware/memory-hierarchy, hardware/cpu-pipelining]
related: [systems-software/virtual-memory]
recommended: []
status: published
schema-version: 1
owner: l1-cache-coherence
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0038, S-0039, S-0040, S-0041]
---

# Cache Coherence — validation

Format: `Q` / `bloom` / `bank` / `A` / `evidence` (spec §7). Banks: formative
(practice), summative (mastery, ≥80% at bloom_target), review (spaced,
interleaved with prerequisites).

## Formative (practice)

- Q: What problem does a coherence protocol solve, in one sentence?
- bloom: understand
- bank: formative
- A: Without coordination, private caches can hold multiple copies of one line, so a read can return a stale value after another processor wrote the line; the protocol enforces the single-writer/multiple-reader (SWMR) invariant so reads always see the last write.
- distractors: It makes all processors execute in program order / it removes the need for caches / it prevents two processors from ever caching the same line.
- evidence: [S-0040]
- topic: hardware/cache-coherence

- Q: Which MESI state describes "the only cached copy, dirty, memory stale"?
- bloom: remember
- bank: formative
- A: M (Modified) — the cache holds the sole copy and its value is newer than memory, so the line must be written back before any other copy can exist.
- distractors: E (clean, not dirty) / S (may be shared, memory valid) / O (MOESI-only, dirty but shared).
- evidence: [S-0040]
- topic: hardware/cache-coherence

- Q: Trace this MESI sequence and check the invariant. Core A: read X (miss). Core B: read X (miss). Core A: write X (hit in S). Core B: read X. At every step, does SWMR hold? Which transition is the interesting one?
- bloom: analyze
- bank: formative
- A: A: I→E (sole copy). B: I→S (snoop forces A E→S). A: S→M via an upgrade that invalidates B's copy (B: S→I). B: I→M? No — read miss fetches to S if a copy exists, else E; A holds M so B fetches a fresh copy and both end in S (A: M→S with write-back). SWMR holds at every step: only A ever holds a writable copy, and B's later read gets the new value. The interesting transition is the S→M upgrade: it must invalidate every other copy *before* A's write becomes visible.
- distractors: SWMR is violated during the upgrade / B ends in M / A stays in M while B also reads X.
- evidence: [S-0040]
- topic: hardware/cache-coherence

- Q: A system is provably coherent (SWMR holds for every line). Does that mean it is sequentially consistent?
- bloom: understand
- bank: formative
- A: No. Coherence governs accesses to one location; consistency governs the ordering of accesses across locations (SC, TSO, weak models). x86 is coherent yet TSO, which allows store-load reordering SC forbids.
- distractors: Yes, SWMR implies SC / Only if the bus is snooping-based / Only in directory systems.
- evidence: [S-0038, S-0040]
- topic: hardware/cache-coherence

## Summative (mastery checkpoint)

- Q: Two cores share line L (initially uncached, memory value 0). Step 1: A reads L. Step 2: B reads L. Step 3: A writes 5 to L. Step 4: B writes 7 to L. Step 5: A reads L. Walk the MESI state of L in A and B after each step and give the final value A observes (canonical MESI, write-invalidate).
- bloom: analyze
- bank: summative
- A: After 1: A=E. After 2: A=S, B=S. After 3: A upgrades S→M (B→I). After 4: B's write misses (I), fetches for ownership (A→I, write-back 5), B=M. After 5: A's read misses, fetches from B (B M→S after supplying 7), A=S. A reads 7. SWMR holds throughout; the final ordering is exactly the interleaving A.read, B.read, A.write(5), B.write(7), A.read — serializable.
- distractors: A reads 5 (missed B's write) / A ends in E / both end in M.
- evidence: [S-0040]
- topic: hardware/cache-coherence

- Q: You are designing a 64-core coherent system. Choose the protocol family and justify: broadcast snooping on a shared bus, or a directory-based protocol?
- bloom: apply
- bank: summative
- A: Directory-based. Snooping broadcasts every coherence transaction to all caches over an ordered shared interconnect; with 64 cores the bandwidth and ordering constraints are prohibitive. A directory tracks sharers per line at the home node and sends point-to-point messages only to interested caches, trading a lookup indirection for scalable traffic.
- distractors: Snooping, because it is simpler and directory latency is worse / Snooping, because it preserves a total bus order (already gone at 64 cores) / Either, coherence traffic is identical.
- evidence: [S-0040]
- topic: hardware/cache-coherence

- Q: On an x86 (TSO) machine, cores A and B each execute: store to their own flag; then load the other's flag. Both loads return 0. Is this a coherence failure? Is it allowed? How would you make it behave like SC?
- bloom: evaluate
- bank: summative
- A: Not a coherence failure — SWMR was never violated; each core legitimately observed its own store via store-buffer forwarding before the store became globally visible. It IS allowed under TSO (loads may pass older stores). To obtain SC behavior, insert fences/barriers or use acquire-release synchronization so each store is globally visible before the load.
- distractors: It is a coherence bug and hardware is broken / It is impossible on x86 / It is allowed under SC too.
- evidence: [S-0038, S-0040]
- topic: hardware/cache-coherence

- Q: Two threads each increment their own counter (fields of one struct, adjacent in the same cache line) in a tight loop; the program slows down dramatically vs running alone. Diagnose and fix.
- bloom: analyze
- bank: summative
- A: False sharing: the two counters live in one line, so every increment invalidates the line in the other core's cache, forcing a fetch for ownership and a ping-pong of the whole line — with no word actually shared. Fix: pad/align so each counter owns a full line (or use per-thread structures and merge at the end). This is a performance problem, not a correctness or race problem.
- distractors: It is a data race / the cache is too small / use volatile everywhere / it is unavoidable on any coherent system.
- evidence: [S-0039]
- topic: hardware/cache-coherence

## Review (spaced repetition — interleaved with prerequisites)

- Q: (memory-hierarchy) For a uniprocessor, larger cache blocks usually cut miss rates thanks to spatial locality. Why can larger blocks *hurt* on a coherent multiprocessor?
- bloom: understand
- bank: review
- A: Larger blocks make false sharing more likely: more distinct data objects share a line, so unrelated writes by different cores invalidate each other's copies and force line transfers — Torrellas et al. measured multiprocessor miss rates failing to drop with block size exactly because of this.
- distractors: Larger blocks overflow the tag array / coherence only applies to small blocks / larger blocks reduce invalidations.
- evidence: [S-0039]
- topic: hardware/cache-coherence (interleaves hardware/memory-hierarchy)

- Q: (cpu-pipelining) Modern cores retire stores into a store buffer instead of draining them straight to the cache. Why is the buffer there, and what ordering consequence does store-to-load forwarding create?
- bloom: apply
- bank: review
- A: The store buffer decouples store completion from the pipeline: stores retire without waiting for cache/memory latency. Forwarding lets the issuing core's own loads see the buffered store early, so other cores observe the store only when it drains — the store can effectively be reordered after a later load of a different location (TSO's store-load relaxation).
- distractors: The buffer exists only for power saving / forwarding is optional and usually disabled / it reorders loads before older loads.
- evidence: [S-0040]
- topic: hardware/cache-coherence (interleaves hardware/cpu-pipelining)

- Q: (memory-hierarchy) In a hierarchy with per-core private L1/L2 and a shared last-level cache, where must coherence state be tracked, and why does the shared LLC help directories?
- bloom: remember
- bank: review
- A: Coherence must span every level where a line can be duplicated: private L1/L2 copies across cores. A shared LLC gives a natural filter/serialization point — many "directory" systems track sharing state at the LLC, because lines not in the LLC cannot be in any private cache above it.
- distractors: Coherence only involves L1 / the LLC removes the need for coherence / private caches never hold shared lines.
- evidence: [S-0040]
- topic: hardware/cache-coherence (interleaves hardware/memory-hierarchy)
