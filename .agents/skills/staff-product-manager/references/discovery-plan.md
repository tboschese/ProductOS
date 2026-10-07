# Planning a discovery

Use when the user is unsure what to investigate, how, or whether discovery is needed at all.
Discovery exists to change a decision. A plan that would not change any decision is waste,
however rigorous it looks.

## 1. Decide whether to do discovery

Skip or shrink discovery when:

- the decision is cheap and reversible, such as a flagged UI change: ship, measure, and learn;
- the answer is already known with good evidence and nobody disputes it;
- no result would change the action, for example a regulatory obligation or a committed
  contract; discover the minimum scope instead;
- the team cannot act on the result in a useful time frame.

Invest more when the decision is expensive, hard to reverse, public, affects pricing or
contracts, or commits a team for a quarter or longer.

## 2. Frame the decision

Write one sentence before choosing any method:

> "Precisamos decidir **[X]** até **[data]**. Hoje tendemos a **[Y]**. Mudaríamos de ideia se
> descobríssemos **[Z]**."

If the user cannot fill Z, there is no discovery question yet; help them find it. Typical
decisions: which problem to prioritize, which segment to serve, whether a solution direction
works, whether people will pay, how to scope a first version.

## 3. Separate what is known

Sort the user's inputs into facts with sources, observations, interpretations, assumptions,
stakeholder opinions, and unknowns. Check cheap sources before new research: product analytics,
support tickets, sales and churn notes, NPS or survey verbatims, past research, CRM loss
reasons, app store reviews, and community forums. Many discovery questions are partly answered
by data the company already has.

## 4. Find the dominant uncertainty

Classify the unknowns, then pick the one or two most likely to change the decision.

| Risk | Question | Typical signal that it dominates |
| --- | --- | --- |
| **Problem / value** | Does the problem exist, matter, and for whom? | New area, no usage data, conflicting stakeholder beliefs. |
| **Usability** | Can people figure out and complete the job with this solution? | Problem is known; solution is new or complex. |
| **Feasibility** | Can we build and run it at acceptable cost, performance, and risk? | New technology, data quality, AI accuracy, integrations. |
| **Viability** | Does it work for the business: pricing, margin, legal, sales, support, brand? | Monetization, regulated domains, channel conflict. |
| **Market / go-to-market** | Can we reach the segment and win against its current alternative? | New segment, new buyer, crowded category. |

Problem-space uncertainty comes before solution-space uncertainty. Testing a prototype for a
problem nobody has produces confident, useless usability findings.

## 5. Write competing hypotheses

