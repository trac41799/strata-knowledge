---
id: systems-software/distributed-consensus
title: Distributed Consensus
band: B5
track: systems-software
tier: T1
bloom_target: analyze
prerequisites: [systems-software/distributed-systems-basics]
related: [data/distributed-databases, systems-software/networking-basics]
recommended: [data/distributed-databases]
status: draft
schema-version: 1
owner: l1-distributed-consensus
reviewed-by: []
updated: 2026-08-18
sources: [S-0034, S-0035, S-0036, S-0037]
---

# Distributed Consensus — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- remember — State the FLP theorem, the CAP theorem, and the failure models (crash vs Byzantine) with their originating papers. (evidence: S-0034, S-0035)
- understand — Explain why FLP and CAP are impossibilities of the *asynchronous* model and how partially synchronous assumptions (Raft) or relaxed requirements escape them. (evidence: S-0034, S-0035, S-0036)
- apply — Compute quorum sizes and failure tolerances (2f+1 for Raft/Paxos, 3f+1 for PBFT). (evidence: S-0036, S-0037)
- analyze — Given a partition, timeout, or leader-change scenario, identify which property (agreement, termination, consistency, availability, liveness) is violated or preserved and why. (evidence: S-0034, S-0035, S-0036) — **bloom_target**
- evaluate — Choose between crash-tolerant (Raft/Paxos) and Byzantine-tolerant (PBFT) designs given a threat model and replica budget. (evidence: S-0036, S-0037)

## Worked example

### Part A — A Raft election and log commit, step by step

Cluster: 5 servers, A–E. A is leader in term 4. Timeline (times are illustrative):

1. **Heartbeat failure.** A's network cable is cut; B–E receive nothing within their election timeouts. B's timeout (say 250 ms) fires first.
2. **Term increment & candidacy.** B increments its term to 5, sets itself candidate, votes for itself, and sends RequestVote to C, D, E with its last log index/term. C, D, E are still in term 4, so the term-5 request bumps them to term 5 before they respond.
3. **Votes.** Each server votes for the *first* candidate whose log is at least as up-to-date as its own, once per term. C, D, E all have logs as old as B's, so they vote yes. B now has 3 of 5 votes — a majority — and becomes leader of term 5. (Had C timed out first, C might have won instead; randomized timeouts make such ties rare.)
4. **Log replication.** A client sends `set x = 1`. B appends it at index 7, term 5, and sends AppendEntries to all followers. C, D, E append it and reply. Majority stored → index 7 is **committed**. B applies `x = 1` to its state machine and replies to the client; followers apply it when the next heartbeat carries the commit index.
5. **Failure during commitment.** Suppose B instead crashed right after the 3 acknowledgements, before notifying anyone. Index 7 is still committed (majority stored). In term 6, D is elected. D must contain index 7 (Leader Completeness): the majority that elected D intersects the 3 servers that stored the entry, and D's log was at least as up-to-date as the voters'. The commit is never lost — this is safety under crash, the property FLP says cannot be *guaranteed to terminate* in pure asynchrony, but that Raft guarantees *conditionally*: liveness holds because a majority can communicate within timeouts (eventual synchrony).

Key mental model: **commit = majority stored, not leader's word; safety = quorum intersection + election restriction; liveness = majority communication within timeouts.**

### Part B — Analyze a CAP scenario

A shopping cart service runs on nodes X and Y in an asynchronous network. A partition drops all traffic between X and Y for 30 seconds. During the partition: client writes to X ("cart item added"); another client reads from Y ("cart is empty").

Analysis:

1. **Which property failed?** Atomic consistency: the read at Y is stale relative to the write at X; operations cannot be ordered as if at a single instant. Availability held: both requests received responses.
2. **Could the system have done better?** With a *total* partition, no protocol can offer both atomic consistency and availability — Gilbert & Lynch proved this for the asynchronous model. The design choice is which side to sacrifice:
   - **CP choice:** Y refuses reads while partitioned (returns an error) → consistency preserved, availability lost on Y.
   - **AP choice:** Y serves stale reads → availability preserved, consistency relaxed.
3. **After the partition heals.** CP systems (e.g., Raft-based) reconcile via the quorum: Y is not a majority by itself, so X's side keeps committing and Y catches up. AP systems (e.g., leaderless/eventually consistent) merge or resolve conflicts later.
4. **Scope check.** The theorem assumes atomic consistency and unbounded response time. A system offering session or causal consistency, or bounding response time in a partially synchronous model, lives outside the theorem's scope — which is why "pick 2 of 3" is a folk reading, not the theorem.

