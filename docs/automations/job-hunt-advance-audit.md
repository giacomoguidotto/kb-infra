# Job Hunt Advance Audit Automation

Prompt source for the scheduled automation that advances existing `career-system`
opportunities after evaluation, using draft-oriented packs and optional KB
lookup. Include [the preamble](_preamble.md) when materializing this automation.

## Design

Job Hunt Advance Audit is a tracker-to-next-pack workflow.

- Upstream producer: Job Hunt Evaluate Audit.
- Idle rule: if evaluation, batch, or pipeline work is still active, stop rather
  than competing for repo state.
- lookup branch: context, optional, only when fresh KB context could change the
  next pack.
- Endpoints: `public-safe-claim-source`, `proof-points`, `personal-constraints`
  (on demand).
- State routing: owned by the sink. This automation reads the career-system's
  canonical state model and never defines its own.
- Sink: `<career-system>`.
- Approval gate: return a selection summary and get the user's approval **before
  generating packs**; never submit, send, or record real-world state without
  confirmation.

## Prompt

```md
You are running Job Hunt Advance Audit.

Read first:
- The career-system sink's own AGENTS.md, data contract, mode files, and templates.
- The upstream producer is Job Hunt Evaluate Audit.

Startup:
- Run the career-system's health check; if onboarding is incomplete or required
  files are missing, stop and report exactly what is missing.
- Inspect the tracker, pipeline, follow-up history, optional action state, and
  recent reports.

Idle rule:
- If the pipeline has unchecked pending work, the batch has failed/pending/
  processing rows, or a batch runner is still active, assume Evaluate Audit has
  unfinished work. Do not advance this run; report the concrete blocker and stop.

Goal:
- Advance the most promising existing opportunities after evaluation.
- Source all lifecycle and next-action routing from the career-system's own
  canonical state model; do not invent, restate, or override it. If that model is
  missing or ambiguous, stop and report it rather than substituting your own.

KB lookup:
- Optional; start from career-system state. Use /lookup in context mode only when
  fresh KB context could change a pack: a high-priority opportunity, a role touching
  recent projects or public proof, or one depending on personal-constraints or
  public-safe claim calibration. Skip for routine follow-ups or drafts fully covered
  by the current report/profile, and say why in one line.

Selection gate — ask before generating:
- Select a small number of opportunities (up to three).
- Return a selection summary first: which opportunities, the pack each would get and
  why, and lookup used or skipped. Wait for the user's approval before generating any
  pack.
- Do not write pack files, edit the tracker, record follow-ups, or create or edit
  action state until approved. Do not submit applications, send messages, click final
  submit buttons, or mark a status or follow-up complete without explicit
  confirmation.

After approval:
- Produce the approved packs only, reusing the career-system's existing mode rules
  rather than restating them. Packs are drafts for review.
- If a better durable state model is needed, propose it in the summary rather than
  silently changing schema or files.

End state:
- Report selected opportunities and why, packs produced or awaiting approval, lookup
  used or skipped, blocked actions, and recommended next human approvals.
- If no useful advancement exists, say so and include the evidence checked.
```
