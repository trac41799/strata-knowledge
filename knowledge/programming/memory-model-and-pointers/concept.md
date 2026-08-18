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

# Memory Model & Pointers

## Claims

### Pointer semantics

- In C, a pointer is a derived type: "pointer to T" designates objects of type T, and a pointer to an object is a value holding the object's address; several pointers may hold the same address (aliasing). [T2][S-0103]
- Pointers and integers are distinct types: conversions between them are never implicit (a cast is required), and converting a pointer to an integer yields an implementation-defined value if it cannot be represented — pointers are not integers. [T2][S-0103]
- An array expression is converted to a pointer to its first element in most contexts (except as operand of sizeof, of &, and string-literal initialization), so "array parameters" are really pointers (C17 6.3.2.1). [T2][S-0103]
- Because pointers alias, the compiler cannot assume distinct names mean distinct memory; restrict (C17 6.7.3.1) lets the programmer assert non-aliasing so the compiler may optimize accordingly. [T2][S-0103]

### Null & dangling pointers

- Every pointer type has a null pointer value; NULL, or any integer constant expression with value 0, converts to it, and dereferencing a null pointer is undefined behavior (C17 6.3.2.3). [T2][S-0103]
- Null is the standard "no object / error" value: functions receiving pointers must check for null, and free(NULL) performs no action by the standard (C17 7.22.3.3). [T2][S-0103]
- When the object a pointer designates ends its lifetime, the pointer's value becomes indeterminate, and accessing an object outside its lifetime is undefined behavior — the formal basis of dangling-pointer and use-after-free bugs (C17 6.2.4). [T2][S-0103]

### Undefined behavior

- The C standard's behavior categories are defined, unspecified, implementation-defined, and undefined behavior — the last being "behavior... for which this document imposes no requirements" (C17 3.4.3), so a conforming compiler may respond in any way, including not at all. [T2][S-0103]
- Annex J.2 of C17 enumerates the undefined behaviors; compilers must diagnose syntax and constraint violations but are not required to diagnose UB, so UB-ridden code can compile silently. [T2][S-0103]
- UB is not hypothetical: a study of production systems found "optimization-unstable code" — code silently discarded or transformed by compiler optimizations because it relies on UB — in the Linux kernel and PostgreSQL. [T1][S-0104]
- Because the compiler may assume UB never occurs, an optimization can exploit a UB-based assumption in ways the programmer never expected (e.g., deleting a null check after an unconditional dereference). [T1][S-0104]

### Memory model & data races

- The C (and C++) memory model defines memory locations, conflicting evaluations, and happens-before: two conflicting evaluations (one writing a location, another reading or writing it) that are not both atomic and not ordered by happens-before constitute a data race, and a data race is undefined behavior (C17 5.1.2.4). [T2][S-0103]
- Synchronization establishes happens-before: a mutex unlock synchronizes-with a later lock of the same mutex, which is why lock-protected data is race-free (C17 5.1.2.4). [T2][S-0103]
- Without synchronization a thread need not see another thread's writes: the language model deliberately abstracts over the hardware consistency model, which ranges from sequential consistency (SC) through total store order (TSO, x86) to relaxed models (ARM, Power). [T3][S-0040]
- Portable multi-threaded code must therefore use language-level atomic operations or locks rather than rely on incidental hardware behavior; hardware consistency is what the language model maps onto, not what programs directly observe. [T3][S-0040]

### Ownership patterns (Rust)

- Rust's ownership discipline is a type-level rule set: every value has exactly one owner, only one owner exists at a time, and the value is dropped when its owner goes out of scope — deterministic reclamation without a GC and without manual free. [T3][S-0105]
- The borrow checker enforces reference rules at compile time: at any moment a value may have either one mutable reference or any number of immutable references, and references must always be valid — making use-after-free and data races on references compile-time errors, not runtime faults. [T3][S-0105]
- Ownership is a static discipline: the checks cost nothing at runtime, but they impose a learning cost (moves, lifetimes), and unsafe blocks deliberately re-open C-like freedom locally and must be kept minimal and audited. [T3][S-0105]

## Boundaries / common misunderstandings

- "A pointer is an integer": pointer-to-integer conversions require casts and are implementation-defined beyond representability; round-tripping addresses through integers is not portable. [T2][S-0103]
- "Dereferencing a dangling pointer crashes": UB imposes no requirements — it may crash, corrupt, or appear to work, which is exactly why it is dangerous and exploitable. [T2][S-0103]
- "A data race just produces a wrong value": the racing location may not be the only casualty, because the compiler may reorder or transform code around UB-based assumptions. [T1][S-0104]
- "The memory model is about cache hardware": the model is the contract between language, compiler, and hardware; programs must obey the language model, not the hardware's incidental behavior. [T3][S-0040]
- "Rust makes memory unsafety impossible": safe Rust excludes the C/C++ error classes, but unsafe code reintroduces them locally, and logic and abstraction bugs remain. [T3][S-0105]

## References (evidence records)

- S-0040 — Sorin, Hill & Wood, memory consistency primer (T3)
- S-0103 — ISO/IEC 9899:2018 (C17) (T2)
- S-0104 — Wang et al., SOSP 2013 (T1)
- S-0105 — Klabnik & Nichols, The Rust Programming Language, 2nd ed. (T3)
