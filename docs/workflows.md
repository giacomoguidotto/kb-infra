# Workflows

Knowledge Bank Infrastructure defines a small set of agent workflows around the live Notion workspace. Notion remains the source of truth.

## Automation Cadence

| Automation | Cadence | Start | Intervention posture |
|------------|---------|-------|----------------------|
| Job Hunt Eval Pulse | Mondays, Wednesdays, Fridays | 09:00 Europe/Rome | Autonomous evaluation output |
| Job Hunt Advancement Pulse | Mondays, Wednesdays, Fridays | 13:00 Europe/Rome | Produces review-later draft packs |
| Knowledge Bank Drift Realignment | Mondays, Fridays | 13:00 Europe/Rome | Low-effort clarification loop; writes still require approval |
| Social Draft Pulse | Mondays, Wednesdays, Fridays | 17:00 Europe/Rome | Approval-gated idea summary, then Typefully drafts |
| Portfolio Surface Sweep | Every 2 weeks, alternating Wednesdays starting July 8, 2026 | 13:00 Europe/Rome | Approval-gated portfolio proposal |
| Job Hunt Tuning Audit | Every 2 weeks, alternating Wednesdays starting July 15, 2026 | 13:00 Europe/Rome | Approval-gated career tuning proposal |

## 1. Manual Capture

Trigger: Giacomo manually invokes `/remember` or asks to save a conversation/session into the Knowledge Bank.

Flow: use `skills/remember`; inspect live Notion structure; draft the smallest coherent Notion update; ask Giacomo to approve the exact draft; write only after approval.

Rules:

- Do not write session knowledge to Notion without explicit confirmation.
- Prefer the existing Notion structure over repo assumptions.
- Keep parent pages thin; put dense knowledge in the right child page.
- Choose one canonical owner for each fact, chapter, or lesson; other pages should link to it instead of duplicating it.

## 2. Knowledge Bank Drift Realignment

Trigger: the scheduled Codex automation `Knowledge Bank Drift Realignment`, or a manual request to find and resolve stale, missing, due, raw, ambiguous, or project-drift knowledge.

Flow: start from this repo's agent instructions, [Knowledge Bank Conventions](knowledge-bank-conventions.md), `/recall`, and `/remember`. Use `/recall` in clarification mode over live Notion and the `build` page `Subtasks`; compare build projects against recent local git history or remote history when useful. Ask Giacomo one question at a time, then hand answered updates, marker candidates, discarded findings, and unresolved questions to `/remember` for an exact approval draft.

Rules:

- This is a scheduled clarification-to-remember loop, not a report-only audit.
- Do not write to Notion during recall or before `/remember` approval.
- Treat due follow-up markers as questions for Giacomo, not as permission to update the Knowledge Bank.
- A normal discard leaves no KB trace; deferrals and final-form decisions become marker candidates only through approved `/remember` writes.
- Runs on Mondays and Fridays at 13:00 Europe/Rome.
- Use ignored local scratch only for mechanical hints such as last run time or commit cursors. Never store copied KB facts, answered questions, suppressions, or durable reports in local state.
- The scheduled prompt source lives in [Knowledge Bank Drift Realignment Automation](automations/kb-drift-realignment.md).

## 3. Social Draft Pulse

Trigger: the scheduled Codex automation `Social Draft Pulse`, or a manual request
to mine recent KB context for work-facing social drafts.

Flow: start from this repo's agent instructions, [Knowledge Bank Conventions](knowledge-bank-conventions.md), `/recall`, and the Typefully integration. Use `/recall` in context mode once over `profile`, `network`, `X`, `LinkedIn`, `build`, and relevant project pages. Return an idea summary first. After Giacomo approves the content direction, create Typefully drafts for approved X and LinkedIn candidates.

Rules:

- This is a social draft workflow, not a publishing workflow.
- Do not post or schedule from Codex.
- Do not write to Notion.
- Runs on Mondays, Wednesdays, and Fridays at 17:00 Europe/Rome.
- Use Typefully as the draft queue after approval.
- Prefer platform-specific drafts over generic cross-posts.
- Include media placeholders when a draft needs a screenshot, short video,
  diagram, generated-image idea, or asset from Giacomo.
