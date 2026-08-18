# Plan — Journey Interface UI (Phase 8, ADR-0001)

> **For agentic workers:** REQUIRED SUB-SKILL: `executing-plans`. Test-first (TDD):
> write the failing test → run it (red) → implement → run again (green) → commit.
> One commit per task, `feat(ui):`/`test(ui):`/`ci(ui):` style. Tasks are bite-sized
> and order-dependent — do not skip ahead. Visual reference:
> `ui/explorations/instrument/index.html` + `brief.md` (the selected Instrument-core
> direction); design-system prose lives in `docs/design-system/` (authored under
> `docs/plan.md` 7.3/7.4 — this plan only creates the code + machine-readable
> annotations it needs); canonical tokens: `ui/design-system/tokens.css`.

## 1. Goal & architecture

A local-first, offline static web app in `ui/app/` renders the six Journey-Interface
screens (dashboard, topic explorer, validate flow, quiz session, review queue,
progress/calibration) from `.journey/`-shaped JSON + committed maps, mirroring the
harness progressive-disclosure protocol (K3) and never mutating canonical knowledge
(K5, ADR-0001). The browser consumes **JSON only** — no YAML/Markdown parsing in JS:
`ui/tools/gen-fixtures.py` deterministically derives browser JSON fixtures from
`knowledge-graph.yml`, `validation.md`, and `concept.md`, so the data contract is the
committed schemas (K6), exactly like the repo's other generated files.

**Stack:** vanilla HTML/CSS/JS (`ui/app/`, no build step, no CDN — offline per ADR-0001)
+ Python stdlib `unittest` for token/fixture unit tests + Python Playwright (chromium,
`file://` URLs per the `webapp-testing` skill) for E2E. **One-line justification:** the
repo is zero-dependency stdlib-Python + no-node by constitution (`docs/spec.md` §12,
`docs/plan.md` tech stack), so the UI keeps the same discipline and Playwright is the
single test-only dependency. Data loading is provenance-aware: `index.html?data=mock|real|empty`
switches the data base (`ui/app/js/loader.js` stamps `source:{base,file}` on every
dataset so renderers can tag REAL vs MOCK); v1 ships these three bases — reading a live
`.journey/` path is a documented extension point, not a v1 goal.

## 2. Test infrastructure

**Layout** (created by task T1, extended per task):

```
ui/
├── app/                     # the app (static, no build)
│   ├── index.html
│   ├── styles/app.css       # component styles (shell, LED, tags, tables, charts)
│   └── js/
│       ├── main.js          # router: tablist ↔ data-screen sections
│       ├── loader.js        # provenance-aware data base resolution + fetch
│       └── screens/{dashboard,explorer,validate,quiz,review,progress}.js
├── design-system/
│   ├── tokens.css           # canonical tokens (dark + light), loaded first
│   └── token-pairs.json     # machine-readable contrast contract (fg/bg token pairs)
├── tests/
│   ├── unit/                # Python stdlib unittest (no deps)
│   │   ├── test_tokens.py
│   │   ├── test_fixtures.py
│   │   └── test_seeds.py
│   ├── e2e/                 # Playwright (Python), file:// URLs
│   │   ├── helpers.py       # browser launch, load_app(), assert_no_console_errors()
│   │   ├── run_all.py       # fixture refresh + run every test_*.py headless
│   │   └── test_00_smoke.py … test_13_smoke_screens.py
│   ├── fixtures/
│   │   ├── generated/       # COMMITTED, tool-derived (graph.json, packs/, claims/)
│   │   ├── mock/            # COMMITTED, hand-written, every file listed in README.md
│   │   ├── seeds/           # COMMITTED, offset-based journey seeds (not schema-valid by design)
│   │   └── empty/           # COMMITTED marker dir (README.md only)
│   └── out/                 # GITIGNORED: date-relative fixtures built at test time
└── tools/gen-fixtures.py    # stdlib; reuses tools/_yaml_mini.py
```

**Local commands** (run from repo root; Windows PowerShell and Ubuntu bash both fine):

```bash
# unit + fixture determinism
python -m unittest discover -s ui/tests/unit -v
python ui/tools/gen-fixtures.py                # rewrites ui/tests/fixtures/generated/
git diff --exit-code                           # generated fixtures must not drift

# E2E (one-time install: python -m pip install playwright; playwright install chromium)
python ui/tests/e2e/run_all.py                 # refreshes date-relative fixtures, runs all test_*.py
```

**CI** (task T17 modifies `.github/workflows/ci.yml` — new `ui-tests` job):
`setup-python 3.12` → `python -m pip install playwright` → `python -m playwright install --with-deps chromium` →
`python -m unittest discover -s ui/tests/unit -v` → `python ui/tools/gen-fixtures.py` →
`git diff --exit-code` → `python ui/tests/e2e/run_all.py`.

**Fixture strategy.**

- **REAL** = `journey/examples/*` (profile, skill-matrix, review-queue, session.jsonl — the
  committed redacted samples) read directly via `?data=real`, plus
  `ui/tests/fixtures/generated/` — `graph.json` (topics: id/title/track/band/tier/bloom/status/
  prerequisites/related, from `knowledge-graph.yml`), `packs/<topic-id>.json` (quiz items
  Q/bloom/bank/A/evidence/topic from `validation.md`), `claims/<topic-id>.json`
  (claim text + `[T*]` tier + `[S-####]` records from `concept.md`). Generated by
  `ui/tools/gen-fixtures.py`, committed, CI drift-checked.
- **MOCK** = `ui/tests/fixtures/mock/` — hand-written calibration dataset
  (`calibration.json`, `events.jsonl`) + `README.md` that lists every mock file; loader
  stamps `source.base='mock'` and the UI renders the amber `MOCK` tag on any element
  fed by it.
- **EMPTY** = `ui/tests/fixtures/empty/` (README only) — simulates a machine with no
  `.journey/`; loader resolves `null` datasets for journey-derived screens.
- **Date determinism** = `ui/tests/fixtures/seeds/*.seed.json` carry integer offsets
  (`due_offset_days: -1, 0, +3 …`); `gen-fixtures.py` rewrites them relative to
  *today* into gitignored `ui/tests/out/fixtures/` (used by the E2E runner via
  `?data=out`). Both Python (expectation) and JS (render) compute "due ≤ today" with
  **local date-only** comparison (no UTC) so the two can never disagree by a timezone
  boundary.

## 3. Tasks

Each task: `Files` (exact paths, C=create / M=modify), `Failing test` (real code),
`Expected failure`, `Implementation sketch`, `Expected pass`, `Commit`.

---

### T1 — App skeleton + E2E harness

