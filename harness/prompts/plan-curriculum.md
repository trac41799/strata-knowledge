# Plan My Curriculum

**Purpose:** compute a corrective/learning path from current mastery to a target topic.
**AGENTS.md clauses activated:** §1, §2, §3, §7.

## Prompt

```
My current mastery is in .journey/state/skill-matrix.json. I want to reach <target topic id>.

Follow AGENTS.md: compute the shortest topological path in knowledge-graph.yml from my current topics to the target (include prerequisite gaps). For each hop, tell me: the topic, its band/tier/bloom_target, what to study (teaching.md), and the validation item I must pass to clear it. Order the plan by wave. Log the plan to my journey (ask first).
```
