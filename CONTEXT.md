# Knowledge Bank Infrastructure

## Glossary

**Knowledge Bank Infrastructure**: The source-of-record for a provider-backed agent operating system. It holds the definitions — agent skills, automation prompts, and Knowledge Bank conventions — that materialize into live systems elsewhere. The provider is the memory, the harness runtime runs the automations, this repo is the spec.
_Avoid_: second brain, source of truth, runtime, knowledge store

**Materialization**: The live system a repo definition becomes once it runs elsewhere: a scheduled automation, a KB page structure, or an agent-loaded skill. The repo owns the definition; the materialization runs outside it.

**KB Provider**: The backend that stores a Knowledge Bank. The spec is provider-agnostic and discovers the concrete provider and structure at setup.

**Endpoint**: A named context surface or rule-set an automation reads from the KB, such as selected projects, public-safe claim source, portfolio change rules, or social rules of engagement. Automations reference endpoints by role; setup binds each to a concrete KB location.

**Point-of-View Surface**: An incrementally-built KB endpoint holding the user's public persona — recorded stances, opinions, and recurring themes that topical social drafts draw from. It grows over time only through approved `/capture` writes; automations read it and never fabricate a stance.

**Published Social Context**: A per-platform KB endpoint recording what has already been published and which concepts and projects have been publicly introduced on each channel. Automations read it to keep continuity and avoid assuming audience knowledge; it is maintained through approved `/capture` writes, not written by draft automations.

**Sink**: An external system an automation materializes into, such as a career system, a portfolio repo, or a social draft queue. Referenced by role, never by repo name or path.

**Binding**: A concrete personal value for a sink or endpoint, supplied at setup and stored in gitignored `local/`. Never committed.

**Setup**: A user-invoked skill that materializes the infrastructure: it connects the KB provider, collects bindings through a grill, installs the lookup and capture skills, and bootstraps the automations.

**kb-infra**: The repository and artifact slug for Knowledge Bank Infrastructure.
_Use for_: GitHub URLs, CLI identifiers, generated artifact names, and other machine-facing handles

**Knowledge Bank**: The provider-backed personal knowledge system. It is not duplicated into this repo.

**KB**: Conversational shorthand for the Knowledge Bank.
_Use for_: agent conversations and user requests that refer to the provider-backed knowledge system
_Avoid_: using `KB` for this repository; use `kb-infra` when referring to Knowledge Bank Infrastructure

**Capture**: A user-invoked skill that drafts durable session knowledge into the KB through `/capture`, behind an HTML approval gate. It is not an accepted workflow.

**Lookup**: A read-only retrieval skill used by workflows to fetch live KB context, with an optional clarification branch for missing, stale, due, or ambiguous facts.

**Knowledge Harvest**: A scheduled observe-to-capture workflow that harvests signals from the user's activity and populates the KB. It runs one pattern — `observe(source) → generate candidates → rank/dedup → clarify → capture` — over many sources (KB-internal staleness, git history, agent transcripts), fanning out one subagent per source, then asks the user one clarification question at a time before drafting exact `/capture` writes for approval.
_Avoid_: Knowledge Bank Drift Realignment (renamed)

**Signal**: A candidate piece of durable knowledge worth remembering that Knowledge Harvest surfaces from a source — a fact, decision, stated opinion, recurring theme, project-state change, or working-style pattern. A signal is a candidate for approval, never an automatic KB write.

**Signal-preferences**: A KB endpoint holding the user's criteria for what is worth remembering — the emergent rubric Knowledge Harvest reads to rank candidates. It starts as a loose seed of registers plus a permanent open "surprising/uncategorised" bucket and grows only through approved rubric updates, rendered as a distinct block in the `/capture` draft.

**Social Draft Pulse**: A scheduled lookup-to-social-draft workflow that turns recent public-safe KB context into approved drafts in the social draft queue sink. It drafts a content mix of project/proof and topical posts, keeps per-platform continuity through the published social context surface, and grounds topical angles in the point-of-view surface. It drafts only; it does not post, schedule, branch, publish, or write to the KB.

**Portfolio Surface Sweep**: A scheduled lookup-to-portfolio-proposal workflow that compares public-safe KB context with the current portfolio sink, then prepares approved branch/PR work for portfolio candidates. It does not create social drafts, merge, deploy, publish, or write to the KB.

**Job Hunt Evaluate Audit**: A scheduled discovery-to-evaluation workflow in the career system sink. It drains existing queue work first, scans bounded new postings only when useful, generates reports and tracker rows, and stops before application or outreach work.

**Job Hunt Tune Audit**: A scheduled lookup-to-career-proposal workflow that compares KB job-search strategy context with the career system's personalization, then proposes approval-gated tuning changes.

**Job Hunt Advance Audit**: A scheduled tracker-to-next-pack workflow that consumes `Job Hunt Evaluate Audit` output and produces copy-pasteable application, outreach, follow-up, reply, interview, or negotiation packs. It does not submit, send, or mark real-world actions complete without the user's confirmation.

**Drift Audit**: A read-only convention check for Knowledge Bank structure, ownership, naming, role, and stale-state drift. It is the KB-internal-staleness source within Knowledge Harvest — a lower-level review pattern, not the whole automation.

**Follow-up Marker**: A short page-body line that tells a future lookup to ask the user about a deferred or time-ambiguous update.

**Approval Draft**: A reviewable proposal showing exact KB writes before anything is applied.

**Narrow Load**: Read only the Knowledge Bank Infrastructure docs or KB pages relevant to the current task.

**Role**: A hidden or low-visibility KB property used only when hierarchy is not enough. Valid values are `Canonical`, `Adapter`, `Raw`, and `Archive`.
