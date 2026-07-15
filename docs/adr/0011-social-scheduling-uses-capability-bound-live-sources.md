---
status: accepted
---

# Social scheduling uses capability-bound live sources

Social Compose derives coverage from a provider-neutral social publishing
source and a private availability calendar source. The committed automation declares
the read capabilities it needs; setup binds those roles to concrete local tools and
accounts. Published Social Context remains a semantic KB ledger, not a mirror of
those operational systems.

## Context

The original scheduling design treated one provider as the named publication source
and used a weekday-specific late-run example. That was enough to schedule approved
drafts, but it mixed a local implementation with the generic spec and left three
questions implicit:

- how a run learns which recurring slots are enabled and still open;
- how planned travel, events, and next-day recovery affect a multi-day coverage
  window without leaking private calendar details into content;
- how account-specific analytics can test better posting windows without allowing an
  automation to rewrite the schedule after a small sample.

Raw publication history and metrics also do not belong in the KB. The durable value
is their semantic effect: what each platform's audience can now be assumed to know
and how the user's broader public arguments have progressed.

## Decision

- Replace the provider-named publication source with
  `<social-publishing-source>` and add `<availability-calendar-source>`.
- Declare live read operations as source capabilities: `publication-history`,
  `post-analytics`, `queue-timeline`, `queue-schedule`, and
  `upcoming-availability`. Setup resolves each role to a concrete, read-only command
  or native workflow instruction in gitignored bindings and injects only declared
  capabilities into the materialized prompt.
- Extend ADR 0002's binding taxonomy with external sources and source capabilities.
  Personal and provider-specific values still live only in gitignored bindings.
- When coverage depends on the next scheduled run, declare that dependency and
  materialize the automation's human-readable recurrence and timezone into the
  self-contained prompt. This is operational context, not a hardcoded generic
  cadence.
- Size each run from recurring enabled slots that remain open and eligible across
  its coverage window. The spec contains no fixed daily count or weekday-specific
  expansion; the schedule and KB rules are the runtime authority.
- For multi-day coverage, reduce upcoming calendar evidence to day and slot
  eligibility using the KB's availability and recovery rules. Event details are
  private scheduling inputs and may not become post ideas, evidence, or public copy.
- Use account analytics to propose controlled testing windows with a hypothesis,
  comparable baseline, repeated observation window, and success measure. An approved
  test uses an explicit scheduled time. Social Compose never changes the
  recurring schedule autonomously.
- Keep Published Social Context as a per-platform semantic audience and argument
  ledger with canonical-owner links. After posts go live, batch the semantic delta
  through `/capture`; do not copy post bodies, raw publication records, queue state,
  analytics, or concepts already owned elsewhere in the KB.
- Supersede ADR 0003's raw publication-ledger description and its per-run volume
  target. The point-of-view and introduce-on-first-use decisions remain in force.

## Consequences

- ADR 0002's original three-kind taxonomy, ADR 0003's raw-ledger and per-run-volume
  clauses, ADR 0005's blanket cadence-exclusion clause, and ADR 0010's
  provider-specific source shape and weekday example are superseded by this ADR.
  Their remaining decisions stay in force; cadence is still excluded unless an
  automation explicitly declares it as required coverage context.
- A social publishing tool may be bound both as a read-only source and as the
  approval-gated draft/scheduling sink; source capabilities never grant write
  authority.
- A calendar connector can improve scheduling without broadening the public content
  boundary or making the calendar a KB mirror.
- Analytics can improve the account's schedule over time, but schedule changes
  remain proposal-driven and evidence-backed.
