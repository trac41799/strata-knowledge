# Audit the Knowledge

**Purpose:** repo-wide quality audit of knowledge content against the conventions.
**AGENTS.md clauses activated:** §5, §6.

## Prompt

```
Run the Strata quality gates and report: python tools/lint.py, tools/check-graph.py, tools/index.py, tools/coverage.py (explain exit codes); then audit docs/coverage-report.md for coverage gaps vs the standards maps; flag any published topic whose validation.md has fewer than 6 items or missing bloom_target coverage; flag stale T4 content (review_after passed). Do not modify files — report findings, propose PRs.
```
