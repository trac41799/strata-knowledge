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

# OS Scheduling

## Claims

### Scheduling model & preemption

- The scheduler decides which ready process runs next; a preemptive scheduler may take the CPU from a running process (typically on a timer interrupt) and return it to the ready queue, whereas a non-preemptive scheduler switches only when the running process blocks or exits. [T3][S-0032]
- Common scheduling metrics are CPU utilization, throughput, turnaround time, waiting time, and response time; average waiting time and response time are the usual user-visible targets. [T3][S-0032]
- CPU scheduling and dispatch are core content of the Operating Systems knowledge area of CS2023. [T2][S-0018]
- CPU-bound processes run long CPU bursts with little I/O; I/O-bound processes have short bursts between I/O operations; real processes mix both, and schedulers that favor I/O-bound processes (short bursts) improve interactive responsiveness. [T3][S-0032]

### Algorithms

- FCFS (FIFO) runs processes in arrival order and is non-preemptive; its convoy effect — short jobs queueing behind a long job — inflates average waiting time. [T3][S-0032]
- SJF (shortest job first) runs the shortest available job; on a single machine, sequencing jobs by non-decreasing processing time (the SPT rule) minimizes mean flow time and therefore average waiting time — Smith's theorem, established by an interchange argument. [T0][S-0117]
- SRTF (preemptive SJF) runs the job with the least remaining processing time; when preemption is allowed, this shortest-remaining-time discipline is optimal for average waiting time (Schrage's proof). [T0][S-0119]
- Round-robin (RR) cycles ready processes with a fixed quantum q: it bounds response time and is fair at coarse timescales, but q is a trade-off — large q degenerates toward FCFS and tiny q multiplies context-switch overhead. [T3][S-0032]
- Multilevel feedback queues (MLFQ) keep several ready queues with different priorities and quanta and migrate processes between queues based on observed behavior (e.g., boosting I/O-bound processes), providing responsiveness without knowing future CPU bursts. [T3][S-0032]

### Starvation

- Priority scheduling (including naive SJF and MLFQ) can starve low-priority or long processes indefinitely when higher-priority work keeps arriving; aging — progressively raising the priority of waiting processes — is the standard remedy. [T3][S-0032]

### Real-time scheduling

- In Liu and Layland's model (preemptive uniprocessor, independent periodic tasks, deadline equal to period), EDF (earliest deadline first) is optimal: if any schedule meets all deadlines, EDF does, and an EDF-schedulable task set is exactly one with total utilization ≤ 1. [T0][S-0118]
- Rate-monotonic scheduling (RM) assigns priority inversely to period and is optimal among fixed-priority schedulers in the same model, with guaranteed feasibility bound Σ(Cᵢ/Tᵢ) ≤ n(2^(1/n) − 1). [T0][S-0118]

### CFS (established practice)

- The Linux CFS (completely fair scheduler, since 2.6.23) approximates an ideal, perfectly fair CPU: each task carries a virtual runtime and the scheduler always runs the task with the smallest vruntime, keeping runnable tasks in a red-black tree keyed by vruntime — established practice rather than a mathematically optimal policy. [T3][S-0032]

## Boundaries / common misunderstandings

- SJF/SRTF optimality concerns average waiting time only: a long job can wait arbitrarily long (starvation), the algorithms assume known service times, and they say nothing about other metrics such as worst-case response. [T0][S-0117]
- EDF optimality holds for the preemptive, uniprocessor, independent-periodic-task model with deadline equal to period [T0][S-0118].
- Outside that model — non-preemptive settings, shared-resource (blocking) constraints, or overload — EDF is not optimal and typically misses many deadlines [T3][S-0032].
- Preemption is not free: each preemption may cost a context switch, so quantum and priority design trade responsiveness against switch overhead. [T3][S-0032]
- RR and MLFQ need no knowledge of job lengths, while SJF/SRTF do — which is why SJF is a theoretical benchmark rather than a general-purpose OS default. [T3][S-0032]
- MLFQ is a policy family, not one algorithm: queue count, quanta, and boost intervals are engineering parameters tuned per workload. [T3][S-0032]

## References (evidence records)

- S-0032 — Silberschatz, Galvin & Gagne (2018), Operating System Concepts, 10th ed., Wiley: mechanism-level consensus for preemption, FIFO/SJF/RR/MLFQ, starvation/aging, CFS. (T3)
- S-0018 — ACM/IEEE-CS/AAAI (2024), CS2023: Operating Systems knowledge area; CPU scheduling as core curriculum content. (T2)
- S-0117 — Smith (1956), NRLQ 3(1–2):59–66: proof that SPT/SJF minimizes mean flow time, hence average waiting time. (T0)
- S-0118 — Liu & Layland (1973), JACM 20(1):46–61: EDF optimality (U ≤ 1) and rate-monotonic optimality bound for preemptive periodic scheduling. (T0)
- S-0119 — Schrage (1968), Operations Research 16(3):687–690: proof of SRTF optimality for average waiting time under preemption. (T0)
