# Security Policy

## Reporting a vulnerability

Strata is a knowledge base and agent harness. Report issues in:

- **Knowledge content** — malicious, fabricated, or misleading citations; broken evidence
  records; stale frontier claims.
- **Harness** — prompt-injection vectors in `harness/prompts/` or `AGENTS.md` instructions;
  anything that could make an agent take harmful actions on behalf of a user.
- **Tooling** — code execution issues in `tools/` or CI.

Do **not** open a public issue for anything that could be actively exploited. Instead,
email a private description to the maintainers via GitHub's security advisory flow
(Security → Report a vulnerability) — or, if the issue is content-only (a wrong claim,
a fake citation), a normal issue is fine and faster.

## Supported

| Component | Support |
|---|---|
| Knowledge content (published topics) | actively reviewed; stale T4 content expires via CI (`review_after`) |
| Tooling (`tools/`, CI) | maintained with the repo |
| Harness prompts | maintained with the repo |
| Unpublished scaffolds | no support |

## Disclosure

We ask for a 30-day embargo before public disclosure of a fixable issue, and we will
credit reporters in release notes unless anonymity is requested.
