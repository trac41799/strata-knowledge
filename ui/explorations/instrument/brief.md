# Design Direction: "Instrument" — a precision data cockpit for Strata's journey UI

**Direction ID:** `ui/explorations/instrument/` · **Agent:** L1 UI/UX (Strata build team) · **Date:** 2026-08-18
**Scope:** Layer 5 consumer UI (ADR-0001). This is a design exploration: one self-contained prototype (`index.html`) + this brief. No other files touched.

---

## 1. Thesis

Learning progress is measurable telemetry; the UI should behave like an instrument panel for your own competence — dense, honest, and calibrated, never gamified. Strata's journey data is already structured telemetry (schema-validated events, scores, intervals, tiers), so the cockpit renders it with instrument-grade precision: heatmaps, sparklines, calibration curves, status LEDs, and fine gridlines — dark-first, monospace-accented, crafted like test equipment rather than a marketing dashboard.

**Two lines:** Learning progress is telemetry; the cockpit displays it like test equipment — heatmaps, calibration curves, LEDs, and tick marks instead of cards, gradients, and charts-that-flatter. Every number on screen names its source field (schema path) or is explicitly tagged MOCK, because an instrument that lies about its readings is worse than no instrument.

Design axioms honored: K3 progressive disclosure (overview → maps → topic → deep artifacts = screens 1→2→3/4→5/6); K5 local-first (OP header, no accounts, "JRNY LOCAL" LED); K6 convention-as-code (all tokens are CSS custom properties; every data element carries its schema path or MOCK tag).

---

## 2. Palette

All ratios computed per WCAG 2.1 (relative luminance formula). **Dark theme** (default) tokens live in `:root`; **light theme** under `:root[data-theme="light"]` and the `prefers-color-scheme: light` media query. Text tokens are paired with the backgrounds they actually sit on (page `--bg-0`, panel `--bg-1`, header/raised `--bg-2`).

### 2.1 Dark theme (default)

| Token | Hex | Usage | Contrast vs bg |
|---|---|---|---|
| `--bg-0` | `#0A0E14` | page canvas (tickbar/backdrop) | — |
| `--bg-1` | `#0F151E` | panel body | — |
| `--bg-2` | `#131B26` | panel headers, raised rows | — |
| `--bg-3` | `#182130` | hover state, meter track | — |
| `--line` | `#1D2A3A` | panel borders, table rules (decorative) | — |
| `--text-1` | `#D3DCE8` | primary text | **14.0:1** on bg-0 · 13.2:1 on bg-1 · 13.4:1 on bg-2 |
| `--text-2` | `#8494A9` | secondary/micro labels | **6.7:1** on bg-0 · 5.9:1 on bg-1 · 5.6:1 on bg-2 |
| `--text-3` | `#5B6B7F` | tick marks, disabled states only | 3.6:1 — decorative/disabled only, never body copy |
| `--acc-teal` | `#2DD4BF` | primary accent (active tab, LED, path, spark) | **10.4:1** on bg-0 · 9.8:1 on bg-1 |
| `--acc-amber` | `#F5A623` | secondary accent (warn, MOCK tag, highlight) | **9.5:1** on bg-0 · 9.0:1 on bg-1 |
| `--ok` | `#34D399` | correct / published / validated | 10.1:1 on bg-0 |
| `--err` | `#F87171` | incorrect / retired | 7.0:1 on bg-0 |
| `--info` | `#60A5FA` | agent-link LED, T1 tier | 7.6:1 on bg-0 |
| `--t0` | `#C084FC` | T0 tier (formal) | 7.3:1 on bg-0 |
| `--t4` | `#F472B6` | T4 tier (frontier) | 7.3:1 on bg-0 |
| `--tint-teal` | `rgba(45,212,191,.14)` | tag/chip fill | chip text `--chip-teal` = 7.5:1 on tint over bg-1 |
| `--tint-amber` | `rgba(245,166,35,.14)` | partial/amber chips | `--chip-amber` = 7.1:1 |
| `--tint-ok` / `--tint-err` / `--tint-info` / `--tint-t0` / `--tint-t4` | rgba fills ~.13 | status & tier chips | chip text tokens 6.5–7.5:1 |

Tier chips double as the evidence-confidence axis (spec §6.3): T0 violet, T1 blue, T2 teal, T3 amber, T4 magenta. Status chips: draft = neutral outline, published = green, validated = blue.

### 2.2 Light theme (`data-theme="light"` / `prefers-color-scheme: light`)

