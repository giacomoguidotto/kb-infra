# Semantic authoring for Capture, and where OKF fits

Updated: 2026-07-13

## Conclusion

Use a lightweight semantic authoring model now; treat OKF as a future read-only
adapter.

The evidence supports:

- one canonical owner and canonical term per meaning;
- concise controlled authoring without a formal controlled language;
- independent page Type, meaning Ownership, editorial Maturity, and section Kind;
- flexible pages with one dominant Kind per section;
- presentation chosen by relationships, not Kind alone;
- reconciled active content with recoverable revisions;
- human approval backed by live reads and read-back.

It does not support rigid page profiles, graph-first authoring, machine-generated
semantic paperwork, or OKF as the KB's native model. The accepted operational rules
live in [Knowledge Bank Conventions](../knowledge-bank-conventions.md).

## Evidence

### Typed content without rigid pages

DITA separates concepts, tasks, and reference material while allowing varied block
structures inside each type. It also distinguishes ordered, unordered, and informal
procedures. A semantic type can therefore constrain meaning without fixing one
visual form. [OASIS DITA concept topic](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/archSpec/technicalContent/dita-concept-topic.html),
[OASIS DITA task elements](https://docs.oasis-open.org/dita/dita/v1.3/os/part2-tech-content/langRef/containers/task-elements.html)

Diataxis likewise separates documentation by user need rather than prescribing one
page template. Its four modes are useful at page scale but too coarse to replace
section Kinds. [Diataxis](https://diataxis.fr/)

SKOS provides the useful vocabulary discipline: one preferred label per language,
alternate labels for retrieval, and explicit relationships. The KB can adopt those
principles without becoming RDF. [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)

### Controlled authoring without formalization

Controlled-natural-language research describes a trade-off among precision,
expressiveness, naturalness, and simplicity; there is no universally best point.
Attempto Controlled English is valuable when deterministic logical interpretation
is the goal, but it is more restrictive than a browsable personal KB needs.
[Kuhn, *A Survey and Classification of Controlled Natural Languages*](https://aclanthology.org/J14-1005/),
[Fuchs and Schwitter, *Attempto Controlled English*](https://arxiv.org/abs/cmp-lg/9603003)

ASD-STE100 and official documentation style guides support the practical middle:
one subject, direct verbs, explicit terminology, parallel lists, and short sentences
that preserve necessary qualifiers. These are authoring controls, not an executable
grammar. [ASD-STE100](https://www.asd-ste100.org/),
[Google developer style guide](https://developers.google.com/style),
[Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)

The resulting rule is:

> Use the least complex form that preserves meaning and makes semantic relationships
> explicit.

### Presentation follows relationships

Google and Microsoft recommend numbers for sequence, bullets for unordered peers,
description lists for term-definition pairs, and tables for repeated comparable
records. Both warn against using tables for one-dimensional content. Presentation
therefore depends on relationship and cardinality, not a fixed Kind-to-block map.
[Google lists](https://developers.google.com/style/lists),
[Google tables](https://developers.google.com/style/tables),
[Microsoft lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists),
[Microsoft tables](https://learn.microsoft.com/en-us/style-guide/scannable-content/tables)

| Content relationship | Default presentation |
| --- | --- |
| One assertion or tightly coupled explanation | Short prose |
| Two or more unordered peers | Parallel bullets |
| Ordered actions or ranking | Numbered list |
| Terms paired with definitions | Labelled entries or description list |
| Repeated records with comparable fields | Table |
| Claim plus qualifier, rationale, or evidence | Keep adjacent |
| Example and governing rule | Separate but adjacent |

This avoids over-bulletization, false sequence, table-shaped prose, detached
evidence, and decorative structure.

### Provenance, time, and non-destructive reconciliation

PROV-O distinguishes derivation, attribution, revision, generation, and
invalidation. OWL-Time distinguishes instants, intervals, and temporal positions.
The KB need not implement either ontology, but it should keep observation, event,
validity, and capture times distinct and preserve recoverable revision evidence.
[W3C PROV-O](https://www.w3.org/TR/prov-o/),
[W3C Time Ontology](https://www.w3.org/TR/owl-time/)

Recent agent-memory results reinforce the risk of eager consolidation. APEX-MEM
reports stronger temporal queries from preserved event history; recent preprints
report omission, corruption, and accuracy loss during repeated LLM memory rewrites.
These systems are not Notion KBs, but they directly support reconciling the active
view without destroying raw evidence or prior states.
[APEX-MEM, ACL 2026](https://aclanthology.org/2026.acl-long.749/),
[Zhang et al., *Useful Memories Become Faulty When Continuously Updated by LLMs*](https://arxiv.org/abs/2605.12978),
[Yang et al., *TrustMem*](https://arxiv.org/abs/2606.25161)

### Validation has a narrow role

SHACL shows how deterministic shapes can check data separately from content. It
does not prove that prose has the right owner, preserves meaning, or avoids semantic
duplication. Those are retrieval and judgment problems. [W3C SHACL](https://www.w3.org/TR/shacl/)

NIST also warns about automation bias around fluent generative output. A legible
approval surface should expose uncertainty, evidence, and provenance, but a table of
machine-generated `Pass` values is not correctness evidence.
[NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1)

Add executable validation only when repeated failures reveal a
provider-independent condition that code can actually decide.

## OKF Assessment

Open Knowledge Format contributes a portable package, content metadata, document
types, Markdown bodies, typed metadata records, relationships, citations, update
logs, and conformance checks. Those are useful constraints for future interchange.

It does not solve canonical ownership, semantic duplication, section Kinds,
Maturity, source trust, editorial quality, or the human approval workflow. As of
this review, OKF v0.1 is still a draft; body sections are flexible, links may be
broken, and file paths act as concept identifiers.
[OKF specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md),
[Google Cloud introduction](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

A future adapter should:

- remain read-only until a round trip can preserve meaning;
- pin an OKF version or commit;
- derive export IDs from stable provider page IDs, not titles or hierarchy;
- preserve unknown fields;
- export section Kinds through a documented producer extension;
- keep native KB authoring and approval stricter than OKF conformance.

## Pilot Result

The first executable semantic-contract pilot on 2026-07-13 was disproportionate.
Six live provider operations produced sixteen transition records, sixteen validation
reports, duplicated contracts, a large serialized approval artifact, and more than
four thousand repository lines. The machinery checked representation shape but did
not prove the semantic judgments that mattered.

The retained safeguards are smaller and stronger:

1. Read the live target, schema, likely owners, and relevant relations.
2. Reconcile the smallest coherent change under the conventions.
3. Show every exact write in a human-readable HTML draft.
4. Require fresh explicit approval.
5. Re-read for drift immediately before writing.
6. Apply exactly and read back every result.

Private audit snapshots may guide a migration, but they remain disposable evidence
under gitignored `local/`; the repo needs no compiler or executable semantic record.

## Confidence And Limits

Confidence is high that the model follows established documentation, vocabulary,
provenance, and validation principles. Confidence is medium that the twelve Kinds
are optimal for this personal KB. The recent agent-memory evidence is partly
preprint research and may change, and OKF may change incompatibly while it remains a
draft. Real captures and the full KB audit—not more schema—should drive future
revision.
