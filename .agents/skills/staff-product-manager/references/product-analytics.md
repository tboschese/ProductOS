# Product analytics

Use for defining metrics, diagnosing a metric change, reading funnels, retention, or cohorts,
designing instrumentation, and interpreting experiments.

## Diagnosing a metric change

1. **Is it real?** Check definition changes, tracking or release bugs, data delays, bot or
   test traffic, seasonality, and the comparison window before any product explanation.
2. **Where is it?** Decompose by segment, platform, acquisition source, cohort, geography, and
   funnel step. Check mix shift: the aggregate can move while every segment is flat.
3. **When did it start?** Align the change with releases, campaigns, pricing, incidents, and
   external events. Coincidence in time is a lead, not proof.
4. **Competing explanations.** Keep several until evidence separates them; state what each
   predicts in the data.
5. **Next analysis.** Name the specific cut or query that best discriminates, and a stop rule.

## Defining metrics

- Start from the user behavior that indicates value, then the business result it drives.
- Separate a north-star or primary metric, input metrics the team can move, and guardrails.
- Define each metric precisely: event, population, time window, and edge cases.
- Prefer rates and cohorts over cumulative totals, which only go up.
- Vanity metrics, such as signups or page views without activation or retention, describe
  activity, not value.

## Retention and engagement

Use cohort curves rather than a single average. Look for whether curves flatten (a retained
core exists) or decay to zero. Define activation by the early behavior that predicts retention,
and validate that relationship rather than assuming it.

## Experiments

Before reading results, check the sample ratio, the planned sample size or power, the duration
across full weekly cycles, novelty effects, and multiple comparisons. Report the effect size
with its uncertainty, not only significance. A small or short test is a signal to investigate,
not a verdict. Never invent p-values, intervals, or power; say what information is missing.

## Output

Lead with what the data does and does not show. Then give the checks, the competing
explanations, and the next query or decision. Label every number the user did not supply as an
assumption.
