# Knowledge Bank Conventions

These conventions define how agents author and maintain the Knowledge Bank. The
KB remains the source of truth; this repo holds the provider-agnostic operating
contract. `setup-kb-infra` discovers how the concrete provider maps to it.

The contract is based on the accepted
[semantic-authoring research](research/semantic-authoring-and-okf.md) and
[ADR 0012](adr/0012-semantic-authoring-and-non-destructive-reconciliation.md).

## Global Invariants

Every page and Capture draft must satisfy three invariants:

1. Avoid duplication: one canonical owner per meaning; link or reconcile instead
   of copying.
2. Prefer the shortest wording that preserves meaning, scope, qualifiers, and
   evidence.
3. Make semantics explicit enough for an agent to parse and natural enough for a
   person to browse.

These invariants govern all page Types, Ownership values, Maturity values, and
Kinds. They do not require a rigid page profile.

## Database Shape

The main KB database is the eagle-eye view of the Knowledge Bank. Keep visible
views sparse. Do not add maintenance-only metadata to the main table unless it
improves day-to-day scanning.

Use hierarchy as the primary classifier. A page's parent and location should
explain its context before a property does. Keep the fewest pages that preserve
clear ownership and retrieval. Prefer strengthening an existing owner page over
creating another page.

Maintain an **Active Canonical View** for people and agents. Presence in that view
implies relevance. Do not keep irrelevant pages merely to preserve history: first
migrate unique durable content, rebind inbound links, and ensure the deletion or
invalidation is recoverable through Revision Evidence.

## Orthogonal Axes

Describe a page or section with four independent questions:

| Axis | Question | Values |
| --- | --- | --- |
| Type | What does the page represent? | Provider- or domain-defined. |
| Ownership | Who owns this meaning? | `Canonical`, `Adapter`; `Unresolved` only during migration. |
| Maturity | How editorially processed is the content? | `Raw`, `Developing`, `Stable`. |
| Kind | What does this section or unit mean? | The versioned registry below. |

Do not derive one axis from another. A project Type can contain Stable State,
Developing Direction, and Raw Evidence. An Adapter can be Stable without becoming
Canonical. Orthogonality does not make every combination valid: Kind-specific
rules and the quality gate still apply.

### Ownership

Choose one canonical owner for each fact, chapter, lesson, term, or policy. Other
pages link to the owner instead of restating it. Canonical ownership may be
implicit only after a complete baseline audit has confirmed one owner and the
migration is complete. Capture must still check for competing owners before every
write.

An Adapter presents selected knowledge for a purpose. Mark it explicitly and link
each adapted meaning to its canonical owner. An Adapter must not silently become a
second owner.

Before that audit and migration are complete, a missing marker does not imply
Canonical ownership. Capture must establish the owner explicitly or mark ambiguous
ownership `Unresolved`, never silently `Canonical`. Unresolved ownership blocks a
Capture write. Source credibility and trustworthiness belong in provenance; they
are not Ownership values.

### Maturity

Maturity measures editorial processing only:

- `Raw`: new intake or unaudited legacy content. It does not silently participate
  in ordinary answers.
- `Developing`: reconciled, approved, and useful, but explicitly unsettled or
  expected to change.
- `Stable`: reconciled, approved, sufficiently supported, and safe to reuse.

All incoming content defaults to `Raw`; retained knowledge should normally progress
toward `Stable`. Stable does not mean immutable, certain, true forever, or final.
Volatility belongs in time metadata, uncertainty in the prose, and relevance in
the Active Canonical View.

The normal transition is:

```text
Raw -> Semantic Quality Gate -> Stable | Developing | retained Raw
```

Retained Raw content in the Active Canonical View must name its owner, provenance,
retention reason, and next review or distillation action. `Archive` and `Final` are
not Maturity values.

## Kind Registry

The initial registry is version 1. Each Kind has a stable identifier independent
of its displayed heading. An agent must use explicit Kind metadata or a registered
mapping; it must not infer Kind from arbitrary heading text. Preferred headings
may be adapted for readability, while registered aliases remain retrieval aids.

