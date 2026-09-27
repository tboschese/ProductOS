# ProductOS
## Evidence-Based Multilingual Product Management Knowledge & Reasoning System

**Version:** 0.3
**Status:** Initial Development Specification
**Primary implementation:** Staff Product Manager Skill
**Canonical knowledge language:** English
**Initial interaction languages:** English, Portuguese (Brazil), Spanish

---

# 1. Vision

ProductOS is a multilingual, evidence-based Product Management knowledge, reasoning and decision-support system designed to operate at the level expected from an experienced Staff or Principal Product Manager.

The objective is not to create:

- a large prompt;
- a Product Management encyclopedia;
- a framework catalog;
- a PRD generator;
- a generic PM chatbot;
- a checklist-based Product Manager;
- a system that mechanically applies methods;
- a repository containing disconnected Product Management articles.

The objective is to create a reusable Product Management intelligence system capable of:

1. understanding ambiguous product problems;
2. identifying the real decision to be made;
3. reframing weak or incorrect problem statements;
4. separating facts from assumptions;
5. identifying the most important uncertainty;
6. generating competing hypotheses;
7. combining customer, market, UX, business, financial, organizational, technical and data reasoning;
8. selecting appropriate methods;
9. identifying when no framework is necessary;
10. evaluating trade-offs;
11. determining the cheapest credible way to reduce uncertainty;
12. evaluating strategic alignment;
13. connecting strategy to execution;
14. making recommendations proportional to available evidence;
15. establishing meaningful measures of success;
16. learning from outcomes;
17. communicating with Staff/Principal-level clarity;
18. operating consistently across multiple languages.

The defining principle is:

> Product reasoning is more important than framework recall.

Frameworks are tools.

They are not the reasoning engine.

---

# 2. Product Thesis

Many Product Management assistants optimize for information retrieval rather than product judgment.

Common failure modes include:

- jumping directly to frameworks;
- treating stakeholder requests as validated customer needs;
- confusing customer requests with customer problems;
- confusing outputs and outcomes;
- generating PRDs before understanding the problem;
- recommending discovery mechanically;
- treating discovery as a project phase;
- generating roadmaps without strategy;
- prioritizing without strategic context;
- using prioritization scores as objective truth;
- treating OKRs as task lists;
- producing vanity metrics;
- accepting metrics without validating instrumentation;
- recommending experiments without statistical justification;
- interpreting correlation as causation;
- overgeneralizing small qualitative samples;
- ignoring market dynamics;
- ignoring unit economics;
- ignoring technical constraints;
- ignoring organizational constraints;
- ignoring regulatory constraints;
- treating launch as the end of product work;
- separating Product Marketing from Product Management;
- treating Product Ops as administrative support;
- generating generic executive recommendations;
- hiding uncertainty behind polished language;
- behaving inconsistently across languages.

ProductOS should instead operate as a product decision-support system.

The basic reasoning loop is:

```text
Context
   ↓
Decision
   ↓
Problem Framing
   ↓
Evidence
   ↓
Uncertainty
   ↓
Hypotheses
   ↓
Options
   ↓
Method Selection
   ↓
Evidence Gathering
   ↓
Trade-offs
   ↓
Decision
   ↓
Execution
   ↓
Measurement
   ↓
Learning
   ↓
Strategy Update
```

---

# 3. ProductOS System Architecture

ProductOS consists of reusable intellectual layers.

```text
ProductOS
│
├── Product Reasoning Engine
├── Product Knowledge Base
├── Product Evidence System
├── Product Terminology System
├── Product Framework Atlas
├── Product Decision Patterns
├── Product Playbooks
├── Product Casebook
├── Product Anti-Pattern Library
├── Product Evals
│
└── Product Skills
    ├── Staff Product Manager
    └── Research Curator
```

Future implementations may include:

```text
Principal Product Manager
Product Leader
Product Strategist
AI Product Manager
Platform Product Manager
Growth Product Manager
B2B Product Manager
Marketplace Product Manager
Product Marketing Advisor
Product Operations Advisor
Product Portfolio Advisor
```

These should share the same underlying reasoning, knowledge, terminology, sources and evidence infrastructure.

---

# 4. Core Design Principles

## 4.1 Evidence over opinion

Every important statement should be distinguishable as:

```text
Fact
Observation
Interpretation
Assumption
Hypothesis
Opinion
Recommendation
Unknown
```

Never present one category as another.

---

## 4.2 Prefer primary sources

Preferred evidence hierarchy:

```text
Primary research
↓
Original framework authors
↓
Peer-reviewed academic research
↓
Authoritative research institutions
↓
Industry empirical research
↓
Company product / engineering publications
↓
Recognized practitioners
↓
Community knowledge
```

Community sources can reveal useful perspectives and real-world experiences but should not automatically override stronger evidence.

---

# 5. Product Reasoning Principles

## 5.1 Frameworks are tools, not answers

Never recommend a framework merely because the situation resembles a framework category.

First understand:

```text
decision
problem
context
evidence
uncertainty
constraints
stakeholders
time horizon
```

Only then determine whether a framework helps.

---

## 5.2 Reasoning before artifacts

Do not optimize primarily for producing:

```text
PRDs
roadmaps
canvases
personas
OKRs
backlogs
prioritization matrices
opportunity trees
strategy decks
```

Artifacts are outputs of thinking.

They must not replace thinking.

---

## 5.3 Challenge the framing

The user's initial question may itself be wrong.

Example:

```text
Which feature should we build?
```

may really require:

```text
Which customer problem is worth solving?
```

or:

```text
Do we have evidence that a product intervention is required at all?
```

ProductOS should challenge weak framing without becoming argumentative.

---

## 5.4 Reduce uncertainty efficiently

Ask:

> What uncertainty most affects this decision?

Then:

> What is the cheapest credible way of reducing it?

---

## 5.5 Context determines method

No method should be treated as universally correct.

Examples:

```text
RICE
JTBD
OKRs
A/B Testing
Scrum
Opportunity Solution Trees
NPS
Personas
MVP
Design Thinking
North Star Metric
```

all have contexts in which they are useful and contexts in which they are poor choices.

---

## 5.6 Avoid false precision

Do not transform subjective judgment into apparently scientific numbers without acknowledging uncertainty.

---

## 5.7 Preserve contradictions

Product Management contains competing schools of thought.

ProductOS must model disagreement explicitly.

Do not manufacture consensus.

---

## 5.8 Recommendations must be proportional to evidence

Weak evidence should produce tentative recommendations.

Strong evidence can support stronger conclusions.

---

# 6. Multilingual Architecture

ProductOS must be language-independent at the reasoning layer and multilingual at the interaction layer.

Use:

```text
Canonical Knowledge
        ↓
Product Reasoning
        ↓
Language Adaptation
        ↓
User Response
```

Do not create independent intellectual systems for each language.

---

# 7. Canonical Knowledge Language

English is the canonical internal language.

Use English for:

- IDs;
- schemas;
- canonical concepts;
- framework names;
- knowledge relationships;
- research synthesis;
- source metadata;
- internal documentation;
- taxonomy.

Reasons:

- most primary Product Management literature is available in English;
- many frameworks originated in English;
- this reduces translation drift;
- this avoids duplicated concepts.

---

# 8. Supported Interaction Languages

Initial languages:

```text
English
Portuguese — Brazil
Spanish
```

The architecture must allow expansion to additional languages.

ProductOS should:

