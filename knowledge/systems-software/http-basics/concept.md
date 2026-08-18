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

# HTTP Basics

## Claims

### Protocol model

- HTTP is a family of stateless, application-level, request/response protocols with a generic interface, extensible semantics, and self-descriptive messages. [T2][S-0023]
- HTTP separates resource identification from request semantics: resources are identified by URIs, and what to do with them is carried by the method and a few request-modifying fields. [T2][S-0023]
- HTTP is stateless at the protocol level: each request can be considered in isolation, and applications layer their own state on top. [T2][S-0023]
- A client sends a request (method, target, fields, optional content); a server answers with a response (status code, fields, optional content); intermediaries (proxies, gateways, tunnels) may sit in the request/response chain. [T2][S-0023]
- HTTP does not transfer resources directly: it exchanges representations (representation metadata plus a stream of representation data) that reflect resource state. [T2][S-0023]

### Identifiers: URI vs URL

- HTTP relies on the URI standard (RFC 3986) for request targets and references; "URL" denotes the subset of URIs that, in addition to identifying a resource, locate it — so a URL is a kind of URI, and the terms are not synonyms. [T2][S-0023]
- The request target is a URI that the server resolves to the resource it serves, e.g. `http://www.example.org/where?q=now`. [T2][S-0023]

### Methods

- HTTP defines eight core methods — GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE — and the registry is extensible (e.g., PATCH). [T2][S-0023]
- GET requests transfer a current representation of the target resource; HEAD is identical to GET except that the response contains no content. [T2][S-0023]
- POST asks the target resource to process the representation enclosed in the request; PUT asks it to replace all current representations of the target resource. [T2][S-0023]
- Safe methods (GET, HEAD, OPTIONS, TRACE) have essentially read-only semantics: the client neither requests nor expects a state change on the origin server. [T2][S-0023]
- Idempotent methods — PUT, DELETE, and all safe methods — have the same intended effect whether executed once or many times; POST is not idempotent. [T2][S-0023]

### Status codes

- The first digit of a status code defines its class: 1xx informational, 2xx successful, 3xx redirection, 4xx client error, 5xx server error. [T2][S-0023]
- A client MUST understand the class of every status code and treat an unrecognized code as its x00 equivalent (e.g., an unknown 4xx as 400). [T2][S-0023]
- Frequently used codes include 200 OK, 201 Created, 301/308 redirects, 304 Not Modified, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error, and 503 Service Unavailable. [T2][S-0023]

### Headers and representations

- A representation consists of representation metadata plus data; key metadata fields are Content-Type, Content-Encoding, Content-Language, and Content-Length. [T2][S-0023]
- Content-Type identifies the media type of the representation data (e.g., `text/html; charset=utf-8`). [T2][S-0023]
- Content-Encoding names the content coding applied to the data (e.g., gzip) so it can be transferred compressed and decoded on receipt. [T2][S-0023]
- Content negotiation lets client and server agree on a representation: proactive (server selects using Accept, Accept-Encoding, Accept-Language), reactive (server lists alternatives), or request-content negotiation. [T2][S-0023]
- Vary lists the request fields that influenced the selected representation, making them part of the cache key for caches. [T2][S-0023][S-0009]

### Connection handling

- HTTP/1.1 defaults to persistent connections: a single connection carries multiple request/response exchanges; the "close" connection option opts out. [T2][S-0093]
- HTTP/1.0 used one connection per exchange with a nonstandard Keep-Alive mechanism; under HTTP/1.1 persistence is the default, and proxies must not maintain persistent connections with HTTP/1.0 clients. [T2][S-0093]
- HTTP/1.1 pipelining lets a client send several requests before reading responses, but the server MUST send responses in request order; after connection failures pipelining is unsafe, and in practice HTTP/1.1 concurrency is limited to parallel connections, which suffer head-of-line blocking. [T2][S-0093]
- HTTP/2 multiplexes many concurrent exchanges over one connection using streams, binary message framing, and field (header) compression; TCP head-of-line blocking remains. [T2][S-0094]
- HTTP/3 maps HTTP semantics onto QUIC — a UDP-based transport providing stream multiplexing, per-stream flow control, TLS 1.3, and low-latency connection establishment — removing TCP head-of-line blocking. [T2][S-0095]

### Caching pointer

- HTTP's caching machinery (freshness, validators, Cache-Control directives) is defined by RFC 9111 and treated in depth in the sibling topic `systems-software/http-caching`. [T2][S-0009]
- Conditional requests (If-None-Match, If-Modified-Since) and the 304 Not Modified response implement validation against the origin — the foundation of revalidation. [T2][S-0023][S-0009]

### Shared semantics across versions

- HTTP/2 and HTTP/3 express the same semantics (methods, status codes, fields) as HTTP/1.1 with different framing and transport; RFC 9110 is the shared semantics layer for all versions. [T2][S-0023][S-0094][S-0095]

## Details

Minimal HTTP/1.1 request (RFC 9112 §3.2.1): the request line carries
method, request-target, and version; Host is mandatory in HTTP/1.1.

```
GET /where?q=now HTTP/1.1
Host: www.example.org
```

The response echoes the version and status:

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 44

<html>...</html>
```

HTTP rides on the transport/network stack of `systems-software/networking-basics`:
TCP (HTTP/1.1, HTTP/2) or QUIC over UDP (HTTP/3). On a persistent
HTTP/1.1 connection each message must carry a self-defined length
(Content-Length or chunked framing) so the receiver knows where one
message ends and the next begins.

## Boundaries / common misunderstandings

- "URL and URI are interchangeable" — a URL is a URI that locates a resource; URI is the broader class, so "URI" is the correct generic term. [T2][S-0023]
- "Stateless means the server stores nothing" — statelessness is a protocol property (each request is processed in isolation); servers routinely store application state (sessions, databases) on top. [T2][S-0023]
- "GET is guaranteed side-effect free" — safe describes what the client requests and expects, not a server promise to perform no writes (access logs, for example, are written on every request). [T2][S-0023]
- "POST is idempotent because the same request can be repeated" — idempotence is a property of the intended server effect; POST is defined without that guarantee, so retries may double-apply. [T2][S-0023]
- "HTTP always runs over TCP" — HTTP/1.1 and HTTP/2 commonly run over TCP (often with TLS); HTTP/3 runs over QUIC, which is UDP-based. [T2][S-0095][S-0094]
- "A 404 means the server is down" — 4xx is the client-error class: 404 means no representation exists for that target under that request; 5xx signals server-side failure. [T2][S-0023]
- "A 304 response contains the resource" — 304 Not Modified carries no content; it confirms that a stored copy is still valid (see `systems-software/http-caching`). [T2][S-0023][S-0009]
- "HTTP/2 is a new protocol that replaces HTTP" — HTTP/2 re-implements HTTP semantics over a new framing layer; methods, status codes, and fields are shared with HTTP/1.1 and HTTP/3. [T2][S-0023][S-0094]

## References (evidence records)

- S-0023 — RFC 9110: HTTP Semantics (IETF, 2022) — protocol model, URIs, methods, status codes, headers, negotiation.
- S-0009 — RFC 9111: HTTP Caching (IETF, 2022) — caching pointer and revalidation machinery.
- S-0093 — RFC 9112: HTTP/1.1 (IETF, 2022) — message syntax, persistence, pipelining, Host.
- S-0094 — RFC 9113: HTTP/2 (IETF, 2022) — multiplexing, streams, binary framing, header compression.
- S-0095 — RFC 9114: HTTP/3 (IETF, 2022) — HTTP over QUIC/UDP.
