---
status: accepted
---

# Social Compose models audience state, not platform reads

> **Superseded in part** by [ADR 0006](0006-write-authority-is-mandate-scoped.md) and
> [ADR 0008](0008-social-and-portfolio-sweeps-under-mandate-scoped-capture.md): the
> "stays draft-only" claim below holds only for the sink-publish half (draft only; do
> not post). Social Compose now first-party-captures `point-of-view` and
> `published-social-context` within its mandate, through `/capture` approval.
>
> **Superseded in part** by
> [ADR 0011](0011-social-scheduling-uses-capability-bound-live-sources.md):
> `published-social-context` is now a semantic audience and argument ledger rather
> than a publication mirror, and live eligible slots replace the per-run volume
> target as the capacity authority.

Social Compose keeps a model of what a public audience already knows and of the
user's persona **in the KB**, and drafts a content mix of project/proof and topical
posts. Two new endpoints carry this: `published-social-context` (a per-platform
ledger of what has been published and which concepts and projects have been publicly
introduced on each channel) and `point-of-view` (the user's incrementally-built
public persona — recorded stances, opinions, and recurring themes). The automation
reads both and stays draft-only; the surfaces are maintained through `/capture`.

Audience state and persona are memory. Per
[ADR 0001](0001-source-of-record-not-runtime.md), memory lives in the provider, so
these belong in the KB, not in the automation and not in an external service.

## Context

Earlier runs mined only project progress. Drafts leaked internal vocabulary — for
example "the KB is the memory" to an audience never introduced to the KB — and
handled concepts inconsistently across platforms, introducing a project on one
channel while assuming it on another. The root cause was that the automation had no
model of audience state, and no source for topical, non-project content.

## Considered options

- **Read the user's own X/LinkedIn timelines through the platform APIs** to
  reconstruct what has been said. Rejected as the mechanism: X timeline reads are
  paywalled behind a paid tier, LinkedIn personal-post reads are effectively
  unavailable to individuals, and it makes a personal automation depend on fragile,
  costly external access. A one-time export or manual seed may bootstrap the ledger;
  ongoing dependence may not.
- **Hardcode "introduce jargon on first use" plus a volume and content-mix target
  into the prompt.** Rejected per [ADR 0002](0002-personal-specifics-are-bindings.md):
  platform strategy, volume, and content mix are bindings owned by
  `social-rules-of-engagement`, not spec.
- **Let the automation invent topical opinions.** Rejected: it turns vibes into
  facts and speaks for the user. Topical angles are grounded in `point-of-view` or
  `identity`; absent a recorded stance, the automation surfaces the hook at the
  approval gate and asks for the take.

## Consequences

- The preamble endpoint vocabulary gains `point-of-view` and
  `published-social-context`; setup binds them like any other endpoint.
- `social-rules-of-engagement` owns the per-run volume target, the project/topical
  content mix, and the self-contained / introduce-on-first-use rule as tunable
  dials.
- Social Compose stays draft-only: new takes given at the gate become
  `point-of-view` capture candidates handed to `/capture`, and post-publication
  ledger updates are `/capture` handoffs too, preserving "write to the KB only
  through capture approval." (Reframed by ADR 0006/0008: these are now Social Compose's own
  first-party-capture mandate, not deferred handoffs; the `/capture`-approval
  invariant is unchanged.)
- The persona and the audience ledger fill in over time, so drafts grow more
  continuous and the topical branch grows more autonomous as the surfaces mature.
