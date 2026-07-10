# Workflows

Knowledge Bank Infrastructure defines a small set of agent workflows around the
live KB. The KB remains the source of truth. Every automation shares
[the preamble](automations/_preamble.md); include it when materializing an
automation. Cadences are bindings, collected at setup, not fixed here.

## Automation Set

| Automation | Consumes | Materializes into | Recommended execution profile | Intervention posture |
|------------|----------|-------------------|-------------------------------|----------------------|
| Job Hunt Evaluate Audit | new + queued postings; job-search-strategy | career-system | balanced / medium | Autonomous output; strategy mirror sync + capture |
| Job Hunt Advance Audit | Evaluate Audit output | career-system | frontier / high | Direct draft packs; real-world actions gated |
| Knowledge Harvest | activity across sources | KB (via `/capture`) | frontier / parallel | Clarify, then approval-gated writes |
| Social Draft Pulse | public-safe endpoints | social-draft-queue | frontier / medium | Approval-gated drafts; first-party point-of-view capture |
| Portfolio Surface Sweep | public-safe endpoints | portfolio | balanced / medium | Approval-gated branch/PR work |

Job Hunt Advance Audit consumes Job Hunt Evaluate Audit; schedule it after, and
let it idle while evaluation work is still in progress. Portfolio Surface Sweep is
lower-frequency; offset it from the heavier runs.

Execution profiles are provider-agnostic recommendations, not model identifiers.
`frontier` favors the strongest available model for ambiguous, high-value synthesis;
`balanced` favors a strong everyday model with a better cost/capability tradeoff;
`parallel` requires a frontier model and a harness mode that can delegate independent
workstreams. Setup resolves each profile to a concrete local model and reasoning
effort, and records the applied selection for drift detection.

## 1. Knowledge Harvest

Trigger: the scheduled automation, or a manual request to harvest signals from
recent activity — stale, missing, due, raw, ambiguous, or project-drift KB
knowledge, plus decisions, opinions, themes, and working-style patterns from git
history and agent transcripts.

Flow: fan out one subagent per source (KB-internal staleness, git history, each
bound transcript source, each bound social profile source); each returns ranked
candidate signals. Merge and convergence-rank them, then ask the user one question
at a time and hand answered updates, marker candidates, discarded findings, and
unresolved questions to `/capture` for an exact approval draft.

Rules:

- This is an observe-to-capture loop, not a report-only audit.
- Subagents self-clarify against their source; only the orchestrator asks the user.
- Treat due follow-up markers as questions, not as permission to write.
- Read `signal-preferences` to rank candidates; propose rubric updates as a distinct
  block in the `/capture` draft.
- Transcript-derived signals are private by default; never route them to public-safe
  or social surfaces.
- Reconcile `published-social-context` from each bound social profile source, best-
  effort: read what has actually been posted per platform and propose ledger updates;
  where a platform cannot be read, ask the user what went out rather than guessing.
- A normal discard leaves no KB trace; deferrals and final-form decisions become
  marker candidates only through approved `/capture` writes.
- Prompt source: [knowledge-harvest.md](automations/knowledge-harvest.md).

## 2. Social Draft Pulse

Trigger: the scheduled automation, or a manual request to mine recent KB context
for work-facing social drafts.

Flow: use `/lookup` in context mode once over the `public-safe-claim-source`,
`network`, `social-rules-of-engagement`, `selected-projects`, `identity`,
`point-of-view`, and `published-social-context` endpoints. Reconcile the semantic
audience and argument state against the `social-publishing-source`, derive eligible
open slots from its recurring schedule and queue timeline, then apply the KB's
day-eligibility and recovery rules to read-only evidence from the
`availability-calendar-source`. Return a slot-sized idea summary first. After
approval, create and schedule drafts in the `social-draft-queue` sink.

Rules:

- This is a social draft and scheduling workflow, not an immediate publishing
  workflow. It may schedule approved drafts through the bound sink; it must not
  publish now without an explicit publish-now instruction.
- Apply `social-rules-of-engagement` for platform strategy, content mix,
  day-eligibility and recovery rules, slot tone, and testing-window policy. Derive
  capacity from enabled, eligible, unfilled live slots; do not hardcode counts or
  weekday expansions.
