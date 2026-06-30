# Public Surface Workflows

Shared rulebook for the two public-surface automations:

- [Social Draft Pulse](social-draft-pulse.md)
- [Portfolio Surface Sweep](portfolio-surface-sweep.md)

The original Public Surface Update design split into two workflows because the
social lane is frequent and lightweight, while the portfolio lane is slower,
repo-sensitive, and better handled as branch/PR work.

## Shared Invariants

- `KB` means Giacomo's Notion Knowledge Bank.
- Notion remains the source of truth for profile, project, task, portfolio, and
  personal knowledge.
- Use `/recall` narrowly. Do not preload broad Notion content.
- Do not write to Notion from either automation.
- Do not publish, schedule, merge, or deploy without Giacomo's approval.
- Start with an idea or surface summary before creating drafts or branches.
- Keep public claims source-backed and public-safe.
- Do not commit raw personal dumps or broad Notion exports.
- Do not turn unsupported vibes into factual claims.
- Use ignored local scratch only for mechanical hints such as last run time,
  refresh date, or commit cursors.

## Workflow Split

### Social Draft Pulse

Purpose: mine recent KB context for X and LinkedIn draft candidates.

Default cadence: Tuesday and Friday.

Allowed outputs:

- idea summary for Giacomo approval
- Typefully drafts after approval
- media placeholders such as screenshots, short videos, diagrams, or generated
  image ideas
- portfolio candidates flagged for the portfolio workflow
- KB rule realignment candidates, reported only

Disallowed outputs:

- posting or scheduling
- deep portfolio repo work
- Notion writes

### Portfolio Surface Sweep

Purpose: compare the current `guidotto.dev` public surface against recent KB
context and propose branch/PR updates when the site can be made stronger.

Default cadence: monthly, plus manual trigger after a meaningful milestone.

Allowed outputs:

- surface summary for Giacomo approval
- branch/PR proposal after approval
- content updates to the portfolio structure when source-backed and approved
- announcement candidates flagged for the social workflow

Disallowed outputs:

- Typefully drafts
- publishing, merging, or deploying without approval
- unsupported metrics, social proof, or factual claims
- Notion writes

## Coordination

The workflows can flag work for each other, but should not do each other's job.

- A social run may say: `Portfolio candidate: Tempo status may affect project
  vessel copy. Hand to Portfolio Surface Sweep.`
- A portfolio run may say: `Announcement candidate: updated centerpiece copy after
  PR approval. Hand to Social Draft Pulse.`

The KB is the knowledge ledger, Typefully is the social draft queue, and GitHub
PRs/issues are the portfolio work queue.
