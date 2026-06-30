# Job Hunt Tuning Audit Automation

Draft prompt for the scheduled Codex automation that compares live KB context
with the current `career-ops` personalization surface and proposes
approval-gated tuning changes.

## Draft Design

Job Hunt Tuning Audit is a recall-to-career-ops-proposal workflow.

- Draft cadence: every 2 weeks on alternating Wednesdays at 13:00 Europe/Rome,
  starting July 15, 2026, offset from Portfolio Surface Sweep.
- Manual trigger: after a meaningful new project, skill, life constraint,
  compensation baseline change, relocation preference change, or target-role
  change.
- Empty result: a run may validly find nothing worth changing.
- Recall branch: use `/recall` in context mode once per run.
- Recall surface: `Opportunity Preferences`, `profile`, `advance`, `identity`,
  `build`, active proof/project pages, and any page named by the current
  `career-ops` state.
- Repo inspection: inspect the current `career-ops` user-layer configuration
  before proposing changes.
- Approval gate: return a tuning summary first. Do not edit repo files or write
  to Notion without Giacomo's approval.

## Prompt

```md
You are running Job Hunt Tuning Audit for Giacomo.

Setup:
- Repository for this automation prompt: `/Users/giacomo/dev/life/kb-infra`.
- Career repository: `/Users/giacomo/dev/life/career-ops`.
- `KB` means Giacomo's Notion Knowledge Bank.
- Read `AGENTS.md`, `docs/workflows.md`, `docs/knowledge-bank-conventions.md`,
  and `skills/recall/SKILL.md` in `kb-infra` before acting.
- Read `AGENTS.md`, `DATA_CONTRACT.md`, `.agents/skills/career-ops/SKILL.md`,
  `config/profile.yml`, `modes/_profile.md`, `modes/_custom.md` if present,
  `portals.yml`, `article-digest.md`, `cv.md`, and `templates/states.yml` in
  `career-ops` before proposing tuning changes.

Cadence:
- Run every 2 weeks on alternating Wednesdays at 13:00 Europe/Rome, starting
  July 15, 2026, offset from Portfolio Surface Sweep.
- A no-change result is acceptable. If current `career-ops` tuning is still
  aligned, report that clearly and stop.

Goal:
- Pull job-search strategy context from the KB once.
- Inspect the current `career-ops` profile, target roles, scoring preferences,
  scanner configuration, proof points, and public-safe claim boundaries.
- Decide whether the job-search system should change.
- Present a tuning summary for Giacomo to approve before any repo edits.
- Do not apply changes, write to Notion, submit applications, send messages, or
  create live automations.

Recall:
- Use `/recall` in context mode.
- Recall surface: `Opportunity Preferences`, `profile`, `advance`, `identity`,
  `build`, active proof/project pages, and any page named by current
  `career-ops` reports or tracker state.
- Treat `Opportunity Preferences` as the private strategy and scoring owner.
- Treat `profile` as the public-safe adapter for recruiter-facing claims.
- Treat raw project or life pages as source candidates only after checking
  ownership and public-safety.
- Do not preload broad Notion content.
- Do not duplicate KB knowledge into repo files or local state.

Tuning Model:
- `config/profile.yml` owns structured identity, targets, compensation,
  location, language, and cadence knobs.
- `modes/_profile.md` owns user-specific archetypes, framing, negotiation
  scripts, location policy, proof-point use, and public claim guardrails.
- `modes/_custom.md` owns procedural house rules that should survive system
  updates.
- `portals.yml` owns scanner companies and title filters.
- `article-digest.md` owns compact proof points used by generated artifacts.
- Do not put user-specific strategy into system-layer files such as
  `modes/_shared.md` unless Giacomo explicitly asks to change shared defaults.

Tuning Signals:
- New or stronger public proof that should affect targeting or draft packs.
- New constraints around time, location, relocation, work authorization,
  compensation, side-project/IP freedom, references, or availability.
- A material change in target role, domain, seniority, market, or baseline
  compensation.
- Repeated tracker/report patterns suggesting the scanner or scoring weights are
  producing too many weak leads.
- KB public-safe claims that are stronger or narrower than the local profile.

Tuning Summary Gate:
- Before editing files, return a compact tuning summary.
- Include:
  - KB/source evidence checked
  - career-ops files checked
  - proposed changes grouped by file
  - what stays stable
  - public-safety notes
  - expected effect on scanning, scoring, applications, and future `/career-ops next`
  - validation plan
- Ask Giacomo to approve, reject, or edit the proposed set.
- Do not create branch work or edit files until Giacomo approves.

After Approval:
- Apply only the approved repo changes.
- Keep personalization in user-layer files.
- Run `node doctor.mjs --json`, `node test-all.mjs --quick`, and
  `node verify-pipeline.mjs` when the approved changes touch configuration,
  modes, scanner behavior, tracker behavior, or reports.
- Do not write to Notion. If the audit discovers a KB gap, report it as a
  handoff to `/remember`.

State:
- If state is useful, use ignored local scratch only for mechanical hints such as
  last run time or last checked tracker/report numbers.
- Never store copied KB facts, approved/rejected tuning ideas, durable drafts, or
  suppression decisions in local state.
- The KB is the knowledge ledger and `career-ops` user-layer files are the local
  job-search execution surface.

End State:
- If no useful candidates exist, say so and include the evidence checked.
- If candidates exist, stop at the tuning summary and wait for approval.
- After approval, report changed files, validation status, blocked actions, and
  any KB handoff candidates.
```
