#!/usr/bin/env python3
"""Validate the provider-blind Knowledge System interface source."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "interfaces/knowledge-system-interface/v1"


def load(relative: str):
    with (PACKAGE / relative).open(encoding="utf-8") as source:
        return json.load(source)


registry = load("endpoint-registry.json")
request_schema = load("request.schema.json")
snapshot_schema = load("snapshot.schema.json")
capture_request_schema = load("capture-request.schema.json")
capture_draft_schema = load("capture-draft.schema.json")
request = load("examples/request.json")
snapshot = load("examples/snapshot.json")
capture_request = load("examples/capture-request.json")
capture_draft = load("examples/capture-draft.json")

preamble = (ROOT / "docs/automations/_preamble.md").read_text(encoding="utf-8")
endpoint_section = preamble.split("### Endpoints", 1)[1].split("### Sinks", 1)[0]
declared_roles = set(re.findall(r"^- `([a-z0-9-]+)`:", endpoint_section, re.MULTILINE))
assert set(registry["roles"]) == declared_roles, "Endpoint Registry differs from the endpoint vocabulary"
assert registry["interface"] == "knowledge-system-interface/v1"
assert registry["revision"]

for role, entry in registry["roles"].items():
    assert entry["compatibility"] in {"active", "deprecated"}, role
    for field in ("meaning", "result_shape", "visibility", "intended_use", "traversal", "provenance", "stopping_conditions"):
        assert entry[field], f"{role} lacks {field}"
    assert {"owner", "source", "observed_at", "revision"} <= set(entry["provenance"]), role

for schema in (request_schema, snapshot_schema, capture_request_schema, capture_draft_schema):
    assert schema["additionalProperties"] is False
    assert schema["properties"]["interface"]["const"] == "knowledge-system-interface/v1"

for document in (request, snapshot, capture_request, capture_draft):
    assert document["interface"] == "knowledge-system-interface/v1"

for forbidden in ("provider", "page", "location", "traversal", "facts", "projects"):
    assert forbidden not in request_schema["properties"], f"provider detail leaked into request: {forbidden}"
    assert forbidden not in request, f"provider detail leaked into example request: {forbidden}"

known_roles = set(registry["roles"])
requested_roles = set(request["roles"]["required"] + request["roles"]["optional"])
assert requested_roles <= known_roles
assert set(request["mandate"]["read_roles"]) == requested_roles
assert request["requirements"]["claim_provenance"] is True
assert request["intended_use"]["mode"] in {"private-context", "named-sink", "public-draft"}

result_variants = snapshot_schema["$defs"]["result"]["oneOf"]
assert {variant["properties"]["state"]["const"] for variant in result_variants} == {"value", "absent", "unresolved"}
assert {result["state"] for result in snapshot["results"].values()} == {"value", "absent", "unresolved"}
assert len(snapshot["snapshot_token"]) >= 16
assert snapshot["capability_status"]["state"] == "blocked"
assert snapshot["capability_status"]["blocking_roles"] == ["personal-constraints"]
assert snapshot["results"]["personal-constraints"]["reason"] == "persistent_drift"
for result in snapshot["results"].values():
    if result["state"] == "value":
        for claim in result["claims"]:
            assert claim["evidence"] and claim["provenance"]
    if result["state"] == "absent":
        assert result["evidence"] and result["provenance"]

assert capture_request["target_role"] in capture_request["mandate"]["capture_roles"]
assert capture_draft["status"] == "drafted"
assert capture_draft["operations"]
assert capture_draft["approval_prompt"] == "Should I apply these exact KB writes now?"
assert capture_draft_schema["properties"]["approval_prompt"]["const"] == capture_draft["approval_prompt"]

print("knowledge-system-interface/v1: OK")
