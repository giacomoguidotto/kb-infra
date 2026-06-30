<p align="center">
  <!-- Logo slot: add assets/logo.png, assets/logo.svg, or light/dark logo variants here. -->
</p>

<h1 align="center">Knowledge Bank Infrastructure</h1>

<p align="center">
  <strong>Operational rails for a Notion-first personal knowledge system.</strong><br>
  <sub>Conventions, agent skills, and reviewable drafts for keeping human-owned knowledge usable by AI agents.</sub>
</p>

<p align="center">
  <a href="https://github.com/giacomoguidotto/kb-infra/actions"><img src="https://github.com/giacomoguidotto/kb-infra/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/giacomoguidotto/kb-infra/blob/main/LICENSE"><img src="https://img.shields.io/github/license/giacomoguidotto/kb-infra" alt="License"></a>
</p>

<br>

AI agents are useful only when they can find the right context without turning the context itself into another stale copy. Knowledge Bank Infrastructure is the repo that keeps that boundary sharp.

Notion owns the actual knowledge: tasks, projects, profile facts, finance notes, learning notes, and portfolio material. This repo owns the operating rules around that knowledge: how agents should read it, how they should draft updates, and how they should realign stale or missing knowledge without writing over the source of truth.

## Core Idea

Keep the knowledge where the human works. Put the agent protocol in Git.

That gives the system three useful properties:

- **Live context**: agents read Notion directly when a task needs personal or project context.
- **Reviewable writes**: agents draft Notion updates and wait for explicit approval before applying them.
- **Auditable structure**: database conventions live in versioned Markdown, so drift can be detected and discussed like code.

## Operating Loop

```mermaid
flowchart LR
    repo["kb-infra<br/>conventions + skills"]
    notion(("Notion<br/>source of truth"))
    agent["Agent<br/>recall + drafts"]
    draft["HTML draft<br/>exact proposed writes"]
    realign["Drift realignment<br/>questions + candidates"]
    approval{"Giacomo<br/>approval"}

    repo -- "protocol" --> agent
    agent -- "narrow reads" --> notion
    agent -- "manual capture" --> draft
    agent -- "scheduled clarification" --> realign
    realign -- "answered updates" --> draft
    draft --> approval
    approval -- "approved writes" --> notion

    classDef source fill:#fff7cc,stroke:#d39e00,stroke-width:2px,color:#1f2937;
    classDef protocol fill:#ddf7ef,stroke:#159570,stroke-width:2px,color:#12372f;
    classDef runtime fill:#e8edff,stroke:#5267d8,stroke-width:2px,color:#172554;
    classDef artifact fill:#f3e8ff,stroke:#8b5cf6,stroke-width:2px,color:#3b0764;
    classDef decision fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#0f172a;

    class notion source;
    class repo protocol;
    class agent runtime;
    class draft,realign artifact;
    class approval decision;
```

## Active Workflows

- **Manual capture**: `/remember` turns a conversation or agent session into an approval draft for Notion.
- **Knowledge Bank drift realignment**: a scheduled Codex automation uses `/recall` in clarification mode to find stale, missing, due, raw, ambiguous, or project-drift knowledge; asks one question at a time; then hands the result to `/remember` for approval-gated writes.

Portfolio generation is intentionally not part of the accepted workflow yet. It will get its own architecture when the shape is clearer.

## Repository Map

- `AGENTS.md`: local instructions for agents working in this repo.
- `CONTEXT.md`: vocabulary for the current operating model.
- `docs/workflows.md`: accepted workflows and non-workflows.
- `docs/knowledge-bank-conventions.md`: formal rules for the Notion `life` database.
- `docs/automations/`: draft prompts for scheduled Codex automations.
- `skills/`: repo-owned agent workflows.
- `dist/`: generated review artifacts, never canonical knowledge.

## Guarantees

- Notion stays canonical.
- This repo does not mirror the Knowledge Bank.
- Agents use live Notion lookup instead of local replicas.
- Notion writes require approval of the exact draft.
- Recall and drift realignment discovery are read-only.
- Agent memory stores routing policy, not copied Notion facts.

## Contributing

Free and open source under the [MIT License](LICENSE). See [CONTRIBUTING.md](.github/CONTRIBUTING.md) to get involved.

Agents should start at [AGENTS.md](AGENTS.md).
