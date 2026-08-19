# Dry Run Report — 2026-08-18 (user-POV)

## Persona

- **alias**: tester-tao (pseudonymous, synthetic test learner — no real user data touched; `.journey/` never written)
- **Self-assessment** (profile.json): systems-software = competent (mid-level dev), hardware = advanced-beginner, programming = novice
- **Created**: 2026-08-18; preferences: 1-day review interval, short-answer quiz style
- **Targets**: systems-software/http-caching (primary), programming/garbage-collection, hardware/cache-coherence — all `status: published` per frontmatter
- **Sessions**: s-tao-hc-001 (09:00Z), s-tao-gc-001 (10:00Z), s-tao-cc-001 (11:00Z)

## Test cases (table: topic | claim | expected verdict | actual verdict | tier | records | passed?)

| topic | claim (persona wording, abbreviated) | expected verdict | actual verdict | tier | records | passed? |
|---|---|---|---|---|---|---|
| http-caching | max-age counts from response generation; 30-min-held response with max-age=3600 has 30 min freshness left | correct | [correct] | T2 | S-0009 | YES |
| http-caching | max-age=600 + Expires → cache uses whichever gives the longer lifetime | partial | [partial] | T2 | S-0009 | YES |
| http-caching | no-cache means the response must not be stored anywhere; strongest anti-caching directive | incorrect | [incorrect] | T2 | S-0009 | YES |
| garbage-collection | Plain RC cannot reclaim cycles without extra cycle-detection machinery | correct | [correct] | T3 | S-0028 | YES |
| garbage-collection | Garbage collection eliminates memory leaks | partial | [partial] | T3 | S-0028 | YES |
| garbage-collection | Reference counting is not GC; it's an alternative to tracing collectors | incorrect | [incorrect] | T3 | S-0028 | YES |
| cache-coherence | Fully coherent system can still be non-SC; coherence = per-location, consistency = cross-location ordering | correct | [correct] | T3 | S-0040 (+S-0038 def.) | YES |
| cache-coherence | MESI is the coherence protocol modern processors implement | partial | [partial] | T3 | S-0040 (+S-0041) | YES |
| cache-coherence | Cache coherence and memory consistency are the same thing | incorrect | [incorrect] | T3 | S-0040 (+S-0038) | YES |

All verdicts derived exclusively from `concept.md` claims (per AGENTS.md §2 — answers from concept, not validation.md); every cited S-#### id verified to exist in `evidence/records/`. 9/9 predicted verdicts matched. Per-verdict detail (evidence line, corrected mental model, suggested validation.md items) is recorded in each `claim.verdict` event payload and was delivered to the learner in-session.

## Quiz session (items answered, scores, bloom_scores)

**http-caching only** (formative bank, validation.md Q1–Q3), answered as the persona:

| item | bloom | persona answer | correct? |
|---|---|---|---|
| Q1: which single directive truly prevents storage/reuse? | remember | `no-store` | YES |
| Q2: order of freshness-lifetime computation (max-age=600 + Expires + Date) | understand | s-maxage → max-age → Expires−Date → heuristic; Expires ignored when max-age present | YES |
| Q3: Age after 3 min resident time, max-age=300 — Age sent + fresh? | apply | "Age: 0 (Age is set by the origin); still fresh (0 < 300)" | NO — plausible mid-level mistake: forgot each cache adds its resident time; correct answer Age = 180, still fresh (180 < 300) |

- Score: 2/3 = **67**. `bloom_scores`: `{remember: 100, understand: 100, apply: 0}`
- The `apply` gap matches the learner's Q3 misconception and drove the `matrix.updated` (http-caching → level advanced-beginner, score 67, validated false) and next review 2026-08-21 (3-day ladder step).
- For GC and cache-coherence, `quiz.attempted` events are end-of-session retrieval probes per AGENTS.md (retrieval practice at session end), scored as persona: GC 33 (novice; `{remember:100, understand:0, apply:0}`), cache-coherence 33 (advanced-beginner; `{remember:100, understand:0, analyze:0}` — F4 answer reproduces the same coherence≠consistency misconception as claim 3, nice calibration signal).

