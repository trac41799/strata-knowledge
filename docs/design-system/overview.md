# Strata Journey Interface — Design System Overview

**Status:** Adopted core (hybrid direction) · **Date:** 2026-08-18 · **Source lineage:** `ui/explorations/instrument/` (base) + Arcade (action-first dashboard CTA) + Atelier (type-scale discipline)
**Files:** `ui/design-system/tokens.css` (canonical tokens) · `docs/design-system/{tokens,components,patterns}.md`

This is the design system for **Layer 5 — Journey Interface** (ADR-0001): a local-first consumer UI that renders journey + knowledge data, writes only `.journey/` via the event schema, and never mutates canonical knowledge. The system is code-first: **tokens are CSS custom properties in `ui/design-system/tokens.css`; these docs describe and document them, never redefine them.**

---

## 1. Design principles

### P1 — Action-first
The next review action dominates every screen where a review is due. The dashboard's first, largest, highest-elevation element is the review CTA (elevation tier 1, `--elev-1-*`), not the stats. Supporting telemetry (due counts, streaks, heatmaps) exists to justify and time the action, never to outrank it. Arcade lineage.

### P2 — Provenance honesty
Every data element declares where it came from: `REAL` (schema-validated journey/knowledge data) or `MOCK` (illustrative). Tags are a core honesty pattern, applied once per panel (header), never per-row. An instrument that lies about its readings is worse than no instrument. Instrument lineage.

### P3 — Progressive disclosure (K3)
Overview → maps → topic → deep artifacts, mirroring the harness protocol (spec §9.1). The dashboard shows aggregates; deeper screens reveal the graph, the verdict logic, and the raw event stream. Never dump the repo into view.

### P4 — Data-then-decor
Every decorative instrument element (tick bars, LEDs, gridlines, registration marks) is subordinate to and redundant with a data channel: LEDs carry text labels, heatmap cells carry counts, charts carry numeric tables. If the decoration is removed, no information is lost.

### P5 — Telemetry metaphor, not gamification
The UI reads like test equipment: calibration curves show overconfidence instead of hiding it; no leaderboards, no streaks-as-reward (a streak is a plain counter). Deliberate-practice honesty (spec §4.1, metacognitive calibration) over score-chasing.

---

## 2. Consuming the tokens

1. **Import once, in order:** `@import url("ui/design-system/tokens.css");` (or copy into the app build). Never redefine a token value in component CSS.
2. **Theming:** dark is the default (`:root`). Light applies automatically under `prefers-color-scheme: light` when no explicit choice is set, or via `<html data-theme="light">` / `<html data-theme="dark">` for the in-page toggle. Toggle script (session-persisted):

   ```js
   const root = document.documentElement;
   function effectiveTheme() {
     if (root.getAttribute("data-theme")) return root.getAttribute("data-theme");
     return matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
   }
   toggleBtn.addEventListener("click", () => {
     root.setAttribute("data-theme", effectiveTheme() === "dark" ? "light" : "dark");
   });
   ```

3. **Rules of use:**
   - Text: `--text` (primary), `--text-soft` (secondary), `--text-faint` (disabled/decorative only — never body copy).
   - Accent: `--accent` for interactive/active states; `--amber` for warnings and MOCK; `--ok`/`--bad`/`--info`/`--frontier` for semantic status; `--tier-0..4` for evidence tiers.
   - Fills for tags/chips: pair `--tint-*` background with `--chip-*` text (the `--chip-*` values are the theme-corrected text-on-tint colors — contrast-verified in tokens.md).
   - Elevation: tier 1 = exactly one prominent CTA per screen; tier 2 = ordinary cards/panels; tier 3 = nested/sunken surfaces (tables inside panels, log streams).
   - Borders: `--border` default, `--border-strong` emphasis, `--border-accent/-ok/-warn/-bad` for state-bearing outlines (verdict left rails).
   - Focus: always `--focus-ring` on dark/surface contexts, `--focus-ring-inverse` on accent-filled controls (WCAG 2.4.7 — see patterns.md).
   - Type: base is `--text-base` (14px). The floor is `--text-caption` (12px). **Nothing renders below 12px** (Atelier discipline; the old 10–11px micro steps are retired).
4. **No hardcoded colors** in components — every hex lives in `tokens.css`. Schema field names are likewise never hardcoded into markup; they render from the journey schemas (K6).

---

## 3. Relation to journey schemas (K6 — convention-as-code)

Tokens describe *presentation*; schemas are the *data contract*. The mapping table below is the canonical bridge; per-component mappings live in `components.md`.

| Data domain | Schema / source | Rendered via |
|---|---|---|
| Learner identity | `.journey/profile.json` → `alias`, `levels` | Shell header (OP register) |
| Proficiency | `.journey/state/skill-matrix.json` → `topics.{id}.{level,score,validated,last_attempt,evidence}` | Skill matrix table, registers, heatmap tints |
| Spaced review | `.journey/state/review-queue.json` → `items[].{topic,due,interval_days,reviews,last_review}` | Review CTA (count + next due), queue rows, ladder |
| Events | `.journey/logs/YYYY-MM-DD-*.jsonl` → `{type,ts,session_id,topic,payload}` | Event stream, verdict history, score history |
| Claim verdicts | `claim.submitted` / `claim.verdict` payloads → `{claim, verdict, tier, record, note}` | Verdict card |
| Quiz items | `knowledge/<track>/<topic>/validation.md` → item blocks `{Q, bloom, bank, A, evidence, topic}` | Quiz item card, feedback, review manifest |
| Topics | topic frontmatter → `{id, band, tier, bloom_target, status, prerequisites, related}` + `INDEX.md` | Explorer tables, corrective path, heatmap axes |
| Calibration | `calibration.updated` payloads (derived aggregate) | Calibration chart (MOCK until AC7 data exists) |

**Provenance rule:** any element whose data is not yet available from these sources renders with the MOCK provenance tag and a placeholder shape — it never renders as real (P2).

---

## 4. The hybrid mandate — four fixes baked in

These four are load-bearing; every component below assumes them:

1. **Action-first dashboard** — review CTA at elevation tier 1, first element, full width on mobile (components.md §2, patterns.md §1).
2. **Readable type** — base 14px, caption floor 12px, no sub-12px text anywhere (tokens.css type block).
3. **In-place heatmap legend** — the heatmap owns its legend inside its panel (components.md §6).
4. **Toned-down provenance** — REAL/MOCK tags remain mandatory but appear once per panel header, not per row (components.md §8, patterns.md §2).