- **Files (C):** `ui/app/index.html`, `ui/tests/e2e/helpers.py`, `ui/tests/e2e/run_all.py`,
  `ui/tests/e2e/test_00_smoke.py`, `ui/tests/fixtures/mock/README.md`,
  `ui/tests/fixtures/empty/README.md`, `ui/README.md`
- **Files (M):** `.gitignore` (append `ui/tests/out/`)
- **Failing test** (`ui/tests/e2e/test_00_smoke.py`):

```python
# ui/tests/e2e/test_00_smoke.py
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="mock")                      # file:// …/ui/app/index.html?data=mock
        assert_no_console_errors(page)                   # helper: collects console + pageerror
        assert page.title() == "STRATA // JOURNEY INTERFACE"
        page.wait_for_selector("#shell", timeout=5000)   # header + tablist container
        assert page.locator("main[data-screen='dashboard']").count() == 1
        browser.close()

if __name__ == "__main__":
    main()
```

`helpers.py` must define `load_app(page, data)` (resolves `Path("ui/app/index.html").resolve().as_uri()` + `?data=`), `assert_no_console_errors(page)`, `focusable(page, root)`; `run_all.py` must enumerate `test_*.py`, refresh out-fixtures, run each in a fresh chromium headless process, exit non-zero on any failure.
- **Expected failure:** `ui/app/index.html` missing → script crashes on `goto`; no `#shell`.
- **Implementation sketch:** create `index.html` with `<html lang="en">`, `<meta name="color-scheme" content="dark light">`, title `STRATA // JOURNEY INTERFACE`, `<div id="shell">` wrapping a placeholder header + `<main data-screen="dashboard">` with one `<section>`. Create helpers/runner per above. `.gitignore` += `ui/tests/out/`. `ui/README.md`: run instructions (`python -m http.server` for manual browsing; `?data=` semantics; "reading a live `.journey/` path is a future extension").
- **Expected pass:** smoke green, zero console errors, title + `#shell` + dashboard screen present.
- **Commit:** `feat(ui): app skeleton + e2e harness (T1)`

---

### T2 — Design tokens + programmatic contrast contract

- **Files (C):** `ui/design-system/tokens.css`, `ui/design-system/token-pairs.json`,
  `ui/tests/unit/test_tokens.py`
- **Files (M):** `ui/app/index.html` (add `<link rel="stylesheet" href="../design-system/tokens.css">` before any other CSS)
- **Failing test** (`ui/tests/unit/test_tokens.py`, stdlib only):

```python
# ui/tests/unit/test_tokens.py
import json, re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # repo root
TOKENS = ROOT / "ui/design-system/tokens.css"
PAIRS  = ROOT / "ui/design-system/token-pairs.json"

REQUIRED = ["--bg-0", "--bg-1", "--bg-2", "--text-1", "--text-2", "--text-3",
            "--acc-teal", "--acc-amber", "--ok", "--err", "--info",
            "--t0", "--t1", "--t2", "--t3", "--t4",
            "--tint-teal", "--tint-amber", "--tint-ok", "--tint-err",
            "--tint-info", "--tint-t0", "--tint-t4",
            "--chip-teal", "--chip-amber", "--chip-ok", "--chip-err",
            "--chip-info", "--chip-t0", "--chip-t4", "--sans", "--mono",
            "--fs-0", "--fs-1", "--fs-2", "--fs-3", "--fs-4", "--fs-5"]

def theme_values(css, selector):
    block = re.search(re.escape(selector) + r"\s*\{(.*?)\}", css, re.S).group(1)
    return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block))

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lum(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ratio(fg, bg):
    l1, l2 = sorted((lum(hex2rgb(fg)), lum(hex2rgb(bg))), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

def composite(fg, alpha, bg):                        # tint token over bg
    bgc, fgc = hex2rgb(bg), hex2rgb(fg)
    return tuple(round(alpha * f + (1 - alpha) * b) for f, b in zip(fgc, bgc))

class TokenContract(unittest.TestCase):
    def test_required_tokens_present_in_both_themes(self):
        css = TOKENS.read_text(encoding="utf-8")
        for theme in (":root", ":root[data-theme='light']"):
            vals = theme_values(css, theme)
            for tok in REQUIRED:
                self.assertIn(tok, vals, f"{tok} missing in {theme}")

    def test_all_contrast_pairs_pass_both_themes(self):
        css = TOKENS.read_text(encoding="utf-8")
        pairs = json.loads(PAIRS.read_text(encoding="utf-8"))["pairs"]
        self.assertTrue(len(pairs) >= 20)
        for theme_name, selector in (("dark", ":root"), ("light", ":root[data-theme='light']")):
            vals = theme_values(css, selector)
            for p in pairs:
                fg = vals[p["fg"]]; bg = vals[p["bg"]]
                if p.get("tint"):                      # chip text on tint over panel bg
                    bg = "%02X%02X%02X" % composite(vals[p["tint"]], 0.14, vals[p["bg"]])
                r = ratio(fg, bg)
                floor = p.get("min", 4.5)
                self.assertGreaterEqual(r, floor,
                    f"{p['fg']} on {p['bg']} ({theme_name}) = {r:.2f}:1 < {floor}:1")
                if p.get("decorative_only"):
                    self.assertIn(p["fg"], ("--text-3",))   # only text-3 may be < 4.5

    def test_text3_flagged_decorative_and_never_body_copy(self):
        for p in json.loads(PAIRS.read_text(encoding="utf-8"))["pairs"]:
            if p["fg"] == "--text-3":
                self.assertTrue(p.get("decorative_only"))
                self.assertLess(p.get("min", 4.5), 4.5)

if __name__ == "__main__":
    unittest.main()
```

`token-pairs.json` contract: `{"pairs": [{"fg": "--text-1", "bg": "--bg-0", "min": 4.5}, …, {"fg": "--chip-amber", "bg": "--bg-1", "tint": "--tint-amber", "min": 4.5}, {"fg": "--text-3", "bg": "--bg-0", "min": 3.0, "decorative_only": true}]}` — every text-bearing color in both themes ≥ 4.5:1 (≥ 3:1 for `decorative_only`/large), matching `instrument/brief.md` §2.
- **Expected failure:** tokens.css / token-pairs.json missing → `FileNotFoundError`; also `test_required_tokens_present_in_both_themes` fails on empty file.
- **Implementation sketch:** port the Instrument token set verbatim (`instrument/index.html` lines 9–54: `:root` dark + `:root[data-theme="light"]`) into `ui/design-system/tokens.css`; add `@media (prefers-color-scheme: light){ :root:not([data-theme]) { … } }`; write `token-pairs.json` covering all text/chip/tint pairs with the ratios stated in the brief (the test enforces them).
- **Expected pass:** both unit tests green — tokens parsed, every pair ≥ floor in both themes.
- **Commit:** `feat(ui): design tokens with enforced contrast (T2)`

