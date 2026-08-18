# journey/ — committed conventions for the local journey layer

`.journey/` (in this repo root, gitignored) holds per-developer learning data.
This folder defines the CONVENTIONS so any tool or agent can interoperate.

## Contents

- `schema/*.schema.json` — JSON Schemas validating every journey artifact
  (profile, skill matrix, review queue, session, event line, project review, checkpoint)
- `examples/*` — fully synthetic, redacted examples that must always validate
- `templates/` — session/checkpoint templates (added in Phase 4)
- `privacy.md` — privacy defaults and opt-in sharing rules (added in Phase 4)

## Rules for agents

- Append one JSON object per line to `.journey/logs/YYYY-MM-DD-<topic>.jsonl`
- Every line validates against `schema/event.schema.json`
- Never log raw conversation text; only structured events
- Never touch another user's journey data
- Ask the human for consent before writing anything

## Examples (CI-validated)

`examples/` is part of CI: `tools/lint.py` validates every example against its schema.
Keep them synthetic and free of real personal data — this repo is public.

## Known contracts & gaps (2026-08-18, from UI spec authoring)

- **Verdict vocabulary is intentionally split:** claims use `correct|partial|incorrect`
  (spec §8.2); checkpoints and project reviews use `pass|partial|fail` (their own schemas).
  UI must not assume one vocabulary across event types.
- **Record locations:** checkpoints and project reviews are stored under
  `.journey/records/checkpoints/` and `.journey/records/reviews/` (JSON per
  `checkpoint.schema.json` / `project-review.schema.json`), NOT in the event log.
- **Event payload shapes** (`payload` in `event.schema.json`) are currently unconstrained
  objects; the de-facto shapes are defined by `examples/session.example.jsonl` and
  rendered verbatim by the UI. Tightening per-type payload constraints is a Phase 4 task.
- **Streak / last-activity** are derived, not stored: from `session.completed` timestamps.
- **Calibration state** contract: `journey/schema/calibration.schema.json`
  (`.journey/state/calibration.json`).