## Elaboration prompts

- Why does FLP not apply to Raft? Walk through which FLP assumption (unbounded delays) Raft relaxes, and which guarantee (termination) becomes conditional. (evidence: S-0034, S-0036)
- Why must a Byzantine quorum be larger (3f+1) than a crash quorum (2f+1)? What would go wrong with 2f+1 under a lying replica? (evidence: S-0037)
- Why is "the leader's log is the truth" insufficient by itself — what role do the *other* replicas play in both electing the leader and confirming commits? (evidence: S-0036)
- The CAP theorem and FLP both arise from asynchrony. Where do their models differ (message loss vs delay; crash vs partition) and what does each forbid? (evidence: S-0034, S-0035)
- If a Raft cluster is partitioned 2/3 and the 2-side elects a leader with a *higher term*, why is that safe even though it sounds like a second authority? (evidence: S-0036)

## Common misconceptions

1. **"Consensus is impossible, so distributed systems can't be consistent."** Wrong scope: FLP says *deterministic* consensus cannot *guarantee termination* in a *totally asynchronous* system with one crash — it is a liveness result, and it explicitly allows solutions in synchronous/partially synchronous models (the paper names the synchronous case). Raft's safety holds always; its liveness needs only a communicating majority. (evidence: S-0034, S-0036)
2. **"CAP means you permanently pick any 2 of 3."** The theorem is about what happens *during a partition*: availability and atomic consistency cannot both hold *while* the partition exists, in an asynchronous model. With no partition both hold; partition tolerance is an assumption about the environment, not a knob. (evidence: S-0035)
3. **"Raft/Paxos tolerate any minority failure, including malicious ones."** They tolerate *crash* (fail-stop) failures — servers assumed to fail by stopping, possibly recovering. A single Byzantine node can break state-machine safety. Byzantine tolerance (PBFT) needs 3f+1 replicas and message authentication. (evidence: S-0036, S-0037)
4. **"The leader commits when it writes to its own log / when it says so."** Commitment requires a *majority* of servers to have stored the entry. A leader crashing after local append but before majority replication can have its entry overwritten by a new leader — the reason quorum intersection exists. (evidence: S-0036)
5. **"More replicas always improve availability."** Under crash faults, availability comes from the majority property, not sheer count; under partitions, adding replicas changes *which* side can form a majority, and a misconfigured quorum (e.g., 2/2 split) can lose liveness entirely. The guarantee is "any majority can communicate," which is a connectivity statement, not a count statement. (evidence: S-0036)

## Feynman targets

Explain to a novice, out loud or in writing, without jargon:

1. Why 3 machines can agree on a value even if 1 of them is dead — using "majority" and "quorum intersection" in plain words. Grade against the quorum and commit claims. (evidence: S-0036)
2. Why a network split forces a choice between "everyone gets an answer" and "everyone sees the same answer" — and why that choice disappears when the split heals. Grade against the CAP claims. (evidence: S-0035)
3. Why a lying member is a different problem than a dead member, and why you need 4 members to outvote 1 liar but only 3 to outvote... (a crash is silent, so 3 of 5 for 2 crashes; a liar must be outvoted *and* cannot be trusted in the count) — grade against the failure-model claims. (evidence: S-0037)

## Interleaving hooks

- **systems-software/distributed-systems-basics (prerequisite):** rehearse partial failure, timeouts, and retries — the vocabulary consensus systems are built on (F1, R1 in validation.md).
- **systems-software/networking-basics (related):** message loss, duplication, and reordering are assumed away in FLP's model but explicitly handled by Raft's safety argument — map each network hazard to the Raft property that absorbs it.
- **data/distributed-databases (recommended):** linearizability (CAP's consistency) vs isolation levels; where a Raft-ordered log sits under a transaction engine. Revisit after consensus is mastered.
- **programming/concurrency-primitives (prerequisite chain):** compare single-node mutual exclusion with multi-node consensus — what changes when the shared memory becomes message passing.
- **cs-foundations/logic-and-proof (cross-track):** FLP and CAP are proofs by construction (bivalent configurations; two-node partition argument) — practice reconstructing the proof skeleton as retrieval practice.
