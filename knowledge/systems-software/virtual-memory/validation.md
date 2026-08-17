---
id: systems-software/virtual-memory
title: Virtual Memory & Paging
band: B2
track: systems-software
tier: T0
bloom_target: apply
prerequisites: [hardware/memory-hierarchy, systems-software/os-processes]
related: [hardware/cache-coherence, systems-software/containers-isolation]
recommended: []
status: published
schema-version: 1
owner: l1-virtual-memory
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0030, S-0031, S-0032]
---

# Virtual Memory & Paging — validation

## Formative (practice)

### F1 — remember: page-table entries
- Q: What does the present (valid) bit in a page-table entry control?
- bloom: remember
- bank: formative
- A: Whether the VA→PA mapping is currently valid. If the present bit is clear, the CPU raises a page fault on access — either the page is not in RAM (must be brought in) or the mapping is invalid/unallocated.
- evidence: [S-0032]
- topic: systems-software/virtual-memory

### F2 — understand: why multi-level page tables
- Q: Why do modern systems use hierarchical (multi-level) page tables instead of one flat table per process?
- bloom: understand
- bank: formative
- A: A flat table must allocate space for every possible page in the address space (4 MiB for 32-bit/4 KiB pages). Multi-level tables allocate only the levels actually used, so sparse address spaces consume little page-table memory.
- evidence: [S-0032]
- topic: systems-software/virtual-memory

### F3 — apply: two-level page-table walk
- Q: A 32-bit machine uses 4 KiB pages and a 2-level table split 10|10|12, with the page directory at physical 0x00100000. Walk VA 0x00401000: what are the page-directory index, page-table index, and offset?
- bloom: apply
- bank: formative
- A: PD index = (VA >> 22) & 0x3FF = 1; PT index = (VA >> 12) & 0x3FF = 1; offset = VA & 0xFFF = 0x000. The walk reads PDE at 0x00100000 + 1×4, then the PTE at the page table base + 1×4, yielding the frame; PA = frame + 0x000.
- evidence: [S-0032]
- topic: systems-software/virtual-memory

### F4 — apply: TLB coverage
- Q: A CPU has a 64-entry TLB. How much of the address space does it cover with 4 KiB pages, and how much with 2 MiB huge pages?
- bloom: apply
- bank: formative
- A: 64 × 4 KiB = 256 KiB; 64 × 2 MiB = 128 MiB. TLB coverage is tiny relative to the address space, which is why locality and huge pages matter.
- evidence: [S-0032]
- topic: systems-software/virtual-memory

### F5 — understand: TLB miss vs page fault
- Q: Is a TLB miss the same as a page fault? What happens in each case?
- bloom: understand
- bank: formative
- A: No. A TLB miss only means the translation is not cached; the page-table walk still finds a resident frame and the access proceeds. A page fault means the PTE is absent/invalid (or access violates protection) and the OS handler must run — possibly doing disk I/O.
- evidence: [S-0032]
- topic: systems-software/virtual-memory

## Summative (mastery checkpoint)

### S1 — apply: Belady's anomaly simulation
- Q: Run FIFO on reference string 1 2 3 4 1 2 5 1 2 3 4 5 with 3 frames and then with 4 frames. How many page faults in each case, and what does the comparison demonstrate?
- bloom: apply
- bank: summative
- A: 3 frames → 9 faults; 4 frames → 10 faults. More frames produce MORE faults — Bélády's anomaly for FIFO. (LRU/OPT, being stack algorithms, would not show this.)
- evidence: [S-0030, S-0032]
- topic: systems-software/virtual-memory

### S2 — apply: fork with copy-on-write
- Q: A process has 4 GiB of anonymous pages and calls fork(). With COW, what memory work does the OS do at fork time, and what happens on the first write by the child?
- bloom: apply
- bank: summative
- A: At fork the OS only copies page-table entries marked read-only/shared — no page contents are copied. On the child's first write, the protection fault handler allocates a frame and copies that single page before allowing the write. Only pages actually written are copied.
- evidence: [S-0032]
- topic: systems-software/virtual-memory

### S3 — analyze: diagnose thrashing
- Q: A server shows near-zero CPU utilization and near-100% paging activity. Argue whether the fix "add more RAM" is always correct, and what the working set model predicts.
- bloom: analyze
- bank: summative
- A: The symptom is thrashing: the sum of resident working sets exceeds physical memory. Adding RAM helps only if it rebalances the aggregate working set; the structural fix is to make resident set sizes track working sets (working-set-based allocation) or suspend a process. Memory alone does not fix a pathological mix of workloads.
- evidence: [S-0031]
- topic: systems-software/virtual-memory

### S4 — understand: mmap semantics
- Q: Two processes mmap the same file with MAP_SHARED. What do they observe, and when is file data actually read from and written to disk?
- bloom: understand
- bank: summative
- A: Both map the same physical frames, so writes by one are visible to the other (subject to cache coherence). Data is read from the file on page faults (demand paging) and written back when dirty pages are evicted or on msync/close — not on every write() syscall.
- evidence: [S-0032]
- topic: systems-software/virtual-memory

## Review (spaced repetition — interleaved with prerequisites)

### R1 — understand (memory-hierarchy): fault latency ladder
- Q: Put these in latency order, roughly: TLB hit, L1 cache hit, main-memory access, major page fault. What does the spread imply about TLB hit rate?
- bloom: understand
- bank: review
- A: TLB hit (~1 cycle) < L1 hit (~4 cycles) < memory access (~100 ns) << major page fault (~ms, disk I/O). Because a fault is ~5–6 orders of magnitude slower than a TLB hit, a high TLB miss rate can dominate a workload even if cache behavior is good.
- evidence: [S-0032]
- topic: hardware/memory-hierarchy

### R2 — apply (os-processes): context switch and the TLB
- Q: On a context switch to another process, why must translations be invalidated (or tagged), and what is the multicore variant of this cost?
- bloom: apply
- bank: review
- A: The old process's VA→PA mappings do not apply to the new one; without flushing (or ASID tagging), the CPU would use stale translations. On multicore systems, invalidating a mapping shared across cores requires a TLB shootdown (IPI to other cores) — a cost that grows with TLB size and core count.
- evidence: [S-0032]
- topic: systems-software/os-processes

### R3 — understand (related: containers): isolation boundary
- Q: Containers share the host kernel, so two processes in the same container share page tables at the kernel level. Where does the memory-isolation boundary actually live?
- bloom: understand
- bank: review
- A: The boundary is the per-process page table + protection bits maintained by the kernel: each process still has its own virtual address space and PTEs, so one process cannot touch another's frames. Containers add namespace/cgroup accounting (and can add limits), but do not change the hardware isolation primitive — that remains the page table.
- evidence: [S-0032]
- topic: systems-software/containers-isolation