- Calendar events are private scheduling evidence only. Reduce them to eligibility
  constraints and never turn their details into content or public claims.
- Keep continuity by using `published-social-context` for semantic audience and
  argument state and the social publishing source for raw publication, analytics,
  queue, and schedule evidence. Do not mirror source records or duplicate concepts
  that already have canonical KB owners.
- Use account analytics to propose controlled testing windows with a hypothesis,
  comparable baseline, repeated observation window, and success measure. Schedule an
  explicit test time only after approval; never mutate the recurring schedule
  autonomously. When an eligible day has no recurring slot, evaluate it under this
  testing policy instead of silently treating it as an off day.
- Topical candidates draw their angle from `point-of-view` or `identity`; when no
  stance is recorded, surface the hook at the gate for the user's take rather than
  inventing one.
- First-party-capture a `point-of-view` take stated at the gate through `/capture`
  (explicit-consent, public-facing); after posts go live, batch only the semantic
  `published-social-context` delta through `/capture`, backstopped by Knowledge
  Harvest. It never publishes immediately.
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
`career-system` clone to its remote first, then realign the career-system
`job-search-strategy` copy from the KB; then process existing pending/failed
work before scanning; scan a bounded batch only when the queue is drained;
evaluate live postings; generate the expected reports and tracker rows; then
verify the pipeline.

Rules:

- This is discovery and evaluation only, not advancement or application work.
- Update the `career-system` clone to its remote before starting; if it cannot
  fast-forward cleanly, stop and report rather than running on stale state.
- Realign the `career-system` `job-search-strategy` copy from the KB as a user-layer
  change; this absorbs the retired Job Hunt Tune Audit (ADR 0007).
- First-party-capture a `job-search-strategy` signal only when a run surfaces one
  (weak-lead scoring, target-role drift); signal-triggered, most runs capture nothing.
- Do not submit applications, send messages, or prefill forms in a hidden browser.
- Process existing queue work before adding new scan work.
- Prompt source: [job-hunt-evaluate-audit.md](automations/job-hunt-evaluate-audit.md).

## 5. Job Hunt Advance Audit

Trigger: the scheduled automation, or a manual request to advance existing
`career-system` opportunities after evaluation.

Flow: inspect the `career-system` tracker, reports, and follow-up history. Resolve
the current job-application throughput target from the career-system strategy mirror
or `/lookup`, invoke the bound deterministic related-opportunity selector, then
select enough eligible opportunities to satisfy that target when the queue allows.
Suppressed alternatives never re-enter through score sorting; unresolved groups
are researched and persisted in the sink before the selector is rerun. Use
`/lookup` in context mode for pack-specific context only when fresh KB context
could change the next pack. Produce the draft next packs directly through the
bound advancement workflow, then
advance each drafted row through the career-system's own agent-owned stages so the
tracker records that a draft exists — no pre-approval gate on either. Stop before
submitting, sending, or recording real-world state changes without the user's
confirmation.

Rules:

- This is an advancement workflow, not discovery or evaluation.
- It consumes Job Hunt Evaluate Audit; idle when evaluation or batch work is still
  in progress.
- Resolve the active throughput target before selection. If no active target exists,
  fall back to a conservative small batch and report that no target was found.
- Run the bound related-opportunity selector before ranking. Its eligible set is
  exclusive; never bypass suppression in an unattended run. Resolve and persist
  any required organizational/ownership research, then rerun it.
- Generate draft packs directly and advance the tracker as part of the run; both are
  ungated. A pack is the reviewable output and the agent-owned stage advance is a safe
  internal-state write that records a draft exists — never a real-world action. Source
  which advances are safe from the career-system's own state model; do not leave a
  drafted pack stranded at its pre-advance stage.
- First-party-capture a `personal-constraints` or `job-search-strategy` signal when
  advancing surfaces one, then realign the career-system copy; signal-triggered.
- Keep the gate only on real-world actions: do not submit, send, record a follow-up as
  sent, or mark a real-world status complete without the user's confirmation.
- Prompt source: [job-hunt-advance-audit.md](automations/job-hunt-advance-audit.md).
