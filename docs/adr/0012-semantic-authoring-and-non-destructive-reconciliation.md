---
status: accepted
---

# Capture uses semantic authoring and reconciliation

## Context

Capture output inherited the preceding conversation's tone and encouraged
append-only notes. The old `Role` property also mixed ownership, editorial maturity,
and lifecycle.

The KB needs consistent meaning without rigid page templates: no duplicate owners,
no avoidable words, and content that agents can parse while people can browse. The
[research](../research/semantic-authoring-and-okf.md) supports lightweight typed
authoring and provenance, not a formal controlled language or OKF as the native KB
model.

## Decision

- Keep page `Type`, meaning `Ownership`, editorial `Maturity`, and section `Kind`
  independent.
- Choose Type from the page's primary purpose. Durable prose inside an Area,
  Project, or Task does not turn it into a Knowledge page.
- Treat provider views as human projections. Operational views show work; knowledge
  views show reference material without duplicating either.
- When one Parent/Subtasks hierarchy contains both work and knowledge, require
  Type-aware views so knowledge does not appear as work.
- Use `Canonical` and `Adapter` Ownership, with `Unresolved` only during migration.
- Default intake to `Raw`; promote reconciled knowledge to `Developing` or `Stable`.
- Use the twelve stable Kinds defined in
  [Knowledge Bank Conventions](../knowledge-bank-conventions.md).
- Reconcile the smallest coherent active section instead of appending session
  summaries.
- Preserve recoverable revision evidence and remove irrelevant pages only after
  unique content and inbound links are safe.
- Block Capture on unresolved ownership, contradiction, unsupported content,
  material omission, or unsafe deletion.
- Treat OKF as a future read-only adapter.

The conventions document owns the operational detail. Capture carries only the
compact subset it needs when materialized outside this repo. No executable semantic
contract is required: deterministic code cannot prove the judgments that matter,
and exact HTML approval plus live re-read and read-back provide the safety boundary.

## Consequences

The active KB stays concise and relevant while history remains recoverable. Stable
content remains revisable. Semantic changes require human judgment, so the protocol
optimizes for a legible approval surface rather than machine-generated evidence
volume.
