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

# ISA Basics — validation

Format: `Q` / `bloom` / `bank` / `A` / `evidence` (spec §7). Banks: formative
(practice), summative (mastery, ≥80% at bloom_target), review (spaced,
interleaved with prerequisites).

## Formative (practice)

- Q: Which RISC-V register is hardwired to zero, and how many GPRs does the architecture expose?
- bloom: remember
- bank: formative
- A: x0 is hardwired to zero; RISC-V exposes 32 GPRs, x0-x31 (x0 is a read-only zero source).
- distractors: x1 / x31 / There is no zero register in RISC-V.
- evidence: [S-0068]
- topic: hardware/isa-basics

- Q: A program compiled once for x86-64 runs unmodified on a 2010 core and a 2025 core. What does this tell you about the ISA vs the microarchitecture?
- bloom: understand
- bank: formative
- A: The ISA is the stable contract between software and hardware: binary compatibility holds as long as the implementation honors the ISA. The two cores are different microarchitectures (pipelines, caches, speculation) implementing the same ISA.
- distractors: It means both chips are the same microarchitecture / It means the ISA was redefined by the newer chip / It only works because of JIT compilation.
- evidence: [S-0064]
- topic: hardware/isa-basics

- Q: In a load-store ISA like RISC-V, how does an ALU instruction obtain its operands, and where do memory values enter the computation?
- bloom: understand
- bank: formative
- A: ALU instructions operate only on registers; memory values enter via explicit load instructions into registers, and results leave via stores. No ALU instruction touches memory directly.
- distractors: ALU instructions can read memory operands directly / All operands are immediates / Memory is accessed only by the OS.
- evidence: [S-0068]
- topic: hardware/isa-basics

- Q: Under the SysV AMD64 ABI, which registers carry the first three integer arguments of a function call?
- bloom: remember
- bank: formative
- A: rdi, rsi, rdx (then rcx, r8, r9 for arguments 4-6; the remainder go on the stack).
- distractors: rax, rbx, rcx / r8, r9, r10 / All arguments go on the stack.
- evidence: [S-0070]
- topic: hardware/isa-basics

## Summative (mastery checkpoint)

- Q: Decode the 32-bit RISC-V instruction 0xFF830293 (I-type): extract imm[11:0], rs1, funct3, rd, and opcode, and state what instruction it is.
- bloom: apply
- bank: summative
- A: Binary 1111 1111 1000 0011 0000 0010 1001 0011. Fields: imm[11:0]=0xFF8 (sign-extended −8), rs1=00110 (x6), funct3=000 (ADDI), rd=00101 (x5), opcode=0010011 (OP-IMM). Instruction: addi x5, x6, -8.
- distractors: add x5, x6, x7 / sw x5, -8(x6) / lui x5, 0xFF8.
- evidence: [S-0068]
- topic: hardware/isa-basics

- Q: On SysV AMD64, where do the arguments of `void f(int a, char *b, long c, int d, void *e, int g, int h)` land? Which registers must `f` preserve?
- bloom: apply
- bank: summative
- A: a→rdi, b→rsi, c→rdx, d→rcx, e→r8, g→r9, h→stack (7th argument). f must preserve the callee-saved registers rbx, rbp, r12-r15 (and rsp alignment), and may clobber rax, rcx, rdx, rsi, rdi, r8-r11.
- distractors: All arguments on the stack / a→rax, b→rbx, c→rcx / f must preserve rdi, rsi, rdx.
- evidence: [S-0070]
- topic: hardware/isa-basics

- Q: RISC-V encodes `addi x5, x6, -8` as 0xFF830293 (verify) and `addi x5, x6, 8` as 0x00830293. Which immediate is harder to decode, and what does the field layout of I-type say about that?
- bloom: apply
- bank: summative
- A: Encoding −8: imm bits are all ones, sign-extended from the 12-bit field. The I-type layout (imm[11:0] | rs1 | funct3 | rd | opcode) keeps the immediate contiguous for I-type, so both decode identically: take bits 31:20, sign-extend, done. (The S/B formats split the immediate across fields — that is where decode gets interesting.)
- distractors: Positive immediates are harder / The immediate is encoded in two's complement, so −8 needs special handling / imm[11:0] must be shifted before use.
- evidence: [S-0068]
- topic: hardware/isa-basics

