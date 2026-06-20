# Knowledge Bank Infrastructure

## Glossary

**Knowledge Bank Infrastructure**: Giacomo's local infrastructure repo for making the Notion Knowledge Bank legible and usable by agents.
_Avoid_: second brain, source of truth

**kb-infra**: The repository and artifact slug for Knowledge Bank Infrastructure.
_Use for_: GitHub URLs, CLI identifiers, generated artifact names, and other machine-facing handles

**Notion Source**: The canonical workspace for Giacomo's personal knowledge, tasks, projects, and portfolio facts.

**Knowledge Bank**: The Notion-backed personal knowledge system. It is not duplicated into this repo.

**Manual Capture**: A user-invoked workflow that drafts durable session knowledge into Notion through `dump-knowledge`.

**Live Lookup**: A narrow, task-scoped read from Notion. This is the normal way agents refresh context.

**Drift Audit**: A read-only check for Knowledge Bank structure, ownership, naming, role, and stale-state drift. The scheduled Codex automation uses this pattern.

**Approval Draft**: A reviewable proposal showing exact Notion writes before anything is applied.

**Narrow Load**: Read only the Knowledge Bank Infrastructure docs or Notion pages relevant to the current task.

**Distribution Artifact**: A generated output under `dist/`. It is never source of truth.

**Role**: A hidden or low-visibility Notion property used only when hierarchy is not enough. Valid values are `Canonical`, `Adapter`, `Raw`, and `Archive`.
