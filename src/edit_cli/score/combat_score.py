"""Per-second weighted combat score timeline.

Pure function of ``AnalysisResult`` + ``ThresholdsConfig`` — this is what
makes re-scoring after a threshold edit cheap (no re-analysis). Every output
sample records its per-signal ``contributions`` so decision.json stays
auditable (spec requirement).
"""

from __future__ import annotations

from edit_cli.config.schema import CombatScoreConfig
from edit_cli.models import AudioEvents, CombatScoreSample, VisionEvents


def compute_combat_score_timeline(
    vision_events: VisionEvents,
    audio_events: AudioEvents,
    duration_seconds: float,
    config: CombatScoreConfig,
) -> list[CombatScoreSample]:
    """Bucket every signal into ``config.window_seconds`` buckets spanning
    ``[0, duration_seconds)``, normalize each raw per-bucket signal value via
    ``config.normalization``, apply ``config.weights``, sum, smooth over
    ``config.smoothing_seconds``, and clamp to [0, 1].

    No single signal is allowed to saturate the score alone by construction
    only insofar as weights are configured that way in thresholds.yaml —
    this function applies whatever weights it's given without an implicit
    single-signal override (spec: "単一シグナルに依存しないこと" is a
    config/weighting discipline, not a hardcoded rule here).
    """
    raise NotImplementedError
