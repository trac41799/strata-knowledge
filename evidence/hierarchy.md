# Evidence Hierarchy — how claims are graded

Reference: `docs/spec.md` §4.3 · `PRINCIPLES.md` K1 (confidence is attached, never implied).

## The 8 levels (method-based, GRADE-style)

| Level | Type | Examples |
|---|---|---|
| 1 | Formal proof / mathematical derivation | Halting problem undecidability; serializability theory; CAP impossibility |
| 2 | Meta-analysis / systematic review | Cepeda et al. (2006) spacing; Dunlosky et al. (2013) learning techniques |
| 3 | Randomized controlled experiment | Roediger & Karpicke (2006) test-enhanced learning; Rohrer & Taylor (2007) interleaving |
| 4 | Quasi-experiment / controlled study | Chi et al. (1994) self-explanation; Sweller & Cooper (1985) worked examples |
| 5 | Large-N observational / industrial dataset | Defect-density studies; DORA/State of DevOps reports |
| 6 | Codified consensus standard | SWEBOK v4.0; CS2023; ISO/IEC 25010:2023; ISO/IEC/IEEE 12207:2017; RFC 9111; CMMI V3.0 |
| 7 | Practitioner literature / widely adopted patterns | SOLID; 12-factor; Dreyfus model; Ericsson (1993) |
| 8 | Anecdote / blog / unreplicated claim | — |

## Mapping to tiers

- **T0** (formal) ← level 1
- **T1** (strong empirical) ← levels 2–5
- **T2** (codified consensus) ← level 6
- **T3** (established practice) ← level 7
- **T4** (frontier, volatile) ← any underlying level that is NOT yet consensus/current; always dated, always carries `review_after`
- **UNVERIFIED** — not a tier: a state. Claims without records must not be published (K1).

## Rules

- Tier assignment is made by L2 (Evidence & Fact-Check) agents, never by authors.
- A claim citing multiple records takes the strongest applicable level for its tier.
- Standards claims cite the specific clause/section where possible (`standard` field in the record).
- `hierarchy-level` is stored on every record in `evidence/records/` and enforced by `tools/schemas/evidence.schema.json`.
- An evidence record may support multiple topics (`claims-supported`), but a claim may never reference a record that does not exist (`tools/lint.py` enforces the bijection).
