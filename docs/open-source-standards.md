# Open-Source Project Standards — ruleset for READMEs & community files

> Source: GitHub official documentation (docs.github.com), opensource.guide, and
> structural conventions distilled from high-star repositories (vuejs/core, vercel/next.js,
> posthog, httpie, htmlhint, redoc, colorls) plus README-guidance literature
> (freeCodeCamp, banesullivan/README, daily.dev badge guidance, matiassingers/awesome-readme).
> Status: canonical ruleset for Strata; mirrored in the opencode skill
> `open-source-repo-standards` for reuse on any repository.

## 0. Principles (why these rules exist)

1. **The README is the front door.** GitHub says a README should answer: what the project
   does, why it is useful, how to get started, where to get help, who maintains/contributes.
   If those five answers are not scannable in 30 seconds, the README failed.
2. **First impressions are visual.** Top repos lead with a name + tagline + 2-4 badges
   above the fold; screenshots/demo GIFs beat prose for user-facing projects.
3. **Expectations are community files.** GitHub's own guidance: README + license +
   citation + contribution guidelines + code of conduct "communicate expectations and help
   you manage contributions". These are not optional for a healthy public repo.
4. **Structure is a contract.** Consistent section order lowers the cost of scanning;
   high-star repos converge on the same skeleton (see §2).
5. **Badges are a budget.** daily.dev: keep 2-4 meaningful badges at top, consistent style
   (shields.io), accurate and maintained; bury or drop the rest.
6. **Users first, contributors second.** Baně Sullivan's rule: the average user should not
   hit build instructions; put user value (features, quickstart, docs) before dev/contrib
   content.
7. **Links must survive clones.** GitHub recommends relative links for in-repo files;
   absolute URLs only for external resources.

## 1. README anatomy (ordered)

| # | Section | Required | Notes |
|---|---|---|---|
| 1 | Title (H1) + one-line tagline | yes | Name the project; tagline = what it is in ≤12 words |
| 2 | Badge row | yes (2-4) | license, CI status, stars/downloads, issues; same style (shields.io) |
| 3 | Hero/intro paragraph | yes | What + why + who it's for, in 2-4 sentences; screenshots/demo for UI projects |
| 4 | Table of contents | long READMEs only | GitHub auto-generates an outline; manual TOC optional |
| 5 | Features | yes | 3-7 bullets; what makes it different |
| 6 | Quickstart / Getting started | yes | Exact copy-paste commands; clone → install → run; demo/screenshots |
| 7 | Usage / examples | yes | Real usage, not hypotheticals |
| 8 | Documentation links | yes | Docs site / deeper guides (don't stuff everything into README) |
| 9 | Structure / architecture (optional) | for complex repos | Repo tree or layer diagram |
| 10 | Status / roadmap / FAQ | recommended | Project health, maturity, known limitations |
| 11 | Contributing | yes | Link to CONTRIBUTING.md; PRs-welcome signal |
| 12 | License | yes | License name + link; copyright line (e.g., "Copyright (c) 2026 …") |
| 13 | Acknowledgments / sponsors | recommended | Credits, standards bodies, backers |

**Rules:** keep under 500 KiB (GitHub truncates); use relative links for repo files; alt
text on images; link text on a single line; put README in root (or `.github/`/`docs/` —
GitHub surfaces it).

## 2. Badge rules

- 2-4 badges, all shields.io (or one consistent style), placed directly under the H1.
- Always include: **license** + **CI/build status**.
- Include for popularity: stars, downloads (npm/pypi), contributors.
- One optional: "PRs welcome", OpenSSF scorecard.
- Never: broken/dead badges, more than 6, unmaintained custom endpoints.

## 3. Community files (the "official" set)

| File | Purpose | Source |
|---|---|---|
| `LICENSE` (root) | Full license text; determines reuse legality | choosealicense.com; SPDX identifiers |
| `CONTRIBUTING.md` | How to contribute: setup, branch/PR flow, conventions, review expectations | GitHub "Setting guidelines for repository contributors" |
| `CODE_OF_CONDUCT.md` | Behavior expectations; use Contributor Covenant 2.1 | contributor-covenant.org |
| `SECURITY.md` | How to report vulnerabilities; supported versions | GitHub security guidance |
| `CHANGELOG.md` | User-visible changes; keep-it-human (Keep a Changelog) | keepachangelog.com |
| `CITATION.cff` | How to cite the project (software/repo) | GitHub citation guidance |
| `.github/pull_request_template.md` | PR checklist driving review quality | GitHub templates docs |
| `.github/ISSUE_TEMPLATE/` | Bug/feature templates (use GitHub's form schema) | GitHub templates docs |

Notes: a repo with no license is "all rights reserved" by default — the single most
common viral-repo failure. Mixed-content repos (docs + code) use two files
(`LICENSE` + `LICENSE-CODE`) and say so in the README.

## 4. GitHub settings (repo-level)

- **Description** (≤350 chars): what it does + who it's for.
- **Topics** (≤20): discoverability keywords (e.g., knowledge-base, agent, cli).
- **Discussions**: enable for Q&A in mature repos (vue pattern: issues exclusively for
  bugs/features; questions go to forum/discussions).
- **Default branch** named `main`; branch protection for direct pushes.
- **Release** tags for milestones (semver).
- **Social preview** image (1280×640) shown on shares — high-star repos have one.

## 5. Writing quality

- Present tense, imperative for instructions ("Clone the repo…").
- Copy-paste-ready commands; no placeholder-y docs.
- Screenshots with alt text; demos as GIF/asciinema for UI projects.
- Every claim in README must be true *today* (badges auto-update; prose doesn't — audit
  on every release).
- Respect the repo's own conventions (Strata: PRINCIPLES.md axioms, AGENTS.md contract,
  CI gates — README must not contradict them).

## 6. Verification checklist (run before commit)

- [ ] H1 + tagline + 2-4 badges exist and render
- [ ] The five GitHub questions answered (what/why/started/help/maintainers)
- [ ] Quickstart has exact commands
- [ ] All links resolve; in-repo links are relative
- [ ] Images have alt text; total size < 500 KiB
- [ ] LICENSE (+ LICENSE-CODE for mixed repos) present with full text
- [ ] CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CHANGELOG, CITATION.cff present
- [ ] PR template present
- [ ] Repo description + topics set; default branch `main`
- [ ] README reviewed against this ruleset §1 table

## 7. House style (trac41799 repositories — see github.com/trac41799/source-forge)

The user's established repos follow a consistent house style on top of the ruleset.
Apply it when fixing this user's repositories:

- **Centered masthead**: project name (H1, centered) + bold one-line tagline (centered) +
  a single row of `?style=flat-square` shields.io badges.
- **Emoji-prefixed section headings**, in this order:
  `✨ Overview` → `🚀 Features` → (domain-specific: `🧩 Supported Agents` /
  `📦 Installation`) → `⚡ Quick Start` → `🏗️ Architecture` → `💻 Development` →
  `🤝 Contributing` → `🗺️ Roadmap` → `📄 License`.
- **Features as a 3-column table**, one emoji-headed cell per feature (width 33% each).
- **Quick Start as numbered steps** (`# 1. …` / `# 2. …`), imperative, one action per step.
- **Contributing** = short section linking the community/contributing docs; **Roadmap** =
  honest status; **License** = name + link + copyright line.
- Badges use `?style=flat-square`, including static stack/platform badges
  (e.g., `stack-Rust_%7C_React_%7C_SQLite`).
- Localization links row (`English · 中文 · Tiếng Việt`) for user-facing apps; skip when
  the repo is English-only by decision.
