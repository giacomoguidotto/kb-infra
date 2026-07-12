# Semantic authoring for Capture, and where OKF fits

Research dates: 2026-07-10 to 2026-07-12

Implementation status: accepted and materialized by
[ADR 0012](../adr/0012-semantic-authoring-and-non-destructive-reconciliation.md)
and the [Knowledge Bank conventions](../knowledge-bank-conventions.md). This file
is their research specification. Earlier sections preserve the research and design
path; where wording conflicts, the
[full-contract stress test](#full-contract-research-stress-test-2026-07-12)
governs the research conclusions, and the materialized contract governs operation.

## Conclusion

The proposed semantic writing model is well supported, but it should be a
**lightweight controlled-authoring model**, not a formal controlled natural
language and not an OKF migration.

The useful order is:

1. define knowledge kinds and their prose forms;
2. enforce a small house style and canonical terminology;
3. validate capture drafts structurally and flag semantic duplication for review;
4. add provenance and valid-time only when they change interpretation;
5. later expose the canonical Notion KB through a read-only OKF adapter.

OKF is useful now as a design constraint and future interchange target. It is too
early to make it the KB's native contract: the current specification is explicitly
**v0.1 Draft**, requires only a free-form `type`, leaves body sections and type
taxonomies to producers, treats links as untyped relationships, and deliberately
uses permissive conformance. It supplies a container for a semantic model; it does
not supply the model itself. [OKF v0.1 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/d44368c15e38e7c92481c5992e4f9b5b421a801d/okf/SPEC.md),
[Google Cloud introduction](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

## What the research supports

### 1. Type knowledge before styling it

DITA is a mature example of content-model-driven authoring. It makes a topic the
single-subject unit of authoring and reuse, distinguishes semantic information
types such as concept, task, and reference, and recommends concise, modular topics
without unnecessary transitional prose. This supports the hypothesis that voice
and structure should follow what a knowledge unit *is*, rather than the tone of the
conversation that produced it. [OASIS DITA topic architecture](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/base/topicover.html)

For this KB, the corresponding unit is not necessarily a whole Notion page. One
page can contain several typed sections or assertions. Call this dimension
**knowledge kind** so it does not collide with the existing page `Role`
(`Canonical`, `Adapter`, `Raw`, `Archive`). A small initial vocabulary is enough:

| Knowledge kind | Canonical form |
| --- | --- |
| Concept | Definition or explanation in neutral present tense. |
| State | Explicit subject, current condition, and `as of` date when volatile. |
| Preference | Explicit owner and preference strength; first person is acceptable only when the page makes the owner unambiguous. |
| Decision | Chosen option first; rationale and rejected alternatives separately. |
| Rule | Explicit normative force: `must`, `should`, or `may`. |
| Procedure | Ordered imperative steps with an observable outcome. |
| Event | Absolute date and concise past-tense statement. |
| Evidence | Source or exact quote only when provenance or wording matters. |

This vocabulary is a project-specific synthesis, not a claim that DITA defines
personal knowledge. DITA's relevant lesson is to start with a few semantic types
and specialize only when repeated authoring needs justify it.

### 2. Use controlled authoring, not a fully formal language

Controlled natural languages range from human-oriented simplification to
machine-oriented formal representation. The field evaluates trade-offs among
precision, expressiveness, naturalness, and simplicity; the survey explicitly
warns that there is no universally best point and that the right compromise
depends on the application. [Kuhn, *A Survey and Classification of Controlled Natural Languages*](https://aclanthology.org/J14-1005/)

At the formal end, Attempto Controlled English translates restricted English into
discourse representation structures and then optionally into Prolog. That is useful
when deterministic logical interpretation is the goal, but it is more restrictive
than this KB needs. [Fuchs and Schwitter, *Attempto Controlled English*](https://arxiv.org/abs/cmp-lg/9603003)

Capture should therefore use a light rule set that improves both retrieval and
reading without pretending that prose is executable logic:

- Write one durable assertion per sentence or list item.
- Use the canonical term and an explicit subject; avoid pronouns with unclear
  antecedents.
- Prefer a direct verb and the shortest wording that preserves meaning.
- Preserve semantic force: a fact, preference, intention, decision, and rule are
  not interchangeable.
- State negation and uncertainty explicitly.
- Separate the decision from its rationale, and the claim from its evidence.
- Use absolute dates and accurate tense; add `as of YYYY-MM-DD` only to volatile
  state.
- Remove transcript framing, agent voice, filler, and repeated context.
- Link to the canonical owner instead of restating its content.
- Preserve a quote verbatim only when the wording itself is durable knowledge.

Stable vocabulary matters as much as sentence style. SKOS separates a preferred
label from alternate and hidden labels, permits only one preferred label per
language, and distinguishes hierarchical from associative concept relations. The
KB does not need to become RDF to adopt the same discipline: one canonical term,
recorded aliases for retrieval, and explicit relationship names where a generic
link would be ambiguous. [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)

### 3. Separate authoring, validation, and semantic review

SHACL demonstrates a useful architectural separation: a data graph is checked
against a separate shapes graph, and validation produces explicit results. Shapes
can also drive interfaces and integration. SHACL itself targets RDF, so applying it
directly to Notion would require an RDF mapping; the immediate lesson is to keep
Capture's content rules separate from captured content and make draft checks
observable. [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/)

A future Capture draft can carry a provider-neutral internal record such as:

```yaml
target: <canonical owner>
operation: create | update | replace-section
knowledge_kind: <kind>
assertions: [...]
valid_time: <optional instant or interval>
provenance: <optional source and observed-at>
```

Deterministic validation can check the owner, allowed knowledge kind, required
fields, dates, terminology, link targets, and forbidden session framing. Duplicate
or contradictory meaning requires retrieval and semantic comparison, so it should
produce a review flag rather than an automatic rejection. This preserves the
existing approval gate while making its reasoning inspectable.

### 4. Model provenance and time only where they affect meaning

PROV-O distinguishes entities, activities, and agents and provides relations for
derivation, attribution, primary source, revision, generation, and invalidation.
This supports retaining provenance separately from final prose instead of adding
"the user said" or "this session established" to every page. Durable provenance is
most useful for external claims, quotations, uncertain or contested facts, and
derived summaries. [W3C PROV-O Recommendation](https://www.w3.org/TR/prov-o/)

OWL-Time distinguishes instants, intervals, temporal positions, and relations
between intervals. The KB does not need that ontology today, but it should preserve
the underlying distinction between record time and valid time: when Capture learned
something is not necessarily when it became or remained true. A minimal form is
`observed_at` plus optional `valid_from`, `valid_until`, or visible `as of` wording.
[W3C Time Ontology in OWL](https://www.w3.org/TR/owl-time/)

## Formatting model stress test

### Result

The proposed defaults are directionally sound, but a rigid mapping from knowledge
kind to visual form would be too strong. The better model has two passes:

1. **Knowledge kind constrains semantics**: voice, tense, normative force,
   required context, and what must not be conflated.
2. **The relationship among content selects presentation**: prose, bullets,
   numbers, a term list, or a table.

DITA supports this distinction. It gives concept, task, and reference content
different semantic structures, but a concept body can still contain paragraphs,
lists, tables, sections, and examples. Its task model distinguishes ordered steps,
unordered steps, and informal procedural prose; it also separates a one-sentence
command from supporting information. A type therefore narrows valid expression
without determining a single block format. [OASIS DITA concept topic](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/dita-concept-topic.html),
[OASIS DITA task elements](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/containers/task-elements.html)

Official documentation style systems make the presentation decision from the
relationship and cardinality of the content. Google uses numbers for significant
sequence, bullets for unordered peers, description lists for term-description
pairs, and tables for repeated items with multiple comparable properties.
Microsoft similarly reserves numbering for sequence or priority and warns against
using a table for a one-dimensional list. Both require parallel list items. This
is more precise than saying that every decision, rule, preference, event, or item
of evidence should be a bullet. [Google lists](https://developers.google.com/style/lists),
[Google tables](https://developers.google.com/style/tables),
[Microsoft lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists),
[Microsoft tables](https://learn.microsoft.com/en-us/style-guide/scannable-content/tables)

Diataxis reinforces purpose-before-form: reference should be neutral, factual,
succinct, and organized in predictable patterns, while explanation and instruction
serve different needs. Its four documentation modes are too coarse to replace the
KB's section kinds, however; they are an architecture for user needs, not a
fine-grained assertion model. [Diataxis reference](https://diataxis.fr/reference/)

The more formal alternatives are useful behind Capture, not as the human-facing
page form. Controlled-natural-language research describes a spectrum among
precision, expressiveness, naturalness, and simplicity rather than one optimal
language. RDF goes further by representing descriptions as subject-predicate-object
triples, and SHACL validates RDF data against separate shapes. Those approaches
offer explicit relations and deterministic validation, but making them the native
Notion surface would sacrifice compact explanation and impose identifiers,
predicates, and schemas on ordinary reading. Use their discipline in Capture's
internal assertion record and validation layer instead. [Kuhn, *A Survey and
Classification of Controlled Natural Languages*](https://aclanthology.org/J14-1005/),
[W3C RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/),
[W3C SHACL](https://www.w3.org/TR/shacl/)

### Recommended selector

| Content relationship | Default presentation |
| --- | --- |
| One assertion, definition, state, or tightly coupled explanation | Short prose. |
| Two or more independent peers with no meaningful order | Bulleted list with parallel items. |
| Actions whose order matters, or an explicitly ranked set | Numbered list. A procedure whose actions can occur in any order uses bullets instead. |
| Terms, options, or fields paired with definitions | Term-description list or compact labelled entries. |
| Repeated records with multiple comparable attributes | Table. Do not use a table for one row, one dimension, or long narrative cells. |
| A claim plus dependent rationale, qualifier, consequence, or evidence | Keep the dependent material adjacent in a paragraph or labelled mini-record; do not promote it to a peer assertion. |
| Examples | Separate from the governing rule or concept, but keep them adjacent when the connection would otherwise be lost. |
| External sources | Numbered `Citations` section at the end, matching OKF; preserve claim-to-source links when provenance matters. |

Applied to the current defaults, this means that concept, state, and direction
remain prose-first; decisions, rules, preferences, events, evidence, and open
items use bullets only when there are at least two independent peers; procedures
use numbers only when order matters; and schemas use tables only for genuinely
two-dimensional repeated data.

Replace **the shortest clear form wins** with the more testable rule:

> Use the least complex form that preserves meaning and makes the semantic
> relationships explicit.

Replace **one durable assertion per sentence or list item** with **one primary
claim, instruction, or question per sentence or list item**. This covers rules,
procedures, and open questions as well as declarative knowledge. It remains an
anti-conflation default, not a fragmentation requirement: a dependent qualifier,
uncertainty, rationale, consequence, or source may stay with its primary unit when
separating it would change or obscure the meaning. A single item is prose, not a
list.

### Failure modes to test in Capture drafts

- **Over-bulletization**: causal explanation becomes disconnected peer claims.
- **False sequence**: numbering implies order where none exists.
- **Table-shaped prose**: narrative is forced into cells or a one-row table.
- **Mixed semantic force**: one item combines a fact, preference, and decision.
- **Detached support**: evidence or a qualifier can no longer be matched to its
  claim.
- **Decorative structure**: a heading, list, or table exists with only one item or
  because a template expected it.
- **Artificial atomization**: brevity removes the subject, scope, uncertainty,
  date, or rationale needed to interpret an assertion.

No alternative reviewed justifies rigid page profiles or a graph-first rewrite.
The concrete recommendation is to keep kind-driven defaults as authoring hints,
add the relation-driven selector above, and validate drafts for both semantic kind
and presentation choice. This is also compatible with OKF, which recommends
structural Markdown but leaves body sections flexible and specifies numbered
citations for externally sourced claims. [OKF v0.1 body and citations](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/d44368c15e38e7c92481c5992e4f9b5b421a801d/okf/SPEC.md#42-body)

## OKF assessment

### What it contributes

OKF defines a portable bundle of Markdown concept documents with YAML frontmatter,
hierarchy, cross-links, optional indexes for progressive disclosure, optional logs,
and citations. It deliberately mixes a few queryable fields with human-readable
body content. Those principles align with this repo's provider-agnostic stance and
the requirement that the same knowledge remain explorable by humans and agents.
[OKF v0.1 sections 3-8](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/d44368c15e38e7c92481c5992e4f9b5b421a801d/okf/SPEC.md#3-bundle-structure)

Notion now exposes page content through an enhanced-Markdown API as well as its
block API, while page properties remain separately typed values. That makes a
read-only Notion-to-OKF exporter plausible without changing the source of record.
It does not establish lossless round-tripping: the exporter must still define how
Notion page identity, properties, hierarchy, relations, and block semantics map to
OKF frontmatter and Markdown. [Notion Markdown API](https://developers.notion.com/guides/data-apis/working-with-markdown-content),
[Notion page properties](https://developers.notion.com/reference/page-property-values)

### What it does not solve

- `type` is the only required concept field, and values are not centrally
  registered.
- The Markdown body has no required sections.
- Link meaning lives in surrounding prose; graph edges are untyped.
- Unknown types, unknown fields, broken links, and absent indexes must be tolerated.
- A concept ID is its file path, so a Notion exporter needs its own stable mapping
  if page hierarchy or titles change.
- Storage, serving, domain schemas, and access control are outside the format's
  scope.

These are intentional properties of a minimal interchange format, not defects.
They are also why adopting OKF before defining the KB's own semantic contract would
standardize the envelope while leaving the current inconsistency untouched.
[OKF v0.1 sections 1, 4, 5, and 9](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/d44368c15e38e7c92481c5992e4f9b5b421a801d/okf/SPEC.md#1-motivation)

## Recommended sequence

### Now: improve Capture without changing the KB platform

1. Add the knowledge-kind vocabulary and controlled-authoring rules to the repo's
   KB conventions.
2. Make Capture classify each proposed unit before drafting prose.
3. Add a preflight checklist to the HTML approval draft: canonical owner,
   deduplication check, knowledge kind, terminology, temporality, provenance need,
   and clarity.
4. Keep semantic kinds mostly invisible in the final human interface; expose a
   property or heading only when it improves retrieval or disambiguation.
5. Run any future inconsistency audit read-only first, report findings by rule, and
   require the existing exact-write approval flow for repairs.

### Next: make the contract testable

Define the provider-neutral Capture record and deterministic validators. Pilot it
on recent captures and measure disagreements: wrong owner, duplicated assertion,
wrong semantic force, vague time, terminology drift, and unnecessary prose. Revise
the vocabulary from observed failures before adding more metadata.

### Later: prototype interchange

Build a read-only Notion-to-OKF export spike for a small, non-sensitive slice. Map
Notion pages to stable export IDs, map knowledge kinds to OKF `type` or a producer
extension, emit canonical-owner links, and run the OKF conformance checks. Do not
make it bidirectional or move the source of record until OKF matures beyond its
draft starting point and the export can preserve the semantics that matter.

The short judgment is: **adopt OKF's constraints now; adopt OKF itself later, as an
adapter rather than as the KB.**

## Full-contract research stress test (2026-07-12)

### Verdict

The accepted contract is a strong basis for Capture, but it should be adopted with
six amendments below. The standards review supports typed, modular content,
canonical terminology, explicit validation results, selective human-visible
metadata, and a human approval boundary. The strongest contrary evidence concerns
**destructive consolidation**: recent agent-memory research finds that repeated LLM
rewrites can omit, corrupt, or hallucinate durable memory, and that retaining raw
evidence and previous temporal states can outperform eager overwrite.

The result is a two-layer rule:

> Reconcile the active canonical view; preserve the evidence and revision trail
> from which that view was derived.

This section supersedes earlier provisional taxonomies in this note where they
conflict with the contract accepted during grilling.

### Maturity: raw at ingestion, not raw by default in the active KB

The proposed change is correct **for ingestion** and counterproductive **as the
default state of approved canonical content**.

- `Raw` means unassessed source material or an unverified assertion. Every incoming
  item starts here before reconciliation. Raw material does not silently
  participate in ordinary retrieval or answers.
- `Developing` means reconciled and approved knowledge that is useful now but still
  has an explicit unresolved qualification or is expected to change.
- `Stable` means reconciled, approved, sufficiently supported for its intended use,
  and safe for ordinary reuse. It does not mean immutable, certain, timeless, or
  final.

Maturity is therefore an **editorial processing state**, not confidence,
truthfulness, volatility, lifecycle, or source authority. A volatile current state
can be stably recorded with valid-time metadata; a confident claim can still be raw
because it has not been reconciled. W3C's Data Quality Vocabulary treats quality as
multidimensional and dependent on fitness for purpose, rather than as one objective
scalar, which is why `Stable` must not absorb those other meanings. [W3C Data
Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/)

Capture should aim to **minimize unresolved Raw and maximize reusable Stable**, not
force every item to Stable. A Raw exception retained in the active KB needs an
owner, provenance, a reason for retention, and a next review or distillation
action. Otherwise it belongs in the evidence/revision layer or should not be
persisted. This preserves the invariant that active KB presence implies relevance
without treating unreviewed material as canonical truth.

Two recent results make the ingestion distinction important. A 2026 preprint found
that continuously consolidated LLM memories can degrade below a no-memory baseline
and that agents which preserved raw episodes by default doubled the accuracy of
forced-consolidation agents. Another 2026 preprint found omission, corruption, and
hallucination during memory transitions and improved results by verifying coverage,
preservation, and faithfulness at each transition. These are recent preprints, not
settled standards, but they directly test the failure mode Capture creates.
[Zhang et al., *Useful Memories Become Faulty When Continuously Updated by
LLMs*](https://arxiv.org/abs/2605.12978), [Yang et al., *TrustMem*](https://arxiv.org/abs/2606.25161)

### Required amendments

#### 1. Keep the axes distinct, but rename `Authority`

`Canonical` and `Adapter` describe **ownership of a meaning**, not the epistemic
authority or trustworthiness of a source. Call this axis `Ownership` (canonical by
default, adapter explicit) and keep source authority in provenance. `Type`,
`Ownership`, `Maturity`, and section `Kind` remain conceptually orthogonal, but the
validator may express dependencies among them; orthogonality must not mean that all
combinations are valid.

Canonical-by-default is safe only after the baseline audit has confirmed one owner.
During migration, ambiguous ownership is `Unresolved`, not silently `Canonical`.
After migration, the absence of an adapter marker can again mean canonical, provided
Capture checks for competing owners before every write.

#### 2. Treat the twelve Kinds as a versioned vocabulary, not heading inference

Keep the accepted twelve Kinds—`State`, `Direction`, `Decision`, `Rule`,
`Preference`, `Procedure`, `Event`, `Evidence`, `Open item`, `Schema`, `Example`,
and `Citation`—as the initial registry. Give each a stable identifier, definition,
semantic-force rules, and registered human-facing heading labels. Flexible headings
remain useful for people, but an agent must not infer Kind from arbitrary heading
text alone. SKOS supports one preferred label per language plus distinct alternate
and hidden labels; aliases aid retrieval but do not replace stable concept identity.
[W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)

There is still no evidence that these exact twelve Kinds are complete. Add or merge
a Kind only after repeated real captures cannot be represented without ambiguity.
No rigid page profile is required, but Kind-specific constraints are appropriate:
an Event needs an absolute temporal anchor when known; a Rule needs scope and
normative force; a sourced claim needs an evidence link. DITA's current OASIS
standard supports this balance of typed topics, specialization, and flexible content
structures. [OASIS DITA 1.3](https://www.oasis-open.org/standard/ditav1-3/)

The three ordering invariants survive with one precedence rule: **claim-to-qualifier,
rationale, and evidence adjacency overrides global section order**. Citations may
remain last, but inline markers must preserve claim-to-source correspondence. The
one-primary-claim rule also remains an anti-conflation default, not a requirement to
split away necessary subject, scope, uncertainty, time, or rationale.

#### 3. Reconcile the active view without destroying history

`Reconcile, do not merely append` remains the correct authoring rule for the
human-facing canonical page. It must not mean destructive storage. Every accepted
transition should retain the previous revision, exact diff, source, observation
time, and explicit `supersedes`, `revises`, or `invalidates` relation where meaning
changed. PROV-O distinguishes revisions and invalidation; OKF itself recommends git
history and permits update logs. [W3C PROV-O](https://www.w3.org/TR/prov-o/), [OKF
v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)

This is not theoretical. A peer-reviewed ACL 2026 memory system reports a 14–25
percentage-point temporal-query advantage for append-only event history over eager
merge/overwrite comparators and attributes the gap to preserved superseded facts and
temporal provenance. That result does not require the KB interface to become an
append-only log; it requires the audit/evidence layer to remain reconstructable.
[APEX-MEM, ACL 2026](https://aclanthology.org/2026.acl-long.749/)

Accordingly, `presence implies relevance` applies to **active browsable pages**, not
to the underlying audit trail. Delete an irrelevant active page only after unique
durable content is migrated, inbound links are rebound, and deletion or invalidation
is recoverable from version history. This avoids archive filters in the human
interface without erasing provenance or breaking stable references.

#### 4. Make provenance and time selectively visible but universally auditable

Keep visible dates and citations selective. Behind the page, every mutation should
retain source, capture time, actor, affected owner, and revision identity. Every
State should retain an observation time internally; use visible `as of` wording only
when volatility changes interpretation. Valid time and capture time remain distinct.
OWL-Time explicitly models instants and intervals but does not itself resolve valid
time, so the project must define `observed_at`, `valid_from`, and `valid_until`
semantics. [W3C Time Ontology in OWL](https://www.w3.org/TR/owl-time/)

The approval artifact is sufficient only if it is durably retained and linked to
the resulting revision. Otherwise provenance disappears as soon as the task ends.
Canonical terminology likewise needs scope: owner-local aliases work for local
language, while cross-cutting terms need one vocabulary owner and language-aware
preferred labels.

#### 5. Turn the quality checklist into an evidence-bearing transition gate

Keep the explicit approval gate, but do not let a row of unexplained `Pass` values
create false confidence. Each check needs its checked scope and evidence. Separate
deterministic results (allowed Kind, date syntax, link resolution) from semantic
judgments (correct owner, contradiction, duplication, faithful compression). Use
`Pass`, `Flag`, `Not checked`, and `Not applicable`; unresolved ownership,
contradiction, material omission, or unsupported assertion blocks the write.

The approval preview should show source evidence, before/after content, deletions,
and the transition checks for coverage, preservation, and faithfulness. Human
approval is a control, not proof of correctness. NIST warns that people can over-rely
on apparently high-quality generative output (automation bias) and defines
high-integrity information as distinguishing fact, opinion, and inference while
exposing uncertainty, evidence, chain of custody, and likely expiry. [NIST AI
600-1](https://doi.org/10.6028/NIST.AI.600-1)

#### 6. Make the audit reproducible and the migration continuously checked

Keep the full read-only audit followed by area-batched refactoring, but define
`full` through a coverage manifest: audited page IDs, inaccessible or partial
records, audit timestamp, rule/version used, and unresolved exceptions. A one-time
audit goes stale while batches are being written. Before each batch, re-read its
targets and inbound/outbound references; after writing, read back the result and run
local checks; after all batches, rerun the global audit. Preserve a rollback path and
stable page identities throughout.

SHACL's stable Recommendation supports immutable input graphs and explicit
validation reports, which is a useful model for read-only audit. SHACL 1.2 Core is
under active development in 2026 but remains a Working Draft, so implementation
should target the 2017 Recommendation's stable concepts and monitor—not depend
on—the draft. [W3C SHACL Recommendation](https://www.w3.org/TR/shacl/), [SHACL 1.2
Core Working Draft](https://www.w3.org/TR/shacl12-core/)

### What survives unchanged

- The least complex presentation that preserves semantic relationships.
- Short description first; current/actionable content before supporting history;
  open questions and citations last, subject to evidence adjacency.
- No empty sections, universal page profiles, or decorative structure.
- Explicit semantic force, with `must`, `should`, and `may` reserved for rules.
  Rules also need a named scope; `will` must not ambiguously mix prediction and
  commitment.
- Canonical terminology and retrieval aliases, with ambiguity flagged rather than
  silently merged.
- A read-only audit before writes and small approval-gated migration batches.
- OKF readiness now and a read-only adapter later.

### OKF boundary

OKF remains a suitable future envelope, not the semantic contract. As of this
review, the live specification is still **Version 0.1 — Draft**; it requires only
`type`, permits producer extensions, leaves body sections optional, represents
links as untyped relationships, tolerates broken links, and uses file paths as
concept IDs. The adapter should therefore pin an OKF version/commit, preserve
unknown fields, use a stable mapping derived from Notion page IDs rather than
titles or hierarchy, and export section Kinds through a documented producer
extension rather than overloading page `type`. The KB's validator should remain
stricter than OKF conformance. [OKF v0.1
specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)

### Confidence and limitations

Confidence is **high** that the amendments follow current W3C/OASIS/NIST standards
and **medium** that they optimize this personal KB. The most directly relevant
agent-memory evidence is very recent: APEX-MEM is peer reviewed, while TrustMem and
the continuous-consolidation study are preprints and may change. Those systems
evaluate conversational or task memory, not a human-curated Notion KB. No reviewed
standard proves that the twelve-Kind vocabulary is optimal, that the headings will
remain legible at KB scale, or that the quality gate prevents semantic duplication.
Those claims require a measured pilot and the planned full audit. OKF is still a
draft and may change incompatibly before an adapter is implemented.
