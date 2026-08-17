---
id: systems-software/distributed-consensus
title: Distributed Consensus
band: B5
track: systems-software
tier: T0
bloom_target: analyze
prerequisites: [systems-software/distributed-systems-basics]
related: [data/distributed-databases, systems-software/networking-basics]
recommended: [data/distributed-databases]
status: published
schema-version: 1
owner: l1-distributed-consensus
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0034, S-0035, S-0036, S-0037, S-0042]
---

# Distributed Consensus — validation

Item anatomy: `Q` · `bloom` · `bank` · `A` · `evidence` · `topic`.

## Formative (practice)

### F1. FLP statement
Q: State the FLP result precisely, including the model it applies to.
bloom: remember
bank: formative
A: In a totally asynchronous system (no bounds on processing speed or message delay), every deterministic consensus protocol has a possible run in which it never terminates (nontermination), even when at most one process fails by crashing. It does not say consensus is unsolvable in synchronous or partially synchronous models.
evidence: [S-0034]
topic: systems-software/distributed-consensus

### F2. Crash vs Byzantine
Q: A replica starts sending conflicting answers to different clients — the same log index answered two ways. Is this within the failure model of Raft? Of PBFT?
bloom: understand
bank: formative
A: No for Raft: Raft assumes servers fail by stopping (crash with recovery); a node behaving arbitrarily is a Byzantine fault outside its guarantees. Yes for PBFT: Byzantine faults are exactly arbitrary behavior, tolerated up to f replicas with 3f+1 total.
evidence: [S-0036][S-0037]
topic: systems-software/distributed-consensus

### F3. Quorum arithmetic
Q: A Raft cluster has 7 servers. How many simultaneous failures can it tolerate, and what is the smallest quorum size?
bloom: apply
bank: formative
A: n = 2f+1 → f = 3 failures tolerated; majority quorum = floor(n/2)+1 = 4 servers. Any two quorums of 4 intersect in at least 4+4-7 = 1 server, which is what keeps safety.
evidence: [S-0036]
topic: systems-software/distributed-consensus

### F4. CAP scenario analysis
Q: A partition splits a 2-node service into {A} and {B}. A client writes v1 to A (available side). Another client reads from B. The system answers the read with v0 (stale). Which CAP property is violated and which is preserved? Could the system answer both sides' requests with atomic consistency?
bloom: analyze
bank: formative
A: Atomic consistency (linearizability) is violated — the read from B does not reflect v1; availability is preserved (both requests got responses). No: with an assumed partition, atomic consistency and availability cannot both hold for the two nodes — this is exactly the CAP impossibility (asynchronous model).
evidence: [S-0035]
topic: systems-software/distributed-consensus

### F5. Raft election analysis
Q: A 5-node Raft cluster loses its leader. Two followers become candidates in the same term; each receives exactly 2 votes. A third follower also times out and becomes a candidate in that same term, receiving only its own vote. No candidate has a majority. What happens, and what mechanism resolves it?
bloom: analyze
bank: formative
A: No candidate has a majority → no leader this term; the term ends with no election result. Resolution: randomized election timeouts make the next candidate-triggering timeout differ across servers, so in the next term one candidate is likely to time out first and win the majority before rivals begin. Without randomization, split votes could repeat forever (a liveness failure — see FLP).
evidence: [S-0036][S-0034]
topic: systems-software/distributed-consensus

## Summative (mastery checkpoint)

### S1. Commit under leader change
Q: Leader L (term 5) appends entry "set x=1" at index 7 and receives AppendEntries success from 3 of 5 servers, then crashes before sending the commit notification. A new leader L' is elected in term 6. Is the entry committed? Can L' possibly lack the entry — and what mechanism guarantees the answer?
bloom: analyze
bank: summative
A: The entry is committed: the commit rule is a majority of servers having stored the entry (3/5 did), not the leader's announcement. L' cannot lack it: any majority quorum that elects L' must intersect the 3 storing servers (quorum intersection), and the election restriction — a voter grants its vote only to a candidate whose log is at least as up-to-date — forces L' to contain every committed entry. This is Leader Completeness: once a leader commits an entry, all future leaders have it, so committed entries are never lost or overwritten.
evidence: [S-0036]
topic: systems-software/distributed-consensus

