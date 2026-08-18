# ARCADE — Design Direction Brief

**Exploration:** `ui/explorations/arcade/`
**Repo:** Strata (journey interface, ADR-0001)
**Date:** 2026-08-18 · **Author:** L1 UI/UX agent (design exploration)
**Status:** Exploration — nothing here is production. Touch only this folder.

---

## 1. Thesis

> Learning is a game worth playing daily. ARCADE makes progress, streaks, and
> mastery visibly rewarding — not by decorating a dashboard, but by re-casting the
> entire journey layer as a small, tasteful arcade: Strata City (the knowledge
> graph as a skyline), Coin Runs (retrieval practice), the Quest Board (spaced
> review), the Verification Arcade (claims → verdicts), and the Scoreboard
> (calibration).
>
> Playful ≠ childish: the energy comes from bold rounded sticker-cards, coin-yellow
> CTAs, hard offset shadows, duotone track identities, big display numerals, and
> celebration micro-interactions — all on disciplined typography, WCAG AA contrast,
> and `prefers-reduced-motion` respect. The game never lies: XP rewards
> *participation*; mastery rings, skill scores, and calibration charts show
> *learning* — the two are visually and semantically distinct.

**Design contract carried from the spec/ADR:** local-first consumer of `.journey/`
+ committed maps (K5); progressive disclosure overview → map → topic → artifact
(K3); design system as code (CSS custom properties, K6); never mutates knowledge.

---

## 2. Palette & Contrast (WCAG 2.1 AA)

Rule of the system: **vivid fills always carry dark ink text (`--on-fill`); white
text appears only on dark neutrals and slate.** This is what lets the palette stay
vibrant without contrast failures. Ratios below computed with the WCAG relative
luminance formula (all text pairings listed; every used pairing is ≥4.5:1 for
normal text).

### 2.1 Neutrals & semantic accents

| Token (light) | Hex | Usage | Text on it | Contrast | |
|---|---|---|---|---|---|
| `--bg` | `#F6F3EC` | page background (cream) | `--ink` `#191623` | 16.05:1 | AA |
| `--surface` | `#FFFFFF` | sticker cards | `--ink` | 17.79:1 | AA |
| `--surface-2` | `#EFE9DD` | inset panels, wells | `--ink` | 14.72:1 | AA |
| `--ink` | `#191623` | primary text | — | — | — |
| `--ink-soft` | `#57536B` | muted text, captions | bg/surface/surface-2 | 6.64 / 7.36 / 6.08 | AA |
| `--sky-deep` | `#2563EB` | links | `--surface` | 5.17:1 | AA |
| `--coin` | `#FFB703` | primary CTA, XP, coins | `--on-fill` `#17131F` | 10.46:1 | AA |
| `--mint` | `#2EC4B6` | correct, validated, mastery | `--on-fill` | 8.43:1 | AA |
| `--coral` | `#FF5C39` | streak flame, energy, hot | `--on-fill` | 5.95:1 | AA |
| `--violet` | `#7C6FF0` | rings, focus, calm mastery | `--on-fill` | 4.69:1 | AA |
| `--rose` | `#EC4899` | partial, highlights | `--on-fill` | 5.18:1 | AA |
| `--red` | `#EF4444` | incorrect, overdue | `--on-fill` | 4.86:1 | AA |
| `--sky` | `#3A86FF` | info fills | `--on-fill` | 5.25:1 | AA |
| `--amber` | `#F59E0B` | mid-progress, "due soon" | `--on-fill` | 8.51:1 | AA |
| `--teal` | `#14B8A6` | tier T2 chip | `--on-fill` | 7.34:1 | AA |
| `--cyan` | `#06B6D4` | cs-foundations, T0-flavored | `--on-fill` | 7.53:1 | AA |
| `--lime` | `#84CC16` | engineering-process | `--on-fill` | 9.25:1 | AA |
| `--purple` | `#A855F7` | ai-ml, tier T0 chip | `--on-fill` | 4.62:1 | AA |
| `--slate` | `#64748B` | hardware track, novice badge | **white** `#FFFFFF` | 4.76:1 | AA (exception, documented in code) |

Dark theme: `--bg #12101C`, `--surface #1D1A2B`, `--surface-2 #262238`,
`--ink #F4F1E9` (16.66 / 15.07 / 13.60), `--ink-soft #B3AECC` (8.82 / 7.97 / 7.19),
link `#8FBEFF` (8.89). Fills keep the same hexes and **always** use dark
`--on-fill` text (bright fills + cream text would fail — ratio ≈1.5:1, so the
fill-text token is constant across themes by design).

