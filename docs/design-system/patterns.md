# Patterns

Cross-component behavior. Principles: `overview.md` P1–P5. Components: `components.md`. Tokens: `tokens.md` / `ui/design-system/tokens.css`.

---

## 1. Dashboard hierarchy — action dominant

The dashboard's job is to get the next review done, not to admire numbers. Hierarchy, top to bottom:

1. **The review CTA (elevation tier 1).** First element in the first row; ~40% width on desktop, full width on mobile; reads "START REVIEW · 2 due · closes 2026-08-19". Its glow (`--elev-1-glow`) is the only glow on the screen. Exactly one per screen (P1).
2. **Decision telemetry (elevation tier 2, second band).** Three registers that time the action: reviews due (count + next window), streak (plain counter + sparkline), calibration error (predicted − actual). Registers render as label-over-value readouts; the count that feeds the CTA is the same field the register shows — one source, two densities.
3. **Review load table (elevation tier 3, third band).** The due list the CTA launches.
4. **Skill heatmap (elevation tier 3).** Orientation data, not action data — always below the action band, always with its in-place legend (components.md §6).
5. **Event stream (bottom).** The raw trace behind everything above.

Rules: no card ever outranks the CTA in size, color, or glow; the CTA never scrolls out of the first viewport on desktop; supporting telemetry may justify a review but never replace the button; when nothing is due, the CTA yields to the next-best action and the empty state explains the source (components.md §11).

## 2. Progressive disclosure (K3 — context is scarce)

The harness protocol (spec §9.1: L0 overview → L1 maps → L2 topic pack → L3 deep artifacts) is the screen order:

| Level | Screen | Shows | Hides |
|---|---|---|---|
| L0 | Dashboard | aggregates: due action, registers, heatmap | raw fields |
| L1 | Topic Explorer | full inventory (tracks, bands, tiers, status) with filters | claim text |
| L2 | Validate / Quiz / Review | one flow at a time: claim → verdict → items | record internals |
| L3 | Progress & Calibration | matrix, calibration chart, score history, event stream | — |

Rules: a deeper level is always reachable from the level above in one click; filters and accordions (`<details>`) collapse the L1 inventory without removing data; tables truncate with "expand" rather than cramming; the event stream is the ceiling — nothing on screen hides information from the stream, the stream just reads last.

## 3. Interleaving display

Review sets are interleaved across the topic and its prerequisites (Rohrer & Taylor 2007; Dunlosky et al. 2013 — spec §4.1). The UI makes the mix visible:

- The review-session dialog opens with a **manifest table**: source topic, item id, bloom level, evidence — prerequisite items visibly mixed in (e.g., http-basics items inside an http-caching review).
- Queue rows expose a **ladder position** (interval 1–3–7–14–30–60–120d) and a "+prereq" chip when the set includes prerequisite items.
- The corrective path strip (components.md §3) uses two edge glyphs: `▶` = order-constrained prerequisite, `→` = related edge (spec §6.2 edge types). Edge labels are text, never color-only.

## 4. Calibration honesty

Metacognitive calibration (Flavell 1979) is the system's scientific core, so its UI pattern is **show the error, never the optimism**:

- The calibration chart plots predicted vs actual against the ideal `y=x` diagonal; overconfidence reads as a gap *above* the diagonal and is labeled in words ("+0.18 overconfident").
- The chart is always paired with its numeric table/registers — charts are decoration, numbers are data (P4).
- No smoothing, no best-fit gloss, no "achievement" framing; a shrinking error is the only celebration, and it is displayed, not announced.
- Where calibration data doesn't exist yet (AC7), the panel renders the empty state with its MOCK provenance tag — the pattern never fakes a reading (P2).

## 5. Keyboard & reduced-motion patterns

**Keyboard.**

- Tab bar: roving tabindex; Left/Right moves and activates; selected tab gets `aria-selected="true"`.
- Dialogs: native `<dialog>`; focus moves to the first control on open; ESC closes; focus returns to the trigger on close.
- Filter chips: `aria-pressed`; Space/Enter toggle; results live in the same page.
- Heatmap/table grids: cells are focusable in interactive mode with arrow-key movement; overflow containers keep natural tab order (no scroll traps).
- Focus visibility: `--focus-ring` on surfaces, `--focus-ring-inverse` on accent-filled controls (WCAG 2.4.7); `:focus-visible` only — no focus decoration on mouse clicks alone; inputs get `--border-accent` + ring on focus.
- Order: header LEDs (status, skip-announced where decorative) → CTA → telemetry → tables; the CTA is the second tab stop on the dashboard (after the theme toggle/skip link).

**Reduced motion** (`prefers-reduced-motion: reduce`):

- All transitions and animations collapse to instant; `--motion-fast/-base` become 0.
- Exemptions (content that must tick): the session clock, the quiz timer, live status text. These remain time-based but never animate layout.
- LED glow is static (no pulse states are defined in the system — there are no animated LEDs at all).
- `scroll-behavior: auto`; disclosure chevrons rotate instantly.

**Other a11y constants.** Target sizes: buttons ≥ 40px tall, chips ≥ 24px hit area, tabs ≥ 36px. Captions never below 12px (tokens.md type floor). Color never sole channel (P4). `aria-live="polite"` on verdict output, review status, and empty-state transitions; `role="status"` on transient states.
