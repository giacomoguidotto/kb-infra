# Knowledge Bank Conventions

These conventions describe how agents should work with Giacomo's Notion Knowledge Bank. Notion remains the source of truth; this repo holds the formal operating rules.

## Database Shape

The Notion `life` database is the eagle-eye view of the Knowledge Bank. Keep visible database views sparse. Do not add maintenance-only metadata to the main table unless it directly improves day-to-day scanning.

Use hierarchy as the primary classifier. A page's parent and location should explain its context before a property does.

Keep the least number of Notion pages possible. Prefer strengthening an existing owner page over creating a new page.

## Ownership

Choose one canonical owner for each fact, chapter, or lesson. Other pages should link to the owner instead of duplicating the fact.

Adapter pages, such as `profile`, present selected facts for a purpose. They should not become source-of-truth stores unless they explicitly say they own that fact.

## Role Property

The `Role` property exists for ambiguous or high-risk pages only. Leave it empty when hierarchy is enough.

Allowed `Role` values:

- `Canonical`: owns a fact, convention, policy, project state, or durable source.
- `Adapter`: presents selected facts from other owners for a specific audience or workflow.
- `Raw`: captures notes that still need distillation or verification.
- `Archive`: preserves history that is not the current source of truth.

## Drift Audits

Drift audits should find places where the Knowledge Bank no longer matches these conventions.

Look for:

- duplicate or generic page names that make retrieval ambiguous
- pages whose owner or role is unclear
- adapter pages that are starting to own canonical facts
- raw notes being treated as canonical knowledge
- pages with unclear parentage
- sparse high-importance pages
- stale project state
- contradictions with the one-owner/no-duplication rule

Drift audits must propose exact drafts or property changes for Giacomo to approve. They must not write to Notion directly.