- Flag portfolio candidates for Portfolio Surface Sweep instead of auditing the
  portfolio in this workflow.
- The scheduled prompt source lives in [Social Draft Pulse Automation](automations/social-draft-pulse.md).

## 4. Portfolio Surface Sweep

Trigger: the scheduled Codex automation `Portfolio Surface Sweep`, or a manual
request after a meaningful milestone, launch, shipped demo, public artifact, or
project status change.

Flow: start from this repo's agent instructions, [Knowledge Bank Conventions](knowledge-bank-conventions.md), `/recall`, and the current `guidotto.dev` repo docs. Use `/recall` in context mode once over `profile`, `network`, `build`, `guidotto.dev`, and relevant project pages. Inspect `guidotto.dev` before proposing changes. Return a surface summary first. After Giacomo approves the content direction, prepare branch/PR work for approved portfolio candidates.

Rules:

- This is a portfolio proposal workflow, not a social drafting workflow.
- Do not create Typefully drafts.
- Do not merge, deploy, or publish from Codex without approval.
- Do not write to Notion.
- Runs every 2 weeks on alternating Wednesdays at 13:00 Europe/Rome, starting
  July 8, 2026, offset from Job Hunt Tuning Audit.
- A no-change result is acceptable; if the portfolio is still current, report the
  evidence checked and stop.
- Content updates are expected when KB context reveals a stronger public surface;
  the Notion boundary is a public-safety and audit rule, not a ban on changing
  copy.
- Keep factual claims, metrics, social proof, employment facts, project status,
  and project capabilities source-backed and public-safe.
- Respect the current portfolio structure unless the approved change explicitly
  revises it: four project vessels, one centerpiece, mission/trajectory, human
  anchor, and contact door.
- Flag announcement candidates for Social Draft Pulse instead of drafting social
  posts in this workflow.
- The scheduled prompt source lives in [Portfolio Surface Sweep Automation](automations/portfolio-surface-sweep.md).

## 5. Job Hunt Tuning Audit

Trigger: a scheduled Codex automation, or a manual request after a meaningful
job-search strategy, proof, project, compensation, relocation, or target-role
change.

Flow: start from this repo's agent instructions, [Knowledge Bank
Conventions](knowledge-bank-conventions.md), `/recall`, and the current
`career-ops` repo docs. Use `/recall` in context mode once over job-search
strategy pages and active proof/project pages. Inspect `career-ops` user-layer
configuration before proposing changes. Return a tuning summary first. Apply
repo changes only after Giacomo approves the proposed set.

Rules:

- This is a tuning proposal workflow, not a live application workflow.
- Do not write to Notion.
- Runs every 2 weeks on alternating Wednesdays at 13:00 Europe/Rome, starting
  July 15, 2026, offset from Portfolio Surface Sweep.
- Keep personalization in `career-ops` user-layer files.
- Do not edit shared system defaults unless Giacomo explicitly asks.
- A no-change result is acceptable.
- The draft prompt source lives in [Job Hunt Tuning Audit Automation](automations/job-hunt-tuning-audit.md).

## 6. Job Hunt Advancement Pulse

Trigger: a scheduled Codex automation, or a manual request to advance existing
`career-ops` opportunities after evaluation.

Flow: inspect `career-ops` tracker, reports, follow-up history, and optional
application action state. Use `/recall` in context mode only when fresh KB
context could change the next pack. Select a small number of opportunities and
produce draft-oriented next-step packs. Stop before submitting applications,
sending messages, or recording real-world state changes.

Rules:

- This is an advancement workflow, not discovery or evaluation.
- Runs on Mondays, Wednesdays, and Fridays at 13:00 Europe/Rome.
- It consumes `Job Hunt Eval Pulse`; it should idle when evaluation or batch work
  is still in progress.
- Do not write to Notion.
- Do not submit, send, or mark actions completed without Giacomo's confirmation.
- Keep lifecycle status in `data/applications.md`; keep operational state in the
  optional `data/application-actions.yml` sidecar.
- The draft prompt source lives in [Job Hunt Advancement Pulse Automation](automations/job-hunt-advancement-pulse.md).
