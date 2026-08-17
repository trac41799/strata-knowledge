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

# Cache Coherence — teaching

## Learning objectives (Bloom)

- **Understand** — state the coherence problem and the SWMR invariant, and
  explain why private caches alone cannot guarantee fresh reads.
- **Understand** — distinguish coherence (per-location freshness) from memory
  consistency (cross-location ordering), e.g., SC vs TSO vs weak.
- **Apply** — classify a given system as snooping or directory-based and
  predict which wins at a given core count.
- **Analyze** (target) — trace MESI/MOESI state transitions for two cores
  sharing a line and verify the SWMR invariant at every step; diagnose
  false-sharing slowdowns in code.
- **Evaluate** — judge whether an observed interleaving (e.g., TSO store-load
  reorder) is a coherence bug, a consistency-model behavior, or a software
  synchronization error.

## Worked example 1 — MESI trace for two cores sharing a line

Line X, value 0, uncached. Cores A and B, canonical MESI (write-invalidate),
snooping bus. States shown as (A, B).

| Step | Event | (A, B) | Why |
|---|---|---|---|
| 0 | — | (I, I) | nothing cached |
| 1 | A: read X (miss) | (E, I) | fetch; A is sole holder → E |
| 2 | B: read X (miss) | (S, S) | bus snoop: A downgrades E→S, supplies data |
| 3 | A: write 5 (S hit) | (M, I) | A issues upgrade: B invalidated S→I, then A S→M |
| 4 | B: read X (miss) | (S, S) | B fetches; A supplies 5 from M and write-backs → M→S |
| 5 | B: write 7 (S hit) | (I, M) | B upgrades: A invalidated → I; B S→M |

Invariant check at every step: never more than one writer; readers only ever
see the last committed value (A reads 5 after step 3, B reads 5 at step 4,
B writes 7 at step 5). Note step 3: the upgrade must invalidate B *before* A's
write becomes visible, or B could read a stale copy — this is why S→M is not
silent.

## Worked example 2 — false sharing scenario

`struct { int x; int y; } s;` — both fields in one 64-byte line.
Thread 1 loops `s.x++`; thread 2 loops `s.y++`.

- No word is shared: thread 1 never reads or writes `s.y`, thread 2 never
  touches `s.x`.
- Yet every increment of `s.x` invalidates the line in thread 2's cache and
  vice versa: each iteration is a fetch-for-ownership miss, and the line
  ping-pongs between the two caches (true-sharing misses would be zero).
- Torrellas, Lam & Hennessy (1994) measured this class of false-sharing
  misses in real shared-memory workloads: multiprocessor miss rates do not
  show the uniprocessor-style drop when block size grows, because larger
  blocks pack more unrelated data into one line.
- Fix: pad `s` so `x` and `y` sit in different lines (or use per-thread
  objects); the slowdown is a performance artifact, not a race.

## Elaboration prompts

- Why must a snooping interconnect be *ordered* (or why must requests on it
  serialize), while a directory can get away with unordered point-to-point
  messages plus a serialization point at the home node?
- Trace the same two-core sequence under write-*update*: which messages differ,
  and at what traffic cost when 8 cores share the line?
- MOESI's O state turns a "dirty but shared" line into a cache-to-cache
  responder. What message does it eliminate, and when does that help vs hurt?
- x86's TSO lets loads pass older stores; ARM does not even order two stores.
  Given a lock-free algorithm, where would you put fences on each ISA, and why
  does coherence alone not make this unnecessary?
- Why is "the line must be written back before a remote read" true in MESI but
  *not* in MOESI? What does memory's staleness mean for the SWMR invariant?

## Common misconceptions

1. **"Coherence and consistency are the same thing."** Coherence is about one
   location (SWMR invariant, freshness); consistency is about the ordering of
   accesses across many locations. A coherent system can still be non-SC —
   x86 is coherent and TSO. (S-0038, S-0040)
2. **"MESI is one fixed protocol; there is a single MESI."** It is a family:
   textbooks give canonical tables, but implementations differ in upgrade
   transactions, transient states, silent vs explicit evictions, and extend
   the state set — MOESI (Owned, AMD), MESIF (Forward, Intel QPI). (S-0040,
   S-0041)
3. **"x86 gives you sequential consistency."** It gives TSO: loads may be
   reordered before older stores (store-buffer bypass). ARM/POWER are weaker
   still. SC is the abstraction you must *reconstruct* with fences/atomics.
   (S-0038, S-0040)
4. **"False sharing is a race / correctness bug."** No word is shared, so no
   race exists; it is a performance artifact of line granularity, quantified
   empirically (S-0039). It also is *not* fixed by making the protocol
   "smarter" — the invalidation is required by coherence.
5. **"A coherent memory system makes threads safe."** Coherence never
   serializes independent accesses: unsynchronized increments still lose
   updates. Locking/atomics are separate.

## Feynman targets

- Explain to a novice why "each core sees its own latest write" is not enough
  and what SWMR adds. Use the stale-bank-account analogy only if it stays
  accurate about *per-line* guarantees.
- Explain in ≤3 sentences why write-invalidate beats write-update when many
  cores share a hot line — then why it *loses* for a line read by all cores
  and written rarely.
- Explain the one-line difference between MESI and MOESI, and between MOESI
  and MESIF, without using the letters M/E/S/I/O/F as a crutch.
- Explain why TSO's "loads may pass older stores" is exactly what your store
  buffer made inevitable, and why SC therefore forces a fence.

## Interleaving hooks

- **hardware/memory-hierarchy** — block size, miss classification, and why
  multiprocessor miss-rate curves flatten (false sharing); the LLC as
  directory filter. Review items recycle both topics.
- **hardware/cpu-pipelining** — store buffers, speculative loads, and
  memory-disambiguation restarts are pipeline mechanisms whose observable
  consequences are consistency-model rules; a pipelining review question asks
  where buffers sit and what they reorder.
- **systems-software/virtual-memory** (related) — TLB shootdowns are a
  "coherence-like" protocol for the TLB at page granularity: the same
  invalidate-vs-update and serialization reasoning applies one level up.
- **programming-level follow-ups** (recommended for later bands) — atomics
  and memory_order semantics (C++/Rust) are the programmer-facing encoding of
  the TSO/weak distinction, and lock-free algorithms live or die by it.
