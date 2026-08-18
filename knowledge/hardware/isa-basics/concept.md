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

# ISA Basics

An instruction set architecture (ISA) is the contract between software and hardware: what the machine must execute, what state it exposes, and what behavior software may rely on — independent of how any particular chip implements it.

## 1. What an ISA is

- An ISA defines the software-visible machine: instruction set and encodings, registers, address space, word size, endianness, exceptions, and memory-access rules [T3][S-0064]
- The ISA is the boundary contract: any program written to the ISA runs on any implementation of it, without recompilation (binary compatibility) [T3][S-0064]
- The same ISA supports many microarchitectures: x86 has shipped since 1978 on cores from 8086 to today's out-of-order superscalars [T3][S-0064]
- CS2023 treats assembly-level machine organization as mandatory: AR/Assembly Level Machine Organization is a core knowledge unit (1 CS core hour + 2 KA core hours) [T2][S-0018]
- The ISA contract also includes the memory-consistency model: which access orderings software may observe (x86 TSO vs ARM/POWER weak) are architectural guarantees, not implementation accidents [T3][S-0040]

## 2. Instruction formats and encoding

- Instructions encode an opcode plus operands (registers, immediates, addresses) into fixed-size fields; how they are packed is the encoding [T3][S-0064]
- RISC-V base instructions are exactly 32 bits, aligned to 32-bit boundaries; six core formats — R, I, S, B, U, J — share field positions so hardware decodes them cheaply [T3][S-0068]
- RISC-V immediates are 12 bits, sign-extended (20 bits in U/J); the S and B formats split the immediate across two fixed fields, a deliberate decode simplification [T3][S-0068]
- RV32I defines 40 unique instructions: integer ALU, load/store, control flow, and system/synchronization (FENCE, ECALL, EBREAK) [T3][S-0068]
- RV64I keeps the same 40-instruction core and adds 64-bit register width plus word-64 variants (LD/SD, LWU, 64-bit shifts) [T3][S-0068]
- x86 is variable-length (1-15 bytes): high code density, but serial decoding; modern x86 cores translate instructions to internal micro-ops first [T3][S-0064]
- Encoding choices have hardware consequences: fixed-width, uniformly decoded RISC-V instructions are why simple pipelined implementations are feasible [T3][S-0068]

## 3. Addressing modes

- Addressing modes define how instruction operands name locations: register, immediate, base+offset (displacement), PC-relative, register-indirect [T3][S-0064]
- RISC-V covers memory only through load/store instructions with base+offset addressing; ALU operations are strictly register-register (load-store architecture) [T3][S-0068]
- Control flow is PC-relative in RISC-V: branches (B format) and jumps (J/JALR) add a signed offset to the PC, so code is position-independent by construction [T3][S-0068]
- PC-relative addressing of data comes from AUIPC (add upper immediate to PC) plus a register offset [T3][S-0068]
- CISC ISAs allow memory operands directly in ALU instructions (e.g., x86 add [mem], reg), trading code density against implementation complexity [T3][S-0069]

## 4. Registers

- An ISA exposes architectural registers — the state a program may name — typically 16-32 general-purpose registers plus the PC [T3][S-0064]
- RISC-V has 32 GPRs, x0-x31, with x0 hardwired to zero (a common source is free); register width is 32 (RV32) or 64 (RV64) bits [T3][S-0068]
- x86-64 exposes 16 GPRs — rax, rbx, rcx, rdx, rsi, rdi, rbp, rsp, r8–r15 — plus the flags register and PC [T3][S-0070]
- Register counts are a compiler-visible tradeoff: more registers reduce spills to memory but enlarge instruction encodings [T3][S-0064]
- ABI names layer onto architectural registers: RISC-V's sp, ra, gp, tp are x2, x1, x3, x4 by convention, not by hardware [T3][S-0068]

## 5. RISC vs CISC

