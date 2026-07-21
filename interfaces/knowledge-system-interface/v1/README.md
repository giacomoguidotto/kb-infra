# `knowledge-system-interface/v1`

This package is the provider-blind boundary between the Knowledge System and an
automation. Knowledge setup installs one copy in the harness. Consumers name
roles and intent; only the Knowledge System resolves providers, locations, owners,
relations, and traversal.

The interface version is independent from the repository release. Additive roles
and optional fields are compatible within v1. A changed role meaning, result state,
approval boundary, visibility rule, evidence guarantee, provenance guarantee, or
mandate guarantee requires a new interface major.

## Endpoint Registry

[`endpoint-registry.json`](endpoint-registry.json) is the declarative owner of role
semantics. Each entry defines:

- stable role meaning and result shape;
- visibility and intended-use rules;
- bounded canonical-owner and evidence traversal;
- required provenance and stopping conditions;
- compatibility status.

Registry revision is distinct from the interface major. Consumers may require an
active role but must not interpret provider structure or registry internals.

## Lookup Request

An automation sends a document matching
[`request.schema.json`](request.schema.json). It contains only:

- interface major, caller, and one dependent capability;
- objective plus required and optional endpoint roles;
- intended-use boundary and evidence/provenance requirements;
- a declarative Knowledge Mandate and clarification permission.

Requests must not name a provider, page, location, traversal instruction, cached
fact, or project inventory. The schema rejects undeclared fields.

The Knowledge System validates roles against the registry, follows only permitted
owner and evidence relations, and stops when every required role is resolved or a
registry stopping condition applies.

## Knowledge Context Snapshot

Automation lookup returns a JSON-compatible document matching
[`snapshot.schema.json`](snapshot.schema.json). Use native structured output when
the harness supports it and fenced JSON otherwise. Interactive `/lookup` renders
the same meanings as concise Markdown.

Each role result has exactly one state:

- `value`: the current canonical owner and evidence establish the returned claims;
- `absent`: the canonical owner explicitly establishes that no applicable value
  exists;
- `unresolved`: ownership, evidence, freshness, access, or revision uncertainty
  prevents a safe answer.

A search miss is never `absent`. Visibility is independent from state. Every claim
and established absence carries evidence and provenance. Unresolved results carry
machine-readable reasons and attempted provenance, never guesses.

`snapshot_token` is opaque to consumers. It covers the exact owners, relations,
evidence revisions, and registry revision used for the snapshot. Consumers may only
return the token for validation, never parse, compare, derive, or cache meaning from
it.

If the covered state drifts during traversal, discard the partial result and rebuild
once. If drift persists, return the affected role as `unresolved` with reason
`persistent_drift`. Block only `request.capability`; unrelated capabilities and
independent requests remain usable.

## Semantic Capture

An automation proposes durable meaning with a document matching
[`capture-request.schema.json`](capture-request.schema.json). It supplies a mandate,
target role, meaning, visibility, evidence, optional source snapshot token, and
rationale. It never supplies a provider write or concrete target location.

The Knowledge System resolves the canonical owner, deduplicates, and rereads. A
safe proposal returns an exact draft matching
[`capture-draft.schema.json`](capture-draft.schema.json). Every draft names its
complete writes in application order, exact before and after state, removal
consequences, sources, reasons, uncertainty, and read-back checks. Array position is
the sole operation order.

When mandate, ownership, evidence, freshness, access, or revision state prevents a
safe draft, return a response matching
[`capture-blocked.schema.json`](capture-blocked.schema.json). A blocked response has
no operations or approval prompt. See
[`examples/capture-blocked.json`](examples/capture-blocked.json).

`drafted` is not write authority. Applying a draft requires the exact `/capture`
approval prompt in the schema and an explicit approval of the latest draft. The
Knowledge System rereads every determining target and relation immediately before
writing. Any drift invalidates approval and requires a new draft. It applies only
the approved operations, then reads back every result. Setup and automation calls
never bypass this boundary.
