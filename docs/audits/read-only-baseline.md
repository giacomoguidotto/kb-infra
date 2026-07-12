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
