# Workflows

Knowledge Bank Infrastructure defines a small set of agent workflows around the
live KB. The KB remains the source of truth. Every automation shares
[the preamble](automations/_preamble.md); include it when materializing an
automation. Cadences are bindings, collected at setup, not fixed here.

## Automation Set

| Automation | Consumes | Materializes into | Intervention posture |
|------------|----------|-------------------|----------------------|
| Job Hunt Evaluate Audit | new + queued postings | career-system | Autonomous evaluation output |
| Job Hunt Advance Audit | Evaluate Audit output | career-system | Approval-gated draft packs |
| Job Hunt Tune Audit | job-search-strategy endpoint | career-system | Approval-gated tuning proposal |
| Knowledge Harvest | activity across sources | KB (via `/capture`) | Clarify, then approval-gated writes |
| Social Draft Pulse | public-safe endpoints | social-draft-queue | Approval-gated drafts |
| Portfolio Surface Sweep | public-safe endpoints | portfolio | Approval-gated branch/PR work |

Job Hunt Advance Audit consumes Job Hunt Evaluate Audit; schedule it after, and
let it idle while evaluation work is still in progress. Portfolio Surface Sweep
and Job Hunt Tune Audit are lower-frequency; offset them from each other.

## 1. Knowledge Harvest

Trigger: the scheduled automation, or a manual request to harvest signals from
recent activity — stale, missing, due, raw, ambiguous, or project-drift KB
knowledge, plus decisions, opinions, themes, and working-style patterns from git
history and agent transcripts.

Flow: fan out one subagent per source (KB-internal staleness, git history, each
bound transcript source); each returns ranked candidate signals. Merge and
convergence-rank them, then ask the user one question at a time and hand answered
updates, marker candidates, discarded findings, and unresolved questions to
`/capture` for an exact approval draft.

Rules:

- This is an observe-to-capture loop, not a report-only audit.
- Subagents self-clarify against their source; only the orchestrator asks the user.
- Treat due follow-up markers as questions, not as permission to write.
- Read `signal-preferences` to rank candidates; propose rubric updates as a distinct
  block in the `/capture` draft.
- Transcript-derived signals are private by default; never route them to public-safe
  or social surfaces.
- A normal discard leaves no KB trace; deferrals and final-form decisions become
  marker candidates only through approved `/capture` writes.
- Prompt source: [knowledge-harvest.md](automations/knowledge-harvest.md).

## 2. Social Draft Pulse

Trigger: the scheduled automation, or a manual request to mine recent KB context
for work-facing social drafts.

Flow: use `/lookup` in context mode once over the `public-safe-claim-source`,
`network`, `social-rules-of-engagement`, `selected-projects`, `identity`,
`point-of-view`, and `published-social-context` endpoints. Draft a candidate set
that honors the volume and project/topical mix in `social-rules-of-engagement` and
keeps per-platform continuity. Return an idea summary first. After approval, create
drafts in the `social-draft-queue` sink.

Rules:

- This is a social draft workflow, not a publishing workflow. Draft only; do not
  post or schedule.
- Apply the `social-rules-of-engagement` endpoint for platform strategy, volume,
  and content mix; do not hardcode them here.
- Keep continuity: use `published-social-context` to avoid assuming knowledge the
  platform's audience does not have, and introduce concepts on first public use.
- Topical candidates draw their angle from `point-of-view` or `identity`; when no
  stance is recorded, surface the hook at the gate for the user's take rather than
  inventing one.
- New takes become `point-of-view` capture candidates for `/capture`; this
  automation never writes to the KB itself.
- Flag portfolio candidates for Portfolio Surface Sweep instead of auditing the
  portfolio here.
- Prompt source: [social-draft-pulse.md](automations/social-draft-pulse.md).

## 3. Portfolio Surface Sweep

Trigger: the scheduled automation, or a manual request after a meaningful
milestone, launch, shipped demo, public artifact, or project status change.

Flow: use `/lookup` in context mode once over the `public-safe-claim-source`,
`network`, `selected-projects`, `portfolio-change-rules`, and `identity`
endpoints. Inspect the `portfolio` sink before proposing changes. Return a
surface summary first. After approval, prepare branch/PR work for approved
candidates.

Rules:

- This is a portfolio proposal workflow, not a social drafting workflow.
- Apply the `portfolio-change-rules` endpoint; do not hardcode portfolio
  structure here.
- A no-change result is acceptable; if the portfolio is still current, report the
  evidence checked and stop.
- Flag announcement candidates for Social Draft Pulse instead of drafting posts
  here.
- Prompt source: [portfolio-surface-sweep.md](automations/portfolio-surface-sweep.md).

## 4. Job Hunt Evaluate Audit

Trigger: the scheduled automation, or a manual request to discover and evaluate
opportunities.

Flow: run the `career-system` discovery-to-evaluation loop. Update the
`career-system` clone to its remote first; then process existing pending/failed
work before scanning; scan a bounded batch only when the queue is drained;
evaluate live postings; generate the expected reports and tracker rows; then
verify the pipeline.

Rules:

- This is discovery and evaluation only, not advancement or application work.
- Update the `career-system` clone to its remote before starting; if it cannot
  fast-forward cleanly, stop and report rather than running on stale state.
- Do not submit applications, send messages, or prefill forms in a hidden browser.
- Process existing queue work before adding new scan work.
- Prompt source: [job-hunt-evaluate-audit.md](automations/job-hunt-evaluate-audit.md).

## 5. Job Hunt Tune Audit

Trigger: the scheduled automation, or a manual request after a meaningful
strategy, proof, project, compensation, relocation, or target-role change.

Flow: use `/lookup` in context mode once over the `job-search-strategy`,
`public-safe-claim-source`, `proof-points`, `personal-constraints`, and
`identity` endpoints. Inspect the `career-system` user-layer configuration before
proposing changes. Return a tuning summary first. Apply repo changes only after
approval.

Rules:

- This is a tuning proposal workflow, not a live application workflow.
- Keep personalization in the `career-system` user-layer; do not edit shared
  system defaults unless explicitly asked.
- A no-change result is acceptable.
- Prompt source: [job-hunt-tune-audit.md](automations/job-hunt-tune-audit.md).

## 6. Job Hunt Advance Audit

Trigger: the scheduled automation, or a manual request to advance existing
`career-system` opportunities after evaluation.

Flow: inspect the `career-system` tracker, reports, and follow-up history. Use
`/lookup` in context mode only when fresh KB context could change the next pack.
Select a small number of opportunities, return a selection summary, and produce the
draft next packs only after the user approves. Stop before submitting, sending, or
recording real-world state changes.

Rules:

- This is an advancement workflow, not discovery or evaluation.
- It consumes Job Hunt Evaluate Audit; idle when evaluation or batch work is still
  in progress.
- Ask before generating: return a selection summary and get approval before writing
  pack files or any other sink state.
- Do not submit, send, or mark actions completed without the user's confirmation.
- Prompt source: [job-hunt-advance-audit.md](automations/job-hunt-advance-audit.md).