---

### T3 — Shell + theme switching (tokens load end-to-end)

- **Files (C):** `ui/app/styles/app.css`, `ui/app/js/main.js` (router stub)
- **Files (M):** `ui/app/index.html` (link app.css; header markup: brand, LED row `#led-local` "JRNY LOCAL", theme toggle `<button id="theme-toggle">`; placeholder `<main data-screen="dashboard">`)
- **Failing test** (`ui/tests/e2e/test_01_themes.py`):

```python
# ui/tests/e2e/test_01_themes.py
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="mock")
        assert_no_console_errors(page)
        dark = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--bg-0').trim()")
        assert dark == "#0A0E14", dark                      # tokens.css actually loaded
        assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(10, 14, 20)"
        page.emulate_media(color_scheme="light", reduced_motion="reduce")
        page.reload(); page.wait_for_selector("#shell")
        assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(244, 246, 248)"
        page.emulate_media(color_scheme="no-preference")
        page.reload(); page.wait_for_selector("#shell")
        page.click("#theme-toggle")
        assert page.get_attribute("html", "data-theme") == "light"
        assert page.evaluate("getComputedStyle(document.body).backgroundColor") == "rgb(244, 246, 248)"
        assert page.locator("#led-local").inner_text() == "JRNY LOCAL"   # LED pairs text, never color alone
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no app.css/theme toggle → body background is default white; `#theme-toggle` missing.
- **Implementation sketch:** `main.js` sets `data-theme` from `matchMedia('(prefers-color-scheme)')` if no explicit choice, toggles on button click, persists for the session; header LED row with visible text labels (Instrument pattern #2); `app.css` uses only `var(--tokens)` — no hardcoded colors.
- **Expected pass:** all three backgrounds + toggle + LED assertions green; zero console errors.
- **Commit:** `feat(ui): shell header, LED row, theme switch (T3)`

---

### T4 — Nav tablist + six screen placeholders (keyboard-first)

- **Files (C):** `ui/app/js/screens/__init__` not needed (vanilla) — only markup in index.html this task
- **Files (M):** `ui/app/index.html` (role=tablist with 6 tabs `Dashboard/Explorer/Validate/Quiz/Review/Progress`, `aria-controls` + `aria-selected`; six `<section data-screen=…>` with `<h2>` headings, all but dashboard `hidden`), `ui/app/js/main.js` (roving tabindex + arrow-key nav)
- **Failing test** (`ui/tests/e2e/test_02_nav.py`):

```python
# ui/tests/e2e/test_02_nav.py
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

TABS = ["dashboard", "explorer", "validate", "quiz", "review", "progress"]

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="mock")
        assert_no_console_errors(page)
        assert page.get_attribute("[role='tablist']", "role") == "tablist"
        tabs = page.locator("[role='tab']")
        assert tabs.count() == 6
        assert [t.get_attribute("aria-controls") for t in tabs.all()] == TABS
        assert page.locator("section[data-screen='dashboard']").is_visible()
        for s in TABS[1:]:
            assert not page.locator(f"section[data-screen='{s}']").is_visible()
        tabs.nth(0).focus()
        page.keyboard.press("ArrowRight")
        assert tabs.nth(1).get_attribute("aria-selected") == "true"
        assert tabs.nth(0).get_attribute("tabindex") == "-1"
        assert tabs.nth(1).get_attribute("tabindex") == "0"
        assert page.locator("section[data-screen='explorer']").is_visible()
        page.keyboard.press("ArrowRight"); page.keyboard.press("ArrowRight")
        page.keyboard.press("ArrowRight"); page.keyboard.press("ArrowRight")
        assert tabs.nth(5).get_attribute("aria-selected") == "true"      # wrap-around
        page.keyboard.press("Home"); assert tabs.nth(0).get_attribute("aria-selected") == "true"
        page.keyboard.press("End");  assert tabs.nth(5).get_attribute("aria-selected") == "true"
        assert page.locator("section[data-screen='dashboard']").get_attribute("hidden") is not None
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no tablist/aria attrs; ArrowRight does nothing.
- **Implementation sketch:** WAI-ARIA tabs pattern — `tabindex=-1` on inactive, `0` on active, `ArrowLeft/Right/Home/End`, `aria-selected` + `hidden` panel swap, `.screen.active` styling off `hidden` (no CSS display games — tests rely on the `hidden` attribute).
- **Expected pass:** keyboard nav + panel switching green in both directions with wrap-around.
- **Commit:** `feat(ui): nav tablist with roving-tabindex keyboard nav (T4)`

---

### T5 — Loader + fixture generator (data contract, K6)

- **Files (C):** `ui/tools/gen-fixtures.py`, `ui/app/js/loader.js`,
  `ui/tests/unit/test_fixtures.py`, `ui/tests/unit/test_seeds.py`
- **Files (C, generated, committed):** `ui/tests/fixtures/generated/graph.json`,
  `ui/tests/fixtures/generated/packs/systems-software/http-caching.json` (+ every published topic),
  `ui/tests/fixtures/generated/claims/systems-software/http-caching.json`
- **Files (C, seeds):** `ui/tests/fixtures/seeds/{profile,skill-matrix,review-queue,session}.seed.json`
- **Failing test** (`ui/tests/unit/test_fixtures.py`, excerpt):

```python
# ui/tests/unit/test_fixtures.py  (stdlib; imports tools._yaml_mini for frontmatter)
import json, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
GEN = ROOT / "ui/tests/fixtures/generated"

class GraphFixture(unittest.TestCase):
    def test_graph_json_matches_knowledge_graph_yml(self):
        graph = json.loads((GEN / "graph.json").read_text(encoding="utf-8"))
        topics = {t["id"]: t for t in graph["topics"]}
        self.assertEqual(graph["topic-count"], 68)            # knowledge-graph.yml: topic-count: 68
        self.assertEqual(graph["wave-count"], 8)
        t = topics["systems-software/http-caching"]
        self.assertEqual(t["band"], "B4"); self.assertEqual(t["tier"], "T2")
        self.assertEqual(t["prerequisites"], ["systems-software/http-basics"])
        self.assertEqual(t["related"], ["architecture-design/caching-strategies"])
        self.assertEqual(t["status"], "published")
        self.assertIn("cs-foundations/logic-and-proof", topics)   # no topic lost

    def test_pack_fixture_item_shape(self):
        pack = json.loads((GEN / "packs/systems-software/http-caching.json").read_text(encoding="utf-8"))
        items = pack["items"]
        self.assertGreaterEqual(len(items), 6)                # AC2: ≥6 Bloom items
        banks = {i["bank"] for i in items}
        self.assertEqual(banks, {"formative", "summative", "review"})
        q1 = items[0]
        for key in ("id", "q", "bloom", "bank", "a", "evidence", "topic"):
            self.assertIn(key, q1)
        self.assertEqual(q1["topic"], "systems-software/http-caching")
        self.assertIn("S-0009", q1["evidence"])
        self.assertIn(q1["bloom"], {"remember", "understand", "apply", "analyze", "evaluate", "create"})

    def test_claims_fixture_shape(self):
        claims = json.loads((GEN / "claims/systems-software/http-caching.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(claims["claims"]), 15)    # 21 claims in concept.md
        for c in claims["claims"]:
            self.assertRegex(c["tier"], r"^T[0-4]$")
            self.assertTrue(c["records"])                     # every claim cites ≥1 record
            self.assertGreater(len(c["text"]), 20)

    def test_generated_fixtures_are_deterministic(self):
        import subprocess, sys
        before = {p.name: p.read_bytes() for p in GEN.rglob("*") if p.is_file()}
        subprocess.run([sys.executable, str(ROOT / "ui/tools/gen-fixtures.py")], check=True, cwd=ROOT)
        for p in GEN.rglob("*"):
            if p.is_file():
                self.assertEqual(before[p.name], p.read_bytes(), f"drift: {p}")

class SeedDates(unittest.TestCase):
    def test_seed_offsets_become_relative_dates(self):
        out = ROOT / "ui/tests/out/fixtures"
        q = json.loads((out / "review-queue.json").read_text(encoding="utf-8"))
        import datetime
        today = datetime.date.today()
        for item in q["items"]:
            due = datetime.date.fromisoformat(item["due"])
            self.assertEqual(due, today + datetime.timedelta(days=item["_offset_days"]))
        self.assertEqual(sum(1 for i in q["items"] if i["_offset_days"] <= 0), 2)  # seeds: -2, -1, +3
```

- **Expected failure:** script/tests missing → `FileNotFoundError`.
- **Implementation sketch:** `gen-fixtures.py` (stdlib, imports `tools/_yaml_mini.py`): parse `knowledge-graph.yml` (yaml-mini block/flow syntax) → `graph.json`; parse each published topic's `validation.md` `### Qn` blocks (`Q:`/`bloom:`/`bank:`/`A:`/`evidence:`/`topic:`) → `packs/<id>.json`; parse `concept.md` claim bullets (`[T*]` + `[S-####]` tags) → `claims/<id>.json`; validate against `tools/schemas` where applicable; assert INDEX.md consistency (topic count + published count lines); `--dates` mode rewrites seeds → `ui/tests/out/fixtures/`. `loader.js`: `resolveBase(data)` maps `mock|real|empty|out` → paths, fetches JSON/JSONL, stamps `source:{base,file}`; unknown base → `null` dataset. `index.html` loads loader.js first.
- **Expected pass:** unit tests green; generated fixtures committed, deterministic.
- **Commit:** `feat(ui): loader + fixture generator, browser JSON contract (T5)`

---

### T6 — Action-first dashboard

- **Files (C):** `ui/app/js/screens/dashboard.js`
- **Files (M):** `ui/app/index.html` (dashboard section: registers from profile + `#primary-action` button + `<dialog id="session-dialog">`), `ui/app/js/main.js` (screen renderer dispatch)
- **Failing test** (`ui/tests/e2e/test_03_dashboard.py`):

```python
# ui/tests/e2e/test_03_dashboard.py
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="mock")
        assert_no_console_errors(page)
        page.click("[role='tab'] >> text=Dashboard")
        # action-first: primary action is the FIRST focusable control in <main>
        first = page.eval_on_selector_all("main button, main a[href], main input, main [tabindex]",
                                          "els => els[0].id")
        assert first == "primary-action", first
        # visual weight: primary bg contrast vs page ≥3:1 and strictly heavier than secondary
        w = page.evaluate("""() => {
          const pageBg = getComputedStyle(document.body).backgroundColor;
          const el = document.getElementById('primary-action');
          const s = getComputedStyle(el);
          const f = s.backgroundColor, fs = parseFloat(s.fontSize);
          const rgb = c => c.match(/\\d+/g).map(Number);
          const lum = c => { const f = rgb(c).map(v => { v/=255;
            return v <= 0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
            return 0.2126*f[0] + 0.7152*f[1] + 0.0722*f[2]; };
          const ratio = (a,b) => { const l = [lum(a), lum(b)].sort((x,y)=>y-x);
            return (l[0]+0.05)/(l[1]+0.05); };
          return { primary: ratio(f, pageBg), fontSize: fs }; }""")
        assert w["primary"] >= 3.0, w
        assert w["fontSize"] >= 15, w                                  # ≥ --fs-3
        page.click("#primary-action")
        assert page.eval_on_selector("#session-dialog", "d => d.open") is True
        assert page.locator("#session-dialog h2").inner_text().startswith("Session")
        assert page.locator("#led-local").inner_text() == "JRNY LOCAL"  # visible text next to every LED
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no `#primary-action` / it is not first / dialog absent.
- **Implementation sketch:** dashboard renders profile alias register + due LED (count from loaded queue, `data-source` stamped by loader); `#primary-action` "Start session" is the first element in the dashboard `<section>` DOM, styled with `--acc-teal` background (≥3:1 on `--bg-0`) and `--fs-3`, heavier than all secondary buttons (transparent/`--bg-2`); click opens native `<dialog>` with session manifest heading; secondary actions follow in DOM.
- **Expected pass:** action-first + weight + dialog + LED-text assertions green.
- **Commit:** `feat(ui): action-first dashboard + session dialog (T6)`

---

### T7 — Topic explorer (graph-driven)

- **Files (C):** `ui/app/js/screens/explorer.js`
- **Files (M):** `ui/app/index.html` (explorer section: registers, track accordions, topic table)
- **Failing test** (`ui/tests/e2e/test_04_explorer.py`):

```python
# ui/tests/e2e/test_04_explorer.py
import json
from pathlib import Path
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    graph = json.loads((Path(__file__).resolve().parents[2] / "fixtures/generated/graph.json")
                       .read_text(encoding="utf-8"))
    expected_topics = {t["id"] for t in graph["topics"]}
    expected_tracks = sorted({t["track"] for t in graph["topics"]})
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="real")
        assert_no_console_errors(page)
        page.click("[role='tab'] >> text=Explorer")
        # registers computed from the SAME fixture the app consumed (not hardcoded)
        page.wait_for_selector("#explorer-registers")
        counts = page.eval_on_selector_all("#explorer-registers .rval", "els => els.map(e => e.textContent)")
        assert counts[0] == str(graph["topic-count"])
        # dense table: every topic row, columns from graph contract
        rows = page.locator("#topic-table tbody tr")
        assert rows.count() == len(expected_topics)
        first = rows.nth(0).locator("td").all_inner_texts()
        assert first[0] == sorted(expected_topics)[0]                 # id
        assert len(first) == 6                                        # id,title,band,tier,bloom,status
        # track accordions
        details = page.locator("#explorer-tracks details")
        assert details.count() == len(expected_tracks)
        # tier distribution register matches graph
        t0 = sum(1 for t in graph["topics"] if t["tier"] == "T0")
        assert page.locator("#stat-t0").inner_text() == str(t0)
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** explorer section empty; no rows/registers.
- **Implementation sketch:** explorer.js consumes `graph.json` (via loader, `data-source="real:<…/graph.json>"`), renders: registers (topic-count, published, tier distribution computed in JS), `<details>` per track with per-track counts, sticky-header table (`th scope="col"`) with one row per topic, `data-topic="<id>"`; filter chips (`aria-pressed`) filter rows client-side.
- **Expected pass:** all counts/rows match the fixture-derived expectations; zero console errors.
- **Commit:** `feat(ui): topic explorer driven by graph fixture (T7)`

---

### T8 — Explorer heatmap + legend (color never the only channel)

- **Files (M):** `ui/app/js/screens/explorer.js` (heatmap grid + legend), `ui/app/index.html` (heatmap container + `.legend` strip)
- **Failing test** (`ui/tests/e2e/test_05_legend.py`):

```python
# ui/tests/e2e/test_05_legend.py
import json
from pathlib import Path
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    graph = json.loads((Path(__file__).resolve().parents[2] / "fixtures/generated/graph.json")
                       .read_text(encoding="utf-8"))
    tracks = sorted({t["track"] for t in graph["topics"]})
    bands = sorted({t["band"] for t in graph["topics"]})
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="real")
        page.click("[role='tab'] >> text=Explorer")
        page.wait_for_selector("#heatmap")
        cells = page.locator("#heatmap .hm-cell")
        assert cells.count() == len(tracks) * len(bands)          # full track × band matrix
        # every cell carries its count as TEXT (color is redundant with the number)
        texts = cells.all_inner_texts()
        assert all(t.isdigit() for t in texts)
        # counts agree with the fixture
        expected = {}
        for t in graph["topics"]:
            expected[(t["track"], t["band"])] = expected.get((t["track"], t["band"]), 0) + 1
        cell = page.locator(f"#heatmap .hm-cell[data-track='systems-software'][data-band='B4']")
        assert cell.inner_text() == str(expected[("systems-software", "B4")])
        # legend: every swatch has a text label; required entries present
        legend = page.locator("#explorer-legend .legend-item")
        labels = legend.all_inner_texts()
        assert len(legend) >= 4
        for required in ("band", "tier", "status", "count"):
            assert any(required in lab.lower() for lab in labels), labels
        for swatch in page.locator("#explorer-legend .legend-swatch").all():
            assert swatch.get_attribute("aria-hidden") is None     # never decorative-only color
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no `#heatmap`/legend; empty.
- **Implementation sketch:** heatmap = CSS grid of `data-track`/`data-band` cells, count text per cell, tint from `--tint-teal` (validated) / amber (published) only as background; legend strip with swatch + text pairs (band axis, tier chips T0–T4, status, count note); wrap in overflow container (natural tab order, no scroll trap).
- **Expected pass:** matrix count, cell text digits, fixture-verified cell, legend entries green.
- **Commit:** `feat(ui): explorer heatmap + legend (T8)`

---

### T9 — Validate flow: verdict card from event schema data

- **Files (C):** `ui/app/js/screens/validate.js`
- **Files (M):** `ui/app/index.html` (validate section: claim form `#claim-form` textarea + topic select, `#verdict-card` container with `aria-live="polite"`)
- **Failing test** (`ui/tests/e2e/test_06_validate.py`):

```python
# ui/tests/e2e/test_06_validate.py
import json
from pathlib import Path
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    # expected values are read from the REAL event fixture — the schema contract
    lines = (Path(__file__).resolve().parents[2].parent / "journey/examples/session.example.jsonl") \
            .read_text(encoding="utf-8").splitlines()
    verdict = next(json.loads(l)["payload"] for l in lines if json.loads(l)["type"] == "claim.verdict")
    assert verdict["verdict"] == "partial"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="real")
        page.click("[role='tab'] >> text=Validate")
        page.wait_for_selector("#claim-form")
        page.fill("#claim-text", "Cache-Control max-age makes a response reusable for that many seconds")
        page.press("#claim-text", "Enter")                 # Enter submits (form semantics)
        page.wait_for_selector("#verdict-card")
        assert page.locator("#verdict-badge").inner_text() == verdict["verdict"].upper()   # PARTIAL
        assert page.locator("#verdict-tier").inner_text() == f"[{verdict['tier']}]"        # [T2]
        assert page.locator("#verdict-record").inner_text() == f"[{verdict['record']}]"    # [S-0009]
        assert verdict["note"] in page.locator("#verdict-note").inner_text()               # verbatim
        # matched claims rendered from the claims fixture, tagged with tier+record
        matched = page.locator("#matched-claims li").first.inner_text()
        assert "[T2]" in matched and "[S-0009]" in matched
        assert page.get_attribute("#verdict-output", "aria-live") == "polite"
        # corrective path: prereq chain from graph fixture, ▶ = order-constrained
        path = page.locator("#corrective-path").inner_text()
        assert "http-basics" in path and "▶" in path
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no form/verdict card; nothing renders.
- **Implementation sketch:** validate.js on submit finds the most recent `claim.verdict` event for the selected topic in the loaded event log (session fixture) and renders badge (CORRECT/PARTIAL/INCORRECT text, tier color only as background), tier tag, record tag, verbatim note, matched claims from `claims/<topic>.json` (filtered by record), corrective path (prerequisite chain from `graph.json` with `▶` separators; `→` for related). `#verdict-output` wraps the card with `aria-live="polite"`. No verdict event for the topic → "no verdict recorded" empty state (task T13 covers it).
- **Expected pass:** all verbatim/derived assertions green.
- **Commit:** `feat(ui): validate flow verdict card (T9)`

---

### T10 — Quiz session: formative items + feedback

- **Files (C):** `ui/app/js/screens/quiz.js`
- **Files (M):** `ui/app/index.html` (quiz section: `#quiz-bank` selector, `#quiz-item` card, `#quiz-feedback`, `#quiz-score`)
- **Failing test** (`ui/tests/e2e/test_07_quiz.py`):

```python
# ui/tests/e2e/test_07_quiz.py
import json
from pathlib import Path
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    pack = json.loads((Path(__file__).resolve().parents[2] / "fixtures/generated/packs/"
                       "systems-software/http-caching.json").read_text(encoding="utf-8"))
    formative = [i for i in pack["items"] if i["bank"] == "formative"]
    q1 = formative[0]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="real")
        page.click("[role='tab'] >> text=Quiz")
        page.wait_for_selector("#quiz-item")
        page.select_option("#quiz-bank", "formative")
        assert q1["q"][:60] in page.locator("#quiz-question").inner_text()      # verbatim Q
        assert page.locator("#quiz-bloom").inner_text() == q1["bloom"].upper()
        assert f"[{q1['evidence'][0]}]" in page.locator("#quiz-tags").inner_text()
        page.click("#quiz-option-1")                                            # answer wrong-ish
        page.wait_for_selector("#quiz-feedback")
        model = q1["a"]
        assert model[:60] in page.locator("#quiz-feedback .feedback-body").inner_text()   # A: shown
        assert page.locator("#quiz-feedback").get_attribute("data-correct") in ("true", "false")
        assert page.locator("#quiz-score .rval").inner_text().isdigit()
        assert page.get_attribute("#quiz-feedback", "aria-live") == "polite"
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no item card/options/feedback.
- **Implementation sketch:** quiz.js loads `packs/<topic>.json`, filters by `bank`, renders Q/bloom/evidence tags + 4 option buttons (`#quiz-option-1..4`); on answer: marks correct option, stamps `data-correct` on the feedback panel, reveals `A:` model answer text, updates `#quiz-score` register; bank selector (formative/summative/review) reloads the item list; `aria-live="polite"` on feedback.
- **Expected pass:** verbatim Q/A, bloom/evidence tags, score, live region green.
- **Commit:** `feat(ui): formative quiz session with feedback (T10)`

---

### T11 — Review queue: due computation from schema

- **Files (C):** `ui/app/js/screens/review.js`
- **Files (M):** `ui/app/index.html` (review section: `#review-table`, `#spacing-ladder`), `ui/tests/fixtures/seeds/review-queue.seed.json` (offsets `-2, -1, +3`), `ui/tests/fixtures/seeds/profile.seed.json` (alias `alex-dev`), `ui/tests/fixtures/seeds/skill-matrix.seed.json`
- **Failing test** (`ui/tests/e2e/test_08_review.py`):

```python
# ui/tests/e2e/test_08_review.py
import datetime, json
from pathlib import Path
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    out = Path(__file__).resolve().parents[2] / "out/fixtures"
    q = json.loads((out / "review-queue.json").read_text(encoding="utf-8"))
    today = datetime.date.today()
    due = [i for i in q["items"] if datetime.date.fromisoformat(i["due"]) <= today]   # local date-only
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="out")                        # date-relative fixtures
        assert_no_console_errors(page)
        # LED count agrees with Python-side computation on the SAME file
        led = page.locator("#led-due").inner_text()
        assert led == f"{len(due)} DUE", (led, len(due))
        page.click("[role='tab'] >> text=Review")
        page.wait_for_selector("#review-table")
        rows = page.locator("#review-table tbody tr")
        assert rows.count() == len(due)                   # only due items listed
        for i in due:
            row = page.locator(f"#review-table tr[data-topic='{i['topic']}']")
            assert row.count() == 1
            assert row.locator("td").nth(1).inner_text() == i["due"]          # due column = schema field
            assert row.locator("td").nth(2).inner_text() == str(i["interval_days"])
        # spacing ladder: 7 steps (1/3/7/14/30/60/120), the item's interval marked
        steps = page.locator("#spacing-ladder .ladder-step")
        assert steps.count() == 7
        for off, lab in zip((1, 3, 7, 14, 30, 60, 120),
                            steps.all_inner_texts()):
            assert str(off) in lab
        assert page.locator("#spacing-ladder .ladder-step.active").count() == len(due)
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no review table/LED count/ladder.
- **Implementation sketch:** review.js renders `items[]` from the loaded queue where `due ≤ today` (JS local date-only: `d.getFullYear()/getMonth()+1/getDate()` string compare — never `toISOString()`), LED count in header (`#led-due`), table columns topic/due/interval_days/reviews/last_review (all from schema fields), ladder with 7 fixed steps and `.active` marks at each due item's `interval_days`.
- **Expected pass:** Python-computed expectation == rendered count; rows/columns/ladder green.
- **Commit:** `feat(ui): review queue with due computation (T11)`

---

### T12 — Progress/calibration: skill matrix + predicted-vs-actual chart

- **Files (C):** `ui/app/js/screens/progress.js`, `ui/tests/fixtures/mock/calibration.json`,
  `ui/tests/fixtures/mock/events.jsonl` (score history, clearly MOCK)
- **Files (M):** `ui/app/index.html` (progress section: `#matrix-table`, `#cal-chart` SVG container, `#cal-legend`, `#cal-table`), `ui/tests/fixtures/mock/README.md` (list new files)
- **Failing test** (`ui/tests/e2e/test_09_progress.py`):

```python
# ui/tests/e2e/test_09_progress.py
import json
from pathlib import Path
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    cal = json.loads((Path(__file__).resolve().parents[2] / "fixtures/mock/calibration.json")
                     .read_text(encoding="utf-8"))
    assert len(cal["points"]) >= 5
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="mock")
        assert_no_console_errors(page)
        page.click("[role='tab'] >> text=Progress")
        page.wait_for_selector("#matrix-table")
        matrix = json.loads((Path(__file__).resolve().parents[2] / "fixtures/mock/skill-matrix.json")
                            .read_text(encoding="utf-8"))
        rows = page.locator("#matrix-table tbody tr")
        assert rows.count() == len(matrix["topics"])
        r0 = rows.nth(0).locator("td").all_inner_texts()
        assert r0[0] == list(matrix["topics"].keys())[0]
        assert r0[2] == str(matrix["topics"][list(matrix["topics"].keys())[0]]["score"])  # score col
        # calibration chart: accessible SVG with name, diagonal, both series, legend, table
        chart = page.locator("#cal-chart")
        assert chart.get_attribute("role") == "img"
        assert chart.locator("title").inner_text() == "Calibration: predicted vs actual"
        assert page.locator("#cal-chart .cal-diag").count() == 1          # y = x ideal
        assert page.locator("#cal-chart .cal-predicted").count() == 1
        assert page.locator("#cal-chart .cal-actual").count() == 1
        leg = page.locator("#cal-legend .legend-item").all_inner_texts()
        assert any("predicted" in t.lower() for t in leg)
        assert any("actual" in t.lower() for t in leg)
        assert page.locator("#cal-table tbody tr").count() == len(cal["points"])
        # calibration is MOCK data → amber MOCK tag, never mistaken for measurement
        assert page.locator("#cal-panel [data-provenance='mock']").count() >= 1
        assert page.locator("#cal-panel .tag-mock").inner_text() == "MOCK"
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no matrix rows/chart/legend/MOCK tag.
- **Implementation sketch:** progress.js renders matrix table (level/score/validated/last_attempt/evidence columns from `skill-matrix.json`), calibration SVG (`role="img"` + `<title>/<desc>`, dashed gridlines with tick labels, `y=x` diagonal, predicted vs actual polylines from `calibration.json`), legend with text labels, numeric table beside the chart (AT parity), `data-provenance="mock"` on the panel + amber `MOCK` tag. REAL mode (no calibration data): panel shows empty state (T13) — never fabricated numbers.
- **Expected pass:** matrix, chart accessibility, legend, parity table, MOCK provenance green.
- **Commit:** `feat(ui): progress + calibration chart (T12)`

---

### T13 — Empty states (missing `.journey/`)

- **Files (M):** `ui/app/js/screens/{dashboard,validate,quiz,review,progress}.js` (empty-state branches), `ui/app/index.html` (`.empty-state` blocks per journey-derived screen)
- **Failing test** (`ui/tests/e2e/test_10_empty.py`):

```python
# ui/tests/e2e/test_10_empty.py
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="empty")
        assert_no_console_errors(page)                       # no crash on missing data
        page.click("[role='tab'] >> text=Dashboard")
        page.wait_for_selector("#empty-dashboard")
        assert "no journey data" in page.locator("#empty-dashboard").inner_text().lower()
        page.click("[role='tab'] >> text=Review")
        assert page.locator("#empty-review").inner_text() == "No review items due — nothing scheduled."
        page.click("[role='tab'] >> text=Progress")
        assert page.locator("#empty-progress").inner_text() == "No skill matrix yet — complete a session."
        page.click("[role='tab'] >> text=Validate")
        assert page.locator("#empty-validate").inner_text() == "No verdict recorded for this topic."
        page.click("[role='tab'] >> text=Explorer")
        rows = page.locator("#topic-table tbody tr").count() # committed maps still render
        assert rows > 50
        page.click("[role='tab'] >> text=Dashboard")
        assert page.locator("#led-due").inner_text() == "NO DATA"
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** blank screens / JS errors / no empty-state text.
- **Implementation sketch:** loader returns `null` datasets for the empty base; every journey-derived screen checks `dataset == null` and renders its `.empty-state` (exact strings asserted); explorer keeps rendering from committed `graph.json` (knowledge ≠ journey — K5); header LED shows `NO DATA` text.
- **Expected pass:** all six screen states + no console errors green.
- **Commit:** `feat(ui): empty states for missing journey files (T13)`

---

### T14 — Provenance labels: REAL vs MOCK

- **Files (M):** `ui/app/js/loader.js` (provenance stamping), `ui/app/styles/app.css` (`.tag-real`/`.tag-mock`), `ui/app/index.html` (footer provenance policy line)
- **Failing test** (`ui/tests/e2e/test_11_provenance.py`):

```python
# ui/tests/e2e/test_11_provenance.py
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        # MOCK base: every data element carries the amber MOCK tag
        load_app(page, data="mock")
        assert_no_console_errors(page)
        page.click("[role='tab'] >> text=Progress")
        page.wait_for_selector("[data-source]")
        for el in page.locator("[data-source]").all():
            src = el.get_attribute("data-source")
            if src.startswith("mock"):
                assert el.locator(".tag-mock").count() == 1, el.get_attribute("id")
        assert page.locator(".tag-mock").first.inner_text() == "MOCK"
        # REAL base: green REAL tag + file path, never MOCK
        page = browser.new_page()
        load_app(page, data="real")
        page.click("[role='tab'] >> text=Review")
        page.wait_for_selector("[data-source]")
        for el in page.locator("[data-source]").all():
            src = el.get_attribute("data-source")
            if src.startswith("real"):
                assert el.locator(".tag-real").count() == 1
        assert "journey/examples" in page.locator(".tag-real").first.inner_text()
        # footer restates the policy (honest-provenance discipline)
        assert "REAL" in page.locator("footer").inner_text() and "MOCK" in page.locator("footer").inner_text()
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no `data-source` attrs/tags; provenance invisible.
- **Implementation sketch:** loader stamps `source.base` per dataset; each renderer emits `data-source="real:<relpath>"` or `data-source="mock:<file>"` on data-bearing containers; CSS renders green `.tag-real` (REAL · path) vs amber `.tag-mock` (MOCK); footer states the policy line (Instrument §4.12 / §8).
- **Expected pass:** every stamped element tagged, tags correctly typed per base, footer present.
- **Commit:** `feat(ui): provenance labels real/mock (T14)`

---

### T15 — Keyboard + reduced-motion a11y (WCAG 2.2 AA)

- **Files (M):** `ui/app/styles/app.css` (`:focus-visible`, `@media (prefers-reduced-motion: reduce)`, motion guard), `ui/app/js/main.js` (motion class + dialog focus management), `ui/app/index.html` (skip link `#skip-to-main`)
- **Failing test** (`ui/tests/e2e/test_12_a11y.py`):

```python
# ui/tests/e2e/test_12_a11y.py
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        page = browser.new_page()
        load_app(page, data="mock")
        assert_no_console_errors(page)
        # skip link first in DOM, targets main
        assert page.locator("#skip-to-main").count() == 1
        assert page.locator("#skip-to-main").get_attribute("href") == "#main-content"
        # focus-visible: 2px outline on the focused tab
        page.locator("[role='tab']").nth(0).focus()
        outline = page.eval_on_selector("[role='tab']", "e => getComputedStyle(e).outlineWidth")
        assert outline in ("2px", "3px"), outline
        # dialog: Escape closes, focus returns to trigger
        page.click("#primary-action")
        assert page.eval_on_selector("#session-dialog", "d => d.open") is True
        page.keyboard.press("Escape")
        assert page.eval_on_selector("#session-dialog", "d => d.open") is False
        assert page.eval_on_selector("document.activeElement", "e => e.id") == "primary-action"
        # reduced motion: all transitions/animations off
        page.emulate_media(reduced_motion="reduce")
        page.reload(); page.wait_for_selector("#shell")
        page.locator("[role='tab']").nth(1).focus()
        assert page.evaluate("getComputedStyle(document.querySelectorAll('[role=tab]')[1]).transitionDuration") == "0s"
        # rendered-text contrast walk (small ≥4.5:1, large ≥3:1) — token-level is unit-tested,
        # this proves actual usage incl. chips/tints, excluding decorative-only elements
        bad = page.evaluate("""() => {
          const lum = c => { const f = c.match(/\\d+/g).map(Number).map(v => { v/=255;
            return v <= 0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
            return 0.2126*f[0] + 0.7152*f[1] + 0.0722*f[2]; };
          const ratio = (a,b) => { const l=[lum(a),lum(b)].sort((x,y)=>y-x); return (l[0]+0.05)/(l[1]+0.05); };
          const out = [];
          const walk = el => {
            for (const n of el.childNodes) {
              if (n.nodeType === 3 && n.textContent.trim()) {
                const c = getComputedStyle(el), fs = parseFloat(c.fontSize), bold = c.fontWeight >= 700;
                const large = fs >= 24 || (fs >= 18.66 && bold);
                if (el.closest('[data-decorative],[disabled]')) continue;
                let bg = getComputedStyle(el).backgroundColor, p = el;
                while ((bg === 'rgba(0, 0, 0, 0)' || !bg) && p.parentElement)
                  { p = p.parentElement; bg = getComputedStyle(p).backgroundColor; }
                if (bg === 'rgba(0, 0, 0, 0)') bg = 'rgb(10, 14, 20)';
                const r = ratio(c.color, bg);
                if (r < (large ? 3 : 4.5)) out.push(`${el.tagName}: ${r.toFixed(2)}`);
              } else if (n.nodeType === 1 && n.offsetParent) walk(n);
            } };
          walk(document.body); return out; }""")
        assert bad == [], bad
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** no skip link; no focus outline; dialog traps/ignores Escape; transitions survive reduced motion; contrast walk reports violations.
- **Implementation sketch:** `:focus-visible{outline:2px solid var(--acc-teal); outline-offset:2px}`; skip link as first focusable; dialog uses native `<dialog>` (Escape free) with focus return handled by `showModal()` restore semantics; `main.js` sets `html.motion-reduced` when `matchMedia('(prefers-reduced-motion: reduce)')` and CSS kills transitions/animations; `--text-3` only ever used inside `[data-decorative]`/`[disabled]` (audited by the walk).
- **Expected pass:** all five blocks green (skip link, outline, dialog, motion, contrast walk).
- **Commit:** `feat(ui): keyboard + reduced-motion + contrast a11y (T15)`

---

### T16 — E2E smoke: all six screens (Playwright, file://)

- **Files (C):** `ui/tests/e2e/test_13_smoke_screens.py`
- **Failing test** (`ui/tests/e2e/test_13_smoke_screens.py`):

```python
# ui/tests/e2e/test_13_smoke_screens.py
from helpers import assert_no_console_errors, load_app
from playwright.sync_api import sync_playwright

def main():
    screens = {
        "dashboard": ("#primary-action", "Dashboard"),
        "explorer":  ("#topic-table",    "Explorer"),
        "validate":  ("#claim-form",     "Validate"),
        "quiz":      ("#quiz-item",      "Quiz"),
        "review":    ("#review-table",   "Review"),
        "progress":  ("#matrix-table",   "Progress"),
    }
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--allow-file-access-from-files"])
        for data in ("mock", "real", "out"):
            page = browser.new_page()
            load_app(page, data=data)
            assert_no_console_errors(page)
            for name, (sel, label) in screens.items():
                page.click(f"[role='tab'] >> text={label}")
                page.wait_for_selector(sel, timeout=5000)
                assert page.locator(f"section[data-screen='{name}']").is_visible()
            page.close()
        browser.close()

if __name__ == "__main__":
    main()
```

- **Expected failure:** any screen missing its anchor on any data base.
- **Implementation sketch:** nothing to build beyond `run_all.py` wiring — this task is the regression net; fix any gaps it surfaces (e.g., a screen that crashes on a data base) as part of this task.
- **Expected pass:** 3 data bases × 6 screens × zero console errors.
- **Commit:** `test(ui): six-screen e2e smoke across data bases (T16)`

---

### T17 — CI job for the UI

- **Files (M):** `.github/workflows/ci.yml` (add `ui-tests` job), `ui/README.md` (CI note)
- **Failing test:** the repo's CI has no UI coverage — verify by running the exact CI command sequence locally; the job definition is the deliverable. Assertion list (run locally, then in CI): `python -m unittest discover -s ui/tests/unit -v` green → `python ui/tools/gen-fixtures.py` green → `git diff --exit-code` exits 0 (generated fixtures committed, no drift) → `python ui/tests/e2e/run_all.py` green.
- **Expected failure:** no job → no UI validation in CI (this is the "red": CI would pass without any UI tests — the task's assertion is the presence of the job + green sequence).
- **Implementation sketch:** add `ui-tests` job to `.github/workflows/ci.yml`: `runs-on: ubuntu-latest`, `setup-python 3.12`, `pip install playwright`, `python -m playwright install --with-deps chromium`, then the four commands above; keep the existing `validate` job untouched (spec §12 gates).
- **Expected pass:** PR shows both jobs green; `ui-tests` fails on any unit/E2E regression or fixture drift.
- **Commit:** `ci(ui): journey interface test job (T17)`

## 4. Definition of done (per task)

1. **Tests green:** exact commands from §2 pass for the task's touched scope — unit: `python -m unittest discover -s ui/tests/unit -v`; E2E: the task's `test_*.py` via `python ui/tests/e2e/run_all.py` (which must also show zero console errors via the helper).
2. **No drift:** any task touching `ui/tests/fixtures/generated/` re-runs `python ui/tools/gen-fixtures.py` and confirms `git diff --exit-code` is clean (generated files are never hand-edited — AGENTS.md §6).
3. **Lint:** new/modified Python files compile — `python -m py_compile <each new .py>`; CSS uses only `var(--tokens)` (no hardcoded colors); no console errors in any E2E run.
4. **Commit:** one commit per task, message as specified, staged files limited to the task's `Files` list (claims protocol: `workspace/claims/` not needed for UI tasks — single-owner linear execution).

## 5. Execution handoff

Subagent-driven execution (per `docs/plan.md` Execution Handoff): L0 orchestrator dispatches one fresh subagent per task **in order T1 → T17** (hard dependency chain: infra → tokens → shell → nav → data contract → screens → a11y → CI). Each subagent: read this plan's task block, `docs/plan-ui.md` §2 commands, `ui/explorations/instrument/brief.md` (visual/a11y reference), write the failing test first, run it red, implement, run green, commit with the given message, report result to L0. Human gates: after **T2** (token freeze — review `tokens.css` + `token-pairs.json` + contrast output) and after **T16** (full screen sweep, render review in browser before T17). No parallel tasks — every task mutates shared files (`index.html`, `main.js`, screens/) and the fixture generator. On CI failure post-merge, the fix is a new PR against `docs/plan-ui.md`'s task scope, never a silent rewrite (AGENTS.md §6).
