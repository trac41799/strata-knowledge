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

# OS Processes

## Claims

### Process model & PCB

- A process is a program in execution: the executable plus its runtime state (program counter, registers, stack, heap, open files, and other resources), represented by the OS in a process control block (PCB). [T3][S-0032]
- The PCB holds the per-process metadata the kernel needs to manage and switch processes: process id, state, saved CPU context, scheduling information, memory-management information, accounting, and I/O status. [T3][S-0032]
- The process abstraction and its management (creation, lifecycle, states) are core content of the Operating Systems knowledge area of CS2023. [T2][S-0018]

### Process states

- The canonical lifecycle states are new, ready, running, waiting (blocked), and terminated; dispatch (ready→running), event waits (running→waiting), event completions (waiting→ready), and completion (running→terminated) drive the transitions. [T3][S-0032]
- A terminated process whose exit status has not been collected remains as a zombie holding only its PCB; orphaned children are reparented so that someone eventually reaps them. [T3][S-0032]

### System calls: fork and exec

- Unix separates creation from program loading: fork() creates a child that is a copy of the parent (returning 0 in the child and the child's PID in the parent), and exec() replaces the calling process's image with a new program — the two-step mechanism described in Ritchie and Thompson's 1974 paper on the UNIX time-sharing system. [T3][S-0112]
- On Linux, processes and threads are both tasks: fork()/clone() create tasks, and threads are tasks that share the parent's address space (CLONE_VM) — the process/thread distinction is which resources are shared, not two different abstractions. [T3][S-0113]
- A multithreaded process is a unit of ownership: threads inside one process share its address space and open files but have separate stacks and saved contexts, whereas different processes have separate address spaces. [T3][S-0032]

### Context switch

- A context switch saves the running process's CPU context into its PCB and restores another process's; it is pure overhead because no user work executes during the switch. [T3][S-0032]
- Switching between processes in different address spaces also switches address-space state (e.g., the page-table base register) with TLB consequences; switching between threads of the same process does not. [T3][S-0032]

### Isolation & kernel mode

- User processes run in a restricted CPU mode and enter the kernel only through system calls, traps, and interrupts; privileged instructions and direct device I/O are denied in user mode. [T3][S-0032]
- Processes are isolated from each other: the MMU enforces per-process address translation and the kernel mediates I/O, so one process cannot read or write another process's memory or files without authorization. [T3][S-0032]
- Inter-process communication (pipes, signals, shared memory, message queues, sockets) is the sanctioned channel for data exchange between processes — the isolation boundary remains intact. [T3][S-0032]

## Boundaries / common misunderstandings

- A process is not a program: the program is a static artifact (a file or image); the process is the executing instance with dynamic state. [T3][S-0032]
- fork() need not copy all of the parent's memory at creation: copy-on-write defers page copies until a page is actually written (see systems-software/virtual-memory). [T3][S-0032]
- Context switching is the mechanism; deciding WHEN to switch is the scheduler's job (see systems-software/os-scheduling). [T3][S-0032]
- A zombie is not a running process: it consumes no CPU and holds only its PCB until reaped. [T3][S-0032]
- A thread is not a lightweight process in the isolation sense: threads share an address space and are not isolated from each other by the MMU — only processes are. [T3][S-0032]

## References (evidence records)

- S-0032 — Silberschatz, Galvin & Gagne (2018), Operating System Concepts, 10th ed., Wiley: mechanism-level consensus for the process model, PCB, states, fork/exec, context switch, isolation. (T3)
- S-0018 — ACM/IEEE-CS/AAAI (2024), CS2023: Operating Systems knowledge area; process management as core curriculum content. (T2)
- S-0112 — Ritchie & Thompson (1974), CACM 17(7):365–375: fork()/exec() as the Unix process-creation mechanism. (T3)
- S-0113 — Love (2010), Linux Kernel Development, 3rd ed.: task_struct, fork/clone, threads as tasks sharing the address space. (T3)
