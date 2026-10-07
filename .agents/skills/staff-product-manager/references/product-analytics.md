# Product analytics

Use for defining metrics, diagnosing a metric change, reading funnels, retention, or cohorts,
designing instrumentation, measuring feature impact, and interpreting experiments.

Never invent numbers, p-values, intervals, benchmarks, or causal effects. Label every number the
user did not supply as an assumption or a placeholder.

## 1. Metric system

Structure metrics in layers rather than a flat dashboard:

- **North star or primary outcome:** a behavior that indicates customers getting value and that
  drives the business over time.
- **Input metrics:** the few levers teams can move that feed the primary outcome, for example
  new activated users, frequency of the core action, retained cohorts, or expansion.
- **Guardrails:** what must not get worse: quality, latency, support contacts, refunds,
  unsubscribes, margin, trust and safety.
- **Health or diagnostic metrics:** used to investigate, not to set goals.

Examples by model, to adapt rather than copy:

- **B2B SaaS:** weekly active accounts performing the core workflow; inputs: activated new
  accounts, seats active per account, use of the features tied to renewal; business: gross and
  net revenue retention.
- **B2C subscription or app:** users completing the core action at the natural frequency of the
  job; inputs: activation, D7 and D30 retention, conversion to paid; guardrails: churn,
  notification opt-outs, refunds.
- **Marketplace:** successful transactions; inputs: liquidity (share of demand matched in a time
  window), supply utilization, repeat rate on both sides; guardrails: cancellations, disputes,
  take rate stability.
- **Internal platform:** adoption by consuming teams, time from new service to production,
  incident rate attributable to the platform, satisfaction of internal users.

Match frequency to the job. A tax product used once a year should not be judged by daily
active users.

## 2. Defining a metric

Write the definition before arguing about the number:

- **Event or state:** what exactly counts, from which system.
- **Unit:** user, account, workspace, order, session. B2B products often need both user and
  account views.
- **Population and exclusions:** internal users, test accounts, bots, free versus paid,
  geography.
- **Window:** daily, weekly, rolling 28 days, calendar month; time zone.
- **Denominator:** for every rate, state what is in the denominator and why.
- **Edge cases:** reactivations, merges, refunds, multi-device identity.

Common traps: "ativo" meaning login rather than value; cumulative totals that only go up;
averages hiding bimodal distributions (use medians and distributions); ratios where the
numerator and the denominator both changed.

## 3. Diagnosing a metric change

Work in this order, stopping when an explanation is confirmed.

1. **Is it real?**
   - Definition, query, or dashboard changes.
   - Tracking breaks: event volume drops for one platform, app version, or browser; new
     release that renamed an event; consent banner changes.
   - Data pipeline delays and late-arriving data.
   - Bot, spam, or test traffic.
   - Calendar effects: weekday mix, holidays, month-end, paydays, seasonality. Compare same
     weekday and year over year where possible.
   - Normal variance: is the change larger than typical week-to-week movement?
2. **Which side of the ratio moved?** For a rate, check the numerator and the denominator
   separately. A conversion drop caused by a traffic spike of low-intent visitors is a different
   problem from fewer purchases.
3. **Where is it?** Cut by platform, app version, browser, country, acquisition channel, new
   versus returning, plan, customer size, cohort, and funnel step. Look for the cut where the
   change concentrates.
