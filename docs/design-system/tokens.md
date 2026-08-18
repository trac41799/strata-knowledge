# Design Tokens — Reference

Canonical source: `ui/design-system/tokens.css`. This file documents every token and states the computed WCAG 2.1 contrast ratio for every text-bearing pair, light and dark.

**Method.** Relative luminance `L` per WCAG 2.1 (sRGB linearization, threshold 0.03928); contrast `C = (L₁+0.05)/(L₂+0.05)`. Requirements: normal text ≥ 4.5:1; large text (≥18.66px bold or ≥24px) ≥ 3:1. All ratios rounded to 1 decimal. "Exempt" = decorative or disabled-state only, never body copy.

**Type floor (Atelier mandate).** Smallest meaningful caption is `--text-caption` = **12px**. No token, no component, no SVG tick label renders below 12px. Core body is `--text-base` = **14px**.

---

## 1. Non-color tokens (theme-independent, `:root`)

| Token | Value | Notes |
|---|---|---|
| `--font-sans` | `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` | prose face |
| `--font-mono` | `ui-monospace, "SF Mono", "Cascadia Mono", "JetBrains Mono", Menlo, Consolas, monospace` | data face |
| `--font-nums` | `"tnum" 1` | tabular numerals on all numeric columns |
| `--text-caption` | 0.75rem (12px) / lh 1.4 / ls 0.08em | **floor**; uppercase labels, tags, table headers, heat cells, tick labels |
| `--text-sm` | 0.8125rem (13px) / lh 1.45 | secondary text, log lines, chips |
| `--text-base` | 0.875rem (14px) / lh 1.5 | **core body** |
| `--text-lead` | 1rem (16px) / lh 1.5 | quiz question text, lead copy |
| `--text-title` | 1.25rem (20px) / lh 1.3 / ls 0.06em | screen titles, register values |
| `--text-stat` | 1.625rem (26px) / lh 1.2 | dashboard stat values (qualifies as large text) |
| `--fw-regular/-medium/-bold` | 400 / 500 / 700 | — |
| `--space-05…--space-7` | 2 · 4 · 8 · 12 · 16 · 24 · 32 · 48px | spacing scale |
| `--gutter` / `--container-max` | 16px / 1280px | layout |
| `--radius-sm/-md/-pill` | 2 / 4 / 999px | panels/chips/LEDs |
| `--motion-fast/-base/-ease` | 120ms / 180ms / ease-out | transitions |
| `--z-sticky` / `--z-tooltip` / `--z-dialog` | 20 / 900 / 1000 | stacking |

---

## 2. Color tokens — values per theme

| Token | Dark | Light | Usage |
|---|---|---|---|
| `--bg` | `#0A0E14` | `#F4F6F8` | page canvas |
| `--surface` | `#0F151E` | `#FAFBFC` | panels, ordinary cards (elev-2) |
| `--surface-2` | `#131B26` | `#FFFFFF` | panel headers, nested (elev-3) |
| `--surface-hover` | `#182130` | `#E9EEF3` | row/cell hover |
| `--line` / `--line-strong` | `#1D2A3A` / `#2A3B52` | `#C8D2DE` / `#9AA8BB` | borders (non-text) |
| `--text` | `#D3DCE8` | `#1B2733` | primary text |
| `--text-soft` | `#8494A9` | `#4A5A6B` | secondary text, captions |
| `--text-faint` | `#5B6B7F` | `#7B8998` | disabled/decorative only |
| `--accent` | `#2DD4BF` | `#0F766E` | primary accent, active states, focus ring |
| `--accent-hover` | `#5EEAD4` | `#0B5F59` | CTA hover fill |
| `--amber` | `#F5A623` | `#8A5B00` | secondary accent, warnings |
| `--info` | `#60A5FA` | `#1D4ED8` | agent-link LED, informational |
| `--ok` | `#34D399` | `#15803D` | correct / published / REAL |
| `--warn` | `#F5A623` | `#8A5B00` | partial / due-soon (alias of amber) |
| `--bad` | `#F87171` | `#B91C1C` | incorrect / retired / MOCK-adjacent errors |
| `--frontier` | `#F472B6` | `#BE185D` | T4 frontier, volatile |
| `--tier-0…` | `#C084FC` | `#7C3AED` | T0 formal (violet) |
| `--tier-1…` | `#60A5FA` | `#1D4ED8` | T1 empirical (blue) |
| `--tier-2…` | `#2DD4BF` | `#0F766E` | T2 consensus (teal = accent) |
| `--tier-3…` | `#F5A623` | `#8A5B00` | T3 practice (amber) |
| `--tier-4…` | `#F472B6` | `#BE185D` | T4 frontier (magenta = frontier) |
| `--on-accent` | `#0A0E14` | `#FFFFFF` | text on accent fills (CTA) |
| `--tint-accent/-amber/-ok/-bad/-info/-tier-0/-tier-4` | rgba fills ≈ .13–.14 | solid pales (`#E4F0EF`, `#F4E8D0`, …) | tag/chip backgrounds |
| `--chip-accent/-amber/-ok/-bad/-info/-tier-0/-tier-4` | bright hues | darkened hues (`#166534`, `#8A5B00`, …) | text on tints |
| `--prov-real-bg/-fg` | `rgba(52,211,153,.13)` / `#34D399` | `#E2F1E8` / `#166534` | REAL provenance tag |
| `--prov-mock-bg/-fg` | `rgba(245,166,35,.14)` / `#F5A623` | `#F4E8D0` / `#8A5B00` | MOCK provenance tag |
| `--led-on/-warn/-bad/-idle/-off` | `#34D399`/`#F5A623`/`#F87171`/`#60A5FA`/`#334155` | `#15803D`/`#8A5B00`/`#B91C1C`/`#1D4ED8`/`#B9C2CE` | status LED fills (non-text) |
| `--led-*-glow` | glow shadows (dark) / ring shadows (light) | same | LED glow |
| `--heat-1…--heat-5` | teal rgba α .12/.22/.34/.42/.64 | teal rgba α .10/.20/.32/.46/.62 | heatmap cell fills (non-text; counts are text) |
| `--heat-validated` | `rgba(245,166,35,.28)` | `rgba(138,91,0,.30)` | learner-validated cell |
| `--heat-text` | `#D3DCE8` | `#1B2733` | cell text (levels 1–4; validated) |
| `--heat-text-strong` | `#0A0E14` | `#1B2733` | cell text on the deepest tint (dark h5) |

