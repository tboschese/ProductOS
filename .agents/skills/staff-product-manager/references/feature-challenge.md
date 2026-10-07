# Arguing about a ready-made feature

Use when the user receives a predefined feature or solution, from leadership, sales, a client,
or another team, and needs to evaluate it and argue a position. The goal is a better decision,
not winning or refusing. The feature may be right, and the requester often knows something the
PM does not.

## 1. Classify the request

The origin of a request predicts what is usually true and what is usually missing. Classify
first; it changes the questions.

| Origin | What is often true | What is often missing | Key question |
| --- | --- | --- | --- |
| Sales deal ("o cliente X fecha se tivermos") | Real revenue pressure, a real customer pain | Whether others share it, whether the deal truly depends on it | Is this a pattern across the pipeline or one account's preference? |
| Executive conviction | Context the PM lacks: board, strategy, market signal | The problem statement, the success measure | What outcome are you betting on, and what would make you drop it? |
| Competitor parity ("o concorrente lançou") | Visible gap in demos or RFPs | Evidence that the gap loses deals or causes churn | Where did we lose because of this, and to whom? |
| Customer success / churn save | Pain of a specific retained account | Whether the feature, rather than service or onboarding, prevents churn | What did churned or at-risk customers actually do before leaving? |
| Compliance or security | Non-negotiable deadline or contract term | Minimum scope that satisfies the requirement | What exactly does the rule require, and by when? |
| Internal stakeholder (ops, finance, support) | Operational cost that is real but invisible to customers | Sizing of the cost, cheaper process fixes | How many hours or errors per week does this cause today? |
| Technology trend ("precisamos de IA") | Strategic anxiety, sometimes a real opportunity | A customer problem the technology solves better than alternatives | Which job gets done better, for whom, compared with what they do now? |
| Customer feature request in volume | Many people mention it | Whether requesters are representative and what problem sits behind the request | What were they trying to do when they asked? |

Compliance and true contractual commitments are usually a scope question, not a whether
question. Say so instead of challenging the premise.

## 2. Reconstruct the intent: the request ladder

Walk the request up until it reaches something measurable:

1. **Solution asked:** "dashboards customizáveis".
2. **Need behind it:** "o cliente quer ver os dados do jeito dele".
3. **Problem:** "o gestor monta relatório manual no Excel toda semana para a diretoria".
4. **Outcome for the customer:** "reportar para a diretoria sem trabalho manual".
5. **Business outcome:** "fechar e renovar contas enterprise".

The rungs that the requester cannot fill are the evidence gaps. Lower rungs are often
negotiable; higher rungs are where alignment matters. Many disputes about a feature dissolve
once both sides agree on rung 3 or 4, because several solutions serve it.

## 3. Assumption inventory with evidence grades

List what must be true for the feature to deliver value, then grade the evidence actually
supplied, not the requester's confidence.

Assumptions to cover:

- **Problem:** the problem exists and matters enough to change behavior or spending.
- **Who:** the target users or accounts have it, in meaningful number or value.
- **Solution fit:** this solution solves it better than the current workaround.
- **Adoption:** people will discover, try, and keep using it.
- **Feasibility:** it can be built and maintained at acceptable cost and risk.
- **Business:** it moves revenue, retention, cost, or strategic position enough to justify the
  opportunity cost.

Evidence grades, from weakest to strongest:

1. **None / belief:** "tenho certeza que os clientes querem".
2. **Single anecdote:** one customer, one call, one deal.
3. **Repeated anecdotes:** several requests, usually from vocal or large customers.
4. **Systematic qualitative:** interviews or observation with a deliberate sample.
5. **Behavioral data:** usage, workarounds visible in data, support volume, lost-deal analysis
   with reasons verified.
6. **Commitment:** signed contract terms, paid pilots, letters of intent, prepayment.
7. **Experiment:** a controlled test of the behavior or outcome.

In B2B, commitment (grade 6) often beats behavioral data because volumes are small. In B2C,
behavioral data and experiments are usually available and cheap, so anecdotes deserve less
weight.

## 4. Size it honestly

Ask, do not invent:

- **Reach:** how many users or accounts, and what share of revenue or of the target segment.
- **Frequency and severity:** how often the problem occurs and what it costs when it does.
- **Current workaround:** what people do today. A cheap, tolerated workaround lowers urgency;
  an expensive, error-prone one raises it.
- **Full cost:** build, then maintain, support, document, test, and the complexity it adds to
  every future change. Custom features for one client carry precedent cost: the next client
  will ask for their own.
- **Opportunity cost:** what the team will not do instead. Name the specific displaced work.

## 5. Generate real alternatives

Compare at least these, each against the same outcome:

- **As asked.**
- **Smaller slice:** the version that serves the core job, for example a scheduled export instead
  of a configurable dashboard.
- **Non-product fix:** process, configuration, services, documentation, training, or a
  partnership.
- **Different solution to the same problem:** often found at rung 3 of the ladder.
- **Time-boxed test:** fake door, concierge, manual delivery for the requesting customers, or a
  prototype.
- **Not now:** with an explicit trigger that would reopen it.

## 6. Steelman before challenging

Write the strongest honest case for the feature: the best-supported version of why it could be
right, including strategic reasons the PM may not see. If the steelman is strong, the
recommendation should lean toward commit or commit with conditions.

## 7. Choose a position