1. infer the user's language;
2. respond primarily in that language;
3. preserve recognized technical terminology;
4. avoid unnatural literal translations;
5. explain ambiguous terms where useful;
6. maintain equivalent reasoning quality across languages.

---

# 9. Terminology Strategy

Technical terminology should reflect actual practitioner usage.

Example:

```yaml
id: product-market-fit

canonical_name: Product-Market Fit

localized:
  en:
    preferred: Product-Market Fit

  pt-BR:
    preferred: Product-Market Fit
    aliases:
      - ajuste produto-mercado
      - PMF

  es:
    preferred: Product-Market Fit
    aliases:
      - ajuste producto-mercado
      - PMF
```

Do not translate established framework names merely for consistency.

Examples that should usually remain unchanged:

```text
Jobs to Be Done
Opportunity Solution Tree
RICE
North Star Metric
Design Thinking
Product-Market Fit
Growth Loop
```

---

# 10. Repository Architecture

```text
product-os/
│
├── AGENTS.md
├── README.md
├── PROJECT_SPEC.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── CHANGELOG.md
│
├── .agents/
│   └── skills/
│       ├── staff-product-manager/
│       │   ├── SKILL.md
│       │   ├── references/
│       │   ├── scripts/
│       │   └── assets/
│       │
│       └── research-curator/
│           ├── SKILL.md
│           ├── references/
│           └── scripts/
│
├── docs/
│   ├── foundations/
│   ├── domains/
│   ├── frameworks/
│   ├── playbooks/
│   ├── casebook/
│   ├── anti-patterns/
│   └── sources/
│
├── knowledge/
│   ├── concepts.yaml
│   ├── frameworks.yaml
│   ├── decision-patterns.yaml
│   ├── sources.yaml
│   ├── cases.yaml
│   ├── anti-patterns.yaml
│   ├── relationships.yaml
│   └── terminology.yaml
│
├── research/
│   ├── README.md
│   ├── methodology.md
│   ├── backlog/
│   ├── active/
│   ├── completed/
│   ├── reviews/
│   └── synthesis/
│
├── evals/
│   ├── README.md
│   ├── rubric.md
│   ├── cases/
│   ├── multilingual/
│   ├── expected-behaviors/
│   ├── anti-patterns/
│   ├── regression/
│   └── results/
│
├── schemas/
│   ├── framework.schema.json
│   ├── source.schema.json
│   ├── concept.schema.json
│   ├── terminology.schema.json
│   ├── decision-pattern.schema.json
│   ├── research-task.schema.json
│   └── eval-case.schema.json
│
└── scripts/
    ├── validate_knowledge.py
    ├── validate_sources.py
    ├── validate_frameworks.py
    ├── validate_terminology.py
    ├── check_duplicates.py
    ├── check_links.py
    ├── build_indexes.py
    └── run_evals.py
```

---

# 11. Product Management Capability Model

ProductOS must organize knowledge around a comprehensive capability model.

---

# 12. Product Sense & Judgment

Topics:

- Product Sense
- Product Judgment
- Customer intuition
- Pattern recognition
- Trade-off judgment
- Taste and quality
- Problem sensitivity
- Opportunity recognition
- Decision quality
- Product critique
- Product teardown
- Product principles

Product Sense should be modeled as:

```text
Customer Understanding
+
Pattern Recognition
+
Behavioral Insight
+
UX Sensitivity
+
Business Judgment
+
Strategic Thinking
+
Technical Awareness
+
Data Literacy
+
Market Awareness
+
Trade-off Judgment
```

---

# 13. Customer Understanding

Topics:

- Customer problems
- Needs
- Pain points
- Motivations
- Jobs to Be Done
- Customer behavior
- Context of use
- Customer journeys
- Segmentation
- ICP
- Personas
- Behavioral segmentation
- Customer lifecycle
- Customer evidence quality

---

# 14. Product Discovery

Topics:

- Continuous Discovery
- Opportunity exploration
- Opportunity Solution Trees
- Assumption mapping
- Risk identification
- Prototyping
- Concept testing
- Fake Door tests
- Concierge experiments
- Wizard of Oz
- Pretotyping
- Riskiest Assumption Tests
- Discovery cadence
- Discovery vs Delivery
- Dual Track
- Continuous discovery habits
- Evidence synthesis

---

# 15. User Research

Topics:

- Research questions
- Interviewing
- Ethnographic research
- Contextual inquiry
- Field studies
- Diary studies
- Surveys
- Usability tests
- Concept tests
- Longitudinal research
- Sampling
- Research bias
- Interview bias
- Research synthesis
- Research repositories

---

# 16. Research Operations

Topics:

- Research governance
- Participant recruitment
- Research repositories
- Research taxonomy
- Consent
- Research planning
- Research democratization
- Research quality standards
- Research reuse
- Insight repositories

---

# 17. UX & Interaction Design

Topics:

- Usability
- Interaction design
- Information architecture
- Navigation
- Cognitive load
- Mental models
- Affordances
- Feedback
- Error prevention
- Discoverability
- Accessibility
- Inclusive design
- Design systems
- UX debt
- Service design

ProductOS should understand UX deeply enough to critique product experiences without pretending to replace professional designers.

---

# 18. Behavioral Science

Topics:

- Behavioral economics
- Cognitive biases
- Habit formation
- Motivation
- Decision architecture
- Friction
- Choice architecture
- Loss aversion
- Social proof
- Defaults
- Commitment
- Behavioral loops
- Ethical behavioral design

Behavioral science must never become justification for manipulative dark patterns.

---

# 19. Product Strategy

Topics:

- Product Vision
- Strategic intent
- Strategic choices
- Strategic positioning
- Competitive advantage
- Differentiation
- Strategic bets
- Product thesis
- Where to play
- How to win
- Strategic constraints
- Strategy narratives
- Product portfolio strategy
- Strategy coherence
- Strategy deployment
- Strategy review
- Product principles

---

# 20. OKRs & Goal Systems

This must be a first-class domain.

Topics:

- Objectives
- Key Results
- Outcomes
- Outputs
- Leading indicators
- Lagging indicators
- Strategic goals
- Operational goals
- Aspirational vs committed goals
- Goal alignment
- Cascading vs shared alignment
- Confidence tracking
- Check-ins
- KR quality
- Outcome metrics
- Portfolio OKRs
- Team OKRs
- Company OKRs
- Goal-setting cadence
- Strategy-to-execution linkage
- OKRs and roadmaps
- OKRs and incentives
- OKRs and performance management
- OKR anti-patterns
- Goodhart's Law
- Gaming metrics

ProductOS must not treat OKRs as:

```text
task lists
feature lists
project plans
performance rating systems
```

---

# 21. Product Metrics

Topics:

- Metric hierarchies
- North Star Metrics
- Input metrics
- Output metrics
- Outcome metrics
- Leading indicators
- Lagging indicators
- Guardrail metrics
- Counter metrics
- Product health metrics
- Adoption
- Activation
- Engagement
- Retention
- Conversion
- Churn
- Resurrection
- Frequency
- Depth
- Breadth
- Stickiness
- Metric trees
- Metric quality
- Metric gaming

---

# 22. Product Analytics

Topics:

- Event instrumentation
- Event schemas
- Data quality
- Funnel analysis
- Cohort analysis
- Segmentation
- Retention curves
- Behavioral analytics
- Path analysis
- Feature adoption
- Lifecycle analysis
- Attribution
- Product telemetry
- Behavioral cohorts
- Diagnostic analytics

ProductOS should always distinguish:

```text
measurement problem
from
product problem
```

---

# 23. Data Literacy & Statistics

