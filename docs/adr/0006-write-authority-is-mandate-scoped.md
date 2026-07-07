---
status: accepted
---

# Write-authority is mandate-scoped; Knowledge Harvest reconciles

Every automation may write knowledge from its own run into its **mandate surfaces** —
the KB (through `/capture` approval) and its sink — while the context is hot, rather
than staying "draft-only" and leaving all KB writes to Knowledge Harvest. Authority is
**scoped to the mandate** and to what the run handled explicitly in-context; anything
cross-cutting, ambient, or requiring inference across runs stays with Knowledge
Harvest. Harvest is repositioned from primary author of KB knowledge to **reconciler**:
it dedups first-party captures against current KB state, proposes what a run should
have captured but did not, and surfaces conflicts.

## Context

The repo carried two contradictory write-authority models. The draft-only automations
(Social Draft Pulse, Portfolio Surface Sweep, the Job Hunt audits) declared they do
not write to the KB, while Knowledge Harvest was scoped to populate the KB by mining
those same automations' transcripts ([ADR 0004](0004-knowledge-harvest-many-sources-one-pattern.md)).
Harvest was therefore positioned to re-derive, from a cold transcript, knowledge an
automation held hot in context and was forbidden to write — lossy, latent, and a
double-write collision waiting to happen (Harvest re-proposing a stance Social Draft
Pulse already elicited at its gate).

`/capture` was already a skill any automation invokes; the invariant was never "only
Harvest writes" but "never write except through `/capture` approval." So the fix makes
an existing capability explicit and deletes the contradicting "draft-only, does not
write to the KB" language.

## Considered options

- **Keep automations draft-only; Harvest owns all KB writes.** Rejected: it re-derives
  hot context from cold transcripts, delays learning until a later harvest, and sets
  up double-writes.
- **Open write-authority — any automation captures anything it judges worth saving,
  Harvest sorts it out.** Rejected: it multiplies approval surfaces, pushes all dedup
  and taste-conflict resolution onto Harvest after the fact, and lets a narrow
  automation make judgments it has no context for.
- **Mandate-scoped first-party capture + Harvest as reconciler (chosen).** Each
  automation writes in-mandate, in-context knowledge to the KB and/or its sink;
  Harvest reconciles against KB state and backstops misses and conflicts.

## Consequences

- The preamble gains a mandate-scoped write rule and repositions Harvest as
  reconciler. The rule lives once in the Operating Rules per
  [ADR 0005](0005-materialized-automation-is-self-contained.md), not restated per
  prompt.
- "Writes to the KB" and "publishes to a sink" stay distinct invariants. Relaxing an
  automation's "does not write to the KB" does not touch "does not post, schedule, or
  publish"; inbound KB capture is low-risk, auto-publishing to a public sink stays
  forbidden.
- Capture is signal-triggered, not forced. An automation improves on itself only when
  a run surfaces a real signal worth storing; it proposes a `/capture` then, and an
  empty run captures nothing.
- First-party capture carries sink reconciliation, and the obligation depends on the
  sink's kind. A **mirror sink** holds its own copy of a KB endpoint (`career-system`
  copies `job-search-strategy`) and is realigned when that endpoint changes —
  bidirectional drift. A **derived sink** is materialized one-way from KB signals
  (`portfolio`, `social-draft-queue`) and carries no inherited drift. Only mirror
  sinks ever produced inherited drift, which is why a Tune Audit existed for the Job
  Hunt system and not for the portfolio or social surfaces.
- Harvest's reconciliation generalizes its Drift Audit source: it already checks
  KB-internal staleness; it now also checks whether the KB reflects what the
  automations' own runs implied. A transcript signal already present in its canonical
  owner is discarded or downgraded to confirmation; a miss is proposed; a walk-back is
  surfaced as drift.
- Harvest proposals that would land on public-facing surfaces (`point-of-view`,
  `public-safe-claim-source`, `published-social-context`) still honor ADR 0004's
  private-by-default boundary — rendered as a distinct, explicit-consent block in the
  `/capture` draft. First-party captures onto those surfaces are safe because the
  owning automation proposes them in-context with the user present.
- Reconciliation-only audits become candidates for absorption. Job Hunt Tune Audit,
  whose whole job is to reconcile `job-search-strategy` with the `career-system`
  sink's personalization, is the first: it is retired and its functions move to Job
  Hunt Evaluate Audit in [ADR 0007](0007-job-hunt-evaluate-absorbs-tuning.md).
  Deprecating such an audit is safe only if continuous KB→sink propagation now owns
  the sync it used to perform, or drift silently returns.
- The concrete per-automation wiring — which surfaces each automation captures, what
  each propagates to its sink, and which audits are deprecated — is evaluated
  automation-by-automation in follow-up. This ADR fixes only the write-authority model
  and Harvest's role.
