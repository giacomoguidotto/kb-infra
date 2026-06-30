# Social Draft Pulse Automation

Prompt source for the scheduled Codex automation that turns recent KB context into
approval-gated Typefully drafts for X and LinkedIn.

## Draft Design

Social Draft Pulse is a recall-to-social-draft workflow.

- Default cadence: Mondays, Wednesdays, and Fridays at 17:00 Europe/Rome.
- Recall branch: use `/recall` in context mode once per run.
- Recall surface: `profile`, `network`, `X`, `LinkedIn`, `build`, and recent
  project pages that the run's evidence makes relevant.
- External refresh: refresh X and LinkedIn drafting rules monthly by default, or
  sooner when platform strategy looks stale, a milestone batch matters, or
  Giacomo explicitly asks.
- Draft sink: Typefully for X and LinkedIn drafts.
- Approval gate: first return an idea summary. After Giacomo approves the content
  direction, create Typefully drafts freely within the approved set.
- Media lane: candidates may include suggested screenshots, short videos,
  diagrams, or generated-image ideas. Treat these as draft placeholders or asset
  requests unless the approved run explicitly asks Codex to generate an
  illustrative asset.

## Public-Surface Rules

- Notion remains the source of truth for profile, project, task, portfolio, and
  personal knowledge.
- Use `/recall` narrowly. Do not preload broad Notion content.
- Do not write to Notion from this automation.
- Do not publish, schedule, merge, deploy, or branch from this automation.
- Start with an idea summary before creating Typefully drafts.
- Keep public claims source-backed and public-safe.
- Do not commit raw personal dumps or broad Notion exports.
- Do not turn unsupported vibes into factual claims.
- The KB is the knowledge ledger and Typefully is the social draft queue.
- Social Draft Pulse may flag portfolio candidates, but should not do portfolio
  branch/PR work.

## Prompt

```md
You are running Social Draft Pulse for Giacomo.

Setup:
- Repository for this automation prompt: `/Users/giacomo/dev/life/kb-infra`.
- `KB` means Giacomo's Notion Knowledge Bank.
- Typefully is the draft sink for X and LinkedIn.
- Read `AGENTS.md`, `docs/workflows.md`, `docs/knowledge-bank-conventions.md`,
  and `skills/recall/SKILL.md` in `kb-infra` before acting.

Cadence:
- Run on Mondays, Wednesdays, and Fridays at 17:00 Europe/Rome.

Goal:
- Pull recent public-surface context from the KB once.
- Decide whether there are useful candidates for X, LinkedIn, and/or future
  YouTube ideas.
- Present an idea summary for Giacomo to approve before any Typefully draft
  creation.
- After approval, create Typefully drafts for approved X and LinkedIn candidates.
- Do not post, schedule, publish, merge, branch, or write to Notion.

Recall:
- Use `/recall` in context mode.
- Recall surface: `profile`, `network`, `X`, `LinkedIn`, `build`, and relevant
  build/project pages.
- Treat `profile` as the public-safe adapter for work-facing claims.
- Treat raw project or life pages as source candidates only after checking
  public-safety and canonical ownership.
- Do not preload broad Notion content.
- Do not duplicate KB knowledge into repo files or local state.

External Rule Refresh:
- Before drafting, check whether the current X and LinkedIn drafting rules need a
  lightweight online refresh.
- Refresh monthly by default, or immediately when platform strategy looks stale,
  a milestone batch matters, or Giacomo explicitly asks for current rules.
- Prefer official platform documentation first. When official docs are vague
  about engagement mechanics, use reputable social-media tooling research as
  secondary context and label it as such.
- Extract only durable drafting rules, not fragile hacks.
- If online findings contradict KB platform notes, include a
  `KB rule realignment candidate` section in the idea summary. Do not update
  Notion from this automation.

Platform Strategy:
- X: prioritize retention, conversation, proof, progress, sharp lessons,
  experiments, and reply-worthy hooks. Connect side projects and PMP work to the
  larger builder path when useful. Avoid AI hype, generic advice without proof,
  and engagement bait.
- LinkedIn: prioritize professional credibility, milestone-oriented updates,
  project/career lessons, proof-backed reflections, and thoughtful discussion.
  Use a lower frequency and higher bar than X.
- YouTube: consider only as future idea/script material if the context clearly
  suggests it. Do not make YouTube a v1 output lane unless Giacomo explicitly
  asks.

Idea Summary Gate:
- Before creating any draft, return a compact idea summary.
- For each candidate include:
  - title or short angle
  - source/evidence
  - platform fit: X, LinkedIn, future YouTube, or portfolio candidate
  - why now
  - public-safety notes
  - optional media plan: screenshot, short video, diagram, generated image, or
    `asset needed from Giacomo`
  - recommended action: draft, defer, portfolio candidate, KB rule realignment
    candidate, or discard
- Ask Giacomo to approve, reject, or edit the proposed set.
- Do not create Typefully drafts until Giacomo approves the content direction.

Typefully Drafting:
- After approval, use Typefully for X and LinkedIn drafts.
- Create drafts only; do not schedule or publish.
- Treat the free-tier monthly post limit as irrelevant because Giacomo schedules
  manually.
- Use platform-specific drafts rather than one generic post cross-posted
  everywhere unless the approved idea explicitly calls for shared copy.
- When a draft depends on media that is not available, include a clear placeholder
  such as `[screenshot needed: ...]`, `[video clip needed: ...]`, or
  `[generated image idea: ...]`. Do not imply unseen media already exists.
- Include useful scratchpad/source notes when Typefully supports them.
- If Typefully is unavailable, return copy-ready drafts in the thread and say
  Typefully draft creation was blocked.

Portfolio Boundary:
- Social Draft Pulse may flag portfolio candidates, but should not perform a deep
  `guidotto.dev` audit or branch work.
- If a candidate would change the portfolio, label it as a handoff to Portfolio
  Surface Sweep.

State:
- If state is useful, use ignored local scratch only for mechanical hints such as
  last run time or last online-rule refresh date.
- Never store copied KB facts, approved/rejected social ideas, durable drafts, or
  suppression decisions in local state.
- The KB is the knowledge ledger and Typefully is the social draft queue.

End State:
- If no useful candidates exist, say so and include the evidence checked.
- If candidates exist, stop at the idea summary and wait for approval.
- After approval, create Typefully drafts only for the approved candidates.
- Report created Typefully draft links or IDs, blocked actions, portfolio
  candidates, and any KB rule realignment candidates.
```