List three to five credible explanations or bets, including the uncomfortable one (often "the
problem is small" or "it is our onboarding, not the feature"). For each, write what it predicts
you would observe. A method is useful only if it can tell the hypotheses apart.

## 6. Choose the smallest sufficient method

| Method | Answers well | Cannot answer | Cost | Common mistake |
| --- | --- | --- | --- | --- |
| Existing data analysis | Who does what, how often, where they drop | Why they do it | Low | Treating correlation as cause |
| Support, sales, churn notes | Recurring pains, words customers use | Prevalence across the base | Low | Counting tickets from a few loud accounts |
| Problem interviews | Context, workarounds, motivations, past behavior | Prevalence; future behavior | Medium | Pitching the idea; asking hypotheticals |
| Contextual observation | Real workflow, unspoken workarounds | Prevalence | Medium-high | Too few sessions across segments |
| Survey | Prevalence of known patterns, segmentation | Discovery of unknown problems | Low-medium | Leading questions; surveying before interviews |
| Prototype usability test | Whether people can complete the task | Whether they want it | Medium | Testing value with a usability test |
| Fake door / painted door | Intent to use, at scale | Retained use | Low | Ignoring the trust cost; no follow-up message |
| Concierge / Wizard of Oz | Value of the outcome before building | Scalability, cost at scale | Medium | Running it too long without a decision rule |
| Pre-sale, LOI, paid pilot (B2B) | Willingness to commit money or effort | Long-term retention | Medium | Accepting a verbal "yes" as commitment |
| Technical spike | Feasibility, performance, data quality | User value | Medium | Spike that turns into the build |
| A/B experiment | Causal effect on behavior | Why; effects below detectable size | Medium-high | Underpowered tests in low-traffic products |

Pick by the dominant uncertainty and by what would discriminate between the hypotheses, not by
habit. Combine a qualitative method (why) with a quantitative one (how many) when both matter.

## 7. Choose who and how many

- **Recruit by behavior, not demographics:** "gerentes que fecharam o mês na ferramenta nos
  últimos 30 dias", not "gerentes de 30 a 45 anos".
- **Include the uncomfortable groups:** churned customers, trial users who never activated,
  lost deals, non-adopters of the feature, and competitors' customers.
- **B2B roles:** buyer, champion, end user, admin, and blocker (security, procurement) often
  want different things. Talk to the roles the decision depends on.
- **Marketplace:** both sides, because a change for one side affects the other.
- **Internal platform:** the engineers or operators who actually use it, not only their
  managers.
- **How many:** for qualitative work, sample per segment and stop when new sessions stop
  changing your understanding. Usability testing commonly uses small rounds of about five users
  per distinct user type, repeated after fixes; treat this as a practitioner heuristic, not a
  statistical rule. Quantitative claims need quantitative samples.

## 8. Write questions about the past

Interviews should collect facts about past behavior, not opinions about the idea. The principles
popularized by Rob Fitzpatrick's *The Mom Test* apply: talk about their life, ask about specific
past events, and listen more than you speak.

Weak question → better question:

- "Você usaria uma funcionalidade de X?" → "Me conta a última vez que você precisou fazer X. O que
  aconteceu?"
- "Isso é um problema para você?" → "Quanto tempo isso tomou na última semana? O que você fez para
  contornar?"
- "Quanto você pagaria por isso?" → "Vocês já pagam por algo para resolver isso hoje? Quanto e por
  quê?"
- "Você gostou do protótipo?" → "Tenta fazer [tarefa] aqui e vai falando o que está pensando."

Question bank for problem interviews:

1. "Me conta a última vez que você [fez a tarefa]. Desde o começo."
2. "O que te levou a fazer isso naquele momento?"
3. "Qual foi a parte mais difícil ou chata?"
4. "O que você usa hoje para isso? Já tentou outra coisa? Por que trocou ou desistiu?"
5. "O que acontece quando isso dá errado? Quem percebe?"
6. "Quanto tempo ou dinheiro isso custa por semana ou mês?"
7. "Se você tivesse uma varinha mágica, o que mudaria nesse processo?" (use only at the end;
   treat answers as hints, not requirements)
8. "Quem mais na empresa se envolve nisso?" (B2B: maps roles and the buying process)

Commitment signals are stronger than compliments: the person gives time for a follow-up, intros
to colleagues, shares real data, joins a pilot, or pays.

## 9. Set the decision rule and stop criteria before collecting

Examples:

- "Se pelo menos 6 de 10 contas entrevistadas descreverem o problema sem a gente sugerir, e
  tiverem workaround que custa tempo semanal, seguimos para protótipo. Se menos de 3, paramos."
- "Se o fake door tiver taxa de clique comparável à das features mais usadas da mesma tela,
  investimos no MVP; se for próxima de zero, arquivamos."
- "Timebox de duas semanas. Se as hipóteses ainda estiverem empatadas, decidimos pela opção mais
  reversível."

The thresholds are judgment calls; state them as such, agree them with stakeholders upfront, and
do not move them after seeing the data.

## 10. Synthesize toward the decision

- Map each finding to the hypotheses it supports or weakens.
- Distinguish frequency (how many said it) from intensity (how much it costs them) and from
  representativeness (who they are).
- Keep contradictory evidence visible; do not average it away.
- End with the decision, the confidence, and what remains unknown.

## Context notes

- **Early stage:** Focus on problem existence, the segment that feels it most, and willingness
  to commit. Founder-led interviews and concierge delivery are cheap and informative.
- **Growth:** Focus on segments, activation, and the gap between who signs up and who stays.
  Data is available; combine it with interviews of retained and churned users.
- **Mature:** Problems are incremental and data-rich. Prefer analysis and experiments for
  optimization, and reserve interviews for new segments or unexplained behavior.
- **B2B with few customers:** Experiments are rarely powered. Use design partners, pilots with
  explicit success criteria, and contractual commitment as evidence.
- **Internal platform:** Observe migrations and support requests; measure time-to-first-use and
  abandonment of the paved road.

## Anti-patterns

- **Validation theater:** seeking confirmation for a decision already made.
- **Leading questions and pitching** during interviews.
- **Hypotheticals:** treating "I would use it" as evidence.
- **Only friendly customers or power users** in the sample.
- **Survey first:** quantifying problems before understanding them.
- **No decision rule:** every result gets interpreted as support.
- **Synthesis by vote:** counting sticky notes instead of weighing evidence.
- **Endless discovery:** no timebox, no stop criteria.

## Worked example

Situation: SMB churn rose over the last two quarters; the PM does not know what to investigate.

- Decision: whether next quarter's roadmap targets onboarding, a product gap, or pricing for SMB.
- Known: churn rate by month (fact, from billing); CS believes "price" is the cause (opinion);
  no exit survey data.
- Hypotheses: (a) new SMB cohorts never activate, so onboarding; (b) a competitor launched a
  cheaper plan, so pricing; (c) a recent release broke a core workflow; (d) acquisition shifted
  to a lower-fit channel, so mix shift.
- What each predicts: (a) churn concentrated in recent cohorts with low early usage; (b) churn
  across tenures, loss reasons citing price or the competitor; (c) churn after the release date
  among users of that workflow; (d) churn concentrated in accounts from the new channel.
- Plan: first, one to two days of cohort and channel analysis to discriminate (a), (c), and (d)
  cheaply; then eight to ten interviews with churned accounts from the segment the data points
  to, plus a review of CS notes for (b).
- Decision rule: the hypothesis supported by both the cut and the interviews drives the roadmap
  proposal; if data and interviews disagree, run a focused follow-up before committing.

## Output

Lead with the recommended next step in one or two sentences. Then give:

- the decision sentence and the dominant uncertainty;
- hypotheses and what each predicts;
- the plan: method, participants or data, recruitment, duration, and owner, sized to the stakes;
- for interviews, five to eight questions about past behavior, in the user's language;
- the decision rule and stop criteria;
- what the plan cannot answer.

Avoid generic discovery checklists, persona templates, and framework names unless they change
what the user should do.
