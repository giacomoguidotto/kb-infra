import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build-audit-baseline.py"
SPEC = importlib.util.spec_from_file_location("build_audit_baseline", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AuditBaselineTests(unittest.TestCase):
    def snapshot(self, records, *, at="2026-07-12T12:00:00Z", complete=True):
        return {
            "schema_version": 1,
            "contract": {
                "conventions": "docs/knowledge-bank-conventions.md",
                "revision": "v1-test",
                "kind_registry_version": 1,
            },
            "audit_started_at": at,
            "compiled_at": "2026-07-12T12:10:00Z",
            "discovery": {"complete": complete, "methods": ["fixture"], "exceptions": []},
            "records": records,
        }

    def record(self, page_id, title, **overrides):
        record = {
            "id": page_id,
            "title": title,
            "access": "full",
            "properties": {"Type": "Project", "Ownership": "Canonical", "Maturity": "Stable", "Status": "Active"},
            "content": "A stable description.",
            "outbound_reference_ids": [],
            "kinds": ["state"],
            "revision_evidence": {"revision": "r1"},
            "assessments": [
                {
                    "area": area,
                    "status": "pass",
                    "code": f"{area}-review",
                    "evidence": "Fixture semantic review completed.",
                }
                for area in sorted(MODULE.SEMANTIC_AREAS)
            ],
        }
        record.update(overrides)
        return record

    def test_compiles_reference_coverage_and_unchanged_recheck(self):
        source = self.record("page-a", "Alpha", outbound_reference_ids=["page-b"])
        target = self.record("page-b", "Beta")
        initial = self.snapshot([source, target])
        recheck = self.snapshot([source, target], at="2026-07-12T12:05:00Z")

        manifest, findings = MODULE.compile_baseline(initial, recheck)

        self.assertTrue(manifest["coverage"]["complete"])
        self.assertEqual(manifest["coverage"]["drift_counts"], {"unchanged": 2})
        indexed = {item["id"]: item for item in manifest["records"]}
        self.assertEqual(indexed["page-b"]["inbound_reference_ids"], ["page-a"])
        self.assertEqual(
            manifest["coverage"]["relationships"],
            {
                "outbound_edge_count": 1,
                "inbound_edge_count": 1,
                "referenced_target_count": 1,
                "unresolved_target_ids": [],
            },
        )
        self.assertEqual(findings["areas"]["inbound-references"]["deterministic_checked_record_count"], 2)
        self.assertEqual(findings["areas"]["outbound-references"]["finding_count"], 0)
        finding_ids = [item["id"] for item in findings["findings"]]
        self.assertEqual(len(finding_ids), len(set(finding_ids)))

    def test_classifies_partial_coverage_and_concurrent_change(self):
        before = self.record("page-a", " Alpha ", properties={"Class": "Signal", "Role": "Raw", "Status": "Done"}, content="Follow-up: ask again on 2026-07-01: Check this.\n<empty-block/>", kinds=[], revision_evidence=None)
        after = dict(before, content=before["content"] + "\nChanged during audit.")
        partial = {"id": "page-b", "title": "Hidden", "access": "partial", "exceptions": ["body unavailable"]}
        initial = self.snapshot([before, partial], complete=False)
        initial["discovery"]["exceptions"] = ["enumeration unavailable"]
        recheck = self.snapshot([after, partial], at="2026-07-12T12:05:00Z", complete=False)

        manifest, findings = MODULE.compile_baseline(initial, recheck)

        self.assertFalse(manifest["coverage"]["complete"])
        self.assertEqual(manifest["coverage"]["access_counts"], {"full": 1, "partial": 1})
        codes = {item["code"] for item in findings["findings"]}
        self.assertIn("changed", codes)
        self.assertIn("unverifiable", codes)
        self.assertIn("missing-type", codes)
        self.assertIn("legacy-role", codes)
        self.assertIn("missing-or-invalid-maturity", codes)
        self.assertIn("unclassified-content", codes)
        self.assertIn("inactive-page-present", codes)
        self.assertIn("title-surrounding-space", codes)
        self.assertIn("due-follow-up-2026-07-01", codes)
        self.assertIn("revision-evidence-unavailable", codes)
        self.assertIn("empty-block", codes)
        self.assertIn("discovery-not-proven-complete", codes)

    def test_unresolved_outbound_reference_is_error(self):
        record = self.record("page-a", "Alpha", outbound_reference_ids=["missing-page"])
        initial = self.snapshot([record])
        recheck = self.snapshot([record], at="2026-07-12T12:05:00Z")

        _, findings = MODULE.compile_baseline(initial, recheck)

        unresolved = [item for item in findings["findings"] if item["area"] == "outbound-references"]
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(unresolved[0]["severity"], "error")

    def test_rejects_contract_drift_between_passes(self):
        record = self.record("page-a", "Alpha")
        initial = self.snapshot([record])
        recheck = self.snapshot([record], at="2026-07-12T12:05:00Z")
        recheck["contract"] = dict(recheck["contract"], revision="different")

        with self.assertRaisesRegex(ValueError, "same contract"):
            MODULE.compile_baseline(initial, recheck)

    def test_does_not_classify_initial_content_when_recheck_is_partial(self):
        before = self.record(
            "page-a",
            "Alpha",
            properties={"Class": "Signal", "Role": "Raw", "Status": "Done"},
            kinds=[],
            revision_evidence=None,
        )
        after = {"id": "page-a", "title": "Alpha", "access": "partial", "exceptions": ["body unavailable"]}
        initial = self.snapshot([before])
        recheck = self.snapshot([after], at="2026-07-12T12:05:00Z")

        manifest, findings = MODULE.compile_baseline(initial, recheck)

        self.assertEqual(manifest["coverage"]["access_counts"], {"partial": 1})
        codes = {item["code"] for item in findings["findings"]}
        self.assertNotIn("missing-type", codes)
        self.assertNotIn("legacy-role", codes)
        self.assertIn("partial", codes)

    def test_merges_recheck_exceptions(self):
        record = self.record("page-a", "Alpha")
        initial = self.snapshot([record])
        recheck = self.snapshot([record], at="2026-07-12T12:05:00Z")
        recheck["discovery"]["exceptions"] = ["late discovery failure"]
        recheck["unresolved_exceptions"] = ["late unresolved exception"]

        manifest, _ = MODULE.compile_baseline(initial, recheck)

        self.assertIn("late discovery failure", manifest["coverage"]["unresolved_exceptions"])
        self.assertIn("late unresolved exception", manifest["coverage"]["unresolved_exceptions"])

    def test_reports_unassessed_semantic_coverage(self):
        record = self.record("page-a", "Alpha", assessments=[])
        initial = self.snapshot([record])
        recheck = self.snapshot([record], at="2026-07-12T12:05:00Z")

        manifest, findings = MODULE.compile_baseline(initial, recheck)

        self.assertFalse(manifest["coverage"]["semantic_assessment"]["complete"])
        self.assertTrue(
            any(
                item.startswith("Semantic assessments remain incomplete")
                for item in manifest["coverage"]["unresolved_exceptions"]
            )
        )
        self.assertEqual(findings["areas"]["duplication"]["status"], "not-checked")
        self.assertEqual(findings["areas"]["duplication"]["semantic_unassessed_record_count"], 1)


if __name__ == "__main__":
    unittest.main()
