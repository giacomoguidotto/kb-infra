# Automation Preamble

Every automation shares this preamble. When `setup-kb-infra` materializes an automation,
it prepends this preamble to the automation body and resolves the placeholders
from `local/bindings.yml`. Keep the shared rules here in one place; do not restate
them inside individual automation prompts.

## KB Interface

The spec does not prescribe a KB structure. Each automation declares the
**endpoints** it reads; `setup-kb-infra` discovers where each lives in your KB and binds
it. Reference endpoints and sinks **by role**, never by a concrete page, repo, or
path. `lookup` resolves endpoint context live by meaning, so a binding is a hint,
not a hard dependency.

## Endpoints

Data surfaces the automations read:

- `selected-projects`: the active/selected projects to consider this run.
- `public-safe-claim-source`: the adapter that presents recruiter/public-facing
  facts. It also owns the **public-safety boundary** — what must not be published.
- `proof-points`: compact, reusable evidence and metrics for generated artifacts.
- `network`: contacts and relationships.
- `identity`: how the user frames themselves; archetypes and narrative.
- `point-of-view`: the user's incrementally-built public persona — recorded
  stances, opinions, and recurring themes that topical drafts draw from. It grows
  over time only through approved `/capture` writes; automations read it and never
  fabricate a stance.
- `published-social-context`: a per-platform ledger of what has already been
  published and which concepts and projects have been publicly introduced on each
  channel. Automations read it to keep continuity and avoid assuming audience
  knowledge; it is maintained through approved `/capture` writes, not written by
  draft automations.

Rule-sets the automations obey (owned by the KB, not the spec):

- `portfolio-change-rules`: the portfolio model and structural constraints.
- `social-rules-of-engagement`: per-platform drafting strategy and guardrails,
  including the per-run volume target, the project/topical content mix, and the
  self-contained / introduce-on-first-use rule.
- `job-search-strategy`: target roles, compensation baseline, scoring preferences.
- `personal-constraints`: relocation, compensation, work authorization,
  references, availability, and side-project/IP freedom.

## Sinks

External systems an automation materializes into. Each resolves from a binding:

- `<career-system>`: the external job-search system repository.
- `<portfolio>`: the public portfolio repository.
- `<social-draft-queue>`: the social draft tool.

## Shared Rules

- The KB is canonical. Never write to it except through `/capture` approval.
- Use `/lookup` narrowly; do not preload broad KB content.
- Keep public claims source-backed and public-safe. Do not turn vibes into facts.
- Do not duplicate KB knowledge into repo files or local state.
- The KB is the knowledge ledger; each sink is its own work queue.
- Return a summary first and wait for approval before materializing any write into
  a sink.

## State Model

- If state is useful, use ignored `local/` scratch only for mechanical hints such
  as last run time, refresh dates, or commit cursors.
- Never store copied KB facts, answered questions, approved/rejected ideas, or
  suppression decisions in local state.
- Deleting local state may make the next run slower; it must not make it less
  correct.

## Follow-up Marker Policy (default)

Automations that revisit deferred knowledge use the follow-up and final-form
marker formats in [knowledge-bank-conventions.md](../knowledge-bank-conventions.md).
This ships as the repo default; `setup-kb-infra` offers to override it as a binding.
