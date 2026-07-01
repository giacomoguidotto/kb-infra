---
status: accepted
---

# kb-infra is a source-of-record, not a runtime

Knowledge Bank Infrastructure defines an agent operating system whose parts run
elsewhere: **the provider is the memory, the harness runtime runs the automations,
and this repo is the spec.** It holds three kinds of definitions — the agent tool
belt (skills), scheduled rituals (automation prompts), and the shape of the memory
(Knowledge Bank conventions) — and nothing in it executes. Each definition is
authored, versioned, and reviewed here before it **materializes** into a live
system. This is Infrastructure-as-Code applied to a personal agent OS: like
Terraform files that declare a cloud without running it.

## Considered options

- **Runtime infra.** Rejected: the repo would then be expected to run automations
  and hold knowledge, duplicating the runtime and the provider and reintroducing
  the stale local copy the project exists to avoid.
- **Untyped "misc agent files" repo.** Rejected: the tool belt, the rituals, and
  the conventions look mismatched only until you name the shared job — they are
  all definitions that materialize outward.

## Consequences

- Every definition doc states where its materialization lives (the runtime, the
  provider, or the loaded skill), so "defined here, runs elsewhere" is explicit,
  not implied.
- Personal facts are leaks by definition; the repo stays a generic spec, and
  decoupling from personal information is a correctness rule, not cosmetics.
- CI validates the source only (links, skill frontmatter, no personal coupling,
  preamble presence). It cannot and should not touch the live systems; that is
  not a coverage gap.
