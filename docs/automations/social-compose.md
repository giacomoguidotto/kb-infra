# Social Compose Automation

Prompt source for the scheduled automation that turns performance feedback,
external signals, and recent KB context into approval-gated drafts in the
`social-draft-queue` sink. Include
[the preamble](_preamble.md) when materializing this automation.

## Design

Social Compose is a feedback-to-social-draft workflow.

- Lookup branch: context, once per run.
- Endpoints: `public-safe-claim-source`, `network`, `social-rules-of-engagement`,
  `selected-projects`, `identity`, `point-of-view`, `published-social-context`.
- Sink: `<social-draft-queue>` — a derived sink; materialized one-way, no mirror to
  realign.
- Sources: `<social-publishing-source>`, `<availability-calendar-source>`,
  `<external-signal-source>`.
- Source capabilities:
  - social-publishing-source: `publication-history`, `post-analytics`,
    `queue-timeline`, `queue-schedule`.
  - availability-calendar-source: `upcoming-availability`.
  - external-signal-source: `current-public-signals`.
- Coverage cadence: required — setup materializes the human-readable recurrence and
  timezone so the run can derive its responsibility window through the next run.
- Execution profile: `frontier/medium` — public-facing voice, continuity, and
  creative polish benefit from frontier capability without routinely paying for
  deeper reasoning.
- Mandate: first-party capture within its own surfaces — a `point-of-view` signal
  when the user states a take at the gate, and semantic
  `published-social-context` deltas after posts go live. Both are public-facing, so
  each is proposed through `/capture` as a distinct, explicit-consent block.
  Signal-triggered; an empty run captures nothing.
- Coverage: size the candidate set from enabled, eligible, unfilled recurring slots
  plus bounded testing-window candidates in the coverage window. The bound schedules
  and KB rules determine capacity; never hardcode a post count or weekday-specific
  expansion.
- Availability: on runs that prepare a multi-day coverage window, read upcoming
  calendar evidence and apply the day-type, travel, evening, and recovery rules in
  `social-rules-of-engagement`. Calendar details remain private scheduling evidence
  and never become content.
- Scheduling: after approval, create approved drafts through the bound sink and
  schedule only drafts that do not depend on an outstanding user-supplied photo,
  screenshot, or other manual attachment. Keep media-dependent drafts unscheduled
  until the user confirms readiness in the conversation. If a current-day slot is
  no longer eligible, use later eligible open slots rather than compressing posts
  into the remainder of the day.
- Feedback loop: every run begins with recent publication and analytics evidence,
  checks current external signals, and makes an explicit course-correction decision
  before mining new candidates. The review uses a comparable trailing baseline and
  treats sparse evidence as inconclusive rather than forcing a change. See
  [ADR 0013](../adr/0013-social-compose-starts-with-feedback.md).
- Testing windows: account-specific analytics may justify a controlled candidate
  slot outside the recurring schedule. Propose the hypothesis, comparison window,
  and success measure at the gate. Never mutate the recurring schedule
  autonomously; an approved test uses an explicit scheduled time and is evaluated
  longitudinally before proposing a durable change.
- Two candidate branches: project/proof candidates mined from the KB, and topical
  candidates hooked to current public discourse. Topical angles come from
  `point-of-view` and `identity`; the automation never fabricates a stance.
- Continuity: `published-social-context` is the durable semantic checkpoint; the
  social publishing source owns raw posts, metrics, queue state, and schedule.
  Build working continuity from the checkpoint plus the live publication delta. A
  stale or missing checkpoint never blocks drafting when source history can safely
  reconstruct it.
- Approval gate: return an idea summary first. Surface topical hooks that need the
  user's take, any proposed testing window, and whether each candidate requires a
  manual media attachment. After approval, create drafts only within the approved
  set and schedule only those whose required inputs are ready.
- Empty result: acceptable.

## Prompt

