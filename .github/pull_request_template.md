# Thank you for contributing to Strata

Before submitting, please verify (CI will check these too — this checklist is for you):

## Content correctness
- [ ] Every claim line carries **exactly one** tier tag (`[T0]`–`[T4]`) and at least one
      `[S-####]` evidence record on the same line
- [ ] Every cited record exists in `evidence/records/` and lists this topic in its
      `claims-supported`
- [ ] All citations are real and web-verified; nothing is fabricated (see
      `evidence/hierarchy.md`)
- [ ] Topic tier = strongest claim tier (spec §6.3); T4 content is dated with
      `review_after`

## Validation & teaching packs
- [ ] `validation.md`: ≥6 items, ≥3 Bloom levels including `bloom_target`, canonical
      anatomy (`- Q: / - bloom: / - bank: / - A: / - evidence: / - topic:`)
- [ ] `teaching.md`: ≥1 worked example, ≥3 misconceptions, Feynman targets

## Gates (must be green)
- [ ] `python tools/lint.py` — no errors
- [ ] `python tools/check-graph.py` — no cycles, no missing prerequisites
- [ ] `python tools/index.py && python tools/coverage.py` — then commit regenerated files

## Scope
- [ ] Only the topic folders, records, and generated files you were assigned were touched
- [ ] `.journey/` (private learner data) was not modified

## Summary
Describe what you added/changed, which records you created (S-####), and anything you
could not verify (mark it `UNVERIFIED` rather than omitting it).
