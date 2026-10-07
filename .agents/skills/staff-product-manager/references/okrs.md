# OKRs and goals

Use when drafting, reviewing, or fixing OKRs or other goal sets. OKRs are a tool to focus a team
on outcomes for a period. They are not a strategy, a roadmap, or a performance review.

## 1. Check whether OKRs fit

- **Good fit:** a team with enough autonomy to choose how to reach an outcome, and a strategy
  that says which outcomes matter.
- **Weak fit:** teams that mostly keep the lights on (use health metrics and service levels),
  very early startups whose priorities change weekly (use a few short-cycle goals), and
  organizations that dictate every initiative from the top (OKRs become a reporting format).
- If there is no stated strategy, say so. Infer the likely strategic choice explicitly and
  label it as an assumption instead of writing goals in a vacuum.

## 2. Anatomy

- **Objective:** a qualitative, directional statement of what should be different and why it
  matters. It should be understandable without the Key Results and should not contain a number.
- **Key Result:** a measurable change in customer behavior or business result, or a validated
  leading indicator of it. Two to four per Objective.
- **Initiatives:** the projects, features, and experiments the team bets will move the Key
  Results. They are listed separately and can change during the period.
- **Health metrics and guardrails:** what must not get worse while pursuing the Key Results, for
  example quality, support load, margin, or reliability.

## 3. The outcome ladder

Most bad Key Results are outputs. Move each one up the ladder until it measures a change that
matters, but not so high that the team cannot influence it within the period.

1. **Activity / output:** "Lançar o novo onboarding". Not a Key Result.
2. **Adoption:** "60% dos novos usuários completam o novo onboarding". Better, but still about
   our artifact.
3. **Behavior change:** "Novos usuários que criam o primeiro projeto em 7 dias: de 35% para 45%".
   Usually the sweet spot for a product team.
4. **Business result:** "Retenção de 90 dias da coorte de novos usuários: de 22% para 26%". Right
   for a group or company level; often too lagging for one team in one quarter.

Pair a lagging result (level 4) with one or two leading behaviors (level 3) that the team can
move and observe within the period. Josh Seiden's *Outcomes Over Output* develops this framing.

## 4. Writing a Key Result

Template:

> **[Métrica com definição precisa]** para **[população]**: de **[baseline]** para **[meta]** até
> **[data]**.

Measurability checks:

- **Definition:** event, population, window, and exclusions are written down. "Usuário ativo"
  without a definition fails.
- **Source:** the data exists today or the instrumentation work is an explicit initiative.
- **Baseline:** known. If not, the first Key Result is to establish it, or the target is set
  after a few weeks of measurement. A missing baseline is a finding, not a detail.
- **Influence:** the team can plausibly move it within the period.
- **Owner:** one person accountable for tracking and reporting.
- **Ratios over totals:** totals only go up and reward volume; prefer rates, per-user, or
  per-cohort measures, with the absolute count as context.

## 5. Setting targets

- Start from the trend: what happens if the team does nothing? A target below the natural trend
  is not a goal.
- Use historical variance to avoid targets inside normal noise.
- Use external benchmarks only with a cited, comparable source; never invent a benchmark.
- Decide whether the Key Result is **committed** (expected to be fully achieved; missing it is a
  problem to explain) or **aspirational** (a stretch; partial achievement is acceptable). Google's
  published OKR guidance, popularized by John Doerr's *Measure What Matters*, treats a score of
  roughly 0.6 to 0.7 on aspirational OKRs as success. Make the type explicit so nobody reads a stretch miss as
  failure, or a committed miss as normal.
- When the target is a guess, say so and plan a recalibration checkpoint, not a silent change.

## 6. Leading indicators must be earned

A leading indicator is useful only if moving it plausibly moves the lagging result. Check:

- Is there evidence that the behavior predicts retention, revenue, or the outcome (cohort
  analysis, past experiments)?
- Could the team move the indicator without moving the outcome, for example by forcing users
  through a step?
- If the relationship is unproven, keep the indicator but also track the lagging result, and
  label the link as a hypothesis.

## 7. Gaming and conflicts

