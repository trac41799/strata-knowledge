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

# Memory Model & Pointers — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember** — state Rust's ownership rules and the C17 definitions of undefined behavior, data race, and indeterminate pointer values ([S-0105], [S-0103]).
- **understand** — explain why UB "imposes no requirements" and why data races are UB rather than merely wrong values ([S-0103], [S-0104]).
- **apply** — trace pointer aliasing and classify memory errors (use-after-free, double free, null deref, leak, data race) with their standard basis and their Rust counterparts ([S-0103], [S-0105]).
- **analyze** — explain compiler transformations that exploit UB (e.g., null-check elimination) and the memory-model contract between language, compiler, and hardware ([S-0104], [S-0040]).
- **evaluate** — assess claims like "Rust makes memory unsafety impossible" against the ownership model's actual scope ([S-0105]).

## Worked example 1 — pointer alias trace (with the dangling bug)

```c
int a = 5;
int *p = &a;      // p holds a's address
int *q = p;       // q copies the address: p and q are aliases
*q = 7;           // store through q: writes to a
printf("%d\n", a); // 7 — a changed via an alias
int *r = (int *)malloc(sizeof(int));
*r = 9;
free(r);
*r = 1;           // UB: r's pointee lifetime ended at free()
```

**Step-by-step.** (1) `p` and `q` both hold the address of `a`; a store through either is a store to `a` — that is aliasing. (2) Pointer assignment copies addresses, never pointees. (3) After `free(r)`, `r` still holds the (now stale) address, but the object's lifetime has ended: the standard says the pointer's value becomes indeterminate and accessing the object is UB (C17 6.2.4). Nothing requires a crash — the program may print garbage, corrupt the allocator, or appear to work — which is why this class of bug is both common and dangerous ([S-0103]).

## Worked example 2 — UB and the compiler (null-check elimination)

```c
void f(struct T *p) {
    *p = 0;        // dereference first
    if (p == NULL) return;   // optimized away
    /* ... */
}
```

**Step-by-step.** (1) `*p = 0` is only well-defined when `p` is non-null; if `p` were null, the program has UB (6.3.2.3 / 6.5.3.2). (2) The standard imposes no requirements on UB, and the compiler may assume UB never occurs. (3) Therefore the compiler may conclude `p != NULL` after the dereference and delete the check as dead code. The result: a "defensive" check the developer wrote never runs — the code behaves differently than it reads. The SOSP 2013 study found exactly this class ("optimization-unstable code") in production systems, including the Linux kernel and PostgreSQL ([S-0104]).

**Practice note.** Because UB is not reliably diagnosable by the language, C/C++ developers detect these classes dynamically: AddressSanitizer (use-after-free, overflow, use-after-return) and UndefinedBehaviorSanitizer (null deref, misaligned access, signed overflow) are the standard tooling, typically enabled in debug/test builds.

## Elaboration prompts

- "A pointer is just an integer holding an address" — what breaks if you act on that belief? (Think: what the standard guarantees about pointer-to-integer conversion, and what the compiler may assume.)
- Dereferencing a dangling pointer is UB; dereferencing a *valid* pointer to a freed-but-still-mapped page often "works". Why does the "works" case make the bug class worse, not better?
- A data race is UB, not "a wrong value sometimes". If the compiler can reorder a hoisted load, what else can go wrong besides the racing variable itself?
- The language memory model guarantees almost nothing about plain shared reads/writes — so what exactly do mutexes and atomics add, in happens-before terms?
- Rust rejects the C/C++ error classes at compile time. What does that cost — where do the moves, lifetimes, and unsafe blocks show up in real code?
- Why is "trust the hardware model" (e.g., x86 TSO) not a portable substitute for language-level synchronization?

## Common misconceptions

1. **"Pointers are integers."** Pointer and integer types are distinct; conversions require casts and are implementation-defined beyond representability — and the compiler is free to reason about pointers without consulting your integer arithmetic. [S-0103]
2. **"UB means it crashes (or doesn't)."** UB means *no required behavior*: the program may crash, corrupt, or work — and optimizations may exploit it silently. [S-0103], [S-0104]
3. **"A data race just flips a value."** Races are UB; compilers can reorder/transform code around the racing access, so unrelated state can be corrupted too. [S-0104]
4. **"The memory model describes what the hardware does."** It is the *contract* the language makes with compiler and hardware; programs must obey the language model (atomics/locks), not incidental hardware behavior. [S-0040]
5. **"Rust's borrow checker makes memory bugs impossible."** Safe Rust excludes the C/C++ classes at compile time; unsafe blocks and non-memory bugs (logic, panics, resource misuse) remain. [S-0105]
6. **"If it compiles without warnings, it's fine."** Annex J.2 UB is not required to be diagnosed; silent UB is the norm, which is why dynamic sanitizers are standard practice. [S-0103]

## Feynman targets

- "Explain to a non-programmer why two names can silently refer to the same memory cell, and why a store through one 'mysteriously' changes the other." ([S-0103])
- "Explain why the C standard 'imposes no requirements' on some programs, and why that freedom is what makes optimizers fast and bugs confusing." ([S-0103])
- "Explain a data race as two people editing the same notebook line without a rule about turns — and why the 'no rule' case is worse than a wrong answer." ([S-0103])
- "Explain how Rust's single-owner rule removes an entire class of memory bugs at compile time, and what you give up to get that." ([S-0105])

## Interleaving hooks

- **hardware/memory-hierarchy** (prerequisite) — pointer dereferences walk the cache hierarchy; locality determines whether the alias trace costs nanoseconds or page faults ([S-0063]).
- **systems-software/virtual-memory** (related) — a pointer holds a *virtual* address; translation, swapping, and page faults live between your pointer and the physical word ([S-0032]).
- **programming/garbage-collection** — GC roots are exactly the stack slots and globals that pointers in this topic target; a GC language forbids arbitrary pointer arithmetic precisely because it needs precise roots.
- **programming/concurrency-primitives** — this topic's memory model is the substrate: mutexes/atomics implement the happens-before edges that make race-free programs well-defined.

If the learner places as **novice**, start with Worked example 1 and Feynman target 1 before any quiz; if **competent**, start with a prediction task ("what will this program print / what does the optimizer delete?"), then use the misconceptions list as a self-check.
