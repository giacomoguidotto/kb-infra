---
status: accepted
---

# Job Hunt Evaluate absorbs tuning; the Tune Audit is retired

Applying [ADR 0006](0006-write-authority-is-mandate-scoped.md) to the Job Hunt trio:
Job Hunt Tune Audit is **retired**, and its two functions move to the automations
already in the career-system loop. Job Hunt Evaluate Audit gains a narrow
`job-search-strategy` mandate — it realigns the `career-system` mirror copy from the
KB on every run and first-party-captures a strategy signal when one surfaces — and Job
Hunt Advance Audit first-party-captures `personal-constraints` and targeting
preferences it hears in-context. Knowledge Harvest backstops both and flags mirror
drift it cannot fix.

## Context

Job Hunt Tune Audit existed only to reconcile the KB's `job-search-strategy` with the
`career-system` sink's copy of it — the reconciliation-only audit ADR 0006 flags for
absorption. `career-system` is the only **mirror sink** (it stores a copy of a KB
endpoint); `portfolio` and `social-draft-queue` are derived sinks with no inherited
drift, which is why only Job Hunt ever had a Tune Audit.

The Tune Audit did two things: (F1) propagate KB strategy into the career-system
config, and (F2) turn career-system signals — tracker/report patterns showing weak
leads — into strategy changes. Under mandate-scoped write-authority, F2 is first-party
capture by whoever generates those signals (Evaluate), and F1 is continuous KB→sink
propagation by whoever runs the loop (Evaluate). Nothing unique remains for a
standalone audit.

## Considered options

- **Keep the Tune Audit.** Rejected: once Evaluate propagates strategy continuously and
  captures strategy signals, a separate periodic tuning pass is redundant and adds an
  approval surface.
- **Put the mirror sync on Advance.** Rejected: Advance idles when Evaluate has pending
  work and only runs when there are opportunities to advance, so it cannot own
  *continuous* propagation.
- **Let Harvest realign the mirror.** Rejected: Harvest writes the KB, not sinks; it can
  flag mirror drift but must not fix it.
- **Evaluate absorbs both functions (chosen).** It runs the loop on cadence and already
  git-syncs the clone, so it is the natural home for continuous KB→sink realignment and
  for capturing strategy signals its own evaluations surface.

## Consequences

- Job Hunt Evaluate Audit is **no longer KB-free**: it does a narrow `/lookup` of
  `job-search-strategy`, realigns the career-system copy from the KB, and captures a
  strategy signal only when a run surfaces one (signal-triggered, so most runs still
  capture nothing). This concentrates more responsibility in one automation; accepted
  now, and it may be split later if it grows unwieldy.
- Deleting the Tune Audit is safe **only because** Evaluate now owns continuous mirror
  realignment; without that, KB↔career-system drift would silently return.
- Mirror realignment propagates already-approved KB state into the career-system
  user-layer config; it is proposed in the run summary and applied as a user-layer
  change, distinct from the KB `/capture` that approved the strategy itself, and never
  touches shared system defaults.
- `job-hunt-tune-audit.md`, its workflow section, its glossary entry, and its
  cadence/binding slot are removed. Advance gains `job-search-strategy` to its
  on-demand endpoints.
