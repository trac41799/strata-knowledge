---
id: data/distributed-databases
title: Distributed Databases
band: B5
track: data
tier: T0
bloom_target: apply
prerequisites: [data/transactions-and-isolation, systems-software/distributed-systems-basics]
related: [systems-software/distributed-consensus, data/sql-and-query-optimization, data/indexing-and-storage]
recommended: []
status: draft
schema-version: 1
owner: l1-distributed-databases
reviewed-by: []
updated: 2026-08-18
sources: [S-0018, S-0034, S-0035, S-0128, S-0202, S-0203, S-0204]
---

# Distributed Databases — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — Enumerate the partitioning and replication techniques of distributed databases (hash/range sharding; single-leader, multi-leader, leaderless) and the four subfields of the discipline. (evidence: S-0128, S-0202)
- understand — Explain why 2PC blocks on coordinator failure, and why CAP makes atomic consistency and availability mutually exclusive during a partition. (evidence: S-0203, S-0035)
- apply — Choose a partition key and replication strategy for a given workload, and trace the consistency guarantee of a design under failure. (evidence: S-0128) — **bloom_target**
- analyze — Given a failure trace (coordinator crash, replication lag, partition), identify the violated guarantee and the minimal fix. (evidence: S-0203, S-0128)

## Worked example — a sharding decision trace

Scenario: an event-ticketing platform. Data: `users`, `events`, `tickets` (sold tickets per event), `orders`. Queries: (1) hot path — `INSERT order` + `UPDATE tickets.sold` atomically when someone buys; (2) user dashboard — "my orders", filtered by `user_id`; (3) admin — revenue by event for a date range. Scale target: 10 shards.

1. **Candidate keys.** `user_id` for orders (dashboard-friendly); `event_id` for tickets (single event's ticket count lives on one shard); `date` for revenue analytics.
2. **Trace the atomic hot path.** An order buys 2 tickets for an event. If `orders` is sharded by `user_id` and `tickets` by `event_id`, the insert and the ticket-count update land on two shards → every purchase is a cross-shard transaction → 2PC per purchase, with its blocking and latency costs. **Rejected.**
3. **Colocate the hot path.** Key `tickets` by `event_id` and `orders` by... the order row must include the event's ticket-update in one transaction. Solution: partition `orders` by `event_id` too (an order belongs to one event) — then purchase = single-partition transaction: atomic, no 2PC, fast. Dashboard "my orders" now scans all shards by `user_id` → mitigate with a per-user secondary index (eventually consistent) or a read-side materialization.
4. **Admin analytics.** Date-range revenue must never drive the OLTP shard key (a hot-shard trap: today's events would saturate one shard). Route it to a separate analytics store/warehouse — the classic "operational key for writes, separate pipeline for analytics" split.
5. **Replication.** Each partition replicated 3x (single-leader) for fault tolerance; dashboard reads may go to followers with bounded staleness.

Decision summary: shard key = `event_id` for the transactional path (colocation), analytics externalized, replication for durability. The trace shows the ranking of concerns: **atomicity of the hot path > query locality > analytics convenience**.

## Worked example (mini) — 2PC blocking trace

Coordinator `C`, participants `P1`, `P2`. Timeline: `P1` and `P2` vote yes (they have logged their prepared state and hold locks). `C` crashes before sending Commit. Neither participant may decide alone: `P1` committing could contradict a crash-recovered `C` that later aborts (violating atomicity if `P2` didn't commit); aborting could discard a commit `C` had already decided. Both hold their locks and wait — the transaction blocks until `C` recovers (or an admin intervenes). This is the liveness gap Gray & Lamport formalize: commit requires consensus, and 2PC has no majority mechanism — Paxos Commit (and production systems like Spanner's 2PC-over-Paxos) supply one.

## Elaboration prompts

- Why is the partition key a correctness decision (not just a performance one)? What breaks if a record's key changes after writes? (evidence: S-0128)
- If eventual consistency "converges", why can two banks reconciling a transfer still end up disagreeing with the real world? (evidence: S-0128)
- Spanner chose 2PC over Paxos groups plus TrueTime. Which of the three (2PC, Paxos, TrueTime) buys safety, which buys progress, and which buys ordering? (evidence: S-0204)
- In the worked example, the secondary index for "my orders" is eventually consistent — which query could then return stale data, and is that acceptable for a ticket dashboard but not for the purchase ack? (evidence: S-0128)
- Where does the 2PC blocking hazard actually enter the worked example's rejected design, and why does colocation remove it rather than paper over it? (evidence: S-0203)

## Common misconceptions

1. **"Eventual consistency means the system eventually becomes correct."** It guarantees convergence to a common value, not to a correct value: conflicting writes resolved by last-writer-wins silently discard updates. Convergence is a liveness property of copies; correctness is an application property. (evidence: S-0128)
2. **"CAP says pick any two of three."** Partition tolerance is not a feature you toggle; it is the assumption that partitions happen. During a partition you choose between atomic consistency and availability — before and after it, both hold. (evidence: S-0035)
3. **"Sharding gives unlimited speedup."** Cross-shard queries and transactions become slower and more complex as data spreads; a hot key or a cross-shard join can make a "scaled" system slower than the single node it replaced. (evidence: S-0128)
4. **"2PC guarantees consistency and availability."** 2PC guarantees atomicity among *live* participants; a coordinator failure blocks the transaction. Consensus-based commit fixes progress, not by being cleverer but by adding majority redundancy. (evidence: S-0203)
5. **"NewSQL systems repealed the distributed-systems laws."** They engineer around them: Spanner's external consistency rests on TrueTime's bounded clock uncertainty and Paxos replication — infrastructure costs, not magic. (evidence: S-0204)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why you'd split a database across machines, and why "just add machines" stops working when one query needs data from many of them — grade against the partitioning claims. (evidence: S-0128)
2. Why a store manager deciding "did the sale happen?" cannot answer after the phone line to the coordinator dies — grade against the 2PC-blocking claims. (evidence: S-0203)
3. Why a copy of data "catching up later" is different from "catching up correctly" — grade against the eventual-consistency claims. (evidence: S-0128)

## Interleaving hooks

- **data/transactions-and-isolation (prerequisite):** local commit is a single-node decision; distributed commit replaces it with agreement — revisit isolation levels and ask which ones survive when replicas are involved (R3 in validation.md).
- **systems-software/distributed-systems-basics (prerequisite):** delivery semantics meet replication — an acked-but-lost write is the database instance of at-least-once (R1 in validation.md).
- **systems-software/distributed-consensus (related):** this pack's 2PC story is the practical face of FLP — Raft/Paxos give the majority mechanism 2PC lacks; CAP and FLP are the shared vocabulary (R2 in validation.md).
- **data/sql-and-query-optimization (related):** a distributed query plan is the join-optimization problem with shipping costs — ask how semijoin changes the cost model across sites.
