<p align="center">
  <!-- Logo slot: add assets/logo.png, assets/logo.svg, or light/dark logo variants here. -->
</p>

<h1 align="center">Knowledge Bank Infrastructure</h1>

<p align="center">
  <strong>Agent infrastructure for a Notion-first knowledge bank.</strong><br>
  <sub>Workflows, skills, policies, and reviewable artifacts for Giacomo's Notion workspace.</sub>
</p>

<p align="center">
  <a href="https://github.com/giacomoguidotto/kb-infra/actions"><img src="https://github.com/giacomoguidotto/kb-infra/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/giacomoguidotto/kb-infra/blob/main/LICENSE"><img src="https://img.shields.io/github/license/giacomoguidotto/kb-infra" alt="License"></a>
</p>

<br>

Knowledge Bank Infrastructure keeps agents pointed at the right source of truth. Notion owns the actual personal knowledge, tasks, projects, and portfolio facts; this repo keeps the supporting workflows and artifacts that make that workspace usable by Codex, ChatGPT, and other agents.

Generated files under `dist/` are reviewable outputs, not canonical records.

Use the full name, Knowledge Bank Infrastructure, in human-facing prose. Use the slug `kb-infra` for repository paths, URLs, generated artifact identifiers, and other machine-facing handles.

## Workflow Map

Knowledge Bank Infrastructure sits between the canonical Notion workspace and the agents that need safe, scoped context from it.

```mermaid
flowchart LR
    notion(("Notion<br/>source of truth"))
    kbInfra["Knowledge Bank Infrastructure<br/>workflows, skills,<br/>policies, artifacts"]
    codex["Codex runs<br/>capture, sync,<br/>govern"]
    codexMemory[("Codex Memory<br/>small routing facts")]
    chatgpt["chatgpt.com<br/>ChatGPT Memory Digest"]
    portfolio["Portfolio<br/>public Notion-backed facts"]
    approval{"Giacomo<br/>approval"}
    clarify{"Clarification<br/>request"}

    notion -- "live reads" --> codex
    codex -- "draft updates" --> approval
    approval -- "approved writes" --> notion

    notion -- "diffs and selected facts" --> kbInfra
    kbInfra -- "rules and safe exports" --> codex
    codex -- "validated patches and PRs" --> kbInfra

    kbInfra -- "routing-safe digest" --> codexMemory
    codexMemory -- "pointers and preferences" --> codex

    kbInfra -- "reviewable digest" --> chatgpt
    chatgpt -. "keeps pointing back to canonical facts" .-> notion

    notion -- "profile, project, career facts" --> portfolio
    kbInfra -. "export-safe data or generated UI" .-> portfolio
    portfolio -. "missing or stale claims" .-> clarify
    kbInfra -. "ambiguous state" .-> clarify
    clarify -- "answers land in Notion" --> notion

    classDef source fill:#fff7cc,stroke:#d39e00,stroke-width:2px,color:#1f2937;
    classDef gateway fill:#ddf7ef,stroke:#159570,stroke-width:2px,color:#12372f;
    classDef runtime fill:#e8edff,stroke:#5267d8,stroke-width:2px,color:#172554;
    classDef memory fill:#f3e8ff,stroke:#8b5cf6,stroke-width:2px,color:#3b0764;
    classDef product fill:#ffe7e2,stroke:#e66b5b,stroke-width:2px,color:#431407;
    classDef decision fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#0f172a;

    class notion source;
    class kbInfra gateway;
    class codex runtime;
    class codexMemory,chatgpt memory;
    class portfolio product;
    class approval,clarify decision;
```

## What's Inside

- `skills/`: repo-owned agent workflows.
- `docs/workflows.md`: the accepted workflow map.
- `docs/agents/`: navigation and issue-tracker guidance for agents.
- `docs/adr/`: durable policy decisions.
- `dist/`: generated snapshots, reports, digests, and context packs.

## Principles

- Notion is canonical.
- Knowledge Bank Infrastructure defines workflows; external runtimes execute them.
- Agents narrow-load only the docs or artifacts needed for the task.
- Codex memory should keep routing facts and preferences, not Notion content.
- Public artifacts must not include private Notion material without explicit approval.

## Contributing

Free and open source under the [MIT License](LICENSE). See [CONTRIBUTING.md](.github/CONTRIBUTING.md) to get involved.

Agents should start at [AGENTS.md](AGENTS.md).
