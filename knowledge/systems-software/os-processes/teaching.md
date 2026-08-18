---
id: systems-software/os-processes
title: OS Processes
band: B2
track: systems-software
tier: T2
bloom_target: apply
prerequisites: [programming/memory-model-and-pointers]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-os-processes
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0032, S-0018, S-0112, S-0113]
---

# OS Processes — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **apply** — trace the states of multiple processes through a lifecycle timeline (new/ready/running/waiting/terminated) and name each transition ([S-0032]).
- **apply** — predict the process count, PIDs, and return values of fork()/exec() programs, and compute fork-chain counts ([S-0112]).
- **apply** — compute context-switch overhead as a fraction of CPU time given switch count and per-switch cost.
- **understand** — explain what a PCB is, what it stores, and why it must exist even for a process that is not running.
- **understand** — contrast process and thread sharing, and explain why threads of one process are not MMU-isolated from each other ([S-0032]).
- **analyze** — diagnose resource leaks (zombie accumulation) and failure modes in process-creation loops.

## Worked example 1 — process lifecycle trace

Three processes share one CPU: P1 (compute-heavy), P2 (I/O-heavy), P3 (compute-heavy). Timeline, one step per event:

| Step | Event | P1 | P2 | P3 |
|---|---|---|---|---|
| 0 | boot, all created | new | new | new |
| 1 | P1 admitted | ready | new | new |
| 2 | P2, P3 admitted | ready | ready | ready |
| 3 | dispatcher runs P1 | running | ready | ready |
| 4 | timer interrupt → dispatcher runs P2 | ready | running | ready |
| 5 | P2 blocks on disk read() | ready | waiting | ready |
| 6 | dispatcher runs P3 | ready | waiting | running |
| 7 | P3 completes | ready | waiting | terminated |
| 8 | disk data arrives, P2 unblocked | ready | ready | terminated |
| 9 | P2 re-dispatched, later exits; parent reaps both | — | terminated | terminated |

Key transitions: running→ready happens on preemption (step 4) — P1 did nothing "wrong"; running→waiting happens only on a blocking event (step 5); waiting→ready needs the event plus scheduling, not an immediate run (step 8). Note step 9: after P2 exits it is still a zombie until its parent calls wait(), and only then does its PCB disappear ([S-0032]).

## Worked example 2 — fork and exec

A shell (PID 100) runs `ls`. The shell forks:

- Child gets PID 101; at the moment fork() returns, child memory is a logical copy of the shell's; the return value is 0 in the child and 101 in the parent.
- The child calls exec("/bin/ls"): its address space is replaced by the ls image — same PID 101, fresh stack/heap, file descriptors beyond the exec-cloexec set survive.
- The parent (still the shell, PID 100) is blocked in wait(); when ls exits, the child becomes a zombie until the shell's wait() reaps it and the shell resumes ([S-0112]).

Why two syscalls? Because the child of fork can change its environment (redirect stdout, close descriptors, set uid) BETWEEN fork and exec — the shell's redirection support depends on this separation. A single "spawn" primitive could not express `ls > out.txt` without extra machinery.

## Elaboration prompts

- Why does the kernel need a PCB for a process that is not currently running — what information must be saved, and where can it be stored (user-level vs kernel-level stack)?
- Why is fork() cheap in modern systems (copy-on-write) but expensive in the abstract model, and which model is "more correct" for understanding ([S-0032])?
- Why is a context switch pure overhead — can any user work happen during the switch? What upper bound does that impose on preemption frequency?
- If threads are just tasks sharing an address space (Linux), why do many textbooks present them as a separate concept? Where does the boundary really live ([S-0113])?
- Why does Unix deliberately leave the parent to reap its children rather than having the kernel clean up instantly?

## Common misconceptions

1. **"A process is the same as its program."** The program is a static artifact (file/image); the process is the executing instance with registers, stack, heap, and open files — two processes can run the same program ([S-0032]).
2. **"fork() copies all of the parent's memory immediately."** Modern systems use copy-on-write: only page tables are copied at fork, and page contents are duplicated lazily on first write ([S-0032]).
3. **"Threads are processes that use less memory."** The difference is structural, not size: threads share one address space (no MMU isolation between them), processes have separate ones. A thread bug can corrupt the whole process; a process can only be corrupted by itself ([S-0032]).
4. **"A zombie process is still running / consuming CPU."** A zombie holds only a PCB (process-table entry) after exit, waiting for its parent to collect the status; it uses no CPU or memory. Orphans are reparented so they eventually get reaped ([S-0032]).
5. **"Context switch and scheduling decision are the same thing."** The scheduler DECIDES who runs next; the context switch is the mechanical save/restore that IMPLEMENTS the decision ([S-0032]).
6. **"The child of fork is completely independent."** Logically yes after fork, but open file descriptions and (optionally) shared mappings are inherited; and until the parent reaps it, the child's exit status ties them together.

## Feynman targets

- "Explain to a junior engineer why 'a process is a program in execution' is too thin — what state does the OS must remember about a process that isn't running?"
- "Explain fork() to a friend who only knows function calls: why does one call 'return twice'?"
- "Explain why a crashed thread can take down its process, but a crashed process cannot take down the OS."
- "Explain what a zombie process is, using the metaphor of a receipt the parent forgot to collect."

## Interleaving hooks

- **programming/memory-model-and-pointers** — the address space a process manipulates is virtual; pointer values are only meaningful inside one process's mapping (isolation in action).
- **hardware/isa-basics** — user/kernel mode is the ISA-level primitive that makes process isolation and syscalls possible; traps are the only legal entry into the kernel.
- **systems-software/os-scheduling** — context switch is the mechanism, scheduling is the policy; switch cost is the budget the scheduler spends (quantum vs overhead).
- **systems-software/virtual-memory** — per-process page tables implement isolation; copy-on-write makes fork cheap; switching processes flushes or tags TLB entries.
- **programming/concurrency-primitives** — threads of one process communicate through shared memory directly, which is exactly why they need locks; processes need IPC plus locks on top.
