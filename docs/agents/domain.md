# Domain Docs

Knowledge System is a single-context specification repo for governed access to a
provider-backed Knowledge Bank.

- Use root `CONTEXT.md` for vocabulary.
- Use `docs/adr/` for policy decisions (the source-of-record framing and the
  binding model live there).
- Use `docs/workflows.md` for accepted workflow boundaries.
- Use `docs/knowledge-bank-conventions.md` for KB conventions and lower-level
  drift-audit rules.
- Use `docs/automations/_preamble.md` for the shared automation preamble, endpoint
  vocabulary, and sink vocabulary.
- Use the setup module's KB Reconcile resource for the Knowledge-owned automation
  definition. Remaining `docs/automations/*.md` files are migration sources for
  their owning systems.

When writing issue titles, test names, docs, or refactor proposals, prefer terms
from `CONTEXT.md`.

If a change contradicts an accepted ADR, say so explicitly before proceeding.
