# Skill and automation ownership under Option B

Updated: 2026-07-16

## Conclusion

The current workspace is an installation surface, not a safe canonical owner.
It contains 57 tracked skill directories, of which 50 are upstream-owned installs,
three are materialized copies from Knowledge Bank Infrastructure, and four are
first-party skills authored only in the workspace. The drift risk comes from
committing all four categories under the same path.

Under Option B:

- `agentic-os` should own first-party cross-system behavior and first-party
  compositions of multiple systems;
- `knowledge-system` should own Knowledge System skills and its own automation;
- `mastery-system` should own Mastery-specific behavior, although it currently has
  no skill or scheduled agent-automation source;
- `career-ops` remains an upstream-owned external dependency and contributes
  nothing to the generated first-party skills bundle;
- `giacomoguidotto/skills` remains a CI-only verbatim projection of
  `skills/public/` from first-party repositories;
- upstream skills remain installed from their upstream repositories and are never
  copied into `agentic-os`, a subsystem, or the first-party distribution bundle.

`public` and `internal` are export dispositions, not secrecy labels. CI scans only
`skills/public/`; committed `skills/internal/` remains excluded. Automation source
can use the same public/internal distinction, but it is not copied into the skills
distribution bundle.

## Scope and evidence

This inventory covers committed agent skills and scheduled agent-automation source
in these current checkouts:

- Knowledge Bank Infrastructure:
  `/Users/giacomo/dev/life/kb-infra`
- workspace:
  `/Users/giacomo/dev/life/workspace`
- Personal Mastery Program:
  `/Users/giacomo/dev/uni/personal-mastery-program`
- Career Ops:
  `/Users/giacomo/dev/life/career-ops`

Repository CI workflows under `.github/workflows/` are not counted as Agentic OS
automations. They remain repository-owned CI or maintenance behavior.

The strongest provenance evidence is the local Skills CLI lock at
`/Users/giacomo/.local/state/skills/.skill-lock.json`. It records the source
repository and source path for 49 of the 50 upstream-owned skills currently present
in the workspace. The remaining upstream artifact, `frontend-design`, matches the
installed official Claude plugin family at
`/Users/giacomo/.claude/plugins/cache/claude-plugins-official/frontend-design/`.

The workspace itself declares that its automation directory is the canonical
source for personal non-KB automations in
`/Users/giacomo/dev/life/workspace/cfg/home/agents/automations/README.md`.
Knowledge Bank Infrastructure declares its canonical skills and materialized-copy
behavior in `/Users/giacomo/dev/life/kb-infra/AGENTS.md`, and maps its five current
scheduled automations in
`/Users/giacomo/dev/life/kb-infra/docs/workflows.md`.

## First-party skill disposition

| Current skill | Category | Canonical owner | Disposition | Evidence and rationale |
| --- | --- | --- | --- | --- |
| `domain-reconnaissance` | First-party cross-system | `agentic-os` | `skills/public/` | The skill is domain-agnostic decision support and hands control back to any caller. Its complete current source is `/Users/giacomo/dev/life/workspace/cfg/home/agents/skills/domain-reconnaissance/SKILL.md`. PMP consumes it but does not own it, as shown by `/Users/giacomo/dev/uni/personal-mastery-program/AGENTS.md`. |
| `setup-project` | First-party wrapper and cross-system composition | `agentic-os` | `skills/internal/` initially | It explicitly composes upstream `setup-matt-pocock-skills`, live KB conventions, and an optional PMP Project Lab branch. It also names Giacomo and concrete current systems, so it is not yet a provider-agnostic public skill. See `/Users/giacomo/dev/life/workspace/cfg/home/agents/skills/setup-project/SKILL.md`. |
| `get-knowledge` | Knowledge-specific convenience wrapper | `knowledge-system` | `skills/internal/` | It hardcodes Giacomo and Notion, while largely specializing the read-only `lookup` contract. Keep it out of the public bundle unless it is rewritten against generic Knowledge System bindings. See `/Users/giacomo/dev/life/workspace/cfg/home/agents/skills/get-knowledge/SKILL.md`. |
| `grill-knowledge` | First-party wrapper | `knowledge-system` | `skills/internal/` | It composes grilling with an approval-gated Notion write draft and hardcodes Giacomo and Notion. It belongs with Knowledge System capture semantics, but is not currently provider-agnostic. See `/Users/giacomo/dev/life/workspace/cfg/home/agents/skills/grill-knowledge/SKILL.md`. |
| `lookup` | Subsystem-specific | `knowledge-system` | `skills/public/` | The canonical provider-agnostic source is `/Users/giacomo/dev/life/kb-infra/skills/lookup/SKILL.md`; the workspace copy at `/Users/giacomo/dev/life/workspace/cfg/home/agents/skills/lookup/SKILL.md` is a materialization. |
| `capture` | Subsystem-specific | `knowledge-system` | `skills/public/` | The canonical approval-gated, provider-agnostic source is `/Users/giacomo/dev/life/kb-infra/skills/capture/SKILL.md`; the workspace copy is a materialization. |
| `setup-kb-infra` | Subsystem-specific setup | `knowledge-system` | Rename to `setup-knowledge-system`, then `skills/public/` | Its source is `/Users/giacomo/dev/life/kb-infra/skills/setup-kb-infra/SKILL.md`. The committed workspace copy is a materialization. The locked system name and setup convention require the new slug. |

