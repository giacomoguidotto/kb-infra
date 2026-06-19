# Knowledge Bank Infrastructure

## Glossary

**Knowledge Bank Infrastructure**: Giacomo's Notion Knowledge Gateway.
_Avoid_: second brain, source of truth

**kb-infra**: The repository and artifact slug for Knowledge Bank Infrastructure.
_Use for_: GitHub URLs, CLI identifiers, generated artifact names, and other machine-facing handles

**Notion Knowledge Gateway**: A local repo that makes Giacomo's canonical Notion workspace legible, auditable, and usable by agents.
_Avoid_: personal knowledge base, memory store

**Notion Source**: The canonical workspace for Giacomo's personal knowledge, tasks, projects, and portfolio facts.

**Workflow**: The casual umbrella name for an agent-enabled process described by an Automation Definition.
_Avoid_: automation run, background job

**Automation Definition**: A repo-owned description of an agent workflow's purpose, inputs, outputs, permissions, and validation rules.
_Avoid_: automation run, source of truth

**Automation Runtime**: The external system that executes an automation definition, such as Codex, a scheduled agent, or Notion automation.
_Avoid_: project-owned background process

**Clarification Request**: A question created when Notion state is incomplete, ambiguous, or unsafe to sync without Giacomo's answer.
_Avoid_: notification, reminder

**Narrow Load**: Read only the Knowledge Bank Infrastructure docs or generated artifacts relevant to the current task.

**Notion Snapshot**: A generated capture of selected Notion state, used for auditability and downstream tooling.

**Context Pack**: A generated, scoped bundle of Notion-derived context for an agent workflow.

**Export Safety**: The rule that generated artifacts must not expose more Notion content than their workflow needs.

**Distribution Artifact**: A generated output under `dist/`. It is never source of truth.

**ChatGPT Memory Digest**: A reviewable generated artifact for transferring routing-safe summaries into ChatGPT or Codex memory.
