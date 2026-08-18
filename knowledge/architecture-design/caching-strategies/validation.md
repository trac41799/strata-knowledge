---
id: architecture-design/caching-strategies
title: Caching Strategies
band: B4
track: architecture-design
tier: T1
bloom_target: apply
prerequisites: [systems-software/http-caching]
related: [systems-software/http-caching]
recommended: []
status: published
schema-version: 1
owner: l1-caching-strategies
reviewed-by: [l2-deepseek-v4-pro]
updated: 2026-08-18
sources: [S-0009, S-0157, S-0158, S-0159]
---

# Caching Strategies — validation

## Formative (practice)

### F1 — remember: the pattern zoo
- Q: Name the four main caching patterns and give a one-line definition of each.
- bloom: remember
- bank: formative
- A: Cache-aside — application loads on miss, then populates the cache. Read-through — the cache loads missing values itself. Write-through — store and cache updated in the same write. Write-behind/write-back — writes acknowledged at the cache and flushed asynchronously.
- evidence: [S-0157]
- topic: architecture-design/caching-strategies

### F2 — remember: Redis eviction
- Q: Which maxmemory-policy groups exist in Redis, and what is the default policy's behavior when memory is full?
- bloom: remember
- bank: formative
- A: allkeys-* (lru/lfu/random — any key eligible) and volatile-* (lru/lfu/ttl — only keys with a TTL). Default is noeviction: write commands return errors when maxmemory is reached.
- evidence: [S-0159]
- topic: architecture-design/caching-strategies

### F3 — understand: cache-aside vs read-through
- Q: Who loads the data on a miss in cache-aside versus read-through, and what practical difference does that make?
- bloom: understand
- bank: formative
- A: In cache-aside the application performs the load and population; in read-through the cache layer does it, so the application only ever calls the cache. The difference is where the loading logic lives — application code versus cache layer.
- evidence: [S-0157]
- topic: architecture-design/caching-strategies

### F4 — understand: TTL vs invalidation
- Q: Why does TTL alone not guarantee freshness, and what does delete-on-write invalidation change?
- bloom: understand
- bank: formative
- A: TTL only caps how long an entry survives; the entry is still served until expiry even if the source changed. Delete-on-write removes the entry when the source changes, so the next read rebuilds fresh data — at the cost of requiring the write path to know about the cache.
- evidence: [S-0158]
- topic: architecture-design/caching-strategies

### F5 — apply: choose a strategy
- Q: A product catalog does 5,000 reads/s and 5 writes/s (admin updates); slight staleness is tolerable; reads must not fail when the cache is down. Which pattern set do you choose and how do you configure it?
- bloom: apply
- bank: formative
- A: Cache-aside with TTL: application reads via cache, on miss loads from the store and populates; on write, update the store and delete the cache entry (invalidate-on-write) so the next read repopulates; a modest TTL (e.g., minutes) bounds staleness if invalidation is ever missed; if the cache is unavailable, fall back to the store. No write-through needed (write rate is tiny), no write-back (writes must not be lost).
- evidence: [S-0157, S-0159]
- topic: architecture-design/caching-strategies

## Summative (mastery checkpoint)

### S1 — apply: sequence trace
- Q: Cache-aside for reads, write-through for writes. Trace R(k)=old, then W(k)=new, then R(k): what is in the cache and store after each operation?
- bloom: apply
- bank: summative
- A: R(k): miss (assuming empty) → load old from store, populate cache, return old. W(k): write-through writes new to both store and cache in the same write operation. R(k): cache hit on new — the reader sees the new value immediately after the successful write.
- evidence: [S-0157]
- topic: architecture-design/caching-strategies

### S2 — apply: stampede timeline
- Q: Hot key K expires at t=0 and 10,000 readers arrive within 100 ms; the store can sustain ~200 qps. What happens without protection, and how does the lease mechanism change the timeline?
- bloom: apply
- bank: summative
- A: Without protection, all 10,000 fall through to the store simultaneously (thundering herd) — the store is overwhelmed. With leases: the cache issues one lease token for K (regulated to ~once per 10 s); the token holder rebuilds K; the other 9,999 readers are told to wait briefly and then served the rebuilt value, so the store sees ~1 rebuild query instead of 10,000. Facebook measured the analogous drop as 17,000/s → 1,300/s for a contended key.
- evidence: [S-0158]
- topic: architecture-design/caching-strategies

### S3 — analyze: consistency spectrum
- Q: Place cache-aside+TTL, write-through, and write-behind on a stale-to-coherent axis, and state the loss/durability risk of each.
- bloom: analyze
- bank: summative
- A: Cache-aside+TTL: bounded staleness (entry served up to TTL after source change); no data loss (store is authoritative). Write-through: coherent at write time (read-your-writes); no loss, but write latency and possibly caching unread data. Write-behind: delayed coherence with a data-loss window if the cache fails before flush — only safe for reconstructable data. The trade is: the further toward coherent, the more the write path pays.
- evidence: [S-0157, S-0158]
- topic: architecture-design/caching-strategies

### S4 — analyze: hit-ratio economics
- Q: Hit ratio drops from 99% to 98%. By what factor does origin load increase, and why is the store — not the cache — the constraint?
- bloom: analyze
- bank: summative
- A: Misses rise from 1% to 2% of reads — origin load doubles. The store is the constraint because it is the expensive, capacity-limited tier: cache RAM buys store headroom, so origin load (miss rate x read rate) is the metric that matters, not the ratio itself.
- evidence: [S-0157]
- topic: architecture-design/caching-strategies

## Review (spaced repetition — interleaved with prerequisites)

### R1 — understand (http-caching): freshness lifetime
- Q: What does max-age mean for a browser cache, and what happens once a stored response's computed age exceeds the freshness lifetime?
- bloom: understand
- bank: review
- A: max-age=N declares the response stale once its age exceeds N seconds from generation; a stale stored response must be revalidated (or dropped) before reuse — it cannot be served as fresh.
- evidence: [S-0009]
- topic: systems-software/http-caching

### R2 — understand (http-caching): no-cache vs no-store
- Q: Which of no-cache and no-store still allows storing the response, and what is required on each reuse in that case?
- bloom: understand
- bank: review
- A: no-cache permits storage but requires successful validation with the origin before every use; no-store forbids storage entirely. Only no-store truly prevents caching.
- evidence: [S-0009]
- topic: systems-software/http-caching

### R3 — remember (http-caching): validators
- Q: Which header-based mechanisms let an HTTP cache revalidate a stale entry without downloading the body?
- bloom: remember
- bank: review
- A: ETag with If-None-Match (strongest validator; 304 response), or Last-Modified with If-Modified-Since (date-based, one-second resolution).
- evidence: [S-0023]
- topic: systems-software/http-caching
