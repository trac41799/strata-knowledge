---
id: systems-software/virtual-memory
title: Virtual Memory & Paging
band: B2
track: systems-software
tier: T1
bloom_target: apply
prerequisites: [hardware/memory-hierarchy, systems-software/os-processes]
related: [hardware/cache-coherence, systems-software/containers-isolation]
recommended: []
status: draft
schema-version: 1
owner: l1-virtual-memory
reviewed-by: []
updated: 2026-08-18
sources: [S-0030, S-0031, S-0032]
---

# Virtual Memory & Paging

## Claims

### Address translation & page tables

- Virtual memory gives every process a private virtual address space; the CPU translates each virtual address (VA) to a physical address (PA) per page through a per-process page table, so processes cannot address each other's memory without the OS arranging it. [T3][S-0032]
- A page-table entry (PTE) holds the physical frame number plus control bits (present/valid, read/write, dirty, referenced); a PTE whose present bit is clear triggers a page fault on access. [T3][S-0032]
- Multi-level (hierarchical) page tables — e.g., the x86-64 four-level radix tree (PML4 → PDPT → PD → PT) with 4 KiB pages — allocate only the levels a process actually uses, so a sparse address space does not pay the cost of a flat table. [T3][S-0032]
- Quantitatively: a flat one-level table for a 32-bit address space with 4 KiB pages costs 4 MiB per process (2^20 PTEs × 4 B); a two-level 10|10|12 split costs at most 4 KiB + 4 MiB and typically far less. [T3][S-0032]

### TLB

- The TLB caches recent VA→PA translations; a TLB hit skips the page-table walk, while a miss triggers a walk — hardware-managed on x86, software-managed on some RISC ISAs. [T3][S-0032]
- A four-level x86-64 walk costs up to four additional memory references per access, so TLB hit rate is a first-order performance factor; page-walk caches and huge pages exist to mitigate walk cost. [T3][S-0032]
- TLB coverage is small: a 64-entry TLB with 4 KiB pages covers 256 KiB of address space, versus 128 MiB with 2 MiB huge pages. [T3][S-0032]

### Demand paging & page faults

- Demand paging loads a page into a frame only on first reference; on a page fault the OS validates the access, locates the page in backing store (swap or file), frees a frame if needed, reads the page, updates the PTE, and restarts the faulting instruction. [T3][S-0032]
- Not all faults touch disk: minor faults (zero-filled pages, copy-on-write, pages already resident) resolve without I/O, while major faults perform disk I/O and dominate fault latency. [T3][S-0032]

### Page replacement

- Page replacement selects a victim frame when all frames are in use; the standard algorithms are FIFO, LRU, and clock (second-chance), and evicting a clean page is cheaper than evicting a dirty one (write-back). [T3][S-0032]
- Bélády's anomaly: for FIFO, adding page frames can increase the page-fault count — Belady, Nelson, and Shedler (1969) constructed reference strings with this behavior and gave a formal treatment. [T0][S-0030]
- LRU and the optimal algorithm (OPT) have the stack property — fault counts never increase when frames are added — so the anomaly cannot occur for them. [T3][S-0032]
- Exact LRU is impractical in an OS (per-access recency bookkeeping for every page); implementations approximate it with the hardware reference bit, e.g., clock/aging and second-chance schemes. [T3][S-0032]

### Working set & thrashing

- Denning's working set W(t, τ) is the set of pages a process references during the last τ references; the working set model predicts a process's current memory demand from the observed locality of reference. [T1][S-0031]
- Thrashing occurs when the sum of active working sets exceeds physical memory: processes fault continuously, CPU utilization collapses, and the system spends its time paging; working-set-aware allocation (or suspending a process) prevents it. [T1][S-0031]

### Copy-on-write & mmap

- Copy-on-write (COW) lets fork() share pages read-only between parent and child; the first write raises a protection fault and the OS copies the page, making fork cheap regardless of the process's size. [T3][S-0032]
- Memory-mapped files (mmap) map file ranges into the virtual address space; pages are faulted in from the file on access and written back when dirty, and MAP_SHARED mappings give multiple processes a shared view of the same pages. [T3][S-0032]
- Page size is a trade-off: 4 KiB pages minimize internal fragmentation but inflate page-table memory and TLB/walk costs; huge pages (2 MiB / 1 GiB) cut those costs at the price of fragmentation. [T3][S-0032]

## Boundaries / common misunderstandings

- Virtual memory is not the same as swap: it also provides isolation, protection, lazy loading, and sharing (mmap, shared libraries, COW); swap is only one backing-store mechanism. [T3][S-0032]
- A TLB miss is not a page fault: a miss only forces a page-table walk, which may still resolve to a resident frame; a fault occurs only when the PTE is absent or the access is invalid. [T3][S-0032]
- A 64-bit virtual address space is not physically backed until pages are touched; mappings are created lazily on demand. [T3][S-0032]
- "Add more RAM → fewer page faults" is not guaranteed for FIFO-like algorithms (Bélády's anomaly); it holds only for stack algorithms such as LRU and OPT. [T0][S-0030]

## References (evidence records)

- S-0030 — Belady, Nelson & Shedler (1969), CACM 12(6):349–353: Bélády's anomaly, formal treatment for FIFO. (T0)
- S-0031 — Denning (1968), CACM 11(5):323–333: working set model, locality, thrashing prevention. (T1)
- S-0032 — Silberschatz, Galvin & Gagne (2018), Operating System Concepts, 10th ed., Wiley: mechanism-level consensus for paging, TLB, replacement, COW, mmap. (T3)