4. **Mix shift.** If every segment is flat but the aggregate moved, the composition changed
   (Simpson's paradox). Example: overall conversion drops because a paid campaign brought many
   low-intent visitors, while conversion within each channel is stable.
5. **When did it start?** Find the first day of the change and align it with releases, feature
   flags, experiments, campaigns, pricing changes, incidents, partner changes, and external
   events. Timing is a lead, not proof.
6. **Competing explanations.** Keep several alive and write what each predicts in the next cut.
7. **Next analysis and stop rule.** Name the query that best separates the remaining
   explanations, and when to stop investigating and act.

## 4. Funnels

- Define step order, whether steps must be strict, and the conversion window.
- Read both step conversion and overall conversion; improving one step can push the drop to the
  next.
- Segment before concluding: a funnel average often mixes users with very different intent.
- Use qualitative evidence (session recordings, usability tests, support tickets) to explain
  why a step drops; the funnel only shows where.
- Watch for survivorship: later steps only include people who passed earlier ones.

## 5. Retention and activation

- Use cohort curves, by acquisition week or month, rather than a single retention number.
- **Shape matters:** a curve that flattens suggests a retained core; a curve that decays toward
  zero suggests no durable fit for that cohort; a curve that rises later can indicate
  resurrection or seasonal use.
- Choose the retention definition deliberately: N-day (active exactly on day N), unbounded (active
  on day N or later), or bracket retention (active within a period). They give different numbers.
- **B2B:** distinguish logo retention, gross revenue retention (losses only), and net revenue
  retention (including expansion). Expansion can hide a churn problem.
- **Marketplace:** retention on both sides, and whether one side's churn follows the other's
  poor liquidity.
- **Activation:** find candidate early behaviors that separate retained from churned users, then
  test whether driving the behavior causes retention. Popular stories of single "magic numbers"
  are correlations; users who adopt more are often simply higher-intent. Validate with an
  experiment or a careful comparison before making it a goal.

## 6. Causality without an experiment

Before claiming that a feature, release, or campaign caused a change, check:

- **Selection bias:** feature adopters are often already more engaged.
- **Reverse causality:** engaged users find the feature, rather than the feature creating
  engagement.
- **Confounding:** a simultaneous campaign, price change, or seasonality.
- **Regression to the mean:** extreme periods tend to be followed by more typical ones.

Stronger alternatives when an A/B test is not possible: holdout groups, staged rollouts by
region or account, difference-in-differences against a comparable untouched group,
interrupted time series with a long pre-period, and matched comparisons. State the remaining
uncertainty explicitly.

## 7. Experiments

Ronny Kohavi, Diane Tang, and Ya Xu's *Trustworthy Online Controlled Experiments* is the standard
practitioner reference for this section.

**Design, before launch:**

- Hypothesis with the mechanism: "Because [insight], changing [X] will move [metric] for
  [population]."
- One primary metric, a few secondary metrics, and guardrails.
- Unit of randomization consistent with the metric: user, account, session, or region. B2B
  experiments usually randomize by account to avoid contamination.
- Minimum detectable effect and the sample size or duration it requires. If the product cannot
  reach that sample in reasonable time, the test is underpowered; choose another method or a
  bolder change.
- Run full weekly cycles and decide the duration in advance.

**During the test:**

- Do not stop at the first significant reading unless using a sequential method designed for
  it; repeated peeking inflates false positives.
- Monitor guardrails and data quality, not the primary metric's daily wiggles.

**Analysis:**

- **Sample ratio mismatch:** if the split differs from the plan beyond chance, the result is
  suspect until the cause is found.
- Report the effect size with a confidence interval, not only "significant".
- Distinguish statistical from practical significance.
- **Novelty and primacy:** early effects can fade or grow; compare early and late periods.
- **Multiple comparisons:** many metrics or segments will produce some false positives; treat
  post hoc segment wins as hypotheses for a new test.
- **Interference:** marketplaces and social products can violate independence between groups;
  consider cluster, geographic, or switchback designs.
- A flat result in an underpowered test is "inconclusive", not "no effect".

## 8. Measuring a launched feature

- **Adoption funnel:** exposed → tried → used repeatedly → retained users of the feature.
- Compare adopters with non-adopters only with caveats about selection; prefer a holdout or
  staged rollout when the decision matters.
- Measure the outcome the feature was meant to move, not only feature usage.
- Set a review date and a decision: keep, iterate, or remove.

## 9. Instrumentation

- Maintain a tracking plan: event names, triggers, properties, owner, and the questions each
  event answers.
- Consistent naming such as object-action ("project_created"), with properties for context.
- Identity: anonymous to known user, user to account, cross-device.
- Instrument before launch, verify in staging and production, and add instrumentation work to
  the plan explicitly. A launch without measurement is an opinion with a release date.

## Anti-patterns

- Vanity metrics as goals: signups, page views, downloads without activation or retention.
- Dashboards without decisions: many charts, no owner, no question.
- Explaining a change before checking that it is real.
- Average-only reporting.
- Declaring causality from a before-and-after chart.
- Celebrating an experiment from one segment found after the fact.
- Moving the metric definition to make the result look better.

## Worked example

Question: "A conversão do checkout caiu 15% semana passada. O que aconteceu?"

1. Real? Compare with the same week in prior periods and normal variance; check whether checkout
   events dropped on one platform or app version; check for tracking or consent changes.
2. Ratio: did purchases fall, or did checkout starts rise? If starts rose sharply from one
   channel, it may be mix shift from a campaign.
3. Where: cut by platform, browser, payment method, country, new versus returning. A drop
   concentrated in one payment method points to a provider issue; a drop in one app version
   points to a release.
4. When: identify the first day; align with releases, payment-provider incidents, price or
   shipping changes, and campaigns.
5. Explanations and predictions: a release bug predicts a drop in one version or platform from
   the release date; a provider failure predicts errors at the payment step for one method; a
   campaign mix shift predicts stable conversion within channels; a price or shipping change
   predicts abandonment at the step that reveals the total.
6. Next query: payment-step error rate by method and app version per day, since it separates
   the two most damaging explanations fastest.

## Output

Lead with what the data does and does not show. Then give the checks done or needed, the
competing explanations with what each predicts, the next query or decision, and the stop rule.
For metric design, give the definition table and the guardrails. For experiments, give the
design or the validity checks before the interpretation.
