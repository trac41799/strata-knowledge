# Components

Inventory of the Strata Journey Interface design system. Every component: anatomy → states → usage → a11y → data source. Tokens referenced from `ui/design-system/tokens.css`; principles from `overview.md`; cross-cutting behavior from `patterns.md`.

---

## 1. Shell & navigation

**Anatomy.** Faceplate header (brand `STRATA//INSTRUMENT`, OP register ← `profile.json.alias`, LED row, session clock, theme toggle) · tick-bar rule · tab bar (`role="tablist"`: Dashboard, Topic Explorer, Validate, Quiz, Review Queue, Progress & Calibration) · `main` with one `<section role="tabpanel">` per screen · footer (provenance policy).

**States.** Tab: default / hover (`--text` ) / selected (`--accent` text + 2px accent top rule + `--bg` fill) / focus (`--focus-ring`). Theme toggle: shows current effective theme; click writes `data-theme` on `<html>`.

**Usage.** Exactly one tab bar; sticky top (`--z-sticky`). Tab order matches progressive disclosure (P3): overview → maps → flows → deep artifacts.

**A11y.** Arrow-key navigation (Left/Right), `aria-selected` + `aria-controls`, `tabindex` management (roving tabindex), screen sections are focusable panels. Header LEDs are `role="status"` with text labels.

**Data source.** `profile.json.alias` · `review-queue.json.items[]` (due-count LED) · `session.started.ts` (clock) · session-settings (theme, in `preferences`).

---

## 2. Action-first review CTA (elevation tier 1)

**Anatomy.** Single dominant control: label ("START REVIEW"), count ("2 due"), next-due window ("closes 2026-08-19"), spacer arrow. Elevation tier 1: `--elev-1-bg`, `--elev-1-text`, `--elev-1-border`, `--elev-1-glow`, radius `--radius-md`. Full-width on mobile; ~40% of the dashboard's first row on desktop (patterns.md §1).

**States.** Default (elev-1) · hover (`--elev-1-bg-hover`) · focus (`--focus-ring-inverse`, because the ring sits on an accent fill) · pressed (`translateY(1px)`, `--motion-fast`) · disabled (no due items; renders as `--text-faint` outline — never as a dimmed green, and paired with an empty-state panel, §11).

**Usage.** Exactly **one** per screen (P1). Where no review is due, the CTA yields to the next-best action (validate a claim) with the same elevation. Amber is reserved for the *due-soon* warning on the label's count, not the button itself.

**A11y.** 44px min height; the count is not announced twice (label + `aria-label`); opens the review dialog (native `<dialog>`) which receives focus on open and returns it on close.

**Data source.** `review-queue.json.items[]` → count of `due <= today` · earliest `due` + its `interval_days` · `validation.md` review-bank items (manifest, dialog).

---

## 3. Verdict card

**Anatomy.** Left rail (`--border-warn`/`-ok`/`-bad` by verdict) · badge (PARTIAL/CORRECT/INCORRECT, `--tint-amber`/`-ok`/`-bad` + `--chip-*` text) · tier tag (`--tier-*` axis) · evidence tags (`S-####`, provenance-tagged) · claim quote (mono) · matched claims list with per-claim `[T*]` tags · gaps list · corrected mental model block · corrective path strip (patterns §3).

**States.** Hidden (empty state) → loading (status line, `--motion-base`) → shown. Verdict badge color + word always together (P4).

**Usage.** Output of the Validate flow. Reads, never mutates, knowledge (ADR-0001): the card is a rendering of the agent's `claim.verdict` event.

**A11y.** `aria-live="polite"` region; the verdict word is announced before the evidence; corrective path is a list, not a decorative chain.

**Data source.** `claim.submitted.payload.claim` · `claim.verdict.payload.{verdict, tier, record, note}` · `concept.md` claims (matched, verbatim, with `[T*][S-####]` tags) · `concept.md` frontmatter `prerequisites`/`related` (path nodes).

---

## 4. Quiz item + feedback dialog