## Journey artifacts (file tree + line counts + schema-validation result)

```
workspace/dryrun-journey/
├── profile.json                       (1 obj — PASS vs profile.schema.json)
├── state/
│   ├── skill-matrix.json              (1 obj — PASS vs skill-matrix.schema.json)
│   └── review-queue.json              (1 obj — PASS vs review-queue.schema.json)
└── logs/
    ├── 2026-08-18-http-caching.jsonl        (11 lines)
    ├── 2026-08-18-garbage-collection.jsonl  (11 lines)
    └── 2026-08-18-cache-coherence.jsonl     (11 lines)
workspace/reviews/
├── verify_dryrun.py                   (self-verify harness, stdlib + tools/_jsonschema_mini.py)
└── dry-run-report-2026-08-18.md       (this report)
```

- **33 event lines total**, one JSON object per line, event types per topic: `session.started` + 3×`claim.submitted` + 3×`claim.verdict` + `quiz.attempted` + `matrix.updated` + `review.completed` + `session.completed` (7 types, 11 lines/topic).
- **Schema validation: ALL PASS** — every JSONL line validated against `journey/schema/event.schema.json` and every state file against its schema using `tools/_jsonschema_mini.py` (run: `python workspace/reviews/verify_dryrun.py` → `RESULT: ALL PASS`, exit 0).
- Verified manually: `type` ∈ the 13-event enum (oneOf), `ts` date-time format, `topic`/`session_id` present, no extra top-level keys (`additionalProperties: false`).

## Harness findings (numbered; each: severity — issue — fix)