### S2. Protocol choice for hostile actors
Q: You must build a replicated ledger where some operators' machines are assumed potentially compromised and may send forged messages. Choose between Raft and PBFT and justify with failure-model and replica-count reasoning.
bloom: evaluate
bank: summative
A: PBFT: Raft assumes fail-stop behavior and is unsafe under Byzantine behavior — one malicious node can violate state-machine safety. PBFT tolerates f Byzantine replicas with 3f+1 total (e.g., 4 replicas for f=1) and uses pre-prepare/prepare/commit with message authentication so replicas cannot equivocate undetected. Cost: higher message complexity and replica count versus Raft's 2f+1.
evidence: [S-0037][S-0036]
topic: systems-software/distributed-consensus

### S3. FLP/CAP relationship
Q: Both FLP and CAP are impossibilities in an asynchronous model, yet Raft and databases work in practice. Explain in one paragraph how practice reconciles these theorems.
bloom: understand
bank: summative
A: Both theorems assume a fully asynchronous model (unbounded delays, message loss allowed). Practical systems relax the model: Raft assumes eventual synchrony — liveness requires a majority able to communicate within election timeouts, while safety holds always; CAP's tradeoff is only forced during an actual partition, where systems choose consistency or availability, and is not forced otherwise. Neither theorem forbids the properties a well-chosen, partially synchronous system actually provides.
evidence: [S-0034][S-0035][S-0036]
topic: systems-software/distributed-consensus

## Review (spaced repetition — interleaved with prerequisites)

### R1. Partial failure and retries (from distributed-systems-basics)
Q: In a distributed system, a client retries a request after a timeout because the server may have crashed or the reply may have been lost. Why does an at-most-once vs exactly-once distinction matter when the operation is "append a log entry"? (Relate to Raft's handling.)
bloom: understand
bank: review
A: A retried append may execute twice unless operations are idempotent or deduplicated; exactly-once semantics are impossible without distinguishing first execution from re-execution. Raft solves this by making each log entry unique (index + term): a retried AppendEntries for an already-stored entry is idempotent, so reordering and duplication are absorbed — a property the Raft safety argument explicitly assumes.
evidence: [S-0036]
topic: systems-software/distributed-consensus

### R2. Liveness under permanent partition
Q: A 5-node Raft cluster is split 2/3 by a permanent partition; the side of 3 elects a leader and serves writes. The side of 2 elects its own leader in a later term. What fails — safety or liveness — and what is the CAP-flavored name for the side of 2's behavior?
bloom: analyze
bank: review
A: Safety holds: the side of 2 cannot commit anything (no majority), and if it ever reconnects, its higher-term leader will step down or be overwritten — the logs converge. Liveness fails for clients on the minority side: they cannot make progress (writes stall). Under CAP language, the cluster is "CP": during the partition it chooses consistency over availability on the minority side.
evidence: [S-0036][S-0035]
topic: systems-software/distributed-consensus

### R3. PBFT replica math
Q: A PBFT system must tolerate 2 Byzantine failures. How many replicas are required, and how many must be non-faulty? Contrast with the Raft requirement for the same tolerance.
bloom: apply
bank: review
A: n = 3f + 1 = 7 replicas (5 non-faulty), because Byzantine replicas may actively mislead and quorums must still intersect on honest behavior. Raft needs only 2f+1 = 5 for 2 crashes, because a stopped node cannot lie. The 3f+1 vs 2f+1 gap is the price of assuming arbitrary behavior.
evidence: [S-0037][S-0036]
topic: systems-software/distributed-consensus
