# Knowledge Bank Infrastructure

## Glossary

**Knowledge Bank Infrastructure**: The source-of-record for a provider-backed agent operating system. It holds the definitions — agent skills, automation prompts, and Knowledge Bank conventions — that materialize into live systems elsewhere. The provider is the memory, the harness runtime runs the automations, this repo is the spec.
_Avoid_: second brain, source of truth, runtime, knowledge store

**Materialization**: The live system a repo definition becomes once it runs elsewhere: a scheduled automation, a KB page structure, or an agent-loaded skill. The repo owns the definition; the materialization runs outside it.

**Execution Profile**: A provider-agnostic recommendation for the capability,
reasoning depth, and delegation posture an automation needs. The committed spec
declares the profile; setup resolves it to a concrete model and reasoning effort
supported by the local harness, records that choice in gitignored `local/`, and
materializes it as harness metadata rather than prompt text.

**KB Provider**: The backend that stores a Knowledge Bank. The spec is provider-agnostic and discovers the concrete provider and structure at setup.

**Endpoint**: A named context surface or rule-set an automation reads from the KB, such as selected projects, public-safe claim source, portfolio change rules, or social rules of engagement. Automations reference endpoints by role; setup binds each to a concrete KB location.

**Point-of-View Surface**: An incrementally-built KB endpoint holding the user's public persona — recorded stances, opinions, and recurring themes that topical social drafts draw from. It grows over time only through approved `/capture` writes; automations read it and never fabricate a stance.

**Published Social Context**: A per-platform semantic audience and argument ledger. It records what an audience can be assumed to know, which concepts and projects were introduced, which broader arguments are in flight, and pointers to their canonical KB owners. It deliberately does not mirror post copy, publication history, queue state, analytics, or concepts already owned elsewhere in the KB. Automations read it for continuity and maintain semantic deltas through approved `/capture` writes after reconciling live publication evidence.

**Sink**: An external system an automation materializes into, such as a career system, a portfolio repo, or a social draft queue. Referenced by role, never by repo name or path.

**Sink Capability**: A named operation required from a sink implementation, such
as an advancement workflow, wait review, or deterministic related-opportunity selector. The
committed automation references the capability by role; setup binds it to a
concrete command or native workflow and injects that only into the materialized
prompt.

**Communication Strategy**: The canonical KB endpoint for the user's cross-surface
voice, tone, charisma, authoring, persuasion, channel strategy, and evidence-
sufficiency rules. It is an optional personalization input to sinks, never a
dependency: a sink must retain complete generic defaults when it is absent. Other
surfaces link to it rather than copying settled guidance.

**Source Capability**: A named read operation required from a source implementation,
such as publication history, post analytics, queue state, recurring schedule, or
upcoming availability. The committed automation references the capability by role;
setup binds it to a concrete command or native workflow and injects that only into
the materialized prompt.

**Mirror Sink**: A sink that stores its own copy of a KB endpoint, such as `career-system` holding a copy of `job-search-strategy`. A first-party capture that changes the mirrored endpoint realigns the sink's copy; drift is bidirectional.

**Derived Sink**: A sink materialized one-way from KB signals, such as `portfolio` or `social-draft-queue`. The KB is the single source; the sink carries no inherited drift.

**Binding**: A concrete local value for a provider, sink, source, sink or source
capability, endpoint, cadence, or runtime model selection, supplied or resolved at
setup and stored in gitignored `local/`. Personal and provider-specific values are
never committed.

**Setup**: A user-invoked skill that materializes the infrastructure: it connects the KB provider, collects bindings through a grill, installs the lookup and capture skills, and bootstraps the automations.

**kb-infra**: The repository and artifact slug for Knowledge Bank Infrastructure.
_Use for_: GitHub URLs, CLI identifiers, generated artifact names, and other machine-facing handles

**Knowledge Bank**: The provider-backed personal knowledge system. It is not duplicated into this repo.

**KB**: Conversational shorthand for the Knowledge Bank.
_Use for_: agent conversations and user requests that refer to the provider-backed knowledge system
_Avoid_: using `KB` for this repository; use `kb-infra` when referring to Knowledge Bank Infrastructure

**Capture**: A user-invoked skill that drafts durable session knowledge into the KB through `/capture`, behind an HTML approval gate. It is not an accepted workflow.

**Mandate**: The set of KB endpoints and the sink an automation is authorized to write within. Write-authority is mandate-scoped: an automation captures only in-context knowledge that falls inside its mandate, and leaves everything else to Knowledge Harvest.

**First-Party Capture**: An automation writing knowledge from its own run into its mandate surfaces — the KB through `/capture` approval and/or its sink — while the context is hot, instead of deferring to Knowledge Harvest.

**Lookup**: A read-only retrieval skill used by workflows to fetch live KB context, with an optional clarification branch for missing, stale, due, or ambiguous facts.

**Knowledge Harvest**: A scheduled observe-to-capture workflow that harvests signals from the user's activity and populates the KB. It runs one pattern — `observe(source) → generate candidates → rank/dedup → reconcile → clarify → capture` — over many sources (KB-internal staleness, git history, agent transcripts, public social profiles), fanning out one subagent per source, then asks the user one clarification question at a time before drafting exact `/capture` writes for approval. As the reconciler of first-party captures, it dedups candidates against current KB state, proposes what an automation's run should have captured but did not, and surfaces conflicts. It also reconciles `published-social-context` best-effort from the Social Profile Source when the social sink cannot carry a post-live trigger.
_Avoid_: Knowledge Bank Drift Realignment (renamed)