Topics:

- Descriptive statistics
- Probability
- Distributions
- Variance
- Confidence intervals
- Statistical significance
- Statistical power
- Effect size
- Sampling bias
- Regression
- Correlation
- Causality
- Simpson's paradox
- Survivorship bias
- Base rates
- Bayesian reasoning
- Forecast uncertainty

A Product Manager does not need to become a statistician, but ProductOS must prevent statistically irresponsible recommendations.

---

# 24. Experimentation

Topics:

- Controlled experiments
- Randomization
- Control groups
- Treatment groups
- Hypothesis definition
- Experimental design
- Sample size
- Statistical power
- Minimum Detectable Effect
- Confidence intervals
- Sample Ratio Mismatch
- Multiple testing
- Novelty effects
- Carryover effects
- Network effects
- Experiment duration
- Guardrail metrics
- Overall Evaluation Criteria
- Long-term effects
- Experiment interpretation
- Experiment sequencing

ProductOS must know when **not** to A/B test.

---

# 25. Causal Reasoning

Topics:

- Correlation vs causation
- Confounding variables
- Selection bias
- Natural experiments
- Quasi-experiments
- Difference-in-differences
- Instrumental variables
- Regression discontinuity
- Causal graphs
- Counterfactual reasoning

The system does not need to perform advanced causal analysis automatically, but it must understand causal limitations.

---

# 26. Growth

Topics:

- Acquisition
- Activation
- Engagement
- Retention
- Referral
- Resurrection
- Growth loops
- Growth models
- Network effects
- Viral loops
- Paid growth
- Organic growth
- Product-led growth
- Growth accounting
- Growth experimentation
- Growth constraints
- Growth saturation

---

# 27. Product-Led Growth

Topics:

- Self-service adoption
- Freemium
- Free trial
- Activation
- Expansion
- Product-qualified leads
- Usage-based signals
- In-product education
- Conversion
- Collaboration loops
- Product-assisted sales

---

# 28. Product Marketing

This must be a first-class domain.

Topics:

- Market understanding
- Customer segmentation
- Ideal Customer Profile
- Positioning
- Messaging
- Value propositions
- Category definition
- Competitive intelligence
- Competitive positioning
- Product narrative
- Market narratives
- Launch strategy
- Go-to-market
- Sales enablement
- Product adoption
- Feature adoption
- Customer evidence
- Case studies
- Win/loss analysis
- Pricing communication
- Packaging communication
- Market feedback
- Analyst relations where relevant

ProductOS must understand the interface between:

```text
Product Management
Product Marketing
Marketing
Sales
Customer Success
```

---

# 29. Market Intelligence

Topics:

- Market structure
- Market size
- TAM
- SAM
- SOM
- Competitive landscape
- Substitutes
- Entrants
- Market maturity
- Market growth
- Market trends
- Regulation
- Category dynamics
- Competitive response
- Market timing

ProductOS should avoid treating TAM estimates as precise facts when based on weak assumptions.

---

# 30. Business Models

Topics:

- SaaS
- Subscription
- Usage-based
- Marketplace
- Transactional
- Advertising
- Freemium
- Licensing
- Hardware + software
- Platform
- Services
- Bundling
- Ecosystems
- Razor-and-blades
- Cross-subsidy

---

# 31. Pricing

Topics:

- Pricing strategy
- Value-based pricing
- Cost-based pricing
- Competitive pricing
- Willingness to pay
- Price sensitivity
- Van Westendorp
- Gabor-Granger
- Conjoint analysis
- Price experimentation
- Discounts
- Price fences
- Enterprise pricing
- Usage-based pricing
- Pricing migration
- International pricing

---

# 32. Packaging

Treat pricing and packaging as related but distinct.

Topics:

- Plans
- Tiers
- Feature packaging
- Usage limits
- Seats
- Entitlements
- Bundles
- Add-ons
- Good-better-best
- Enterprise packaging
- Free vs paid boundaries
- Packaging migration

---

# 33. Monetization

Topics:

- Revenue models
- ARPU
- ARPA
- Conversion
- Expansion
- Upsell
- Cross-sell
- Churn
- Revenue retention
- Gross Revenue Retention
- Net Revenue Retention
- Monetization experimentation
- Revenue quality

---

# 34. Product Finance

Topics:

- Revenue
- Gross margin
- Contribution margin
- CAC
- LTV
- Payback
- Unit economics
- NPV
- ROI
- IRR
- Cost of Delay
- Opportunity cost
- Investment cases
- Portfolio economics
- Financial scenarios
- Sensitivity analysis

---

# 35. Product Economics

Topics:

- Marginal cost
- Economies of scale
- Economies of scope
- Switching costs
- Network effects
- Multi-sided markets
- Marketplace economics
- Platform economics
- Pricing power
- Cannibalization
- Cross-subsidization

---

# 36. Prioritization

Frameworks may include:

- RICE
- ICE
- WSJF
- Cost of Delay
- Kano
- MoSCoW
- Value/Effort
- Opportunity Scoring
- Buy-a-Feature
- Weighted scoring
- Impact mapping

But ProductOS must reason before applying them.

Prioritization requires understanding:

```text
strategy
opportunity
risk
confidence
capacity
dependencies
economics
timing
```

---

# 37. Roadmapping

Topics:

- Outcome roadmaps
- Now / Next / Later
- Theme roadmaps
- Time-based roadmaps
- Portfolio roadmaps
- Strategic roadmaps
- Dependency roadmaps
- Roadmap communication
- Roadmap confidence
- Commitment management
- Roadmaps vs plans

---

# 38. Product Planning

Topics:

- Annual planning
- Quarterly planning
- Continuous planning
- Capacity allocation
- Strategic bets
- Product investments
- Dependencies
- Portfolio balancing
- Planning horizons
- Scenario planning
- Replanning
- Planning uncertainty

---

# 39. Product Portfolio Management

Topics:

- Portfolio strategy
- Product investment allocation
- Horizon management
- Core vs growth vs bets
- Portfolio health
- Strategic alignment
- Cannibalization
- Product lifecycle
- Product sunset
- Portfolio dependencies
- Resource allocation
- Portfolio metrics
- Portfolio reviews

---

# 40. Product Operations

This must be a first-class domain.

Topics:

- Product operating model
- Product governance
- Product planning processes
- Product review cadence
- Portfolio visibility
- Product tooling
- Decision logs
- Research repositories
- Product taxonomy
- Metric governance
- Experiment governance
- Product documentation
- Product rituals
- Cross-team coordination
- Product health reporting
- Product maturity
- Product analytics enablement
- Product discovery enablement
- Product onboarding
- Product capability development
- Product community of practice
- Standards and templates
- Process simplification

Product Ops should optimize the **system in which product teams operate**, not create bureaucracy.

---

# 41. Product Organization Design

Topics:

- Product team topology
- Empowered product teams
- Component teams
- Feature teams
- Platform teams
- Stream-aligned teams
- Product domains
- Ownership boundaries
- Team cognitive load
- Decision rights
- Product/design/engineering collaboration
- Centralization vs decentralization
- Product maturity

---

# 42. Delivery

Topics:

- Product slicing
- Incremental delivery
- MVP
- MLP
- Release strategy
- Feature flags
- Progressive rollout
- Backlogs
- Dependency management
- Risk management
- Agile
- Lean
- Scrum
- Kanban
- Flow metrics
- Lead time
- Cycle time
- Throughput
- WIP

ProductOS must not confuse Agile rituals with Product Management.

---

# 43. Technical Product Management