| ID | Kind | Meaning and semantic force | Preferred heading; aliases |
| --- | --- | --- | --- |
| `state` | State | A verified current condition. Use `is`, `has`, or `uses`; show `as of` when volatility changes interpretation. | State; Current state, Status |
| `direction` | Direction | An aim or exploration, not a settled choice. Use `aims to`, `is intended to`, or `is exploring`. | Direction; Intent, Goal |
| `decision` | Decision | A selected option or commitment. State the choice before rationale and alternatives. | Decisions; Choice, Commitment |
| `rule` | Rule | A scoped norm. `must` has no exception, `should` is the default with justified exceptions, and `may` grants permission. | Rules; Policy, Constraint |
| `preference` | Preference | What a named subject favors or avoids, including strength when material. | Preferences; Tendency |
| `procedure` | Procedure | Ordered actions with an observable outcome. Use imperative steps. | Procedure; Steps, How to |
| `event` | Event | Something that happened. Use an absolute date when known and past tense. | Events; History, Timeline |
| `evidence` | Evidence | Material supporting or qualifying a claim, with provenance. | Evidence; Sources, Basis |
| `open-item` | Open item | An unresolved question or outcome requiring follow-up. Phrase it directly. | Open questions; Follow-up, Unknowns |
| `schema` | Schema | A reusable shape, field contract, or controlled vocabulary. | Schema; Fields, Vocabulary |
| `example` | Example | A concrete illustration that does not itself define the rule. | Examples; Sample |
| `citation` | Citation | An external source reference with enough identity to retrieve it. | Citations; References |

Treat semantic-force phrases as preferred controlled authoring, not a closed
dictionary. Lowercase `must`, `should`, and `may` are this project's contract; they
do not claim IETF BCP 14 semantics. Every Rule needs a scope. Do not use `will`
where it could mean either a prediction or a commitment. State uncertainty
explicitly.

Add, merge, or retire a Kind only after repeated captures expose ambiguity that the
registry cannot represent. Version the change and preserve stable IDs or an
explicit migration mapping.

## Page and Section Structure

Keep one canonical subject per page and one dominant Kind per section. A knowledge
unit should carry one primary claim, instruction, or question while retaining the
subject, scope, qualifiers, time, uncertainty, and adjacent rationale or evidence
needed for independent interpretation.

Do not create universal page profiles, empty sections, or decorative structure.
Order what exists by these rules:

1. Put a one-sentence description first.
2. Put current or actionable content before supporting history and evidence.
3. Put Open questions and Citations last.

Claim-to-qualifier, rationale, and evidence adjacency overrides the global order.
Citations may remain last when inline correspondence still makes the supporting
source unambiguous.

Choose the least complex presentation that preserves relationships:

- use short prose for one assertion or a tightly coupled explanation;
- use parallel bullets for two or more unordered peers;
- use numbers for ordered or ranked items;
- use a description or labelled list for term-definition pairs;
- use a table for repeated records with comparable attributes;
- separate examples from rules while keeping them adjacent when needed;
- number external Citations and use inline correspondence when source mapping
  would otherwise be unclear.

## Naming and Terminology

Use names that make retrieval unambiguous without making the workspace stiff.
Project pages should usually use stable repo or product slugs—the same handle used
on GitHub and in local paths. Put the human-readable description in the body.

Use human-readable names for life areas, credentials, milestones, lesson
collections, strategies, and public concepts. Generic names are allowed only when
the parent path disambiguates them. If search results are ambiguous, add context to
the title.

Use one canonical term for one concept. Keep aliases with the term's owner as
retrieval aids, not duplicate definitions. Expand uncommon abbreviations. Flag
uncertain equivalence instead of silently merging concepts. Cross-cutting terms
must have one vocabulary owner.

## Time and Provenance

Use four distinct temporal meanings:

- `observed_at`: when a State was observed. Retain it internally for every State;
  add visible `as of` only when volatility changes interpretation.
- `event_at`: when an Event happened. Use an exact known date and show it with the
  Event.
- `valid_from` and `valid_until`: the optional interval in which knowledge applies.
  Record either only when validity changes interpretation.
- `captured_at`: when an accepted mutation entered the KB. Retain it for every
  mutation.

Never use relative time without an absolute anchor. Do not substitute one temporal
meaning for another.

Visible citations and dates are selective; Revision Evidence is universal. Every
accepted mutation must retain the source, actor, `captured_at`, affected owner,
revision identity, prior revision, and exact diff, plus `observed_at` for every
State it changes. When meaning changes, record an explicit `supersedes`, `revises`,
or `invalidates` relation. An Approval Draft counts as provenance only when it is
durably retained and linked to the resulting revision. Raw content requires
stronger visible provenance than Stable content.

## Reconciliation

Capture reconciles the Active Canonical View; it does not merely append notes.
Before drafting a write:

1. Read the complete affected section and its owner context.
2. Compare every new assertion with current content and linked owners.
3. Preserve, merge, replace, or delete each affected meaning deliberately.
4. Rewrite the smallest coherent section that can express the result.
5. Append only a genuine chronological Event or a new peer in an existing set.
6. Remove superseded wording in the same write.
7. Show the exact before/after diff and preserved Revision Evidence.

Reconciliation may simplify the active page, but it must not destroy history.

## Semantic Quality Gate

Every Approval Draft must show the gate, either visible or collapsed. Each result
uses `Pass`, `Flag`, `Not checked`, or `Not applicable` and includes the checked
scope plus evidence. A bare `Pass` is invalid.

