#!/usr/bin/env python3
"""Black-box tests for the Capture transition validator."""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-capture-transition.py"
FIXTURES = ROOT / "tests" / "fixtures" / "capture-transitions"


class CaptureValidationTest(unittest.TestCase):
    def validate(self, fixture: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR), str(FIXTURES / fixture)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        report = json.loads(completed.stdout)
        return completed, report

    def validate_record(self, record: dict) -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as fixture:
            json.dump(record, fixture)
            fixture.flush()
            completed = subprocess.run(
                [sys.executable, str(VALIDATOR), fixture.name],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        return completed, json.loads(completed.stdout)

    def test_stable_transition_passes_with_evidence_but_not_approval(self) -> None:
        completed, report = self.validate("stable.json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(report["disposition"], "Pass")
        self.assertTrue(report["human_approval"]["required"])
        self.assertEqual(report["human_approval"]["status"], "Not checked")
        self.assertFalse(report["write_allowed"])
        self.assertIn("deterministic", {result["category"] for result in report["results"]})
        self.assertIn("semantic", {result["category"] for result in report["results"]})
        for result in report["results"]:
            self.assertIn(result["status"], {"Pass", "Flag", "Not checked", "Not applicable"})
            self.assertTrue(result["scope"])
            self.assertTrue(result["evidence"])

    def test_valid_orthogonal_axis_transitions_pass(self) -> None:
        for fixture in ("developing.json", "retained-raw.json", "adapter.json", "deletion-safe.json"):
            with self.subTest(fixture=fixture):
                completed, report = self.validate(fixture)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(report["disposition"], "Pass")

    def test_deterministic_contract_failures_block_without_semantic_inference(self) -> None:
        cases = {
            "invalid-kind.json": "kind-structure",
            "bad-time.json": "time-and-provenance",
            "broken-references.json": "reference-resolution",
        }
        for fixture, failed_check in cases.items():
            with self.subTest(fixture=fixture):
                completed, report = self.validate(fixture)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(report["disposition"], "Block")
                matching = [result for result in report["results"] if result["check"] == failed_check]
                self.assertEqual(matching[0]["category"], "deterministic")
                self.assertEqual(matching[0]["status"], "Flag")
                semantic = [result for result in report["results"] if result["category"] == "semantic"]
                self.assertTrue(all(result["status"] == "Not checked" for result in semantic))

    def test_blocking_semantic_judgments_block_the_transition(self) -> None:
        cases = {
            "contradiction.json": ("duplication-and-contradiction", "contradiction"),
            "missing-evidence.json": ("faithfulness", "unsupported-assertion"),
            "material-omission.json": ("coverage", "material-omission"),
            "deletion-unsafe.json": ("deletion-safety", "unsafe-deletion"),
        }
        for fixture, (failed_check, issue) in cases.items():
            with self.subTest(fixture=fixture):
                completed, report = self.validate(fixture)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(report["disposition"], "Block")
                matching = [result for result in report["results"] if result["check"] == failed_check]
                self.assertEqual(matching[0]["category"], "semantic")
                self.assertEqual(matching[0]["status"], "Flag")
                self.assertIn(issue, matching[0]["issues"])

    def test_nonblocking_semantic_uncertainty_is_flagged_for_review(self) -> None:
        completed, report = self.validate("possible-duplication.json")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(report["disposition"], "Flag")
        self.assertFalse(report["write_allowed"])

    def test_reports_exercise_all_contract_statuses(self) -> None:
        statuses = set()
        for fixture in (
            "stable.json",
            "invalid-kind.json",
            "possible-duplication.json",
        ):
            _, report = self.validate(fixture)
            statuses.update(result["status"] for result in report["results"])

        self.assertEqual(statuses, {"Pass", "Flag", "Not checked", "Not applicable"})

    def test_bare_pass_is_invalid_contract_drift_and_blocks(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["semantic_judgments"][0]["evidence"] = []

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(report["disposition"], "Block")
        contract_failures = [
            result
            for result in report["results"]
            if result["check"] == "semantic-judgment-contract"
        ]
        self.assertEqual(contract_failures[0]["category"], "deterministic")
        ownership = [result for result in report["results"] if result["check"] == "ownership"]
        self.assertEqual(ownership[0]["status"], "Not checked")

    def test_executable_kind_registry_matches_the_normative_table(self) -> None:
        contract = json.loads((ROOT / "contracts" / "capture-transition-v1.json").read_text())
        conventions = (ROOT / "docs" / "knowledge-bank-conventions.md").read_text()
        registry_section = conventions.split("## Kind Registry", 1)[1].split("## Page and Section Structure", 1)[0]
        documented = re.findall(r"^\| `([^`]+)` \|", registry_section, flags=re.MULTILINE)

        self.assertEqual(contract["kinds"], documented)
        self.assertEqual(
            set(contract["result_statuses"]),
            {"Pass", "Flag", "Not checked", "Not applicable"},
        )

    def test_malformed_reference_is_reported_instead_of_crashing(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["references"] = [42]

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertEqual(report["disposition"], "Block")
        reference_result = [
            result for result in report["results"] if result["check"] == "reference-resolution"
        ]
        self.assertEqual(reference_result[0]["status"], "Flag")

    def test_unknown_semantic_check_is_invalid_contract_drift(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["semantic_judgments"].append(
            {
                "check": "plausibility",
                "status": "Pass",
                "scope": "all assertions",
                "evidence": ["This check is not part of contract version 1."],
                "issues": [],
            }
        )

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(report["disposition"], "Block")
        failures = [
            result
            for result in report["results"]
            if result["check"] == "semantic-judgment-contract"
        ]
        self.assertTrue(failures)
        self.assertEqual(failures[0]["category"], "deterministic")

    def test_type_is_a_required_axis_independent_of_ownership(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        del record["target"]["type"]

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2)
        matching = [result for result in report["results"] if result["check"] == "type-structure"]
        self.assertEqual(matching[0]["status"], "Flag")

    def test_time_requires_an_absolute_timezone_anchor(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["revision"]["captured_at"] = "2026-07-12T12:00:00"

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2)
        matching = [result for result in report["results"] if result["check"] == "time-and-provenance"]
        self.assertEqual(matching[0]["status"], "Flag")

    def test_rule_requires_scope_and_normative_force(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["kind"] = "rule"
        del record["assertions"][0]["observed_at"]
        record["assertions"][0]["text"] = "Agents must validate transitions."

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2)
        matching = [result for result in report["results"] if result["check"] == "kind-structure"]
        self.assertEqual(matching[0]["status"], "Flag")

    def test_every_assertion_requires_source_provenance(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["sources"] = []
        record["assertions"][0]["source_refs"] = []

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2)
        matching = [result for result in report["results"] if result["check"] == "time-and-provenance"]
        self.assertEqual(matching[0]["status"], "Flag")

    def test_adapter_links_each_assertion_to_a_canonical_owner(self) -> None:
        record = json.loads((FIXTURES / "adapter.json").read_text())
        del record["assertions"][0]["canonical_owner_ref"]

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2)
        matching = [result for result in report["results"] if result["check"] == "adapter-links"]
        self.assertEqual(matching[0]["status"], "Flag")

    def test_deletion_recovery_reference_must_resolve(self) -> None:
        record = json.loads((FIXTURES / "deletion-safe.json").read_text())
        record["deletion"]["recovery_ref"] = "revision:missing"

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2)
        matching = [result for result in report["results"] if result["check"] == "deletion-structure"]
        self.assertEqual(matching[0]["status"], "Flag")

    def test_revision_evidence_requires_exact_diff_relation_and_resolved_prior(self) -> None:
        mutations = (
            lambda record: record["revision"].update(diff="summary only"),
            lambda record: record["references"].__setitem__(1, {"id": "revision:project-alpha-1", "resolves": False}),
            lambda record: record["revision"].pop("relation"),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                record = json.loads((FIXTURES / "stable.json").read_text())
                mutate(record)
                completed, report = self.validate_record(record)
                self.assertEqual(completed.returncode, 2)
                matching = [result for result in report["results"] if result["status"] == "Flag"]
                self.assertTrue(matching)

    def test_semantic_force_is_a_separate_judgment(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["semantic_judgments"] = [
            judgment
            for judgment in record["semantic_judgments"]
            if judgment["check"] != "kind-and-semantic-force"
        ]

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(report["disposition"], "Flag")
        matching = [result for result in report["results"] if result["check"] == "kind-and-semantic-force"]
        self.assertEqual(matching[0]["category"], "semantic")
        self.assertEqual(matching[0]["status"], "Not checked")

    def test_non_deletion_transition_may_invalidate_prior_meaning(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["revision"]["relation"] = "invalidates"

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(report["disposition"], "Pass")

    def test_malformed_assertion_shape_is_an_evidence_bearing_block(self) -> None:
        malformed_assertions = (
            {"source_refs": ["source:run-log"]},
            {"id": "assertion:runtime", "text": "Project Alpha uses the runtime.", "source_refs": 42},
        )
        for assertion in malformed_assertions:
            with self.subTest(assertion=assertion):
                record = json.loads((FIXTURES / "stable.json").read_text())
                record["kind"] = "direction"
                record["assertions"] = [assertion]
                completed, report = self.validate_record(record)
                self.assertEqual(completed.returncode, 2, completed.stderr)
                self.assertEqual(report["disposition"], "Block")
                matching = [result for result in report["results"] if result["check"] == "kind-structure"]
                self.assertEqual(matching[0]["status"], "Flag")

    def test_malformed_target_shape_is_an_evidence_bearing_block(self) -> None:
        record = json.loads((FIXTURES / "stable.json").read_text())
        record["target"] = "page:project-alpha"

        completed, report = self.validate_record(record)

        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertEqual(report["disposition"], "Block")
        audit = [result for result in report["results"] if result["check"] == "audit-baseline"]
        self.assertEqual(audit[0]["status"], "Not applicable")
        ownership = [result for result in report["results"] if result["check"] == "ownership-structure"]
        self.assertEqual(ownership[0]["status"], "Flag")


if __name__ == "__main__":
    unittest.main()
