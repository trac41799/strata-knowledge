---
id: systems-software/http-basics
title: HTTP Basics
band: B4
track: systems-software
tier: T2
bloom_target: apply
prerequisites: [systems-software/networking-basics]
related: []
recommended: []
status: published
schema-version: 1
owner: l1-http-basics
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0023, S-0009, S-0093, S-0094, S-0095]
---

# HTTP Basics — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: name the eight core methods, the five status-code classes, and the key representation fields (Content-Type, Content-Encoding, Content-Length). [T2][S-0023]
- **understand**: explain what "stateless" means in HTTP, why a URL is a kind of URI, and how persistent connections changed message framing. [T2][S-0023][S-0093]
- **apply**: given an API operation, choose the correct method/status pairing and write a correct HTTP/1.1 exchange. [T2][S-0023]
- **analyze**: diagnose negotiation, retry, and caching failures from headers and status codes. [T2][S-0023][S-0009]

## Worked example — a full HTTP/1.1 request/response trace

Setup: `curl -v http://www.example.org/where?q=now` over HTTP/1.1.

1. **Resolution and connection.** DNS resolves `www.example.org`; curl opens a TCP connection to (203.0.113.7, 80) — port 80 is the well-known HTTP port (networking-basics interleave). [S-0088]
2. **Request.** On the wire: `GET /where?q=now HTTP/1.1` (method, request-target, version) followed by fields; Host is mandatory in HTTP/1.1 — the server may host many sites on one IP, so the target's authority must be explicit. Optional `Accept: text/html`, `Accept-Encoding: gzip` declare negotiation preferences. [S-0093][S-0023]
3. **Response.** The server answers `HTTP/1.1 200 OK` with representation metadata (`Content-Type: text/html; charset=utf-8`, `Content-Length: 44`) and the body. The status line's first digit 2 = Successful; 200 = OK. Content-Length gives the message a self-defined length. [S-0023][S-0093]
4. **Connection reuse.** Because HTTP/1.1 defaults to persistent connections, the same TCP connection may carry the next request; the receiver knows exactly where this message ended from Content-Length. Without a self-defined length, reuse would corrupt the stream. [S-0093]
5. **What if the copy were stale?** The client would send `If-None-Match: "v7"`; an unchanged origin answers `304 Not Modified` (3xx, no body) and the client serves its stored copy — the caching machine of `systems-software/http-caching`. [S-0023][S-0009]
6. **Same semantics, faster plumbing.** The same method/status/header semantics run over HTTP/2 (streams, one multiplexed connection) and HTTP/3 (QUIC over UDP, no TCP head-of-line blocking). [S-0094][S-0095]

Evidence: [S-0023][S-0009][S-0093][S-0094][S-0095]

## Elaboration prompts

- Why does HTTP need the Host header when the TCP connection already identifies the server's address? (Hint: virtual hosting — one IP, many sites.) [T2][S-0093]
- Why is "stateless" a feature for intermediaries (proxies, CDNs, load balancers) rather than just a limitation? [T2][S-0023]
- GET is safe, PUT is idempotent, POST is neither — how does each property map to what a client may safely do after a lost response? [T2][S-0023]
- Why would a server choose 204 No Content instead of 200 with an empty body, and what class does it share with 101 Switching Protocols? [T2][S-0023]
- Content negotiation happens before caching in a sense: why must the cache key include the negotiated fields (Vary)? [T2][S-0023][S-0009]

## Common misconceptions

1. **"URL and URI are the same thing."** A URL is the subset of URIs that locate a resource; URI is the generic class the protocol actually uses. "The URI of the resource" is precise; "URL" is the everyday term. [T2][S-0023]
2. **"Stateless means the server stores nothing."** Statelessness is a protocol property — each request is processed in isolation — not a ban on server-side state (sessions, databases). [T2][S-0023]
3. **"HTTP always runs over TCP."** HTTP/1.1 and HTTP/2 typically run over TCP (+TLS); HTTP/3 runs over QUIC, a UDP-based transport. The semantics are transport-independent. [T2][S-0095][S-0094]
4. **"POST can be retried safely because it is the same request."** POST is not idempotent: identical requests may have different effects (double charge, duplicate order). Only PUT/DELETE/safe methods carry the idempotence guarantee. [T2][S-0023]
5. **"A 404 means the server is down or the site is gone."** 404 is a client-error response: no representation for that target. Server failures are 5xx. Reading the class digit first prevents exactly this confusion. [T2][S-0023]
6. **"HTTP/2 and HTTP/3 are new languages you must relearn."** They re-express the same semantics (methods, status codes, fields) over new framing/transport — RFC 9110 is the shared core. [T2][S-0023][S-0094][S-0095]

## Feynman targets

Explain, in plain language a non-engineer could follow:

- Why the address in your browser bar is not quite the same thing as "where to find the page" (URI vs URL).
- How the server knows where one request ends and the next begins when many requests share one connection.
- Why refreshing a page can either be instant (304: "nothing changed, use what you have") or slow (200: "here is the new content").
- Why pressing "send again" on an order form is dangerous, but re-downloading a file is not.

## Interleaving hooks

- **systems-software/networking-basics (prerequisite)**: HTTP is the application-layer example of the stack — sockets, ports, TCP/UDP, DNS all do concrete work in every HTTP exchange.
- **systems-software/http-caching (next topic)**: methods/statuses/headers learned here are the vocabulary of caching (304, ETag, Vary, cacheable methods).
- **architecture-design/rest-apis (related, later)**: REST-style design leans on method semantics (safe/idempotent), status codes, and representations — this topic supplies the protocol facts those designs must respect.
