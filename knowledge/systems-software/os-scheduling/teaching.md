---
id: systems-software/os-scheduling
title: OS Scheduling
band: B2
track: systems-software
tier: T0
bloom_target: apply
prerequisites: [systems-software/os-processes]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-os-scheduling
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0032, S-0018, S-0117, S-0118, S-0119]
---

# OS Scheduling — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **apply** — simulate FIFO, SJF, SRTF, and round-robin on a workload with arrival and service times, and compute average waiting time for each ([S-0032]).
- **apply** — check EDF schedulability of a periodic task set via the utilization condition, and contrast the rate-monotonic bound ([S-0118]).
- **understand** — explain preemption, starvation, and aging, and the quantum trade-off in round-robin.
- **understand** — state precisely what SJF/SRTF optimality says (and does not say) about scheduling ([S-0117], [S-0119]).
- **analyze** — explain why MLFQ parameters are workload-dependent engineering choices, and diagnose starvation in priority schedulers.
- **understand** — describe the Linux CFS as a practice-level fair-scheduling design (virtual runtime, smallest-vruntime-wins) rather than an optimal-policy claim ([S-0032]).

## Worked example 1 — scheduling simulation (arrival/service times)

Workload: A(0,7), B(1,4), C(2,9), D(3,2) — (arrival, service). Waiting time = completion − arrival − service.

**FIFO** (arrival order): completions A=7, B=11, C=20, D=22 → waits 0, 6, 9, 17 → **avg 8**.

**SJF** (non-preemptive; at each completion pick the shortest arrived): A (only job) 0–7; then D 7–9, B 9–13, C 13–22 → waits 0, 8 (B), 11 (C), 4 (D) → **avg 5.75**.

**SRTF** (preemptive; at each arrival, run the job with the least remaining):
- t=0: A runs. t=1: B(4) < A(6 remaining) → preempt, B runs. t=2: C arrives, B(3) < C(9) → continue. t=3: D(2) < B(3) → preempt, D runs.
- t=5: D done. B runs 5–8 (done). A runs 8–14 (done). C runs 14–23 (done).
- Waits: A 7, B 3, C 12, D 0 → **avg 5.5**.

**Round-robin q=4**: A 0–4 (rem 3); B 4–8 (done); C 8–12 (rem 5); D 12–14 (done); A 14–17 (done); C 17–22 (done). Waits: A 10, B 3, C 11, D 9 → **avg 8.25**.

Result: SRTF 5.5 < SJF 5.75 < FIFO 8 < RR 8.25. Two lessons: (1) shortest-first really minimizes average waiting time — the numeric pattern behind Smith's and Schrage's proofs ([S-0117], [S-0119]); (2) SJF/SRTF require knowing service times, which is why real OSes use RR/MLFQ-style policies instead — fairness and responsiveness, not provable minimum wait ([S-0032]).

## Worked example 2 — EDF vs rate-monotonic

Three periodic tasks on one preemptive CPU, deadline = period: T1(C=1,T=4), T2(C=2,T=6), T3(C=3,T=8).

- Utilization: U = 0.25 + 0.333 + 0.375 = **0.958 ≤ 1** → EDF schedules all deadlines (optimality: if any schedule works, EDF does) ([S-0118]).
- RM bound for n=3: 3(2^(1/3) − 1) ≈ **0.78** < 0.958 → RM's guarantee does NOT cover this set; RM might still meet every deadline, but the fixed-priority guarantee is weaker than EDF's ([S-0118]).

Moral: EDF extracts all schedulable capacity (U ≤ 1) but must be re-evaluated when tasks block on shared resources or the model changes; RM offers a cheap, static-priority check with a conservative bound.

## Elaboration prompts

- Why is SJF "optimal" in textbooks but absent from real OSes? What assumption breaks in practice ([S-0117])?
- Round-robin with q→∞ is FCFS and q→0 is pure context-switch overhead: where is the sweet spot, and what workload properties does it depend on ([S-0032])?
- Why does MLFQ need a periodic boost even though it already has multiple priorities? (Hint: it cannot distinguish "long job" from "starved job" without one.)
- EDF is optimal in Liu & Layland's model — which of these assumptions (preemption, uniprocessor, independent tasks, deadline = period) does a video-streaming pipeline violate, and what breaks ([S-0118])?
- CFS "always runs the smallest vruntime" looks like round-robin with finer granularity — what does the red-black tree buy over a simple queue ([S-0032])?

## Common misconceptions

1. **"SJF is optimal, period."** It minimizes AVERAGE waiting time only (given known service times, no release surprises). A long job can starve; worst-case response can be terrible; other metrics are untouched by the theorem ([S-0117]).
2. **"Preemptive scheduling is always better."** Preemption buys responsiveness at the cost of context switches and (for SRTF/EDF) the need for accurate timing information; non-preemptive FCFS is still the right default for batch pipelines where jobs must run to completion.
3. **"A smaller quantum is always better."** Below the context-switch overhead threshold, the CPU spends more time switching than working; the quantum must be large relative to switch cost ([S-0032]).
4. **"EDF is optimal everywhere, so use it."** The optimality proof assumes preemptive uniprocessor, independent tasks, deadline = period; overloaded systems make EDF miss many deadlines, and shared resources (priority inversion) break its assumptions ([S-0118]).
5. **"Starvation only happens with malicious workloads."** It is a structural property of pure priority schemes: any continuous stream of higher-priority arrivals starves the lower classes; aging exists precisely because this happens in practice ([S-0032]).
6. **"CFS is provably fair."** CFS approximates an ideal CPU fairly in practice (vruntime balancing), but it is an engineering design with tunable granularity — not a mathematically optimal policy like SJF/EDF in their models.

## Feynman targets

- "Explain to a junior engineer why a 'provably optimal' scheduler (SJF) is not what Linux runs, without mentioning starvation twice in the same sentence."
- "Explain round-robin's quantum trade-off to a product manager: why not make the time slice 1 nanosecond."
- "Explain EDF with the metaphor of deadlines in a kitchen: why does cooking the soonest-expiring dish first beat any other plan, and when does that stop being true?"
- "Explain the difference between 'optimal for average waiting time' and 'best' to someone who just learned the word optimal."

## Interleaving hooks

- **systems-software/os-processes** — context switch is the mechanism the scheduler pays for; every preemption is a switch; the ready queue holds processes in the ready state.
- **systems-software/virtual-memory** — demand paging and scheduling interact: an I/O-bound pattern can be paging-heavy, and page faults change burst structure; scheduler time is measured against fault latency.
- **hardware/isa-basics** — the timer interrupt is the ISA/hardware event that makes preemption possible; without a clock device, only voluntary (non-preemptive) scheduling exists.
- **cs-foundations/algorithms** — CFS's red-black tree is a balanced BST keyed by vruntime; SJF's greedy choice is provably optimal on a single machine, the rare case where greedy is exactly right.
- **cs-foundations/computability** — (optional stretch) EDF's feasibility test is polynomial (U ≤ 1) for the Liu-Layland model, while multiprocessor real-time feasibility is NP-hard — scheduling theory lives at the boundary of tractability.
