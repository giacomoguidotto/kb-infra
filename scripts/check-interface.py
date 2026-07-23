#!/usr/bin/env python3
"""Validate the provider-blind Knowledge System interface source."""

import json
import re
import subprocess
from copy import deepcopy
from hashlib import sha256
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
token_request_schema = load("snapshot-token-validation-request.schema.json")
token_operation_schema = load("snapshot-token-validation-operation.schema.json")
token_result_schema = load("snapshot-token-validation-result.schema.json")
request = load("examples/request.json")
snapshot = load("examples/snapshot.json")
capture_request = load("examples/capture-request.json")
capture_draft = load("examples/capture-draft.json")
capture_blocked = load("examples/capture-blocked.json")
token_request = load("examples/snapshot-token-validation-request.json")
token_operation = load("examples/snapshot-token-validation-operation.json")
token_result = load("examples/snapshot-token-validation-result.json")

schema_examples = (
    (request_schema, request),
    (snapshot_schema, snapshot),
    (capture_request_schema, capture_request),
    (capture_draft_schema, capture_draft),
    (capture_blocked_schema, capture_blocked),
    (token_request_schema, token_request),
    (token_operation_schema, token_operation),
    (token_result_schema, token_result),
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

token_validator_path = PACKAGE / "validate-snapshot-token.py"
require(token_validator_path.stat().st_mode & 0o111, "Snapshot Token validator is not executable")
token_result_validator = Draft202012Validator(token_result_schema)
for forbidden in ("provider", "page", "location", "traversal", "facts", "projects"):
    require(
        forbidden not in token_request_schema["properties"],
        f"provider detail leaked into token validation request: {forbidden}",
    )
    require(
        forbidden not in token_request,
        f"provider detail leaked into token validation example: {forbidden}",
    )
token_statuses = set()
for variant in token_result_schema["oneOf"]:
    status_schema = variant["properties"]["status"]
    token_statuses.update(status_schema.get("enum", [status_schema.get("const")]))
require(
    token_statuses == {"unchanged", "changed", "malformed", "unsupported", "unresolved"},
    "Snapshot Token result schema does not distinguish every required state",
)


def package_digest():
    digest = sha256()
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(PACKAGE)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def run_token_validation(operation):
    completed = subprocess.run(
        [str(token_validator_path)],
        input=json.dumps(operation),
        text=True,
        capture_output=True,
        check=True,
    )
    require(not completed.stderr, f"Snapshot Token validator wrote stderr: {completed.stderr}")
    result = json.loads(completed.stdout)
    token_result_validator.validate(result)
    serialized = json.dumps(result)
    for observation in operation.get("observations", []):
        observation_token = observation.get("snapshot_token")
        if observation_token is not None:
            require(observation_token not in serialized, "Snapshot Token validator leaked a live token")
    request_token = operation.get("request", {}).get("snapshot_token")
    if request_token is not None:
        require(request_token not in serialized, "Snapshot Token validator leaked the returned token")
    return completed.stdout, result


package_before = package_digest()
unchanged_output, unchanged = run_token_validation(token_operation)
identical_output, identical = run_token_validation(token_operation)
require(unchanged["status"] == "unchanged", "matching Snapshot Token was not unchanged")
require(unchanged_output == identical_output, "identical validation rerun was not deterministic")
require(unchanged == identical, "identical validation rerun changed its result")

unicode_operation = deepcopy(token_operation)
unicode_operation["request"]["snapshot_token"] = "opaque-token-åäö-1234"
unicode_operation["observations"][0]["snapshot_token"] = "opaque-token-åäö-1234"
_, unicode_result = run_token_validation(unicode_operation)
require(unicode_result["status"] == "unchanged", "non-ASCII opaque token could not be validated")

surrogate_operation = deepcopy(token_operation)
surrogate_operation["request"]["snapshot_token"] = "opaque-token-\ud800-1234"
_, surrogate_result = run_token_validation(surrogate_operation)
require(surrogate_result["status"] == "malformed", "non-encodable token did not return malformed")

changed_operation = deepcopy(token_operation)
changed_operation["observations"][0]["snapshot_token"] = "opaque-changed-token-1234"
_, changed = run_token_validation(changed_operation)
require(changed["status"] == "changed", "changed Snapshot Token was not detected")

malformed_operation = deepcopy(token_operation)
malformed_operation["request"]["snapshot_token"] = "short"
_, malformed = run_token_validation(malformed_operation)
require(malformed["status"] == "malformed", "malformed Snapshot Token was not rejected")

unsupported_operation = deepcopy(token_operation)
unsupported_operation["request"]["interface"] = "knowledge-system-interface/v2"
_, unsupported = run_token_validation(unsupported_operation)
require(unsupported["status"] == "unsupported", "unsupported interface was not distinguished")

unresolved_operation = deepcopy(token_operation)
unresolved_operation["observations"] = [{"state": "unresolved", "reason": "access_blocked"}]
_, unresolved = run_token_validation(unresolved_operation)
require(unresolved["status"] == "unresolved", "unresolved live state was not distinguished")
require(unresolved["reason"] == "access_blocked", "unresolved reason was not preserved")

persistent_drift_operation = deepcopy(token_operation)
persistent_drift_operation["observations"].append(
    {"state": "resolved", "snapshot_token": "opaque-rebuilt-token-1234"}
)
_, persistent_drift = run_token_validation(persistent_drift_operation)
require(
    persistent_drift == {
        "interface": "knowledge-system-interface/v1",
        "caller": token_request["caller"],
        "capability": token_request["capability"],
        "status": "unresolved",
        "reason": "persistent_drift",
    },
    "persistent validation drift did not block the dependent capability",
)
require(package_digest() == package_before, "Snapshot Token validation wrote interface content")

print("knowledge-system-interface/v1: OK")
