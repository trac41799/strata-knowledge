---
id: hardware/isa-basics
title: ISA Basics
band: B1
track: hardware
tier: T2
bloom_target: apply
prerequisites: [hardware/memory-hierarchy]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-isa-basics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0064, S-0068, S-0069, S-0070, S-0018, S-0040]
---

# ISA Basics — teaching

## Learning objectives (Bloom)

- **Remember** — state the RISC-V base formats (R/I/S/B/U/J), the 40-instruction RV32I set, and the SysV AMD64 argument-register order.
- **Understand** — explain the ISA as the software/hardware contract, and why ISA ≠ microarchitecture ≠ ABI.
- **Apply** (target) — decode/encode a RISC-V instruction from its bit fields; map a C function's arguments to SysV AMD64 registers.
- **Analyze** — compare RISC vs CISC encodings on decode cost, code density, and pipeline consequences; classify a reordering as consistency-model behavior.
- **Evaluate** — choose an ISA/ABI combination for a product given cost, power, density, and ecosystem constraints.

## Worked example 1 — instruction encoding decode

Decode the RISC-V I-type instruction 0xFF830293.

1. Split the 32-bit word (MSB first): `1111 1111 1000 | 00110 | 000 | 00101 | 0010011`
2. Fields: imm[11:0] = 0xFF8 = −8 (sign-extended); rs1 = 0b00110 = x6; funct3 = 0b000 = ADDI; rd = 0b00101 = x5; opcode = 0b0010011 = OP-IMM.
3. Read off: `addi x5, x6, -8` — compute x5 ← x6 + (−8).
4. Sanity: funct3 000 selects ADDI within OP-IMM; the sign-extension of 0xFF8 makes the 12-bit immediate −8, so the operation is an add of a negative constant — the encoding of a `x5 = x6 - 8` idiom.

Encoding checklist (I-type): opcode (7) | rd (5) | funct3 (3) | rs1 (5) | imm[11:0] (12) — fields are contiguous and fixed-position, which is exactly why simple RISC-V decoders are small.

## Worked example 2 — calling convention walkthrough

C: `long scale(long n) { return n * 4; }` on SysV AMD64.

1. Caller: argument n in rdi (first integer arg). Caller aligns rsp to 16 bytes at the call site.
2. Callee entry: return address pushed; body may use rax freely (caller-saved) but must preserve rbx/rbp/r12-r15.
3. Compute: `lea rax, [rdi*4]` — or the shift `shl rax, 2` — the LEA form shows addressing-mode arithmetic without a multiply. Result in rax (integer return register).
4. Caller reads rax after return. No stack frame was needed for a leaf function — it could even use the 128-byte red zone without moving rsp.

The same function on a different ABI (Microsoft x64: first arg in rcx) is the same x86-64 ISA — the ABI is the layer that differs.

## Worked example 3 — RISC vs CISC tradeoff at decode time

- RISC-V: fetch one aligned 32-bit word; field positions are fixed, so a handful of gates decode the opcode; the pipeline can start executing next cycle.
- x86: a variable-length byte stream (1-15 bytes); the decoder must find the instruction boundary before it can decode — modern x86 cores pay this with a translate-to-micro-ops stage (and huge decode bandwidth), which is why the "simple CISC core" no longer exists.
- Same program, same ISA, two implementation styles: 8086 (microcoded, no uop cache) vs modern core (uop cache, out-of-order) — ISA fixed, microarchitecture free.

## Elaboration prompts

- Why does a fixed-width encoding "simplify decode" in a way variable-width cannot, even with a big decoder budget?
- RISC-V splits the B-format immediate across two fields — why would a spec deliberately complicate the encoding? (Hint: it keeps the rs1/rs2 fields fixed, so register read can start before decode finishes.)
- If the ABI is not part of the ISA, why does a C compiler care about it at all — what breaks if two objects assume different ABIs?
- Why does the memory-consistency model belong in the ISA contract, and what would break for a kernel if it were purely an implementation property?
- x0 hardwired to zero "for free": what instructions become no-ops (e.g., `addi x0, x0, 0`), and what does that do for compilers?

## Common misconceptions

1. **"The ISA is the chip."** The ISA is a contract; a microarchitecture implements it. The same ISA has shipped on microcoded, pipelined, and out-of-order cores — binary compatibility, wildly different performance. (S-0064)
2. **"Assembly language is the ISA."** `li`, `mv`, and `call` are pseudo-instructions the assembler expands; the ISA defines machine encodings. Reading disassembly, not assembler syntax, shows the real contract. (S-0064)
3. **"RISC = fewer instructions than CISC."** RISC-V's 40 base instructions vs x86's hundreds is a side effect, not the definition: the defining axes are fixed-width encoding, load-store memory access, and a uniform register model. (S-0068, S-0069)
4. **"ARM is RISC and x86 is CISC, and the distinction still describes modern chips."** It describes the external ISA contract. Internally, modern x86 and ARM both decode to RISC-like micro-ops; the taxonomy is historical at the implementation level. (S-0064)
5. **"The calling convention is part of the ISA."** It is part of the ABI, an OS+toolchain agreement. SysV and Microsoft x64 use the same x86-64 ISA with different conventions; mixing them corrupts the stack. (S-0070)
6. **"A reordered observation means the hardware is broken."** The consistency model is part of the ISA: TSO/weak orderings are guarantees, and observing them is normal — fences and atomics are the software's job. (S-0040)

## Feynman targets

- Explain the ISA as "the API of the CPU" — what an API is to a library, an ISA is to a processor — then state where that analogy breaks (ABI, consistency model).
- Explain in ≤3 sentences why "compiled once, runs everywhere (of that ISA)" is a contract, not a coincidence.
- Explain the RISC/CISC tradeoff to a beginner using two vending machines: one that accepts any coin (CISC) vs one that accepts exact change (RISC) — then note which one the modern implementation actually contains.
- Explain why `addi x5, x6, -8` and `addi x5, x6, 8` differ only in 12 bits of immediate, and what sign-extension does for the decoder.

## Interleaving hooks

- **hardware/memory-hierarchy** (prerequisite) — instruction fetch is a sequential stream with spatial locality; fixed-width encodings make line-aligned fetch and prefetch clean; AMAT governs the instruction cache the same way it governs data.
- **hardware/cache-coherence** (upstream topic) — the consistency model cited in this pack (S-0040) is exactly what coherence protocols implement at the memory level; fences written by the compiler are the software encoding of the ISA's model.
- **systems-software/virtual-memory** — the page table is walked by hardware per the ISA's memory model; the TLB is a cache of that walk, and page faults surface as the ISA's trap mechanism.
- **programming-level follow-ups** — C `volatile`, atomics, and `std::memory_order` are the programmer-facing vocabulary of the same contract; a later "concurrency" topic reuses the TSO/weak distinction here.
