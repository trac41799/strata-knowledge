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

# OS Scheduling — validation

## Formative (practice)

### F1 — remember: preemption
- Q: What is the difference between a preemptive and a non-preemptive scheduler?
- bloom: remember
- bank: formative
- A: A preemptive scheduler may take the CPU from a running process (typically on a timer interrupt) and move it back to the ready queue; a non-preemptive (cooperative) scheduler switches only when the running process blocks or exits on its own.
- evidence: [S-0032]
- topic: systems-software/os-scheduling

### F2 — understand: the quantum trade-off
- Q: Why is the round-robin quantum a trade-off rather than "smaller is better"?
- bloom: understand
- bank: formative
- A: A small quantum improves responsiveness (everyone gets the CPU sooner) but multiplies context-switch overhead, because every quantum boundary may switch processes. A large quantum degenerates toward FCFS, letting long jobs monopolize the CPU and inflating response time for short jobs.
- evidence: [S-0032]
- topic: systems-software/os-scheduling

### F3 — apply: FCFS average waiting time
- Q: Four processes arrive at times 0, 1, 2, 3 with service times 7, 4, 9, 2 (A, B, C, D). Compute the average waiting time under FCFS.
- bloom: apply
- bank: formative
- A: Completion times: A=7, B=11, C=20, D=22. Waiting times (completion − arrival − service): A 0, B 6, C 9, D 17. Average = (0+6+9+17)/4 = 8.
- evidence: [S-0032]
- topic: systems-software/os-scheduling

## Summative (mastery checkpoint)

### S1 — apply: SJF vs RR on one workload
- Q: Same workload as F3 (A(0,7), B(1,4), C(2,9), D(3,2)). Compute average waiting time for non-preemptive SJF and for round-robin with quantum 4, and state which property the comparison demonstrates.
- bloom: apply
- bank: summative
- A: SJF order: A (only job at t=0) → D → B → C; completions 7, 9, 13, 22; waits A 0, D 4, B 8, C 11; average 23/4 = 5.75. RR(q=4): completions B=8, D=14, A=17, C=22; waits B 3, D 9, A 10, C 11; average 33/4 = 8.25. SJF beats RR here — consistent with SJF's proven optimality for average waiting time.
- evidence: [S-0117]
- topic: systems-software/os-scheduling

### S2 — apply: SRTF preemption trace
- Q: Same workload (A(0,7), B(1,4), C(2,9), D(3,2)). Trace SRTF: at what times does a new arrival preempt the running process, and what is the average waiting time?
- bloom: apply
- bank: summative
- A: t=1: B(4) preempts A (remaining 6). t=3: D(2) preempts B (remaining 3); B resumes at t=5 (D done), A at t=8, C at t=14; completions D=5, B=8, A=14, C=23. Waits: A 7, B 3, C 12, D 0; average 22/4 = 5.5 — lower than non-preemptive SJF (5.75), as the preemptive proof guarantees.
- evidence: [S-0119]
- topic: systems-software/os-scheduling

### S3 — apply: EDF schedulability check
- Q: Three independent periodic tasks on one preemptive CPU: T1(C=1, T=4), T2(C=2, T=6), T3(C=3, T=8). Is the set EDF-schedulable? Would the rate-monotonic bound guarantee it?
- bloom: apply
- bank: summative
- A: Utilization U = 1/4 + 2/6 + 3/8 = 0.9583 ≤ 1, so EDF meets all deadlines (EDF optimality, deadline = period model). The RM bound for n=3 is 3(2^(1/3) − 1) ≈ 0.78 < 0.9583, so the RM bound does NOT guarantee feasibility — RM may still work, but the bound is silent.
- evidence: [S-0118]
- topic: systems-software/os-scheduling

### S4 — analyze: starvation and aging
- Q: A system runs a priority scheduler. A batch job arrives with the lowest priority and the system is busy; it never completes. Diagnose the cause and evaluate the standard fix.
- bloom: analyze
- bank: summative
- A: Cause: starvation — continuously arriving higher-priority work means the low-priority job is never dispatched; priority scheduling guarantees service only if higher-priority arrivals eventually stop. Standard fix: aging — raise the priority of waiting processes over time so the job's priority eventually exceeds the arrival rate and it runs; the trade-off is that aging adds response-time variance to high-priority work.
- evidence: [S-0032]
- topic: systems-software/os-scheduling

## Review (spaced repetition — interleaved with prerequisites)

### R1 — understand (os-processes): mechanism vs policy
- Q: A process is preempted: the timer interrupt fires, the OS saves registers, and the dispatcher runs another process. Which part is "context switch" and which is "scheduling", and where does the overhead come from?
- bloom: understand
- bank: review
- A: Saving/restoring CPU state (registers, PC, stack pointer, address-space state) is the context switch — pure overhead. Choosing WHICH process runs next is the scheduling decision (policy). The overhead is the switch; the decision itself is what the scheduling algorithms in this topic optimize.
- evidence: [S-0032]
- topic: systems-software/os-processes

### R2 — apply (os-processes): fork chain
- Q: A process calls fork() four times in a loop and no process exits early. How many processes exist at the end, and why does this matter for the ready queue the scheduler maintains?
- bloom: apply
- bank: review
- A: The count doubles per round: 2, 4, 8, 16 total processes (15 children). The scheduler's ready queue must hold all runnable processes, so fork chains directly inflate queue length — and, under preemptive schedulers, the per-process bookkeeping (PCBs, timers) the OS must manage.
- evidence: [S-0032]
- topic: systems-software/os-processes

### R3 — apply (os-scheduling): SJF optimality in action
- Q: Three processes arrive together with service times 3, 1, 2. Verify numerically that SJF minimizes average waiting time compared with FCFS.
- bloom: apply
- bank: review
- A: SJF order 1, 2, 3: waits 0, 1, 3 → average 4/3 ≈ 1.33. FCFS order 3, 1, 2: waits 0, 3, 4 → average 7/3 ≈ 2.33. SJF is strictly better on this instance, consistent with Smith's theorem that shortest-first minimizes average waiting time.
- evidence: [S-0117]
- topic: systems-software/os-scheduling
