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

![Knowledge Bank Infrastructure workflow map](assets/diagram.png)

## Active Workflows

- **Knowledge Bank drift realignment**: a scheduled Codex automation uses `/recall` in clarification mode to find stale, missing, due, raw, ambiguous, or project-drift knowledge; asks one question at a time; then hands the result to `/remember` for approval-gated writes.
- **Social Draft Pulse**: a scheduled Codex automation uses KB context to propose work-facing X and LinkedIn ideas, then creates approved Typefully drafts without posting or scheduling.
- **Portfolio Surface Sweep**: a scheduled Codex automation compares KB context with `guidotto.dev`, then prepares approved branch/PR work for portfolio candidates without publishing, merging, or writing to Notion.
- **Job Hunt Eval Pulse**: a scheduled Codex automation runs the `career-ops` discovery-to-evaluation loop and stops before application work.
- **Job Hunt Tuning Audit**: a scheduled Codex automation compares KB strategy context with `career-ops` personalization and proposes approval-gated tuning changes.
- **Job Hunt Advancement Pulse**: a scheduled Codex automation consumes evaluated opportunities and produces draft-oriented next packs without sending, submitting, or recording real-world completion.

Generative UI, richer curriculum surfaces, and future YouTube lanes are intentionally deferred expansion surfaces.

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
