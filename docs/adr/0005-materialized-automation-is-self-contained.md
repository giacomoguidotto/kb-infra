---
status: accepted
---

# A materialized automation runs in the sink checkout and must be self-contained

> **Superseded in part** by
> [ADR 0011](0011-social-scheduling-uses-capability-bound-live-sources.md): declared
> source capabilities follow the same resolved-line composition rule, and an
> automation may explicitly require its human-readable coverage cadence in the
> prompt when the next run defines its responsibility window. Undeclared cadence and
> model metadata remain excluded.

[ADR 0001](0001-source-of-record-not-runtime.md) fixes that kb-infra is a spec:
each automation is authored here and **materializes** into a scheduled run
elsewhere. This ADR pins down *where* "elsewhere" is and what the running agent may
assume about its surroundings.

A materialized automation runs with its **sink checkout as the working directory**
— Job Pursue runs inside the `career-system` clone, Portfolio Refresh inside the `portfolio` clone. The kb-infra repository is **not** checked out
next to it. Therefore the composed prompt is the agent's entire world: it must carry
every rule and context surface the run needs, and it must never instruct the agent
to read a kb-infra spec file by a working-directory-relative path.

## Context

The automation prompts inherited a `Setup:` step that told the agent to "read this
repo's AGENTS.md, docs/workflows.md, docs/knowledge-bank-conventions.md,
docs/automations/_preamble.md, and skills/lookup/SKILL.md before acting." That step
silently assumed the run happened inside a kb-infra checkout. In production it does
not: "this repo" resolves to the sink, those paths are absent, and the run either
errors on missing files or wastes a turn discovering they are gone. The instruction
was also redundant — `setup-kb-infra` already prepends the preamble into the composed
prompt, and `lookup`/`capture` are installed as skills, not files to open.

The composition itself leaned on the same wrong assumption: it dumped the full
endpoint/sink/source catalog and a separate resolved-bindings block into every
prompt, treating the preamble as a shared file the agent could cross-reference,
rather than as the raw material for a single self-contained artifact.

## Considered options

- **Give the run a path to a kb-infra checkout (a binding).** Rejected: it makes the
  spec a runtime dependency of every scheduled run, reintroducing the stale local
  copy ADR 0001 exists to avoid, and it couples the run to a second checkout being
  present and current on the box.
- **Keep prepending the whole preamble and let the agent ignore the irrelevant
  parts.** Rejected: it forces the agent to read a full vocabulary catalog, a
  resolved-bindings block, cadence, and blank overrides to use a handful of surfaces,
  and it keeps the description of a surface split from its resolved location.
- **Compose a lean, self-contained prompt (chosen).** `setup-kb-infra` selects only
  the surfaces an automation declares, emits each as one resolved line (role
  description + binding hint together), injects only the operating rules, and names
  the sink clone as the working directory. The preamble becomes the composer's
  reference vocabulary, not injected text.

## Consequences

- The composer treats the preamble as a lookup table: it injects the shared
  operating rules and, for each surface or sink capability the automation
  declares, one resolved line — never the whole catalog, the provider block,
  cadence, model selection, reasoning effort, or overrides. Cadence and concrete
  model selection live in the local desired/installed state and the harness; they
  are runtime metadata, not prompt text.
- Automation sources declare only a provider-agnostic execution profile. Setup maps
  that recommendation to a model and reasoning effort supported by the local
  harness, while a recorded concrete local selection remains the materialized
  choice and drift boundary.
- Automation bodies reference the sink by role as the working directory and read only
  the sink's own docs; they never read kb-infra spec files at runtime.
- A runtime dependency on a kb-infra convention (for example KB Reconcile's
  follow-up marker formats) is **inlined** into the composed prompt at materialize
  time, not left as a path the agent is told to open.
- Sink-native commands and workflow names are capability bindings. The generic
  automation declares the operation it needs; only materialization names the
  concrete implementation in the bound sink checkout.
- A composed prompt is judged self-contained: if a run needs a fact, that fact is in
  the prompt or reachable through `/lookup`, never through the spec checkout.
