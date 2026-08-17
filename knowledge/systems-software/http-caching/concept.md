---
id: systems-software/http-caching
title: HTTP Caching
band: B4
track: systems-software
tier: T2
bloom_target: apply
prerequisites: [systems-software/http-basics]
related: [architecture-design/caching-strategies]
recommended: []
status: draft
schema-version: 1
owner: l1-http-caching
reviewed-by: []
updated: 2026-08-18
sources: [S-0009, S-0023, S-0024]
---

# HTTP Caching

## Claims

### Freshness model

- A stored response may satisfy a request only while it is fresh: its age must not exceed its freshness lifetime; once stale it must be revalidated or dropped before reuse. [T2][S-0009]
- Freshness lifetime is chosen in order: `s-maxage` (shared caches only), then `max-age`, then `Expires` minus `Date`; the first directive present wins. [T2][S-0009]
- `max-age=N` declares the response stale once its age exceeds N seconds counted from the time the response was generated. [T2][S-0009]
- `Expires` carries an absolute expiration HTTP-date; if `Cache-Control: max-age` or `s-maxage` is also present, recipients MUST ignore `Expires`. [T2][S-0009]
- The `Age` response header reports how many seconds the response has spent being forwarded through caches; each cache adds its resident time, letting clients estimate age without trusting wall clocks alone. [T2][S-0009]
- Age is derived from the `Date` header and observed response time (current_age = corrected age + resident time); a cache MUST NOT present a response as fresh once its computed age exceeds the freshness lifetime. [T2][S-0009]
- Heuristic freshness: when no explicit expiration exists, a cache MAY apply a heuristic — RFC 9111's example is 10% of the time since `Last-Modified` — but heuristics MUST NOT be used when explicit freshness information is present. [T2][S-0009]

### Validation (revalidation)

- Revalidation asks the origin whether a stored response is still valid using a conditional request; a `304 Not Modified` confirms validity and carries no message body. [T2][S-0009][S-0023]
- ETag-based validation sends the stored entity-tag in `If-None-Match`; the origin compares tags using the strong comparison function and returns 304 when a tag matches. [T2][S-0023]
- When a stored response carries an ETag, caches prefer `If-None-Match` over date-based checks because entity-tags are stronger validators. [T2][S-0009][S-0023]
- `If-Modified-Since` carries a date and is used when the stored response has a `Last-Modified` value; date-based validation has one-second resolution and can miss changes made within the same second. [T2][S-0023]
- Weak entity-tags (prefixed `W/`) match when representations are semantically equivalent; strong comparison requires byte-for-byte equality, so caches must send the right comparison form. [T2][S-0023]
- After a successful revalidation the cache updates the stored response's metadata from the 304 (freshness, validators) and serves the stored body; a 304 without a matching stored response cannot be used to reconstruct one. [T2][S-0009]

### Cache-Control directives

- `no-store` forbids the cache from storing any part of the response or using it to satisfy any request — it is the only directive that truly prevents caching. [T2][S-0009]
- `no-cache` permits storing the response but requires successful validation with the origin before every use; it does NOT forbid storing. [T2][S-0009]
- `private` restricts storage to the user-agent's private cache; shared caches MUST NOT store it. `public` permits shared caches to store a response that would otherwise be non-cacheable. [T2][S-0009]
- `must-revalidate` forbids serving a stale response without revalidation; if the origin is unreachable, the cache MUST respond `504 Gateway Timeout` rather than serve stale. [T2][S-0009]
- `s-maxage` overrides `max-age` for shared caches only; private caches ignore it. [T2][S-0009]
- `stale-while-revalidate=N` lets a cache serve a stale response for up to N seconds while revalidating asynchronously; a successful revalidation replaces the stored copy. [T2][S-0009][S-0024]
- `stale-if-error=N` lets a cache serve a stale response when the origin fails (5xx or network error) within the window. [T2][S-0009][S-0024]
- Unknown cache directives MUST be ignored rather than cause failure, which is how extensions like stale-while-revalidate deploy safely. [T2][S-0009]

### Shared vs private caches

- A shared cache serves more than one user (proxy, CDN); a private cache serves a single user (browser cache); directive semantics differ between them. [T2][S-0009]
- A cache MUST NOT store a response to a request carrying `Authorization` unless the response includes `public`, `must-revalidate`, or `s-maxage`. [T2][S-0009]
- GET and HEAD responses are cacheable by default; other methods (e.g., POST) may be cached only with explicit freshness information and a matching `Content-Location`. [T2][S-0009]

### Vary

- `Vary` names request header fields whose values participate in the cache key; a stored response may be reused only when the current request's values for those fields match. [T2][S-0009]
- `Vary: *` means the response varies on all request header fields, which in practice prevents cache reuse for most clients. [T2][S-0023]

### Heuristics in practice

- Absence of cache directives does not mean "no caching": user agents and shared caches may still store and heuristically reuse responses. [T2][S-0009]

## Details

Freshness decision at a cache: compute current age (Date/Age based), compare
against freshness lifetime (s-maxage > max-age > Expires-Date > heuristic).
If fresh, serve stored; if stale, revalidate (If-None-Match preferred, else
If-Modified-Since) or apply stale-while-revalidate / stale-if-error / serving
stale on disconnect (§4.2.4 of RFC 9111).

## Boundaries / common misunderstandings

- `no-cache` does NOT mean no caching: the response is stored but must be revalidated before each reuse. Only `no-store` prevents storage. [T2][S-0009]
- `max-age` counts from response generation (Date/Age), not from the moment the client received it; a response cached for 30 minutes with `max-age=3600` has only 30 minutes of freshness left. [T2][S-0009]
- `max-age=0` does not disable caching — it forces revalidation on every use, like `no-cache` plus an ETag. [T2][S-0009]
- `private` does not mean "don't cache"; it means the browser may cache but shared caches (CDNs) must not. [T2][S-0009]
- `Expires` depends on the origin's clock and is superseded by `max-age`; mixing both with a skewed clock yields surprising lifetimes. [T2][S-0009]
- A `304` is not a standalone response: it only refreshes a stored entry, so caches cannot fabricate a response from it. [T2][S-0009]
- `stale-while-revalidate` does not mean "serve stale forever": it is bounded by N seconds and the revalidation result replaces the entry. [T2][S-0009][S-0024]
- Not every 200 response is cacheable: the method and status must be cacheable, `no-store` absent, and Authorization responses exempted for shared caches. [T2][S-0009]
- Ignoring `Vary` (e.g., serving a gzip variant to a client that did not send `Accept-Encoding: gzip`) corrupts content negotiation and is a common real-world cache bug. [T2][S-0023]

## References (evidence records)

- S-0009 — RFC 9111: HTTP Caching (IETF, 2022) — freshness, validation, cache-control, cache keying.
- S-0023 — RFC 9110: HTTP Semantics (IETF, 2022) — conditional requests, validators, Vary, 304.
- S-0024 — RFC 5861: HTTP Cache-Control Extensions for Stale Content (Nottingham, 2010).
