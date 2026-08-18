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

# OS Processes — validation

## Formative (practice)

### F1 — remember: the PCB
- Q: What information does the OS keep in a process control block (PCB)?
- bloom: remember
- bank: formative
- A: The PCB stores per-process metadata the kernel needs to manage and switch processes: process id, state, saved CPU context (registers/PC/stack pointer), scheduling info, memory-management info, accounting, and I/O status. It is the kernel's representation of the process.
- evidence: [S-0032]
- topic: systems-software/os-processes

### F2 — understand: fork's two return values
- Q: Why does fork() appear to return two different values, and how does the child differ from the parent at that moment?
- bloom: understand
- bank: formative
- A: fork() creates a child process that is a copy of the parent; the call returns 0 in the child and the child's PID in the parent, so one call site can branch on which process it is. The two processes have identical memory contents (logically) and open-file tables, but different PIDs and different return values.
- evidence: [S-0112]
- topic: systems-software/os-processes

### F3 — apply: lifecycle trace
- Q: Process P1 is running and issues a blocking read() on a pipe with no data; the scheduler then dispatches P2. List P1's and P2's state transitions in order.
- bloom: apply
- bank: formative
- A: P1: running → waiting (blocked) when read() cannot proceed; later waiting → ready when data arrives; P2: ready → running when dispatched. If a timer interrupt fires instead of a blocking call, P1 would go running → ready (preemption), not running → waiting.
- evidence: [S-0032]
- topic: systems-software/os-processes

### F4 — apply: fork then exec
- Q: A shell process forks a child, and the child immediately execs /bin/ls. How many processes exist after each step, and which one runs the new program?
- bloom: apply
- bank: formative
- A: After fork: two processes (parent shell + child copy). After exec in the child: still two processes, but the child's image is replaced by /bin/ls — same PID, new code/data. The parent's memory is untouched. Creation (fork) and program loading (exec) are deliberately separate.
- evidence: [S-0112]
- topic: systems-software/os-processes

## Summative (mastery checkpoint)

### S1 — apply: fork-chain count
- Q: A process calls fork() three times in a loop (each process, including children, continues the loop). How many total processes exist when the loop finishes? What would the count be if the child processes exited immediately after each fork?
- bloom: apply
- bank: summative
- A: With each process forking, the count doubles each iteration: 2, 4, 8 — 8 total processes (7 children). If every child exited immediately after forking, each parent would have one zombie child, and the living processes would number 8 minus the 7 exited zombies that are not yet reaped — the zombie PCBs remain until wait() is called.
- evidence: [S-0032]
- topic: systems-software/os-processes

### S2 — analyze: zombie accumulation
- Q: A long-running daemon forks a child per task and never calls wait(). Over weeks the process table fills. Diagnose the mechanism and the failure mode.
- bloom: analyze
- bank: summative
- A: Each finished child whose exit status is uncollected remains as a zombie: a process-table entry (PCB) with no memory or CPU usage. Accumulated zombies exhaust the per-user process table, so new fork() calls fail with EAGAIN. Fix: reap children promptly (SIGCHLD handler + waitpid, or subreapers), not by killing the daemon — its children are already dead.
- evidence: [S-0032]
- topic: systems-software/os-processes

### S3 — understand: process vs thread
- Q: Which resources are shared between two threads of one process, and which are not? How does this differ from two processes?
- bloom: understand
- bank: summative
- A: Threads share the address space (code, data, heap) and open files but have private stacks and saved CPU contexts; a context switch between threads of one process does not switch address spaces. Two processes share nothing implicitly — separate address spaces and file tables — and require IPC to exchange data.
- evidence: [S-0032]
- topic: systems-software/os-processes

## Review (spaced repetition — interleaved with prerequisites)

### R1 — understand (memory-model-and-pointers): pointers are virtual
- Q: A process prints the address of a stack variable. Why can another process safely use the same numeric address, and what does the value actually denote?
- bloom: understand
- bank: review
- A: Addresses a process sees are virtual addresses in its own address space; the MMU/page tables map them to physical frames. Each process has its own mapping, so identical virtual addresses in different processes refer to different physical memory — a concrete consequence of per-process isolation.
- evidence: [S-0032]
- topic: programming/memory-model-and-pointers

### R2 — apply (os-processes): context-switch cost
- Q: A server performs 50,000 context switches per second and each switch costs 4 microseconds of pure overhead. What fraction of one CPU is consumed by switching, and how would switching threads of one process instead change the cost?
- bloom: apply
- bank: review
- A: 50,000 × 4 µs = 0.2 s per second — 20% of the CPU lost to switching. Thread switches within one process skip the address-space change (no page-table base swap, reduced TLB effects), so per-switch cost is typically lower; the arithmetic is the same method either way.
- evidence: [S-0032]
- topic: systems-software/os-processes

### R3 — understand (isa-basics): privilege as the isolation primitive
- Q: What exactly does the hardware enforce when a process runs in user mode, and why is a syscall a trap rather than a function call?
- bloom: understand
- bank: review
- A: In user mode the CPU rejects privileged instructions (e.g., loading the page-table base, device I/O, interrupt control) with a fault, so a process cannot install its own memory map or touch devices directly. A syscall executes a trap instruction that atomically switches to kernel mode at a fixed entry point — a plain function call would keep the process in user mode where the privileged operation is impossible.
- evidence: [S-0032]
- topic: hardware/isa-basics