| Token | Hex | Usage | Contrast vs bg |
|---|---|---|---|
| `--bg-0` | `#F4F6F8` | page | — |
| `--bg-1` | `#FAFBFC` | panels | — |
| `--bg-2` | `#FFFFFF` | headers/raised | — |
| `--text-1` | `#1B2733` | primary | **14.0:1** on bg-0 |
| `--text-2` | `#4A5A6B` | secondary | **6.5:1** on bg-0 |
| `--acc-teal` | `#0F766E` | primary accent (text-safe on light) | 5.1:1 on bg-0 |
| `--acc-amber` | `#8A5B00` | secondary accent | 5.4:1 on bg-0 |
| `--ok` | `#15803D` | correct | 4.6:1 on bg-0 |
| `--err` | `#B91C1C` | incorrect | 6.0:1 on bg-0 |
| `--info` | `#1D4ED8` | info/T1 | 6.2:1 on bg-0 |
| `--t0` | `#7C3AED` | T0 | 5.3:1 |
| `--t3` | `#8A5B00` | T3 | 4.7:1 (large-text-safe for labels) |
| `--t4` | `#BE185D` | T4 | 5.6:1 |
| `--tint-*` | solid pale fills (`#E4F0EF` teal, `#F4E8D0` amber, …) | chips | chip text tokens 4.7–6.1:1 (rgba tints fail contrast on light — replaced by solid fills) |

Rule: **every text-bearing color in both themes ≥ 4.5:1** (small) or ≥ 3:1 (large `≥18.66px` bold / `≥24px`), verified in §2.1/§2.2. `--text-3` is the single exception, restricted to decorative tick marks and disabled controls (WCAG-flagged, see §7).

---

## 3. Type scale

Stack: `--sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` (body) · `--mono: ui-monospace, "SF Mono", "Cascadia Mono", "JetBrains Mono", Menlo, Consolas, monospace` (data). No webfonts, no CDN (ADR-0001 local-first, offline).

| Step | Size / line-height | Face | Usage |
|---|---|---|---|
| `--fs-0` micro | 0.625rem / 1.4 | mono, uppercase, `letter-spacing:.09em` | panel labels, table headers, tick labels, tags |
| `--fs-1` small | 0.6875rem / 1.4 | mono | log lines, filter chips, path nodes, LEDs row |
| `--fs-2` body | 0.8125rem / 1.5 | sans | body copy, table cells (tabulated numerals) |
| `--fs-3` lead | 0.9375rem / 1.55 | sans | quiz question text, brand |
| `--fs-4` h2 | 1.25rem / 1.3 | mono, letter-spacing | screen titles, register values |
| `--fs-5` stat | 1.5rem / 1.3 | mono, tabular | stat values (68, 12, +0.18) |

Discipline: prose is sans; every *datum* is mono. Tabular numerals on all numeric columns so columns align like meter registers.

---

## 4. Pattern language

1. **Faceplate chrome** — tick-bar rule (repeating 1px ticks) above the header; panel corner registration marks (1px L-corners via `::before/::after`); panel titles prefixed `▍` like a channel marker. Reads as hardware, not SaaS.
2. **Status LEDs** — 8px dots with glow (`box-shadow`), always paired with a text label: `JRNY LOCAL`, `AGENT LINK`, `2 DUE`. Off-LED = neutral slate.
3. **Registers** — label-over-value readouts (`rlab` micro-caps + `rval` mono), each backed by a meter bar with an edge tick at the value boundary.
4. **Bracket tags** — `[T2]`, `[S-0009]`, `PUBLISHED`, `MOCK`, `REAL`: mono chips whose color carries the tier/status axis (never color alone — text present).
5. **Dense tables** — sticky headers in mono micro-caps, hairline rows, hover row tint, right-aligned tabular numerics, `data-source` provenance on real rows.
6. **Heatmap grid** — 3px-gutter cell matrix (track × band) with counts as text; tint encodes mastery (mock), amber cell = learner-validated. Color is redundant with the number.
7. **Sparklines** — inline SVG polylines with soft area fill; used for streak and score history.
8. **Calibration chart** — SVG line chart with dashed gridlines, tick labels, ideal diagonal (`y=x`), teal predicted vs amber actual, legend, `role="img"` + `<title>/<desc>`.
9. **Corrective path strip** — node/edge chain (`▶` = order-constrained prerequisite, `→` = related edge) rendered as bracketed stations.
10. **Event stream** — JSONL log lines with timestamp + type badge (SESSION/CLAIM/VERDICT/QUIZ/MATRIX) + payload excerpt; the honest trace behind every headline number.
11. **Dialog** — native `<dialog>` for session start with the interleaved item manifest; form-dismissable.
12. **Mock discipline** — every illustrative value carries a `MOCK` tag (amber) or `REAL · <file>` (green) provenance tag; the footer restates the provenance policy.

