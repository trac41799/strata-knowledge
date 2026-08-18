---
id: systems-software/containers-isolation
title: Containers & Isolation
band: B3
track: systems-software
tier: T2
bloom_target: apply
prerequisites: [systems-software/virtual-memory, systems-software/os-processes]
related: [systems-software/virtual-memory]
recommended: []
status: published
schema-version: 1
owner: l1-containers-isolation
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0018, S-0122, S-0123, S-0124]
---

# Containers & Isolation — validation

## Formative (practice)

### F1 — remember: namespace types
- Q: Which Linux namespaces isolate the following resources, and which CLONE_NEW* flag family creates them: process IDs, network devices/stacks/ports, the list of mounts, and UID/GID mappings?
- bloom: remember
- bank: formative
- A: PID (CLONE_NEWPID), network (CLONE_NEWNET), mount (CLONE_NEWNS), and user (CLONE_NEWUSER); namespaces are created or joined via clone(2), unshare(2), and setns(2). Other namespace types: cgroup, IPC, time, UTS.
- evidence: [S-0123]
- topic: systems-software/containers-isolation

### F2 — remember: cgroups v2
- Q: What changed between cgroups v1 and v2, and which v2 controllers exist (name at least three)?
- bloom: remember
- bank: formative
- A: v2 mounts all controllers in a single unified hierarchy (v1 allowed multiple independent hierarchies). Controllers include cpu, memory, io, and pids.
- evidence: [S-0123]
- topic: systems-software/containers-isolation

### F3 — understand: chroot vs pivot_root
- Q: Why do container runtimes use pivot_root(2) instead of chroot(2) when setting up the container root filesystem?
- bloom: understand
- bank: formative
- A: chroot only changes the process's root directory: the working directory is unchanged, the mount table is not isolated, and a privileged process can escape the "jail" (e.g., chroot then cd ..). pivot_root, executed inside a new mount namespace, moves the old root to put_old so it can be unmounted — the host tree is then unreachable from inside the container.
- evidence: [S-0123]
- topic: systems-software/containers-isolation

### F4 — understand: container vs VM
- Q: What does a container share with its host that a VM does not, and what security consequence follows?
- bloom: understand
- bank: formative
- A: The kernel. A VM runs a guest kernel on virtualized hardware (hypervisor boundary); a container is isolated by namespaces and cgroups but executes on the shared host kernel. A kernel vulnerability is therefore a common attack surface for every container on the host (NIST SP 800-190).
- evidence: [S-0124]
- topic: systems-software/containers-isolation

### F5 — apply: overlayfs layering
- Q: An image has three layers; the container writes /app/config.json, a file present in layer 1. What filesystem regions exist at runtime and what happens on that first write?
- bloom: apply
- bank: formative
- A: The three image layers are the read-only lowerdirs; the container gets an empty writable upperdir; overlayfs presents a merged view. The first write triggers copy-up: /app/config.json (and its parent directories) are copied into the upperdir, then modified there; the lower layers stay untouched, so other containers sharing the image are unaffected.
- evidence: [S-0123]
- topic: systems-software/containers-isolation

## Summative (mastery checkpoint)

### S1 — apply: container startup walk
- Q: Design the kernel-level setup for a container that must see only its own PID space, its own network interface, its own mount table, and be capped at 512 MiB of RAM. Enumerate the namespace flags, the cgroup files written, and the root-filesystem step.
- bloom: apply
- bank: summative
- A: Create the process with CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS (plus CLONE_NEWUSER with a uid_map if running unprivileged); place it in a cgroup: mkdir a cgroup, write 512MiB to memory.max (and optionally cpu.max); switch root inside the new mount namespace using pivot_root into the merged overlayfs view of the bundle; exec the container init, which becomes PID 1 in the PID namespace.
- evidence: [S-0123]
- topic: systems-software/containers-isolation

### S2 — apply: escape-surface review
- Q: A deployment runs containers with the host's /var/lib/docker mounted read-write and with full capabilities. Using NIST SP 800-190's risk categories, identify the risk classes and the countermeasures you would apply.
- bloom: apply
- bank: summative
- A: Risks: insecure runtime configuration (sensitive host directory mounted writable; excessive capabilities), which enlarge the escape surface; runtime/kernel vulnerabilities become cross-container attacks. Countermeasures: least-privilege configuration (drop capabilities, read-only host mounts, seccomp-style filtering where available), runtime patching, and orchestrator-level policy restricting mounts and privileges.
- evidence: [S-0124]
- topic: systems-software/containers-isolation

### S3 — analyze: threat-model comparison
- Q: Compare the blast radius of a kernel exploit in a containerized workload versus a VM workload on the same host. What does each boundary add?
- bloom: analyze
- bank: summative
- A: In containers the shared kernel is the boundary: one kernel exploit can compromise the host and every container on it, so hardening (capabilities, mounts, patching) and patching cadence are first-order controls. In VMs the guest kernel is separated by the hypervisor, so a guest-kernel exploit is contained unless the hypervisor itself is vulnerable — a stronger but more expensive boundary. The analysis determines whether the workload's isolation requirements are met by namespaces/cgroups or need hardware virtualization.
- evidence: [S-0123, S-0124]
- topic: systems-software/containers-isolation

## Review (spaced repetition — interleaved with prerequisites)

### R1 — understand (virtual-memory): two isolation layers
- Q: Two containers share the host kernel. Where does memory isolation between their processes actually live, and what does a cgroup memory limit add?
- bloom: understand
- bank: review
- A: Per-process page tables and protection bits: each process has its own virtual address space and PTEs, so one process cannot touch another's frames. A cgroup memory.max limit adds aggregate accounting and enforcement (reclaim/OOM-kill at the cgroup level) — a different mechanism layered on top of page-table isolation.
- evidence: [S-0032, S-0123]
- topic: systems-software/virtual-memory

### R2 — understand (os-processes): containers are process trees
- Q: How does the OS process model (fork/exec) relate to starting a container?
- bloom: understand
- bank: review
- A: A container is a process tree, not a new OS instance: the init process is created with clone(2) namespace flags (PID 1 in its namespace), children are forked/exec'd normally, and every process inherits the container's namespaces and cgroup membership. There is no kernel "container" object.
- evidence: [S-0018, S-0123]
- topic: systems-software/os-processes

### R3 — apply (virtual-memory): OOM at the limit
- Q: A container hits its memory.max and processes are OOM-killed. Explain what the kernel does at that boundary and why page-table isolation still holds for the surviving processes.
- bloom: apply
- bank: review
- A: The cgroup memory controller reclaims memory within the cgroup and, when the hard limit is still exceeded, OOM-kills processes in that cgroup (memory.events reports the events). Surviving processes keep private address spaces enforced by their PTEs — cgroup limits bound aggregate usage; page tables bound per-process access.
- evidence: [S-0032, S-0123]
- topic: systems-software/virtual-memory
