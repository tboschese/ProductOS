# Go-to-market

Use for launches, positioning, messaging, pricing and packaging, sales enablement, beta
programs, and adoption of a released capability. Do not invent market size, competitor facts,
or willingness to pay; mark them as research needed.

## 1. Who exactly

- **Best-fit customer:** the segment that gets the most value fastest, defined by observable
  traits and situations (size, workflow, tooling, trigger event), not aspirations.
- **Roles (B2B):** economic buyer, champion, end user, admin, and blockers such as security,
  legal, or procurement. Each needs a different message and proof.
- **Current alternative:** what they do today: a competitor, a spreadsheet, an agency, an
  internal tool, or nothing. You compete with the alternative, not with the category.
- **Trigger:** the event that makes them look for a solution now, such as growth, a new
  regulation, a failed audit, a new hire, or a contract renewal.

## 2. Positioning

April Dunford's *Obviously Awesome* gives a practical sequence:

1. **Competitive alternatives** the best-fit customers would use if this did not exist.
2. **Unique attributes** this offering has that the alternatives lack.
3. **Value** those attributes deliver, with proof.
4. **Best-fit customers** who care most about that value.
5. **Market category** that frames the offering so buyers understand it.

Optional summary statement:

> Para **[cliente ideal]** que **[situação ou problema]**, **[produto]** é **[categoria]** que
> **[valor principal]**. Diferente de **[alternativa atual]**, **[diferencial com prova]**.

Tests: a target customer would recognize their situation; the differentiator is something they
value, not only something we built; there is proof (data, customer quote, demo) and not only a
claim. Write messaging in the customer's words, gathered from interviews, calls, and reviews.

## 3. Launch tiers

Size the effort to the change. Indicative criteria:

| Tier | When | Typical activities |
| --- | --- | --- |
| **Tier 1 (major)** | New product, new segment, pricing change, major differentiator, or a change in how customers work | Positioning work, external announcement, sales and support enablement, campaign, press or analyst briefings where relevant, success review |
| **Tier 2 (notable)** | Meaningful improvement for an existing segment, or a reason to upgrade | Release notes, in-product announcement, email to affected users, sales one-pager, help docs |
| **Tier 3 (minor)** | Fixes, small improvements, internal changes | Changelog, help-doc update, support briefing if behavior changes |

Overlaunching trains customers and sales to ignore announcements; underlaunching hides real
value. A change that alters existing workflows needs communication even if it is small.

## 4. Motion

- **Product-led:** users discover, try, and buy in product. Critical: activation, time to
  value, in-product prompts, self-serve upgrade paths, usage limits that trigger upgrades.
- **Sales-led:** account executives sell to buyers. Critical: enablement, demo stories,
  objection handling, proof, security and procurement readiness, pipeline signals.
- **Product-led sales (hybrid):** product usage identifies accounts ready for sales contact.
  Critical: account-level usage signals and a clear handoff.
- **Partner or channel:** partners resell or integrate. Critical: partner incentives,
  integration quality, joint enablement, channel conflict.
- **Marketplace:** cold-start problem. Usually concentrate in a narrow geography or category,
  seed the harder side first, and measure liquidity before broad marketing.
- **Internal platform:** adoption by consuming teams. Critical: migration tooling, a paved road
  that is easier than alternatives, documentation, champions in early teams, and a deprecation
  plan for the old path.

The motion determines who must be enabled and which success signals matter.

## 5. Pricing and packaging

- **Value metric:** what the price scales with (seats, usage, accounts, transactions) should
  track the value the customer gets and be predictable for them.
- **Packaging:** good-better-best tiers, add-ons, or usage-based components. Put features where
  they create a reason to upgrade for the segment that values them, and keep the entry tier
  useful enough to activate.
- **Included versus add-on:** include when the feature drives retention or adoption of the
  core; sell as an add-on when the value is concentrated in a segment willing to pay.
- **Existing customers:** grandfathering, migration windows, communication, and the effect on
  trust. Removing value from existing plans carries churn and reputation risk.
