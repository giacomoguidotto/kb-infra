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
- Sink: `<career-system>`.
- Approval gate: produce drafts and recommendations only. Do not submit, send, or
  update real-world statuses without confirmation.

## Prompt

```md
You are running Job Hunt Advance Audit.

The preamble is prepended to this prompt at materialize time.

Setup:
- Read this repo's AGENTS.md, docs/workflows.md,
  docs/knowledge-bank-conventions.md, docs/automations/_preamble.md, and
  skills/lookup/SKILL.md before acting.
- Read the career-system sink's own AGENTS.md, data contract, mode files, and
  templates before producing packs.
- The upstream producer is Job Hunt Evaluate Audit.

Startup:
- Run the career-system's health check; if onboarding is incomplete or required
  files are missing, stop and report exactly what is missing.
- Inspect the tracker, pipeline, follow-up history, optional action state, and
  recent reports.

Idle rule:
- If the pipeline has unchecked pending work, the batch has failed/pending/
  processing rows, or a batch runner is still active, assume Evaluate Audit has
  unfinished work. Do not advance in that run; report the concrete blocker and
  stop.

Goal:
- Advance the most promising existing opportunities after evaluation.
- Use the career-system's next-action routing.
- Produce draft-oriented packs only.
- Do not submit applications, send messages, click final submit buttons, update
  outward-facing systems, or record a status/follow-up as completed without the
  user's explicit confirmation.

KB lookup:
- Optional. Start from career-system state.
- Use /lookup in context mode only when fresh KB context could change the pack:
  high-priority opportunity, a role touching recent projects or public proof, or a
  role that depends on personal-constraints or public-safe claim calibration.
- Skip lookup for routine follow-ups or drafts fully covered by the current
  report/profile. When skipping, say why briefly.

Output pack:
- Select a small number of opportunities (up to three).
- For each, produce the appropriate next pack for its lifecycle stage, reusing the
  career-system's existing mode rules rather than restating them.

Writes:
- Do not edit the tracker unless the user confirms a real-world status change.
- Do not record follow-ups unless the user confirms they were sent.
- Do not create or edit action state unless the user approves.
- If a better durable state model is needed, propose it in the run summary rather
  than silently changing schema or files.

End state:
- Report selected opportunities, why, packs produced, lookup used/skipped, blocked
  actions, and recommended next human approvals.
- If no useful advancement exists, say so and include the evidence checked.
```
