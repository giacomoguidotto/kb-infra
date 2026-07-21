#!/usr/bin/env python3
"""Validate the provider-blind Knowledge System interface source."""

import json
import re
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/public/setup-knowledge-system/resources/knowledge-system-interface/v1"


def load(relative: str):
    with (PACKAGE / relative).open(encoding="utf-8") as source:
        return json.load(source)


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


registry = load("endpoint-registry.json")
request_schema = load("request.schema.json")
snapshot_schema = load("snapshot.schema.json")
capture_request_schema = load("capture-request.schema.json")
capture_draft_schema = load("capture-draft.schema.json")
capture_blocked_schema = load("capture-blocked.schema.json")
request = load("examples/request.json")
snapshot = load("examples/snapshot.json")
capture_request = load("examples/capture-request.json")
capture_draft = load("examples/capture-draft.json")
capture_blocked = load("examples/capture-blocked.json")

schema_examples = (
    (request_schema, request),
    (snapshot_schema, snapshot),
    (capture_request_schema, capture_request),
    (capture_draft_schema, capture_draft),
    (capture_blocked_schema, capture_blocked),
)
for schema, example in schema_examples:
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(example)

preamble = (ROOT / "docs/automations/_preamble.md").read_text(encoding="utf-8")
endpoint_section = preamble.split("### Endpoints", 1)[1].split("### Sinks", 1)[0]
declared_roles = set(re.findall(r"^- `([a-z0-9-]+)`:", endpoint_section, re.MULTILINE))
require(set(registry["roles"]) == declared_roles, "Endpoint Registry differs from the endpoint vocabulary")
require(registry["interface"] == "knowledge-system-interface/v1", "registry interface is invalid")
require(bool(registry["revision"]), "registry revision is empty")

for role, entry in registry["roles"].items():
    require(entry["compatibility"] in {"active", "deprecated"}, f"{role} has invalid compatibility")
    for field in ("meaning", "result_shape", "visibility", "intended_use", "traversal", "provenance", "stopping_conditions"):
        require(bool(entry[field]), f"{role} lacks {field}")
    require(
        {"owner", "source", "observed_at", "revision"} <= set(entry["provenance"]),
        f"{role} lacks required provenance",
    )

for schema in (request_schema, snapshot_schema, capture_request_schema, capture_draft_schema, capture_blocked_schema):
    require(schema["additionalProperties"] is False, f"{schema['title']} permits undeclared fields")
    require(
        schema["properties"]["interface"]["const"] == "knowledge-system-interface/v1",
        f"{schema['title']} has the wrong interface",
    )

for document in (request, snapshot, capture_request, capture_draft, capture_blocked):
    require(document["interface"] == "knowledge-system-interface/v1", "example has the wrong interface")

for forbidden in ("provider", "page", "location", "traversal", "facts", "projects"):
    require(forbidden not in request_schema["properties"], f"provider detail leaked into request: {forbidden}")
    require(forbidden not in request, f"provider detail leaked into example request: {forbidden}")

active_roles = {role for role, entry in registry["roles"].items() if entry["compatibility"] == "active"}
requested_roles = set(request["roles"]["required"] + request["roles"]["optional"])
require(requested_roles <= active_roles, "request includes a role that is not active")
require(set(request["mandate"]["read_roles"]) == requested_roles, "request roles differ from mandate roles")
require(request["requirements"]["claim_provenance"] is True, "request does not require claim provenance")
require(
    request["intended_use"]["mode"] in {"private-context", "named-sink", "public-draft"},
    "request has an invalid intended-use mode",
)

result_variants = snapshot_schema["$defs"]["result"]["oneOf"]
require(
    {variant["properties"]["state"]["const"] for variant in result_variants}
    == {"value", "absent", "unresolved"},
    "snapshot schema does not define the exact result states",
)
require(
    {result["state"] for result in snapshot["results"].values()} == {"value", "absent", "unresolved"},
    "snapshot example does not cover every result state",
)
require(len(snapshot["snapshot_token"]) >= 16, "snapshot token is too short")
require(snapshot["capability_status"]["state"] == "blocked", "drift example capability is not blocked")
require(
    snapshot["capability_status"]["blocking_roles"] == ["personal-constraints"],
    "drift example blocks the wrong roles",
)

snapshot_validator = Draft202012Validator(snapshot_schema)
for state, blocking_roles in (("ready", ["identity"]), ("blocked", [])):
    invalid_snapshot = deepcopy(snapshot)
    invalid_snapshot["capability_status"]["state"] = state
    invalid_snapshot["capability_status"]["blocking_roles"] = blocking_roles
    try:
        snapshot_validator.validate(invalid_snapshot)
    except ValidationError:
        pass
    else:
        raise AssertionError(f"snapshot permits inconsistent {state} capability state")

require(
    snapshot["results"]["personal-constraints"]["reason"] == "persistent_drift",
    "drift example has the wrong unresolved reason",
)
for result in snapshot["results"].values():
    if result["state"] == "value":
        for claim in result["claims"]:
            require(bool(claim["evidence"] and claim["provenance"]), "value claim lacks evidence or provenance")
    if result["state"] == "absent":
        require(bool(result["evidence"] and result["provenance"]), "absence lacks evidence or provenance")

require(capture_request["target_role"] in active_roles, "capture target role is not active")
require(
    capture_request["target_role"] in capture_request["mandate"]["capture_roles"],
    "capture target role is outside the mandate",
)
require(capture_draft["status"] == "drafted", "capture draft has the wrong status")
require(bool(capture_draft["operations"]), "capture draft has no operations")
require(
    capture_draft["approval_prompt"] == "Should I apply these exact KB writes now?",
    "capture draft has the wrong approval prompt",
)
require(
    capture_draft_schema["properties"]["approval_prompt"]["const"] == capture_draft["approval_prompt"],
    "capture schema and example approval prompts differ",
)
require(capture_blocked["status"] == "blocked", "blocked capture example has the wrong status")
require(
    "operations" not in capture_blocked and "approval_prompt" not in capture_blocked,
    "blocked capture includes write authority",
)

print("knowledge-system-interface/v1: OK")
