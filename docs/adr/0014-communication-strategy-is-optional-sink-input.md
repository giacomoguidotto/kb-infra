# ADR 0014: Communication strategy is an optional sink input

## Status

Accepted

## Context

Generated job-application work needs one consistent personal communication
strategy across the Knowledge Bank, career tooling, network messages, and public
surfaces. Copying tone, charisma, persuasion, and channel rules into each prompt or
repository would create competing sources of truth.

At the same time, Knowledge Bank Infrastructure and a career-system sink are
independently progressing projects. A user must be able to run the career system
manually, without a KB provider or scheduled automation. Knowledge Bank
Infrastructure must reference the career system only through abstract sink roles
and capabilities, never through repository-specific state or commands.

## Decision

The KB owns one canonical `communication-strategy` endpoint. Other KB surfaces
link to it instead of duplicating settled guidance.

Knowledge Bank Infrastructure may resolve that endpoint and pass it as optional
personalization to a bound sink. It never copies the strategy prose into committed
automation prompts or makes the endpoint a prerequisite.

The career-system sink owns the generic communication planner, its lifecycle,
cadence, writers, and UI. It must provide complete research-backed defaults when no
personal strategy is supplied. User-layer voice material may keep unique examples
or explicit overrides, but should point to the canonical strategy for shared rules.

Job Pursue consumes two sink-native capabilities:

- `advance-workflow` for user-owned next-work planning and safe projection writes.
- `wait-review` for read-only review of externally owned waits and next-route
  recommendations.

Both capabilities retain the real-world approval boundary. Drafting and safe
agent-owned projection state are ungated. Sends, submissions, attempts, replies,
and other factual external events require user confirmation.

## Consequences

- Personal voice stays unanimous across surfaces without creating a repository
  mirror of the KB.
- Career-system quality improves for standalone users because generic planning is
  implemented in the sink rather than hidden in JHAA.
- A missing or unbound communication strategy degrades to generic defaults instead
  of blocking automation.
- kb-infra can change providers or sink implementations without learning their
  lifecycle vocabulary.
- Wait review can evolve with the sink's state model while the automation retains a
  small, stable capability contract.
- Setup gains one optional endpoint binding and one required capability binding for
  enabled Job Pursue materialization.