Tier chips (T0 `#A855F7`, T1 `#3A86FF`, T2 `#14B8A6`, T3 `#F59E0B`, T4 `#FF5C39`)
and level badges (novice `#64748B` white-text, advanced-beginner `#3A86FF`,
competent `#2EC4B6`, proficient `#7C6FF0`, expert `#FFB703`) all pass with their
documented text pairing. Color is never the only signal: tier chips carry the
letter (`T0`…`T4`), verdicts carry a stamped word + icon, levels carry the Dreyfus
name.

---

## 3. Type Scale

System sans stack only (`system-ui, -apple-system, "Segoe UI", Roboto,
"Helvetica Neue", Arial`); mono stack for ids (`ui-monospace, Cascadia Code,
Consolas`). Numbers use `font-variant-numeric: tabular-nums`.

| Token | Size / weight | Tracking | Use |
|---|---|---|---|
| `--fs-display` | `clamp(2.4rem, 5.5vw, 3.6rem)` · 900 | −0.03em | screen h1, big numerals (`res-big` 3.4rem) |
| `--fs-h2` | `clamp(1.6rem, 3.2vw, 2.2rem)` · 850 | −0.03em | section headings |
| `--fs-h3` | 1.15rem · 750 | −0.03em | card titles |
| `--fs-body` | 1rem · 400–650 | — | body, options |
| `--fs-small` | .8125rem · 600–750 | — | chips, meta, table |
| `--fs-micro` | .6875rem · 800, uppercase | +.06–.16em | kickers, labels, HUD captions |

Display-scale numerals + uppercase micro-labels are the "arcade marquee" voice;
the uppercase-kicker + tight-tracking h1 pattern is the crafted, non-template-y
signature.

---

## 4. Pattern Language

| Pattern | Description | Where |
|---|---|---|
| Sticker card | white/surface card, 2px ink border, `border-radius 24/16/10`, hard offset shadow `0 5px 0 ink` (theme-aware in dark) | every screen |
| Coin button | pill, `--coin` fill, dark ink text, 2px border, hard shadow that *depresses* on `:active`, hover lift | all CTAs; `.mint/.coral/.violet` variants for meaning |
| Stamp | rotated dashed-border word (PARTIAL/CORRECT/INCORRECT) with `stampIn` scale-from-1.9 animation | verdict card |
| Progress ring | SVG circle, `stroke-dashoffset` transitioned 1.1s ease-out, label in center | dashboard mastery, calibration |
| Flame | SVG flame, `flameFlicker` transform loop, drop-shadow; small static variant | streak HUD, streak forge, combo meter |
| Window | tower window button — lit/dim/off/locked/due-blink states, `blink` steps animation | world map |
| Blink | `steps(2,start)` opacity toggle for due attention (never rely on it alone — due rows also carry text chips) | map windows, heatmap cells |
| Ladder | rung dots (1→3→7→14→30→60→120) with done/now/upcoming states | quest cards, spacing explainer |
| Combo meter | `×N` + flame, `pulseRing` halo when it grows; cosmetic only (never affects scores) | quiz |
| Confetti | JS-spawned colored rects, `confettiFall` keyframe with per-piece `--dx/--rot/delay`, auto-cleanup, **disabled under reduced motion** | correct answers, verdicts, results |
| Toast | bottom-centered pill (ink bg, cream text), slide-up + auto-dismiss | scheduling, quest start, reflection |
| Shake | 0.4s `shake` on wrong options only | quiz |
| Typing dots | 3-dot bounce indicator before the verdict resolves | validate |

Motion budget: entries are ≤1.1s, non-looping except flame flicker / shimmer /
blink (all killed under `prefers-reduced-motion: reduce`).

---

## 5. Component Inventory → Screens