Topics:

- Architecture
- System boundaries
- APIs
- Integration
- Databases
- Events
- Distributed systems
- Cloud
- Reliability
- Scalability
- Performance
- Security
- Observability
- Technical debt
- Legacy systems
- Build vs buy
- Developer experience

The skill should understand enough technology to reason about trade-offs without pretending to replace architects or engineers.

---

# 44. Platform Products

Topics:

- Internal platforms
- External platforms
- API platforms
- Developer platforms
- Platform adoption
- Platform customers
- Platform roadmaps
- Platform metrics
- Self-service
- Developer experience
- Platform governance
- Platform product-market fit
- Platform economics
- Platform maturity
- Golden paths

---

# 45. API Products

Topics:

- API usability
- API lifecycle
- Versioning
- Developer experience
- Documentation
- Authentication
- Rate limits
- Reliability
- Developer onboarding
- API metrics
- Ecosystems
- Developer relations

---

# 46. Data Products

Topics:

- Data as a product
- Data consumers
- Data contracts
- Data quality
- Data ownership
- Semantic layers
- Discoverability
- Data lineage
- Data governance
- Data SLAs
- Analytics products
- Decision products

---

# 47. AI Product Management

This must be a major domain.

Topics:

- AI product discovery
- AI capability assessment
- LLM products
- AI agents
- RAG
- Fine-tuning
- Prompting
- AI UX
- Human-in-the-loop
- AI evaluation
- Golden datasets
- Hallucination
- Accuracy
- Precision
- Recall
- Model confidence
- Latency
- Cost
- Reliability
- Non-determinism
- Guardrails
- AI safety
- AI observability
- Model drift
- AI experimentation
- AI economics
- Agentic workflows

AI features must be evaluated by user value, not novelty.

---

# 48. AI-Assisted Product Management

Separate AI products from the use of AI in Product Management.

Topics:

- AI-assisted research
- Qualitative synthesis
- Product analytics assistance
- PRD generation
- Code understanding
- Legacy discovery
- Competitive research
- Product ideation
- Prototyping
- AI-supported experimentation
- AI-supported decision making

ProductOS should understand the risks of automation bias.

---

# 49. Legacy Modernization

Topics:

- Legacy discovery
- Domain understanding
- Business rule extraction
- Code archaeology
- Strangler pattern
- Modernization sequencing
- Platform migration
- Technical debt
- Risk
- Migration economics
- User continuity
- Data migration
- Incremental modernization
- AI-assisted modernization

---

# 50. B2B Product Management

Topics:

- ICP
- Buying committees
- Users vs buyers
- Enterprise requirements
- Sales cycles
- Procurement
- Security reviews
- Integrations
- Customization
- Implementation
- Professional services
- Customer success
- Expansion
- Enterprise roadmap pressure

---

# 51. Enterprise Product Management

Topics:

- Complex stakeholders
- Procurement
- Compliance
- Integration dependencies
- SLA
- Enterprise contracts
- Custom requests
- Strategic accounts
- Roadmap commitments
- Enterprise rollout
- Change management

---

# 52. B2C Product Management

Topics:

- Consumer behavior
- Scale
- Engagement
- Retention
- Habit
- Virality
- Consumer UX
- Personalization
- Trust
- Pricing
- Marketplace discovery
- Brand-product interaction

---

# 53. SaaS Product Management

Topics:

- Subscription economics
- Activation
- Retention
- Expansion
- Churn
- PLG
- Product-qualified leads
- Usage metrics
- Seat growth
- Entitlements
- B2B SaaS economics

---

# 54. Marketplace Product Management

Topics:

- Supply
- Demand
- Liquidity
- Match quality
- Fill rate
- Marketplace density
- Cold start
- Network effects
- Incentives
- Trust
- Reputation
- Marketplace fraud
- Disintermediation
- Take rate
- Multi-homing

---

# 55. Ecosystem Product Management

Topics:

- Partners
- Integrations
- Third-party developers
- Ecosystem incentives
- APIs
- Marketplace ecosystems
- Certification
- Partner economics
- Ecosystem governance

---

# 56. Internal Products

Topics:

- Internal users
- Adoption
- Productivity
- Internal platforms
- Tooling
- ROI
- Employee experience
- Internal product discovery
- Mandatory vs voluntary adoption

---

# 57. Developer Products

Topics:

- Developer experience
- APIs
- SDKs
- Documentation
- Onboarding
- Time to first success
- Reliability
- Communities
- Developer advocacy
- Platform adoption

---

# 58. Product Marketing / Sales Interface

ProductOS should understand:

```text
Product
Product Marketing
Sales
Sales Engineering
Customer Success
Marketing
```

and how responsibilities interact.

Topics:

- Sales feedback
- Deal intelligence
- Feature requests
- Competitive intelligence
- Lost deals
- Enterprise commitments
- Launch enablement
- Sales collateral
- Value narratives

---

# 59. Customer Success Interface

Topics:

- Adoption
- Health scores
- Onboarding
- Expansion
- Churn
- Renewal
- Support signals
- Customer maturity
- Success plans
- Feedback loops
- Strategic accounts

---

# 60. Support & Service Signals

Topics:

- Support tickets
- Contact rate
- Issue taxonomy
- Complaint analysis
- Voice of Customer
- Service recovery
- Support-driven discovery
- Escalations

Support data should be treated as evidence, not just operational noise.

---

# 61. Go-to-Market

Topics:

- Launch strategy
- Launch sequencing
- Market readiness
- Distribution
- Channels
- Adoption
- Demand generation interface
- Sales readiness
- Customer success readiness
- Operational readiness
- Pricing readiness
- Competitive response
- Launch metrics

---

# 62. Product Launch

Topics:

- Launch tiers
- Beta
- Early access
- Private preview
- Public preview
- General availability
- Rollout strategy
- Feature flags
- Communication
- Enablement
- Launch measurement
- Post-launch learning

---

# 63. Product Lifecycle Management

Topics:

- Introduction
- Growth
- Maturity
- Decline
- Maintenance
- Sunset
- Migration
- End of life
- Product consolidation
- Customer communication

---

# 64. Innovation

Topics:

- Exploration
- Exploitation
- Innovation portfolios
- Adjacent innovation
- Disruptive innovation
- Business model innovation
- Corporate innovation
- Innovation accounting
- Experiment portfolios

---

# 65. Product Leadership

Topics:

- Influence without authority
- Strategic communication
- Decision facilitation
- Conflict
- Alignment
- Coaching
- Product critique
- Product reviews
- Organizational influence
- Executive communication
- Narrative building
- Cross-functional leadership

---

# 66. Staff Product Management

Special research domain.

Topics:

- Cross-team influence
- Large scope
- Ambiguous ownership
- Strategic leverage
- Multiplying other PMs
- Product quality standards
- Portfolio thinking
- Decision architecture
- Organizational influence
- Deep domain expertise
- Coaching
- Systems thinking

---

# 67. Principal Product Management

Topics:

- Company-level influence
- Multi-year strategy
- Portfolio architecture
- Large strategic bets
- Executive influence
- Product doctrine
- Organizational design
- Complex systems
- Cross-domain decisions

---

# 68. Executive Product Leadership

Topics:

- Product organization
- Strategy
- Portfolio
- Investment
- Governance
- Talent
- Operating model
- Executive communication
- Board communication
- Product culture
- Product transformation

---

# 69. Stakeholder Management

Topics:

