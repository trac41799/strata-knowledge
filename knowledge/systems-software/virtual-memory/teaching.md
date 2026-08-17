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

# Virtual Memory & Paging — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **apply** — translate a virtual address through a 2-level (and, given a diagram, 4-level x86-64) page table: compute directory/table indices and offset, and find the physical frame.
- **apply** — compute page-fault counts for FIFO, LRU, and clock on a reference string, and verify Bélády's anomaly numerically ([S-0030]).
- **understand** — explain the demand-paging fault path (trap → validate → locate → replace → read → restart) and distinguish minor vs major faults.
- **understand** — explain copy-on-write fork and mmap semantics, including when I/O actually happens.
- **analyze** — diagnose thrashing from utilization/paging signals and argue fixes using the working set model ([S-0031]).
- **evaluate** — choose a page size / huge-page strategy for a workload given TLB coverage and fragmentation arithmetic.

## Worked example 1 — walking a two-level page table

Setup: 32-bit VAs, 4 KiB pages, 2-level split 10 | 10 | 12 (each table = 1024 × 4 B = 4 KiB), page directory base = 0x00100000.

Walk VA `0x00401000`:

1. Offset = bits 11..0 = `0x00401000 & 0xFFF = 0x000`.
2. PT index = bits 21..12 = `(0x00401000 >> 12) & 0x3FF = 0x401 & 0x3FF = 1`.
3. PD index = bits 31..22 = `(0x00401000 >> 22) & 0x3FF = 1`.
4. Read PDE at `0x00100000 + 1×4` → gives page-table base (say `0x00200000`), present.
5. Read PTE at `0x00200000 + 1×4` → gives frame `F`, present, writable.
6. PA = `F + 0x000`.

Why hierarchy? A flat table would be 4 MiB per process, allocated eagerly. The 2-level version costs 4 KiB for the directory plus one 4 KiB table per used 4 MiB region — 8 KiB total for a 4 MiB program, and the walk is only 2 extra memory reads ([S-0032]).

## Worked example 2 — simulating Bélády's anomaly

Reference string: `1 2 3 4 1 2 5 1 2 3 4 5`. Run FIFO:

- **3 frames**: 1(F) 2(F) 3(F) | 4 evicts 1 → faults 1,2,3,4 | 1 evicts 2 | 2 evicts 3 | 5 evicts 4 | 1,2 hit | 3 evicts 1 | 4 evicts 2 | 5 hit → **9 faults**.
- **4 frames**: 1(F) 2(F) 3(F) 4(F) | 1,2 hit | 5 evicts 1 | 1 evicts 2 | 2 evicts 3 | 3 evicts 4 | 4 evicts 5 | 5 evicts 1 → **10 faults**.

More memory, more faults — Bélády's anomaly ([S-0030]). Check: LRU on the same string gives 10 faults with 3 frames and 8 with 4 frames — monotonically better, the stack property. Moral: "add RAM → fewer faults" is only guaranteed for stack algorithms.

## Elaboration prompts

- Why does a 4-level x86-64 walk cost up to 4 memory references, and how does that justify a TLB and page-walk caches?
- Why is exact LRU not implementable in an OS page table, and what exactly does the clock algorithm give up? (Every PTE a timestamp? Where would it be stored?)
- Why does the OS pre-zero pages lazily, and how does a "minor" zero-page fault avoid disk I/O? What must the OS do to keep the zero page read-only-safe?
- Why does mmap beat `read()` for large files even though both must fault pages in? (Hint: copying, page-cache aliasing, and write-back.)
- Belady's anomaly is formally proven for FIFO — what practical engineering lesson does it teach about caches that grow? ([S-0030])

## Common misconceptions

1. **"Virtual memory = swap/swapfile."** Swap is only the backing store; the same mechanisms give isolation, protection, sharing, lazy loading, and COW. A machine with zero swap still has virtual memory. [S-0032]
2. **"TLB miss = page fault."** A TLB miss is resolved by a page-table walk and needs no OS involvement (hardware walk); only an absent/invalid PTE raises a fault. [S-0032]
3. **"More frames always mean fewer faults."** True for stack algorithms (LRU, OPT) but provably false for FIFO — Bélády's anomaly. [S-0030]
4. **"The OS implements LRU."** OS page replacement uses approximations (clock/aging) because exact LRU needs per-access recency data at scale; LRU is the *ideal*, not the implementation. [S-0032]
5. **"Virtual address space is fully backed by RAM."** Pages are mapped lazily; a 64-bit process can have terabyte-sized *reserved* regions backed by a handful of frames. [S-0032]
6. **"fork() copies all of the parent's memory."** With COW it copies only page tables; contents are duplicated lazily per written page. [S-0032]

## Feynman targets

- "Explain to a junior engineer why a program can address more memory than the machine has, without it being slow — until it is."
- "Explain why a 2 MiB page can make a database faster than a 4 KiB page, using TLB coverage arithmetic."
- "Explain what thrashing is, why it happens, and why 'add RAM' is sometimes the wrong answer" ([S-0031]).
- "Explain the difference between a TLB miss and a page fault as if to someone who has only heard of caching."

## Interleaving hooks

- **hardware/memory-hierarchy** — the TLB is a cache of translations at the top of the same latency ladder; recall the fault-latency spread (~ns vs ~ms).
- **hardware/cache-coherence** — TLB shootdowns: when the OS changes a shared PTE (or flushes on context switch), cores must be interrupted to invalidate their TLBs — coherence for translations, not data.
- **systems-software/os-processes** — context switches now cost TLB flushes (or ASID swaps); relate process isolation to per-process page tables.
- **systems-software/containers-isolation** — containers add cgroup memory limits on top of page-table isolation; the isolation primitive is still the PTE's protection bits.
- **programming/memory-model-and-pointers** — what `malloc` returns is a *virtual* address; the frame appears only when touched (demand paging + lazy zero).
