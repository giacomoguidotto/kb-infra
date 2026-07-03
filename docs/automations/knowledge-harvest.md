# Knowledge Harvest Automation

Prompt source for the scheduled automation that harvests **signals** from the user's
activity and populates the KB through `/capture`. Include [the preamble](_preamble.md)
when materializing this automation. This file is a reviewable source prompt before it
is copied into the harness automation settings.

## Design

Knowledge Harvest is an observe-to-capture loop, not a report-only audit. It runs one
pattern — `observe(source) → generate candidates → rank/dedup → clarify → capture` —
over many sources.

- Orchestrator + workers: the orchestrator fans out **one subagent per source**; each
  runs `observe → generate candidates` autonomously in its own context. Sources:
  KB-internal staleness (the Drift Audit), git history, and each bound
  `<transcript-source>`.
- Subagent contract: each returns a ranked list of candidate signals, each carrying
  evidence, provenance (source, session/commit, timestamp), a confidence, and a
  one-line "why this might be a signal." Subagents self-clarify against their own
  source; they never ask the user.
- Merge in the orchestrator: dedup and **convergence-rank** — a candidate seen in more
  than one source outranks a one-off — then run a single interactive clarify loop.
- Ranking rubric: read `signal-preferences` to rank candidates. It is an emergent
  rubric — a seed of registers plus a permanent open "surprising/uncategorised"
  bucket — so novel signal types can still surface.
- Question loop: one question at a time, grouped by register. A soft ceiling keeps a
  sitting from becoming an endless grill; it is guidance, not a hard cap.
- Answer outcomes: answered update, deferred follow-up marker candidate, final-form
  marker candidate, discarded finding, or unresolved question.
- Write path: hand the clarified result to `/capture`; KB writes happen only after
  approval of the latest exact draft. Rubric updates for `signal-preferences` are
  proposed as a **distinct block** in the capture draft, separate from the signals.
- State: forward-only per-source cursor (mechanical `local/` hint), bounded backfill
  on first run. No local rejection log — dedup comes from the cursor, learned taste
  from `signal-preferences`.
- Privacy: transcript-derived signals are private by default and never auto-flow to
  public-safe or social surfaces.

## Prompt

```md
You are running Knowledge Harvest.

The preamble is prepended to this prompt at materialize time.

Setup:
- Read this repo's AGENTS.md, docs/workflows.md,
  docs/knowledge-bank-conventions.md, docs/automations/_preamble.md,
  skills/lookup/SKILL.md, and skills/capture/SKILL.md before acting.

Goal:
- Observe the user's recent activity across sources, surface candidate signals,
  and populate the KB.
- Merge and rank candidates, ask the user one question at a time until each is
  answered, deferred, discarded, converted into a final-form marker candidate, or
  left explicitly unresolved.
- After clarification, use /capture in this same thread to draft the exact KB
  write proposal and wait for approval.

Fan out, one subagent per source:
- Spawn one subagent for each source: KB-internal staleness, git history, and each
  bound <transcript-source>. Each subagent works only in its own context.
- Each subagent runs observe -> generate candidates and returns a ranked list.
  For every candidate include: the evidence, provenance (source, session/commit,
  timestamp), a confidence, and a one-line "why this might be a signal."
- Subagents may self-clarify by reading more of their own source (more transcript
  turns, git log, the KB page). They never ask the user.
- Bound each source by its forward-only cursor from local state; on first run do a
  bounded backfill, not the whole history.

Per-source guidance:
- KB-internal staleness (Drift Audit): find holes, stale current-state prose, due
  follow-up markers, and raw or ambiguous prose (relative-time phrases, "current",
  "for now"). Treat due follow-up markers as first-priority.
- Git history: compare project pages (start from selected-projects) against recent
  local git history when the clone is available, or remote history when it is not.
  Ignore mechanical churn unless it changes durable project state.
- Transcript sources: mine agent conversation transcripts for decisions, stated
  opinions, recurring themes, friction points, working-style patterns, and the gap
  between what was set out and what shipped. Keep these private by default.

Merge and rank:
- Dedup across sources and convergence-rank: a candidate corroborated by more than
  one source outranks a one-off.
- Read signal-preferences and rank candidates by it. Keep an open bucket for
  surprising candidates that fit no recorded register.

Question style:
- Before the first question, say how many candidates were found, per source, and
  which group comes first.
- Group by register: due follow-ups, project drift, dated task signals, life or
  identity updates, decisions/opinions/themes from activity, other stale, missing,
  or ambiguous findings, then low-confidence findings.
- Include the page or source, the evidence, and why the question matters.
- Keep the sitting from running forever: when it has gone long, say how many
  candidates remain and ask whether to continue or defer. This is a soft ceiling,
  not a hard cap.
- A normal discard leaves no KB trace. Use the marker formats from
  docs/knowledge-bank-conventions.md.

Capture:
- Feed answered updates, marker candidates, discarded findings, and unresolved
  questions into /capture.
- When a discard or a pattern implies a change to what counts as a signal, propose
  a signal-preferences rubric update as a distinct block in the capture draft,
  clearly separated from the signal writes, so the user approves it deliberately.
- Apply KB writes only after the user approves the latest exact /capture draft.

End state:
- Do not stop after the candidate lists.
- Transcript-derived signals stay private by default; never route them to
  public-safe or social surfaces.
- After the run, advance each source cursor in local state.
```
