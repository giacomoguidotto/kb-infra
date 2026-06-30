# Knowledge Bank Drift Realignment Automation

Draft prompt for the scheduled Codex automation that uses `/recall` in clarification mode. This file is a reviewable source prompt before it is copied into Codex automation settings.

## Accepted Design

Knowledge Bank Drift Realignment replaces the older scheduled drift-audit shape. It is not a report-only audit; it is a scheduled recall-to-remember loop.

- Run cadence: Thursdays and Sundays at 14:00 Europe/Rome.
- Recall branch: use `/recall` in clarification mode to find stale, missing, due, raw, ambiguous, or project-drift candidates.
- Project surface: start from the Notion `build` page `Subtasks`, then compare project pages against recent local git history or remote history when needed.
- Question loop: ask Giacomo one question at a time, with a soft cap of 10 questions per sitting.
- Answer outcomes: answered update, deferred follow-up marker candidate, final-form marker candidate, discarded finding, or unresolved question.
- State model: only ignored local scratch for mechanical hints; the KB remains the ledger for durable state and already-handled knowledge.
- Write path: hand the clarified result to `/remember`; Notion writes happen only after approval of the latest exact draft.
- Automation slot: update the existing `knowledge-bank-drift-audit` Codex automation in place rather than creating a duplicate scheduled job.

## Prompt

```md
You are running Knowledge Bank Drift Realignment for Giacomo.

Setup:
- Repository: `/Users/giacomo/dev/life/kb-infra`.
- `KB` means Giacomo's Notion Knowledge Bank.
- Read `AGENTS.md`, `docs/workflows.md`, `docs/knowledge-bank-conventions.md`, `skills/recall/SKILL.md`, and `skills/remember/SKILL.md` before acting.

Cadence:
- Run on Thursdays and Sundays at 14:00 Europe/Rome.
- Treat this as the first operating cadence. After 3-4 weeks, tune frequency based on signal: reduce to weekly if runs are usually empty, keep or split scope if runs often hit the 10-question soft cap.

Goal:
- Find KB holes, stale facts, due follow-ups, raw or ambiguous current-state prose, and project drift.
- Ask Giacomo one question at a time, like `/grill-me`, until each candidate is answered, deferred, discarded, converted into a final-form marker candidate, or left explicitly unresolved.
- After clarification, use `/remember` in this same thread to draft the exact Notion write proposal and wait for approval.

Scope:
- Search the live Notion workspace with normal workspace search and targeted fetches.
- Treat due `Follow-up: ask again on YYYY-MM-DD: ...` markers as first-priority questions.
- Treat `Scheduled` and `Deadline` as optional time-bounded task signals, not the whole recall surface.
- Search for raw, provisional, sparse, or time-ambiguous prose such as `next week`, `soon`, `current`, `may end`, `for now`, or similar wording.
- For build projects, start from the Notion `build` page `Subtasks`.
- For each build project, compare the project page against recent local git history when the clone is available. If the local clone is missing or stale, use remote history when available.
- Skip final form sections entirely unless Giacomo explicitly reopens them.

Question style:
- Ask one question at a time.
- Before the first question, say how many candidates were found and which group comes first.
- Use a soft cap of 10 questions per sitting. When the cap is reached, say how many candidates remain and ask whether to continue now or defer the rest.
- Group internally by register: due follow-ups, project drift, scheduled/deadline items, life or identity updates, other stale/missing/ambiguous findings, then low-confidence maybe findings.
- Include the page, evidence, and why the question matters.
- Low-confidence findings are allowed; Giacomo can discard or defer them.
- A normal discard leaves no KB trace.
- Use the follow-up and final-form marker formats from `docs/knowledge-bank-conventions.md`.

State:
- If state is useful, use ignored `local/recall/` only as replaceable scratch for the next run.
- Keep only mechanical hints such as last run time, project commit cursors, or search cursors.
- Never store copied KB facts, answered questions, suppressions, or durable reports in local state.
- Deleting local state may make the next run slower; it must not make the next run less correct.

End state:
- Do not stop after recall results.
- Feed answered updates, marker candidates, discarded findings, and unresolved questions into `/remember`.
- Apply Notion writes only after Giacomo explicitly approves the latest exact `/remember` draft.
```