- RISC: fixed-length instructions, load-store memory access, a large uniform register file, simple addressing — designed as a good compiler target and easy to pipeline [T3][S-0069]
- CISC: variable-length instructions, memory operands, many addressing modes, complex instructions — the 1960s-70s response to code density and immature compilers [T3][S-0069]
- Patterson & Ditzel's 1980 case for RISC: simpler hardware runs faster, compilers exploit registers better than microcode, and complex instructions were measured rarely used [T3][S-0069]
- The case was contested at the time (VAX rebuttals) and empirically validated by the Berkeley RISC-I (1982) and Stanford MIPS projects [T3][S-0069]
- The dichotomy converged: modern x86 and ARM cores both decode complex/variable ISAs into RISC-like micro-ops internally [T3][S-0064]
- RISC/CISC is now primarily about the ISA's external contract (encoding, memory operands, register model), not about raw instruction count [T3][S-0069]

## 6. Calling conventions and the ABI

- An ABI (application binary interface) is the OS+ISA agreement on calling conventions, data layout, and symbol rules — layered ON the ISA, not part of it [T3][S-0070]
- SysV AMD64 (Linux, macOS): first six integer/pointer arguments in rdi, rsi, rdx, rcx, r8, r9; remaining arguments on the stack, right-to-left [T3][S-0070]
- SysV AMD64 returns: integer in rax (rdx:rax for 128-bit), floating-point in xmm0; float/double arguments pass in xmm0-7 [T3][S-0070]
- Callee-saved registers (rbx, rbp, r12-r15) must be restored before returning; caller-saved (rax, rcx, rdx, rsi, rdi, r8-r11) may be clobbered [T3][S-0070]
- The stack grows downward; the stack pointer must be 16-byte aligned at the point of a call; a 128-byte red zone below rsp lets leaf functions skip frame setup [T3][S-0070]
- The same x86-64 ISA coexists with different ABIs (SysV vs Microsoft x64), proving the ABI is a separate contract from the ISA [T3][S-0070]

## 7. Endianness, alignment, and memory rules

- RISC-V's base is little-endian; big-endian is a nonstandard extension — endianness is an architectural property programs depend on [T3][S-0068]
- Unaligned loads/stores are permitted by the RISC-V spec but handling is implementation-defined: hardware may support them or trap to a software handler [T3][S-0068]
- Word size is part of the ISA contract: the same ISA family (RV32 vs RV64) is a different architectural contract for programs [T3][S-0068]

## Boundaries / common misunderstandings

- ISA ≠ microarchitecture: the ISA is the contract, the microarchitecture is the implementation — the same ISA, same code, can span orders of magnitude in speed and power [T3][S-0064]
- Assembly language is not machine code: pseudo-instructions (li, mv, call) and labels are assembler conveniences that expand to real encodings; the ISA defines the encodings [T3][S-0064]
- RISC vs CISC is not "few vs many instructions": RISC-V's 40 base instructions vs x86's hundreds — the real differences are encoding uniformity, memory operands, and register model [T3][S-0068][S-0069]
- An ISA does not dictate performance: implementations choose pipelines, caches, and speculation; the ISA only fixes the observable contract [T3][S-0064]
- The ABI is not part of the ISA: SysV and Microsoft x64 are different calling conventions for the same x86-64 ISA, and a binary built for one may not run under the other [T3][S-0070]
- RISC-V is an open ISA standard, not a chip: implementations range from tiny microcontroller cores to server-class SoCs, all running the same contract [T3][S-0068]
- The consistency model is part of the ISA contract, not a hardware bug: observing a store-load reorder on x86 is legal TSO behavior, not a coherence failure [T3][S-0040]

## References (evidence records)

- S-0064 — Patterson & Hennessy (2021), Computer Organization and Design RISC-V Edition, 2nd ed.
- S-0068 — Waterman & Asanović (eds.) (2019), The RISC-V Instruction Set Manual, Vol. I: User-Level ISA, v20191213 (ratified)
- S-0069 — Patterson & Ditzel (1980), The Case for the Reduced Instruction Set Computer, ACM SIGARCH CAN 8(6):25-33
- S-0070 — x86-64 psABI v1.0 (2021), System V ABI — AMD64 Architecture Processor Supplement
- S-0018 — ACM/IEEE-CS/AAAI (2024), CS2023 — AR/Assembly Level Machine Organization core unit
- S-0040 — Sorin, Hill & Wood (2011), A Primer on Memory Consistency and Cache Coherence
