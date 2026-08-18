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

# Networking Basics — validation

## Formative (practice)

### Q1
- Q: Name the four protocol layers of the Internet architecture as defined by RFC 1122, and state which transport protocols sit in the transport layer.
- bloom: remember
- bank: formative
- A: Application, transport, internet, and link. The transport layer holds TCP (reliable, connection-oriented) and UDP (connectionless datagram service).
- evidence: [S-0088]
- topic: systems-software/networking-basics

### Q2
- Q: Why is it inaccurate to say "TCP/IP is a single protocol"? What does the name actually denote?
- bloom: understand
- bank: formative
- A: TCP/IP denotes the layered Internet protocol suite — many cooperating protocols (IP, ICMP, ARP, TCP, UDP, DNS, SMTP, ...), at least one per layer. "TCP" and "IP" are just the best-known members of the suite.
- evidence: [S-0088]
- topic: systems-software/networking-basics

### Q3
- Q: Your application needs (a) ordered, loss-free delivery of a large file and (b) fast, loss-tolerant streaming where each message is independent. Which transport do you pick for each, and why?
- bloom: apply
- bank: formative
- A: (a) TCP — reliable connection-oriented service with end-to-end reliability, resequencing, and flow control. (b) UDP — connectionless datagram service; it does not retransmit or reorder, which fits loss-tolerant streaming. IP alone is never the answer: it provides no delivery guarantees.
- evidence: [S-0088]
- topic: systems-software/networking-basics

### Q4
- Q: A packet leaves your laptop for www.example.org. List the addresses present at each of the four layers of the stack (name the address type and what it identifies).
- bloom: apply
- bank: formative
- A: Application: no address (host names are resolved by DNS before transmission). Transport: source and destination port numbers (identify processes). Internet: source and destination IP addresses (32-bit IPv4 or 128-bit IPv6; identify hosts). Link: source and destination Ethernet addresses (identify interfaces on the directly-connected network), with ARP used to resolve the next hop's link-layer address.
- evidence: [S-0088][S-0089]
- topic: systems-software/networking-basics

## Summative (mastery checkpoint)

### Q5
- Q: Trace the full path of one HTTP GET from a browser to a server two routers away: for each step name the protocol involved and the unit of data (message/segment/datagram/frame) being handled.
- bloom: apply
- bank: summative
- A: 1) DNS resolution (DNS messages over UDP/TCP, port 53 convention) maps the host name to an IP address — possibly from a TTL-bounded cache. 2) The application forms the HTTP request (message). 3) TCP segments it (segment) with source/destination ports. 4) IP wraps each segment in a datagram (32-bit IPv4 or 128-bit IPv6 addresses). 5) The link layer wraps each datagram in a frame (Ethernet addresses, MTU 1500 on Ethernet) for each hop; each router strips the frame, reads the datagram's destination IP, and re-frames for the next link. 6) At the server, each layer strips its header and demultiplexes (frame type → protocol field → port) until the application receives the request.
- evidence: [S-0088][S-0089]
- topic: systems-software/networking-basics

### Q6
- Q: A colleague says: "I don't need DNS caching to be clever — the answer is either right or wrong, and the source of truth never lies." Explain what TTLs and caching exist for, and the failure mode of ignoring TTLs.
- bloom: analyze
- bank: summative
- A: DNS is a distributed hierarchy: answers come from zones owned by different servers, and resolving through the whole chain on every request is expensive. TTLs bound how long a resource record may be cached before discard, trading lookup latency against freshness. Ignoring TTLs (caching "forever") means stale records — including changed addresses or retired names — keep being served to clients, so DNS changes fail to propagate.
- evidence: [S-0089]
- topic: systems-software/networking-basics

### Q7
- Q: A developer claims "IPv6 is just IPv4 with 96 more bits, so I can port my code by swapping the address type." Identify what the address-model changes are beyond width, and one operational consequence of each.
- bloom: analyze
- bank: summative
- A: Beyond 128-bit width, IPv6 changes the model: text representation is hexadecimal groups with "::" compression (so parsing/serialization code must change); address types are unicast/anycast/multicast with multicast subsuming broadcast (so group-addressing logic changes); every interface has a mandatory link-local address (so routing and neighbor discovery behave differently); and addressing is structured administratively, not by class. Porting by "swapping the type" breaks on every one of these.
- evidence: [S-0090]
- topic: systems-software/networking-basics

## Review (spaced repetition — interleaved with prerequisites)

### Q8
- Q: What exactly does "IP is connectionless" mean for a client that sends a datagram? What layer must fix the consequences, and how?
- bloom: understand
- bank: review
- A: IP treats each datagram independently: no connection, no end-to-end delivery guarantees — datagrams may arrive damaged, duplicated, out of order, or not at all. The transport layer (TCP, or the application over UDP) provides reliability when required: sequencing, retransmission, flow control.
- evidence: [S-0088]
- topic: systems-software/networking-basics

### Q9
- Q: In one sentence each: what does ARP resolve, and what does a port number identify?
- bloom: remember
- bank: review
- A: ARP resolves IP addresses to link-layer (Ethernet) addresses on Ethernet/IEEE 802 networks. A port number identifies an application process at a host endpoint, demultiplexing transport-layer data; ports 0–255 are reserved as well-known ports for standardized services.
- evidence: [S-0088]
- topic: systems-software/networking-basics

### Q10
- Q: Write the preferred text form of an IPv6 address with four groups of zeros in the middle, and explain what "::" does.
- bloom: apply
- bank: review
- A: Example: 2001:db8:abcd::1 compresses 2001:db8:abcd:0:0:0:0:1 — "::" stands for one or more consecutive groups of zeros and may appear only once per address. The preferred form is eight groups of one to four hexadecimal digits.
- evidence: [S-0090]
- topic: systems-software/networking-basics
