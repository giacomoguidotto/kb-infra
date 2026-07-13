# Knowledge Bank Conventions

These conventions define how agents author the KB. The KB is the source of truth;
this repo holds the provider-neutral rules. See the supporting
[research](research/semantic-authoring-and-okf.md) and
[ADR 0012](adr/0012-semantic-authoring-and-non-destructive-reconciliation.md).

## Global Invariants

1. **Avoid duplication.** Keep one canonical owner per meaning; reconcile or link
   instead of copying.
2. **Be concise without loss.** Use the shortest wording that preserves meaning,
   scope, qualifiers, time, rationale, and useful evidence.
3. **Serve agents and people.** Make semantics explicit enough to parse and natural
   enough to browse.

These rules apply everywhere without imposing a universal page template.

## Active View And Metadata

Keep the active KB relevant. Preserve history through provider revisions or a bound
evidence surface, not by keeping obsolete pages in ordinary views. Before deleting
anything, migrate unique meaning, rebind inbound links, and confirm recovery.

Use hierarchy before metadata: a page's parent and location should explain its
context. Add only properties that improve ownership, retrieval, or everyday use.

Keep four semantic axes independent:

| Axis | Meaning | Values |
| --- | --- | --- |
| Type | What the page represents | Provider- or domain-defined |
| Ownership | Where meaning is owned | `Canonical`, `Adapter`; migration-only `Unresolved` |
| Maturity | How processed the content is | `Raw`, `Developing`, `Stable` |
| Kind | What a section or unit means | Registry below |

Do not use Ownership for trust, relevance, lifecycle, or maturity. Do not infer one
axis from another.

### Ownership

A Canonical page owns its subject. An Adapter presents selected meaning for a
purpose and links back to its owner. Until migration establishes an owner,
`Unresolved` is honest and blocks Capture.

Check for competing owners before each write. Store source trust in provenance,
not Ownership.

### Maturity

- `Raw`: new intake or unaudited legacy content.
- `Developing`: reconciled and useful, but explicitly unsettled.
- `Stable`: reconciled, supported, and safe to reuse.

New intake defaults to Raw; retained knowledge should normally progress to Stable.
Stable means reusable, not immutable or eternally true. Express uncertainty in the
content, volatility in time, and relevance through presence in the active view.

## Kind Registry

Use one dominant Kind per section. Store the stable ID in provider metadata or a
registered mapping; headings may use readable aliases.

| ID | Kind | Semantic force |
| --- | --- | --- |
| `state` | State | A current condition; name the subject and observation time when volatility matters. |
| `direction` | Direction | An aim or exploration, not a settled choice. |
| `decision` | Decision | A selected option or commitment; state the choice first. |
| `rule` | Rule | A scoped norm: `must`, `should`, or `may`. |
| `preference` | Preference | What a named subject favors or avoids. |
| `procedure` | Procedure | Ordered actions with an observable result. |
| `event` | Event | Something that happened; use past tense and an absolute date when known. |
| `evidence` | Evidence | Material supporting or qualifying a claim, with provenance. |
| `open-item` | Open item | An unresolved question or outcome requiring follow-up. |
| `schema` | Schema | A reusable shape, field contract, or vocabulary. |
| `example` | Example | An illustration that does not define the rule. |
| `citation` | Citation | A retrievable external source reference. |

Add or retire a Kind only after repeated captures reveal meaning the registry cannot
represent. Preserve stable IDs or publish a migration mapping.

## Page And Section Structure

Treat rows whose meaning is fully carried by a structured table's schema and fields
as records, not knowledge pages. The data source supplies their type and context; do
not force page-level Ownership, Maturity, Kind, or semantic prose into a Notes field
or blank page body. Use table and hierarchy context to disambiguate repeated titles.
Treat a row as a knowledge page only when its page body owns independent durable
knowledge.

- Keep one canonical subject per page and one primary claim, instruction, or
  question per knowledge unit.
- Start with a one-sentence description.
- Put current or actionable content before supporting history.
- Keep qualifiers, rationale, and evidence beside the claim they affect.
- Put open items and citations last when adjacency does not require otherwise.
- Create no empty sections or decorative structure.

Use the least complex shape that preserves relationships: prose for one assertion,
bullets for unordered peers, numbers for sequence, labelled entries for definitions,
and tables only for repeated comparable records. Keep examples distinct from rules.

## Language And Naming

Use one canonical term per concept and keep aliases at its owner for retrieval.
Expand uncommon abbreviations and flag uncertain equivalence. Avoid ambiguous
`will`; name a prediction, direction, or decision.

Project pages usually use stable repository or product slugs. Other pages use clear
human names; the parent path may supply context. Add title context only when search
results would otherwise be ambiguous.

Tone comes from the bound KB or target surface, never from the length, mood, or
verbosity of the preceding conversation. Without a binding, write in a neutral,
direct, calm voice.

## Time And Revision Evidence

Keep temporal meanings distinct:

- `observed_at`: when a State was observed;
- `event_at`: when an Event happened;
- `valid_from` / `valid_until`: when knowledge applies;
- `captured_at`: when an approved mutation entered the KB.

Use absolute anchors; never substitute one time for another.

Every accepted mutation must remain recoverable through provider history or the
bound Revision Evidence surface. Retain the source, actor, capture time, affected
owner, prior revision, and exact change. When meaning changes, identify whether the
new revision supersedes, revises, or invalidates the prior one. A changed State also
keeps its observation time.

## Reconciliation And Capture

Capture maintains the active canonical view; it does not append session summaries.

Before drafting:

1. Read the complete affected section, live schema, likely owner, and competing
   owners.
2. Compare each new meaning with current content and relevant relations.
3. Preserve, merge, replace, append, or remove it deliberately.
4. Rewrite the smallest coherent section that expresses the result.
5. Append only chronological Events or new peers in an existing set.
6. Show the exact current and proposed result in the approval draft.

Check ownership, source coverage, faithfulness, duplication, contradiction,
semantic force, time, and deletion safety. Unresolved ownership, contradiction,
unsupported content, material omission, or unsafe deletion blocks the write. A
formal machine-readable report is unnecessary; the approval draft must make the
evidence and any gap understandable.

Immediately before applying an approved draft, re-read the affected targets. Drift
invalidates approval. After applying, read back every result.

## Lookup Markers

Use a follow-up marker for a deferred knowledge question, not a task status:

```md
Follow-up: ask again on YYYY-MM-DD: <short question or update prompt>.
```

Use an absolute local date and keep the marker near the content it affects. Remove
or defer it only through approved Capture.

Use a final-form marker only when the user explicitly closes a topic to future
questions:

```md
Lookup: this topic is in its final form; its content should not be questioned unless the user explicitly reopens it.
```

This is a lookup directive, not Maturity.

## Audits And OKF

Drift audits are read-only. Check duplicates, competing owners, ambiguous names,
misused metadata, unsupported Raw reuse, Kind mismatch, missing time or provenance,
stale State, due follow-ups, broken relations, unclear hierarchy, and irrelevant
active pages. Keep private snapshots under gitignored `local/`; do not commit a KB
mirror or require a repository compiler.

Open Knowledge Format remains a future read-only interchange adapter, not the KB's
native contract. Pin its version, map stable provider IDs, preserve unknown fields,
and export Kinds through a documented extension.
