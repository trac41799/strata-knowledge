# Atelier — Design Direction Brief

**Exploration:** 01 · L1 UI/UX agent · 2026-08-18 · repo: `ui/explorations/atelier/`

---

## Thesis

**Learning is a scholarly practice, so the journey interface should feel like a
beautifully kept annotated notebook — serif display type, warm paper, ink-toned
text, and fountain-pen-blue marginalia — where every claim carries its evidence
in the margin.** Strata is not an app that tracks you; it is a desk, an index, a
review shelf, and a ledger. The UI earns trust by looking as honest as the data
is: provenance printed beside every figure, simulated values stamped `MOCK`,
tiers drawn as ink marks rather than status lights.

---

## Palette

All tokens are CSS custom properties in `:root`; the dark variant lives under
`[data-theme="dark"]` and `@media (prefers-color-scheme: dark)` (targeting
`:root:not([data-theme="light"])`), with an in-page manual toggle that persists
to `localStorage` (local-only, no telemetry — K5).

Contrast ratios are computed per WCAG 2.2 relative luminance (hand-computed to
±0.2). All **text** pairs ≥ 4.5:1 (large ≥ 3:1); non-text UI components use
`--pen` vs `--paper` ≥ 3:1; hairline rules are decorative.

| Token | Light hex | Usage | Background | Ratio | Dark hex | Dark ratio |
|---|---|---|---|---|---|---|
| `--paper` | `#F5F0E6` | page / card background | — | — | `#1B1812` | — |
| `--paper-2` | `#EDE6D6` | leaf-card fill, input fill | — | — | `#211D15` | — |
| `--paper-3` | `#E2D9C4` | chip fill, pressed chip | — | — | `#2B2619` | — |
| `--ink` | `#2A2722` | primary text, buttons, rules | paper | **13.1:1** | `#E9E2D2` | 13.7:1 |
| `--ink-soft` | `#57534A` | secondary text, captions, labels | paper | **6.7:1** | `#A8A194` | 6.9:1 |
| `--ink-faint` | `#8A8578` | tertiary marks (decorative / large only) | paper | 3.2:1 ⚠ | `#7A746A` | 3.8:1 ⚠ |
| `--pen` | `#23486B` | accent: links, marginalia, tabs, focus | paper | **8.4:1** | `#8FB0D8` | 7.9:1 |
| `--pen-soft` | `#4A6C92` | selection, hover fills | paper | 4.6:1 | `#A9C4E4` | 5.4:1 |
| `--ok` (correct) | `#3A6B47` | verdict stamps, "due soon" | paper | **5.5:1** | `#7FB493` | 7.5:1 |
| `--ok-bg` | `#E4EDE2` | correct stamp fill | — | (ok on it: 5.2:1) | `#26352B` | — |
| `--warn` (partial) | `#8A5300` | partial verdict, warnings | paper | **5.6:1** | `#D9A441` | 7.9:1 |
| `--warn-bg` | `#F3E8D5` | partial stamp fill | — | (warn on it: 5.2:1) | `#362D1B` | — |
| `--bad` (incorrect) | `#9B3B2F` | incorrect verdict, overdue | paper | **6.0:1** | `#D98A7E` | 6.7:1 |
| `--bad-bg` | `#F2E3DE` | incorrect stamp fill | — | (bad on it: 5.5:1) | `#3A2723` | — |
| `--t4` (frontier) | `#6B3E80` | T4 chips / violet warning mark | paper | **7.0:1** | `#C39BD8` | 7.6:1 |
| `--rule` | `#D8CFBC` | hairlines, table rules | paper | ~1.5:1 (decorative) | `#3A362C` | decorative |
| `--rule-strong` | `#B8AE96` | tab underline, button borders | paper | ~1.9:1 (never sole affordance) | `#58523F` | non-text only |
| `--heat-1…5` | ink rgba .06→.58 | heatmap washes | paper-2 | n/a (graphic) | ink-light rgba | n/a |

> ⚠ `--ink-faint` is reserved for footnotes/meta text at small sizes where it
> risks falling below 4.5:1 — in practice it is used for non-essential marks
> (page numbers, decorative rules). Where faint text must be read (source file
> paths), the mono variant inherits `--ink-soft` instead.

---

## Type scale

System stacks only: serif display (`Iowan Old Style / Palatino Linotype /
Book Antiqua / Georgia`), serif body (`Georgia / Times New Roman`), mono data
(`ui-monospace / Cascadia Mono / SF Mono / Menlo / Consolas`). Mono is reserved
for *ledger* content — ids, dates, scores, evidence records — so the eye reads
"data" at a glance.

| Step | Size | Role |
|---|---|---|
| display | clamp(2.1–3.0rem) | brand title — the notebook cover |
| h1 | clamp(1.6–2.15rem) | folio titles (one per screen) |
| h2 | clamp(1.2–1.5rem) | card titles |
| h3 | 1.05rem | sub-headings, item titles |
| body | 1.0rem / 1.62 | running text |
| small | .875rem | leaf-sub descriptions |
| caption | .78rem | labels, chips, captions |
| mono | .85rem | ledger data |
| mono caption | .72–.78rem | tab numerals, badges |

