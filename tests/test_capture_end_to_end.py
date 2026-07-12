#!/usr/bin/env python3
"""End-to-end regressions for a materialized semantic Capture package."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / "skills" / "capture"
AUDIT_COMPILER = ROOT / "scripts" / "build-audit-baseline.py"
FIXTURES = ROOT / "tests" / "fixtures"


class CaptureEndToEndTest(unittest.TestCase):
    def compile_audit(self, output: Path, recheck: Path | None = None) -> tuple[Path, Path]:
        audit = FIXTURES / "capture-end-to-end"
        completed = subprocess.run(
            [
                sys.executable,
                str(AUDIT_COMPILER),
                "--initial",
                str(audit / "audit-initial.json"),
                "--recheck",
                str(recheck or audit / "audit-recheck.json"),
                "--output",
                str(output),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return output / "manifest.json", output / "findings.json"

    def materialize_capture(self, destination: Path) -> Path:
        shutil.copytree(CAPTURE, destination)
        return destination / "scripts" / "validate-capture-transition.py"

    def validate(
        self,
        validator: Path,
        manifest: Path,
        findings: Path,
    ) -> tuple[subprocess.CompletedProcess[str], dict]:
        completed = subprocess.run(
            [
                sys.executable,
                str(validator),
                str(FIXTURES / "capture-transitions" / "stable.json"),
                "--audit-manifest",
                str(manifest),
                "--audit-findings",
                str(findings),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        return completed, json.loads(completed.stdout)

    def test_materialized_capture_validates_an_unchanged_audited_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            manifest, findings = self.compile_audit(temp / "baseline")
            validator = self.materialize_capture(temp / "capture")

            completed, report = self.validate(validator, manifest, findings)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(report["disposition"], "Pass")
        audit_result = next(result for result in report["results"] if result["check"] == "audit-baseline")
        self.assertEqual(audit_result["category"], "deterministic")
        self.assertEqual(audit_result["status"], "Pass")
        self.assertIn("page:project-alpha", audit_result["scope"])
        self.assertFalse(report["write_allowed"])

    def test_materialized_capture_blocks_a_transition_based_on_concurrent_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            changed_recheck = temp / "audit-recheck.json"
            recheck = json.loads(
                (FIXTURES / "capture-end-to-end" / "audit-recheck.json").read_text()
            )
            recheck["records"][0]["content"] = "Project Alpha changed during the audit."
            changed_recheck.write_text(json.dumps(recheck))
            manifest, findings = self.compile_audit(temp / "baseline", changed_recheck)
            validator = self.materialize_capture(temp / "capture")

            completed, report = self.validate(validator, manifest, findings)

        self.assertEqual(completed.returncode, 2, completed.stderr)
        self.assertEqual(report["disposition"], "Block")
        audit_result = next(result for result in report["results"] if result["check"] == "audit-baseline")
        self.assertEqual(audit_result["status"], "Flag")
        self.assertIn("concurrent", " ".join(audit_result["evidence"]).lower())

    def test_materialized_contract_matches_the_repository_compatibility_copy(self) -> None:
        repository_contract = ROOT / "contracts" / "capture-transition-v1.json"
        runtime_contract = CAPTURE / "contracts" / "capture-transition-v1.json"

        self.assertEqual(repository_contract.read_bytes(), runtime_contract.read_bytes())

    def test_repository_cli_delegates_to_the_materialized_validator(self) -> None:
        record = FIXTURES / "capture-transitions" / "stable.json"
        repository_cli = ROOT / "scripts" / "validate-capture-transition.py"
        runtime_cli = CAPTURE / "scripts" / "validate-capture-transition.py"

        repository = subprocess.run(
            [sys.executable, str(repository_cli), str(record)],
            text=True,
            capture_output=True,
            check=False,
        )
        runtime = subprocess.run(
            [sys.executable, str(runtime_cli), str(record)],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(repository.returncode, runtime.returncode)
        self.assertEqual(json.loads(repository.stdout), json.loads(runtime.stdout))

    def test_mismatched_audit_outputs_block_the_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp = Path(temporary)
            manifest, findings = self.compile_audit(temp / "baseline")
            classified = json.loads(findings.read_text())
            classified["manifest_sha256"] = "0" * 64
            findings.write_text(json.dumps(classified))
            validator = self.materialize_capture(temp / "capture")

            completed, report = self.validate(validator, manifest, findings)

        self.assertEqual(completed.returncode, 2, completed.stderr)
        audit_result = next(result for result in report["results"] if result["check"] == "audit-baseline")
        self.assertEqual(audit_result["status"], "Flag")
        self.assertIn("do not match", " ".join(audit_result["evidence"]))

    def test_capture_orders_executable_validation_before_approval(self) -> None:
        skill = (CAPTURE / "SKILL.md").read_text()
        normalized = " ".join(skill.split())

        validation = skill.index("python3 scripts/validate-capture-transition.py")
        draft = skill.index("### 5. Draft Exact Writes")
        approval = skill.index("### 6. Ask For Fresh Approval")

        self.assertLess(validation, draft)
        self.assertLess(validation, approval)
        self.assertIn("read-only discovery evidence", normalized)
        self.assertIn("never replaces the required live reads", normalized)


if __name__ == "__main__":
    unittest.main()
