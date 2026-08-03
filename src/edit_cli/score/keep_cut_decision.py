"""Final keep/cut segment list: combat_segments + speech (VAD) - long
non-combat silence, with cut points snapped outside any word/VAD span.

This is the single place a cut point is ever decided. Spec invariant: 0
occurrences of a cut point falling inside a word span, verified here by
construction (snap outward), not by post-hoc validation elsewhere.
"""

from __future__ import annotations

from edit_cli.config.schema import KeepCutDecisionConfig
from edit_cli.models import CombatSegment, CutSegment, KeptSegment, VadSegment, Word


def build_keep_cut_segments(
    combat_segments: list[CombatSegment],
    vad_segments: list[VadSegment],
    words: list[Word],
    duration_seconds: float,
    config: KeepCutDecisionConfig,
) -> tuple[list[KeptSegment], list[CutSegment]]:
    """Union ``combat_segments`` and ``vad_segments`` into keep regions;
    the remaining gaps become cut regions only where a gap's length >=
    ``config.min_cut_silence_seconds`` (shorter gaps are folded into the
    adjacent kept region instead of producing a sub-threshold micro-cut).

    Every keep/cut boundary is then snapped outward by at least
    ``config.cut_point_safety_margin_seconds`` from the nearest word's
    ``[start, end]`` (never inward, never truncating a word) before being
    returned. Each ``KeptSegment`` records whether it originated from a
    combat segment or a VAD segment (or both) via ``reason`` +
    ``source_combat_segment`` / ``source_vad_segment``.
    """
    raise NotImplementedError
