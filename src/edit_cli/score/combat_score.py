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

    ``vision_events.kill_count`` increases are weighted like HP/shield loss
    (``weights.vision.kill_count_increase``) — the player's own elimination
    is as strong a combat signal as taking damage.

    ``vision_events.storm_status`` is NOT itself weighted into the sum; it's
    read to find buckets overlapping a ``"in_storm"`` phase and multiply
    THOSE buckets' ``hp_shield_delta`` and ``hit_sound`` raw contributions by
    ``config.storm_damage_suppression_factor`` before weighting, so storm
    damage taken while rotating isn't misread as a firefight.
    """
    raise NotImplementedError
