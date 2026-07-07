---
status: accepted
---

# Social and portfolio sweeps under mandate-scoped capture

Applying [ADR 0006](0006-write-authority-is-mandate-scoped.md) to the two derived-sink
automations, the outcome is **asymmetric**. Social Draft Pulse gains an explicit
first-party-capture mandate over `point-of-view` and `published-social-context`, so it
stops being "draft-only, does not write to the KB". Portfolio Surface Sweep gets an
**empty** capture mandate — it consumes public-safe KB claims and writes only to the
`portfolio` sink, originating no durable KB knowledge — and keeps "does not write to the
KB" as a legitimate mandate, not a contradiction. Neither sink is a mirror, so neither
realigns a KB copy.

## Context

Both sinks are **derived**: `social-draft-queue` and `portfolio` are materialized
one-way from KB signals and carry no inherited drift, so mirror realignment (the
career-system case in [ADR 0007](0007-job-hunt-evaluate-absorbs-tuning.md)) does not
apply here. The only open question per automation is what, if anything, falls inside
its first-party-capture mandate.

Social Draft Pulse already elicited durable knowledge in its runs and handed it to
`/capture` while declaring it "does not write to the KB" — the exact contradiction
ADR 0006 removes, and the ADR's own motivating example (Harvest re-deriving "a stance
Social Draft Pulse already elicited at its gate"). A user's stated take at the gate is a
run-surfaced signal SDP owns; the audience ledger is the persona/audience state ADR 0003
says SDP models. Both are SDP's surfaces.

Portfolio Surface Sweep, by contrast, reads public-safe claims and proposes portfolio
changes. It surfaces *gaps* (unsupported claims), which are absences, not captures, and
stale KB claims are Knowledge Harvest's drift job. Nothing it handles in-context
originates KB knowledge, so its capture mandate is genuinely empty — and ADR 0006 does
not force a run to capture.

## Considered options

- **Give both automations a capture mandate for symmetry.** Rejected: PSS originates no
  durable KB knowledge, so a mandate would invent captures it has no source for.
- **Keep SDP draft-only and let Harvest author `point-of-view`.** Rejected by ADR 0006:
  it re-derives hot context from a cold transcript and sets up the double-write that ADR
  names directly.
- **Have SDP capture `published-social-context` mid-run.** Rejected: the signal (a post
  going live) fires after the scheduled run, not during it, and SDP never posts.
- **Asymmetric mandates (chosen).** SDP captures `point-of-view` and
  `published-social-context`; PSS captures nothing. Each mandate matches what the run
  actually originates.

## Consequences

- Social Draft Pulse loses its "does not write to the KB" language. It first-party-
  captures a `point-of-view` signal when the user states a take at the gate, and the
  `published-social-context` ledger update — both onto public-facing surfaces, so each
  is proposed through `/capture` as a distinct, explicit-consent block per
  [ADR 0004](0004-knowledge-harvest-many-sources-one-pattern.md)'s private-by-default
  boundary.
- `published-social-context` capture is **trigger-deferred**: the signal is a live post,
  which happens outside the scheduled run and only on the user's action. SDP captures it
  when a run actually has the signal (the user confirms posting), otherwise it records
  the ledger update as a capture-at-post-time note, with Harvest as backstop. The "SDP
  never auto-posts" invariant is untouched.
- The "KB rule realignment candidate" for `social-rules-of-engagement` stays
  **out-of-mandate**: it is a tunable rules/binding dial ([ADR 0002](0002-personal-specifics-are-bindings.md),
  ADR 0003), not run-surfaced knowledge. SDP keeps surfacing it in the summary and does
  not write it.
- Portfolio Surface Sweep keeps "does not write to the KB", now framed as an empty
  capture mandate rather than a blanket ban. Its Design block states the derived sink and
  the empty mandate so the model is legible; the prompt body is unchanged.
- [ADR 0003](0003-social-draft-pulse-models-audience-state.md)'s "stays draft-only"
  clause is superseded for the KB-write half; the sink-publish half ("draft only; do not
  post") stands, since ADR 0006 keeps "writes to the KB" and "publishes to a sink" as
  distinct invariants.