Ratio ≈ 1.25 (major third) through h3→h1; the display jump is intentional
(brand presence, not hierarchy).

---

## Pattern language

1. **Folio header** — every screen opens with a ruled header: Roman numeral in
   pen blue, serif title, mono rule line ("folio 04 of 06 · L1 maps"). The
   document is a book; screens are pages.
2. **Bookmark tab bar** — in-page navigation as cloth bookmarks with a pen-blue
   top edge for the active folio. ARIA tabs with roving tabindex.
3. **Marginalia** — right-hand margin notes in fountain-pen blue: provenance,
   protocol references (`K3`, `K5`), depth markers. Collapses to bordered
   callouts on narrow viewports. This is the signature move: *the UI explains
   itself in the margin, like an annotated edition*.
4. **Leaf cards** — paper-2 cards with a double-rule top border (stationery
   grammar), hairline sides, soft paper shadow.
5. **Ink stamp** — the verdict rendered as a rubber stamp: double border,
   slight rotation, serif caps. Correct = forest green, partial = ochre,
   incorrect = brick. Colour is never the only signal (the word is printed).
6. **Ledger typography** — all scores, dates, intervals, record ids in mono:
   the interface reads like a bookkeeper's journal.
7. **Field-notes heat grid** — practice activity as ink washes (dense page =
   well-kept notebook), never traffic-light colours. Seeded pseudo-random data.
8. **Footnote apparatus** — evidence records rendered as small bordered
   `S-####` chips; every verdict and every quiz answer cites its records,
   echoing the repo's citation honesty.
9. **MOCK badge** — dashed-border tag on anything simulated. Honesty is part
   of the aesthetic: the interface visibly refuses to invent data.
10. **Graph-paper chart** — calibration plot drawn in SVG with hairline axes,
    dashed "pencil" prediction and solid pen actual line.

---

## Component inventory (31) → screens

| # | Component | Screens |
|---|---|---|
| 1 | Skip link | all |
| 2 | Masthead / brand | all |
| 3 | Theme toggle (manual + system) | all |
| 4 | Bookmark tab bar | all |
| 5 | Folio header (numeral + rule line) | all |
| 6 | Stat tile | 1 Desk |
| 7 | Leaf card | all |
| 8 | Shelf row (due item) | 1, 5 |
| 9 | Field-notes heat grid | 1 |
| 10 | Heat legend | 1 |
| 11 | Marginal note | all |
| 12 | MOCK badge | 1, 3, 4, 5, 6 |
| 13 | Status badge (bad/ok/warn/ghost/mono) | 1, 3, 4, 5, 6 |
| 14 | Tier chip (T0–T4) | 2, 3, 4, 6 |
| 15 | Band mark (B1–B6) | 2 |
| 16 | Status glyph (published/validated/draft) | 2 |
| 17 | Chapter list (`<details>`) | 2 |
| 18 | Topic row | 2 |
| 19 | Legend row | 2 |
| 20 | Claim textarea + sample chips | 3 |
| 21 | Verdict stamp | 3 |
| 22 | Evidence record chip | 3, 6 |
| 23 | Corrective path (ordered steps) | 3 |
| 24 | Session ledger | 4 |
| 25 | Quiz item card + self-grade buttons | 4 |
| 26 | Model answer block | 4 |
| 27 | Feedback dialog (`<dialog>`) | 4 |
| 28 | Spacing ladder (rungs 1…120) | 5 |
| 29 | Due flag (overdue/soon) | 1, 5 |
| 30 | Matrix table | 6 |
| 31 | Calibration chart (SVG) + legend | 6 |
| — | Event log table (bonus, real data) | 6 |

---

## Data mapping — every UI element ← committed field

*Real = present in the shipped examples; the "real" tag is printed in the UI.*

