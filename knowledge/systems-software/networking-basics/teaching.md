---
id: systems-software/networking-basics
title: Networking Basics
band: B2
track: systems-software
tier: T2
bloom_target: apply
prerequisites: []
related: []
recommended: []
status: published
schema-version: 1
owner: l1-networking-basics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0088, S-0089, S-0090, S-0018]
---

# Networking Basics — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: name the four Internet layers (application, transport, internet, link), the two principal transports (TCP, UDP), and the address types at each layer (ports, 32-bit IPv4, 128-bit IPv6, link-layer/Ethernet addresses). [T2][S-0088][S-0090]
- **understand**: explain what encapsulation is, why IP alone guarantees nothing, and how DNS's hierarchy plus TTLs make resolution fast yet eventually consistent. [T2][S-0088][S-0089]
- **apply**: given a message, produce the segment/datagram/frame chain with the correct addressing at each layer; given a transport need, choose TCP or UDP. [T2][S-0088]
- **analyze**: diagnose addressing and layering errors in traces (wrong-layer state, DNS staleness, port-vs-host confusion). [T2][S-0088][S-0089]

## Worked example — one packet, hop by hop (packet walkthrough)

Setup: a laptop at 192.168.1.10 sends `GET /index.html` to `www.example.com`. Walk each layer.

1. **Application — DNS first.** The browser must turn `www.example.com` into an address. It sends a DNS query (over UDP, port 53 convention) to its resolver; the resolver follows the hierarchy (root → .com → example.com zones) or answers from cache. Answer: `www.example.com → 203.0.113.7` (TTL-bounded cache). No address is carried inside the HTTP message itself — host names are resolved before transmission. [S-0089]
2. **Transport.** The browser opens a TCP connection to (203.0.113.7, 80) — well-known port 80 for HTTP — so the segment headers carry source port (ephemeral, e.g., 54321) and destination port 80. TCP provides reliability: sequencing, retransmission, flow control. [S-0088]
3. **Internet.** IP wraps each segment in a datagram with source 192.168.1.10 and destination 203.0.113.7 (32-bit IPv4 addresses). IP itself is connectionless: this datagram may be damaged, duplicated, reordered, or lost — TCP above it will fix that. [S-0088]
4. **Link.** The laptop resolves the next hop (its gateway 192.168.1.1) via ARP to a link-layer address, then wraps the datagram in an Ethernet frame (MTU 1500). The frame's source/destination fields are link-layer addresses, which change at every hop — the IP datagram inside does not. [S-0088]
5. **The server.** Each layer strips its header and hands the payload up; demultiplexing happens by frame type (Ethernet), protocol field (IP), and port number (TCP). The application receives the original message. Same walkthrough works over IPv6 (128-bit addresses, hex text form, link-local addressing per interface). [S-0088][S-0090]

Evidence: [S-0088][S-0089][S-0090]

## Elaboration prompts

- Why does a TCP segment need both a source and a destination port when the connection's IP addresses already identify both hosts? (Hint: how many processes may share one host?) [T2][S-0088]
- Encapsulation adds headers on the way down and strips them on the way up — why can a router not just forward the datagram without touching the frame? [T2][S-0088]
- DNS answers are cached with TTLs; what would break if TTL were ignored (0 or forever)? What does this imply about deploying a DNS change? [T2][S-0089]
- If IP is best-effort, why do we still speak of "network reliability"? Where does the guarantee actually live? [T2][S-0088]
- IPv6 introduced mandatory link-local addresses — why would an interface that only talks to the local network still need a globally-formatted address scheme at all? [T2][S-0090]

## Common misconceptions

1. **"TCP/IP is a single protocol."** It is a layered suite: IP, ICMP, ARP, TCP, UDP, DNS, and more — each layer has its own protocol(s), and "TCP/IP" is shorthand for the stack. [T2][S-0088]
2. **"IP guarantees delivery, so TCP just adds ports."** IP is connectionless with no end-to-end guarantees; TCP adds reliability (sequencing, retransmission, flow control) on top — ports are only one of its jobs. [T2][S-0088]
3. **"The OSI 7-layer model and TCP/IP are the same thing."** They are different frameworks: the Internet suite has four layers and no separate session/presentation layers; RFC 1122 explicitly contrasts the two. [T2][S-0088]
4. **"DNS is a central directory maintained by one authority."** The name space is a distributed tree; authority is delegated per zone, and answers commonly come from caches with bounded TTLs. [T2][S-0089]
5. **"Well-known ports are a security boundary."** They are a registration convention (ports 0–255 for standardized services); nothing stops an application from using another port, so security must not assume otherwise. [T2][S-0088]

## Feynman targets

Explain, in plain language a non-engineer could follow:

- Why a letter sent over the Internet is wrapped in multiple envelopes, each opened by a different post office, and why the addresses on the envelopes differ from the addresses inside.
- Why asking "one big directory" for a website's address would not scale, and why the answer you get is sometimes slightly out of date.
- Why two computers can talk to each other even though the number used to reach them (IPv4/IPv6) and the number used to reach a program on them (port) are different things.

## Interleaving hooks

- **systems-software/http-basics (prerequisite for the next topic)**: HTTP is an application-layer protocol that rides on exactly this stack — sockets and ports are where HTTP requests enter TCP.
- **systems-software/http-caching**: every revalidation round-trip costs a full network path (RTT); caching exists because round trips are expensive at every layer.
- **hardware/isa-basics (sibling band B1)**: framing and demultiplexing mirror instruction decoding — fields in a fixed envelope tell the receiver which handler to dispatch to.
