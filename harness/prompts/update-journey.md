# Update My Journey

**Purpose:** reconcile journey state (skill matrix, review queue, calibration) after a session.
**AGENTS.md clauses activated:** §4, §7.

## Prompt

```
Update my journey per AGENTS.md §4/§7 after today's session on <topic id>:
1. Append any missing events to .journey/logs/ per journey/schema/event.schema.json
2. Reconcile state/skill-matrix.json (level, score, validated) and state/review-queue.json (next due date per the ladder)
3. Record calibration: I predicted <N>% before the quiz, I scored <M>%
Ask before writing; then confirm each file validates against its schema.
```
