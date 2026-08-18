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

# HTTP Basics — validation

## Formative (practice)

### Q1
- Q: List the eight core HTTP methods defined by RFC 9110, then name the three that are safe.
- bloom: remember
- bank: formative
- A: GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE. Safe methods: GET, HEAD, OPTIONS, TRACE (their semantics are essentially read-only).
- evidence: [S-0023]
- topic: systems-software/http-basics

### Q2
- Q: Your API returns a cached resource after revalidation: the server answers 304. The developer on call says "the 304 must contain the updated body, otherwise we have nothing to show." Correct or incorrect, and why?
- bloom: understand
- bank: formative
- A: Incorrect. 304 Not Modified carries no content: it only tells the client that its stored copy is still valid, so the client serves the stored body and refreshes its metadata. A 304 is meaningless without a stored representation.
- evidence: [S-0023][S-0009]
- topic: systems-software/http-basics

### Q3
- Q: A client repeats the same POST twice because the first response was lost. Is this safe, and why does the method choice matter?
- bloom: apply
- bank: formative
- A: Repeating POST is not automatically safe: POST is neither safe nor idempotent, so the second execution may apply the request's effect again (e.g., duplicate order). PUT and DELETE are idempotent — repeating them has the same intended effect as one execution — which is exactly why retries over unreliable networks are only straightforward for idempotent methods.
- evidence: [S-0023]
- topic: systems-software/http-basics

### Q4
- Q: A server must tell a client "your request was fine but the resource moved permanently." Which status code class and code do you use, and what would a 4xx mean instead?
- bloom: apply
- bank: formative
- A: 3xx (Redirection), specifically 301 Moved Permanently. A 4xx (Client Error) would mean the request itself was wrong (bad syntax, missing authorization, not found) — the client would need to fix the request, not follow a redirect.
- evidence: [S-0023]
- topic: systems-software/http-basics

## Summative (mastery checkpoint)

### Q5
- Q: Write the full HTTP/1.1 request/response exchange a browser sends for `http://www.example.org/where?q=now`, then identify the minimum framing fields that let a persistent connection reuse work, and name the version of HTTP that made persistence the default.
- bloom: apply
- bank: summative
- A: Request: `GET /where?q=now HTTP/1.1` with a mandatory `Host: www.example.org` header (and other fields such as Accept/User-Agent). Response: `HTTP/1.1 200 OK` with representation metadata (Content-Type) and a self-defined length (Content-Length, or chunked framing). Self-defined length is what makes reuse safe: without it, the receiver cannot tell where one message ends, so persistent reuse would corrupt the stream. HTTP/1.1 made persistent connections the default (RFC 9112 §9.3).
- evidence: [S-0023][S-0093]
- topic: systems-software/http-basics

### Q6
- Q: An engineer proposes switching a checkout endpoint from POST to PUT "so retries are safe." Evaluate: which property would improve, which would not, and what is the correct design move?
- bloom: analyze
- bank: summative
- A: Switching to PUT buys idempotence of intent — retrying the same PUT has the same intended server effect — which is genuinely useful for network retries. It does not buy safety: PUT is not safe, so it still causes state changes, and it replaces the whole representation semantics, which a checkout payload usually does not have (no resource to replace). The correct design move is usually to keep POST (or PUT with an explicit idempotency key header, a registered extension pattern) and add an idempotency key rather than misuse method semantics.
- evidence: [S-0023]
- topic: systems-software/http-basics

### Q7
- Q: A CDN serves gzip content to clients that never sent `Accept-Encoding: gzip`, and browsers render garbage. The origin sets Vary correctly. Where in the protocol chain did the failure occur, and which two concepts (one from HTTP, one from caching) does it violate?
- bloom: analyze
- bank: summative
- A: The failure is at the cache/CDN: content negotiation selected a representation based on the request's Accept-Encoding, and Vary declares that the cache key includes that field. Serving a stored gzip variant to a request without the matching header violates the rule that a stored response may only be reused when the current request's values for every Vary-listed field match — a content-negotiation violation with a cache-keying violation.
- evidence: [S-0023][S-0009]
- topic: systems-software/http-basics

## Review (spaced repetition — interleaved with prerequisites)

### Q8
- Q: HTTP is called a "stateless request/response protocol." What does stateless mean precisely, and what does it NOT mean about server-side storage?
- bloom: understand
- bank: review
- A: Stateless means each request can be considered in isolation — the protocol keeps no coupling between requests and no session state in the message layer. It does NOT mean the server stores nothing: applications add their own state (sessions, databases, caches) on top of the protocol.
- evidence: [S-0023]
- topic: systems-software/http-basics

### Q9
- Q: Why did HTTP/1.1 need self-defined message lengths (Content-Length or chunked framing) once persistent connections became the default, and what framing problem does this solve?
- bloom: understand
- bank: review
- A: On a persistent connection many messages share one TCP stream. Without a self-defined length the receiver could not tell where one message ends, so it would misinterpret the tail of one message as the start of the next. Self-defined length makes message boundaries explicit and reuse safe.
- evidence: [S-0093]
- topic: systems-software/http-basics

### Q10
- Q: When your browser looks up the address of api.example.com, which distributed, hierarchical system answers, and what limits how long its answer may be reused? (Prerequisite interleave: networking-basics.)
- bloom: remember
- bank: review
- A: DNS (the Domain Name System). The answer is a resource record that carries a TTL, which bounds how long any resolver or server may cache it before discard — reuse beyond the TTL can serve stale data.
- evidence: [S-0089]
- topic: systems-software/networking-basics

### Q11
- Q: A request leaves a browser for an HTTPS server. Name the transport-layer protocol and the two things it adds on top of IP that the HTTP message depends on. (Prerequisite interleave: networking-basics.)
- bloom: understand
- bank: review
- A: TCP (for HTTP/1.1/2; QUIC over UDP for HTTP/3). TCP provides a reliable, connection-oriented byte stream — end-to-end reliability, resequencing, and flow control — and demultiplexes by port number so the HTTP message reaches the right process. IP alone guarantees none of this.
- evidence: [S-0088]
- topic: systems-software/networking-basics
