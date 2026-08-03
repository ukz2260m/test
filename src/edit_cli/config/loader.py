"""Loads, validates, and profile-merges config/*.yaml into a ResolvedConfig.

This is the ONLY module allowed to read config/*.yaml paths off disk.
Everything downstream receives a validated ``ResolvedConfig`` object.

Implementation note (not yet implemented): profile merging is a recursive
deep-merge of ``overrides`` from ``config/profiles/<profile>.yaml`` (and
whatever it ``extends``, recursively) onto the base documents, applied
BEFORE pydantic validation so schema errors always point at final values.
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.config.schema import ResolvedConfig


def load_config(config_dir: Path, profile: str = "default") -> ResolvedConfig:
    """Load config/*.yaml under ``config_dir``, apply ``profile`` overrides.

    Args:
        config_dir: directory containing rois.yaml, thresholds.yaml,
            glossary.txt, corrections.yaml, telop_style.yaml, profiles/.
        profile: name of a file under ``config_dir/profiles/<profile>.yaml``.

    Returns:
        A fully validated ``ResolvedConfig``. Raises on missing files,
        invalid YAML, schema validation errors, or an unresolvable
        ``extends`` chain (including cycles).
    """
    raise NotImplementedError


def compute_fingerprint(config_dir: Path, profile: str) -> str:
    """Stable hash of the fully-resolved config content.

    Used for two independent purposes with different sensitivity:
    - ``analysis_cache`` keys on the fingerprint of ONLY the config that
      affects analyze-time output (rois.yaml, glossary.txt) — changing
      thresholds.yaml must NOT invalidate the analyze cache.
    - ``decision.json`` records the fingerprint of the config that affects
      export-time output (thresholds.yaml, telop_style.yaml, corrections.yaml)
      for auditability.

    Returns:
        Hex digest string.
    """
    raise NotImplementedError


def load_glossary(path: Path) -> list[str]:
    """Parse config/glossary.txt: one term per line, '#' comments, blank lines ignored."""
    raise NotImplementedError