The three Knowledge System materializations under
`/Users/giacomo/dev/life/workspace/cfg/home/agents/skills/` should stop being
committed once installation is sourced from first-party releases and the generated
distribution bundle. Until that migration, edits must still begin in their
canonical Knowledge System paths.

## Upstream-owned workspace skills

These remain upstream dependencies. Their canonical owner and update history are
recorded in `/Users/giacomo/.local/state/skills/.skill-lock.json`; they should not
appear under any first-party `skills/public/` or `skills/internal/` tree.

### `mattpocock/skills`

`ask-matt`, `caveman`, `claude-handoff`, `code-review`, `codebase-design`,
`decision-mapping`, `design-an-interface`, `diagnose`, `diagnosing-bugs`,
`domain-model`, `domain-modeling`, `edit-article`, `git-guardrails-claude-code`,
`grill-me`, `grill-with-docs`, `grilling`, `handoff`, `implement`,
`improve-codebase-architecture`, `loop-me`, `migrate-to-shoehorn`,
`obsidian-vault`, `prototype`, `qa`, `request-refactor-plan`, `research`,
`resolving-merge-conflicts`, `review`, `scaffold-exercises`,
`setup-matt-pocock-skills`, `setup-pre-commit`, `setup-ts-deep-modules`, `tdd`,
`teach`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`,
`ubiquitous-language`, `wayfinder`, `wizard`, `write-a-skill`, `writing-beats`,
`writing-fragments`, `writing-great-skills`, `writing-shape`, and `zoom-out`.

Several are deprecated, in-progress, aliases, or overlapping generations in the
upstream lock, for example `review` and `code-review`, `diagnose` and
`diagnosing-bugs`, and `domain-model` and `domain-modeling`. That is an installation
hygiene issue, not a reason to fork or republish them.

### Other upstream owners

- `find-skills`: `vercel-labs/skills`, recorded in
  `/Users/giacomo/.local/state/skills/.skill-lock.json`.
- `typefully`: `typefully/agent-skills`, recorded in the same lock and declared in
  `/Users/giacomo/dev/life/workspace/cfg/home/agents/skills/typefully/SKILL.md`.
- `frontend-design`: official Claude plugin dependency, with installed upstream
  evidence under
  `/Users/giacomo/.claude/plugins/cache/claude-plugins-official/frontend-design/`.

## Automation disposition

| Current automation | Category | Canonical owner | Disposition | Evidence and rationale |
| --- | --- | --- | --- | --- |
| Repo PR CI Repair Sweep | First-party cross-system | `agentic-os` | `automations/internal/` | It operates across the repository fleet, not around the KB. Its current source also hardcodes Giacomo, local paths, timezone, model, and runtime identifiers, so it is not a reusable public definition yet. See `/Users/giacomo/dev/life/workspace/cfg/home/agents/automations/repo-pr-ci-repair-sweep/automation.toml` and `prompt.md`. |
| KB Reconcile | Subsystem-specific | `knowledge-system` | Public subsystem automation source | It reconciles activity into canonical KB state through `lookup` and approval-gated `capture`. See `/Users/giacomo/dev/life/kb-infra/docs/automations/kb-reconcile.md`. |
| Portfolio Refresh | First-party cross-system | `agentic-os` | Public automation source | It coordinates Knowledge System context with a separate portfolio sink and deliberately owns no KB knowledge. See `/Users/giacomo/dev/life/kb-infra/docs/automations/portfolio-refresh.md`. |
| Social Compose | First-party cross-system | `agentic-os` | Public automation source | It coordinates Knowledge System endpoints, a social publishing source, calendar availability, public research, and a social draft sink. See `/Users/giacomo/dev/life/kb-infra/docs/automations/social-compose.md`. |
| Job Scout | First-party Career System integration | `agentic-os` | Public Career System integration source | It coordinates one-way KB-owned strategy with the external Career Ops implementation. Agentic OS owns this integration because Career Ops is upstream-derived. See `/Users/giacomo/dev/life/kb-infra/docs/automations/job-scout.md`. |
| Job Pursue | First-party Career System integration | `agentic-os` | Public Career System integration source | It consumes Job Scout output and invokes Career Ops capabilities while preserving real-world approval gates. See `/Users/giacomo/dev/life/kb-infra/docs/automations/job-pursue.md`. |

The shared file
`/Users/giacomo/dev/life/kb-infra/docs/automations/_preamble.md` currently couples
all five definitions to Knowledge System lookup, capture, and mandate vocabulary.
It is support material, not a sixth automation. Before moving the four cross-system
definitions, the migration must establish one stable Knowledge System interface for
those rules rather than copying the preamble into two canonical owners.

## Mastery System and Career Ops

The current Personal Mastery Program repository has no committed `SKILL.md` and no
scheduled agent-automation source. It consumes cross-system skills through its
instructions, particularly `domain-reconnaissance`, and has only repository CI at
`/Users/giacomo/dev/uni/personal-mastery-program/.github/workflows/ci.yml`.
The future `setup-mastery-system` validation skill is therefore new work, not a
migration of a current artifact.

Career Ops has one upstream-owned `career-ops` router projected into seven harness
directories, beginning with
`/Users/giacomo/dev/life/career-ops/.agents/skills/career-ops/SKILL.md`. Six copies
are byte-identical in the current checkout; the Kimi projection differs. The repo's
`origin` is Giacomo's fork and `upstream` is `santifer/career-ops`, while the live
checkout also contains unrelated dirty work. These facts reinforce the locked
boundary: treat the router and Career Ops workflows as upstream-owned external
behavior, publish none of them through `giacomoguidotto/skills`, and keep
first-party integration policy such as `setup-career-system` in `agentic-os`.

## Migration order implied by the inventory

1. Create canonical `skills/public/` and `skills/internal/` trees in the owning
   first-party repositories.
2. Move the four workspace-authored first-party skills to their owners without
   touching upstream installations.
3. Rename and move the three canonical Knowledge System skills, then stop tracking
   their workspace materializations.
4. Move cross-system automation source to `agentic-os`; retain KB Reconcile in
   `knowledge-system`; resolve the shared preamble seam once during that move.
5. Configure Distribution Bundle CI to copy only first-party `skills/public/`
   directories verbatim from immutable releases.
6. Leave local upgrades explicit through `bunx skills@latest add
   giacomoguidotto/skills -y -g` or an agent-invoked equivalent.

## Confidence and limits

Confidence is high for current ownership and provenance because the inventory uses
tracked repository files, the Skills CLI lock, repository instructions, and current
Git remotes. Confidence is medium for the exact future public/internal disposition
of the two personalized Knowledge wrappers and `setup-project`; their current
content clearly excludes them from public export, but later refactoring may make a
provider-agnostic public form worthwhile.

This note does not decide publication CI mechanics, setup registry schema, or the
exact migration commits. It classifies current artifacts only.
