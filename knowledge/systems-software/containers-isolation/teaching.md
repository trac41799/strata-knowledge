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

# Containers & Isolation — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember** — list the Linux namespace types and the CLONE_NEW* flags that create them, and name the cgroups v2 controllers ([S-0123]).
- **understand** — explain why chroot(2) is not an isolation boundary and why runtimes use pivot_root(2) in a new mount namespace ([S-0123]).
- **understand** — explain the difference between a container and a VM at the isolation boundary (shared kernel vs hypervisor) and its security consequence ([S-0124]).
- **apply** — walk the kernel-level setup of a container: namespace flags, cgroup files, pivot_root, overlayfs assembly of the root filesystem ([S-0123], [S-0122]).
- **apply** — review a container deployment for escape-surface risks and map countermeasures using the NIST lifecycle categories ([S-0124]).
- **analyze** — compare the blast radius of kernel vs hypervisor boundaries for a given workload's isolation requirements.

## Worked example 1 — starting a container by hand

Goal: run one container process isolated from the host, with a 512 MiB memory cap and its own root filesystem. What the runtime actually does:

1. **Namespaces** — clone the init process with `CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS | CLONE_NEWUTS` (plus `CLONE_NEWUSER` with a uid_map/gid_map when unprivileged). The child becomes PID 1 of a fresh PID namespace, sees an empty mount table, a new network stack, and its own hostname ([S-0123]).
2. **Filesystem** — assemble the root from the image: the image's layers become overlayfs lowerdirs, a fresh empty upperdir is created for the container, and the runtime mounts `-t overlay -olowerdir=layer1:layer2:layer3,upperdir=...,workdir=... /merged` ([S-0123], [S-0122]).
3. **pivot_root** — inside the new mount namespace, pivot_root into the merged view, moving the old (host) root to put_old and unmounting it, so the host tree is unreachable ([S-0123]).
4. **Cgroup** — `mkdir /sys/fs/cgroup/ctr-1`, write `512MiB` to `memory.max` (and `cpu.max` if desired), then write the init PID to `cgroup.procs`; the kernel now enforces the limit ([S-0123]).
5. **Exec** — `execve` the bundle's init binary. From the inside this looks like a tiny standalone machine; from the outside it is one process tree with kernel-enforced limits.

## Worked example 2 — image layers and copy-up

`Dockerfile`: FROM base (layer 1) → apt install (layer 2) → COPY app (layer 3). Pulling the image downloads each layer once (content-addressed digests); two images sharing `base` share its storage ([S-0122]). At run time the layers are read-only lowerdirs; the container's writes land in its own upperdir. First write to a lower file: overlayfs copy-up copies the file (and parents) into the upperdir, then applies the change — the base layers are never mutated, which is why a container can "delete" a file from its image (whiteout) or write anywhere without affecting other containers ([S-0123]).

## Elaboration prompts

- Why can't a container with its own mount namespace still see the host's `/proc`? What must the runtime mount inside the namespace instead, and why does that matter for `ps` output?
- User namespaces map UID 0 to an unprivileged host UID — what does that imply about file permissions on shared/host volumes? (Root in the container is not root on the host.)
- cgroups v2 memory.high throttles while memory.max kills: when would you set only memory.high, and what would a runaway container do then?
- The OCI runtime-spec lists namespaces, cgroups path, and resource limits in the config — which of these can a non-root runtime still set, and which require privilege?
- If overlayfs copy-up happens on first write, what is the performance cost of writing to a large lower-layer file, and how do storage drivers mitigate it?

## Common misconceptions

1. **"Containers are lightweight VMs."** Containers share the host kernel; the isolation boundary is namespaces/cgroups, not a hypervisor. A kernel exploit crosses all containers on a host — VMs add a hardware boundary at higher overhead. [S-0124]
2. **"chroot = isolation."** chroot(2) changes only the root directory: no mount isolation, no working-directory change, and privileged escape is documented ("chroot foo; cd .."). Real containers use namespaces + cgroups + pivot_root. [S-0123]
3. **"A container is a single process."** It is a process tree: init is PID 1 in its namespace and forks/execs children; all inherit the same namespaces and cgroup. [S-0123]
4. **"Namespaces alone are a security boundary."** They isolate views of resources; escape risk depends on the whole configuration (capabilities, mounted host directories, runtime bugs, kernel CVEs). NIST treats container isolation as attackable and prescribes hardening. [S-0124]
5. **"The container root filesystem is a copy of the host's."** It is assembled from read-only image layers plus a writable upper layer; the host tree is excluded by the mount namespace and pivot_root. [S-0123]
6. **"Memory limits are the runtime's job."** The runtime only writes cgroup files; the kernel enforces limits (memory.max → reclaim/OOM within the cgroup). [S-0123]

## Feynman targets

- "Explain to a junior engineer why two containers on the same host cannot see each other's processes or files, in two sentences each for namespaces, cgroups, and pivot_root."
- "Explain why a kernel CVE is a cross-container problem but a VM guest CVE usually is not" ([S-0124]).
- "Explain what 'image layering' buys you, using pull-times, shared base layers, and copy-up" ([S-0122], [S-0123]).
- "Explain why `chroot` was never enough, using one command an attacker can run" ([S-0123]).

## Interleaving hooks

- **systems-software/virtual-memory** — per-process page tables are the memory-isolation primitive; cgroups add aggregate limits on top. Recall R3 of the virtual-memory pack, which asks exactly this.
- **systems-software/os-processes** — containers are process trees: clone flags, fork/exec, PID 1, cgroup membership per process group.
- **systems-software/networking-basics** — network namespaces + veth pairs give each container its own network stack; revisit socket and interface semantics inside a namespace.
- **systems-software/os-scheduling** — cpu.max/cpu.weight are scheduling knobs: cgroups change the CPU-sharing policy among process groups on the same kernel.
