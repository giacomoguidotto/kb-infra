---
status: accepted
---

# ADR 0013: Social Draft Pulse starts with a performance feedback loop

## Context

Social Draft Pulse could read account analytics, but the workflow used them mainly
to justify optional posting-window tests later in a run. It did not require each run
to begin by asking what worked, what did not, and whether recent evidence should
change the next candidate set.

That made drafting too open-loop. Recent account results and current external
signals could be available while candidate generation still followed the previous
direction unchanged. At the other extreme, reacting to only one post or a short
spike would overfit noise.

## Decision

- Every Social Draft Pulse run begins with publication history and account analytics
  for posts since the previous pulse, supplemented by a comparable trailing baseline
  when the recent sample is too small or immature.
- The review classifies evidence as worked, did not work, or inconclusive across
  content lane, angle, hook, format, framing, audience assumption, and posting time.
  It states limitations and does not infer causation from correlation.
- Every run also performs a bounded scan of relevant current external signals before
  candidate generation. Primary sources and direct public evidence outrank generic
  trend summaries. External attention does not create a user stance or validate a
  claim by itself.
- Declare that read through `<external-signal-source>` and its
  `current-public-signals` capability so setup must bind a concrete public research
  surface before materializing an enabled automation.
- After the KB lookup, the run combines strategy, performance, and external evidence
  into one explicit decision: hold, refine, test, or realign. The approval summary
  leads with this decision and the evidence behind it before listing candidates.
- Sparse or conflicting evidence defaults to holding direction or proposing a
  bounded test. It does not justify a wholesale strategy or schedule change.
- A run may adapt its proposed content mix, angles, format, framing, sequence, and
  controlled timing tests. KB strategy changes and recurring schedule changes remain
  proposal-driven and approval-gated through their existing paths.

## Consequences

- Social drafting becomes a closed feedback loop rather than a context-only content
  generator.
- The user can inspect the reasoning behind each new batch before approving it.
- Analytics remain live source evidence, not durable KB records.
- External-signal scanning happens every run, while the slower platform-rule refresh
  cadence remains a separate concern.
- Missing analytics or external evidence produces an explicit degraded-mode report,
  not invented benchmarks or a silent skip.
