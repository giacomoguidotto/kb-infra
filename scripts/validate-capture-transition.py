#!/usr/bin/env python3
"""Run the validator bundled with the materialized Capture skill."""

from pathlib import Path
from runpy import run_path


VALIDATOR = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "capture"
    / "scripts"
    / "validate-capture-transition.py"
)


if __name__ == "__main__":
    run_path(str(VALIDATOR), run_name="__main__")
