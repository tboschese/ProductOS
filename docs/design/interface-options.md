# ProductOS interface options

**Date:** 2026-10-05  
**Status:** Terminal direction selected by the user; runtime implementation remains proposed

## Decision and recommendation

The user selected a terminal direction with a user-supplied AI connection. ProductOS should
own its reasoning instructions, evidence handling, and decision workflow while allowing the
user to choose the inference service through supported adapters. See the
[proposed terminal AI contract](terminal-ai-contract.md).

The alternatives remain useful if the first-user profile changes. Prefer a local browser
workspace if the initial users are product practitioners who do not use a terminal. The
terminal choice is a user preference and a provisional fit with the repository-native
implementation, rather than observed usability evidence.

The interactive concepts use one illustrative retention scenario. They contain no connected
customer data and do not execute analysis, save decision records, or invoke models.

## Alternatives

| Option | Proposed interaction | Principal trade-off |
|---|---|---|
| Terminal: Command Room | Keyboard navigation between context, evidence, hypotheses, and next action; mouse support | Fits a technical personal workflow; less familiar to users who avoid terminals and less suited to long visual documents |
| Local browser: Decision Studio | Decision memo in the center, sources and uncertainty beside it | Stronger document reading and source inspection; requires a local application runtime and browser lifecycle |
| Desktop: Decision Desk | Decisions organized by investigation, readiness, and follow-up, with a selected decision detail | Familiar installed application; adds packaging, platform updates, and distribution work before demand is established |

The desktop board and browser document are distinct interaction concepts; neither layout
requires its pictured delivery platform. Validate the interaction before choosing packaging.

## Common proposed workflow

1. State the decision and its context.
2. Attach or locate evidence, preserving its source and limitations.
3. Inspect competing hypotheses, options, and material uncertainty.
4. Review a recommendation and its confidence.
5. Record a next action and what evidence would change the decision.

Expose sources and unknowns at the point where they affect the decision. Keep schemas,
validator output, and evaluation administration in a separate maintainer view. A language
choice should affect presentation while preserving the underlying evidence and reasoning.

## Implementation boundary

The current [architecture](../../ARCHITECTURE.md) defines repository-native skills and
deterministic scripts. Product runtime model execution, persisted user workspaces, application
installation, and collaboration are additional work, not existing capabilities of the mockups.
The evaluation-only CLI adapter is not a product runtime contract.

A first terminal increment can explore existing knowledge and repository health and prepare
context for the existing skill. Automated in-app analysis requires an explicit runtime
contract for model invocation, instruction selection, provenance, errors, and cancellation.
Any implementation should preserve the current canonical files and avoid creating a second
source of truth. No SaaS service, new database, or retrieval service is proposed here.

For a Python terminal implementation, [Textual's app documentation](https://textual.textualize.io/guide/app/)
describes keyboard and mouse interaction. It is a candidate, not an installed dependency.
For later desktop packaging, [Tauri](https://tauri.app/start/) supports web frontends; packaging
would remain a separate choice after validating the workflow.

## What would change the recommendation

- First users avoid terminal tools: prioritize the local browser option.
- Frequent document comparison or source review dominates use: favor Decision Studio.
- An installed application is needed for adoption or distribution: consider desktop packaging.
- Repeated use remains entirely in the existing chat: keep the skill as the primary surface.

Observe whether users can start a real decision, identify its missing evidence, and recover the
recommendation's sources without assistance. Record confusion and workflow interruptions
before setting numeric usability targets or committing to broader infrastructure.
