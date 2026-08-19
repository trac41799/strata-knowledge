# Contributing to Strata

Strata is a knowledge commons for software engineering: an evidence-tiered knowledge
base plus an agent harness. All contributions go through the standard open-source
flow — **draft → CI → human review** — described below. Read
[`AGENTS.md`](AGENTS.md) (the harness contract) and [`PRINCIPLES.md`](PRINCIPLES.md)
(the axioms) before contributing; every rule in this repo derives from them.

## What we accept

- **Knowledge content** (the big one): new topic packs or corrections to existing ones —
  claims tagged `[Tier]` + `[S-####]` evidence records, validation items, teaching packs.
  Start from the coverage report (`docs/coverage-report.md`) — it is the roadmap.
- **Evidence records**: new `evidence/records/S-####.md` entries with verified citations.
- **Tooling**: improvements to `tools/*.py` (stdlib-only), CI, or the harness.
- **Docs & design**: spec, plan, ADRs, design system, UI.
- **Bug reports** for anything that is wrong, misleading, or stale.

## Ground rules (non-negotiable)

1. **Never fabricate citations.** A claim without a record must not be published; a record
   without a real source must not exist. `UNVERIFIED` is an honest state — use it.
2. **Tier discipline.** Topic tier = strongest claim tier (spec §6.3). One tier tag per
   claim line. T4 (frontier) content must be dated and volatile-flagged.
3. **Generated files are sacred.** `knowledge-graph.yml`, `INDEX.md`,
   `docs/coverage-report.md` are outputs of `tools/*.py` — never hand-edit; regenerate.
4. **Conventions are code.** Frontmatter, schemas, and item anatomy are CI-enforced.
   Run the gates before opening a PR:
   ```bash
   python tools/lint.py && python tools/check-graph.py && python tools/index.py && python tools/coverage.py
   ```
5. **Don't rewrite published content silently.** Corrections go through review like
   everything else.

## Workflow

1. **Find your gap**: pick a missing topic from the coverage report, or open an issue
   proposing a correction.
2. **Draft**: create the topic pack (use `python tools/new-topic.py --help` to scaffold)
   or edit the content. Tag every claim; cite real records; verify citations via web.
3. **Open a PR**: draft status, with a summary of what you added and which evidence
   records you created. PR template: `.github/pull_request_template.md`.
4. **CI runs**: schema, links, claim↔record bijection, graph acyclicity, staleness,
   determinism. Fix anything red.
5. **Review**: maintainers (or the L2 review process) check claim accuracy, provenance,
   tiers, and pedagogy. T0/T1 claims and standards mappings get the strictest look.
6. **Publish**: approval flips `status: published`; indexes regenerate.

## Agent contributors

If you are a coding agent contributing on behalf of a human: follow `AGENTS.md` §6 —
propose via PR, never silently rewrite, never invent events or citations, and leave
`.journey/` alone (it is the human's private data).

## Code of Conduct

All contributions are governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Be
precise, be kind, and assume good faith.

## Security

Found a vulnerability (e.g., a malicious citation, prompt-injection vector in the
harness)? See [SECURITY.md](SECURITY.md).
