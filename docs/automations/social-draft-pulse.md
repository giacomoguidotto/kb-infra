# Social Draft Pulse Automation

Prompt source for the scheduled automation that turns recent KB context into
approval-gated drafts in the `social-draft-queue` sink. Include
[the preamble](_preamble.md) when materializing this automation.

## Design

Social Draft Pulse is a lookup-to-social-draft workflow.

- lookup branch: context, once per run.
- Endpoints: `public-safe-claim-source`, `network`, `social-rules-of-engagement`,
  `selected-projects`, `identity`, `point-of-view`, `published-social-context`.
- Sink: `<social-draft-queue>` — a derived sink; materialized one-way, no mirror to
  realign.
- Source: `<typefully-published-source>` — Typefully queue, scheduled, and published
  state for the bound social set.
- Mandate: first-party-capture within its own surfaces — a `point-of-view` signal when
  the user states a take at the gate, and the `published-social-context` ledger. Both
  are public-facing, so each is proposed through `/capture` as a distinct,
  explicit-consent block. Signal-triggered; an empty run captures nothing.
- Volume and mix: honor the per-run volume target and the project/topical content
  mix defined in `social-rules-of-engagement`; do not hardcode either here.
- Scheduling: read the posting schedule from `social-rules-of-engagement` — the per-
  platform slots and each slot's intended tone. After approval, schedule approved
  drafts in Typefully. Do not publish immediately.
- Late-day runs: if the automation runs too late for the current day, schedule into the
  next coverage window instead of compressing posts into the remainder of the day. For
  the Wednesday late-afternoon run, schedule across Thursday and Friday.
- Two candidate branches: project/proof candidates mined from the KB, and topical
  candidates hooked to current public discourse. Topical angles come from
  `point-of-view` and `identity`; the automation never fabricates a stance.
- Continuity: read `published-social-context` and the Typefully published/queue state
  to keep a per-platform narrative and to apply the self-contained /
  introduce-on-first-use rule from `social-rules-of-engagement`. Do not reference
  internal vocabulary the platform's audience has not been given.
- Approval gate: return an idea summary first. Surface topical hooks that need the
  user's take at the gate. After approval, create drafts freely within the approved
  set.
- Writes go through `/capture`, not scheduling silence: a new take becomes a
  `point-of-view` capture the run proposes directly. `published-social-context` capture
  is trigger-deferred — its signal is a post going live. Use Typefully published state
  as the first read source for what actually went out, then propose the ledger update
  through `/capture`. SDP never publishes immediately.
- Empty result: acceptable.

## Prompt

```md
You are running Social Draft Pulse.

Goal:
- Pull recent public-surface context from the KB once.
- Produce a candidate set that honors the per-run volume target and the
  project/topical content mix in social-rules-of-engagement.
- Recommend a posting slot and a slot-matched tone for each draft, from the
  schedule in social-rules-of-engagement.
- Keep continuity with what has already been published, per platform.
- Present an idea summary for approval before creating any draft.
- After approval, create drafts in the social-draft-queue sink and schedule them in
  Typefully across the appropriate coverage window.

Lookup:
- Use /lookup in context mode over: public-safe-claim-source, network,
  social-rules-of-engagement, selected-projects, identity, point-of-view,
  published-social-context.
- Treat public-safe-claim-source as the adapter for work-facing claims and its
  public-safety boundary.
- Apply social-rules-of-engagement for platform strategy, volume, content mix, and
  guardrails; do not invent platform rules here.
- Read the posting schedule in social-rules-of-engagement — the per-platform slots and
  each slot's intended tone — and use it to place and voice each draft.
- Read published-social-context and Typefully published/queue state for what has
  already gone out, what is already scheduled, and which concepts and projects have
  been introduced on each platform.
- Read point-of-view for the user's recorded stances and recurring themes.

Candidate branches:
- Project/proof branch: mine selected-projects and public-safe-claim-source for
  progress, proof, and milestone candidates.
- Topical branch: hook to current public discourse relevant to the user's field.
  Ground every topical angle in point-of-view or identity. Where no recorded stance
  fits, surface the hook at the gate and ask the user for their take; never
  manufacture an opinion or turn a hook into a claim.

Continuity and assumed knowledge:
- Apply the self-contained / introduce-on-first-use rule from
  social-rules-of-engagement, using published-social-context to know, per platform,
  what the audience has already been given.
- Introduce (define in-post) a concept the first time it appears on a platform;
  build on it once it has been introduced there.
- Do not reference internal vocabulary — project or system shorthand — that the
  platform's audience has not been introduced to.
- Sequence the run's drafts as a per-platform narrative, not isolated one-offs.

External rule refresh:
- Follow the refresh cadence named in social-rules-of-engagement. Prefer official
  platform docs; label tooling research as secondary.
- If online findings contradict the KB rules, include a "KB rule realignment
  candidate" section in the summary. Do not write social-rules-of-engagement — it is a
  tunable rule dial outside this run's capture mandate.

Idea summary gate:
- Before creating any draft, return a compact idea summary sized to the volume and
  mix targets. For each candidate include: content type (project or topical),
  angle, source/evidence, platform fit, recommended posting slot and the slot's
  tone (from social-rules-of-engagement), why now, whether it introduces a concept
  new to that platform, public-safety notes, optional media plan, and recommended
  action (draft, defer, needs-your-take, portfolio candidate, point-of-view capture
  candidate, KB rule realignment candidate, or discard).
- For topical candidates without a recorded stance, mark them needs-your-take and
  request the user's line before drafting them.
- Ask the user to approve, reject, or edit the set. Do not create drafts until the
  content direction is approved.

Drafting:
- After approval, create drafts in the social-draft-queue sink.
- Write each draft in the tone of its recommended slot, and note the recommended
  slot on the draft using the sink's own scheduling note or scratchpad.
- Schedule approved drafts in Typefully, using the per-run coverage target. If the
  current day is already late relative to the automation cadence, use subsequent days
  in the coverage window instead of scheduling into the current evening.
- Do not publish immediately. Scheduling is allowed after approval; instant publishing
  still requires an explicit publish-now instruction.
- Prefer platform-specific drafts over one generic cross-post unless the approved
  idea calls for shared copy.
- Use clear placeholders for missing media (e.g. [screenshot needed: ...]). Do not
  imply unseen media exists.
- If the sink is unavailable, return copy-ready drafts in the thread and say draft
  creation was blocked.

Persona and continuity persistence:
- When the user gives a new take at the gate, first-party-capture it: propose a
  /capture to point-of-view directly, as an explicit-consent block (a public-facing
  surface). This is your mandate — do not defer it to Knowledge Harvest.
- published-social-context is trigger-deferred: once Typefully shows a post as live,
  propose the ledger update through /capture so the next run stays in continuity.
  Knowledge Harvest still backstops missed live-post reconciliation.

Portfolio boundary:
- Flag portfolio candidates as a handoff to Portfolio Surface Sweep; do not do
  portfolio branch work here.

End state:
- If no useful candidates exist, say so and include the evidence checked.
- Otherwise stop at the idea summary and wait for approval, then create the
  approved drafts and schedule them.
- Report created draft links or IDs, scheduled times, blocked actions,
  needs-your-take items, portfolio candidates, point-of-view capture candidates,
  published-social-context updates to record, and any KB rule realignment candidates.
```
