"""analysis.json / decision.json (de)serialization, schema-validated.

The only module allowed to read/write these two JSON files — callers pass
pydantic model instances, not dicts.
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.models import AnalysisResult, DecisionResult


def write_analysis(result: AnalysisResult, out_path: Path) -> None:
    raise NotImplementedError


def read_analysis(path: Path) -> AnalysisResult:
    """Raises on schema_version mismatch with the current
    ``models.ANALYSIS_SCHEMA_VERSION`` rather than attempting a silent
    migration.
    """
    raise NotImplementedError


def write_decision(result: DecisionResult, out_path: Path) -> None:
    raise NotImplementedError


def read_decision(path: Path) -> DecisionResult:
    raise NotImplementedError
