# Frameworks

Frameworks are tools, not answers. Use one only when it improves the decision, explain why it
fits, apply it to the user's real context, and say when it would mislead. When the user asks for
a framework, check whether it suits the problem and propose a better fit if not.

## Choose by question

| The question is… | Consider | Avoid |
| --- | --- | --- |
| Which of many similar items first? | RICE/ICE, Cost of Delay | MoSCoW |
| Which strategic bet? | Strategy as choices, kernel of strategy, 7 Powers | Scoring models |
| What problem to solve for whom? | Jobs to be Done, Opportunity Solution Tree | Personas without research |
| What to test before building? | Four product risks, assumption mapping | Business Model Canvas as evidence |
| How to scope a first version? | Story mapping, appetite (Shape Up), MoSCoW | RICE |
| Which metrics? | North Star with inputs, HEART, AARRR | Vanity dashboards |
| How much rigor for this decision? | One-way and two-way doors, pre-mortem | Full process for everything |
| How to communicate a roadmap? | Now-Next-Later, outcome roadmaps | Date-driven feature lists with false certainty |
| Which features delight versus are expected? | Kano, with real survey data | Desk-only Kano |

## Prioritization

**RICE** (Reach × Impact × Confidence ÷ Effort, popularized by Intercom) and **ICE** (Impact,
Confidence, Ease).

- Fits: comparing many items of similar kind and size, making assumptions explicit, and
  depersonalizing debates.
- How to use well: define Reach with a real source and period; use a small fixed Impact scale;
  make Confidence honest and justified by the evidence grade; estimate Effort with the team.
  Show the inputs, not only the score, and test whether the ranking flips under plausible
  ranges.
- Misleads when: inputs are guesses dressed as data, items differ in kind (strategic bet versus
  bug fix), or the score replaces strategy. Two items within the uncertainty of the inputs are
  tied.

**Cost of Delay and WSJF** (Don Reinertsen; WSJF is used in SAFe).

- Fits: when timing changes value: deadlines, seasonal windows, competitive moves, compounding
  costs, or risk reduction.
- How to use well: describe how value decays over time (urgency profile), then divide by
  duration so short, urgent items rise.
- Misleads when: value over time is invented, or every item is called urgent.

