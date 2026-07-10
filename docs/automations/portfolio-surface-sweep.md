# Portfolio Surface Sweep Automation

Prompt source for the scheduled automation that compares recent KB context with
the `portfolio` sink and proposes approval-gated branch/PR updates. Include
[the preamble](_preamble.md) when materializing this automation.

## Design

Portfolio Surface Sweep is a lookup-to-portfolio-proposal workflow.

- lookup branch: context, once per run.
- Endpoints: `public-safe-claim-source`, `network`, `selected-projects`,
  `portfolio-change-rules`, `identity`.
- Sink: `<portfolio>` — a derived sink; materialized one-way, no mirror to realign.
- Execution profile: `balanced/medium` — the normal case is a bounded comparison or
  no-op audit; an approved complex redesign should be escalated as separate
  frontier/high work rather than making every sweep pay that cost.
- Mandate: no KB capture. This is a pure consumer of public-safe claims that writes
  only to the portfolio sink; it originates no durable KB knowledge, so it captures
  nothing. Unsupported claims are surfaced as gaps, not captures, and stale KB claims
  are Knowledge Harvest's drift job.
- Approval gate: return a surface summary first. After approval, prepare branch/PR
  work for approved changes.
- Empty result: acceptable.

## Prompt

```md
You are running Portfolio Surface Sweep.

Read first:
- The portfolio sink's own AGENTS.md and content/docs entry points.

Goal:
- Pull public-surface context from the KB once.
- Inspect the current portfolio sink state.
- Decide whether the portfolio should change.
- Present a surface summary for approval before any branch work.
- After approval, prepare branch/PR work only for approved candidates.

Lookup:
- Use /lookup in context mode over: public-safe-claim-source, network,
  selected-projects, portfolio-change-rules, identity.
- Treat public-safe-claim-source as the adapter for portfolio, recruiter-facing,
  and resume-like claims, and its public-safety boundary.
- Apply portfolio-change-rules for the portfolio model and structural constraints;
  do not invent portfolio structure here.

Source boundary:
- Factual claims, social proof, metrics, employment facts, project status, and
  project capabilities need public-safe source material.
- Editorial presentation may change with approval. Leave unsupported claims as
  gaps.

Surface summary gate:
- Before creating a branch or editing files, return a compact surface summary:
  current portfolio state checked, KB/source evidence checked, proposed
  candidates, affected surfaces/files, what changes and what stays stable,
  public-safety notes, validation plan, and announcement candidates for Social
  Draft Pulse if any.
- Ask the user to approve, reject, or edit the set. Do not create branch work
  until approved.

Branch/PR work:
- After approval, create or switch to a working branch for the approved work.
- Keep edits scoped to approved candidates. Update the canonical content model and
  mirrored docs/tests together when relevant.
- Run the portfolio sink's own validation before proposing the PR.
- Open a draft PR only if PR creation was approved; otherwise return a
  branch/patch summary.
- Do not merge, deploy, or publish without approval.

Social boundary:
- Flag announcement candidates as a handoff to Social Draft Pulse; do not create
  social drafts here.

End state:
- If no useful candidates exist, say so and include the evidence checked.
- Otherwise stop at the surface summary and wait for approval, then prepare the
  approved branch/PR work.
- Report branch name, PR link if created, validation status, blocked actions, and
  announcement candidates.
```
