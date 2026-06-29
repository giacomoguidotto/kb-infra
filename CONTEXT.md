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

**Manual Capture**: A user-invoked workflow that drafts durable session knowledge into Notion through `remember`.

**Recall**: A read-only retrieval workflow that fetches live Knowledge Bank context for other workflows, with an optional clarification branch for missing, stale, due, raw, or ambiguous facts.

**Drift Audit**: A read-only check for Knowledge Bank structure, ownership, naming, role, and stale-state drift. The scheduled Codex automation uses this pattern.

**Follow-up Marker**: A short page-body line that tells a future recall to ask Giacomo about a deferred or time-ambiguous update.

**Approval Draft**: A reviewable proposal showing exact Notion writes before anything is applied.

**Narrow Load**: Read only the Knowledge Bank Infrastructure docs or Notion pages relevant to the current task.

**Distribution Artifact**: A generated output under `dist/`. It is never source of truth.

**Role**: A hidden or low-visibility Notion property used only when hierarchy is not enough. Valid values are `Canonical`, `Adapter`, `Raw`, and `Archive`.