### Elevation (three tiers)

| Token | Dark | Light | Applies to |
|---|---|---|---|
| `--elev-1-bg` / `-bg-hover` / `-text` / `-border` / `-glow` | `#2DD4BF` / `#5EEAD4` / `#0A0E14` / `#2DD4BF` / glow 1px ring + 16px halo | `#0F766E` / `#0B5F59` / `#FFFFFF` / `#0F766E` / ring + 10px shadow | **prominent CTA** — exactly one per screen |
| `--elev-2-bg` / `-border` / `-shadow` | `#0F151E` / `#1D2A3A` / none | `#FAFBFC` / `#C8D2DE` / `0 1px 2px rgba(27,39,51,.06)` | ordinary cards, panels |
| `--elev-3-bg` / `-border` / `-shadow` | `#131B26` / `#1D2A3A` / inset 1px ring | `#FFFFFF` / `#C8D2DE` / inset 1px ring | nested tables, log streams, accordions |

### Borders & focus

| Token | Value |
|---|---|
| `--border` / `--border-strong` | 1px `--line` / 1px `--line-strong` |
| `--border-accent` / `-ok` / `-warn` / `-bad` | 1px accent / ok / warn / bad (verdict rails, state outlines) |
| `--focus-ring` | 2px solid `--accent` (visible on all surface contexts) |
| `--focus-ring-inverse` | 2px solid `--bg` (on accent-filled controls) |
| `--focus-ring-offset` | 2px |
| `--focus-ring-shadow` / `--focus-ring-inverse-shadow` | `0 0 0 2px` forms where `outline` is clipped |
| `--backdrop` | `rgba(10,14,20,.7)` / `rgba(27,39,51,.35)` (dialog) |

---

## 3. Contrast — text tokens on surfaces (dark)

| Token (fg) | on `--bg` | on `--surface` | on `--surface-2` |
|---|---|---|---|
| `--text` | **14.0:1** | **13.2:1** | **13.4:1** |
| `--text-soft` | **6.7:1** | **5.9:1** | **5.6:1** |
| `--text-faint` | 3.6:1 ⚠ exempt | 3.4:1 ⚠ exempt | 3.4:1 ⚠ exempt |
| `--accent` | 10.4:1 | 9.8:1 | 9.3:1 |
| `--amber` / `--warn` | 9.5:1 | 9.0:1 | 8.5:1 |
| `--ok` | 10.1:1 | 9.5:1 | 9.0:1 |
| `--bad` | 7.0:1 | 6.6:1 | 6.3:1 |
| `--info` / `--tier-1` | 7.6:1 | 7.2:1 | 6.8:1 |
| `--frontier` / `--tier-4` | 7.3:1 | 6.9:1 | 6.5:1 |
| `--tier-0` | 7.3:1 | 6.9:1 | 6.6:1 |
| `--tier-2` | = accent | = accent | = accent |
| `--tier-3` | = amber | = amber | = amber |

## 4. Contrast — text tokens on surfaces (light)

| Token (fg) | on `--bg` | on `--surface` | on `--surface-2` |
|---|---|---|---|
| `--text` | **14.0:1** | **14.6:1** | **15.2:1** |
| `--text-soft` | **6.5:1** | **6.8:1** | **7.1:1** |
| `--text-faint` | 3.3:1 ⚠ exempt | 3.4:1 ⚠ exempt | 3.4:1 ⚠ exempt |
| `--accent` | 5.1:1 | 5.3:1 | 5.5:1 |
| `--amber` / `--warn` | **4.7:1** ⚠ | 4.9:1 | 5.1:1 |
| `--ok` | **4.6:1** ⚠ | 4.8:1 | 5.0:1 |
| `--bad` | 6.0:1 | 6.2:1 | 6.5:1 |
| `--info` / `--tier-1` | 6.2:1 | 6.5:1 | 6.7:1 |
| `--frontier` / `--tier-4` | 5.6:1 | 5.8:1 | 6.0:1 |
| `--tier-0` | 5.3:1 | 5.5:1 | 5.7:1 |

