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
- Endpoints: `public-safe-claim-source`, `proof-points`, `personal-constraints`,
  `job-search-strategy` (on demand).
- State routing: owned by the sink. This automation reads the career-system's
  canonical state model and never defines its own.
- Sink: `<career-system>` — a mirror sink holding a copy of `job-search-strategy`.
- Mandate: first-party-capture a `personal-constraints` or `job-search-strategy`
  signal when advancing surfaces one — a stated constraint (relocation, compensation,
  work authorization, references, availability, side-project/IP) or a targeting
  preference — then realign the career-system copy. Signal-triggered; do not infer.
- Approval gate: two things are ungated here — the draft packs (this automation's
  reviewable output) and the tracker advance that records a draft now exists.
  Generate packs directly and advance the career-system's own agent-owned stages as
  part of the run, **without pre-approval**; that advance is a safe internal-state
  write, never a real-world action. Source which advances are safe from the
  career-system's own state model — never invent or override it. The gate survives
  only for real-world actions and any record that asserts one happened: never submit,
  send, click final submit, record a follow-up as sent, or mark a real-world status
  complete without the user's confirmation.

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

Selection:
- Select a small number of opportunities (up to three).
- Generate the packs directly — there is no pre-approval gate. Draft packs are this
  automation's reviewable output, not a gated sink write.
- Advance the tracker as part of the run. When the career-system's canonical state
  model marks a stage as agent-owned, advance the row to its paired ready stage so it
  records that the draft pack now exists — a safe internal-state write, never a
  real-world action, so do not gate it. Read which advances are safe from the
  career-system's own state model; if that model is missing or ambiguous, stop and
  report rather than guessing. Do not leave a drafted pack stranded at its
  pre-advance stage.
- Keep the gate only on real-world actions and the records that assert one happened:
  do not submit applications, send messages, click final submit buttons, record a
  follow-up as sent, or mark a real-world status complete without the user's
  confirmation.

Producing packs:
- Produce the selected packs, reusing the career-system's existing mode rules
  rather than restating them. Packs are drafts for review.
- If a better durable state model is needed, propose it in the summary rather than
  silently changing schema or files.

First-party capture:
- If advancing an opportunity surfaces a new personal-constraint (relocation,
  compensation, work authorization, references, availability, side-project/IP) or a
  targeting preference you state in-context, propose a /capture to its owning endpoint
  (personal-constraints or job-search-strategy), then realign the career-system copy.
- Signal-triggered — capture only what this run surfaced explicitly; do not infer
  across runs, that is Knowledge Harvest's job.

End state:
- Report selected opportunities and why, packs produced, the tracker advances
  applied, lookup used or skipped, any personal-constraints or job-search-strategy
  captures proposed and the mirror realignments, blocked actions, and recommended
  next human approvals for real-world state.
- If no useful advancement exists, say so and include the evidence checked.
```
