# SPEC — Journey Interface (Layer 5, ADR-0001)

- **Status:** Draft for review
- **Basis:** ADR-0001 (Journey Interface as a Consumer Layer), `docs/spec.md` §5.1, §7, §8
- **Selected direction:** Instrument-core hybrid (from `ui/explorations/instrument/brief.md`,
  informed by `ui/explorations/atelier/brief.md` and `ui/explorations/arcade/brief.md`)
- **Design system:** lives at `docs/design-system/` (`tokens.css`, `overview.md`, `tokens.md`,
  `components.md`, `patterns.md`). This spec references those paths as the single source of
  truth for tokens and components; it does not restate them.
- **Data contract:** the committed schemas (`journey/schema/*.schema.json`) and generated maps
  (`INDEX.md`, `knowledge-graph.yml`, `tracks.yml`). Every field cited in §4 exists in those
  files as of this writing; where the UI needs a field that does not exist, it is listed as a
  gap in §4.6 — never invented.

---

## 1. Vision & scope

The Journey Interface is a **local-first consumer UI** for the Strata harness (Layer 5,
ADR-0001). It renders one learner's journey and the committed knowledge maps as an honest
instrument panel: registers, tables, heatmaps, and calibration curves built from the same
data the harness reads.

- **Reads:** `.journey/` (private, per-developer) and the committed maps
  (`INDEX.md`, `knowledge-graph.yml`, `tracks.yml`, `knowledge/<track>/<topic>/*.md` frontmatter).
- **Writes:** only `.journey/`, exclusively via the event schema
  (`journey/schema/event.schema.json`, one JSON object per line in
  `.journey/logs/YYYY-MM-DD-<topic>.jsonl` per `journey/README.md`).
- **Never mutates** canonical knowledge, `evidence/records/`, or any committed file (PRs
  only, per AGENTS.md §6). The UI has no edit affordance over knowledge content.
- **No accounts, no telemetry, no cloud sync** (K5). The UI works from `file://`; journey
  data never leaves the machine.
- **Optional:** the UI is a consumer convenience; the harness remains fully functional
  without it. It is not an LMS and not a quiz platform (spec non-goal preserved): it
  renders validation banks and records events, it does not own curriculum.

The UI is built from the committed schemas as its contract (K6): field names are consumed
from the schemas, never hardcoded ad hoc, and unknown fields are tolerated gracefully (§7,
AC-UI-09).

## 2. Design principles

Derived from the Instrument-core hybrid; each principle is a derivation of the axioms, not
a stylistic preference.

