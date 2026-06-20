<p align="center">
  <!-- Logo slot: add assets/logo.png, assets/logo.svg, or light/dark logo variants here. -->
</p>

<h1 align="center">Knowledge Bank Infrastructure</h1>

<p align="center">
  <strong>Agent infrastructure for a Notion-first knowledge bank.</strong><br>
  <sub>Repo-owned conventions, skills, and reviewable artifacts for Giacomo's Notion workspace.</sub>
</p>

<p align="center">
  <a href="https://github.com/giacomoguidotto/kb-infra/actions"><img src="https://github.com/giacomoguidotto/kb-infra/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/giacomoguidotto/kb-infra/blob/main/LICENSE"><img src="https://img.shields.io/github/license/giacomoguidotto/kb-infra" alt="License"></a>
</p>

<br>

Knowledge Bank Infrastructure keeps agents pointed at the right source of truth. Notion owns the actual personal knowledge, tasks, projects, and portfolio facts; this repo holds the conventions and skills that make that workspace usable by Codex and other agents.

Generated files under `dist/` are reviewable outputs, not canonical records.

Use the full name, Knowledge Bank Infrastructure, in human-facing prose. Use the slug `kb-infra` for repository paths, URLs, generated artifact identifiers, and other machine-facing handles.

## Workflow Map

Knowledge Bank Infrastructure sits beside the canonical Notion workspace. It does not mirror or replicate Notion; it tells agents how to read, draft, and audit it.

```mermaid
flowchart LR
    notion(("Notion<br/>source of truth"))
    kbInfra["Knowledge Bank Infrastructure<br/>conventions, skills,<br/>reviewable artifacts"]
    codex["Codex agents<br/>manual capture,<br/>live lookup,<br/>drift audit"]
    approval{"Giacomo<br/>approval"}
    report["Drift report<br/>proposed fixes"]

    kbInfra -- "formal rules" --> codex
    codex -- "narrow live reads" --> notion
    codex -- "approval drafts" --> approval
    approval -- "approved writes" --> notion
    codex -- "read-only audit" --> report
    report -- "human-reviewed changes" --> approval

    classDef source fill:#fff7cc,stroke:#d39e00,stroke-width:2px,color:#1f2937;
    classDef gateway fill:#ddf7ef,stroke:#159570,stroke-width:2px,color:#12372f;
    classDef runtime fill:#e8edff,stroke:#5267d8,stroke-width:2px,color:#172554;
    classDef artifact fill:#f3e8ff,stroke:#8b5cf6,stroke-width:2px,color:#3b0764;
    classDef decision fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#0f172a;

    class notion source;
    class kbInfra gateway;
    class codex runtime;
    class report artifact;
    class approval decision;
```

## What's Inside

- `AGENTS.md`: entry point for agents working in this repo.
- `CONTEXT.md`: vocabulary for the current operating model.
- `docs/workflows.md`: accepted live workflows.
- `docs/knowledge-bank-conventions.md`: formal conventions for the Notion `life` database and drift audits.
- `docs/agents/`: navigation and issue-tracker guidance for agents.
- `skills/`: repo-owned agent workflows.
- `dist/`: generated review artifacts.

## Principles

- Notion is canonical.
- This repo documents conventions; it does not duplicate the Knowledge Bank.
- Agents should use narrow live Notion lookup when task context requires it.
- Notion writes require explicit approval of the exact draft.
- Drift audits are read-only and propose fixes for human approval.
- Codex memory should keep routing facts and preferences, not Notion content.

## Contributing

Free and open source under the [MIT License](LICENSE). See [CONTRIBUTING.md](.github/CONTRIBUTING.md) to get involved.

Agents should start at [AGENTS.md](AGENTS.md).
