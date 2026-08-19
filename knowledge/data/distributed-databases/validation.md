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
status: published
schema-version: 1
owner: l1-distributed-databases
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0018, S-0034, S-0035, S-0128, S-0202, S-0203, S-0204]
---

# Distributed Databases — validation

Item anatomy: `- Q:` `- bloom:` `- bank:` `- A:` `- evidence:` `- topic:`.

## Formative (practice)

### F1. Replication topology recall
- Q: Name the three replication topologies and, for each, one consistency-relevant property a designer must manage.
- bloom: remember
- bank: formative
- A: (1) Single-leader — all writes go to one node; failover must handle the acknowledged-but-not-replicated window. (2) Multi-leader — several nodes accept writes; conflicts between leaders must be resolved. (3) Leaderless/quorum — reads and writes hit multiple nodes; quorum intersection (W + R > N) controls how fresh reads are.
- evidence: [S-0128]
- topic: data/distributed-databases

### F2. Hash vs range partitioning
- Q: Explain why a hash-partitioned table cannot serve an efficient range scan over a date column, and what failure mode range partitioning instead risks.
- bloom: understand
- bank: formative
- A: Hash partitioning scatters adjacent keys across shards (each shard sees a pseudo-random subset), so a range scan must visit every shard; range partitioning keeps keys ordered within one shard, enabling scans, but if the workload concentrates on recent dates all writes hit one "hot" shard.
- evidence: [S-0128]
- topic: data/distributed-databases

### F3. Partition-key selection (design exercise)
- Q: A ride-hailing app stores trips. Analytics queries aggregate by day (range over `completed_at`); the hot path reads/writes a single trip by `trip_id`. Propose a partition key and state what each query pattern then costs.
- bloom: apply
- bank: formative
- A: Partition by `trip_id` (hash): single-trip reads and writes hit exactly one shard with no coordination, but day-range analytics must scan all shards — acceptable if analytics run on an export/warehouse or a secondary index. Partitioning by `completed_at` (range) makes analytics cheap but concentrates daily writes on one shard. For a write-heavy OLTP system, `trip_id` is the defensible primary choice; analytics gets its own path.
- evidence: [S-0128]
- topic: data/distributed-databases

### F4. 2PC failure trace
- Q: A distributed transaction uses 2PC. All participants vote "yes"; the coordinator then crashes before sending Commit. What happens to the participants, and why is this a liveness rather than a safety problem?
- bloom: understand
- bank: formative
- A: Each participant that voted yes cannot decide alone: aborting could contradict a commit the coordinator had decided, and committing alone could violate atomicity if the coordinator aborts — so they hold locks and wait for the coordinator to recover (blocking). Safety (agreement) is preserved; liveness (progress) is lost, which is why Gray & Lamport tie non-blocking commit to consensus.
- evidence: [S-0203]
- topic: data/distributed-databases

## Summative (mastery checkpoint)

### S1. Replicated counter with read replicas
- Q: A single-leader system with three async read replicas serves a global counter. A client increments, receives the leader's ack, then reads from a random replica and sees the old value. Classify the guarantee, state whether the ack was a lie, and give the design options that close the gap.
- bloom: analyze
- bank: summative
- A: The system offers eventual consistency: the ack only guarantees the write is on the leader, not on any replica. The ack is not a lie — it promised durability on the leader, not linearizability — but a client that reads after an ack can legitimately see stale data. Options: read from the leader, read from a quorum (W + R > N), replicate synchronously before acking, or version reads; each trades latency or availability.
- evidence: [S-0128]
- topic: data/distributed-databases

### S2. CAP configuration under a partition
- Q: A payment system spans two datacenters that lose connectivity. For each choice — (a) reject writes in the disconnected region until the link returns, (b) accept writes in both regions and reconcile later — state which CAP property is kept, which is dropped, and the concrete correctness risk.
- bloom: apply
- bank: summative
- A: (a) keeps atomic consistency and drops availability: the disconnected region refuses service during the partition. (b) keeps availability and drops atomic consistency: both regions accept writes, so concurrent updates can diverge and must be reconciled — with non-mergeable data (e.g., a balance), reconciliation means lost or double-counted updates (eventual convergence, not eventual correctness).
- evidence: [S-0035]
- topic: data/distributed-databases

### S3. Distributed transaction design
- Q: An order workflow writes an `orders` row (shard by `customer_id`) and decrements `inventory` (shard by `product_id`) — two shards. Enumerate the design options for atomicity, and identify the one that avoids the 2PC blocking hazard entirely.
- bloom: apply
- bank: summative
- A: (a) Run 2PC across the two shards — atomic but blocking on coordinator failure. (b) Run 2PC over consensus-replicated groups (Spanner-style) — atomic and non-blocking, at infrastructure cost. (c) Change the data model: store inventory reservation inside the order document or colocate by product/customer — single-partition transaction, no coordination. (d) Drop atomicity: place an order and decrement with a compensating flow. (c) eliminates the hazard; (b) removes it; (d) accepts it.
- evidence: [S-0203][S-0204]
- topic: data/distributed-databases

## Review (spaced repetition — interleaved with prerequisites)

### R1. Delivery semantics meets replication (from distributed-systems-basics)
- Q: A client sends an increment to a single-leader replicated counter; the leader applies it, acknowledges, then crashes before replicating. A follower is promoted. What does the client observe, and which consistency/durability guarantee was violated?
- bloom: analyze
- bank: review
- A: The client observes the increment disappear: the new leader's state predates the acknowledged write. The acknowledged write was never durably replicated — the ack overpromised. Fixes: replicate to a quorum (or synchronously to a follower) before acknowledging, or accept and reconcile.
- evidence: [S-0128]
- topic: systems-software/distributed-systems-basics

### R2. Quorum intersection (from distributed-consensus)
- Q: With N = 5 replicas and write quorum 3, why does a read quorum of 3 suffice to see the latest acknowledged write, and what happens with W = 2, R = 2?
- bloom: understand
- bank: review
- A: Any read quorum of 3 intersects any write quorum of 3 in at least one replica carrying the latest write (pigeonhole: 3 + 3 > 5). With W = R = 2, quorums can miss each other, so a read may return stale data unless reads use versioning and repair.
- evidence: [S-0036]
- topic: systems-software/distributed-consensus

### R3. Local vs distributed atomicity (from transactions-and-isolation)
- Q: In a single-node DBMS, one component decides whether a transaction commits. What changes when the same transaction touches two nodes, and which single-node concept does the commit protocol replace?
- bloom: understand
- bank: review
- A: Atomicity in one node is a local decision: the DBMS logs and either commits or aborts as one unit. Across nodes, the participants must reach agreement on commit/abort despite failures — that is the distributed commit problem, and the commit protocol (e.g., 2PC) is the distributed replacement for the local commit decision. This is why Gray & Lamport formalize commit as a consensus problem: no single node's knowledge suffices.
- evidence: [S-0203]
- topic: data/distributed-databases