- Q: A microcontroller vendor offers you a processor with an ISA whose instructions are variable-length (1-15 bytes) with memory operands, and one with a fixed 32-bit load-store ISA. Which do you choose for a low-power embedded design, and why?
- bloom: evaluate
- bank: summative
- A: The fixed-width load-store ISA (RISC-V class): uniform 32-bit encoding makes decode simple and the pipeline short, register-register ALU avoids repeated memory traffic, and the small base set fits in a tiny decoder — better power/area, at the cost of code density (mitigated by a compressed-extension variant). Choose the CISC-style only if code density or legacy compatibility dominates.
- distractors: The CISC one, more instructions means more power / Either, ISAs do not affect power / The RISC one, because RISC is always faster in every metric.
- evidence: [S-0068, S-0069]
- topic: hardware/isa-basics

- Q: An x86-64 program observes: core A stores to flagA, then loads flagB, and sees the OLD value of flagB while B concurrently stores flagB then loads flagA and sees the old flagA. Is this an ISA violation on x86-64? What layer of the ISA contract governs this?
- bloom: analyze
- bank: summative
- A: Not a violation: it is the TSO behavior the ISA permits (a load may pass an older store). The memory-consistency model is part of the ISA contract; making the program behave sequentially requires fences or acquire/release synchronization. This is a consistency-model fact, not a coherence bug.
- distractors: The ISA guarantees sequential consistency, so hardware is broken / Only the OS can observe this / This proves x86 is not a valid ISA.
- evidence: [S-0040]
- topic: hardware/isa-basics

## Review (spaced repetition — interleaved with prerequisites)

- Q: (memory-hierarchy) A 32 KB, 8-way cache with 64-byte lines on a 32-bit address space: how many sets, and how many bits per address for tag/index/offset?
- bloom: apply
- bank: review
- A: Sets = 32 KB / (64 × 8) = 64; index = 6 bits, offset = 6 bits, tag = 32 − 12 = 20 bits.
- distractors: 256 sets / tag = 16 bits / offset = 5 bits.
- evidence: [S-0063]
- topic: hardware/isa-basics

- Q: (memory-hierarchy) Why does sequential instruction fetch make a small instruction cache effective, and how would a variable-length ISA change the fetch pattern vs a fixed-width one?
- bloom: understand
- bank: review
- A: Sequential fetch has strong spatial locality — consecutive lines are touched in order, so a small cache holds the active code window. Fixed-width encodings align fetches to word boundaries and predictable block counts per line; variable-length ISAs require parsing from the start of the line, and the next instruction may straddle a block boundary, complicating line-aligned prefetch.
- distractors: Instruction caches rely on temporal locality only / Variable-length ISAs fetch exactly one line per instruction / The ISA does not affect fetch.
- evidence: [S-0064]
- topic: hardware/isa-basics

- Q: (memory-hierarchy) A kernel routine's hot loop misses L1 40% of the time but the working set fits in L2. Which AMAT lever would you pull, and why is that an ISA-adjacent concern for the instruction cache?
- bloom: analyze
- bank: review
- A: Pull the miss-penalty lever for the L1→L2 path (or restructure so the hot loop stays in L1). For the instruction cache the same reasoning applies: instruction-fetch misses stall the pipeline, so code layout (hot path contiguity, alignment) is a programmer-visible lever — the ISA's encoding width shapes how much code fits per line.
- distractors: Reduce hit time by shrinking the cache / Increase block size past the working set / Miss rate is fixed by hardware.
- evidence: [S-0063]
- topic: hardware/isa-basics
