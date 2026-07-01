# Knowledge Bank Conventions

These conventions describe how agents should work with the Knowledge Bank. The KB
remains the source of truth; this repo holds the formal operating rules. They are
the reference shape a KB can take; `setup` discovers how your KB actually maps to
them.

## Database Shape

The main KB database is the eagle-eye view of the Knowledge Bank. Keep visible
views sparse. Do not add maintenance-only metadata to the main table unless it
directly improves day-to-day scanning.

Use hierarchy as the primary classifier. A page's parent and location should
explain its context before a property does.

Keep the least number of pages possible. Prefer strengthening an existing owner
page over creating a new page.

## Ownership

Choose one canonical owner for each fact, chapter, or lesson. Other pages should
link to the owner instead of duplicating the fact.

Adapter pages present selected facts for a purpose. They should not become
source-of-truth stores unless they explicitly say they own that fact.

## Naming

Use names that make retrieval unambiguous without making the workspace stiff.

Project pages should usually use stable repo or product slugs — the same handle
you use on GitHub and in local paths. Slugs map cleanly to repositories, paths,
and agent lookup. Do not rename established project slug pages only to make them
prettier; put the human-readable description inside the page body.

Non-project knowledge pages should use human-readable names when they represent a
life area, credential, milestone, lesson collection, strategy, or public concept.

Generic names are allowed only when the parent path disambiguates them clearly. If
search results become ambiguous, add context or role to the title, such as
`Ideas Archive`, `Interview Scratchpad`, or `Reading Notes (2024)`.

Raw, archive, adapter, and scratchpad pages should signal that role in the title
or first paragraph when they could be mistaken for canonical knowledge.

## Role Property

The `Role` property exists for ambiguous or high-risk pages only. Leave it empty
when hierarchy is enough.

Allowed `Role` values:

- `Canonical`: owns a fact, convention, policy, project state, or durable source.
- `Adapter`: presents selected facts from other owners for a specific audience or
  workflow.
- `Raw`: captures notes that still need distillation or verification.
- `Archive`: preserves history that is not the current source of truth.

## Follow-up Markers

Use a follow-up marker when a page contains a deferred, raw, provisional, or
time-ambiguous fact that the user should be asked about in a future lookup. This
is for life and project knowledge that should be revisited, but is not itself a
time-bounded task.

Format:

```md
Follow-up: ask again on YYYY-MM-DD: <short question or update prompt>.
```

Rules:

- Put the marker near the start of the page body, after any structural block that
  must stay first.
- Use an absolute ISO date in the user's local calendar. Do not use relative
  phrases such as `next week`, `tomorrow`, or `soon`.
- Keep the prompt short enough that a future agent can ask it directly.
- Use page-body markers instead of dated task properties when the update is a
  deferred knowledge question rather than a dated task.
- Remove or replace the marker only through an approved `capture` write after the
  question has been answered or intentionally deferred again.

## Final Form Markers

Use a final form marker only when the user explicitly says a topic should not be
questioned again. This is stronger than discarding a lookup question; a normal
discard leaves no KB trace.

Format:

```md
Lookup: this topic is in its final form; its content should not be questioned unless the user explicitly reopens it.
```

Rules:

- Put the marker near the specific page section or page opening it applies to.
- Use it rarely. Prefer no marker when the user only discards one lookup question.
- Lookup should skip final form content entirely unless the user explicitly
  reopens it.
- Add, remove, or change the marker only through an approved `capture` write.

## Drift Audits

Drift audits should find places where the Knowledge Bank no longer matches these
conventions.

Look for:

- duplicate or generic page names that make retrieval ambiguous
- pages whose owner or role is unclear
- adapter pages that are starting to own canonical facts
- raw notes being treated as canonical knowledge
- pages with unclear parentage
- sparse high-importance pages
- stale project state
- due follow-up markers and relative-time phrases that should become exact
  follow-up markers
- contradictions with the one-owner/no-duplication rule

Drift audits must propose exact drafts or property changes for the user to
approve. They must not write to the KB directly.
