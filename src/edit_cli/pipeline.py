"""Orchestration for the two pipeline halves. cli.py calls into here; no
business logic lives in cli.py itself.

See docs/ARCHITECTURE.md "Pipeline flow" for the full call sequence each
function wires together.
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.config.schema import ResolvedConfig
from edit_cli.models import AnalysisResult, DecisionResult


def run_analyze(input_path: Path, config: ResolvedConfig, work_dir: Path, use_cache: bool = True) -> AnalysisResult:
    """ingest -> vision -> audio -> transcribe -> filler classification.

    Returns (and caches, if ``use_cache``) an ``AnalysisResult``. Never reads
    ``config.thresholds`` — analyze-time output must not depend on
    export-time tunables.
    """
    raise NotImplementedError


def run_export(analysis: AnalysisResult, config: ResolvedConfig, profile_name: str, out_dir: Path) -> DecisionResult:
    """score (combat_score -> segment_builder -> keep_cut_decision) -> write
    XML/EDL + ASS + decision.json into ``out_dir``.

    Never touches the source video or re-derives anything analyze already
    computed — reads only from ``analysis``.
    """
    raise NotImplementedError