| Position | Use when |
| --- | --- |
| **Commit** | Problem and value evidence is grade 5 or higher, or the commitment is cheap and reversible, or it is a genuine compliance obligation. |
| **Commit with conditions** | The direction is plausible but scope, success measure, or a kill criterion must be agreed first. |
| **Test first** | The riskiest assumption can be tested for a small fraction of the build cost within weeks. |
| **Reshape** | The problem is real, but a different or smaller solution serves it better. |
| **Decline for now** | Evidence is weak, cost or opportunity cost is high, and a reopening trigger can be named. |

Calibrate to reversibility: a feature flag on a small change deserves less scrutiny than a
platform commitment, a contract clause, a pricing change, or a public promise.

If the user loses the argument after a fair hearing, "disagree and commit" with an agreed
success metric and review date is a legitimate outcome. Document the assumptions so the review
compares outcomes with what was knowable at the time.

## Context notes

- **B2B enterprise:** Separate buyer, user, and admin needs. Ask for deal size, stage, whether
  the requirement is written in the contract, and how many other pipeline accounts share it.
  "Build for one, design for many": if building for one account, keep the solution generic or
  configurable, and avoid account-specific branches.
- **B2C:** Request volume reflects who complains, not who matters. Weight behavior and
  experiments over requests. Small UX changes are usually cheaper to test than to debate.
- **Marketplace:** Ask which side benefits and what happens to the other side. A feature that
  helps buyers can reduce seller supply, and the reverse.
- **Internal platform:** The customer is the consuming team. Distinguish adoption by mandate
  from adoption by value. Ask what the consuming teams would stop doing if this existed.
- **Early stage:** Speed and learning dominate. Founder conviction is a legitimate input; the
  useful challenge is usually scope and test design, not whether.
- **Mature product:** Complexity, consistency, cannibalization, and support load dominate.
  Ask what the feature adds to the maintenance surface and who owns it in two years.

## Conversation tactics

Lead with the shared goal, then the risk, then a concrete proposal. Never lead with "no" or
"the data says" when the data is thin.

Questions that surface evidence without sounding like a veto:

- Problem: "Que problema o cliente está tentando resolver quando pede isso?" / "O que ele faz hoje
  no lugar?"
- Evidence: "Quantos clientes trouxeram isso, e quem são?" / "Temos algum caso em que perdemos
  negócio por causa disso?"
- Success: "Daqui a três meses, como a gente sabe que funcionou?"
- Urgency: "O que acontece se a gente entregar isso daqui a dois trimestres em vez de agora?"
- Scope: "Qual é a menor versão que resolveria o caso do cliente X?"
- Trade-off: "Se fizermos isso, paramos Y. Você prefere isso a Y?"
- Commitment (B2B): "O cliente topa entrar como design partner ou assinar isso no contrato?"

Phrases that keep the door open:

- "Concordo com o objetivo; minha dúvida é se essa é a forma mais barata de chegar lá."
- "Proponho testar a hipótese mais arriscada em duas semanas antes de comprometer o trimestre."
- "Se o resultado for X, eu mesmo defendo construir a versão completa."

## Anti-patterns in the analysis

- **Reflexive skepticism:** treating every request as wrong. Requesters often hold real signal.
- **Unreachable evidence bar:** demanding proof nobody can produce before any action.
- **Discovery as a stall:** proposing research without a decision rule or deadline.
- **False neutrality:** listing pros and cons without taking a position.
- **Arguing the solution when the dispute is the goal:** if leadership wants a different outcome
  than the PM, no feature analysis resolves it; escalate the goal question explicitly.
- **Invented numbers:** estimating reach or revenue without a source and presenting it as fact.

## Worked example

Request: the VP of Sales says a large prospect will sign only if the product has customizable
dashboards, and asks for it this quarter.

- Classification: sales deal; risk of one-account feature.
- Ladder: dashboards → see data their way → the manager builds a weekly Excel report for the
  board by hand → report to the board without manual work → close this deal and future
  enterprise deals.
- Riskiest assumptions: that the deal depends on dashboards rather than on reporting in
  general; that other enterprise accounts share the need.
- Alternatives: scheduled export to their BI tool; three fixed executive report templates;
  services-built report for this client; full dashboard builder.
- Steelman: enterprise buyers do evaluate reporting in RFPs, and if several pipeline deals cite
  it, the feature may unlock a segment, not one deal.
- Position: reshape and test. Offer the prospect a scheduled export plus one executive report
  template as a contract commitment; in parallel, check lost-deal notes and the pipeline for the
  same requirement. Reopen the full builder if three or more qualified deals cite it.

Sample argument in pt-BR:

> Concordo que reporting está travando o deal do cliente X e quero resolver isso neste
> trimestre. Pelo que entendi, o problema real é o gestor montar o relatório da diretoria na mão
> toda semana. Proponho entregar export agendado para o BI deles e um template de relatório
> executivo, que dá para fazer em semanas, e colocar isso no contrato. Em paralelo, vou levantar
> quantos deals do pipeline pedem a mesma coisa. Se aparecerem outros com a mesma necessidade,
> eu defendo o builder completo no próximo ciclo, já com o desenho validado.

## Output

Lead with the recommended position in one sentence. Then give:

- the request classification and the reconstructed ladder, marking unknown rungs;
- the critical assumptions with their evidence grade;
- the alternatives worth discussing, with cost and what each sacrifices;
- the steelman;
- questions to ask the requester;
- a short argument in the user's language: shared goal, key risk, concrete next step, and the
  condition under which the user would support the full version;
- what evidence would change the position.

Do not invent customer, usage, revenue, or market facts to strengthen the argument. If the case
depends on information the user does not have, say exactly what to ask for and from whom.
