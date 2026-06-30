# Domain Docs

Knowledge Bank Infrastructure is a single-context infrastructure repo for a Notion-backed knowledge system.

- Use root `CONTEXT.md` for vocabulary.
- Use `docs/adr/` for policy decisions that touch the change.
- Use `docs/workflows.md` for accepted workflow boundaries.
- Use `docs/knowledge-bank-conventions.md` for Notion `life` database conventions and lower-level drift-audit rules.
- Use `docs/automations/kb-drift-realignment.md` for the accepted scheduled Knowledge Bank Drift Realignment prompt.
- Use `docs/automations/social-draft-pulse.md` for the accepted scheduled social-draft prompt.
- Use `docs/automations/portfolio-surface-sweep.md` for the accepted scheduled portfolio-sweep prompt.
- Use `docs/workflows.md` for the accepted Job Hunt Eval Pulse boundary; its live automation id is `career-ops-scan-and-evaluate`.
- Use `docs/automations/job-hunt-tuning-audit.md` for the accepted scheduled career tuning prompt.
- Use `docs/automations/job-hunt-advancement-pulse.md` for the accepted scheduled advancement-pack prompt.

When writing issue titles, test names, docs, or refactor proposals, prefer terms from `CONTEXT.md`.

If a change contradicts an accepted ADR, say so explicitly before proceeding.