Separate deterministic checks—allowed Kind, absolute date syntax, link resolution,
required fields—from semantic judgments—correct owner, contradiction, duplication,
faithful compression, and material omission.

At minimum, the gate covers:

| Check | Required evidence |
| --- | --- |
| Ownership | Canonical owner checked, competing owners considered, Adapter links identified. |
| Coverage | Source assertions mapped to preserved, changed, omitted, or rejected content. |
| Preservation | Qualifiers, uncertainty, time, rationale, and unique durable content accounted for. |
| Faithfulness | Draft claims trace to sources without unsupported strengthening. |
| Duplication and contradiction | Affected section and linked owners compared. |
| Kind and semantic force | Stable Kind ID and Kind-specific constraints checked. |
| Time and provenance | Required anchors, source, actor, and revision evidence present. |
| Deletion safety | Unique content, inbound links, and recovery path checked when deleting. |

Unresolved ownership, contradiction, material omission, unsupported assertion, or
unsafe deletion blocks the write. Human approval is a control, not proof.

### Executable Validation

The provider-neutral Capture transition record is versioned in
[`contracts/capture-transition-v1.json`](../contracts/capture-transition-v1.json).
Validate one JSON record with:

```sh
python3 scripts/validate-capture-transition.py <record.json>
```

The validator generates deterministic results for the record contract, operation,
provider-defined Type, registered Kind and structurally expressible Kind
constraints, Maturity, Ownership structure, source provenance, timezone-aware
absolute time, exact Revision Evidence, references, per-assertion Adapter links,
retained Raw context, and deletion structure. Lifecycle stays in the operation: a
deletion keeps its content Maturity unchanged and uses an `invalidates` revision
relation. The validator carries supplied semantic judgments into separate result
rows only when each judgment has a registered check, status, checked scope,
evidence, and issue code. Missing judgments become `Not checked`; malformed,
unknown, or duplicate judgments are deterministic contract failures.
In particular, Kind registration and required assertion fields are deterministic;
whether the prose preserves the Kind's semantic force is a separate
`kind-and-semantic-force` judgment and is never inferred from structure.

The report disposition is `Pass`, `Flag`, or `Block`. Blocking deterministic
failures and the five contract-defined semantic blockers return exit status 2;
`Pass` and non-blocking `Flag` return 0. Every report still sets `write_allowed` to
false and records human approval as required and `Not checked`: validation never
approves a KB write. Representative records live in
[`tests/fixtures/capture-transitions/`](../tests/fixtures/capture-transitions/), and
the repository check runs their black-box validation tests.

## Follow-up Markers

Use a follow-up marker for a deferred or time-ambiguous knowledge update that a
future lookup should ask about. It is an `Open item`, not a task status.

```md
Follow-up: ask again on YYYY-MM-DD: <short question or update prompt>.
```

- Put it near the start of the page body, after any structural block that must stay
  first.
- Use an absolute ISO date in the user's local calendar.
- Keep the prompt short enough to ask directly.
- Use a page-body marker instead of a dated task property when the update is a
  deferred knowledge question rather than a dated task.
- Remove or replace it only through an approved Capture write after resolution or
  intentional deferral.

## Final Form Markers

A final form marker is a rare lookup interaction directive, not Maturity. Use it
only when the user explicitly says a topic should no longer prompt questions.

```md
Lookup: this topic is in its final form; its content should not be questioned unless the user explicitly reopens it.
```

Put it near the content it covers. Lookup skips that content until the user reopens
it. Add, remove, or change the marker only through an approved Capture write.

## Drift Audits

Drift audits are read-only and reproducible. A full audit produces a coverage
manifest with page IDs, inaccessible or partial records, timestamp, convention and
Kind-registry version, and unresolved exceptions. It checks:

- duplicate meanings, ambiguous names, and competing owners;
- Unresolved Ownership or Adapters that have started owning canonical facts;
- Raw content used as Stable knowledge or retained without required context;
- Kind or semantic-force mismatch;
- missing time, provenance, revision evidence, or source correspondence;
- stale State, due Follow-up markers, relative time, and broken relations;
- sparse high-importance pages, unclear parentage, and irrelevant active pages.

Before each migration batch, re-read its targets and inbound and outbound
relations. After a write, read back the result and run local checks. After all
batches, rerun the global audit. Preserve stable page identities and a rollback
path. Audits propose exact drafts; they never write to the KB.

## OKF Boundary

Open Knowledge Format is a future read-only interchange adapter, not the KB's
native semantic contract. An adapter must pin an OKF version or commit, map stable
provider page IDs rather than titles or hierarchy, preserve unknown fields, and
export Kinds through a documented producer extension instead of overloading page
Type. KB validation remains stricter than OKF conformance.