Anti-patterns deliberately avoided: rounded-corner cards, drop shadows on cards, purple-to-blue gradients, emoji, oversized hero numbers without units, chart axes without tick labels, dark-only UI.

---

## 5. Component inventory (26) → screens

| # | Component | Screens |
|---|---|---|
| 1 | Faceplate header (brand + LED row + clock + theme switch) | all |
| 2 | Tab bar (role=tablist, arrow-key nav) | all |
| 3 | Status LED (on/warn/err/idle/off) | 1, 3, 6 |
| 4 | Stat register (label + value + unit) | 1, 2 |
| 5 | Meter bar with edge tick | 1, 4 |
| 6 | Sparkline (SVG polyline + area) | 1, 6 |
| 7 | Heatmap grid (counts + tint) | 1 |
| 8 | Dense data table (sticky header, tabular nums) | 1, 2, 3, 5, 6 |
| 9 | Bracket tag (tier / status / evidence / MOCK / REAL) | 1, 2, 3, 4, 5, 6 |
| 10 | Track accordion (`<details>`, ▸ toggle, counts) | 2 |
| 11 | Filter chip group (aria-pressed) | 2, 4 |
| 12 | Legend strip | 2 |
| 13 | Claim input form (textarea + topic select) | 3 |
| 14 | Verdict card (badge + matched claims + gaps + corrected model) | 3 |
| 15 | Corrective path strip (prereq/related edges) | 3 |
| 16 | Verdict history table | 3 |
| 17 | Quiz item card (bloom/evidence tags + options) | 4 |
| 18 | Answer option (immediate correct/wrong state) | 4 |
| 19 | Feedback panel (LED + title + explanation) | 4 |
| 20 | Score register + timer | 4 |
| 21 | Bank selector (formative/summative/review) | 4 |
| 22 | Review queue table | 1, 5 |
| 23 | Spacing ladder (1–3–7–14–30–60–120d with position marks) | 5 |
| 24 | Session control + status line | 5 |
| 25 | Native `<dialog>` session manifest | 5 |
| 26 | Calibration chart (SVG, gridlines, ticks, legend) | 6 |

---

## 6. Data mapping (UI element ← source field)

Real data used: `journey/examples/profile.example.json`, `skill-matrix.example.json`, `review-queue.example.json`, `session.example.jsonl`, plus `INDEX.md` (68 topics, 12 tracks), `knowledge/systems-software/http-caching/{concept,validation}.md` (frontmatter, 21 claims, 10 items). Knowledge paths reference the committed repo, not `.journey/` (K5).