- Stakeholder mapping
- Influence
- Alignment
- Conflict
- Negotiation
- Decision rights
- Executive stakeholders
- Sales stakeholders
- Technology stakeholders
- Regulatory stakeholders
- Customer stakeholders

---

# 70. Decision Making

Topics:

- Decision quality
- Reversible decisions
- Irreversible decisions
- Decision velocity
- Decision rights
- Decision logs
- Pre-mortems
- Post-mortems
- Expected value
- Bayesian updates
- Scenario thinking

---

# 71. Systems Thinking

Topics:

- Feedback loops
- Delays
- Emergent behavior
- Second-order effects
- Local vs global optimization
- Constraints
- Bottlenecks
- System dynamics
- Organizational systems

---

# 72. Product Risk

Categories:

```text
Value Risk
Usability Risk
Feasibility Risk
Business Viability Risk
Market Risk
Operational Risk
Regulatory Risk
Security Risk
Reputation Risk
Execution Risk
Organizational Risk
```

---

# 73. Trust & Safety

Topics:

- Abuse
- Fraud
- Harassment
- Moderation
- Platform integrity
- Identity
- Reputation systems
- User protection
- Safety metrics
- Abuse prevention

---

# 74. Privacy

Topics:

- Privacy by design
- Consent
- Data minimization
- User control
- Data retention
- Sensitive data
- Product analytics privacy
- Personalization trade-offs

---

# 75. Security Product Thinking

Topics:

- Authentication
- Authorization
- Identity
- Threat modeling
- Security UX
- Fraud
- Account recovery
- Enterprise security
- Product-security trade-offs

---

# 76. Accessibility

Topics:

- Accessibility principles
- Inclusive design
- WCAG concepts
- Assistive technology
- Accessible interaction
- Accessible content
- Accessibility testing

Accessibility should not be treated as optional polish.

---

# 77. Ethics

Topics:

- Dark patterns
- Manipulation
- Addiction
- Vulnerable populations
- Fairness
- Transparency
- Explainability
- Algorithmic bias
- Responsible AI
- Ethical trade-offs

---

# 78. Regulation & Compliance

ProductOS should recognize contexts involving:

- privacy;
- financial regulation;
- healthcare;
- accessibility;
- consumer protection;
- AI regulation;
- data residency;
- industry compliance.

It should know when specialist legal or regulatory review is required.

---

# 79. Change Management

Important especially for enterprise/internal products.

Topics:

- Stakeholder readiness
- Organizational adoption
- Training
- Communication
- Migration
- Change champions
- Resistance
- Adoption measurement
- Process change

---

# 80. Product Transformation

Topics:

- Product operating model change
- Agile transformation
- Product model adoption
- Discovery adoption
- Product capability building
- Product maturity
- Organizational incentives
- Governance reform
- Transformation metrics

---

# 81. Product Talent & Capability

Topics:

- Product competency models
- Career ladders
- PM hiring
- Product interviews
- Coaching
- Skill assessment
- Staff progression
- Leadership development

---

# 82. Product Reasoning Engine

This is the core intellectual system.

Every significant product question should pass through a flexible version of the following stages.

---

## Stage 1 — Context

Understand:

```text
Product
Customer
Business model
Market
Company strategy
Product maturity
Team
Technology
Regulation
Organization
Constraints
Time horizon
```

---

## Stage 2 — Decision

Ask:

> What decision actually needs to be made?

Examples:

```text
Should we build this?
Should we invest further?
Why is retention declining?
Should we change pricing?
Which segment should we target?
Should we enter this market?
Should this become a platform?
Should we modernize?
Should we stop the product?
```

---

## Stage 3 — Problem Framing

Determine whether the stated problem is:

```text
a symptom
a cause
an assumption
a request
an opportunity
a constraint
```

---

## Stage 4 — Evidence

Classify:

```text
Facts
Quantitative observations
Qualitative observations
Research
Market evidence
Business evidence
Technical evidence
Assumptions
Opinions
Unknowns
```

---

## Stage 5 — Uncertainty

Identify dominant uncertainty:

```text
Customer
Value
Market
Usability
Technical
Business
Economic
Data
Operational
Regulatory
Execution
Organizational
```

---

## Stage 6 — Hypotheses

Each meaningful hypothesis may include:

```yaml
claim:
supporting_evidence:
contradicting_evidence:
confidence:
impact_if_true:
cost_to_test:
```

---

## Stage 7 — Options

Generate multiple realistic options when appropriate.

Avoid premature convergence.

---

## Stage 8 — Method Selection

Determine how to reduce uncertainty.

Methods may include:

```text
Data analysis
Customer interviews
Field research
Usability testing
Prototype
Fake Door
Survey
Experiment
Technical spike
Financial model
Competitive research
Market research
Pilot
Concierge
Operational test
```

---

## Stage 9 — Trade-off Analysis

Evaluate:

```text
Customer value
Strategic fit
Business impact
Cost
Risk
Complexity
Time
Reversibility
Dependencies
Opportunity cost
```

---

## Stage 10 — Decision

State:

```text
What we know
What we do not know
What matters most
What options exist
What evidence supports each
What decision is justified
What confidence exists
```

---

## Stage 11 — Execution

Translate decisions into:

```text
next actions
owners when relevant
experiments
delivery slices
dependencies
risks
```

---

## Stage 12 — Measurement

Define:

```text
success metric
leading indicators
guardrails
counter metrics
measurement window
```

---

## Stage 13 — Learning

After execution:

```text
What happened?
Why?
What changed?
What should be updated?
```

---

# 83. Framework Atlas

Maintain a structured registry of approximately 100–200 relevant frameworks, models and methods.

Quantity is not the objective.

Each framework should include:

```yaml
id:
name:
aliases:

category:
domains:

origin:
authors:
year:

problem_it_addresses:

purpose:

inputs:

process:

outputs:

use_when:

avoid_when:

assumptions:

strengths:

limitations:

risks:

common_misuse:

alternatives:

complements:

examples:

evidence:

sources:

confidence:
```

Critical requirement:

> Every framework entry must explain when it should not be used.

---

# 84. Framework Categories

Initial categories:

```text
Strategy
Goals
Discovery
Research
UX
Prioritization
Metrics
Analytics
Experimentation
Growth
Pricing
Business Models
Portfolio
Roadmapping
Delivery
Product Marketing
Product Ops
Leadership
Decision Making
Innovation
Technology
AI
```

---

# 85. Decision Patterns

Decision Patterns represent recurring structures of product reasoning.

Initial patterns:

```text
Retention decline
Conversion decline
Activation problem
Feature request
Enterprise request
New market
Pricing change
Packaging change
Platform investment
Legacy modernization
Technical debt
Low adoption
High usage / low value
High NPS / high churn
Marketplace liquidity
AI feature proposal
Build vs buy
Portfolio conflict
Roadmap overload
Sales-driven roadmap
Product launch
Product sunset
Competitive threat
Regulatory change
```

---

# 86. Product Playbooks

Initial playbooks:

```text
Diagnose Retention
Diagnose Activation
Diagnose Conversion
Evaluate Feature Request
Evaluate Enterprise Request
Launch New Product
Create Product Strategy
Design OKRs
Diagnose Bad OKRs
Connect Strategy to OKRs
Create Product Metrics
Design Product Discovery
Design Product Roadmap
Prioritize Portfolio
Change Pricing
Design Packaging
Product Launch
Positioning & Messaging
Win/Loss Analysis
Build Platform Capability
Modernize Legacy Product
Launch AI Product
Evaluate Build vs Buy
Design Product Operating Model
Improve Product Planning
Design Product Governance
Design Marketplace
Design B2B Product
Design PLG Motion
Sunset Product
```

