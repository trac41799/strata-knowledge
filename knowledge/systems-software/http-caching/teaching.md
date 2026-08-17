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

# HTTP Caching — teaching

## Learning objectives (Bloom)

By the end of this topic the learner can:

- **remember**: name the freshness inputs (`max-age`, `s-maxage`, `Expires`, `Age`) and the validation inputs (`ETag`/`If-None-Match`, `Last-Modified`/`If-Modified-Since`). [T2][S-0009]
- **understand**: explain why a response becomes stale, why `no-cache` still stores, and why `Vary` is part of the cache key. [T2][S-0009]
- **apply**: given real response headers, decide whether a stored response is fresh, and choose the correct `Cache-Control` directives for a given endpoint. [T2][S-0009]
- **analyze**: diagnose misconfigurations (private on a CDN endpoint, Vary mismatch, no-cache misinterpreted as no-store) and their user-visible effects. [T2][S-0009][S-0023]

## Worked example — end-to-end trace of a cached response

Setup: a news site serves `GET /headlines` through a CDN (shared cache) to a
browser (private cache). The origin responds:

```
HTTP/1.1 200 OK
Date: Tue, 18 Aug 2026 09:00:00 GMT
Cache-Control: public, max-age=300
ETag: "hl-8842"
Vary: Accept-Encoding
Content-Encoding: gzip
```

Step-by-step:

1. **09:00:00 — browser cache miss.** The browser sends a plain `GET /headlines` (no `If-None-Match`, nothing stored). The CDN also has nothing, so it forwards to the origin.
2. **09:00:00 — origin.** Returns the 200 above. The CDN stores it: `public` permits shared storage; freshness lifetime = 300 s from generation; cache key = URL + the value of `Accept-Encoding` (because of `Vary`). It forwards to the browser, adding `Age: 0`.
3. **09:02:00 — browser hit within freshness.** The browser's copy is fresh (age 120 s < 300 s): served locally, zero network traffic. This is the entire point of caching.
4. **09:03:00 — CDN forwards to a second user.** The CDN's copy is fresh (age 180 s < 300 s); it serves the stored body and sends `Age: 180` so downstream entities know 3 of the 300 seconds have already been consumed.
5. **09:06:00 — browser copy stale.** Age 360 s > 300 s. The browser must revalidate: it sends `GET /headlines` with `If-None-Match: "hl-8842"` and `Accept-Encoding: gzip`. The CDN's copy is also stale, so it forwards the conditional request to the origin.
6. **Origin revalidation.** The origin compares `"hl-8842"` (strong comparison) against the current entity-tag. Unchanged → `304 Not Modified` with updated `Cache-Control`/`Date`, no body. The CDN refreshes its stored metadata, forwards the 304, and the browser does the same. The stored body is served, now with a fresh lifetime.
7. **Had the tag differed**, the origin would return `200` with a new body + new ETag, and both caches would replace their stored copies.

Evidence: [S-0009][S-0023]

## Elaboration prompts

- Why does `stale-while-revalidate` exist when a cache could simply wait for revalidation to finish? What latency does it hide, and what consistency trade-off does it make? [T2][S-0024]
- Why is an ETag preferred over `If-Modified-Since` even though both can produce a 304? (Hint: think about one-second resolution and edits within the same second.) [T2][S-0023]
- If `no-store` forbids storage, why does `no-cache` exist at all — what does storing-with-revalidation buy you over never storing? [T2][S-0009]
- Why does `max-age` require trustworthy `Date` headers, and how does `Age` protect clients from lying or skewed intermediate clocks? [T2][S-0009]
- When is it correct for an origin to respond 504 rather than serve a stale response? [T2][S-0009]

## Common misconceptions

1. **"`no-cache` means don't cache."** Wrong: `no-cache` stores the response but forces revalidation before every reuse. Only `no-store` prevents storage entirely. [T2][S-0009]
2. **"`max-age` starts when the client receives the response."** Wrong: freshness is measured from response generation (via `Date`/`Age`); time spent in intermediate caches counts against it. [T2][S-0009]
3. **"`private` means the browser must not cache it."** Wrong: `private` means *shared* caches (CDNs, proxies) must not store it; the user's own browser cache is exactly the cache that may. [T2][S-0009]
4. **"A 304 is a normal response that contains the content."** Wrong: 304 has no body and is only a signal to refresh metadata of an already-stored response. [T2][S-0009][S-0023]
5. **"No cache headers = no caching."** Wrong: caches may apply heuristic freshness (e.g., 10% of time since Last-Modified), so responses can be reused even without directives. [T2][S-0009]

## Feynman targets

Explain, in plain language a non-engineer could follow:

- Why a page can load instantly on repeat visits yet still show fresh data five minutes later.
- Why two different users may receive *different* cached copies of "the same" URL (Vary + private/public).
- Why deleting a file from the origin does not immediately remove it from visitors' browsers.

## Interleaving hooks

- **http-basics (prerequisite)**: reuse method/status semantics (GET vs POST, 304 vs 200) and header mechanics; conditional requests are just headers like any other.
- **architecture-design/caching-strategies (related)**: connect HTTP's time-based freshness to invalidation strategies (TTL vs event-driven invalidation, cache-busting with versioned URLs).
- **systems-software/networking-basics**: tie round-trip latency to why even one revalidation round-trip is worth avoiding; `stale-while-revalidate` trades one RTT of freshness for one RTT of latency.
