"""Content-hash + config-fingerprint keyed cache for AnalysisResult.

Lets `analyze` skip re-running ingest/vision/audio/transcribe entirely when
called again for the same video with the same analyze-relevant config
(rois.yaml + glossary.txt — NOT thresholds.yaml, which never affects
analyze output). Cache root defaults to ``.analysis_cache/`` next to the
input, overridable — see ``cli.py``.
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.models import AnalysisResult


def cache_key(source_sha256: str, analyze_config_fingerprint: str, tool_version: str) -> str:
    raise NotImplementedError


def get(cache_dir: Path, key: str) -> AnalysisResult | None:
    """Returns None on a cache miss (including a version-mismatched hit,
    which is treated as a miss rather than an error)."""
    raise NotImplementedError


def put(cache_dir: Path, key: str, result: AnalysisResult) -> None:
    raise NotImplementedError
