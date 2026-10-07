# Evidence model

## Purpose

The evidence model prevents ProductOS from turning inputs, observations, and interpretations into stronger claims than they support.

## Evidence ledger

For a decision, ProductOS maintains an evidence ledger distinct from the long-lived knowledge base. Ledger items may come from the user, product data, research, market material, technical inspection, or explicit analysis.

Each item records:

- a stable ID within the decision record;
- the statement being considered;
- epistemic status;
- evidence modality;
- origin and any source locator;
- qualitative confidence;
- limitations and temporal relevance.

## Epistemic status

- `fact`: verified within an explicitly bounded context;
- `observation`: something recorded or measured without a causal interpretation;
- `interpretation`: a meaning inferred from observations;
- `assumption`: a proposition temporarily treated as true;
- `hypothesis`: a testable explanation or prediction;
- `opinion`: a judgment not presented as evidence;
- `recommendation`: a proposed action derived from reasoning;
- `unknown`: information material to the decision but not established.

Statuses can change only when new evidence justifies the transition. A repeated assumption does not become a fact.

## Evidence modality

Modalities are `quantitative`, `qualitative`, `market`, `business`, `technical`, `organizational`, `regulatory`, `mixed`, and `none`. Modality describes the evidence, not its quality.

## Origin

- `user_provided`: accepted as a statement from the user, not independently verified;
- `cited_source`: an identifiable external source with a precise locator;
- `tool_observation`: produced by a named analysis or inspection tool;
- `derived_analysis`: inferred from other ledger items;
- `unknown`: origin is unavailable and must remain explicit.

## Operating rules

1. Validate measurement and instrumentation before diagnosing a product change from a metric.
2. Preserve supporting and contradicting evidence separately.
3. State when evidence is stale, indirect, non-representative, or context-dependent.
4. Calibrate recommendations to the weakest material uncertainty, not the strongest available fact.
5. Do not fabricate a source, locator, customer quote, metric, or causal conclusion.
6. When citations are not available, identify the statement as user-provided, assumed, or unknown.