| UI element | Source |
|---|---|
| Folio date, "today" (2026-08-18) | demo reference date (matches env date) |
| Reviews-due stat (2), overdue count (1) | `review-queue.example.json` items where `due` ≤ today |
| Validated-topics stat (1 of 2) | `skill-matrix.example.json` `topics.*.validated` |
| Index stat (68 topics, 12 tracks, 5 published) | `knowledge-graph.yml` `topic-count`; `INDEX.md` |
| Streak (12 d) | **MOCK** (no committed field) |
| Heatmap cells | **MOCK** (future: derived from `logs/*.jsonl` activity) |
| Shelf rows: title/id/due/interval/reviews/last_review | `review-queue.example.json` per item |
| Chapter = track (title, count, published) | `INDEX.md` track sections; `tracks.yml` |
| Topic row: title/id/band/tier/bloom/status | topic frontmatter `id, title, band, tier, bloom_target, status` |
| "Mastered" green marker | `skill-matrix.example.json` `topics.<id>.level` |
| Wave count (8) in marginal | `knowledge-graph.yml` `wave-count` |
| Tier legend text | spec §6.3 tier table |
| Claim textarea default (Sample A) | `session.example.jsonl` `claim.submitted` payload.claim |
| Verdict stamp + label | `claim.verdict` payload.verdict (correct\|partial\|incorrect) |
| Verdict tier | payload.tier |
| Record chip `S-0009` / `S-0023` | payload.record → `evidence/records/S-####.md` |
| Verdict note | payload.note (verbatim for Sample A) |
| Corrective path steps | protocol (AGENTS.md §2); references `concept.md` sections + `validation.md` items + `review-queue` |
| Sample B / C | **MOCK**, built from `concept.md` §Boundaries / §Vary claims |
| Session ledger (session id, started, objective) | `session.example.jsonl` + `session.schema.json` |
| Topic/bank/tier/bloom-target line | `validation.md` frontmatter + `concept.md` frontmatter |
| Quiz items (Q1, Q3): question, bank, bloom, model answer, evidence | `validation.md` item anatomy (Q/A/bank/bloom/evidence) |
| Item 2 distractors | **demo-constructed** from `concept.md` claims (file has no distractors) |
| Self-grade → `quiz.attempted` | event schema (UI only simulates the emission) |
| Ladder 1/3/7/14/30/60/120 | spec §4.1 spacing schedule |
| Matrix table rows | `skill-matrix.example.json` `topics.<id>` (level, score, validated, last_attempt, evidence) |
| Extended matrix rows | **MOCK** |
| Calibration chart + MAE | **MOCK** data; contract = `calibration.updated` payload (predicted vs actual) |
| Event log table (6 rows) | `session.example.jsonl` lines (type, ts, payload) |

---

## Accessibility

- Semantic landmarks throughout: `header`, `nav` (tablist), `main`, `section`
  (tabpanel), `footer`; one `h1` per page; headings nested h2→h3.
- **Tabs**: proper `role=tablist/tab/tabpanel`, `aria-selected`,
  `aria-controls`, roving tabindex, Arrow/Home/End key navigation; panel
  heading receives focus on switch.
- **Dialog**: native `<dialog>` with `aria-labelledby`/`aria-describedby`,
  backdrop, Esc and explicit close; focus returns naturally.
- **Live region**: verdict zone is `aria-live="polite"`.
- **Contrast**: every text pair ≥ 4.5:1 (≥ 3:1 large); the only sub-3:1
  elements are decorative hairlines — interactive boundaries always carry text
  or fill. Color is never the sole signal (tiers print `T0`…`T4`; verdicts
  print words).
- **Theming**: system `prefers-color-scheme` honored; manual override; choice
  stored locally only.
- **Reduced motion**: all transitions disabled, stamp rotation removed.
- **Graphics**: heatmap and chart expose descriptive `aria-label`/`role=img`
  summaries; decorative glyphs are `aria-hidden`.
- **Print stylesheet**: tabs/tools hidden, every folio prints on its own page.
- **No keyboard traps**; all controls are native buttons.

## Risks / tradeoffs

1. **Serif + tiny mono captions on low-DPI screens** — Georgia/Palatino render
   wide; 0.72rem mono is tight. Mitigation: conservative stacks, ≥4.5:1 ink,
   generous line spacing; flagging as the top readability risk for Windows
   laptops. Consider bumping caption step to 0.8rem in the app build.
2. **Marginalia collapse** — the "read the margin" habit only exists on wide
   layouts; on narrow screens notes become callouts and reading order changes.
   Acceptable; must be tested in real use.
3. **Static demo ceiling** — verdicts for free text are out of scope (the
   harness does that); the UI clearly says so. Production would read
   `.journey/` directly and render live events.
4. **`MOCK` badges everywhere** may read as "unfinished" rather than
   "honest" to some viewers — a deliberate trade; the alternative (silent
   simulation) violates K5/K6 honesty.
5. **`dialog.showModal`** needs a modern browser (Safari < 15.4 lacks it);
   exploration-level risk, note for the implementation phase.
6. **Hairline rules < 3:1** — decorative; if auditors require 3:1 for all
   lines, darken `--rule-strong` and lose some delicacy.
7. **Print colour** — stamps/badges are flattened to black-on-white in print;
   fine for a notebook aesthetic, loses verdict colour cues.
8. **The aesthetic is opinionated** — "quiet trust" can read as "boring
   spreadsheet" to users expecting dashboard chrome; that is the point of the
   direction, but it will be polarizing in review.

## Files

- `index.html` — 80 KB, single self-contained file, vanilla HTML+CSS+JS, zero
  external dependencies, works from `file://` (all data inlined).
- `brief.md` — this document.
- Open `index.html` directly in any modern browser; no server required.
