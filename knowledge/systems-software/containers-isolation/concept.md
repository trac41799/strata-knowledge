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

# Containers & Isolation

## Claims

### Namespaces: the isolation mechanism

- A Linux namespace wraps a global system resource in an abstraction so that processes inside it appear to have their own isolated instance of that resource; changes to the resource remain visible to other namespaces. [T3][S-0123]
- Linux provides namespace types for cgroup, IPC, network, mount, PID, time, UTS, and user resources; a namespace is created or joined with the CLONE_NEW* flags of clone(2), unshare(2), and setns(2). [T3][S-0123]
- PID namespaces isolate the process-ID number space, so processes in different PID namespaces can have the same PID; PIDs in a new PID namespace start at 1, giving a container its own self-contained process tree. [T3][S-0123]
- Mount namespaces isolate the list of mounts a process can see, so container mounts and container root filesystems do not appear in the host's mount table. [T3][S-0123]
- Network namespaces isolate network devices, stacks, and ports, so each container has an independent network view (own interfaces, IP addressing, routing). [T3][S-0123]
- User namespaces map UID/GID ranges between namespaces via uid_map/gid_map, so a process can be UID 0 inside its user namespace without holding the corresponding host privilege. [T3][S-0123]
- There is no single kernel object called a "container": a container is a set of processes created with new namespaces (CLONE_NEW* flags) plus cgroup membership, so the kernel's per-process isolation primitives are composed rather than replaced. [T3][S-0123]
- OS-level virtualization (containers) is codified curriculum content: CS2023's Operating Systems knowledge area includes a Virtualization unit, and its competencies cover deployment on "virtualized operating system/container" runtimes. [T2][S-0018]

### Cgroups: resource limits and accounting

- Control groups (cgroups) constrain and account the resource usage of groups of processes; the cgroups v2 controllers include cpu, memory, io, and pids. [T3][S-0123]
- cgroups v2 mounts all controllers in a single unified hierarchy, in contrast to v1's multiple independent hierarchies. [T3][S-0123]
- The v2 memory controller exposes memory.max (hard limit) and memory.high (throttling threshold) per cgroup; when the hard limit is exceeded the kernel reclaims memory or OOM-kills processes in that cgroup. [T3][S-0123]
- The v2 cpu controller provides cpu.max (quota/period) and cpu.weight (relative share) controls. [T3][S-0123]
- Container engines place each container's processes in its own cgroup, so configured memory and CPU limits are enforced by the kernel rather than voluntarily by the runtime. [T3][S-0123]

### Root filesystem: chroot(2) vs pivot_root(2)

- chroot(2) only changes the calling process's root directory: it leaves the working directory unchanged, does not isolate the mount table, and — per the manual page — the superuser can escape a chroot "jail" (e.g., mkdir foo; chroot foo; cd ..), so chroot is not an isolation or security boundary. [T3][S-0123]
- pivot_root(2) moves the old root to put_old and makes new_root the process's root, so the old root can subsequently be unmounted; the manual page documents its use to set up a root filesystem during container creation. [T3][S-0123]
- Container runtimes switch root inside a new mount namespace with pivot_root rather than plain chroot, so the host's filesystem tree is not reachable from inside the container. [T3][S-0123]

### Images and filesystem layering

- An OCI image is an ordered collection of root-filesystem changes (layers) plus the execution parameters; layers are referenced by content descriptors in a Merkle DAG, so identical layers are stored and transferred once and shared across images. [T2][S-0122]
- An OCI image is unpacked into an OCI runtime bundle, which an OCI runtime then executes per the runtime-spec: the spec defines the bundle layout, the configuration schema (process, root filesystem, mounts, and Linux namespaces, cgroup path, and resource limits), and the runtime lifecycle. [T2][S-0122]
- OverlayFS combines a read-only lowerdir with a writable upperdir into a single merged view; the first modification of a lower-layer file copies it (and its parent directories) into the upper layer — copy-up — leaving the lower layer untouched. [T3][S-0123]
- OverlayFS supports multiple lower layers (colon-separated lowerdirs); container engines stack image layers as lowerdirs and give each container a fresh upperdir as its writable layer. [T3][S-0123]
- Container images are stored in registries, which are effectively file storage for images wrapped in APIs for pushing, tagging, and pulling (NIST SP 800-190). [T2][S-0124]

### Containers vs virtual machines

- Containers are not lightweight VMs: a container shares the host kernel and is isolated by namespaces and cgroups, whereas a VM virtualizes hardware and runs its own guest kernel; the kernel is therefore a common attack surface for every container on a host. [T2][S-0124]
- Because the container boundary is kernel-mediated rather than a hardware-virtualization boundary, NIST treats the shared-kernel surface as a distinct risk class requiring hardening (privilege minimization, secure runtime configuration, patching). [T2][S-0124]

### Security boundaries

- NIST SP 800-190 organizes container security risks across the lifecycle: image, registry, orchestrator, container, and host OS, each with its own risk categories and countermeasures. [T2][S-0124]
- Vulnerabilities in the runtime software are especially damaging in containers: a vulnerability in the kernel or runtime can be exploited to escape the container and attack the host or other containers. [T2][S-0124]
- Insecure runtime configurations — such as containers permitted to mount sensitive host directories or run with excessive capabilities — enlarge the escape surface; NIST's countermeasures include least-privilege runtime configuration and orchestrator policy. [T2][S-0124]

## Boundaries / common misunderstandings

- "Containers are lightweight VMs": incorrect — containers share the host kernel; a kernel exploit crosses every container on the host, while a VM escape must additionally cross the hypervisor boundary. [T2][S-0124]
- "chroot is container isolation": chroot is only a root-directory change, escapable by privileged processes and without mount isolation; containers combine namespaces, cgroups, and pivot_root. [T3][S-0123]
- "A container is a process": a container is a process tree running in its own namespaces and cgroup; the kernel has no container object. [T3][S-0123]
- "Namespaces are a security mechanism": they isolate views of resources; security depends on the whole configuration (capabilities, mounts, hardened runtime, patched kernel), and NIST treats the boundary as attackable. [T2][S-0124]
- "The container's root filesystem is a copy of the host's": it is assembled from read-only image layers plus a writable upper layer, and the host tree is excluded via mount namespace plus pivot_root. [T3][S-0123]

## References (evidence records)

- S-0018 — CS2023 (ACM/IEEE-CS/AAAI, 2024): Virtualization knowledge unit in the OS KA; container competencies. (T2)
- S-0122 — OCI runtime-spec v1.2 + image-spec v1.1 (Open Container Initiative, 2024): bundle/config/lifecycle, layered content-addressed images. (T2)
- S-0123 — Linux man-pages 6.18 (Kerrisk, 2026): namespaces(7), cgroups(7), chroot(2), pivot_root(2), overlayfs. (T3)
- S-0124 — NIST SP 800-190 (2017): container security lifecycle, shared-kernel risk, escape surface. (T2)
