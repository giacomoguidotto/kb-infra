# Domain Docs

Knowledge Bank Infrastructure is a single-context infrastructure repo for a
provider-backed knowledge system.

- Use root `CONTEXT.md` for vocabulary.
- Use `docs/adr/` for policy decisions (the source-of-record framing and the
  binding model live there).
- Use `docs/workflows.md` for accepted workflow boundaries.
- Use `docs/knowledge-bank-conventions.md` for KB conventions and lower-level
  drift-audit rules.
- Use `docs/automations/_preamble.md` for the shared automation preamble, endpoint
  vocabulary, and sink vocabulary.
- Use `docs/automations/*.md` for each accepted scheduled automation prompt:
  `knowledge-harvest`, `social-draft-pulse`, `portfolio-surface-sweep`,
  `job-hunt-evaluate-audit`, `job-hunt-advance-audit`, `job-hunt-tune-audit`.

When writing issue titles, test names, docs, or refactor proposals, prefer terms
from `CONTEXT.md`.

If a change contradicts an accepted ADR, say so explicitly before proceeding.
