# AI features

Use when evaluating, scoping, or reviewing a feature built on machine learning or generative AI,
including "we need AI" requests. Pair with the feature-challenge reference when the AI feature
arrives ready-made.

## 1. Start from the job, not the model

- Which user decision or workflow gets better, for whom, and compared with what they do today?
- What is the value of automation here: time saved, quality, coverage, new capability, or cost?
- Establish a **non-AI baseline:** rules, templates, search, better defaults, or a human
  service. If the baseline gets most of the value, prefer it; it is cheaper, predictable, and
  easier to support.
- "Precisamos de IA" is a technology choice, not a problem. Walk it up the request ladder in the
  feature-challenge reference.

## 2. Classify the error tolerance

The most important product question for AI is what happens when it is wrong.

| Pattern | Error cost | Typical design |
| --- | --- | --- |
| **Suggest** (draft, autocomplete, recommendations) | Low; the user reviews | Easy to edit, easy to ignore, show sources |
| **Assist with review** (summaries, classification for triage) | Medium; errors can mislead | Confidence cues, citations, sampling for quality, easy correction |
| **Act autonomously** (send, approve, change data, decide) | High; errors reach customers or money | Narrow scope, thresholds, human approval above risk limits, audit trail, undo |
| **Regulated or safety-critical** (health, credit, legal, hiring) | Severe; legal and ethical exposure | Legal review, explainability, bias evaluation, human accountability |

Move from suggest to autonomous only with evidence from production quality data.

## 3. Feasibility questions that decide the plan

- **Data:** does the needed data exist, is it accessible, clean, labeled, and permitted for this
  use? Customer data rights and contracts often block use for training or even for prompts.
- **Quality bar:** what accuracy, or what rate of severe errors, makes the feature useful? Agree
  it with users and stakeholders before building.
- **Evaluation set:** a representative set of real cases with expected outputs or grading
  criteria, including hard and adversarial cases. Without it, quality is an opinion.
- **Latency and cost:** cost per request and response time at expected volume; whether unit
  economics work for the pricing plan.
- **Model change risk:** vendor models change and are deprecated; plan regression evaluation
  and version pinning.
- **Privacy and security:** personal data, data residency, prompt injection, data leakage
  between customers, and retention by vendors.

## 4. Demo versus production

Demos succeed on chosen examples; production meets the long tail. Before committing:

- run the evaluation set, not hand-picked examples;
- test with real users on real data in a limited beta;
- measure severe-error rate, not only average quality;
- check behavior on empty, ambiguous, multilingual, and malicious inputs;
- plan observability: logging inputs and outputs within privacy limits, user feedback capture,
  and quality sampling.

## 5. UX principles

- Set expectations: make clear what the AI does and that it can be wrong.
- Keep the human in control where errors matter: preview, edit, approve, undo.
- Show provenance: sources, citations, or the data used.
- Design the failure path: what the user sees when the model is unsure or fails.
- Capture feedback in the flow (accept, edit, reject) and use it as a quality signal.

## 6. Measuring success

- **Task success:** the job got done better or faster than the baseline, measured on the
  outcome, not on usage of the AI button.
- **Quality:** acceptance rate, edit distance or edit rate, severe-error rate from sampling,
  escalation rate.
- **Adoption and retention:** repeated use by the target users, not novelty spikes.
- **Economics:** cost per successful task against the value or price.
- **Guardrails:** complaints, support contacts, trust signals, incidents, policy violations.

Novelty inflates early usage of AI features; read retention over several weeks before
concluding.

## 7. Rollout

Internal dogfooding → design partners or a small beta with explicit success criteria → staged
rollout with monitoring and a kill switch → general availability with ongoing evaluation.

## Context notes

- **B2B:** Customers' security and legal teams will ask about data use, training, retention,
  sub-processors, and residency; readiness here often decides adoption more than quality.
- **B2C:** Scale magnifies rare failures and reputational risk; moderation and abuse handling
  matter.
- **Internal tools:** Lower reputational risk and a good place to learn, but errors still affect
  decisions; keep human review where outcomes matter.

## Anti-patterns

- Choosing the technology before the problem.
- Judging quality from a demo.
- No evaluation set, or one that does not represent production.
- Autonomous actions without undo, thresholds, or audit.
- Measuring AI usage instead of the outcome.
- Ignoring cost per request until the bill arrives.
- Inventing accuracy figures; when unknown, say what must be measured.

## Output

Lead with the recommendation: build, test first, use a non-AI baseline, narrow the scope, or not
now. Then give the job and baseline, the error-tolerance pattern, feasibility unknowns, the
quality bar and evaluation plan, the UX safeguards, success and guardrail measures, and the
rollout stages.