- **Willingness-to-pay research:** interviews about current spend, Van Westendorp price
  sensitivity, Gabor-Granger, conjoint analysis, and live price tests. Stated preferences are
  weaker than purchases; treat survey prices as ranges, not answers.
- **Discounting:** heavy or inconsistent discounting signals a value or positioning problem.
- **Change process:** define the hypothesis, the segments affected, the guardrails (churn,
  conversion, sales cycle, support contacts), and the rollback or grandfathering plan.

## 6. Beta and early access

- Select design partners from the best-fit segment, not only friendly accounts.
- Agree success criteria and a time frame upfront; in B2B, document them in the pilot agreement.
- Collect usage and qualitative feedback, and decide explicitly whether to launch, iterate, or
  stop.
- Avoid betas that become permanent custom deployments.

## 7. Readiness

Limit to what applies to the tier:

- product: feature flags, rollout plan, monitoring, rollback;
- measurement: instrumentation verified and the baseline captured;
- support: training, macros, escalation path, known issues;
- sales and success: one-pager, demo script, objection handling, pricing guidance, target
  account list;
- documentation: help center, API docs, release notes;
- legal, security, compliance, and billing where affected;
- internal communication: everyone who talks to customers knows before customers do.

## 8. Adoption after launch

Adoption funnel: aware → tried → used repeatedly → retained. Diagnose low adoption by stage:

- **Low awareness:** poor discoverability or communication; fix placement and messaging.
- **Tried but not repeated:** weak value, poor usability, or wrong target users; investigate
  with sessions and interviews.
- **Repeated by few:** a niche fit; decide whether to focus on that segment or reshape.

Success measures should include adoption by the target segment, activation, retention of
adopters, and the business result, each against a baseline with a review date.

## Context notes

- **B2B:** Long cycles, so leading indicators are pipeline influenced, deals using the
  capability in the sales process, and pilot conversions. Security and procurement readiness
  often decide timing.
- **B2C:** Distribution and onboarding dominate; channels, app store presence, referral loops,
  and the first session matter more than announcements.
- **Early stage:** Founder-led sales and narrow positioning; win a small segment decisively
  before broadening.
- **Mature:** Coordinate with existing packaging, avoid cannibalizing higher tiers by accident,
  and manage change for a large installed base.

## Anti-patterns

- Launching to everyone at once, with no target segment.
- Positioning around features rather than the customer's alternative and value.
- Treating the launch date as the finish line, with no adoption review.
- Pricing decisions made without a hypothesis, guardrails, or rollback.
- Sales hearing about the feature from customers.
- Celebrating announcement reach instead of adoption and retention.

## Worked example

Situation: a B2B SaaS releases automated approval workflows, useful mostly for customers with
more than one approval level.

- Best fit: mid-size and enterprise accounts with multi-level approvals, currently using email
  and spreadsheets; the champion is the operations manager, the buyer is the finance or
  operations director.
- Positioning: against email and spreadsheets, it gives an audit trail and cuts the approval
  cycle; proof comes from beta customers' before-and-after cycle time, if measured.
- Tier: Tier 1 for the target segment because it is a reason to upgrade; Tier 3 for small
  accounts that will not see it.
- Packaging: included in the upper tier as an upgrade driver; consider a time-limited trial for
  accounts in the lower tier that show multi-approver behavior in usage data.
- Motion: product-led sales; usage signals, such as several people commenting on the same request
  or frequent exports before approval, flag accounts for success managers.
- Success: share of target accounts that activate a workflow within the review window,
  retention of workflow usage, upgrades attributed to the feature, and support contacts as a
  guardrail. Baselines captured before launch; targets marked as guesses until the first
  cohort.

## Output

Lead with the recommended launch approach and tier. Then give the best-fit segment and roles,
the positioning (alternative, differentiator, proof), the motion and who must be enabled,
packaging and pricing considerations with risks, the readiness checklist limited to what
applies, success measures with baselines and a review date, and the main risks. List open
research questions instead of inventing market facts.
