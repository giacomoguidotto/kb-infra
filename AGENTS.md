# Agent Instructions

You are inside Knowledge Bank Infrastructure, the source-of-record for a
provider-backed agent operating system. The KB is the memory, the harness runtime
runs the automations, and this repo is the spec. The spec is provider-agnostic;
the concrete provider and runtime are bindings.

The KB (my Knowledge Bank) is the source of truth for personal knowledge, tasks,
projects, and portfolio facts. This repo never mirrors it. In agent conversations,
`KB` means the Knowledge Bank.

## First Run

If asked to set up, install, bootstrap, or wire up this infra, load
`skills/setup-kb-infra/SKILL.md` and follow it. It connects the KB provider, collects
bindings into gitignored `local/bindings.yml`, installs the skills, and bootstraps
the automations. Personal values are bindings and never get committed; see
[ADR 0002](docs/adr/0002-personal-specifics-are-bindings.md).

## Tool Belt

- `lookup` (`skills/lookup/`): read-only KB retrieval. Invoke as `/lookup`.
- `capture` (`skills/capture/`): approval-gated KB writes. Invoke as `/capture`.
- `setup-kb-infra` (`skills/setup-kb-infra/`): materialize the infra. Invoke as `/setup-kb-infra`.

When a skill is edited, re-run `setup-kb-infra`'s install step to re-copy it into the
harness skill directory, and commit the change in the workspace skills repo too.
The installed copies are materialized copies, not symlinks, so both repos must be
committed.

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
