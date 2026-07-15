# Automation Preamble

This file is the composer's reference material, **not** a block that is pasted
verbatim into a prompt. When `setup-kb-infra` materializes an automation it composes a
lean, self-contained prompt: it injects the [Operating Rules](#operating-rules), and
for each surface the automation **declares** it emits a single resolved line —
the role description from the [vocabulary](#vocabulary) joined with the binding hint
from `local/bindings.yml`. The full catalog, the provider block, cadence, and blank
overrides never reach the prompt. See
[ADR 0005](../adr/0005-materialized-automation-is-self-contained.md).

Reference surfaces, sinks, sources, and their capabilities **by role**, never by a
concrete page, repo, command, or path.
`/lookup` resolves an endpoint live by meaning, so a binding is a location hint, not a
hard dependency. Keep the shared rules here in one place; do not restate them inside
individual automation prompts.

## Operating Rules

Injected into every composed prompt:

- The KB is canonical; never write to it except through `/capture` approval.
- Write within your mandate: when a run surfaces a real signal worth storing, propose
  a `/capture` and reconcile it into your mandate surfaces while the context is hot.
  No run is forced to capture — an empty result is fine. Do not chase knowledge
  outside your mandate, and never infer across runs; that is Knowledge Harvest's job.
- Knowledge Harvest is the reconciler, not the primary author of KB knowledge: it
  dedups first-party captures against current KB state, proposes what a run should
  have captured but did not, and surfaces conflicts. Do not defer an in-mandate
  capture to a later harvest.
- Return a run summary and wait for approval before materializing a write into a
  sink, unless the automation body explicitly classifies a narrow in-mandate write
  as safe and ungated. That exception never authorizes a real-world action, public
  send/publish, or a record claiming one happened.
- Reconcile sink drift by the sink's kind: a mirror sink that holds a copy of a KB
  endpoint gets its copy realigned to the KB; a derived sink materialized from KB
  signals updates one way and carries no inherited drift.
- Use `/lookup` narrowly; do not preload broad KB content.
- Keep public claims source-backed and public-safe; do not turn vibes into facts.
- Do not duplicate KB knowledge into repo files or local state; the KB is the
  knowledge ledger and each sink is its own work queue.
- Resolved harness-owned automation-local state is disposable: use it only for
  mechanical hints (last completion time, refresh dates, commit cursors), never
  copied KB facts, answered questions, or approved/rejected/suppression decisions.
  Deleting it may make the next run slower, never less correct.
- Read `last_completed_at` from the resolved automation-local state location at startup.
  It records the last successful completion, not the last invocation. Update it to
  the current ISO 8601 timestamp only after the run reaches its defined End state and
  all required automation-owned work is complete. A fully checked no-op may count as
  complete. Human follow-up the automation is forbidden to perform does not prevent
  completion. Do not update it while waiting for required approval or clarification,
  or when the run is blocked, stopped on an error, or interrupted.

## Vocabulary

The composer emits one resolved line per **declared** surface, drawn from the
descriptions below. It does not inject surfaces an automation does not declare.

### Endpoints

Data surfaces and rule-sets automations read from the KB:

- `selected-projects`: the active/selected projects to consider this run.
- `public-safe-claim-source`: the adapter presenting recruiter/public-facing facts;
  also owns the public-safety boundary — what must not be published.
- `proof-points`: compact, reusable evidence and metrics for generated artifacts.
- `network`: contacts and relationships.
- `identity`: how the user frames themselves; archetypes and narrative.
- `point-of-view`: the user's recorded public stances, opinions, and recurring themes;
  grows only through approved `/capture` writes — automations read it and never
  fabricate a stance.
- `published-social-context`: the per-platform semantic audience and argument ledger:
  what the audience can be assumed to know, which concepts and projects were
  introduced, which broader arguments are in flight, and links to their canonical KB
  owners. It does not mirror post copy, publication history, queue state, or metrics;
  those remain in the bound social publishing source. Maintained through approved
  `/capture` writes and read for continuity.
- `portfolio-change-rules`: the portfolio model and structural constraints.
- `social-rules-of-engagement`: per-platform drafting strategy and guardrails — the
  project/topical content mix, the self-contained / introduce-on-first-use rule,
  day-eligibility and recovery rules, and the posting schedule: the per-platform slots
  to post in and the intended tone for each slot.
- `job-search-strategy`: target roles, compensation baseline, scoring preferences.
- `communication-strategy`: the user's canonical cross-surface voice, tone,
  charisma, authoring, persuasion, channel strategy, and evidence-sufficiency
  rules. Optional personalization only; a bound sink retains complete generic
  defaults when this endpoint is absent.
- `personal-constraints`: relocation, compensation, work authorization, references,
  availability, and side-project/IP freedom.
- `signal-preferences`: the user's criteria for what is worth remembering — the
  emergent rubric Knowledge Harvest ranks candidates against; grows only through
  approved rubric updates.

### Sinks

External systems an automation materializes into; each resolves from a binding to a
clone path (or tool handle). The primary sink clone is the run's working directory.

- `<career-system>`: the external job-search system repository. A mirror sink — it
  holds a copy of `job-search-strategy`, so writes realign that copy against the KB
  (bidirectional drift).
- `<portfolio>`: the public portfolio repository. A derived sink — materialized one-way
  from KB signals; no inherited drift.
- `<social-draft-queue>`: the social draft tool. A derived sink — materialized one-way
  from KB signals; no inherited drift.

### Sink Capabilities

Operations supplied by the concrete implementation of a bound sink. Automations
declare these by role; setup resolves each to an executable command or native
workflow instruction and emits only the declared capability into the composed
prompt.

- `advance-workflow`: the sink-native orchestration contract for selecting,
  producing, and recording Agent-owned next work. It owns the sink's lifecycle
  vocabulary and canonical writers; the automation never reconstructs them.
- `wait-review`: the sink-native read and recommendation contract for externally
  owned waits. It reads confirmed real-world attempts, current generated guidance,
  and cadence, then returns wait, next-route, deprioritize, or discard advice. It
  never invents a response, records an attempt, or changes factual lifecycle state.
- `related-opportunity-selector`: a deterministic, read-only preflight applied
  before global throughput or priority ranking. It returns an exclusive eligible
  set, suppressed related alternatives, and unresolved groups requiring research.
  An unattended automation may not bypass or override its suppression result.

### Sources

External systems an automation observes (reads, never writes); each resolves from a
binding, referenced by role:

- `<transcript-source>`: agent conversation transcripts on the local machine that
  Knowledge Harvest mines for signals. Read-only, forward-only by cursor, and private
  by default — derived signals never auto-flow to public-safe or social surfaces.
- `<social-profile-source>`: the user's own public social profiles, one per platform
  (currently X and LinkedIn), that Knowledge Harvest reads **best-effort** to reconcile
  `published-social-context` when the social sink cannot carry a post-live trigger.
  Read-only and public; a public source reconciling a public-facing ledger, so it does
  not touch the private-by-default rule. Best-effort: a platform that cannot be read
  degrades to a clarification question, never a fabricated ledger entry.
- `<social-publishing-source>`: the bound social publishing system's queue, recurring
  schedule, published history, and account analytics. Social Draft Pulse reads it
  before drafting or scheduling to avoid duplicates, find eligible open slots, and
  reconcile semantic continuity after posts go live. Read-only as a source; actual
  draft creation and scheduling happen through `<social-draft-queue>` after approval.
- `<availability-calendar-source>`: the user's upcoming calendar availability and
  free/busy evidence for the coverage window. Social Draft Pulse uses it only to apply
  the KB's day-eligibility and recovery rules. Event details are private scheduling
  evidence and never become post ideas, claims, or public copy.
- `<external-signal-source>`: a bounded public research surface for current discourse
  and ecosystem changes relevant to the user's active field and projects. Social
  Draft Pulse reads it before candidate generation. It supplies timely evidence, not
  a user stance, a verified personal claim, or a durable KB record.

### Source Capabilities

Read operations supplied by the concrete implementation of a bound source.
Automations declare these by role; setup resolves each to a concrete command or
native workflow instruction and emits only the declared capability into the composed
prompt.

- `publication-history`: read posts that actually went live, with stable identifiers,
  platform, and publication time, so the run can reconcile the semantic audience and
  argument delta without treating a scheduled draft as published.
- `post-analytics`: read account-specific performance for published posts over
  comparable windows, including any platform or metric limitations. Metrics remain in
  the source and inform controlled scheduling proposals; they are not copied into the
  KB ledger.
- `queue-timeline`: read queued and scheduled drafts with their exact times and state,
  so occupied slots and duplicates are visible before drafting.
- `queue-schedule`: read the recurring per-platform schedule, timezone, and enabled
  slots so the run can derive the eligible coverage capacity without hardcoded counts.
- `upcoming-availability`: read upcoming events or free/busy state over the coverage
  window. Calendar details stay private and are reduced to scheduling constraints.
- `current-public-signals`: read recent primary sources and direct public evidence
  relevant to the user's active field and projects, preserving source and observed
  date and distinguishing recurring signals from isolated attention spikes.

## Follow-up Marker Policy

Automations that declare a dependency on deferred-knowledge markers (Knowledge
Harvest) use the follow-up and final-form marker formats in
[knowledge-bank-conventions.md](../knowledge-bank-conventions.md). Those formats are
**inlined** into the composed prompt at materialize time, not left as a file path for
the run to open. This ships as the repo default; `setup-kb-infra` offers to override it
as a binding.