| # | Component | D1 Dashboard | D2 World map | D3 Validate | D4 Quiz | D5 Quests | D6 Progress |
|---|---|---|---|---|---|---|---|
| 1 | Top bar (brand, alias HUD, streak HUD, theme toggle) | ● | ● | ● | ● | ● | ● |
| 2 | Tab rail (6 tabs, hash-routed) | ● | ● | ● | ● | ● | ● |
| 3 | Streak forge (flame + 7-day dot row + grace) | ● | | | | | |
| 4 | Quest mini-list (overdue / due chips) | ● | | | | ● | |
| 5 | Progress ring | ● | | | | | ● |
| 6 | Rank & XP card (shimmer bar, XP ledger) | ● | | ● | ● | | |
| 7 | Skill heatmap (12 columns × topics, states) | ● | | | | | ● |
| 8 | Quick actions grid | ● | | | | | |
| 9 | City legend | | ● | | | | |
| 10 | Tower (track header, floor axis B6–B0, window grid) | | ● | | | | |
| 11 | Window button (lit/dim/off/lock/due) + topic dialog | | ● | | | | |
| 12 | Claim box (textarea + topic chip) | | | ● | | | |
| 13 | Verdict sim switch (REAL/partial/correct/incorrect) | | | ● | | | |
| 14 | Verdict card (stamp, tier chip, evidence records, corrective path, rewards, schedule) | | | ● | | | |
| 15 | Quiz meta (item counter, progress bar, combo) | | | | ● | | |
| 16 | Question card (bank/bloom chips, options, feedback) | | | | ● | | |
| 17 | Quiz results (score, reschedule, replay) | | | | ● | | |
| 18 | Quest card (due chip, ladder, meta, start → dialog) | | | | | ● | |
| 19 | Spacing ladder explainer | | | | | ● | |
| 20 | Calibration card (ring, insight chips) | | | | | | ● |
| 21 | Predicted-vs-actual SVG chart | | | | | | ● |
| 22 | Activity sparkline | | | | | | ● |
| 23 | Skill matrix table | | | | | | ● |
| 24 | Reflection pocket | | | | | | ● |
| 25 | Dialog (native `<dialog>`) | | ● | | | ● | |
| 26 | Toast + confetti FX layer | ● | ● | ● | ● | ● | ● |

27 components; 6 screens.

---

## 6. Data Mapping (UI ← schema / frontmatter)

`R` = real data in the exploration; `M` = plausible mock, **always labeled MOCK in-UI**.

| UI element | Data source (field) |
|---|---|
| Alias HUD | `profile.json → alias` (`alex-dev`, R) |
| Rank badge (R3 · Ship It) | derived from XP thresholds (M); Dreyfus levels from `profile.json → levels` (R: cs-foundations=advanced-beginner, systems-software=novice, engineering-process=competent) |
| Streak HUD / forge | derived from `logs/*.jsonl → session.completed` dates (M; no streak field exists — computed, per event schema) + grace rule (design decision) |
| Quest mini-list / board | `review-queue.json → items[]`: `topic`, `due`, `interval_days`, `reviews`, `last_review` (R: http-caching 08-19/3d/2, garbage-collection 08-17/1d/1) |
| Mastery ring (62%) | avg of `skill-matrix.json → topics[].score` (R: 80, 55) + M |
| Skill heatmap cell states | `skill-matrix.json → topics[]` score+validated (R for http-caching 80 ✓, garbage-collection 55 ✗) + `review-queue.json` due (blink) |
| Rank & XP card | XP ledger = derived from event types (`claim.verdict`, `quiz.attempted`…) with per-event point values (M values; event *types* R from `event.schema.json`) |
| Tower track header | `tracks.yml → track.<id>.title`, `.bands` (R) |
| Tower floors | `concept.md frontmatter → band` (B6…B0) (R) |
| Window states | `INDEX.md/knowledge-graph.yml → status` (published/draft, R) + `skill-matrix.json → validated` (R) + `review-queue.json → due` (R) |
| Topic dialog | frontmatter: `id, title, band, tier, bloom_target, status, sources[]` (R) + matrix/queue overlay |
| Tier chips | frontmatter `tier` T0–T4 (R) — topic tier = strongest claim tier (spec §6.3 v1.1) |
| Claim textarea | `session.example.jsonl → claim.submitted.payload.claim` (R) |
| Verdict stamp/note/records | `claim.verdict.payload → verdict, tier, record, note` (R) |
| Corrective path chips | `knowledge-graph.yml → prerequisites[] / recommended[]` (R: http-basics → http-caching; next: caching-strategies) |
| Reward pills (+XP, streak) | derived from `event.schema.json` types (M values) |
| Quiz items | `validation.md` Q1–Q10: `Q, A, bloom, bank, evidence, topic` (R; MC-ified, distractors written from the model answers) |
| Combo / progress | in-memory session state → `quiz.attempted.payload → bank, score, bloom_scores` (schema R, values M) |
| Ladder | spec §4.1 ladder (1,3,7,14,30,60,120) + `review-queue.json → interval_days, reviews` (R) |
| Skill matrix table | `skill-matrix.json → topics[]` (R 2 rows) |
| Calibration ring/chart | `calibration.updated` payload → predicted vs actual (M; mechanism from spec §4.1 Flavell) |
| Reflection pocket | `reflection.logged` (M) |
| "Schedule review" / "Quest started" | writes `review.due`, `session.started`, `review.completed`, `reflection.logged` events per `event.schema.json` (simulated in exploration) |

