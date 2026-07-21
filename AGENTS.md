# Agent Instructions

You are inside Knowledge System, the source-of-record for governed agent access to
a provider-backed Knowledge Bank. The KB is the memory, the harness runtime runs
KB Reconcile, and this repo is the spec. The spec is provider-agnostic; the
concrete provider and runtime are bindings.

The KB (my Knowledge Bank) is the source of truth for personal knowledge, tasks,
projects, and portfolio facts. This repo never mirrors it. In agent conversations,
`KB` means the Knowledge Bank.

## First Run

If asked to set up, install, bootstrap, or reconcile this System, load
`skills/public/setup-knowledge-system/SKILL.md` and follow it. It preserves and
validates gitignored `local/bindings.yml`, installs the shared interface, and
materializes only KB Reconcile. Personal values are bindings and never get committed; see
[ADR 0002](docs/adr/0002-personal-specifics-are-bindings.md).

## Tool Belt

- `lookup` (`skills/public/lookup/`): read-only KB retrieval. Invoke as `/lookup`.
- `capture` (`skills/public/capture/`): approval-gated KB writes. Invoke as `/capture`.
- `setup-knowledge-system` (`skills/public/setup-knowledge-system/`): check or reconcile the standalone System. Invoke as `/setup-knowledge-system check|reconcile`.
- Knowledge elicitation helpers live under `skills/internal/` and require explicit
  repo-native installation.

Public skills are canonical here and exported from `skills/public/`; internal skills
are canonical under `skills/internal/` and are excluded from normal distribution.
Installed copies are materializations, never sources.

## Repo Docs

- Vocabulary: root `CONTEXT.md`.
- Decisions: `docs/adr/` (single-context repo; prefer an ADR over an ad-hoc doc).
- Workflows and automations: `docs/workflows.md`, `docs/automations/`.
- KB conventions: `docs/knowledge-bank-conventions.md`.

## Commits and Versioning

The spec is versioned by git tags (`vX.Y.Z`). Pushing to `main` runs
`scripts/bump-version.sh`, which derives the next version from the conventional-commit
types since the last tag: `fix:` → patch, `feat:` → minor, a `!` marker or
`BREAKING CHANGE` → major. Every commit therefore chooses a release.

Before committing, if I have not stated the intended release type, ask for explicit
approval of which one the commit should trigger — patch, minor, major, or none (a
non-releasing type such as `docs`, `chore`, `refactor`, `ci`, or `test`) — and use
the matching commit type. Do not assume the release type.

## Agent Skills

- Issues and PRDs: this repository's GitHub Issues; see
  [issue tracker](docs/agents/issue-tracker.md).
- Triage labels: use the default five-label vocabulary; see
  [triage labels](docs/agents/triage-labels.md).
- Domain docs: this is a single-context repo; use root `CONTEXT.md` and relevant
  ADRs; see [domain docs](docs/agents/domain.md).