**Anatomy (item).** Meta row (bank tag, bloom tag, evidence tag) · question text (`--text-lead`) · option list (mono key `[A]…`, sans stem) · immediate feedback panel (LED + title + model-answer explanation) · navigation (PREV / NEXT / RESET) · session telemetry rail (bank selector, item position, elapsed, score register with meter).

**States (option).** Default → hover (`--border-accent`) → chosen-correct (`--tint-ok` fill + `--border-ok`) → chosen-wrong (`--tint-bad` fill + `--border-bad`) → locked (all disabled). Free-response items reveal a model answer then self-grade (GOT IT / MISSED), preserving the score register.

**States (feedback dialog).** Opens as a native `<dialog>` when an item is answered: header (verdict + LED), body (explanation from the model answer, evidence tags), footer (CONTINUE). Dismissable with ESC; focus moves to CONTINUE.

**Usage.** Banks match `validation.md`: formative (practice, immediate feedback), summative (mastery, ≥80% rule), review (interleaved, spaced). Feedback is immediate (Ericsson, deliberate practice; spec §4.1).

**A11y.** Options are real buttons; feedback is announced via `aria-live`; dialog focus management per patterns §5; timer is exempt from reduced-motion (content that must tick).

**Data source.** `validation.md` item blocks → `Q`, `bloom`, `bank`, `A` (feedback body), `evidence`, `topic` · `quiz.attempted.payload.{score, bloom_scores}` (telemetry rail).

---

## 5. Review queue row

**Anatomy.** Table row: topic id (mono) · due date (tabular) · interval · review count · last review · provenance tag (panel-level, §8). Extended row (details): ladder position marker, prerequisite mix chips.

**States.** Due-soon (amber count, `--led-warn`) · overdue (bad text, `--led-bad`) · upcoming (neutral) · hover (row tint) · focus (row-level `--focus-ring` — rows are selectable).

**Usage.** Rows render inside the Review Queue screen table and the dashboard's due-load panel; both read the same `review-queue.json` — one source, two densities (P3).

**A11y.** `th scope="col"` headers; numeric columns `--font-nums`; row selection announced; ladder visualization has an adjacent textual list for AT.

**Data source.** `review-queue.json.items[]` → `topic, due, interval_days, reviews, last_review` · due-soon/overdue derived from `due` vs today · ladder rung from `interval_days` (spec §4.1 cadence).

---

## 6. Skill heatmap (with point-of-use legend)

