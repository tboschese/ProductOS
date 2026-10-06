# Source quality model

## Purpose

The source model records provenance without treating authority labels as automatic truth. Evaluation occurs at both source and claim level.

## Authority classes

| Level | Typical source |
|---|---|
| A | Primary data, original research, standards, regulation, or original framework author |
| B | Peer-reviewed work or high-authority research institution |
| C | Strong empirical industry practice or transparent company research |
| D | Recognized practitioner synthesis |
| E | Community discussion or anecdotal experience |

Authority describes origin. Reviewers must separately assess:

- relevance to the claim and context;
- methodological quality;
- recency and temporal stability;
- sample and population limitations;
- incentives and conflicts of interest;
- directness versus interpretation;
- corroborating and contradicting evidence.

## Source acceptance

A source record requires identity, authorship or organization, publication year when available,
URL, language, type, access level, authority class, summary, limitations, verification date,
temporal stability, and review interval.

Missing metadata must be represented as unknown rather than inferred. Paywalled or restricted access is recorded explicitly.

The current source contract is `schema_version: 0.3.1`. When migrating an older source record,
add freshness metadata and update its schema version and metadata review date. Preserve
`last_verified` unless source metadata and access were actually checked again.

## Claim provenance

Material claims cite source IDs with precise locators such as page, section, table, timestamp, dataset slice, or quoted heading. A bare URL is not sufficient provenance for an approved claim.

Claims record supporting and contradicting references separately. Reviewers assign qualitative confidence only after considering relevance and limitations.

## Freshness

`last_verified` records when the source metadata and access path were checked. Review cadence depends on volatility: laws, market data, product documentation, and platform behavior require more frequent review than stable historical material.

Each source classifies its temporal stability and records an explicit review interval:

- `stable`: the underlying publication is not expected to change, although access and metadata
  can still decay;
- `evolving`: maintained guidance, standards, or syntheses may change between reviews;
- `volatile`: laws, product documentation, market data, policies, or platform behavior can change
  quickly.

The label does not set the interval automatically. Curators choose and justify a cadence that is
proportionate to the claim's use and the cost of stale guidance. `scripts.audit_sources` computes
the next due date deterministically from `last_verified` and `review_interval_days`. Optional URL
probing is a best-effort access check, not proof that source content is unchanged.

## Copyright and privacy

Store metadata, short compliant excerpts when necessary, and original synthesis. Do not commit full copyrighted works, restricted datasets, personal research data, credentials, or confidential company information.
