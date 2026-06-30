# Knowledge Bank Infrastructure

## Glossary

**Knowledge Bank Infrastructure**: Giacomo's local infrastructure repo for making the Notion Knowledge Bank legible and usable by agents.
_Avoid_: second brain, source of truth

**kb-infra**: The repository and artifact slug for Knowledge Bank Infrastructure.
_Use for_: GitHub URLs, CLI identifiers, generated artifact names, and other machine-facing handles

**Notion Source**: The canonical workspace for Giacomo's personal knowledge, tasks, projects, and portfolio facts.

**Knowledge Bank**: The Notion-backed personal knowledge system. It is not duplicated into this repo.

**KB**: Conversational shorthand for the Notion Knowledge Bank.
_Use for_: agent conversations and user requests that refer to the Notion-backed knowledge system
_Avoid_: using `KB` for this repository; use `kb-infra` when referring to Knowledge Bank Infrastructure

**Remember**: A user-invoked skill that drafts durable session knowledge into Notion through `/remember`. It is not an accepted workflow.

**Recall**: A read-only retrieval skill used by workflows to fetch live Knowledge Bank context, with an optional clarification branch for missing, stale, due, raw, or ambiguous facts.

**Knowledge Bank Drift Realignment**: A scheduled recall-to-remember workflow that finds stale, missing, due, raw, ambiguous, or project-drift knowledge; asks Giacomo one clarification question at a time; then drafts exact `/remember` writes for approval.

**Social Draft Pulse**: A scheduled recall-to-social-draft workflow that turns recent public-safe KB context into approved Typefully drafts for work-facing X and LinkedIn posts. It drafts only; it does not post, schedule, branch, publish, or write to Notion.

**Portfolio Surface Sweep**: A scheduled recall-to-portfolio-proposal workflow that compares public-safe KB context with the current `guidotto.dev` portfolio, then prepares approved branch/PR work for portfolio candidates. It does not create social drafts, merge, deploy, publish, or write to Notion.

**Job Hunt Eval Pulse**: A scheduled `career-ops` discovery-to-evaluation workflow. It drains existing queue work first, scans bounded new postings only when useful, generates reports and tracker rows, and stops before application or outreach work.

**Job Hunt Tuning Audit**: A scheduled recall-to-career-ops-proposal workflow that compares KB job-search strategy context with `career-ops` personalization files, then proposes approval-gated tuning changes.

**Job Hunt Advancement Pulse**: A scheduled tracker-to-next-pack workflow that consumes `Job Hunt Eval Pulse` output, uses `/career-ops next` semantics, and produces copy-pasteable application, outreach, follow-up, reply, interview, or negotiation packs. It does not submit, send, or mark real-world actions complete without Giacomo's confirmation.

**Application Action State**: Optional `career-ops` user-layer state for current post-evaluation action readiness. It belongs in `data/application-actions.yml` when approved, separate from lifecycle status in `data/applications.md`.

**Drift Audit**: A read-only convention check for Knowledge Bank structure, ownership, naming, role, and stale-state drift. It is a lower-level review pattern, not the scheduled automation's whole shape.

**Follow-up Marker**: A short page-body line that tells a future recall to ask Giacomo about a deferred or time-ambiguous update.

**Approval Draft**: A reviewable proposal showing exact Notion writes before anything is applied.

**Narrow Load**: Read only the Knowledge Bank Infrastructure docs or Notion pages relevant to the current task.

**Distribution Artifact**: A generated output under `dist/`. It is never source of truth.

**Role**: A hidden or low-visibility Notion property used only when hierarchy is not enough. Valid values are `Canonical`, `Adapter`, `Raw`, and `Archive`.