| Key Result type | How it gets gamed | Countermeasure |
| --- | --- | --- |
| Volume (signups, leads, tickets closed) | Lower quality inputs, closing without solving | Pair with quality or conversion downstream |
| Speed (time to resolve, cycle time) | Cutting corners, splitting work | Pair with reopen rate, defects, satisfaction |
| Conversion rate | Shrinking the denominator, filtering hard cases | Track absolute counts and the population |
| Engagement (sessions, time in app) | Notifications, dark patterns, friction that adds time | Pair with task success, retention, opt-outs |
| Revenue | Discounting, pull-forward, unsustainable deals | Pair with margin, churn, net revenue retention |
| Adoption of a feature | Forced exposure, default-on | Measure retained or repeated use |

Also check across teams: growth's activation target versus security's friction, sales' new
bookings versus success's churn, platform's migration count versus product teams' delivery.
Shared Key Results or explicit guardrails resolve most conflicts.

## 8. Alignment and focus

- One to three Objectives per team per period. A long list means choices were avoided.
- Alignment does not require cascading every Key Result into a child Objective. Teams should
  propose how they contribute to the higher-level outcomes, and leadership should check the sum.
- Make dependencies explicit: if a Key Result requires another team's work, it must appear in
  that team's plan or be renegotiated.
- Tying OKRs to individual compensation or ratings encourages sandbagging and gaming; say so
  when the user describes that setup.

## 9. Operating the OKRs

- **Weekly or biweekly check-in:** current value, confidence to hit, and what changes in the
  plan. Change initiatives freely; change Key Results rarely.
- **Mid-period review:** if a Key Result proves unmeasurable or wrong, fix it openly and record
  why.
- **End of period:** score honestly, then run a retrospective on the bets: which initiatives
  moved the metric, which assumptions were wrong, what to keep.

## 10. Review smells

- Key Results that are tasks, launches, or dates.
- Objectives that are a metric ("Aumentar NPS para 50") or a slogan without direction.
- Every Key Result is lagging, so the team learns nothing until the quarter ends.
- No baselines, or baselines "to be defined" with no plan to define them.
- Sandbagged targets that the trend already delivers.
- Ten Key Results for one team.
- Guardrails missing on a Key Result that is easy to game.
- Key Results that no one on the team can influence.

## Rewrites by context

- **B2B SaaS, growth stage:**
  - Weak: "O: Melhorar o produto enterprise. KR: Lançar SSO e audit log."
  - Better: "O: Tornar o produto aprovável por times de segurança enterprise. KR1: Deals
    enterprise que travam em revisão de segurança: de [baseline] para [meta]. KR2: Tempo médio do
    questionário de segurança até aprovação: de [baseline] para [meta]. Iniciativas: SSO, audit log,
    portal de segurança. Guardrail: tempo de deploy do time não piora."
- **B2C app:**
  - Weak: "KR: Aumentar o tempo médio de sessão em 20%."
  - Better: "KR: Usuários novos que completam [ação central] 3 vezes na primeira semana: de
    [baseline] para [meta]. Guardrail: taxa de opt-out de notificações e desinstalação em 7 dias
    não pioram."
- **Marketplace:**
  - Weak: "KR: Cadastrar 2.000 novos prestadores."
  - Better: "KR: Pedidos com pelo menos uma proposta em até 1 hora, nas três cidades foco: de
    [baseline] para [meta]. Guardrail: taxa de cancelamento por prestador não piora."
- **Internal platform:**
  - Weak: "KR: Migrar 30 serviços para a nova plataforma."
  - Better: "KR: Tempo de um novo serviço até o primeiro deploy em produção: de [baseline] para
    [meta]. KR2: Serviços migrados que continuam na plataforma após 60 dias, sem exceções abertas:
    [meta]."
- **Early-stage startup:**
  - Weak: "KR: Atingir R$ 1 milhão de ARR" for a team of five with an unclear segment.
  - Better: "O: Provar que [segmento] tem o problema e paga para resolver. KR1: [N] clientes
    pagantes do segmento que usam semanalmente após 8 semanas. KR2: Pelo menos [N] clientes
    renovam ou expandem sem desconto."

Bracketed values are placeholders; never fill them with invented numbers.

## Output

For a review, lead with the two or three changes that matter most, then rewrite the weakest
items and show the reasoning for each rewrite. For a draft, give:

- the strategic choice the goals serve, marked as stated or inferred;
- one to three Objectives;
- two to four Key Results each, with definition, source, baseline (or "unknown: establish
  first"), target, type (committed or aspirational), and owner;
- initiatives listed separately;
- guardrails and the gaming risks they address;
- which targets are guesses and when to recalibrate them.