---

## 7. Accessibility Notes

- **Contrast:** every text pairing in use ≥4.5:1 (see §2 — all computed, not assumed).
  The `--on-fill` rule (dark text on bright fills, both themes) is what makes
  vivid styling safe; slate is the one white-text exception and is tokenized.
- **Motion:** all animation/transition durations killed to ~0 under
  `@media (prefers-reduced-motion: reduce)`; confetti is additionally gated in JS
  via `matchMedia`. No animation is essential to understanding — due/verdict
  states always carry text + chips, never blink alone.
- **Semantics:** `header/nav/main/section/article/table/dialog`, `role=tablist/
  tabpanel`, `aria-selected/controls/label`, `aria-live="polite"` verdict slot,
  `role="status"` feedback + toast, `aria-hidden` on decorative SVGs, skip link,
  native `<dialog>` (focus trap + Esc free).
- **Keyboard/touch:** all interactive elements are real buttons/links; 42px
  icon buttons, ≥44px option rows; `:focus-visible` ring token.
- **Color-blind safety:** meaning never carried by hue alone — tier letters, stamped
  verdict words, text labels, icons alongside color.
- **Gamification without exclusion:** no leaderboards (data stays local, K5), no
  shame states — incorrect verdicts still award participation XP, streak grace
  flame forgives one miss per week, and "calibration" is framed as a dial to tune,
  not a grade. The `<noscript>` path explains the JS dependency; layout/tokens are
  plain CSS.
- **Themes:** tokens under `:root` + `[data-theme="dark"]`; pre-paint boot script
  respects stored choice else `prefers-color-scheme`; manual toggle in the HUD.
  (Exploration note: with JS disabled the UI stays readable in light mode.)

---

## 8. Risks & Tradeoffs

| Risk | Mitigation in this direction | Residual |
|---|---|---|
| **Novelty decay** — confetti is a dopamine loan; it compounds, not cancels | Celebration budget is capped (correct answers, verdicts, results — never per-click); XP is explicitly labeled participation, mastery is the ring; the scoreboard reframes value as *calibration*, which gets *more* interesting as data accumulates | Daily-driver novelty may still fade; needs periodic "seasonal" refresh patterns (not in scope) |
| **Engagement theater** — progress that isn't learning | Every reward maps to a schema event (`claim.verdict`, `quiz.attempted`, `review.completed`); the UI states where each number comes from; MOCK data is labeled | Risk that users optimize XP instead of matrix scores — mitigated by keeping XP cosmetic |
| **Streak anxiety / guilt** | Grace flame (1 free miss/week), streak is only "showing up", never compounded pressure; no streak-shaming copy | Streaks still nudge; some learners are negatively motivated by them — offer opt-out in a future iteration |
| **Childish = untrusted** | Bold ≠ cutesy: display type discipline, uppercase micro-labels, muted cream base, restrained palette per screen; only the city map is "illustrated" | Tone is subjective; needs real-user testing with senior engineers (persona §3) |
| **Noise vs K3 progressive disclosure** | Screens mirror the protocol: dashboard (L0 summary) → map (L1) → topic dialog (L2) → records (L3); one screen at a time via tabs | 6 screens can still overwhelm; tab rail stays text-first |
| **Accessibility of decorative motion** | Reduced-motion kill switch + non-essential status (see §7) | Blink pattern must never be the sole due indicator (already doubled with chips) |
| **CSS feature support** (`color-mix`, `backdrop-filter`) | Body/background fallback colors declared; `color-mix` only used for tints; exploration targets evergreen browsers | Older browsers lose tint gradients, not function |
| **Local-first honesty** | No accounts/telemetry anywhere; theme choice in localStorage (local only); every "writes event" action is simulated and labeled in this exploration | None beyond scope |

---

## 9. Files

| File | Purpose | Size |
|---|---|---|
| `index.html` | self-contained exploration: 6 screens, 27 components, light/dark themes, reduced-motion, real + labeled mock data | ~63 KB |
| `brief.md` | this document | — |

Everything lives in `ui/explorations/arcade/`; nothing else in the repo was touched.
