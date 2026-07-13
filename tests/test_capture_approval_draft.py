#!/usr/bin/env python3
"""Black-box regressions for the Capture approval-draft review contract."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills" / "capture" / "scripts" / "validate-approval-draft.py"


def draft(
    *,
    summary: str = "Add the semantic fields to Recipes.",
    table_row: str = "<tr><td>Type</td><td>Add</td><td>Absent</td><td>Recipe</td><td>Record type</td></tr>",
    preview: str = "<p>Recipes will expose Type as Recipe.</p>",
    unchanged: str = "12 existing fields and every page body remain unchanged.",
    technical_open: str = "",
    raw_outside: str = "",
    outline: str = '<a data-mutation-link href="#op-001">01 Recipes schema</a>',
) -> str:
    return f"""<!doctype html>
<html lang="en">
<body data-capture-draft-version="1" data-draft-id="draft-1">
  <nav class="mutation-outline" aria-label="Proposed write outline">
    {outline}
  </nav>
  <section id="proposed-results">
    <details class="technical-evidence">
      <summary>Complete batch evidence</summary>
      <pre data-raw-provider-state>{{"batch": "exact"}}</pre>
    </details>
    {raw_outside}
    <article id="op-001" class="kb-page mutation" data-mutation-id="op-001" data-mutation-kind="schema">
      <section class="change-summary"><h2>What changes</h2><p>{summary}</p></section>
      <table class="change-table">
        <thead><tr><th>Field</th><th>Action</th><th>Current</th><th>Proposed</th><th>Meaning</th></tr></thead>
        <tbody>{table_row}</tbody>
      </table>
      <section class="provider-preview">{preview}</section>
      <p class="unchanged-scope">{unchanged}</p>
      <details class="technical-evidence" {technical_open}>
        <summary>Exact provider evidence</summary>
        <section data-exact-before><pre>{{"schema": "before"}}</pre></section>
        <section data-exact-after><pre>{{"schema": "after"}}</pre></section>
        <pre data-raw-provider-state>{{"tool": "update"}}</pre>
      </details>
    </article>
  </section>
</body>
</html>
"""


class CaptureApprovalDraftTest(unittest.TestCase):
    def validate(self, html: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html") as artifact:
            artifact.write(html)
            artifact.flush()
            completed = subprocess.run(
                [sys.executable, str(VALIDATOR), artifact.name],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
        return completed, json.loads(completed.stdout)

    def test_human_readable_review_layer_and_closed_exact_evidence_pass(self) -> None:
        completed, report = self.validate(draft())

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(report["disposition"], "Pass")
        self.assertEqual(report["mutation_count"], 1)
        self.assertFalse(report["write_allowed"])
        self.assertTrue(all(not result["blocking"] for result in report["results"]))

    def test_raw_provider_state_outside_technical_evidence_blocks(self) -> None:
        completed, report = self.validate(
            draft(raw_outside='<pre data-raw-provider-state>{"schema": "dump"}</pre>')
        )

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(report["disposition"], "Block")
        placement = next(
            result for result in report["results"] if result["check"] == "raw-evidence-placement"
        )
        self.assertTrue(placement["blocking"])

    def test_unmarked_serialized_json_in_visible_preformatted_block_blocks(self) -> None:
        completed, report = self.validate(
            draft(raw_outside='<pre>{"schema": {"Name": {"type": "title"}}}</pre>')
        )

        self.assertEqual(completed.returncode, 2)
        placement = next(
            result for result in report["results"] if result["check"] == "raw-evidence-placement"
        )
        self.assertTrue(placement["blocking"])

    def test_missing_visible_change_information_blocks(self) -> None:
        completed, report = self.validate(
            draft(summary="", table_row="", preview="", unchanged="")
        )

        self.assertEqual(completed.returncode, 2)
        review = next(
            result for result in report["results"] if result["check"] == "review-layer:op-001"
        )
        self.assertTrue(review["blocking"])

    def test_visible_placeholder_blocks(self) -> None:
        completed, report = self.validate(draft(preview="{{complete_after_state}}"))

        self.assertEqual(completed.returncode, 2)
        review = next(
            result for result in report["results"] if result["check"] == "review-layer:op-001"
        )
        self.assertTrue(review["blocking"])

    def test_open_exact_evidence_blocks(self) -> None:
        completed, report = self.validate(draft(technical_open="open"))

        self.assertEqual(completed.returncode, 2)
        evidence = next(
            result for result in report["results"] if result["check"] == "exact-evidence:op-001"
        )
        self.assertTrue(evidence["blocking"])

    def test_missing_mutation_outline_blocks(self) -> None:
        completed, report = self.validate(draft(outline=""))

        self.assertEqual(completed.returncode, 2)
        outline = next(
            result for result in report["results"] if result["check"] == "mutation-outline"
        )
        self.assertTrue(outline["blocking"])

    def test_mutation_outline_must_match_card_order(self) -> None:
        completed, report = self.validate(
            draft(outline='<a data-mutation-link href="#op-999">01 Wrong card</a>')
        )

        self.assertEqual(completed.returncode, 2)
        outline = next(
            result for result in report["results"] if result["check"] == "mutation-outline"
        )
        self.assertTrue(outline["blocking"])


if __name__ == "__main__":
    unittest.main()