**Anatomy.** Panel with header (title + provenance tag) · **legend row directly inside the panel, above the grid** (mandated fix #3): "count = topics · tint = mastery · amber = validated" with swatches for `--heat-2`, `--heat-4`, `--heat-5`, `--heat-validated`, and the count-only cell (`--heat-1`) · grid: rows = tracks, columns = bands B5–B1; cell = topic count (text), fill = `--heat-1..5`; validated cells = `--heat-validated` · caption (bottom) restating the legend in words.

**States.** Cell hover (outline `--focus-ring`-adjacent 1px `--accent`), cell focus (cells are keyboard-navigable when grid has interactive mode), overflow container scrolls horizontally without trapping focus.

**Usage.** Dashboard (aggregate) and Topic Explorer (drill target). The legend is **in place** — never a distant color key (mandated fix #3). Tints encode mastery (MOCK until matrix coverage grows); counts are always visible, so color is redundant (P4).

**A11y.** Real `<table>` with `th scope`; legend is a `<caption>`-adjacent visible block AND announced text; dark `--heat-5` cells switch text to `--heat-text-strong` (tokens.md §7 — component rule, not optional); aria-label per cell includes count + track + band.

**Data source.** `INDEX.md` / `knowledge-graph.yml` (counts per track × band) · `skill-matrix.json.topics[].{score,validated}` (tint + validated marker) · frontmatter `band`, `track`.

---

## 7. Calibration chart

**Anatomy.** SVG line chart: dashed gridlines, tick labels (12px floor), ideal diagonal `y=x` (`--text-faint` dashed), predicted line (`--accent`), actual line (`--amber`), per-point dots, legend inside the chart, title + `<desc>`. Always accompanied by a numeric table or register trio (mean error / direction / trend) — data-then-decor (P4).

**States.** Static (read-only) · hover on point (tooltip with session index + pred/actual pair, `--z-tooltip`) · focus (points are focusable when interactive).

**Usage.** Progress screen. Calibration honesty (P5): overconfidence is *shown*, never smoothed away; the chart renders whatever `calibration.updated` aggregates say.

**A11y.** `role="img"` + `<title>`/`<desc>`; the paired numeric table is the authoritative AT channel; tick labels ≥12px (no SVG text below the floor).

**Data source.** `calibration.updated` payloads (predicted vs actual per session; derived aggregate) — **currently MOCK** until AC7 data exists; the panel then carries the MOCK provenance tag.

---

## 8. Provenance tags (REAL / MOCK)

**Anatomy.** 12px mono chip: `REAL` (green: `--prov-real-bg`/`--prov-real-fg`) or `MOCK` (amber: `--prov-mock-bg`/`--prov-mock-fg`), optionally with a source path (`REAL · review-queue.example.json`). Placed in the **panel header**, right-aligned.

**States.** Static; tooltip (`title`) may expand the source path.

**Usage.** Core honesty pattern (P2) — mandatory for every panel whose data is not real schema data. **Toning-down rule (mandated fix #4):** exactly one tag per panel header; rows inside inherit panel provenance and carry no per-row tags. Per-row tags return only when a single row within a mixed panel differs (e.g., one MOCK row among REAL rows — tag the row, not the panel).

**A11y.** Tag text is the full word (`REAL`, `MOCK`) — color is never the only channel; chips are plain text, not buttons.

**Data source.** Provenance is metadata, not journey data: it records whether the renderer's input came from `.journey/`/knowledge files (REAL) or a bundled mock (MOCK).

---

## 9. Status LEDs

**Anatomy.** 8px dot (`--led-size`), fill `--led-on/-warn/-bad/-idle/-off`, glow `--led-*-glow`; always paired with a text label in `--text-soft` (12–13px).

**States.** on / warn / bad / idle / off (off = `--led-off`, no glow).

**Usage.** System status row (JRNY LOCAL, AGENT LINK, reviews due), verdict badges, matrix `validated` column, quiz feedback.

**A11y.** Decorative element (`aria-hidden`); the label carries the meaning; never the sole indicator (P4).

**Data source.** Label semantics only; no direct schema field (the LED reflects computed states such as `due <= today`).

---

## 10. Data tables

**Anatomy.** Sticky header row (`--surface-2` fill, mono uppercase 12px captions, `--text-soft`) · hairline row separators (`--line`) · hover tint (`--surface-hover`) · tabular numerals (`--font-nums`) on all numeric columns · provenance tag in the panel header (§8).

**States.** Default / hover / focus(row) / empty (§11) / filtered (row visibility toggled by chips, `aria-pressed`).

**Usage.** The workhorse of the dense screens (explorer inventory, verdict history, review queue, skill matrix). Sortable columns and filter chips use `aria-sort`/`aria-pressed`.

**A11y.** `th scope="col"`; captions summarize; no custom scroll traps; every numeric column keeps its text value (no icon-only cells).

**Data source.** Per-table: `review-queue.json.items[]` · `skill-matrix.json.topics[]` · `INDEX.md`/frontmatter (`id, band, tier, bloom_target, status`) · `claim.verdict` history · `calibration.updated` (table form).

---

## 11. Empty states

**Anatomy.** Panel-level: LED-off dot + 12px caption title + one-line `--text-soft` explanation + optional action (secondary). No placeholder art; the panel keeps its provenance tag so the *absence* is also honest (e.g., "no calibration data yet — generated after your first review session").

**States.** Static; action button (secondary, `--elev-2`) when a next step exists.

**Usage.** First-run, no-due-items, empty history, MOCK-not-yet-available aggregates. Empty states are first-class (the CTA's disabled state links here).

**A11y.** `role="status"` where the state is transient; the action remains keyboard-reachable.

**Data source.** Any schema whose collections are empty (`review-queue.items[]`, logs, `calibration.updated`); the empty message names the exact missing source.