1. **High — `harness/prompts/` is empty (only `.gitkeep`).** Spec §9.3 promises 11 ready-made prompts incl. `validate-claim.md`; AC1 literally says "one pasted prompt from `harness/prompts/validate-claim.md`". The file does not exist, so AC1's exact procedure cannot be executed; the verdict flow had to be driven by AGENTS.md alone (which worked). Fix: ship the §9.3 prompt set (they are listed in spec and OVERVIEW claims they exist), or mark the folder as pending and add the prompt-file check to CI.
2. **High — INDEX.md and knowledge-graph.yml disagree on `status` for 14+ topics.** INDEX.md says `os-processes`, `parallel-programming`, `distributed-systems-basics`, `containers-isolation`, `os-scheduling`, `architectural-styles`, `modularity`, `design-patterns`, `system-design-process`, `caching-strategies`, `devops-pipeline`, `incident-response`, `observability`, `software-maintenance` are `published`; knowledge-graph.yml marks them `draft` (pack frontmatter confirms `published` — the graph is stale). Both are generated outputs that drifted from each other; a navigation agent could wrongly skip a publishable pack or misplace it in a corrective path. Fix: single generated source of truth (or regenerate both in one CI step with `git diff --exit-code`, which §12 already promises for index determinism).
3. **Medium — `event.schema.json` does not constrain `payload`.** Any payload shape validates, so a `claim.verdict` line may lack `verdict`/`tier`/`record` and still be schema-clean — the harness cannot machine-detect a malformed verdict, and the de-facto shapes live only in `journey/examples/session.example.jsonl` (this is documented as a known contract/gap in journey/README.md, Phase 4). Fix: per-type payload subschemas (`oneOf` on `type` with required payload keys), plus a calibration example (see #5).
4. **Medium — no documented dry-run/QA procedure.** AGENTS.md hardcodes `.journey/` as the journey root; nothing says how to point a session at a test root, and no documented command validates a journey against the schemas (`tools/lint.py` only covers committed examples). I had to invent `workspace/dryrun-journey/` + a bespoke verify script. Fix: add a `JOURNEY_ROOT` override note and a `tools/validate-journey.py` (or document `python workspace/reviews/verify_dryrun.py` as the QA entrypoint).
5. **Low — `journey/examples/` lacks calibration, session, checkpoint, and project-review examples.** Only 4 of 8 schemas have examples (profile, skill-matrix, review-queue, session-log). `calibration.schema.json` exists and §7 debrief requires calibration, but CI validates nothing for it. Fix: add synthetic examples for the 4 missing schemas so the contract for payload/entry shapes is pinned.
6. **Low — `journey/templates/` and `journey/privacy.md` don't exist yet** (README honestly marks them "Phase 4"; spec §8.1 tables them as committed conventions). Not a blocker, but a fresh agent may look for the session template. Fix: land them in Phase 4 with the rest of the known-gap list.
7. **Low — cache-coherence validation.md items are unlabeled.** GC/http-caching items have ids (F1..S4, Q1..Q10); cache-coherence items are unlabeled bullets, so `claim.verdict` "suggested item" pointers had to reference bank+position+first-words. Fix: normalize item ids across packs (also helps machines assemble interleaved review sets, spec §7).
8. **Low — no score→level mapping documented for `matrix.updated`.** The schema allows any 0–100 score with any level enum; I had to pick thresholds (67→advanced-beginner, 33→novice) from the example's implied mapping. Fix: document level thresholds (e.g., novice <40, advanced-beginner 40–69, competent 70–84, proficient 85–94, expert ≥95) in journey/README.md.
9. **Low — navigation friction.** For a single-claim session, INDEX.md (145 lines) is fine, but knowledge-graph.yml (762 lines) must be scanned wholesale to resolve prerequisites/corrective path for one topic; no per-topic lookup tool or small `grep`-able index. Fix (optional): a `tools/topic-info.py <id>` helper or machine-readable per-topic graph extracts.
10. **Info — no evidence gaps encountered.** Every verdict needed only records that exist (S-0009/23/24, S-0026/27/28, S-0038/39/40/41); no fabricated or missing-citation case arose. The no-cache/max-age/RC-is-GC/coherence-vs-consistency misconceptions were all covered by concept.md boundaries — packs were sufficient for all 9 test cases.

## AC1 / AC4 verdict (pass/fail per criterion, with evidence)

**AC1 — FAIL (procedurally), with working fallback.** Criterion: "fresh clone + one mainstream coding agent + one pasted prompt from `harness/prompts/validate-claim.md` yields a verdict with evidence tier + citations + corrective path, in a single session." The core capability works — 9/9 claims received a verdict with tier + real record ids + corrective model + suggested items in-session, driven purely by AGENTS.md §2 and concept.md (evidence: test-cases table + logs). But the literal criterion fails: `harness/prompts/validate-claim.md` does not exist (finding 1), so no agent can paste the specified prompt. AC1 is provisionally **pass-on-behavior, fail-on-requirement** until prompts ship.

**AC4 — PASS.** Criterion: "agent writes a full session (`session.completed`, `quiz.attempted`, `matrix.updated`) to `.journey/`; all lines validate against committed schemas; `git status` shows `.journey/` untracked; conventions documented in `journey/README.md`." Evidence:
- A full session (all 7 event types incl. the three named) was written per topic — 33/33 lines validate against `event.schema.json` (verify_dryrun.py, RESULT: ALL PASS); state files validate against their schemas.
- Test data was deliberately written to `workspace/dryrun-journey/` (gitignored workspace per spec §11), not `.journey/`; the real user's `.journey/` exists and was not touched (per constraints). AC4's "untracked" property holds by construction — workspace/ is gitignored (spec §11) and `.journey/` is gitignored (§8.3); no git commands were run.
- Conventions are documented in `journey/README.md` (rules, event taxonomy, known contracts); README's own caveat that payload shapes are unconstrained (finding 3) is the main residual risk to AC4's "schema-validated" promise.
