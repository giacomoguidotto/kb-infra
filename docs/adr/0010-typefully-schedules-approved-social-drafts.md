---
status: accepted
---

# Typefully schedules approved social drafts

The provider-specific source shape and weekday example in this decision are
superseded by [ADR 0011](0011-social-scheduling-uses-capability-bound-live-sources.md).
Its approval gate, scheduling permission, and no-immediate-publish boundary remain
in force.

Typefully is now the scheduling sink for approved Social Draft Pulse posts. Social
Draft Pulse still stops at the idea-summary gate before creating anything, but after
approval it may create and schedule drafts in Typefully across the run's coverage
window. It must not publish immediately unless the user gives an explicit
publish-now instruction.

## Context

ADR 0009 kept Social Draft Pulse draft-only because the social sink could not
schedule and because publication needed to remain deliberate. The account now has
Typefully Pro with enough monthly post capacity for the intended cadence, so leaving
approved drafts unscheduled creates avoidable manual work and makes late-day runs
awkward.

The schedule remains a strategy dial owned by `social-rules-of-engagement`. The
machine-specific Typefully account details remain bindings.

## Decision

- After approval, Social Draft Pulse creates and schedules Typefully drafts.
- Immediate publishing remains out of scope unless the user explicitly asks for it.
- Typefully published and queue state are live context for Social Draft Pulse, so
  the workflow can avoid duplicates and understand what is already scheduled or live.
- If the automation fires late in the day, it schedules the approved run volume over
  the next coverage days instead of compressing posts into the remaining evening.
  For a Wednesday late-afternoon run, that means Thursday and Friday.

## Consequences

- ADR 0009's draft-only scheduling stance is superseded by this decision; its
  schedule-aware drafting and public-profile reconciliation rules still stand.
- The local binding can declare Typefully Pro scheduling behavior and quota without
  committing personal account details into the generic spec.
- Published Social Context is still updated through `/capture` only after posts are
  actually live. Typefully provides evidence; it is not the KB ledger.
