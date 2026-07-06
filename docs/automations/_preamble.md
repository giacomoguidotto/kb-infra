# Automation Preamble

This file is the composer's reference material, **not** a block that is pasted
verbatim into a prompt. When `setup-kb-infra` materializes an automation it composes a
lean, self-contained prompt: it injects the [Operating Rules](#operating-rules), and
for each surface the automation **declares** it emits a single resolved line —
the role description from the [vocabulary](#vocabulary) joined with the binding hint
from `local/bindings.yml`. The full catalog, the provider block, cadence, and blank
overrides never reach the prompt. See
[ADR 0005](../adr/0005-materialized-automation-is-self-contained.md).

Reference surfaces and sinks **by role**, never by a concrete page, repo, or path.
`/lookup` resolves an endpoint live by meaning, so a binding is a location hint, not a
hard dependency. Keep the shared rules here in one place; do not restate them inside
individual automation prompts.

## Operating Rules

Injected into every composed prompt:

- The KB is canonical; never write to it except through `/capture` approval.
- Return a run summary and wait for approval before materializing any write into a
  sink.
- Use `/lookup` narrowly; do not preload broad KB content.
- Keep public claims source-backed and public-safe; do not turn vibes into facts.
- Do not duplicate KB knowledge into repo files or local state; the KB is the
  knowledge ledger and each sink is its own work queue.
- Local state is disposable: use gitignored `local/` only for mechanical hints (last
  run time, refresh dates, commit cursors), never copied KB facts, answered
  questions, or approved/rejected/suppression decisions. Deleting it may make the
  next run slower, never less correct.

## Vocabulary

The composer emits one resolved line per **declared** surface, drawn from the
descriptions below. It does not inject surfaces an automation does not declare.

### Endpoints

Data surfaces and rule-sets automations read from the KB:

- `selected-projects`: the active/selected projects to consider this run.
- `public-safe-claim-source`: the adapter presenting recruiter/public-facing facts;
  also owns the public-safety boundary — what must not be published.
- `proof-points`: compact, reusable evidence and metrics for generated artifacts.
- `network`: contacts and relationships.
- `identity`: how the user frames themselves; archetypes and narrative.
- `point-of-view`: the user's recorded public stances, opinions, and recurring themes;
  grows only through approved `/capture` writes — automations read it and never
  fabricate a stance.
- `published-social-context`: the per-platform ledger of what has been published and
  which concepts and projects were publicly introduced on each channel; maintained
  through approved `/capture` writes, read for continuity.
- `portfolio-change-rules`: the portfolio model and structural constraints.
- `social-rules-of-engagement`: per-platform drafting strategy and guardrails — the
  per-run volume target, the project/topical content mix, and the self-contained /
  introduce-on-first-use rule.
- `job-search-strategy`: target roles, compensation baseline, scoring preferences.
- `personal-constraints`: relocation, compensation, work authorization, references,
  availability, and side-project/IP freedom.
- `signal-preferences`: the user's criteria for what is worth remembering — the
  emergent rubric Knowledge Harvest ranks candidates against; grows only through
  approved rubric updates.

### Sinks

External systems an automation materializes into; each resolves from a binding to a
clone path (or tool handle). The primary sink clone is the run's working directory.

- `<career-system>`: the external job-search system repository.
- `<portfolio>`: the public portfolio repository.
- `<social-draft-queue>`: the social draft tool.

### Sources

External systems an automation observes (reads, never writes); each resolves from a
binding, referenced by role:

- `<transcript-source>`: agent conversation transcripts on the local machine that
  Knowledge Harvest mines for signals. Read-only, forward-only by cursor, and private
  by default — derived signals never auto-flow to public-safe or social surfaces.

## Follow-up Marker Policy

Automations that declare a dependency on deferred-knowledge markers (Knowledge
Harvest) use the follow-up and final-form marker formats in
[knowledge-bank-conventions.md](../knowledge-bank-conventions.md). Those formats are
**inlined** into the composed prompt at materialize time, not left as a file path for
the run to open. This ships as the repo default; `setup-kb-infra` offers to override it
as a binding.