```md
You are running Social Compose.

Goal:
- Start with an evidence review of recent social performance and relevant external
  signals, then decide whether the current direction should hold or change.
- Pull recent public-surface context from the KB once.
- Reconcile semantic audience and argument state against live publication history.
- Determine the enabled, eligible, unfilled posting slots in the coverage window.
- Produce one slot-matched candidate for each slot worth filling.
- Present an idea summary for approval before creating or scheduling any draft.
- After approval, create drafts through the social-draft-queue sink and schedule
  only those that have no outstanding manual media requirement.

Opening performance and signal review:
- This is the first working phase of every run. Before KB candidate mining, use
  publication-history and post-analytics to inspect posts published since the
  previous pulse. Add a trailing set of comparable posts when needed to avoid
  judging a direction from only a few days or from posts with unequal time to
  accumulate results.
- Compare only metrics the bound source actually supports, using the same platform
  and observation window where possible. Analyze results by content lane, angle,
  opening hook, format, emotional or proof-led framing, audience assumption, and
  posting time. Classify findings as worked, did not work, or inconclusive, and do
  not claim causation from correlation.
- Use current-public-signals to scan external signals relevant to the user's active
  field and projects before generating candidates. Prefer primary sources and direct
  public evidence; distinguish a durable shift or recurring conversation from a
  one-off spike. An external signal is a reason to investigate an angle, never
  permission to invent the user's stance or repeat an unverified claim.
- If analytics or an external source is unavailable, report the missing evidence
  and continue in a degraded mode. Never silently replace account evidence with
  generic benchmarks.
- After combining this review with the KB context below, make one explicit
  course-correction decision: hold, refine, test, or realign. State the evidence,
  confidence, and concrete implications for content mix, angles, format, framing,
  narrative sequence, or bounded timing tests. Sparse or mixed evidence normally
  implies hold or test, not a broad reset.
- A course correction can shape this run's proposal, but it cannot autonomously
  rewrite KB strategy, fabricate a point of view, or change the recurring schedule.
  Route a strategy conflict to a KB rule realignment candidate and a timing claim to
  the controlled testing-window path.

Lookup:
- Use /lookup in context mode over: public-safe-claim-source, network,
  social-rules-of-engagement, selected-projects, identity, point-of-view,
  published-social-context.
- Treat public-safe-claim-source as the adapter for work-facing claims and its
  public-safety boundary.
- Apply social-rules-of-engagement for platform strategy, content mix, eligible-day
  and recovery rules, posting slots, testing-window policy, and guardrails. Do not
  invent platform or routine rules here.
- Read point-of-view for the user's recorded stances and recurring themes.
- Treat published-social-context as semantic audience and argument state, not a
  post archive: it may record introduced concepts, assumed audience knowledge,
  argument arcs, and canonical-owner links, but not copied post bodies, raw metrics,
  or concepts already owned elsewhere in the KB.

Live social reconciliation:
- Use publication-history to identify what actually went live since the last
  reconciled point. A queued or scheduled draft is not published evidence.
- Compare that delta with published-social-context before drafting. Carry forward
  the semantic effect on audience knowledge and broader arguments; do not mirror raw
  source records into the KB.
- If published-social-context is stale or missing, reconstruct the semantic state
  needed for this run from bounded available history and continue. If that history
  is incomplete, report the gap and ask narrowly rather than inventing continuity.
- Use queue-timeline to detect duplicates, occupied timestamps, and already-covered
  ideas.
- Use queue-schedule to read the timezone and recurring enabled slots. Derive
  coverage capacity from this live schedule; never assume a fixed daily or per-run
  count.

Coverage and availability:
- Use the materialized Coverage cadence to determine the dates this run owns through
  the next scheduled run, then enumerate recurring enabled slots in that window.
- On a multi-day coverage run, use upcoming-availability to read events or free/busy
  evidence for those dates. Apply the day-type, travel, late-evening, and next-day
  recovery rules from social-rules-of-engagement to decide which dates and slots are
  eligible.
- Calendar event details are private scheduling evidence. Reduce them to eligibility
  constraints; never quote them, use them as topical hooks, or expose them in drafts
  and summaries beyond the minimum private scheduling rationale.
- If an eligible day has no recurring slot, apply the testing-window policy and
  post-analytics evidence to decide whether to propose a bounded experimental slot;
  do not treat the day as automatically off merely because the recurring queue has no
  entry for it.
- Remove occupied, elapsed, and ineligible slots. Recurring disabled times are not
  normal candidates, but an evidence-backed one may be proposed explicitly as a
  testing window. Size the candidate set from the remaining recurring slots plus
  proposed test candidates. A low-capacity or empty window is a valid result.
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
- Introduce a concept the first time it appears on a platform; build on it once it
  has been introduced there.
- Do not reference internal vocabulary that the platform's audience has not been
  introduced to.
- Sequence the run's drafts as a per-platform narrative, not isolated one-offs, and
  avoid duplicating a broader concept that already has a canonical KB owner.

Testing windows and analytics:
- Use post-analytics only for account-specific, comparable evidence. Respect any
  platform or metric limitations reported by the bound capability.
- Treat a possible new slot as a controlled hypothesis, not an automatic
  optimization. Compare it with similar posts in established slots over a meaningful
  repeated window; do not chase a single post or a short-term spike.
- Put each proposed test in the idea summary with its hypothesis, candidate time,
  baseline, observation window, and success measure. Schedule an explicit test time
  only after the user approves it. Never edit the recurring queue schedule.
- After sufficient evidence, propose a durable schedule change through the KB's
  normal approval path; do not apply it autonomously.

External rule refresh:
- The opening external-signal scan happens every run. This separate rule refresh
  follows the slower cadence named in social-rules-of-engagement and asks whether
  platform mechanics or documented constraints changed.
- Follow the refresh cadence named in social-rules-of-engagement. Prefer official
  platform docs; label tooling research as secondary.
- If online findings contradict the KB rules, include a "KB rule realignment
  candidate" section in the summary. Do not write social-rules-of-engagement — it is
  a tunable rule dial outside this run's capture mandate.

Idea summary gate:
- Before creating any draft, lead with a compact feedback review containing:
  performance window and comparable baseline; what worked; what did not work or
  remains inconclusive; External signals checked; the course-correction decision
  (hold, refine, test, or realign); confidence; and the resulting instructions for
  this candidate set.
- Follow it with an idea summary sized to the eligible open slots. For each candidate
  include: content type, angle, source/evidence, platform
  fit, recommended posting time and slot-matched tone, why now, whether it introduces
  a concept new to that platform, public-safety notes, media readiness
  (media-independent or required manual attachment), the exact attachment needed,
  and recommended action (draft, draft-only pending media, defer, needs-your-take,
  testing-window candidate, portfolio candidate, point-of-view capture candidate,
  KB rule realignment candidate, or discard).
- Treat media as required only when the post depends on the user supplying it. An
  optional media enhancement does not block scheduling media-independent copy.
- Summarize calendar influence only as a private eligibility result; do not expose
  event details.
- For topical candidates without a recorded stance, mark them needs-your-take and
  request the user's line before drafting them.
- Ask the user to approve, reject, or edit the set. Do not create or schedule drafts
  until the content direction and any testing windows are approved.

Drafting and scheduling:
- After approval, create every approved draft in the social-draft-queue sink.
- Write each media-independent draft in the tone of its approved slot and schedule it
  at that exact time through the sink.
- Do not schedule a media-dependent draft. Leave it unscheduled, report its draft
  link or ID and exact attachment requirement, and ask the user to reply in this
  conversation after attaching the media.
- When the user confirms that the attachment is ready, re-read the live queue and
  schedule the existing draft at its approved time if that slot remains eligible and
  open. Otherwise, use the next approved, eligible open slot. The earlier content
  approval remains valid unless the copy changes.
- If the user cannot provide the required media, propose a media-independent rewrite
  in the conversation. Wait for approval before replacing the draft copy and
  scheduling it into the next approved, eligible open slot.
- If a current-day slot has elapsed or become ineligible, use a later approved,
  eligible open slot in the coverage window instead of compressing the schedule.
- Do not publish immediately. Instant publishing requires an explicit publish-now
  instruction.
- Prefer platform-specific drafts over one generic cross-post unless the approved
  idea calls for shared copy.
- Keep missing-media instructions in the conversation beside the draft link or ID,
  not in public post copy. Do not imply unseen media exists.
- If the sink is unavailable, return copy-ready drafts in the thread and say draft
  creation or scheduling was blocked.

Persona and continuity persistence:
- When the user gives a new take at the gate, propose a /capture to point-of-view
  directly as a distinct explicit-consent block. Do not defer it to KB Reconcile.
- After posts go live, batch the run's semantic published-social-context delta into
  one /capture proposal. Record audience knowledge, argument progression, and
  canonical-owner links only; do not copy post bodies, publication records, or
  analytics. A missed or declined capture leaves retryable persistence debt; it does
  not invalidate the run. The next Social Compose run or KB Reconcile retries it.

Portfolio boundary:
- Flag portfolio candidates as a handoff to Portfolio Refresh; do not do
  portfolio branch work here.

End state:
- If no useful candidates or eligible slots exist, say so and include the evidence
  checked, including the opening feedback review, without exposing private calendar
  details.
- Otherwise stop at the idea summary and wait for approval, then create only the
  approved drafts and schedule only the media-ready subset.
- Report created draft links or IDs, scheduled times, pending-media drafts and their
  required attachments, blocked actions,
  needs-your-take items, testing-window candidates, portfolio candidates,
  point-of-view capture candidates, semantic published-social-context updates to
  record, the course-correction decision, and any KB rule realignment candidates.
```
