# Terminology model

## Purpose

Terminology maps multiple practitioner expressions to one stable concept without creating separate language-specific knowledge systems.

## Canonical representation

- IDs and canonical names use English.
- IDs are lowercase kebab-case and remain stable when display labels change.
- Locales initially supported for interaction are `en`, `pt-BR`, and `es`.
- Established names such as Jobs to Be Done, RICE, and Product-Market Fit are preserved when practitioners normally use the English form.

## Localized terms

Each locale may define:

- `preferred`: the default display term;
- `aliases`: accepted variants and abbreviations;
- `notes`: ambiguity or usage guidance.

Aliases are for recognition and retrieval. They do not create new concepts.

## Ambiguity

Potentially ambiguous aliases require a terminology note. The same normalized alias should not point to multiple active concepts in the same locale unless the ambiguity is explicitly documented and handled by context.

## Translation policy

Translate meaning, not surface form. A localized response should preserve technical precision, natural practitioner language, and equivalent reasoning. Localization must not alter evidence strength, confidence, or recommended action.

## Change control

Renaming a preferred label is non-breaking when the canonical ID remains stable. Splitting or merging concepts requires an architecture or editorial decision, redirects from deprecated IDs, and regression coverage.
