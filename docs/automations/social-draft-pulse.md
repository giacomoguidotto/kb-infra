# Social Draft Pulse Automation

Prompt source for the scheduled automation that turns recent KB context into
approval-gated drafts in the `social-draft-queue` sink. Include
[the preamble](_preamble.md) when materializing this automation.

## Design

Social Draft Pulse is a lookup-to-social-draft workflow.

- lookup branch: context, once per run.
- Endpoints: `public-safe-claim-source`, `network`, `social-rules-of-engagement`,
  `selected-projects`, `identity`.
- Sink: `<social-draft-queue>`.
- Approval gate: return an idea summary first. After approval, create drafts
  freely within the approved set.
- Empty result: acceptable.

## Prompt

```md
You are running Social Draft Pulse.

The preamble is prepended to this prompt at materialize time.

Setup:
- Read this repo's AGENTS.md, docs/workflows.md,
  docs/knowledge-bank-conventions.md, docs/automations/_preamble.md, and
  skills/lookup/SKILL.md before acting.

Goal:
- Pull recent public-surface context from the KB once.
- Decide whether there are useful work-facing social candidates.
- Present an idea summary for approval before creating any draft.
- After approval, create drafts in the social-draft-queue sink.

Lookup:
- Use /lookup in context mode over: public-safe-claim-source, network,
  social-rules-of-engagement, selected-projects, identity.
- Treat public-safe-claim-source as the adapter for work-facing claims and its
  public-safety boundary.
- Apply social-rules-of-engagement for platform strategy and guardrails; do not
  invent platform rules here.

External rule refresh:
- Follow the refresh cadence named in social-rules-of-engagement. Prefer official
  platform docs; label tooling research as secondary.
- If online findings contradict the KB rules, include a "KB rule realignment
  candidate" section in the summary. Do not write to the KB from this automation.

Idea summary gate:
- Before creating any draft, return a compact idea summary. For each candidate
  include: angle, source/evidence, platform fit, why now, public-safety notes,
  optional media plan, and recommended action (draft, defer, portfolio candidate,
  KB rule realignment candidate, or discard).
- Ask the user to approve, reject, or edit the set. Do not create drafts until the
  content direction is approved.

Drafting:
- After approval, create drafts only, in the social-draft-queue sink.
- Prefer platform-specific drafts over one generic cross-post unless the approved
  idea calls for shared copy.
- Use clear placeholders for missing media (e.g. [screenshot needed: ...]). Do not
  imply unseen media exists.
- If the sink is unavailable, return copy-ready drafts in the thread and say draft
  creation was blocked.

Portfolio boundary:
- Flag portfolio candidates as a handoff to Portfolio Surface Sweep; do not do
  portfolio branch work here.

End state:
- If no useful candidates exist, say so and include the evidence checked.
- Otherwise stop at the idea summary and wait for approval, then create the
  approved drafts.
- Report created draft links or IDs, blocked actions, portfolio candidates, and
  any KB rule realignment candidates.
```
