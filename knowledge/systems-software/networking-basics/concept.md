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

# Networking Basics

## Claims

### Layered models (TCP/IP vs OSI)

- The Internet is built from a layered set of protocols, and a host must implement at least one protocol from each layer to communicate. [T2][S-0088]
- The Internet architecture has four protocol layers — application, transport, internet, and link (RFC 1122 §1.1.3). [T2][S-0088]
- The Internet suite's application layer combines the functions of the top two OSI layers (presentation and application); the OSI reference model is a separate framework, not an alias for TCP/IP. [T2][S-0088]
- TCP is a reliable, connection-oriented transport service providing end-to-end reliability, resequencing, and flow control; UDP is a connectionless ("datagram") transport service. [T2][S-0088]
- IP is a connectionless datagram internetwork service with no end-to-end delivery guarantees: datagrams may arrive damaged, duplicated, out of order, or not at all — layers above IP provide reliability when required. [T2][S-0088]
- "TCP/IP" names the whole Internet protocol suite (TCP, UDP, IP, ICMP, ARP, DNS, ...), not a single protocol. [T2][S-0088]

### Encapsulation

- End-to-end communication works by encapsulation: a message is wrapped in a datagram, which is wrapped in a frame, each layer adding its own header as data descends the stack. [T2][S-0088]
- A packet is the unit passed between the internet layer and the link layer; a frame is the link layer's unit of transmission; a frame may carry a complete datagram or a fragment of one. [T2][S-0088]
- On Ethernet, IP datagrams are encapsulated directly in Ethernet frames (RFC 894); the Ethernet MTU is 1500 octets (1492 for IEEE 802.3). [T2][S-0088]

### IP addressing (IPv4 / IPv6 basics)

- IPv4 addresses are 32-bit numbers; the IP layer treats them as featureless identifiers whose structure (network/host bits) is assigned administratively, not implied by the value. [T2][S-0088]
- IPv6 addresses are 128-bit identifiers for interfaces and for sets of interfaces. [T2][S-0090]
- The preferred text form of an IPv6 address is x:x:x:x:x:x:x:x with one to four hexadecimal digits per group, and "::" compressing one or more groups of zeros. [T2][S-0090]
- IPv6 address types are unicast (one interface), anycast (a set of interfaces, delivered to one), and multicast (a set, delivered to all); multicast subsumes IPv4 broadcast. [T2][S-0090]
- Every IPv6 interface is required to have at least one link-local unicast address. [T2][S-0090]

### Link layer / Ethernet basics

- The link layer (media-access layer) is the protocol of the directly-connected network; a host must implement it to communicate with its neighbors. [T2][S-0088]
- On Ethernet and IEEE 802 networks, hosts use ARP to resolve IP addresses to link-layer (Ethernet) addresses. [T2][S-0088]

### DNS

- DNS provides a distributed, hierarchical name space: a single tree rooted at the root domain ("."), where names are composed of labels ordered from least to most specific. [T2][S-0089]
- Name servers are authoritative for the parts of the tree they own (zones); for everything else they answer from cache or by querying other servers. [T2][S-0089]
- Every resource record carries a TTL that states how long it may be cached before it must be discarded — which is why DNS changes propagate slowly. [T2][S-0089]
- Resolvers may request recursive service (RD/RA), so that a server performs the full lookup chain on the client's behalf. [T2][S-0089]

### Ports and sockets

- Transport protocols demultiplex data to the correct application process using port numbers; TCP reserves ports 0–255 as "well-known" ports for standardized services (RFC 1122 §4.2.2.1, following RFC 793 §2.7). [T2][S-0088]
- UDP port conventions follow TCP's, including the well-known port rules. [T2][S-0088]
- A TCP connection is defined by the (remote socket, local socket) endpoint pair; each socket is a host-and-port endpoint of the connection. [T2][S-0088]

### Curriculum standing

- Networking and Communication is a core knowledge area of CS2023 (Systems Fundamentals), which Strata's systems-software track implements. [T2][S-0018]

## Details

Packet walk-through for a single HTTP GET (see also `systems-software/http-basics`):

1. The browser asks DNS to resolve a host name (UDP/TCP to a resolver, port 53 convention) and receives an IP address, possibly from a cache with a bounded TTL.
2. The application hands its message to TCP, which segments it and addresses it with source/destination port numbers.
3. TCP hands segments to IP, which wraps each in a datagram addressed with 32-bit (IPv4) or 128-bit (IPv6) source/destination addresses.
4. IP hands the datagram to the link layer, which wraps it in a frame addressed with link-layer (Ethernet) addresses and sends it on the wire.
5. Each receiver strips its layer's header and hands the payload up — demultiplexing by port, protocol, and frame type.

- Traditional NAT (RFC 3022) rewrites addresses/ports at a gateway so many hosts can share one public address; it is a common extension that breaks IP's end-to-end transparency [T2][S-0111].

## Boundaries / common misunderstandings

- "TCP/IP is one protocol" — it is a suite: different protocols live at each layer (IP, ICMP, ARP; TCP/UDP; DNS, SMTP, HTTP), and "TCP/IP" is shorthand for the whole layered stack. [T2][S-0088]
- "The OSI 7-layer model describes TCP/IP" — OSI and the Internet suite are different models; the Internet suite has no separate session/presentation layers and the layers do not map 1:1. [T2][S-0088]
- "IP guarantees delivery" — IP is best-effort: no delivery guarantees; reliability is TCP's or the application's job. [T2][S-0088]
- "DNS is one big central directory" — the name space is distributed across zones owned by many servers; no single server holds all names. [T2][S-0089]
- "Cached DNS data lives until it changes" — cache lifetime is bounded by TTLs, not by change detection. [T2][S-0089]
- "Ports identify hosts" — ports identify processes on a host; host identity lives at the IP layer (and link-layer addresses at layer 2). [T2][S-0088]
- "Well-known ports are a security mechanism" — they are a registration convention; applications may use any port, so allowlists must not assume otherwise. [T2][S-0088]
- "IPv6 is just IPv4 with longer numbers" — IPv6 also changes the address model (unicast/anycast/multicast, link-local, text form) and interface semantics. [T2][S-0090]

## References (evidence records)

- S-0088 — RFC 1122 (IETF, 1989) — Internet architecture, layering, encapsulation, IPv4, TCP/UDP, ports, Ethernet/ARP.
- S-0089 — RFC 1034 (IETF, 1987) — DNS concepts, hierarchy, zones, TTL caching, recursion.
- S-0090 — RFC 4291 (IETF, 2006) — IPv6 addressing architecture, text form, address types.
- S-0018 — CS2023 (ACM/IEEE-CS/AAAI, 2024) — curriculum standing of the Networking and Communication KA.