**Signal**: A candidate piece of durable knowledge worth remembering that Knowledge Harvest surfaces from a source — a fact, decision, stated opinion, recurring theme, project-state change, or working-style pattern. A signal is a candidate for approval, never an automatic KB write.

**Signal-preferences**: A KB endpoint holding the user's criteria for what is worth remembering — the emergent rubric Knowledge Harvest reads to rank candidates. It starts as a loose seed of registers plus a permanent open "surprising/uncategorised" bucket and grows only through approved rubric updates, rendered as a distinct block in the `/capture` draft.

**Social Draft Pulse**: A scheduled feedback-to-social-draft workflow that begins with recent account analytics and current external signals, then combines that evidence with public-safe KB context to decide whether to hold, refine, test, or realign the next approved candidate set. It fills eligible open slots across the coverage window, evaluates eligible days without recurring slots as controlled testing-window candidates, uses private calendar availability only to apply KB scheduling rules, and keeps continuity through the semantic published social context plus live publishing state. It never changes the recurring schedule autonomously. Approved media-dependent posts remain unscheduled drafts until the user confirms the required attachment or approves media-independent replacement copy. It first-party-captures a point-of-view take stated at the gate and batches semantic published-social-context updates after posts go live (both public-facing, via explicit-consent `/capture`), but never publishes immediately.

**Social Publishing Source**: The read-only view of the bound social publishing
system: publication history, account analytics, queue timeline, and recurring posting
schedule. It supplies live operational evidence; it is not a duplicate KB ledger.

**Availability Calendar Source**: A read-only source of upcoming events or free/busy
state used to apply the KB's day-eligibility and recovery rules. Calendar details are
private scheduling evidence and never become content candidates or public claims.

**External Signal Source**: A read-only public research surface for current discourse
and ecosystem changes relevant to active projects and the user's field. It supplies
timely evidence for Social Draft Pulse, but never creates a user stance, verifies a
personal claim, or becomes a duplicate KB ledger.

**Social Profile Source**: A read-only external source, one per platform (currently X and LinkedIn), holding the user's own public social profiles. Knowledge Harvest reads it best-effort to reconcile the published social context ledger when the social sink cannot carry a post-live trigger. It is a public source feeding a public-facing surface, so it is exempt from the transcript private-by-default rule; a platform that cannot be read degrades to a clarification question, never a fabricated entry.

**Portfolio Surface Sweep**: A scheduled lookup-to-portfolio-proposal workflow that compares public-safe KB context with the current portfolio sink, then prepares approved branch/PR work for portfolio candidates. Its capture mandate is empty — a pure consumer that writes only to the portfolio sink. It does not create social drafts, merge, deploy, publish, or write to the KB.

**Job Hunt Evaluate Audit**: A scheduled discovery-to-evaluation workflow in the career system sink. It drains existing queue work first, scans bounded new postings only when useful, generates reports and tracker rows, and stops before application or outreach work. It realigns the career-system `job-search-strategy` mirror copy from the KB each run and first-party-captures a strategy signal when one surfaces, absorbing the retired Job Hunt Tune Audit.

**Job Hunt Advance Audit**: A scheduled tracker-to-next-plan and wait-review workflow that consumes `Job Hunt Evaluate Audit` output. For user-owned work it asks the career-system sink to produce ranked, copy-pasteable routes through its own communication planner and records only safe agent-owned projection state. For externally owned waits it asks the sink to review confirmed attempts and cadence, then drafts or recommends the next route without inventing a response or changing factual lifecycle state. It resolves the current job-application throughput target, uses optional `communication-strategy` personalization when available, and always checks whether personal outcome evidence is sufficient before drawing a channel conclusion. Draft plans and safe internal projection writes are ungated. The approval gate survives for every real-world action and record that asserts one happened. It first-party-captures a `personal-constraints` or `job-search-strategy` signal when advancing surfaces one, then realigns the career-system copy.

**Drift Audit**: A read-only convention check for Knowledge Bank structure, ownership, naming, role, and stale-state drift. It is the KB-internal-staleness source within Knowledge Harvest — a lower-level review pattern, not the whole automation.

**Follow-up Marker**: A short page-body line that tells a future lookup to ask the user about a deferred or time-ambiguous update.

**Approval Draft**: A reviewable proposal showing exact KB writes before anything is applied.

**Narrow Load**: Read only the Knowledge Bank Infrastructure docs or KB pages relevant to the current task.

**Type, Ownership, Maturity, Kind**: The KB's four independent semantic axes: what
a page represents; where meaning is owned; how editorially processed it is; and
what a section means. Their values and rules live in
[Knowledge Bank Conventions](docs/knowledge-bank-conventions.md).

**Active Canonical View**: The relevant, current human-facing KB. History remains
recoverable without keeping obsolete pages in ordinary views.

**Revision Evidence**: Recoverable source, actor, time, prior revision, and exact
change behind an accepted KB mutation.
