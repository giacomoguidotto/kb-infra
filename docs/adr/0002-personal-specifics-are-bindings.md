---
status: accepted
---

# Personal specifics are bindings, not spec

The spec stays generic; everything personal is a **binding** supplied at setup
and stored in gitignored `local/`, never committed. Three kinds of binding exist:
**sinks** (external systems an automation materializes into — a career system, a
portfolio repo, a social draft queue), **sink capabilities** (named operations
the bound sink implementation exposes, such as its advancement workflow or a
deterministic related-opportunity selector), and **KB endpoints** (the named
context surfaces and rule-sets an automation reads from the Knowledge Bank —
selected projects, public-safe claim source, portfolio change rules, social rules
of engagement, job-search strategy, personal constraints, and so on).

The `setup-kb-infra` skill collects sink bindings and, after connecting to the KB
provider, explores the KB to bind each endpoint to wherever it actually lives.
Automations reference sinks, capabilities, and endpoints **by role**, never by a
concrete page, command, path, or repo name. Setup resolves a capability to the
bound sink's executable command or native workflow instruction and injects that
resolution only into the materialized prompt.

## Considered options

- **Hardcode the personal values in the prompts.** Rejected: it couples the spec
  to one person, leaks private structure into version control, and makes the repo
  unforkable.
- **Prescribe a fixed KB structure everyone must adopt.** Rejected: every KB is
  shaped differently. The only thing an automation can legitimately require is the
  *endpoints* it consumes, not a page hierarchy.

## Consequences

- Personal rules currently baked into prompts (portfolio model, social strategy)
  move into the KB as endpoints; the generic prompt says "read your <endpoint>
  and apply it."
- `local/bindings.yml` (gitignored) is the single home for provider connection,
  sinks, sink capabilities, endpoint bindings, cadences, and clone paths.
- No committed file names a real page, repo, or absolute path. CI can enforce
  this as a personal-coupling check.
- `lookup` resolves endpoint context live by meaning, so most endpoints need no
  exact binding beyond a hint; only sinks and the provider connection are
  strictly required.
