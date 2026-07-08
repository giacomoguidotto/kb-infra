---
status: accepted
---

# Schedule-aware drafts and profile-reconciled published context

Two changes land together as the social surfaces mature. First,
`social-rules-of-engagement` gains ownership of **posting slots** (the per-platform
schedule of when to post) and the **intended tone for each slot**, and Social Draft
Pulse reads them to recommend a slot and a slot-matched tone per draft — still
draft-only, never scheduling into the sink. Second, `published-social-context` gains a
reconciliation path that does not depend on the sink publishing: a read-only, per-
platform `<social-profile-source>` (currently X and LinkedIn) that Knowledge Harvest
observes **best-effort** to reconcile the ledger, degrading to a manual confirmation
question where a platform cannot be read.

Both are memory or tunable dials, so both live where the model already keeps them: the
schedule and tone are a `social-rules-of-engagement` dial per
[ADR 0002](0002-personal-specifics-are-bindings.md), and the profile source feeds the
KB-resident ledger through the reconciler named in
[ADR 0008](0008-social-and-portfolio-sweeps-under-mandate-scoped-capture.md).

## Context

The user tuned a set of posting slots with an intended tone for each moment, and that
schedule had no home: `social-rules-of-engagement` owned volume and content mix but not
*when* to post or *how* each slot should sound. Drafts therefore carried no timing or
per-slot voice.

At the same time the social sink is a free-tier draft tool that does not publish or
schedule. The `published-social-context` post-time capture trigger
([ADR 0008](0008-social-and-portfolio-sweeps-under-mandate-scoped-capture.md)) fires
when a post goes live *through the sink*, which never happens here, so the ledger has no
update path and stalls. [ADR 0003](0003-social-draft-pulse-models-audience-state.md)
foresaw a bootstrap read of the platforms but rejected *ongoing* dependence on the paid
timeline APIs; it left open that "a one-time export or manual seed may bootstrap the
ledger." The changed constraint — a sink that cannot carry the trigger — turns that
one-time allowance into a standing need for a reconciliation source.

## Considered options

- **Add a new `posting-schedule` endpoint.** Rejected: scheduling and per-slot tone are
  drafting strategy, which `social-rules-of-engagement` already owns. A second endpoint
  proliferates surfaces for no gain (the "simplify the endpoints" instinct).
- **Have Social Draft Pulse schedule into the sink.** Rejected: it breaks the draft-only
  invariant ([ADR 0003](0003-social-draft-pulse-models-audience-state.md),
  [ADR 0006](0006-write-authority-is-mandate-scoped.md),
  [ADR 0008](0008-social-and-portfolio-sweeps-under-mandate-scoped-capture.md)), and the
  free tier cannot schedule regardless. SDP *suggests* a slot; it does not commit one.
- **Keep relying on the sink's post-time trigger.** Rejected: the free-tier sink never
  fires it, so the ledger has no update path at all.
- **Read the profiles from Social Draft Pulse directly.** Rejected: Knowledge Harvest is
  already the ledger's reconciler and backstop
  ([ADR 0008](0008-social-and-portfolio-sweeps-under-mandate-scoped-capture.md)) and
  already runs one pattern over many sources
  ([ADR 0004](0004-knowledge-harvest-many-sources-one-pattern.md)). A public source
  reconciling a public-facing surface belongs on that pattern, not bolted onto the
  draft loop.
- **Read the paid timeline APIs** — the mechanism
  [ADR 0003](0003-social-draft-pulse-models-audience-state.md) rejected. Still rejected:
  costly and fragile. This ADR instead reads the *public profile surface* best-effort;
  a headless browser or scraper **may** manage it, but reliability is not assumed, so
  the source degrades to a manual confirmation question where a platform (notably
  LinkedIn, which blocks logged-out reads) cannot be read.

## Consequences

- `social-rules-of-engagement` widens to own posting slots and per-slot tone, as tunable
  dials per [ADR 0002](0002-personal-specifics-are-bindings.md). The concrete slots and
  tones live in the KB, so refining them never needs a spec change.
- Social Draft Pulse reads the schedule and, for each candidate and draft, recommends a
  time slot and writes the draft in that slot's tone. It stays draft-only: the slot is a
  suggestion in the idea summary and a note on the draft, never a scheduled post.
- The preamble Sources vocabulary gains `<social-profile-source>` — read-only, per-
  platform, public. Knowledge Harvest declares it, observes it best-effort, and
  reconciles candidate ledger updates into `published-social-context`, falling back to a
  clarification question when a platform is unreadable.
- The flow is public-to-public — a public profile reconciling a public-facing ledger —
  so it does not touch Knowledge Harvest's private-by-default rule, which governs
  transcript-derived signals
  ([ADR 0004](0004-knowledge-harvest-many-sources-one-pattern.md)).
- [ADR 0003](0003-social-draft-pulse-models-audience-state.md)'s rejection of platform
  reads is **superseded for the public-profile-read case**; its rejection of the paid
  timeline APIs and its draft-only stance both stand.
- Setup collects `<social-profile-source>` as a per-platform binding, like a sink; where
  a platform is unreadable the ledger update falls back to a Harvest question rather than
  a fabricated entry.
