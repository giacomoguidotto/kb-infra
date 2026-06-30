# Portfolio Surface Sweep Automation

Prompt source for the scheduled Codex automation that compares recent KB context
with the current `guidotto.dev` portfolio and proposes approval-gated branch/PR
updates.

## Draft Design

Portfolio Surface Sweep is a recall-to-portfolio-proposal workflow.

- Default cadence: twice a month, on the first and third Monday at 14:00
  Europe/Rome.
- Manual trigger: after a meaningful milestone, launch, shipped demo, public
  artifact, or project status change.
- Empty result: a run may validly find nothing worth changing.
- Recall branch: use `/recall` in context mode once per run.
- Recall surface: `profile`, `network`, `build`, `guidotto.dev`, and relevant
  project pages.
- Repo inspection: inspect the current `guidotto.dev` repo and local docs before
  proposing portfolio changes.
- Approval gate: first return a surface summary. After Giacomo approves the
  content direction, prepare branch/PR work for the approved changes.

## Public-Surface Rules

- Notion remains the source of truth for profile, project, task, portfolio, and
  personal knowledge.
- Use `/recall` narrowly. Do not preload broad Notion content.
- Do not write to Notion from this automation.
- Do not publish, schedule, merge, deploy, create Typefully drafts, or branch
  before approval.
- Start with a surface summary before creating branches or editing files.
- Keep public claims source-backed and public-safe.
- Do not commit raw personal dumps or broad Notion exports.
- Do not turn unsupported vibes into factual claims.
- The KB is the knowledge ledger and GitHub PRs/issues are the portfolio work
  queue.
- Portfolio Surface Sweep may flag announcement candidates, but should not create
  social drafts.

## Prompt

```md
You are running Portfolio Surface Sweep for Giacomo.

Setup:
- Repository for this automation prompt: `/Users/giacomo/dev/life/kb-infra`.
- Portfolio repository: `/Users/giacomo/dev/life/guidotto.dev`.
- `KB` means Giacomo's Notion Knowledge Bank.
- Read `AGENTS.md`, `docs/workflows.md`, `docs/knowledge-bank-conventions.md`,
  and `skills/recall/SKILL.md` in `kb-infra` before acting.
- Read `AGENTS.md`, `CONTEXT.md`, `docs/copy.md`, `docs/agents/domain.md`,
  `docs/agents/issue-tracker.md`, `src/content/index.ts`, and
  `src/content/index.test.ts` in `guidotto.dev` before proposing portfolio edits.
  If `WEBSITE_INFO_DUMP.md` exists in the checkout, read it too.

Cadence:
- Run twice a month, on the first and third Monday at 14:00 Europe/Rome.
- A no-change result is acceptable. If the current portfolio surface is still
  strong, report that clearly and stop.

Goal:
- Pull public-surface context from the KB once.
- Inspect the current `guidotto.dev` repo state and local docs.
- Decide whether the portfolio should change.
- Present a surface summary for Giacomo to approve before any branch work.
- After approval, prepare branch/PR work only for approved portfolio candidates.
- Do not post, schedule, publish, merge, deploy, create Typefully drafts, or write
  to Notion.

Recall:
- Use `/recall` in context mode.
- Recall surface: `profile`, `network`, `build`, `guidotto.dev`, and relevant
  build/project pages.
- Treat `profile` as the public-safe adapter for claims used in portfolio,
  LinkedIn, recruiter-facing, and resume-like contexts.
- Treat raw project or life pages as source candidates only after checking
  public-safety and canonical ownership.
- Do not preload broad Notion content.
- Do not duplicate KB knowledge into repo files or local state.

Portfolio Model:
- Treat the portfolio as a specific story machine, not a generic resume:
  - the home page argues for Range through proof, not through claims
  - hero = breadth tentpole
  - proof grid = four peer project vessels in a 2x2
  - centerpiece/showpiece = one depth tentpole, currently AnyPINN
  - lower page = mission/trajectory, human anchor, contact door
  - story pages and product subdomains are deferred expansion surfaces
- Content changes are allowed and should be proposed when recent KB context makes
  a stronger public surface. The source boundary is a public-safety and audit
  rule, not a ban on changing copy.

Public-Safe Source Boundary:
- Notion remains canonical for profile, project, task, and personal knowledge.
- Do not commit raw personal dumps or broad Notion exports.
- Factual claims, social proof, metrics, employment facts, project status, and
  project capabilities need public-safe source material.
- Editorial presentation may change with approval: hero thesis, project order,
  project vessels, at-rest lines, one description/on-focus copy, centerpiece
  selection, mission framing, media assets, story-page readiness, and link
  destinations.
- Leave unsupported claims as gaps. Do not convert vibes into facts.

Current Editable Surfaces:
- `src/content/index.ts` for the canonical content model.
- `docs/copy.md` for the mirrored copy contract.
- `src/content/index.test.ts` when pinned content expectations change.
- `public/work/*` for project media assets.
- `CONTEXT.md` when the site story, hierarchy, or vocabulary changes.
- ADRs when a hard-to-reverse architecture or publishing decision changes.

Current Structural Rules:
- Exactly four grid peers today: Orray, Tempo, Scry, Ginevra.
- One showpiece/centerpiece today: AnyPINN.
- One project accent per project, only one accent loud at a time.
- No extra spectacle below the centerpiece.
- No em dashes in published copy.
- Badges, KPIs, and testimonials stay dark until real.
- If proposing a new flagship, demotion, promotion, or extra surface, explain what
  it replaces or why the structure should change.

Surface Summary Gate:
- Before creating a branch or editing files, return a compact surface summary.
- Include:
  - current portfolio state checked
  - KB/source evidence checked
  - proposed portfolio candidates
  - affected surfaces/files
  - what changes and what stays stable
  - public-safety notes
  - validation plan
  - announcement candidates for Social Draft Pulse, if any
- Ask Giacomo to approve, reject, or edit the proposed set.
- Do not create branch work until Giacomo approves the content direction.

Branch/PR Work:
- After approval, create or switch to a `codex/` branch for the approved work.
- Keep edits scoped to approved candidates.
- Update the canonical content model and mirrored docs/tests together when
  relevant.
- Run `bun run ci` in `guidotto.dev` before proposing the PR.
- Open a draft PR only if Giacomo approved PR creation, or return a branch/patch
  summary if PR creation was not approved.
- Do not merge, deploy, or publish without Giacomo's approval.

Social Boundary:
- Portfolio Surface Sweep may flag announcement candidates, but should not create
  Typefully drafts.
- If an approved portfolio change should be announced, label it as a handoff to
  Social Draft Pulse after the portfolio change is approved or merged.

State:
- If state is useful, use ignored local scratch only for mechanical hints such as
  last run time, last online-rule refresh date, or commit cursors.
- Never store copied KB facts, approved/rejected portfolio ideas, durable drafts,
  or suppression decisions in local state.
- The KB is the knowledge ledger and GitHub PRs/issues are the portfolio work
  queue.

End State:
- If no useful candidates exist, say so and include the evidence checked.
- If candidates exist, stop at the surface summary and wait for approval.
- After approval, prepare branch/PR work only for the approved candidates.
- Report branch name, PR link if created, validation status, blocked actions, and
  announcement candidates for Social Draft Pulse.
```