1. **Action-first dashboard (critique lesson #1).** Every screen has exactly one primary
   action that is first-class: visually dominant, the first interactive control in reading
   order after skip-link navigation, reachable with a single Tab press, and never buried
   behind secondary controls. Screens are verbs, not displays.
2. **Provenance honesty.** Every datum on screen carries a provenance label: `REAL · <file>`
   (green) when it came from an actual file on this machine, `MOCK` (amber) when it is
   illustrative. Aggregated values additionally state their inputs ("derived from
   `skill-matrix.json.topics[].score`"). The footer restates the provenance policy. An
   instrument that lies about its readings is worse than no instrument.
3. **Progressive disclosure mirroring the harness (K3).** Screens are levels:
   L0 dashboard (aggregates only) → L1 topic explorer (maps) → L2 topic pack (loaded only
   when a topic is opened) → L3 evidence records and rubrics (on explicit drill-down).
   No topic-pack content is loaded to render an L0/L1 screen.
4. **Data-then-decor.** Numbers, tables, and structure precede styling: registers with
   labels and units, dense tables with tabular numerals, tick labels on every axis. Every
   decorative element is subordinate to a data element it duplicates or annotates; no
   number appears without its source label.
5. **Telemetry metaphor, not gamification.** Learning progress is measured telemetry of
   your own competence. The calibration curve shows overconfidence instead of hiding it;
   the event stream is the honest trace behind every headline number; streaks are plain
   counters or absent — never combos, rewards, or leaderboards (K5: no shared state to
   rank against; spec §4.1 calibration science).
6. **Convention-as-code (K6).** All visual tokens come from `docs/design-system/tokens.css`;
   all components from `docs/design-system/components.md`; no component-local hex values,
   no webfonts, no CDN (local-first, offline).

## 3. Screens & flows

Six screens, one per tab. All share the faceplate header (alias, LED row, theme toggle,
clock) and the tab rail (`role="tablist"`, arrow-key navigation). The tab rail exposes the
due-review count as a badge on the Review queue tab so "work exists" is visible at L0.

### 3.1 Dashboard (L0)

**Purpose.** The aggregate state of the journey at a glance: what is due, what is
validated, where the learner stands per track — the L0 summary the harness would read.

**PRIMARY ACTION — "Continue".** A single dominant control that starts the highest-
priority next step: (1) an overdue review from `review-queue.json.items[]` where
`due` < today; else (2) the next due review; else (3) a new session on the weakest
unvalidated topic by `skill-matrix.json.topics[<id>].score`. Label states the target
(e.g., "Continue: 1 review overdue — http-caching"). One Tab press from focus start
reaches it. It appends a `session.started` event on activation.

**Supporting content.**
- Alias register (`profile.json.alias`) and per-track level chips (`profile.json.levels`).
- Due registers: `due` count and `overdue` count computed from `review-queue.json.items[]`
  `due` vs today; validated count from `skill-matrix.json.topics[<id>].validated`.
- Index register: topic count and wave count from `knowledge-graph.yml` (`topic-count`,
  `wave-count`).
- Mastery sparkline / mean-score register derived from `skill-matrix.json.topics[].score`.
- Heatmap grid (track × band) with cell **counts as text**; tint encodes density; cells
  with learner-validated topics are marked with a distinct tick (legend in §3.1 pattern
  set). Counts are REAL (derived from `knowledge-graph.yml.topics[]` band/track); tint
  depth is derived — labeled as such, never MOCK unless simulated.
- Event stream preview: the last few lines of `.journey/logs/*.jsonl` (`type`, `ts`,
  `topic`, `payload` excerpt) — the honest trace, truncated with a link to Progress.

**Entry / exit.** Entry: app open. Exit: "Continue" → Review queue flow (3.5) or new
session; any tab switch; heatmap cell or register → Topic explorer (3.2).

**Empty states.**
- No `.journey/` at all: the dashboard renders structure with zero-filled registers and
  the PRIMARY ACTION becomes "Start first session" (opens the explorer to pick a topic);
  no fabricated history is shown; every empty register states its source file is absent.
- `.journey/` present but no `review-queue.json`: due registers show "no queue file",
  action (2)/(3) skip to (3) with the label explaining why.

### 3.2 Topic explorer (L1)

**Purpose.** The full topic inventory from the committed maps, browsable by track and
band, with learner state overlaid — the L1 map layer.

**PRIMARY ACTION — open a topic.** Each topic row is a large-target button (≥44 px)
that drills into the L2 topic pack (concept claims, validation items). Opening a topic
loads its `knowledge/<track>/<topic>/concept.md` + `validation.md` on demand — nothing
else loads.

**Supporting content.**
- Track chapters from `tracks.yml` (`tracks[]`, `track.<id>.title`, `.bands`, `.status`),
  rendered as `<details>` accordions with per-track counts (derived from
  `knowledge-graph.yml.topics[]` by `track`).
- Topic rows from `knowledge-graph.yml.topics[]`: `id`, `title`, `band`, `tier`,
  `bloom_target`, `status`, `depth`. Tier chips print the letter (`T0`–`T4`) per spec
  §6.3; status prints the word (`draft | validated | published`).
- Learner overlay per row: `skill-matrix.json.topics[<id>]` → `level`, `score`,
  `validated`; due marker from `review-queue.json.items[].topic/.due`.
- Legend strip: band axis B0–B6, tier axis T0–T4, status axis, learner markers
  (validated/due) — every legend entry pairs glyph with text (color-not-alone).
- Filter chips (`aria-pressed`): track, band, tier, status, "due", "unvalidated".

**Entry / exit.** Entry: dashboard heatmap cell or register, or tab. Exit: open topic →
L2 detail (back returns to explorer with filter state preserved); "Validate a claim"
button on a topic row → Validate flow (3.3) prefilled with that topic.

**Empty states.**
- Committed maps absent (no `knowledge-graph.yml` / `INDEX.md`): explorer renders an
  explicit "maps not found" state listing the expected files — never an empty track list
  that implies no topics exist.
- A topic id present in `.journey/` but missing from the maps: the row renders with the
  id as label and a "not in committed maps" tag (schema-tolerant join, §4.5).

### 3.3 Validate flow (L2)

**Purpose.** Submit a claim for validation and receive the verdict the harness would
produce — with the evidence chain shown, verbatim and cited.

**PRIMARY ACTION — "Submit claim".** A form (topic selector + claim textarea). Submit is
the single dominant control; on activation the UI appends a `claim.submitted` event
(payload carries the claim text) and shows the submitting state. The verdict itself is
produced by the harness agent flow, not by the UI: the UI renders verdicts that exist in
the event log and cannot fabricate one.

**Supporting content.**
- Topic selector: options from `knowledge-graph.yml.topics[]` (`id`, `title`); learner
  level for the chosen topic from `skill-matrix.json.topics[<id>].level` shown inline.
- Verdict card: renders the latest `claim.verdict` event for the topic —
  `payload.verdict` (word printed: CORRECT/PARTIAL/INCORRECT), `payload.tier`,
  `payload.record` (linked to `evidence/records/S-####.md`), `payload.note` (verbatim).
  If no verdict exists yet for the current claim, the card shows "awaiting verdict" —
  it never guesses.
- Corrective path strip: shortest path derived from
  `knowledge-graph.yml.topics[].prerequisites` / `.recommended` / `.related` from the
  learner's weakest mastered topic to the target; order-constrained edges (`▶`) vs
  related edges (`→`) per spec §6.2.
- Verdict history table: prior `claim.verdict` events for the topic from `logs/*.jsonl`
  (`ts`, `session_id`, `payload.verdict`, `payload.record`).

**Entry / exit.** Entry: "Validate a claim" from explorer (prefilled topic) or Dashboard.
Exit: verdict card offers "Continue to practice" → Quiz session (3.4) on the same topic,
or "Schedule review" → appends `review.due` event and returns to Dashboard.

**Empty states.**
- No `claim.submitted`/`claim.verdict` events for the topic: history table shows the
  empty trace ("no validation events on record") — the trace is honest about absence.
- Claim textarea is never pre-filled with simulated claims in the real build; prefills
  only reproduce a real prior `claim.submitted.payload.claim` if the user opts in.

### 3.4 Quiz session (L2)

**Purpose.** Retrieval practice from the topic's validation bank with immediate
feedback, recorded as events.

**PRIMARY ACTION — the active answer.** During an item, the answer options (or "show
answer" for open items) are the primary controls; exactly one answer action is enabled
per item. After feedback, the PRIMARY ACTION becomes "Next item". Feedback is immediate
(spec §7: retrieval practice with immediate feedback).

**Supporting content.**
- Bank selector (`formative | summative | review`) — banks from `validation.md` items'
  `bank` field (spec §7). Review bank items are the interleaved set assembled from
  `review-queue.json.items[].topic` and that topic's `prerequisites`.
- Item card: `Q` question, `bloom` tag, `bank` tag, `evidence` list (`S-####` chips),
  `topic` (required per spec §7). Multiple-choice items render `distractors` when
  present; otherwise the item is open-answer with a reveal.
- Feedback panel: model answer `A` (verbatim from `validation.md`), correct/wrong
  states printed as words, `aria-live="polite"`.
- Score register + item counter; on completion appends `quiz.attempted` with
  `payload.bank`, `payload.score`, `payload.bloom_scores` (shape per §4.4 gap note).
- Ladder affordance: current position vs spacing schedule 1/3/7/14/30/60/120 (spec
  §4.1) with `review-queue.json.items[].interval_days` when in review bank.

**Entry / exit.** Entry: "Continue to practice" from Validate, or "Start review
session" from Review queue (prefilled review bank), or bank pick from a topic in the
explorer. Exit: results register → "Schedule review" (`review.due` event) or "Back to
dashboard".

**Empty states.**
- Topic has no `validation.md` or no items in the chosen bank: the session cannot
  start; the screen states exactly which file/bank is missing and offers another bank
  or topic. A quiz is never manufactured from non-existent items.

### 3.5 Review queue (L3-adjacent scheduling)

**Purpose.** The spaced-repetition queue: what is due, what is scheduled, and where each
topic sits on the spacing ladder.

**PRIMARY ACTION — "Start review session".** Opens a native `<dialog>` manifest of the
due items (from `review-queue.json.items[]` where `due` ≤ today), their `interval_days`
and `reviews` count, and the interleaved-set note; confirming appends `session.started`
and enters the Quiz session (3.4) in review bank. Disabled with a reason when nothing is
due.

**Supporting content.**
- Due table: `review-queue.json.items[]` → `topic`, `due` (relative to today: overdue /
  today / in N days), `interval_days`, `reviews`, `last_review`. Sort: overdue first,
  then by `due`.
- Spacing ladder: per item, rungs 1–3–7–14–30–60–120 (spec §4.1) with position marks
  from `interval_days` and `reviews`.
- Session control/status line: last `session.started`/`session.completed` event for the
  session (`session.schema.json` fields `session_id`, `status`, `started`, `completed`,
  `objective`).
- Session manifest dialog lists items and warns which have unmet `prerequisites`
  (`knowledge-graph.yml.topics[].prerequisites`).

**Entry / exit.** Entry: Dashboard "Continue", queue tab, or "Schedule review" from
Validate/Quiz (which appends `review.due` and returns here). Exit: "Start review
session" → Quiz; item row → Topic explorer.

**Empty states.**
- Queue file absent: "no review queue yet — complete a validation or quiz session and
  the harness will schedule reviews"; the screen still renders the ladder legend.
- Queue present, nothing due: "nothing due — next: <earliest due>"; the PRIMARY ACTION
  is disabled with the date reason visible.

### 3.6 Progress & calibration (L3)

**Purpose.** The longitudinal view: skill matrix, score history, calibration curve, and
the raw event stream — the deepest, most honest screen. It is allowed to be dense; it is
never allowed to be silent about missing data.

**PRIMARY ACTION — inspect a topic's record.** Selecting a topic row in the matrix
table opens that topic's detail pane: score history (derived from `quiz.attempted`
events), verdict history (`claim.verdict` events), and its calibration points. The row
is the primary control; the detail pane is a first-class region, not a hover tooltip.

**Supporting content.**
- Skill matrix table: `skill-matrix.json.topics[<id>]` → `level`, `score`, `validated`,
  `last_attempt`, `evidence` (linked `S-####` records); topic titles joined from
  `knowledge-graph.yml`.
- Calibration chart: predicted-vs-actual points from the `calibration.updated` event
  payload (predicted vs actual per topic, spec §4.1 Flavell), ideal diagonal `y=x`,
  dashed gridlines, labeled axes, legend, `role="img"` + title/desc. Every point
  carries its topic and date. **The chart is REAL only when calibration data exists on
  disk; otherwise it renders the empty state below — it is never populated with
  illustrative points.** (Contract gap: §4.4.)
- Score history sparklines: aggregate of `quiz.attempted` events (`payload.score`) per
  topic — labeled "derived from quiz.attempted events".
- Event stream: `.journey/logs/*.jsonl` rendered as rows (`ts`, `type`, `session_id`,
  `topic`, `payload` excerpt) with type badges; filterable by type. This is the
  source-of-truth trace under every headline number.
- Checkpoint and project-review records validating against `checkpoint.schema.json`
  (`topic`, `date`, `verdict`, `bloom_levels`, `next_actions`, `next_review`,
  `evidence`) and `project-review.schema.json` (`topic`, `rubric`, `verdict`,
  `reviewed`, `reviewer`, `standards-refs`, `scores`, `evidence`, `notes`) when
  present in `.journey/`.
- Calibration stats registers: mean absolute error, over/under-confidence sign —
  derived only from real calibration data, else absent.

**Entry / exit.** Entry: tab, or "Event stream" link from Dashboard. Exit: topic row →
detail pane (L3); "Review evidence record" → `evidence/records/S-####.md` in a
read-only viewer (never an editor).

**Empty states.**
- No logs: the stream renders "no events recorded"; every derived chart/sparkline shows
  its explicit absence state ("insufficient data — needs N+ quiz attempts"), never a
  blank axis that implies zero.
- No calibration data: the chart region renders "no calibration data on record —
  calibration.updated events accumulate it" (the mechanism from spec §8.2), and the
  registers are omitted.

## 4. Data contracts

The UI consumes the committed schemas as its contract. Field names below are quoted
exactly as they appear in `journey/schema/*.schema.json`, topic frontmatter, and the
generated maps; the mapping tables are the contract a real build must render from.

### 4.1 Shared chrome

| UI element | Source |
|---|---|
| Alias register | `profile.json.alias` |
| Per-track level chips | `profile.json.levels[<track>]` (enum: `novice`, `advanced-beginner`, `competent`, `proficient`, `expert`) |
| Profile dates | `profile.json.created`, `profile.json.updated` |
| Theme preference | `profile.json.preferences` (free object; may hold `language`, theme) or `localStorage` — both local-only |
| Due LED / queue badge | `review-queue.json.items[].due` (count where `due` ≤ today) |
| JRNY LOCAL LED | static (no data dependency) |
| Screen titles, tier/status legend text | spec §6.3 tier table; static copy |

### 4.2 Dashboard

| UI element | Source |
|---|---|
| Continue action target | `review-queue.json.items[]` (`topic`, `due`) then `skill-matrix.json.topics[<id>]` (`score`, `validated`) |
| Due / overdue registers | `review-queue.json.items[].due` vs today; `interval_days`, `reviews` for context |
| Validated register | `skill-matrix.json.topics[<id>].validated` (count of `true`) |
| Mastery mean / sparkline | `skill-matrix.json.topics[].score`, `last_attempt` |
| Topic index register | `knowledge-graph.yml.topic-count`, `knowledge-graph.yml.wave-count` |
| Heatmap grid (track × band) | derived: `knowledge-graph.yml.topics[]` (`track`, `band`) → counts; validated overlay from `skill-matrix.json.topics[<id>].validated` |
| Event stream preview | `logs/YYYY-MM-DD-*.jsonl` lines: `type`, `ts`, `session_id`, `topic`, `payload` |
| Streak counter | **GAP-4** — see §4.4; otherwise omitted, never invented |

### 4.3 Topic explorer / Validate flow / Quiz / Review queue

| UI element | Source |
|---|---|
| Track chapters | `tracks.yml.tracks[]`; `track.<id>.title`, `track.<id>.bands`, `track.<id>.status` |
| Topic rows | `knowledge-graph.yml.topics[]`: `id`, `title`, `track`, `band`, `tier`, `bloom_target`, `status`, `depth` |
| Corrective path | `knowledge-graph.yml.topics[].prerequisites` (order-constrained), `.recommended`, `.related` (spec §6.2) |
| Learner overlay per topic | `skill-matrix.json.topics[<id>]`: `level`, `score`, `validated`, `last_attempt`, `evidence` |
| Due marker per topic | `review-queue.json.items[].topic`, `.due` |
| Topic pack (L2) | `concept.md` frontmatter: `id`, `title`, `band`, `track`, `tier`, `bloom_target`, `prerequisites`, `related`, `recommended`, `status`, `updated`, `sources`; claims with inline `[T*]` `[S-####]` tags |
| Claim submission | appends `event.schema.json` line `type: "claim.submitted"` with `payload.claim` |
| Verdict card | latest `claim.verdict` event `payload`: `verdict`, `tier`, `record`, `note` (de facto shape — **GAP-2**) |
| Evidence chips | `payload.record` → `evidence/records/S-####.md` |
| Verdict history | prior `claim.verdict` events: `ts`, `session_id`, `topic`, `payload.verdict` |
| Bank selector | `validation.md` items: `bank` (`formative`/`summative`/`review` per spec §7) |
| Quiz items | `validation.md` items: `Q`, `bloom`, `bank`, `A`, `evidence`, `topic` (required per spec §7), `distractors` (optional) |
| Feedback body | `validation.md` item `A` (model answer, verbatim) |
| Quiz result | appends `quiz.attempted` with `payload`: `bank`, `score`, `bloom_scores` (de facto shape — **GAP-2**) |
| Review ladder | spec §4.1 schedule 1, 3, 7, 14, 30, 60, 120 + `review-queue.json.items[].interval_days`, `.reviews` |
| Session manifest / control | `session.schema.json`: `session_id`, `status` (`active`/`completed`), `started`, `completed`, `objective`, `agent`; appends `session.started` / `session.completed` |
| Scheduling actions | appends `review.due` / `review.completed` event lines |

### 4.4 Progress & calibration

| UI element | Source |
|---|---|
| Matrix table | `skill-matrix.json.topics[<id>]`: `level`, `score`, `validated`, `last_attempt`, `evidence` |
| Topic titles in matrix | joined from `knowledge-graph.yml.topics[].title` by `id` |
| Calibration chart | `calibration.updated` events, `payload` predicted vs actual per topic (spec §4.1, §8.2) — **GAP-1** |
| Score history sparks | derived: `quiz.attempted` events `payload.score` per `topic` |
| Event stream rows | `logs/*.jsonl`: `type`, `ts`, `session_id`, `topic`, `payload` |
| Checkpoint records | files validating `checkpoint.schema.json`: `topic`, `date`, `verdict` (`pass`/`partial`/`fail`), `bloom_levels`, `next_actions`, `next_review`, `evidence` — **GAP-5** (no committed location) |
| Project review records | files validating `project-review.schema.json`: `topic`, `rubric`, `artifact`, `verdict`, `reviewed`, `reviewer`, `standards-refs`, `scores`, `evidence`, `notes` — **GAP-5** |
| Calibration registers (MAE etc.) | derived from real calibration data only; absent otherwise |

### 4.5 Tolerance rules

- Topic ids in `.journey/` without a match in `knowledge-graph.yml.topics[].id`: render
  the id as label + "not in committed maps" tag; never crash.
- Unknown fields in any file: ignored (the schemas use `additionalProperties: false`,
  but the UI must not hard-depend on that enforcement; a tolerant reader ignores extras).
- `schema-version` mismatches (`const: 1` in profile/skill-matrix/review-queue): show a
  labeled "unsupported schema version" state for that file; do not attempt partial render.
- Event types in `logs/*.jsonl` outside the `event.schema.json` `oneOf` list: render the
  generic row with the type as printed; no type-specific rendering.

### 4.6 Schema gaps the UI needs (proposed, not invented)

| # | Gap | Evidence of need |
|---|---|---|
| GAP-1 | No calibration state schema. `calibration.updated` exists in `event.schema.json` but its `payload` is unconstrained; `docs/plan.md` §4.3 proposes `state/calibration.json` (predicted vs actual per topic) with no schema in `journey/schema/`. The calibration chart (§3.6) has no committed contract. | Propose `journey/schema/calibration.schema.json` + a constrained `payload` shape for `calibration.updated`. |
| GAP-2 | Event `payload` shapes unconstrained. `event.schema.json`'s `oneOf` constrains only `type`; `payload.verdict/tier/record/note` (claim.verdict) and `payload.bank/score/bloom_scores` (quiz.attempted) exist only as de facto conventions in `journey/examples/session.example.jsonl`. The UI renders these verbatim and needs them contractual. | Propose per-type `payload` subschemas in `event.schema.json`. |
| GAP-3 | Verdict vocabulary drift. Claim events use `correct|partial|incorrect` (spec §8.2, example), while `checkpoint.schema.json` and `project-review.schema.json` use `pass|partial|fail`. A single verdict axis renders inconsistently today. | Propose one vocabulary (or an explicit mapping table in the schema docs). |
| GAP-4 | No streak / last-activity field. Streaks can only be derived from `session.completed` `ts` in logs; both instrument and arcade explorations flagged it. The dashboard either derives it or omits it. | Accept derivation rule; no schema change strictly required. |
| GAP-5 | No committed location convention for checkpoint / project-review records inside `.journey/` (README lists `profile.json`, `state/`, `logs/`, `artifacts/` only). The UI needs a discovery rule to render §3.6 records. | Propose `state/checkpoints/` + `state/project-reviews/` in `journey/README.md`. |

## 5. Accessibility

WCAG 2.2 AA, applied via the design-system tokens (`docs/design-system/tokens.css`).
The Instrument direction's density is an accessibility risk; this section is the floor,
not the ceiling.

1. **Contrast.** Every text-bearing pairing ≥ 4.5:1 (normal) and ≥ 3:1 (large ≥ 24px or
   ≥ 18.66px bold) in both themes, per `docs/design-system/tokens.md`; non-text UI
   components (focus ring, meter tracks, legend swatches) ≥ 3:1 against adjacent colors
   (WCAG 1.4.11). Decorative rules and tick marks are exempt and documented as such in
   the token docs; no text token below the AA floor is used for information.
2. **Visible focus (WCAG 2.4.11/2.4.13).** `:focus-visible` renders a 2px ring from a
   dedicated focus token, ≥ 3:1 vs both the element and its surroundings; focus is never
   removed programmatically and is never obscured by sticky chrome.
3. **Keyboard navigation.** Every control is operable by keyboard alone: natural Tab
   order matching visual order; tab rail uses roving tabindex with Arrow/Home/End keys;
   accordions and dialogs are native `<details>`/`<dialog>`; dialog closes on Esc and
   returns focus; no focus traps; skip link first in the document. Focus start on each
   screen is the PRIMARY ACTION control (after skip link).
4. **prefers-reduced-motion (WCAG 2.3.3).** All non-essential animation is disabled
   under `prefers-reduced-motion: reduce`; no animation is required to understand any
   state — due/verdict/validated states always carry text, never motion or blink alone.
5. **Color-not-alone (WCAG 1.4.1).** Meaning is never carried by hue alone: verdicts
   print CORRECT/PARTIAL/INCORRECT; tiers print `T0`–`T4`; status prints
   draft/validated/published; heatmap cells print counts; LEDs carry text labels;
   sparklines sit beside numeric values; every chart has a data table or numeric
   readout nearby.
6. **Typography floor.** No information-bearing text below **12px (0.75rem)** at the
   default root size. Sub-12px text is restricted to decorative tick labels that
   duplicate adjacent information. Body copy is proportional sans; mono is reserved for
   data (ids, dates, scores, records) — a semantic, not stylistic, choice.
7. **Target size (WCAG 2.5.8).** Interactive targets ≥ 24×24 CSS px; primary actions
   and topic rows ≥ 44×44 px; all controls are native buttons/links.
8. **Structure & live regions.** One `h1` per screen; landmarks (`header`, `nav`, `main`,
   `footer`); tables use `th scope`; `aria-live="polite"` on verdict output, quiz
   feedback, and status lines; SVG charts expose `role="img"` with `<title>`/`<desc>`.

## 6. Local-first & privacy

1. **`file://` capability.** The app runs from `file://` with no server: no CDN, no
   web fonts, no remote fetches. Where browser policy blocks directory reads from
   `file://`, the UI offers an explicit folder picker for `.journey/` (File System
   Access API / `<input type="file" webkitdirectory>`) and reads the committed maps
   from the repo directory in the same way. A loopback-only local server is a supported
   convenience, never a requirement.
2. **No telemetry, no accounts.** No analytics, no network requests, no accounts, no
   cloud sync. The only persisted local state is the theme preference (in
   `profile.json.preferences` or `localStorage`). No learner data is written anywhere
   but `.journey/`.
3. **`.journey/` layout expectations** (per `journey/README.md` and spec §8.1):
   `profile.json`, `state/skill-matrix.json`, `state/review-queue.json`,
   `logs/YYYY-MM-DD-<topic>.jsonl` (append-only, one object per line), `artifacts/`.
   The UI discovers exactly these; everything else is tolerated and ignored.
4. **Write discipline.** All UI-initiated writes append event lines to
   `.journey/logs/` strictly per `event.schema.json`. The UI never rewrites
   `skill-matrix.json`, `review-queue.json`, or `profile.json` — those are the
   harness's outputs; the UI only records the events (quiz.attempted, review.completed,
   session.started/completed, claim.submitted) from which the harness updates them.
5. **Absent files.** Every screen has a defined empty state (§3) naming the missing
   file(s) and the way to create them (run a harness session). Missing files render
   structure + explicit absence — never errors walls, never fabricated values, never
   implied zeros where data is merely missing.

## 7. Acceptance criteria

Numbered, testable. All criteria are evaluated against the committed schemas and
example files as fixtures, on a machine with no network access.

- **AC-UI-01 — Action-first dashboard.** On the Dashboard, exactly one control is the
  PRIMARY ACTION ("Continue"); it is the first focusable control after the skip link,
  visually dominant per `docs/design-system/components.md`, and its label states its
  concrete target (e.g., "Continue: 1 review overdue"). With no due reviews it targets a
  new session on the lowest-`score` unvalidated topic; with no `.journey/` data at all,
  it reads "Start first session". The target selection rule (§3.1) is exercised by a
  fixture test.
- **AC-UI-02 — Provenance labels.** Every data-derived value on every screen carries a
  visible provenance label: `REAL · <path>` (green) or `MOCK` (amber); derived values
  additionally list their input fields. A fixture sweep over all six screens finds no
  unlabeled numeric or status value, and no `MOCK` value that a fixture file actually
  provides. The footer restates the provenance policy.
- **AC-UI-03 — Heatmap legend.** The Dashboard heatmap and the Topic explorer legend
  render a legend that maps every fill/tick to a text meaning (count, validated marker,
  due marker). With a simulated color-vision deficiency (greyscale render), every
  heatmap cell remains interpretable from its printed count and text markers alone.
- **AC-UI-04 — Calibration honesty.** The calibration chart (Progress screen) renders
  points only from real `calibration.updated` events; with no such events on disk it
  renders the defined "no calibration data" empty state and shows no axes implying
  measurements. A fixture with two calibration events renders exactly two points with
  their topics and dates, the `y=x` diagonal, labeled axes, and legend.
- **AC-UI-05 — Keyboard operability.** All six screens are fully operable with the
  keyboard alone: Tab order follows visual order; the tab rail supports Arrow/Home/End;
  every `<dialog>` closes on Esc and returns focus; no focus is trapped; the PRIMARY
  ACTION is reachable within one Tab from focus start on every screen. Verified by an
  automated traversal script.
- **AC-UI-06 — Visible focus.** `:focus-visible` is never suppressed; the focus ring
  token is applied to every interactive element and has ≥ 3:1 contrast in both themes.
  Verified by fixture screenshots in light and dark themes.
- **AC-UI-07 — Reduced motion.** With `prefers-reduced-motion: reduce`, no
  transitions, chevron animations, or chart animations run; all due/verdict/validated
  states remain fully communicated by text. Verified by fixture screenshot comparison.
- **AC-UI-08 — Color-not-alone.** No state is encoded by color alone: verdicts print
  words, tiers print `T0`–`T4`, statuses print draft/validated/published, heatmap cells
  print counts, LEDs carry text. Verified by greyscale screenshot review of all six
  screens and an assertion that each colored element carries a text alternative.
- **AC-UI-09 — Schema-driven rendering with graceful tolerance.** The UI renders every
  element from the committed schema contract (no hardcoded field names outside the
  mapping tables in §4). Fixture tests: (a) a fixture with an unknown extra field in a
  journey file renders identically and does not crash; (b) a topic id present in
  `.journey/` but absent from `knowledge-graph.yml` renders with the "not in committed
  maps" tag; (c) a `schema-version` ≠ 1 file renders its labeled "unsupported schema
  version" state; (d) an unknown event `type` in a log renders the generic row.
- **AC-UI-10 — Local-only writes.** No UI action writes outside `.journey/`; every
  UI-initiated write is an event line appended to `.journey/logs/` that validates
  against `event.schema.json` (verified with `tools/lint.py` on the fixture output).
  A network-monitoring fixture run (browser devtools, offline mode) shows zero
  outbound requests across all six screens and all flows.
- **AC-UI-11 — `file://` operation.** The app functions fully from `file://` with no
  server and no network: all six screens render, the Continue flow completes a session
  start, and the folder-picker path loads a fixture `.journey/` directory. No CDN or
  remote font is referenced anywhere in the built assets.
- **AC-UI-12 — Progressive disclosure.** L0/L1 screens (Dashboard, Topic explorer)
  load no topic-pack content: a fixture DOM/network assertion shows no
  `concept.md`/`validation.md` payloads in initial render, and the L2 topic pack loads
  only when a topic is opened; evidence records (L3) load only on explicit drill-down.

## 8. Out of scope

- **Server sync, accounts, cloud storage, multi-device** — journey data stays on the
  machine (K5). Sharing an anonymized summary would require the explicit opt-in flow
  from spec §8.3 and is not built here.
- **Editing canonical knowledge** — no creation, modification, or deletion of
  `knowledge/`, `evidence/`, `docs/`, or any committed file from the UI (PRs only,
  AGENTS.md §6).
- **Mobile apps** — no native mobile clients; the UI is a desktop browser app. A
  narrow-viewport responsive fallback is allowed but not a mobile product.
- **LMS / quiz-platform features** — the UI is not a curriculum authoring tool, does
  not own scoring rules beyond recording events, and does not implement the harness's
  validation/teaching behavior itself (spec non-goal preserved).
- **Gamification systems** — leaderboards, rewards, XP economies, and streak
  mechanics beyond a plain counter (telemetry metaphor, §2.5).
- **Telemetry/analytics of usage** — the UI itself is never instrumented.
- **Real-time collaboration or multi-user journey data.**
- **Authentication/authorization infrastructure** — none exists by design; nothing is
  added.
