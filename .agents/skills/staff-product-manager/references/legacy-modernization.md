# Legacy modernization

Use when the user must decide whether, how, or how much to modernize a legacy system, product,
or platform, or must argue for or against a rewrite.

## 1. Find the business reason

Modernization competes with customer-facing work, so it needs a reason stakeholders recognize.
Common legitimate reasons:

- delivery speed: changes take too long or break too often;
- reliability or performance: incidents, outages, latency that affect customers;
- security, compliance, or end-of-support components;
- operating cost: infrastructure, licenses, or manual operations;
- a strategic capability the current system cannot support, such as a new market or product;
- talent risk: few people understand the system.

"The code is ugly" or "the stack is old" is not a business reason on its own. Translate it into
one of the above with evidence, or say the evidence is missing.

## 2. Measure the pain

Ask for, rather than invent:

- lead time for changes and change failure rate in the legacy area versus elsewhere;
- incident count and severity attributable to the system;
- share of roadmap items that touch the system and their delay;
- cost to run and to maintain;
- knowledge concentration: how many people can safely change it.

These measures also become the success criteria of the modernization.

## 3. Map the system

- Domain boundaries and business rules, including undocumented ones embedded in code.
- Dependencies: upstream and downstream systems, integrations, customers' integrations.
- Data: ownership, quality, volume, migration complexity, retention rules.
- Users and workflows that depend on current behavior, including quirks customers rely on.
- Regulatory and contractual constraints.

Undocumented business rules are the main reason rewrites fail or run late.

## 4. Compare options

| Option | Fits when | Main risk |
| --- | --- | --- |
| **Deliberate maintenance** | Stable area, little change expected | Slow decay; talent risk grows |
| **Containment** | Isolate the legacy behind an interface and stop expanding it | Interface becomes a bottleneck |
| **Incremental refactoring** | Team can improve in place alongside features | Never finishes without explicit allocation |
| **Strangler fig** (Martin Fowler's pattern) | Functionality can be replaced piece by piece behind a routing layer | Long dual-running period, data synchronization |
| **Platform or service extraction** | One domain changes often or needs to scale independently | Distributed-system complexity |
| **Vendor or SaaS replacement** | The capability is not differentiating | Customization limits, migration, lock-in |
| **Full rewrite** | Small system, well-understood rules, or the old platform is truly unusable | Feature freeze, missed rules, long time to value; historically a frequent failure mode |

Prefer options that deliver value incrementally and can be stopped midway with a benefit kept.

## 5. Plan for continuity

- Rollback for every step; dual running or shadow traffic where possible.
- Data migration validated by reconciliation, not spot checks.
- Behavior parity tests for business rules, including the quirks customers depend on.
- Communication with customers and internal users affected by changes.
- A capacity split agreed with leadership, for example a fixed share of the team over several
  quarters, instead of competing ad hoc with features.

## 6. Measure the outcome

Track the measures from step 2 against their baseline: lead time, change failure rate,
incidents, cost, roadmap delay, plus migration progress and adoption of the new path.
Milestones like "service X migrated" are progress, not outcomes.

## Arguing for it

- Lead with the business consequence, not the technology.
- Show the cost of inaction over time with the measured pain.
- Propose the first increment that delivers visible value within a quarter.
- State the stop or reassessment points.

Sample framing in pt-BR:

> Hoje, toda mudança no módulo de faturamento leva [baseline] e [N]% delas geram incidente.
> Isso atrasa [iniciativas do roadmap]. Proponho extrair primeiro o cálculo de impostos, que é
> onde concentra o risco, com rollback em cada etapa. Em um trimestre a gente mede se o tempo de
> mudança caiu; se não cair, reavaliamos antes de seguir.

## Anti-patterns

- Defaulting to a rewrite or a fashionable architecture.
- Modernization with no business metric, only technical milestones.
- Feature freeze for a long rewrite.
- Ignoring undocumented business rules and customer-dependent quirks.
- Starting without capacity agreed by leadership.

## Output

Lead with the recommended option and first increment. Then give the business reason with its
evidence status, the measured pain or what to measure, the options compared, the continuity
plan, outcome measures with baselines, and reassessment points.
