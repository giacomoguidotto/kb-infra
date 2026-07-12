---
status: accepted
---

# Capture uses semantic authoring and non-destructive reconciliation

Capture writes a reconciled Active Canonical View under a lightweight semantic
authoring contract while preserving Revision Evidence behind every accepted
change. Page Type, Ownership, Maturity, and section Kind remain separate axes.
Open Knowledge Format is reserved for a future read-only adapter.

## Context

Capture output varied with the length and tone of the preceding conversation. The
existing `Role` property also combined three different concerns: canonical versus
adapter ownership, raw versus processed content, and archive lifecycle. That made
rules hard for agents to apply consistently and encouraged append-only note
accretion.

The desired KB must avoid duplicate meanings, use no more words than meaning
requires, and remain equally parseable by agents and browsable by people. It must
also keep the active interface relevant without destroying revision history or
source evidence.

Research across controlled authoring, DITA, SKOS, PROV-O, temporal knowledge,
validation, agent memory, and OKF supports a lightweight typed-authoring model. It
does not support a rigid page schema, a formal controlled natural language, or OKF
as the native KB contract. The evidence and limitations are recorded in
[Semantic authoring for Capture, and where OKF fits](../research/semantic-authoring-and-okf.md).

## Decision

- Replace `Role` with orthogonal axes: provider-defined page `Type`, meaning
  `Ownership`, editorial `Maturity`, and section or unit `Kind`.
- Use `Canonical` and `Adapter` for Ownership. Canonical may be implicit only after
  a complete baseline audit and migration establish one owner; Capture still
  checks competing owners before every write. Until then, ownership is explicit or
  `Unresolved`; unresolved ownership blocks a write.
- Default new and unaudited content to `Raw`. Promote it through the Semantic
  Quality Gate to `Developing` or `Stable`. Maturity never means truth,
  confidence, volatility, relevance, lifecycle, or finality.
- Adopt version 1 of the twelve-Kind registry: `State`, `Direction`, `Decision`,
  `Rule`, `Preference`, `Procedure`, `Event`, `Evidence`, `Open item`, `Schema`,
  `Example`, and `Citation`. Use stable IDs and Kind-specific semantic force; do
  not infer Kind from arbitrary headings.
- Keep pages flexible. Require a one-sentence description first, current or
  actionable content before supporting material, and Open questions and Citations
  last. Evidence or qualifier adjacency takes precedence.
- Reconcile the smallest coherent active section instead of merely appending.
  Preserve prior revisions, exact diffs, provenance, time, actor, and semantic
  change relations as Revision Evidence.
- Treat presence in the Active Canonical View as relevance. Remove an irrelevant
  page only after migrating unique durable content, rebinding inbound links, and
  preserving a recoverable deletion or invalidation.
- Require an evidence-bearing Semantic Quality Gate in every Approval Draft.
  `Pass`, `Flag`, `Not checked`, and `Not applicable` results name their scope and
  evidence. Unresolved ownership, contradiction, material omission, unsupported
  assertion, and unsafe deletion block writes.
- Keep visible time and citations selective while making revision provenance
  universal. Retain `observed_at` for every State and `captured_at` for every
  mutation; distinguish both from `event_at`, `valid_from`, and `valid_until`.
- Keep the final form marker only as a rare lookup interaction directive. It is
  not Maturity.
- Treat OKF as a future read-only adapter. Pin its version, map stable provider
  IDs, and export Kinds as a producer extension; keep KB validation stricter.

## Consequences

- Capture and validation work can share one versioned vocabulary and transition
  model instead of deriving structure from conversational tone.
- Existing `Raw` and `Archive` Role values require migration. Raw becomes Maturity;
  archival history becomes Revision Evidence, while irrelevant active pages are
  safely removed. Canonical and Adapter become Ownership.
- Stable content remains revisable and may still be uncertain or volatile when
  that meaning is explicit.
- Human pages stay concise and explorable; machine-oriented evidence can remain
  behind the active view.
- The contract adds semantic judgments that deterministic validators can flag but
  cannot prove. Human approval remains necessary and must not be presented as
  correctness evidence.
- The twelve Kinds are an initial controlled vocabulary, not a claim of
  completeness. Changes require observed ambiguity, a version change, and an
  explicit migration mapping.
- OKF compatibility can be added later without forcing a draft interchange format
  onto native authoring.