Playbooks should be adaptive guides rather than recipes.

---

# 87. Product Casebook

Build a library of cases for pattern recognition.

Potential companies and products:

```text
Adobe
Airbnb
Amazon
Apple
Atlassian
Canva
Figma
GitHub
Google
Intercom
Mercado Livre
Microsoft
Netflix
Notion
Nubank
OpenAI
Shopify
Slack
Spotify
Stripe
Uber
```

Each case should cover:

```text
Context
Customer problem
Business model
Strategic choices
Product choices
Trade-offs
Growth mechanism
Metrics
Economics
Technology
Moat
Failures
Risks
Lessons
```

Avoid hero narratives.

Study failed decisions too.

---

# 88. Anti-Pattern Library

Initial anti-patterns:

```text
Framework-first thinking
Output over outcome
Solution jumping
Stakeholder request = customer need
Sales request = strategy
Backlog = strategy
Roadmap = strategy
OKRs = task list
KR = project milestone
Metric without instrumentation validation
Correlation = causation
NPS as universal truth
Persona without evidence
Discovery theater
Research theater
Fake precision
Vanity metrics
Experiment without power
A/B test everything
MVP = bad product
Platform without customers
AI because AI
AI without evaluation
Premature scaling
Overgeneralizing qualitative evidence
Ignoring organizational constraints
Ignoring opportunity cost
Ignoring adoption
Launch = success
Process bureaucracy disguised as Product Ops
```

---

# 89. Research Methodology

Research should happen through structured research tasks.

Never issue instructions like:

> Research everything about Product Management.

Each task should have bounded scope.

---

# 90. Research Task Schema

```yaml
id:

title:

domain:

research_question:

why_it_matters:

scope:

out_of_scope:

subtopics:

primary_sources:

secondary_sources:

questions:

expected_outputs:

conflicting_views_to_investigate:

acceptance_criteria:

review_status:
```

---

# 91. Research Source Model

Each source should include:

```yaml
id:

title:

authors:

organization:

year:

url:

language:

type:

authority_level:

domains:

concepts:

summary:

claims_supported:

limitations:

conflicts_with:

last_verified:
```

---

# 92. Source Authority

Use:

```text
A — Primary
B — High-authority secondary
C — Strong industry practice
D — Practitioner
E — Community
```

Primary sources should be preferred where practical.

---

# 93. Research Waves

## Wave 0 — Foundations

```text
Capability Model
Reasoning Engine
Evidence Model
Terminology Model
Source Model
Research Methodology
Eval Architecture
```

---

## Wave 1 — Product Judgment

```text
Product Sense
Decision Making
Systems Thinking
Product Strategy
Customer Understanding
```

---

## Wave 2 — Discovery & Research

```text
Product Discovery
User Research
Research Ops
Behavioral Science
JTBD
```

---

## Wave 3 — UX

```text
Interaction Design
Information Architecture
Usability
Accessibility
Service Design
Design Systems
```

---

## Wave 4 — Data

```text
Metrics
Analytics
Statistics
Experimentation
Causal Reasoning
Instrumentation
```

---

## Wave 5 — Strategy Execution

```text
OKRs
Goal Systems
Planning
Roadmaps
Prioritization
Portfolio
```

---

## Wave 6 — Growth & Commercial

```text
Growth
PLG
Product Marketing
GTM
Pricing
Packaging
Monetization
Market Intelligence
```

---

## Wave 7 — Business

```text
Business Models
Product Finance
Product Economics
Unit Economics
```

---

## Wave 8 — Technology

```text
Technical Product
Platforms
APIs
Developer Products
Data Products
AI Products
Legacy Modernization
```

---

## Wave 9 — Product Contexts

```text
B2B
Enterprise
B2C
SaaS
Marketplace
Internal Products
Ecosystems
```

---

## Wave 10 — Operating Model

```text
Product Ops
Research Ops
Organization Design
Governance
Product Planning
Product Transformation
```

---

## Wave 11 — Leadership

```text
Staff PM
Principal PM
Product Leadership
Executive Leadership
Stakeholders
Influence
Communication
```

---

## Wave 12 — Risk & Responsibility

```text
Trust & Safety
Privacy
Security
Accessibility
Ethics
Regulation
Responsible AI
```

---

# 94. Research Curator Skill

Create:

```text
.agents/skills/research-curator/
```

Responsibilities:

```text
Define research question
Find strongest sources
Prioritize primary evidence
Compare schools of thought
Identify contradictions
Extract concepts
Extract frameworks
Record provenance
Identify anti-patterns
Update decision patterns
Create eval proposals
Check duplicates
Maintain terminology
```

The Research Curator creates and maintains knowledge.

It should not act as the primary Product Manager skill.

---

# 95. Staff Product Manager Skill

Create:

```text
.agents/skills/staff-product-manager/
```

Purpose:

> Apply Staff-level Product Management judgment to ambiguous product problems using ProductOS knowledge and reasoning.

The skill should:

```text
Understand context
Determine decision
Challenge framing
Identify evidence
Identify uncertainty
Generate hypotheses
Identify relevant domains
Retrieve appropriate knowledge
Select methods
Evaluate trade-offs
Recommend next actions
Define measurement
Communicate clearly
```

The skill should not automatically expose every reasoning stage in every answer.

Internal rigor should remain high even when external communication is concise.

---

# 96. Staff PM Communication Modes

The skill should adapt output to context.

Possible modes:

```text
Diagnostic
Executive
Analytical
Coaching
Decision Memo
Product Review
Discovery
Strategy
Metrics Review
Experiment Review
Roadmap Review
```

The user should not need to explicitly choose a mode in ordinary use.

---

# 97. Knowledge Relationships

Support relationships such as:

```text
supports
contradicts
alternative_to
complements
derived_from
requires
tests
measures
influences
causes
mitigates
used_for
```

This may later evolve into a knowledge graph.

Do not build graph infrastructure prematurely.

---

# 98. Evals

Evals are first-class product infrastructure.

Test realistic decision scenarios rather than trivia.

Bad eval:

```text
What does RICE mean?
```

Good eval:

```text
Sales wants an enterprise feature that would unlock a $2M deal,
but product data shows almost no usage of similar capabilities.
How should the PM approach the decision?
```

---

# 99. Eval Rubric

Score:

```text
Problem framing
Product sense
Customer reasoning
Strategic reasoning
Business reasoning
Market reasoning
Data reasoning
Statistical reasoning
UX reasoning
Technical reasoning
Organizational reasoning
Hypothesis quality
Evidence discipline
Experimentation rigor
Trade-off awareness
Method selection
Decision quality
Measurement quality
Communication
Language & terminology fidelity
```

Scale:

```text
0 — Missing or harmful
1 — Weak
2 — Acceptable
3 — Strong
4 — Staff/Principal level
```

---

# 100. Multilingual Evals

Selected cases must exist in:

```text
English
Portuguese
Spanish
```

Expected reasoning should be materially equivalent.

Measure:

```text
Reasoning consistency
Terminology accuracy
Nuance preservation
Natural language quality
Framework naming
Statistical terminology
Business terminology
```

---

# 101. Initial Eval Suite

Create at least 50 cases.

Examples:

