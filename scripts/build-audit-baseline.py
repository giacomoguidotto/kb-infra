#!/usr/bin/env python3
"""Compile two read-only KB snapshots into a reproducible audit baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

AREAS = (
    "type",
    "ownership",
    "maturity",
    "kind",
    "duplication",
    "relevance",
    "terminology",
    "time",
    "provenance",
    "formatting",
    "inbound-references",
    "outbound-references",
    "coverage",
    "concurrent-drift",
)
KINDS = {
    "state",
    "direction",
    "decision",
    "rule",
    "preference",
    "procedure",
    "event",
    "evidence",
    "open-item",
    "schema",
    "example",
    "citation",
}
OWNERSHIP = {"Canonical", "Adapter", "Unresolved"}
MATURITY = {"Raw", "Developing", "Stable"}
SEMANTIC_AREAS = {
    "ownership",
    "maturity",
    "kind",
    "duplication",
    "relevance",
    "terminology",
    "time",
    "provenance",
    "formatting",
}
ASSESSMENT_STATUSES = {"pass", "flag", "not-checked", "not-applicable"}
RELATIVE_TIME = re.compile(
    r"\b(today|tomorrow|yesterday|currently|recently|last\s+(?:week|month|year)|"
    r"next\s+(?:week|month|year))\b",
    re.IGNORECASE,
)
FOLLOW_UP = re.compile(r"Follow-up: ask again on (\d{4}-\d{2}-\d{2}):", re.IGNORECASE)


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(record: dict[str, Any]) -> str | None:
    if record.get("access") != "full":
        return None
    material = {
        "title": record.get("title", ""),
        "properties": record.get("properties", {}),
        "content": record.get("content", ""),
        "outbound_reference_ids": sorted(set(record.get("outbound_reference_ids", []))),
    }
    return hashlib.sha256(stable_json(material).encode()).hexdigest()


def finding_id(area: str, page_id: str | None, code: str, source: str) -> str:
    key = f"{source}|{area}|{page_id or 'audit'}|{code}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def normalized_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().casefold())


def index_records(snapshot: dict[str, Any], label: str) -> dict[str, dict[str, Any]]:
    if snapshot.get("schema_version") != 1:
        raise ValueError(f"{label} snapshot must use schema version 1")
    records: dict[str, dict[str, Any]] = {}
    for record in snapshot.get("records", []):
        page_id = record.get("id")
        if not page_id:
            raise ValueError(f"{label} snapshot contains a record without a stable id")
        if page_id in records:
            raise ValueError(f"{label} snapshot contains duplicate stable id {page_id}")
        records[page_id] = record
    return records


def compile_baseline(initial: dict[str, Any], recheck: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if initial.get("contract") != recheck.get("contract"):
        raise ValueError("initial and recheck snapshots must pin the same contract")
    initial_records = index_records(initial, "initial")
    recheck_records = index_records(recheck, "recheck")
    all_ids = sorted(set(initial_records) | set(recheck_records))
    findings: list[dict[str, Any]] = []

    def add(
        area: str,
        page_id: str | None,
        code: str,
        severity: str,
        evidence: str,
        fingerprint: str | None = None,
        status: str = "flag",
        source: str = "deterministic",
    ) -> None:
        findings.append(
            {
                "id": finding_id(area, page_id, code, source),
                "area": area,
                "page_id": page_id,
                "code": code,
                "severity": severity,
                "status": status,
                "source": source,
                "evidence": evidence,
                "relies_on_sha256": fingerprint,
            }
        )

    inbound: dict[str, set[str]] = defaultdict(set)
    manifest_records: list[dict[str, Any]] = []
    current_records: dict[str, dict[str, Any]] = {}
    assessed_by_area: dict[str, set[str]] = defaultdict(set)
    for page_id in all_ids:
        before = initial_records.get(page_id)
        after = recheck_records.get(page_id)
        before_hash = content_hash(before) if before else None
        after_hash = content_hash(after) if after else None
        if before is None:
            drift = "appeared"
        elif after is None:
            drift = "recheck-unavailable"
        elif before.get("access") != "full" or after.get("access") != "full":
            drift = "unverifiable" if before.get("access") == after.get("access") else "access-changed"
        elif before_hash == after_hash:
            drift = "unchanged"
        else:
            drift = "changed"
        current = after or before
        assert current is not None
        current_access = after.get("access", "partial") if after else "inaccessible"
        if after and after.get("access") == "full":
            current_records[page_id] = after
        outbound = sorted(set(after.get("outbound_reference_ids", []))) if after and after.get("access") == "full" else []
        for target in outbound:
            inbound[target].add(page_id)
        manifest_records.append(
            {
                "id": page_id,
                "title": current.get("title"),
                "access": current_access,
                "initial_access": before.get("access") if before else None,
                "recheck_access": after.get("access") if after else None,
                "exceptions": sorted(
                    set((before or {}).get("exceptions", []))
                    | set((after or {}).get("exceptions", []))
                    | ({"Record was absent from the recheck snapshot."} if after is None else set())
                ),
                "initial_sha256": before_hash,
                "recheck_sha256": after_hash,
                "drift": drift,
                "outbound_reference_ids": outbound,
            }
        )
        if drift != "unchanged":
            add(
                "concurrent-drift",
                page_id,
                drift,
                "error" if drift == "recheck-unavailable" else "info" if drift == "unverifiable" else "warning",
                f"Initial and recheck snapshots classified this record as {drift}.",
                after_hash,
            )
        if current_access != "full":
            add("coverage", page_id, current_access, "error", f"Record access is {current_access}.")

    titles: dict[str, list[str]] = defaultdict(list)
    audit_date = datetime.fromisoformat(initial["audit_started_at"].replace("Z", "+00:00")).date()
    for page_id, record in sorted(current_records.items()):
        fingerprint = content_hash(record)
        props = record.get("properties", {})
        title = str(record.get("title", ""))
        content = str(record.get("content", ""))
        titles[normalized_title(title)].append(page_id)

        page_type = props.get("Type") or record.get("type")
        if not page_type:
            detail = "Legacy Class is present but the provider-defined Type mapping is unresolved." if props.get("Class") else "No provider-defined Type was captured."
            add("type", page_id, "missing-type", "warning", detail, fingerprint)

        ownership = props.get("Ownership") or props.get("Role")
        if ownership not in OWNERSHIP:
            code = "legacy-role" if ownership in {"Raw", "Archive"} else "missing-or-invalid-ownership"
            add("ownership", page_id, code, "error", f"Ownership resolves to {ownership!r}.", fingerprint)
        elif ownership == "Adapter" and not record.get("canonical_owner_ids"):
            add("ownership", page_id, "adapter-without-owner", "error", "Adapter has no captured canonical owner link.", fingerprint)

        maturity = props.get("Maturity") or record.get("maturity")
        if maturity not in MATURITY:
            add("maturity", page_id, "missing-or-invalid-maturity", "warning", f"Maturity resolves to {maturity!r}.", fingerprint)

        kinds = {str(kind).casefold().replace(" ", "-") for kind in record.get("kinds", [])}
        if not kinds:
            add("kind", page_id, "unclassified-content", "warning", "No explicit registered Kind was captured.", fingerprint)
        for kind in sorted(kinds - KINDS):
            add("kind", page_id, f"unknown-kind-{kind}", "error", f"Kind {kind!r} is not in registry version 1.", fingerprint)

        status = props.get("Status")
        if status == "Done" or ownership == "Archive":
            add("relevance", page_id, "inactive-page-present", "warning", f"Page remains present with Status={status!r} and Ownership={ownership!r}.", fingerprint)
        if title != title.strip():
            add("terminology", page_id, "title-surrounding-space", "warning", "Title has leading or trailing whitespace.", fingerprint)

        relative_terms = sorted({match.group(0).casefold() for match in RELATIVE_TIME.finditer(content)})
        if relative_terms:
            add("time", page_id, "relative-time", "warning", f"Relative time terms found: {', '.join(relative_terms)}.", fingerprint)
        for raw_date in FOLLOW_UP.findall(content):
            if datetime.fromisoformat(raw_date).date() <= audit_date:
                add("time", page_id, f"due-follow-up-{raw_date}", "warning", f"Follow-up marker is due as of {audit_date.isoformat()}.", fingerprint)

        if not record.get("revision_evidence"):
            add("provenance", page_id, "revision-evidence-unavailable", "warning", "No Revision Evidence was exposed by the read snapshot.", fingerprint)
        if "<empty-block/>" in content:
            add("formatting", page_id, "empty-block", "info", "Provider content contains an empty block.", fingerprint)

        for target in sorted(set(record.get("outbound_reference_ids", []))):
            if target == page_id:
                add("outbound-references", page_id, "self-reference", "info", "Page contains a self-reference.", fingerprint)
            elif target not in all_ids:
                add("outbound-references", page_id, f"unresolved-{target}", "error", f"Outbound target {target} is outside the coverage manifest.", fingerprint)

        for manual in record.get("assessments", []):
            area = manual.get("area")
            if area not in AREAS:
                raise ValueError(f"unknown assessment area {area!r} on {page_id}")
            status = manual.get("status", "flag")
            if status not in ASSESSMENT_STATUSES:
                raise ValueError(f"unknown assessment status {status!r} on {page_id}")
            if status != "not-checked":
                assessed_by_area[area].add(page_id)
            if status in {"flag", "not-checked"}:
                add(
                    area,
                    page_id,
                    manual["code"],
                    manual.get("severity", "warning"),
                    manual["evidence"],
                    fingerprint,
                    status,
                    "semantic-assessment",
                )

    for title, page_ids in sorted(titles.items()):
        if title and len(page_ids) > 1:
            for page_id in sorted(page_ids):
                add("duplication", page_id, f"duplicate-title-{hashlib.sha256(title.encode()).hexdigest()[:8]}", "warning", f"Normalized title is shared by {sorted(page_ids)}.", content_hash(current_records[page_id]))
                add("terminology", page_id, f"ambiguous-title-{hashlib.sha256(title.encode()).hexdigest()[:8]}", "warning", "Title is not unique in the audited scope.", content_hash(current_records[page_id]))

    for item in manifest_records:
        item["inbound_reference_ids"] = sorted(inbound.get(item["id"], set()))

    initial_discovery = initial.get("discovery", {})
    recheck_discovery = recheck.get("discovery", {})
    discovery = {
        "complete": bool(initial_discovery.get("complete", False)) and bool(recheck_discovery.get("complete", False)),
        "initial": initial_discovery,
        "recheck": recheck_discovery,
    }
    unresolved = sorted(
        set(initial_discovery.get("exceptions", []))
        | set(recheck_discovery.get("exceptions", []))
        | set(initial.get("unresolved_exceptions", []))
        | set(recheck.get("unresolved_exceptions", []))
    )
    if not discovery.get("complete", False):
        add("coverage", None, "discovery-not-proven-complete", "error", "Provider enumeration could not prove that no inaccessible or orphan records exist.")

    full_record_ids = set(current_records)
    semantic_coverage = {}
    for area in sorted(SEMANTIC_AREAS):
        assessed = assessed_by_area[area] & full_record_ids
        unassessed = full_record_ids - assessed
        semantic_coverage[area] = {
            "assessed_record_count": len(assessed),
            "unassessed_record_count": len(unassessed),
        }
        if unassessed:
            add(
                area,
                None,
                "semantic-assessment-incomplete",
                "warning",
                f"Semantic assessment is missing for {len(unassessed)} full records.",
                status="not-checked",
            )
    semantic_complete = all(item["unassessed_record_count"] == 0 for item in semantic_coverage.values())
    if not semantic_complete:
        incomplete_areas = ", ".join(
            area for area, item in sorted(semantic_coverage.items()) if item["unassessed_record_count"]
        )
        unresolved.append(f"Semantic assessments remain incomplete for: {incomplete_areas}.")

    access_counts: dict[str, int] = defaultdict(int)
    drift_counts: dict[str, int] = defaultdict(int)
    for item in manifest_records:
        access_counts[item["access"]] += 1
        drift_counts[item["drift"]] += 1

    relationship_targets = {
        target
        for item in manifest_records
        for target in item["outbound_reference_ids"]
    }
    outbound_edge_count = sum(len(item["outbound_reference_ids"]) for item in manifest_records)
    unresolved_target_ids = sorted(relationship_targets - set(all_ids))

    manifest = {
        "schema_version": 1,
        "contract": initial["contract"],
        "audit": {
            "started_at": initial["audit_started_at"],
            "rechecked_at": recheck["audit_started_at"],
            "compiled_at": initial.get("compiled_at") or recheck["audit_started_at"],
        },
        "coverage": {
            "complete": bool(discovery.get("complete", False)) and semantic_complete and access_counts.get("partial", 0) == 0 and access_counts.get("inaccessible", 0) == 0,
            "discovery": discovery,
            "record_count": len(manifest_records),
            "access_counts": dict(sorted(access_counts.items())),
            "drift_counts": dict(sorted(drift_counts.items())),
            "relationships": {
                "outbound_edge_count": outbound_edge_count,
                "inbound_edge_count": sum(len(item["inbound_reference_ids"]) for item in manifest_records),
                "referenced_target_count": len(relationship_targets),
                "unresolved_target_ids": unresolved_target_ids,
            },
            "semantic_assessment": {
                "complete": semantic_complete,
                "areas": semantic_coverage,
            },
            "unresolved_exceptions": unresolved,
        },
        "records": manifest_records,
    }

    findings.sort(key=lambda item: (item["area"], item.get("page_id") or "", item["code"]))
    finding_ids = [item["id"] for item in findings]
    if len(finding_ids) != len(set(finding_ids)):
        raise ValueError("compiled findings contain duplicate stable ids")
    full_record_count = len(current_records)
    area_index = {}
    for area in AREAS:
        area_findings = [item for item in findings if item["area"] == area]
        semantic = semantic_coverage.get(area)
        if semantic and semantic["unassessed_record_count"]:
            area_status = "not-checked" if semantic["assessed_record_count"] == 0 else "partial"
        elif any(item["status"] == "flag" for item in area_findings):
            area_status = "flag"
        else:
            area_status = "pass"
        area_index[area] = {
            "status": area_status,
            "deterministic_checked_record_count": len(all_ids) if area in {"coverage", "concurrent-drift"} else full_record_count,
            "semantic_assessed_record_count": semantic["assessed_record_count"] if semantic else None,
            "semantic_unassessed_record_count": semantic["unassessed_record_count"] if semantic else None,
            "finding_count": len(area_findings),
            "finding_ids": [item["id"] for item in area_findings],
        }
    classified = {
        "schema_version": 1,
        "manifest_sha256": hashlib.sha256(stable_json(manifest).encode()).hexdigest(),
        "areas": area_index,
        "findings": findings,
    }
    return manifest, classified


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--initial", type=Path, required=True)
    parser.add_argument("--recheck", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest, findings = compile_baseline(load(args.initial), load(args.recheck))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "findings.json").write_text(json.dumps(findings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
