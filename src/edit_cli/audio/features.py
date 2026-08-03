"""F0 (pitch) and RMS (volume) feature extraction with rolling baselines.

Two consumers with different window granularity, both implemented here so
the extraction code (and its baseline-window definition) is shared:
  - score.combat_score: per-second commentary volume/pitch spike signal
  - transcribe.filler_classifier: per-WORD gap/pitch/volume features for A/B
    classification (word-aligned windows, not fixed 1s buckets)
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.models import CommentaryFeatureWindow, Word


def extract_commentary_features(audio_path: Path, window_seconds: float) -> list[CommentaryFeatureWindow]:
    """Compute RMS/F0 mean per ``window_seconds`` bucket, with a rolling
    baseline (trailing window, excludes the current bucket) for spike-ratio
    computation downstream.
    """
    raise NotImplementedError


def extract_word_features(audio_path: Path, words: list[Word]) -> dict[str, tuple[float, float, float]]:
    """Per word (keyed by ``f"{word.start}:{word.end}"``), compute
    ``(gap_before_seconds, pitch_ratio, rms_ratio)`` against the immediately
    preceding word/silence window. Used by transcribe.filler_classifier.
    """
    raise NotImplementedError