```text
01 Retention decline
02 Conversion drop
03 Enterprise feature request
04 New market
05 Pricing change
06 Packaging change
07 Low activation
08 High usage / low retention
09 High NPS / high churn
10 Platform investment
11 Legacy modernization
12 AI feature proposal
13 Marketplace liquidity
14 Strategic customer request
15 Technical debt
16 Build vs buy
17 Sales-driven roadmap
18 Poor onboarding
19 Growth plateau
20 Small experiment sample
21 Metric conflict
22 Roadmap overload
23 Strategic pivot
24 New competitor
25 Cannibalization
26 B2B onboarding
27 API product
28 Internal platform
29 Freemium conversion
30 Portfolio prioritization
31 Bad OKRs
32 Too many OKRs
33 Output KRs
34 Product positioning problem
35 Failed product launch
36 Win/loss contradiction
37 Product Ops bureaucracy
38 Discovery inconsistency
39 Poor instrumentation
40 Conflicting qualitative research
41 Product sunset
42 Accessibility conflict
43 Regulatory constraint
44 Security requirement
45 Customer success churn signal
46 AI hallucination problem
47 Marketplace fraud
48 Internal product adoption
49 Product team ownership conflict
50 Strategy without differentiation
```

---

# 102. Regression Testing

Every meaningful change to:

```text
Reasoning
Skills
Knowledge
Framework selection
Core instructions
```

should run a regression subset.

Knowledge expansion must not reduce reasoning quality.

---

# 103. AGENTS.md

AGENTS.md should stay compact.

Recommended structure:

```text
# ProductOS

## Mission

Build an evidence-based multilingual Product Management
knowledge and reasoning system.

## Principles

- Evidence over opinion.
- Prefer primary sources.
- Frameworks are tools, not answers.
- Reasoning precedes artifact generation.
- Distinguish facts, assumptions and hypotheses.
- Preserve meaningful contradictions.
- Avoid false precision.
- Never invent sources.
- Language must not alter reasoning quality.

## Repository Map

docs/foundations
Core reasoning models.

docs/domains
Domain knowledge.

knowledge
Structured registries.

research
Research pipeline.

evals
Behavior evaluation.

.agents/skills
Executable ProductOS skills.

## Rules

Before adding knowledge:
- search existing concepts;
- search existing frameworks;
- check terminology;
- check duplicates;
- identify primary sources;
- identify conflicting evidence.

After research:
- update sources;
- update concepts;
- update frameworks;
- update decision patterns;
- update anti-patterns;
- propose evals.

After reasoning changes:
- run regression evals.
```

---

# 104. Deterministic Scripts

Use scripts for deterministic work.

Examples:

```text
validate_knowledge.py
validate_sources.py
validate_frameworks.py
validate_terminology.py
check_duplicates.py
check_links.py
build_indexes.py
run_evals.py
```

Do not attempt to encode product judgment into deterministic scripts.

---

# 105. Definition of Done — Research

A research task is complete only when:

```text
Research question answered
Primary sources investigated
Strong secondary sources reviewed
Competing perspectives recorded
Limitations documented
Concepts extracted
Frameworks extracted
Sources registered
Terminology updated
Decision patterns considered
Anti-patterns identified
Potential evals created
Duplicate knowledge checked
```

---

# 106. Definition of Done — Framework

A framework is complete only when:

```text
Origin identified
Problem documented
Inputs documented
Process documented
Outputs documented
Assumptions documented
Use cases documented
Avoid-use cases documented
Limitations documented
Common misuse documented
Alternatives linked
Complementary methods linked
Sources attached
```

---

# 107. Definition of Done — Skill

A skill release requires:

```text
Clear routing description
Concise instructions
Externalized knowledge references
Relevant evals passing
Regression evals passing
Known failure modes documented
Multilingual behavior validated
```

---

# 108. Project Roadmap

## Phase 0 — Bootstrap

Deliver:

```text
Repository structure
AGENTS.md
README
PROJECT_SPEC
ARCHITECTURE
ROADMAP
Schemas
Research methodology
Source model
Terminology model
Eval skeleton
```

---

## Phase 1 — Reasoning Foundation

Deliver:

```text
Capability Model
Product Reasoning Engine
Product Sense Model
Evidence Model
Decision Model
Risk Model
Anti-Pattern Model
```

---

## Phase 2 — Research Infrastructure

Deliver:

```text
Source Registry
Concept Registry
Framework Registry
Decision Pattern Registry
Terminology Registry
Research Curator Skill
Validation Scripts
```

---

## Phase 3 — Product Foundations

Research:

```text
Product Sense
Strategy
Decision Making
Systems Thinking
Customer Understanding
Discovery
```

---

## Phase 4 — UX & Research

```text
User Research
Research Ops
UX
Behavioral Science
Accessibility
```

---

## Phase 5 — Data & Experimentation

```text
Metrics
Analytics
Statistics
Experimentation
Causal Reasoning
```

---

## Phase 6 — Strategy Execution

```text
OKRs
Goal Systems
Planning
Roadmapping
Prioritization
Portfolio
```

---

## Phase 7 — Commercial Product

```text
Product Marketing
GTM
Growth
PLG
Pricing
Packaging
Monetization
Market Intelligence
```

---

## Phase 8 — Economics

```text
Business Models
Product Finance
Product Economics
Unit Economics
```

---

## Phase 9 — Technology

```text
Technical Product
Platform
API
Developer Product
Data Product
AI Product
Legacy Modernization
```

---

## Phase 10 — Product Contexts

```text
B2B
Enterprise
B2C
SaaS
Marketplace
Internal Products
Ecosystems
```

---

## Phase 11 — Operating Model

```text
Product Ops
Product Organization
Governance
Product Transformation
Change Management
Product Capability
```

---

## Phase 12 — Leadership

```text
Staff PM
Principal PM
Product Leadership
Executive Product Leadership
Stakeholders
Communication
```

---

## Phase 13 — Responsible Product

```text
Trust & Safety
Privacy
Security
Accessibility
Ethics
Regulation
Responsible AI
```

---

## Phase 14 — Staff PM Skill Alpha

Build first integrated Staff Product Manager Skill.

---

## Phase 15 — Eval Expansion

Target:

```text
100+ decision scenarios
```

---

## Phase 16 — Staff PM v1.0

Stable release.

---

# 109. Initial Backlog

Create at minimum:

```text
POS-001 Repository bootstrap
POS-002 AGENTS.md
POS-003 Architecture
POS-004 Capability Model
POS-005 Product Reasoning Model
POS-006 Product Sense Model
POS-007 Evidence Model
POS-008 Uncertainty Model
POS-009 Risk Model
POS-010 Research Methodology
POS-011 Source Schema
POS-012 Framework Schema
POS-013 Concept Schema
POS-014 Terminology Schema
POS-015 Decision Pattern Schema
POS-016 Eval Schema
POS-017 Source Registry
POS-018 Concept Registry
POS-019 Framework Registry
POS-020 Terminology Registry
POS-021 Research Curator Skill
POS-022 Eval Harness
POS-023 Initial 50 Eval Cases
POS-024 Product Sense Research
POS-025 Strategy Research
POS-026 Customer Understanding Research
POS-027 Discovery Research
POS-028 User Research
POS-029 UX Research
POS-030 Behavioral Science Research
POS-031 Analytics Research
POS-032 Metrics Research
POS-033 Statistics Research
POS-034 Experimentation Research
POS-035 OKRs Research
POS-036 Goal Systems Research
POS-037 Roadmapping Research
POS-038 Prioritization Research
POS-039 Portfolio Research
POS-040 Product Marketing Research
POS-041 GTM Research
POS-042 Growth Research
POS-043 Pricing Research
POS-044 Packaging Research
POS-045 Monetization Research
POS-046 Business Models Research
POS-047 Product Finance Research
POS-048 Technical Product Research
POS-049 Platform Research
POS-050 AI Product Research
POS-051 Product Ops Research
POS-052 Product Organization Research
POS-053 Staff PM Research
POS-054 Product Leadership Research
POS-055 Responsible Product Research
POS-056 Staff PM Skill Alpha
POS-057 Multilingual Eval Suite
POS-058 Regression Suite
```

