# Knowledge Bank Drift Realignment Automation

Prompt source for the scheduled automation that uses `/lookup` in clarification
mode, then `/capture`. Include [the preamble](_preamble.md) when materializing
this automation. This file is a reviewable source prompt before it is copied into
the harness automation settings.

## Design

Knowledge Bank Drift Realignment is a lookup-to-capture loop, not a report-only
audit.

- lookup branch: clarification, to find stale, missing, due, raw, ambiguous, or
  project-drift candidates.
- Endpoints: the whole KB is in scope; start from `selected-projects` and expand.
- Question loop: one question at a time, soft cap of 10 per sitting.
- Answer outcomes: answered update, deferred follow-up marker candidate,
  final-form marker candidate, discarded finding, or unresolved question.
- Write path: hand the clarified result to `/capture`; KB writes happen only after
  approval of the latest exact draft.

## Prompt

```md
You are running Knowledge Bank Drift Realignment.

The preamble is prepended to this prompt at materialize time.

Setup:
- Read this repo's AGENTS.md, docs/workflows.md,
  docs/knowledge-bank-conventions.md, docs/automations/_preamble.md,
  skills/lookup/SKILL.md, and skills/capture/SKILL.md before acting.

Goal:
- Find KB holes, stale facts, due follow-ups, raw or ambiguous current-state
  prose, and project drift.
- Ask the user one question at a time, like grill-me, until each candidate is
  answered, deferred, discarded, converted into a final-form marker candidate, or
  left explicitly unresolved.
- After clarification, use /capture in this same thread to draft the exact KB
  write proposal and wait for approval.

Scope:
- Search the live KB with normal search and targeted fetches.
- Treat due follow-up markers as first-priority questions.
- Search for raw, provisional, sparse, or time-ambiguous prose (relative-time
  phrases, "current", "for now", and similar).
- For projects, start from the selected-projects endpoint. Compare each project
  page against recent local git history when the clone is available, or remote
  history when it is not.
- Skip final-form sections unless the user explicitly reopens them.

Question style:
- Before the first question, say how many candidates were found and which group
  comes first.
- At the 10-question cap, say how many remain and ask whether to continue or defer.
- Group by register: due follow-ups, project drift, dated task signals, life or
  identity updates, other stale/missing/ambiguous findings, then low-confidence
  findings.
- Include the page, the evidence, and why the question matters.
- A normal discard leaves no KB trace. Use the marker formats from
  docs/knowledge-bank-conventions.md.

End state:
- Do not stop after lookup results.
- Feed answered updates, marker candidates, discarded findings, and unresolved
  questions into /capture.
- Apply KB writes only after the user approves the latest exact /capture draft.
```
