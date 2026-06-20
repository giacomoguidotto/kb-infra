# Agent Instructions

You are inside Knowledge Bank Infrastructure, Giacomo's local infrastructure repo for his Notion knowledge system.

Notion is the source of truth for Giacomo's personal knowledge, tasks, projects, and portfolio facts. Knowledge Bank Infrastructure supports agents with workflow definitions, repo-owned skills, policy docs, and reviewable artifacts.

For Knowledge Bank database conventions, including the `life` database role model and drift-audit rules, consult [Knowledge Bank Conventions](docs/knowledge-bank-conventions.md). If the Notion project page is unclear, treat this repository as the formal documentation surface.

## Agent skills

- Issues and PRDs: GitHub Issues for `giacomoguidotto/kb-infra`; see [issue tracker](docs/agents/issue-tracker.md).
- Triage labels: use the default five-label vocabulary; see [triage labels](docs/agents/triage-labels.md).
- Domain docs: this is a single-context repo; use root `CONTEXT.md` and relevant ADRs; see [domain docs](docs/agents/domain.md).