**MoSCoW** (Must, Should, Could, Won't).

- Fits: negotiating scope inside a fixed release or timebox.
- Misleads when: used to choose between opportunities; everything becomes Must.

**Kano** (Noriaki Kano).

- Fits: separating basic expectations, performance attributes, and delighters, using a Kano
  questionnaire with real customers.
- Misleads when: done as a desk exercise; categories also shift over time as delighters become
  expected.

**Opportunity cost and strategic fit** usually matter more than any score. Always state what is
not being done.

## Discovery and customer understanding

**Jobs to be Done** (Clayton Christensen; Bob Moesta and others for the switch interview).

- Fits: describing the progress a customer seeks in a situation, independent of the solution;
  finding non-obvious competitors; understanding switching (push of the current situation, pull
  of the new, anxiety, habit).
- How to use well: base jobs on interviews about real past switches or purchases; write them as
  situation, motivation, and expected outcome.
- Misleads when: jobs are invented at a desk or so abstract ("ser mais produtivo") that they
  exclude nothing.

**Opportunity Solution Tree** (Teresa Torres, *Continuous Discovery Habits*).

- Fits: connecting a desired outcome to customer opportunities (needs, pains, desires), then to
  several candidate solutions, then to assumption tests; prevents jumping to one solution.
- How to use well: start from one outcome the team owns; source opportunities from research;
  compare at least three solutions per chosen opportunity.
- Misleads when: the tree is filled once and never updated, or opportunities are solutions in
  disguise.

**Four product risks** (Marty Cagan): value, usability, feasibility, and business viability.

- Fits: checking which risk dominates before choosing a discovery method. See the discovery
  reference.

**Assumption mapping** (popularized by David Bland and Alex Osterwalder, *Testing Business
Ideas*).

- Fits: plotting assumptions by importance and evidence, then testing the important ones with
  the least evidence first.
- Misleads when: assumptions are generic or the map is not followed by tests.

**Personas.**

- Fits: only when grounded in research and tied to decisions, such as which segment to design
  for.
- Misleads when: fictional, demographic, or decorative; they add false confidence.

## Strategy

**Strategy as choices** (A.G. Lafley and Roger Martin, *Playing to Win*): winning aspiration,
where to play, how to win, required capabilities, management systems.

- Fits: testing whether a strategy makes real choices and says what the company will not do.

**The kernel of strategy** (Richard Rumelt, *Good Strategy Bad Strategy*): diagnosis, guiding
policy, coherent actions.

- Fits: reviewing a strategy document. Bad strategy signs Rumelt names include fluff, failure
  to face the challenge, mistaking goals for strategy, and bad strategic objectives.

**7 Powers** (Hamilton Helmer): scale economies, network economies, counter-positioning,
switching costs, branding, cornered resource, process power.

- Fits: asking what durable advantage a bet builds, beyond being better today.
- Misleads when: used to justify an early-stage product that has not yet found fit.

**Business Model Canvas / Lean Canvas** (Alex Osterwalder; Ash Maurya).

- Fits: making a business model's assumptions visible on one page.
- Misleads when: a filled canvas is treated as evidence that the model works.

**Five Forces** (Michael Porter) and **SWOT.**

- Fits: structured market context and industry attractiveness.
- Misleads when: SWOT becomes an unprioritized list with no choice attached.

## Scoping and planning

**User story mapping** (Jeff Patton): arrange the user journey horizontally and detail
vertically, then slice releases across the whole journey.

- Fits: finding a thin first version that delivers an end-to-end outcome.

**Appetite** (Basecamp's *Shape Up*): decide how much time a problem deserves, then shape a
solution that fits, instead of estimating a fixed solution.

- Fits: avoiding scope creep and matching investment to value.

**Now-Next-Later roadmaps** (popularized by Janna Bastow) and outcome-based roadmaps.

- Fits: communicating priorities with honest uncertainty; near-term items are specific, later
  items are problems or outcomes.
- Misleads when: "Later" becomes a polite graveyard with no review.

## Decision quality

**One-way and two-way doors** (from Jeff Bezos's shareholder letters).

- Fits: matching process weight to reversibility. Two-way doors deserve fast decisions by small
  groups; one-way doors deserve deliberate analysis.

**Pre-mortem** (Gary Klein): imagine the decision failed and list why.

- Fits: surfacing risks people hesitate to voice, before committing.

**Decision memo or narrative** (for example, Amazon-style written narratives).

- Fits: complex or contested decisions; forces explicit reasoning, options, and trade-offs.

## Metrics and growth

**North Star metric with input metrics** (popularized by Amplitude and Sean Ellis).

- Fits: aligning teams on a value-indicating behavior and the levers that drive it.
- Misleads when: the North Star is revenue alone, or lacks guardrails against gaming.

**AARRR** (Dave McClure): acquisition, activation, retention, referral, revenue.

- Fits: a funnel checklist for growth.
- Misleads when: it hides that retention drives the rest; fixing acquisition into a leaky
  product burns money.

**HEART** (Google: happiness, engagement, adoption, retention, task success) with **Goals,
Signals, Metrics.**

- Fits: choosing user-experience metrics for a specific feature or product area.

**Growth loops** (popularized by Reforge): self-reinforcing cycles where output of one cycle
becomes input to the next, such as user-generated content attracting new users.

- Fits: explaining compounding growth better than a linear funnel.

## How to apply

1. State the decision the framework serves.
2. Explain why this framework fits better than alternatives for this question.
3. Apply it to the user's actual context, marking every input that is an assumption.
4. Check sensitivity: would plausible changes in inputs change the conclusion?
5. Give the conclusion in plain language, plus what the framework cannot capture.

Do not present a filled template as analysis. If the user's question would be better answered
without a framework, say so and answer directly.