⚠ = the three pairs nearest the 4.5:1 threshold (see §9). They still pass; treat as the pairs most likely to fail first if values drift.

## 5. Contrast — on-accent (CTA text)

| Pair | Dark | Light |
|---|---|---|
| `--on-accent` on `--elev-1-bg` (`--accent`) | **10.4:1** | **5.5:1** |
| `--on-accent` on `--elev-1-bg-hover` (`--accent-hover`) | **13.1:1** | **7.5:1** |
| `--focus-ring-inverse` (`--bg`) on `--elev-1-bg` | 10.4:1 | 5.1:1 (visible ring ✓) |

## 6. Contrast — chip text on tint fills (tags, badges, provenance)

Dark theme: tints are rgba over `--surface` (blend computed); light theme: solid pales.

| Chip token | Dark (fg on tint-over-surface) | Light (fg on solid tint) |
|---|---|---|
| `--chip-accent` on `--tint-accent` | 7.5:1 | 4.7:1 |
| `--chip-amber` on `--tint-amber` | 7.1:1 | 4.8:1 |
| `--chip-ok` on `--tint-ok` | 7.5:1 | 6.1:1 |
| `--chip-bad` on `--tint-bad` | 5.6:1 | 5.3:1 |
| `--chip-info` on `--tint-info` | 5.9:1 | 5.6:1 |
| `--chip-tier-0` on `--tint-tier-0` | 5.7:1 | 4.9:1 |
| `--chip-tier-4` on `--tint-tier-4` | 5.8:1 | 5.1:1 |
| `--prov-real-fg` on `--prov-real-bg` | 7.5:1 | 6.1:1 |
| `--prov-mock-fg` on `--prov-mock-bg` | 7.1:1 | 4.8:1 |

## 7. Contrast — heatmap cells (text on tint fills)

Cell numbers are `--text-caption` (12px) — they must meet 4.5:1. Dark fills blend teal/amber rgba over `--surface`; light blends over `--surface`.

| Fill (dark α / light α) | Dark text token → ratio | Light text token → ratio |
|---|---|---|
| `--heat-1` (.12 / .10) | `--heat-text` 10.6:1 | `--heat-text` 13.4:1 |
| `--heat-2` (.22 / .20) | `--heat-text` 8.3:1 | `--heat-text` 12.3:1 |
| `--heat-3` (.34 / .32) | `--heat-text` 6.1:1 | `--heat-text` 10.8:1 |
| `--heat-4` (.42 / .46) | `--heat-text` **4.9:1** ⚠ | `--heat-text` 9.2:1 |
| `--heat-5` (.64 / .62) | `--heat-text-strong` **4.9:1** ⚠ | `--heat-text` 7.3:1 |
| `--heat-validated` (.28 / .30) | `--heat-text` 7.5:1 | `--heat-text` 11.0:1 |

⚠ Dark `--heat-4` and `--heat-5` are the riskiest heat pairs: `--heat-4` sits at 4.9:1 with the default text token, and `--heat-5` requires the `--heat-text-strong` switch (component rule, not optional). The dark ramp is capped at α .64 because deeper tints cannot hold either light or dark text at ≥4.5:1 (the 0.12–0.19 luminance dead zone).

## 8. Non-text pairs (informational)

- `--led-*` fills + glow: status only — every LED is accompanied by a text label in `--text-soft` (6.5–6.7:1). LED color is never the sole channel.
- `--line` / `--line-strong` / `--border*` / `--elev-*-border` / `--heat-*` fills: decorative, no text directly on them.
- `--backdrop`: scrim behind dialogs; page content remains distinguishable (≥ 3:1 against underlying panel edges in both themes).

## 9. Risk register — the three pairs to protect

1. **Light `--ok` on `--bg`: 4.6:1** — the closest pass in the system. `--ok` is used for REAL tags, published status, correct-answer borders. If any light-theme green value is lightened, it breaks 4.5:1. Guard: keep light `--ok` ≤ `#15803D`; use `--chip-ok` `#166534` for text on tints (6.1:1).
2. **Dark `--heat-4` cell text: 4.9:1** — second-closest; the ramp step above it (`--heat-5`) *requires* `--heat-text-strong`. Component rule: at heat-5 and above the cell text token switches; never widen the alpha ramp past .64 without re-verifying both text tokens.
3. **Light `--amber` on `--bg`: 4.7:1** — amber is the MOCK/warn/partial hue; it must stay ≤ `#8A5B00` in light. Pair with `--chip-amber` (4.8:1) for tint fills. Note `--amber` is also `--warn` and `--tier-3` in light — a single drift point affects three tokens.
