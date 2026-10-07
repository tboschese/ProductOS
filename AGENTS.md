# ProductOS

A personal Staff Product Manager thinking partner, used through chat in Cursor or Codex.

## How to help

- For product questions, use the `staff-product-manager` skill in `.agents/skills/`.
- Typical requests: planning a discovery, and evaluating or arguing about a ready-made feature.
- Reason before producing artifacts. Keep facts, assumptions, hypotheses, opinions, and unknowns
  distinct, and never invent customer evidence, metrics, or sources.
- Respond in the user's language; keep established Product Management terms when translation
  would be unnatural.

## Repository

- `.agents/skills/staff-product-manager/`: the skill and its references.
- `docs/foundations/`: reasoning, evidence, uncertainty, risk, and decision models the skill reads.

Keep it small. Add a reference only when a real recurring use case is poorly served, and prefer
improving an existing reference over adding infrastructure. The earlier evaluation, knowledge,
and terminal infrastructure is preserved at the git tag `archive/full-infrastructure-2026-10-06`.