---

# 110. Versioning

Suggested milestones:

```text
0.1.0 — Architecture
0.2.0 — Reasoning foundation
0.3.0 — Research infrastructure
0.4.0 — Core PM knowledge
0.5.0 — UX + Data
0.6.0 — Strategy execution
0.7.0 — Commercial + economics
0.8.0 — Technical Product + AI
0.9.0 — Operating model + leadership
0.10.0 — Large eval suite
0.11.0 — Staff PM Release Candidate
1.0.0 — Staff Product Manager Stable
```

---

# 111. Non-Goals for v1

Do not attempt to:

- replace human judgment;
- build a SaaS UI;
- ingest every Product Management book;
- create dozens of specialized skills;
- implement a graph database immediately;
- implement complex RAG infrastructure before needed;
- maximize framework count;
- optimize for token usage prematurely;
- automate every Product Management artifact;
- create separate language-specific knowledge bases.

---

# 112. Major Risks

## Knowledge bloat

Mitigation:

```text
Canonical taxonomy
Progressive loading
Registries
Domain separation
Search before loading
```

---

## Framework obsession

Mitigation:

```text
Reasoning engine before framework selection
```

---

## Product management folklore

Mitigation:

```text
Evidence hierarchy
Primary sources
Source provenance
Contradiction tracking
```

---

## Fake consensus

Mitigation:

```text
Explicit competing perspectives
```

---

## Prompt bloat

Mitigation:

```text
Concise SKILL.md
Knowledge in references
Progressive disclosure
```

---

## Taxonomy fragmentation

Mitigation:

```text
Canonical concepts
Terminology registry
Duplicate detection
```

---

## Multilingual semantic drift

Mitigation:

```text
English canonical knowledge
Localized aliases
Multilingual evals
```

---

## Eval overfitting

Mitigation:

```text
Continuous new scenarios
Hidden regression sets when possible
```

---

## Research quantity over quality

Mitigation:

```text
Research contracts
Definition of Done
Source hierarchy
Review phase
```

---

# 113. ProductOS Success Criteria

ProductOS should eventually be able to receive:

> Our B2B SaaS retention dropped 12% after acquisition accelerated. Sales believes we need more enterprise features.

and avoid immediately accepting the sales hypothesis.

A strong reasoning path could include:

```text
Validate whether retention actually declined.

Check instrumentation.

Analyze cohorts.

Segment by acquisition source.

Segment by customer type.

Determine whether acquisition mix changed.

Compare activation.

Compare time-to-value.

Analyze engagement.

Analyze churn timing.

Review qualitative churn evidence.

Examine support and customer success signals.

Investigate product quality.

Investigate pricing and packaging.

Evaluate whether requested enterprise features correlate with churn.

Generate competing hypotheses.

Determine which hypothesis has greatest expected impact.

Determine cheapest tests.

Define decision criteria.

Define success and guardrail metrics.
```

No framework name is required for this to be good Product Management.

---

# 114. Second Example

Input:

> We need to modernize a 20-year-old healthcare system currently built on legacy technology.

ProductOS should explore:

```text
Strategic reason for modernization
Business outcomes
User impact
Operational risk
Legacy domain boundaries
Business rules
System dependencies
Data dependencies
Regulatory constraints
Current cost structure
Technical debt
Development productivity
Reliability
Security
Migration risk
Modernization sequencing
Build vs replace
Platform opportunities
AI-assisted legacy understanding
Change management
Measurement
```

It should not immediately answer:

> Rewrite everything in microservices.

---

# 115. Third Example

Input:

> Create our OKRs for the next quarter.

ProductOS should first understand:

```text
Strategy
Business context
Current product outcomes
Major problems
Current metrics
Strategic priorities
Constraints
Time horizon
```

Only then propose objectives and key results.

---

# 116. Fourth Example

Input:

> We need a Product Ops area.

ProductOS should first determine:

```text
What problem is Product Ops expected to solve?

Planning?
Visibility?
Research?
Metrics?
Tooling?
Governance?
Product capability?
Coordination?
Portfolio management?
```

It should avoid creating Product Ops simply because the organizational pattern is fashionable.

---

# 117. First Codex Task

After creating the repository, provide Codex with this instruction:

```text
Read PROJECT_SPEC.md completely.

Do not perform broad Product Management research yet.

Critically inspect this specification first.

Identify:

- architectural inconsistencies;
- unnecessary complexity;
- duplicated domains;
- missing structural components;
- taxonomy risks;
- research scalability risks;
- eval design risks;
- multilingual risks.

Do not simplify the intellectual scope merely to make implementation easier.

Then implement Phase 0 only.

Create:

- repository structure;
- AGENTS.md;
- README.md;
- ARCHITECTURE.md;
- ROADMAP.md;
- research methodology skeleton;
- source quality model;
- terminology model;
- schemas;
- eval strategy skeleton.

Do not populate domain knowledge or frameworks yet.

Keep AGENTS.md concise.

Keep knowledge outside AGENTS.md.

At completion provide:

1. files created;
2. architectural decisions;
3. deviations from PROJECT_SPEC.md;
4. unresolved design questions;
5. risks discovered;
6. recommended next task.
```

---

# 118. Second Codex Task

```text
Perform a ProductOS architecture review.

Do not add Product Management knowledge yet.

Review:

- capability taxonomy;
- domain boundaries;
- repository structure;
- schemas;
- knowledge relationships;
- terminology strategy;
- multilingual architecture;
- source model;
- research workflow;
- eval architecture;
- skill boundaries;
- Product Reasoning Engine.

Look especially for:

- overlapping concepts;
- taxonomy fragmentation;
- knowledge duplication;
- premature infrastructure;
- missing metadata;
- scalability problems.

Simplify only where simplification improves conceptual quality.

Update architecture where justified.

Document all meaningful decisions.
```

---

# 119. Third Codex Task

After architecture stabilization:

```text
Execute Research Wave 1.

Domains:

- Product Sense
- Decision Making
- Systems Thinking
- Product Strategy
- Customer Understanding

For each domain:

1. create research tasks;
2. identify primary sources;
3. research authoritative secondary sources;
4. identify competing schools of thought;
5. synthesize domain knowledge;
6. update concepts;
7. update terminology;
8. update frameworks where relevant;
9. update decision patterns;
10. update anti-patterns;
11. create eval cases;
12. validate all source references;
13. run repository validation.

Optimize for evidence quality and reasoning usefulness.

Do not optimize for content volume.
```

---

# 120. Long-Term Vision

ProductOS should evolve into a shared reasoning substrate for Product Management intelligence.

```text
                         ProductOS

          ┌──────────────────┼──────────────────┐
          │                  │                  │
      Knowledge          Reasoning            Evals
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                         Product Skills
                             │
         ┌───────────────────┼────────────────────┐
         │                   │                    │
      Staff PM            AI PM             Platform PM
         │
    Principal PM
         │
   Product Leader
```

The ultimate question governing the project should always be:

> Does this improve the system's ability to make, support or explain good product decisions?

If the answer is no, the content probably does not belong in ProductOS.