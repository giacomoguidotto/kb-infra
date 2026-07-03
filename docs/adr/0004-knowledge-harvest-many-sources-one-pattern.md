---
status: accepted
---

# Knowledge Harvest observes many sources through one pattern

The automation previously scoped as Knowledge Bank Drift Realignment is renamed and
re-scoped to **Knowledge Harvest**. Its mandate is not to reconcile stale facts but
to **observe the user's activity, surface candidate signals, and populate the KB**
through approved capture. A **signal** is a candidate piece of durable knowledge
worth remembering — a fact, a decision, a stated opinion, a recurring theme, a
project-state change, a working-style pattern. Reconciling KB-internal staleness
(the old "drift" behavior) becomes **one source** among several, alongside git
history and agent transcripts.

Knowledge Harvest is one **pattern** — `observe(source) → generate candidates →
rank/dedup → clarify → capture` — instantiated over many pluggable sources. The
orchestrator fans out **one subagent per source**; each generates ranked candidates
autonomously. The orchestrator merges them with cross-source convergence ranking,
dedups, runs a **single interactive clarify loop** with the user, and hands approved
results to `/capture`. What counts as a signal is itself KB-resident knowledge: a
`signal-preferences` endpoint the user grows through approved rubric updates.

## Context

The original name described a mechanism (reconcile stale facts), but the real intent
is broader: harvest durable knowledge from what the user actually does. The name
quietly constrained the design to its narrowest source, which is why observing
activity outside the KB felt out of scope. Most valuable knowledge is generated in
activity the KB never sees — agentic coding sessions, git history, decisions made in
passing — and the hard part is finding the few gems in a large, noisy corpus.

Two forces shape the design. The corpus is large and noisy, so it must not be read
inline in one context. And the user cannot predict up front what will be valuable,
so a fixed taxonomy of signal types would gate discovery to what is already known.

## Considered options

- **Keep it drift-only, or a report-only audit.** Rejected: it captures the
  narrowest source and misses the mandate. Drift realignment survives as one source
  feeding the shared pattern, not as the whole automation.
- **One monolithic prompt scanning every source inline.** Rejected: it blows up the
  orchestrator's context and is mediocre at each source. Fan-out with one subagent
  per source keeps the main context clean and lets each source own its candidate
  detector.
- **Let the subagents clarify with the user.** Rejected: fanned-out workers run
  autonomously and cannot own the user conversation, and only the orchestrator sees
  every source, so only it can dedup, convergence-rank, and budget questions.
  Subagents self-clarify against their own source; user clarification is central.
- **A rigid, upfront taxonomy of signal types.** Rejected: it gates discovery to
  known types. Instead an **emergent rubric** — a seed of registers plus a permanent
  open "surprising / uncategorised" bucket — grows only from what the user approves.
- **Learn the user's taste from a local rejected-ideas log.** Rejected: correctness
  would then depend on disposable local state (deleting `local/` must not change
  correctness), the log grows unbounded, and it persists sensitive rejected content
  in plaintext. Per [ADR 0001](0001-source-of-record-not-runtime.md), the learned
  criteria are memory and live in the KB as `signal-preferences`. Forward-only
  cursors handle re-surfacing without a suppression log.

## Consequences

- The rename propagates to the glossary, the preamble endpoint vocabulary, and the
  automation spec (`kb-drift-realignment.md` becomes `knowledge-harvest.md`).
  KB-internal staleness is documented as one source.
- The endpoint vocabulary gains `signal-preferences`, framed user-facing as "my
  criteria for what is worth remembering." It grows only through approved rubric
  updates, which are rendered as a **distinct block** in the `/capture` draft,
  separate from the signals themselves, so changing the criteria is a deliberate
  approval and not a rubber-stamp.
- Agent transcripts are read from a `transcript-source` binding, referenced by role
  and bound at setup per [ADR 0002](0002-personal-specifics-are-bindings.md), so the
  spec stays provider-agnostic across whichever agents the user runs.
- State stays disposable: a **forward-only per-source cursor** bounds each run and
  handles dedup, with a bounded backfill on first run. No local rejection log.
- Each subagent returns ranked candidates carrying evidence, provenance (source,
  session, timestamp), a confidence, and a one-line "why this might be a signal."
- Transcript-derived signals are **private by default** and never auto-flow to the
  public-safe or social surfaces without separate approval.
- The per-sitting question count is soft guidance to avoid an endless grill, not a
  hard cap; eager recall internally is paired with bounded surfacing externally.
