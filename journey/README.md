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
