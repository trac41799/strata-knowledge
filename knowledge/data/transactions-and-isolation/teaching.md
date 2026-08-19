---
id: data/transactions-and-isolation
title: Transactions & Isolation
band: B4
track: data
tier: T0
bloom_target: apply
prerequisites: [data/relational-model]
related: [systems-software/distributed-consensus, data/distributed-databases]
recommended: []
status: draft
schema-version: 1
owner: l1-transactions-and-isolation
reviewed-by: []
updated: 2026-08-18
sources: [S-0192, S-0193, S-0194, S-0199, S-0203, S-0034]
---

# Transactions & Isolation — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — Enumerate the four SQL isolation levels, the phenomena P1–P3, and the ACID properties. (evidence: S-0194)
- understand — Explain the two-phase locking theorem, why snapshot isolation permits write skew, and why 2PC blocks on coordinator failure. (evidence: S-0192, S-0199, S-0203)
- apply — Choose an isolation level and concurrency-control mechanism for a given workload, and trace schedules to classify the anomalies each level admits. (evidence: S-0194, S-0199) — **bloom_target**
- analyze — Given a failure or interleaving trace (dirty read, lost update, write skew, coordinator crash), identify the violated guarantee and the minimal fix. (evidence: S-0199, S-0203)

## Worked example — the transfer under four lenses

Setup: accounts A = 500, B = 500. T1 checks the invariant "A + B = 1000". T2 transfers 100 from A to B (writes A = 400, B = 600).

**Lens 1 — READ UNCOMMITTED: dirty read.** T1 reads A = 500. T2 writes A = 400 (uncommitted). T1 reads A again — sees 400, sums 900. T2 aborts, so the true state is A + B = 1000. T1 acted on a value that never existed: it read a dirty write. READ COMMITTED (P1 excluded) fixes exactly this.

**Lens 2 — READ COMMITTED: non-repeatable read.** T1 reads A = 500. T2 writes A = 400 and commits. T1 re-reads A = 400. No dirty read occurred, but T1's two reads disagree: P2. REPEATABLE READ excludes P2 by holding read locks to transaction end.

**Lens 3 — REPEATABLE READ: phantom.** T1 counts open orders → 100. T2 inserts an open order and commits. T1 re-runs the count → 101. Row locks cannot lock the not-yet-inserted row, so the result set changed: P3. Only SERIALIZABLE (range/predicate locks) excludes P3.

**Lens 4 — SERIALIZABLE vs snapshot isolation: write skew.** Two doctors; invariant "at least one on call". T1 reads both flags (1, 1), sets A off-call. T2 reads both flags (1, 1), sets B off-call. Both commit. Under snapshot isolation neither write conflicts (disjoint rows), so MVCC approves both — nobody is on call. No serial execution produces that outcome, so the schedule is not serializable: SI hides the conflict behind snapshot reads. True serializability (or explicit `SELECT ... FOR UPDATE`) would serialize the two checks.

Trace summary: each lens is a *different anomaly with a different minimal guarantee* — the exercise of choosing an isolation level is precisely choosing which of these traces your application can survive.

## Worked example (mini) — 2PC blocking trace

Coordinator C, participants P1, P2. Both vote yes (each logged its prepared state and holds locks). C crashes before sending Commit. P1 cannot commit alone (P2 might abort, breaking atomicity) and cannot abort alone (C might have decided commit). P1 and P2 block until C recovers. Safety is intact; liveness is gone. This is why Gray & Lamport model commit as consensus and why non-blocking commit needs majority-based protocols (Paxos Commit) — 2PC has no majority mechanism.

## Elaboration prompts

- Why is "we run READ COMMITTED" a correctness decision rather than a performance preference — which trace above does it buy, and which does it sell? (evidence: S-0194)
- The 2PL theorem requires locks held until all are acquired. Where exactly does the proof break if a transaction releases one lock mid-way — what schedule becomes possible? (evidence: S-0192)
- Snapshot isolation prevents P1–P3 for read-only transactions; write skew still slips through. What is structurally different about write skew that version-based conflict checking misses? (evidence: S-0199)
- In the dirty-read lens, T1 read A twice and got two different answers. Would a single read of A have been safe? What does that say about "reads are harmless"? (evidence: S-0194)
- 2PC blocks because one coordinator is a single point of failure. Is the problem really the coordinator, or the absence of a majority decision — and what does Paxos Commit change? (evidence: S-0203)

## Common misconceptions

1. **"The default isolation level is a fine isolation decision."** The default is not standardized: systems ship different defaults (commonly READ COMMITTED or REPEATABLE READ). "We use the default" never names the anomalies the workload accepts. (evidence: S-0194)
2. **"Lower isolation levels just make things faster."** They permit named wrong answers: READ COMMITTED admits non-repeatable reads and phantoms, and lost update is outside the SQL taxonomy entirely — a level choice is a correctness contract. (evidence: S-0194)
3. **"MVCC makes the database safe from anomalies."** Snapshot isolation prevents dirty reads and gives consistent snapshots, but write skew and serialization anomalies remain; serializability must be argued, not assumed from the mechanism. (evidence: S-0199)
4. **"2PC gives distributed transactions single-node strength."** It gives atomicity among live participants; a coordinator crash blocks everyone, and isolation across nodes still needs distributed coordination. (evidence: S-0203)
5. **"Read-only transactions are immune to isolation problems."** They are not: a read-only transaction under READ COMMITTED still sees non-repeatable reads; isolation constrains what any transaction can observe. (evidence: S-0194)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why "the bank either does the whole transfer or nothing, even if the power dies" is a promise the database keeps with a log — grade against the atomicity/durability claims. (evidence: S-0193)
2. Why two people updating the same account balance can lose each other's update, and what "levels" of seeing-other-people's-work mean for a shared spreadsheet — grade against the P1–P3 claims. (evidence: S-0194)
3. Why a store manager cannot decide whether the sale happened after the phone line to the coordinator dies — grade against the 2PC blocking claims. (evidence: S-0203)

## Interleaving hooks

- **data/relational-model (prerequisite):** keys and declared constraints are what make "consistency" checkable at all — review bank items R1/R2 exercise exactly this boundary.
- **systems-software/distributed-consensus (related):** 2PC's blocking behavior is the practical face of FLP; "commit as consensus" (S-0203) is the bridge between this pack and consensus theory.
- **data/distributed-databases (related):** this pack's 2PC story is the mechanism distributed databases run on sharded systems — revisit it when tracing cross-shard atomicity.
- **data/indexing-and-storage (sibling):** MVCC keeps old versions around, so storage structures must index version chains — ask how a B+ tree page layout would store multiple versions of one row.
