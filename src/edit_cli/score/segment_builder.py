"""Combat score timeline -> merged, margined combat segments."""

from __future__ import annotations

from edit_cli.config.schema import SegmentBuilderConfig
from edit_cli.models import CombatScoreSample, CombatSegment


def build_combat_segments(
    timeline: list[CombatScoreSample],
    combat_threshold: float,
    config: SegmentBuilderConfig,
) -> list[CombatSegment]:
    """Threshold ``timeline`` at ``combat_threshold`` into raw runs, expand
    each run by ``config.pre_margin_seconds`` / ``post_margin_seconds``
    (clamped to [0, duration]), then merge any two segments whose gap is
    < ``config.merge_gap_seconds``.

    ``reason`` on each output segment names the dominant contribution(s)
    (from ``CombatScoreSample.contributions``) across the run, for
    decision.json auditability.
    """
    raise NotImplementedError
