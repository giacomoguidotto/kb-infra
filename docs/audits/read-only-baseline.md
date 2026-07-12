# Reproducible read-only audit baseline

A baseline audit is a provider-neutral compilation of two read-only snapshots of
the same Knowledge Bank scope. Live page content and provider identifiers stay in
gitignored `local/audits/`; the repository commits only this contract, compiler,
and non-personal test fixtures.

## Snapshot envelope

Each snapshot is JSON with this shape:

```json
{
  "schema_version": 1,
  "contract": {
    "conventions": "docs/knowledge-bank-conventions.md",
    "revision": "<git commit or tag>",
    "kind_registry_version": 1
  },
  "audit_started_at": "2026-07-12T12:00:00Z",
  "compiled_at": "2026-07-12T12:10:00Z",
  "discovery": {
    "complete": false,
    "methods": ["provider database enumeration", "relation closure"],
    "exceptions": ["why completeness could not be proved"]
  },
  "unresolved_exceptions": [],
  "records": [
    {
      "id": "stable-provider-id",
      "title": "Example",
      "access": "full",
      "exceptions": [],
      "properties": {},
      "content": "Complete provider-rendered content",
      "outbound_reference_ids": [],
      "canonical_owner_ids": [],
      "kinds": [],
      "revision_evidence": null,
      "assessments": [
        {
          "area": "duplication",
          "status": "pass",
          "code": "duplicate-meaning-review",
          "evidence": "Compared the page with its linked owners."
        }
      ]
    }
  ]
}
```

`access` is `full`, `partial`, or `inaccessible`. Include a record even when only
its stable identity is known. `assessments` carries evidence-backed semantic
checks that a provider adapter or reviewer can establish but the generic compiler
cannot infer. Its `area` must be one of the compiler's classified areas and its
`status` is `pass`, `flag`, `not-checked`, or `not-applicable`. The compiler reports
unassessed semantic records instead of presenting deterministic proxies as full
semantic coverage.

## Read-only run

1. Pin the current conventions revision and Kind-registry version.
2. Enumerate every provider container in scope. Record blocked containers,
   inaccessible identities, pagination limits, and possible orphan records as
   discovery exceptions; do not reinterpret a search sample as full coverage.
3. Fetch every discovered page completely. Preserve stable provider IDs, access
   state, properties, content, and explicit inbound/outbound relation evidence.
4. Save the initial snapshot below `local/audits/<audit-id>/initial.json`.
5. Re-read every discovered identity after the first pass and save the same
   envelope as `recheck.json`. Do not rely on a finding whose target changed;
   classify the drift and use the recheck fingerprint as the finding basis. If a
   recheck is partial, inaccessible, or absent, do not classify the stale initial
   content.
6. Compile the manifest and findings:

   ```sh
   python3 scripts/build-audit-baseline.py \
     --initial local/audits/<audit-id>/initial.json \
     --recheck local/audits/<audit-id>/recheck.json \
     --output local/audits/<audit-id>/baseline
   ```

7. Verify `manifest.json` records contract revision, audit times, stable page
   identities, partial/inaccessible records, unresolved exceptions, reference
   coverage, and drift rechecks. Verify `findings.json` indexes Type, Ownership,
   Maturity, Kind, duplication, relevance, terminology, time, provenance,
   formatting, inbound references, and outbound references even when an area has
   no findings.

The compiler performs no network calls and exposes no write operation. Provider
reads happen before compilation; any later repair remains a separate exact-draft,
approval-gated Capture workflow.

## Baseline-to-frontier contract

A compiled baseline is discovery evidence, not a migration plan. Build the live
migration frontier from the record-level findings and relationship graph in the
matching `manifest.json` and `findings.json`; aggregate counts or a narrative audit
summary are not sufficient inputs.

Before drafting tickets, confirm that the baseline pair has matching hashes and
contract versions, every readable record has complete semantic assessments, and
all partial access, discovery limits, unresolved exceptions, and concurrent drift
remain explicit. A changed, unverifiable, or newly discovered target must be read
again before it can enter an approval draft.

Classify the record-level work in this order:

1. **Global taxonomy decisions.** Settle provider-neutral decisions that every
   area must share, such as canonical Type vocabulary, representation of
   Ownership, Maturity, Kind and Revision Evidence, and the rules for redirects
   and safe deletion.
2. **Cross-area Ownership conflicts.** Resolve competing canonical owners and
   decide which surfaces become Adapters before an area-local ticket can depend on
   those owners.
3. **Area-local reconciliation batches.** Select one bounded owner subgraph and
   reconcile all applicable findings end to end. Split the work again whenever
   one fresh agent context or one reviewable Approval Draft cannot hold it. Do not
   leave a ticket for all remaining pages.
4. **Final global re-audit.** Block this ticket on every reconciliation batch and
   regenerate the full two-pass baseline. Compare coverage, unresolved exceptions,
   relationships, semantic assessments, and concurrent drift with the starting
   baseline without treating an access limitation as success.

Every write-bearing ticket must require one approval-batched Capture run that:

- re-reads every target plus its inbound and outbound references immediately
  before drafting, and stops for a refreshed draft when any fingerprint drifted;
- shows exact before and after content, semantic decisions, deletions, preserved
  references, and Revision Evidence before the first write;
- applies only the approved batch, preserves stable identities, Revision Evidence,
  and a rollback path, and deletes only after canonical ownership, replacements or
  redirects, and inbound references are resolved;
- reads back every mutation and deletion, verifies the retained Revision Evidence,
  and reruns the bounded area audit before reporting completion.

The issue tracker is the live frontier source of truth. Before publication, present
the exact ticket tree and blocking graph for approval. After approval, publish in
dependency order so every blocker references a real ticket. Tracker issues name
the provider-neutral area and selection rule; provider identifiers, personal page
content, manifests, and findings stay under gitignored `local/audits/`. Commit this
operating contract, not a duplicate inventory of issue bodies.
