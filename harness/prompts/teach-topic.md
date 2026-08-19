# Teach Me a Topic

**Purpose:** structured teaching of one topic at the learner's level.
**AGENTS.md clauses activated:** §1, §3 (teach), §4 (record), §7.

## Prompt

```
Teach me <topic id> at my level (see .journey/profile.json if present; else I self-assess as <novice|advanced-beginner|competent|proficient|expert>).

Follow AGENTS.md §3: honor the topic's bloom_target (<e.g. apply>); if I'm a novice, start with the worked example from teaching.md before any problem; use elaboration prompts; end the session with retrieval practice from validation.md (questions, not rereading); interleave my prerequisite topics (<list from knowledge-graph.yml>). Do not dump the whole pack into the chat — teach in a session structure with checkpoints. Log the session if I consent.
```