| UI element | Source |
|---|---|
| OP: `alex-dev` (header) | `profile.json.alias` |
| LED row / "2 DUE" | `review-queue.json.items[]` (due ≤ today count) |
| Clock | session start `session.started.ts` (mock ticker) |
| Due review table rows | `review-queue.json.items[]` → topic, due, interval_days, reviews, last_review |
| Mastery register 80 / meter | `skill-matrix.json.topics["systems-software/http-caching"].score` |
| Mastery 55 (garbage-collection) | `skill-matrix.json.topics["programming/garbage-collection"].score` |
| Bloom register 100/75 | `session.example.jsonl` `quiz.attempted.payload.bloom_scores` |
| Event stream rows | `logs/YYYY-MM-DD-*.jsonl` lines → type, ts, session_id, topic, payload |
| Heatmap counts | `INDEX.md` / `knowledge-graph.yml` (track × band counts; tints MOCK) |
| Explorer stats (68 / 5 pub / tier dist) | `INDEX.md` status + tier columns (computed) |
| Topic table rows | topic frontmatter → id, band, tier, bloom_target, status |
| Track meta | `tracks.yml` + spec §6.5 |
| Claim textarea (prefilled) | `session.example.jsonl` `claim.submitted.payload.claim` |
| Verdict badge PARTIAL / T2 / S-0009 / gaps | `claim.verdict.payload` → verdict, tier, record, note (verbatim) |
| Matched claims | `concept.md` claims tagged `[T2][S-0009]` (verbatim quotes) |
| Corrective path | `concept.md` frontmatter prerequisites/related + `knowledge-graph.yml` edges |
| Quiz items Q1–Q10 | `validation.md` item blocks → Q, bloom, bank, A, evidence, topic |
| Quiz feedback bodies | `validation.md` `A:` model answers |
| Review ladder | `review-queue.items[].interval_days` + spec §4.1 ladder |
| Review dialog manifest | `validation.md` review bank + prerequisite link note |
| Matrix table | `skill-matrix.json.topics[]` → level, score, validated, last_attempt, evidence |
| Calibration chart | `calibration.updated` events payload (derived; **MOCK** in this prototype — AC7 data doesn't exist yet) |
| Score history sparks | aggregate of `quiz.attempted` events (**MOCK**) |

---

## 7. Accessibility notes (dark-first pitfalls)

1. **Dark-first is not dark-only.** Light theme ships as first-class tokens; `prefers-color-scheme` respected when no explicit choice; manual toggle writes `data-theme` and persists for the session. Verified light-theme contrast in §2.2 — rgba tints fail on light, replaced with solid fills.
2. **Text contrast audited, not assumed.** All text tokens ≥4.5:1 (large ≥3:1) against every background they occur on (§2 tables). `--text-3` (3.6:1) is restricted to tick marks and disabled states; disabled controls are exempt from WCAG contrast but flagged in the token docs.
3. **Color is never the only channel.** LEDs pair with text; heatmap cells show counts; verdict cards show the word (CORRECT/PARTIAL/INCORRECT); tier chips carry the letter (T0–T4); sparklines sit beside numeric values.
4. **Semantic structure.** `nav/role=tablist` with `aria-selected`/`aria-controls`; arrow-key tab navigation; `main` with `section` per screen; tables with `th scope`; `<dialog>` native for modality; `aria-live="polite"` on verdict output and status lines; SVG charts expose `role="img"` + title/desc (and every chart has a data table or numeric readout nearby).
5. **Focus & density.** Visible `:focus-visible` (2px teal outline); dense tables remain keyboard-scrollable (no custom scroll containers that trap focus; heatmap/cal wrap in overflow containers with natural tab order).
6. **Motion.** `prefers-reduced-motion: reduce` kills all transitions/animations; the only animations are 150ms disclosure chevrons and the clock/quiz timer (content that must tick).
7. **Typography.** Body is proportional sans; mono is reserved for data. Uppercase micro-labels use generous letter-spacing. No text below 10px; no pure-CAPS sentences in body copy.
8. **Target sizes.** Chips/options ≥ 24px hit area with padding; tabs ≥ 36px; all controls are real `<button>`s.
9. **Dark-theme-specific glare/HRTF notes.** Avoid pure-black backgrounds (`#0A0E14` is near-black, not `#000`) to limit halation on OLED; accent-on-accent is never used for text; amber reserved for warnings/MOCK so it never reads as "active success".

---

## 8. Risks & tradeoffs

| Risk | Mitigation |
|---|---|
| **Density defeats readability** (instrument aesthetic can overload novices, persona Band B4/B3). | Progressive disclosure is literal: screen 1 shows aggregates, screen 2 the full inventory, screens 3–6 one flow each. `--fs-2` floor + generous row padding. |
| **Dark-first alienates daylight/office users.** | Full light theme, parity-tested contrast; toggle is one click in the header. |
| **Monospace/data-heavy look reads as "developer-only".** | Body copy stays sans; mono is a semantic (data ≠ prose), not a stylistic, choice. |
| **Color-coded tiers/status invite colorblind misreading.** | Text glyphs (T0–T4, DRAFT/PUBLISHED, CORRECT/PARTIAL/INCORRECT) always accompany color. |
| **Charts (calibration, sparks) are MOCK — risk of being mistaken for real measurements.** | Every MOCK element carries an explicit amber tag + footer provenance line; calibration chart is labeled MOCK in its panel title. |
| **Goodhart risk: telemetry becomes a score-chasing game** (numbers over learning; spec §4.1 calibration science). | No leaderboards, no fake rewards; calibration curve *shows* overconfidence instead of hiding it; streak is a plain counter, not a gamified combo. |
| **Stale real data** (examples reflect a fixed date; queue dates age). | All dates render from fields; a real build computes "due" relative to `today` from `review-queue.json`, never hardcodes. |
| **Data contract drift** (UI hardcodes field names → violates K6). | This prototype hardcodes only *for the demo*; the §6 mapping table is the contract a real build must render from — flags where the schema has no field yet (streak, calibration). |
| **Single-file scope** (this exploration cannot load `.journey/` from disk). | index.html simulates the read path; provenance tags make the boundary explicit so the app build can swap mock → real loaders without layout change. |
| **SVG charts without tables fail AT users.** | Each chart is paired with a numeric table/readout (matrix table, calibration stats registers). |

---

## 9. Report data

- Thesis: see §1.
- Palette: primary accent `--acc-teal #2DD4BF` (10.4:1 on bg-0), secondary `--acc-amber #F5A623` (9.5:1); backgrounds `#0A0E14/#0F151E/#131B26` (dark) and `#F4F6F8/#FAFBFC/#FFFFFF` (light); all text tokens ≥4.5:1.
- Screens: 6 (dashboard, explorer, validate, quiz, review, progress/calibration).
- Components: 26 (inventory §5).
- Files: `index.html` (104 KB, self-contained, no dependencies) + `brief.md` (this file).
