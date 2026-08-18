---
id: programming/memory-model-and-pointers
title: Memory Model & Pointers
band: B3
track: programming
tier: T1
bloom_target: apply
prerequisites: [hardware/memory-hierarchy]
related: [systems-software/virtual-memory]
recommended: []
status: published
schema-version: 1
owner: l1-memory-model-and-pointers
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0103, S-0104, S-0105, S-0040]
---

# Memory Model & Pointers — validation

## Formative (practice)

### F1 — remember: ownership rules
- Q: State Rust's three ownership rules.
- bloom: remember
- bank: formative
- A: (1) Each value in Rust has an owner. (2) There can be only one owner at a time. (3) When the owner goes out of scope, the value is dropped.
- evidence: [S-0105]
- topic: programming/memory-model-and-pointers

### F2 — understand: why dangling dereference is UB
- Q: Why is dereferencing a dangling pointer "undefined behavior" rather than "guaranteed to crash"?
- bloom: understand
- bank: formative
- A: The standard imposes no requirements on UB (C17 3.4.3): the pointer's value is indeterminate once the object's lifetime ends (6.2.4), and the compiler may assume UB never happens. The behavior may be a crash, silent corruption, or an apparently correct result — which is why this bug class is dangerous rather than merely crash-prone.
- evidence: [S-0103]
- topic: programming/memory-model-and-pointers

### F3 — apply: alias trace
- Q: Trace: int x = 5; int *p = &x; int *q = p; *q = 7; printf("%d", x); What prints, and why are p and q aliases?
- bloom: apply
- bank: formative
- A: x prints 7. p and q hold the same address (aliases); *q = 7 stores through that address, mutating x. Pointer assignment copies addresses, not pointees.
- evidence: [S-0103]
- topic: programming/memory-model-and-pointers

### F4 — understand: data race definition
- Q: Define "data race" in C17 terms: which evaluations conflict, and which two conditions exclude a race?
- bloom: understand
- bank: formative
- A: Two evaluations conflict when one writes a memory location and the other reads or modifies the same location. Conflicting evaluations are a data race unless both are atomic or one happens-before the other; a data race is undefined behavior (5.1.2.4).
- evidence: [S-0103]
- topic: programming/memory-model-and-pointers

## Summative (mastery checkpoint)

### S1 — apply: find the UB
- Q: For each snippet, name the UB class and the standard basis: (a) int *p = malloc(...); free(p); *p = 1; (b) int *p = NULL; *p = 1; (c) two threads, no synchronization, one writes global g while the other reads it.
- bloom: apply
- bank: summative
- A: (a) use-after-free — accessing an object outside its lifetime is UB (6.2.4); (b) null-pointer dereference — UB (6.3.2.3 / 6.5.3.2); (c) data race — UB (5.1.2.4). In each case the standard imposes no requirements on the outcome.
- evidence: [S-0103]
- topic: programming/memory-model-and-pointers

### S2 — analyze: optimization and UB
- Q: A compiler removed a null check from code that dereferenced a pointer earlier. Explain, in terms of the standard and optimization-unstable code, why that transformation is legal.
- bloom: analyze
- bank: summative
- A: Dereferencing a null pointer is UB, and the compiler may assume the program never executes UB. After the dereference (which the compiler assumes succeeded) the pointer cannot be null, so the later check is dead code and removable. Production systems including the Linux kernel and PostgreSQL were found to contain such UB-dependent code that optimizations silently altered.
- evidence: [S-0104]
- topic: programming/memory-model-and-pointers

### S3 — apply: classify memory errors across languages
- Q: Classify: (a) never freeing a buffer; (b) freeing then using it; (c) freeing the same object twice; (d) two threads writing a shared global without synchronization. For each, state the outcome in C/C++, and which are compile-time errors in safe Rust.
- bloom: apply
- bank: summative
- A: (a) leak — compiles everywhere; Rust prevents it via drop-at-scope-end; (b) use-after-free — UB in C/C++; (c) double free — UB in C/C++; (d) data race — UB in C/C++. In safe Rust, (b), (c), and (d) are rejected at compile time by ownership/borrow rules (d unless the shared state is synchronized); (a) is prevented by scoped drop.
- evidence: [S-0103, S-0105]
- topic: programming/memory-model-and-pointers

### S4 — evaluate: "Rust makes unsafe programs impossible"
- Q: Evaluate: "Rust's borrow checker makes it impossible to write memory-unsafe programs."
- bloom: evaluate
- bank: summative
- A: Incorrect as stated. Safe Rust turns the C/C++ classes (use-after-free, double free, null deref, data races on references) into compile-time errors and gives deterministic reclamation. But (1) unsafe blocks re-open the same freedoms locally and must be audited; (2) safety excludes logic bugs, panics, and resource misuse. Verdict: borrow checking eliminates a specific, large bug class — it is not a general correctness guarantee.
- evidence: [S-0105]
- topic: programming/memory-model-and-pointers

## Review (spaced repetition — interleaved with prerequisites)

### R1 — remember (memory-hierarchy): why caching works
- Q: State why a memory hierarchy uses several levels (registers, cache, DRAM) and name the two locality forms it exploits.
- bloom: remember
- bank: review
- A: Fast levels are small and expensive; a hierarchy gives most accesses the speed of the top level and the capacity of the bottom. It exploits temporal locality (recently used data reused soon) and spatial locality (nearby data accessed together).
- evidence: [S-0063]
- topic: hardware/memory-hierarchy

### R2 — understand (memory-model-and-pointers): language model vs hardware
- Q: Why can two threads on x86 (TSO hardware) still observe surprising orderings when the program uses only plain reads/writes, and what is the correct portable fix?
- bloom: understand
- bank: review
- A: Two reasons: the hardware consistency model (TSO) allows store buffering, and — decisively — the language model declares unsynchronized conflicting accesses a data race (UB) and only guarantees visibility through synchronization. The portable fix is language-level synchronization (mutex or atomics with ordering), never reliance on incidental hardware behavior.
- evidence: [S-0040]
- topic: programming/memory-model-and-pointers

### R3 — apply (virtual-memory): where a pointer's address lives
- Q: A user-space pointer holds an address. At what layer is that address meaningful, and what is its relationship to physical memory?
- bloom: apply
- bank: review
- A: A user-space pointer holds a virtual address, meaningful only within the process's address space. The MMU translates it to a physical address via page tables; the program never sees physical addresses, and the mapping may change (swapping, migration) without the pointer changing. Pointer equality and copying operate at the virtual level.
- evidence: [S-0032]
- topic: systems-software/virtual-memory
