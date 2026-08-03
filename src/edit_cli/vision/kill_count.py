"""Own elimination counter OCR (small digit readout near the HP bar).

Distinct from vision.killfeed: killfeed logs eliminations by anyone that
appear in the on-screen feed (short-lived, scrolling), this reads the
persistent "how many eliminations do I have this match" counter. An
increase here is treated as combat-strength as HP/shield loss (weights.
vision.kill_count_increase in thresholds.yaml).
"""

from __future__ import annotations

from collections.abc import Iterable

from edit_cli.config.schema import VisionDetectionConfig
from edit_cli.ingest.ffmpeg_ops import SampledFrame
from edit_cli.models import KillCountSample
from edit_cli.vision.roi_calibration import CalibratedRois


def read_kill_count(
    frames: Iterable[SampledFrame],
    rois: CalibratedRois,
    config: VisionDetectionConfig,
) -> list[KillCountSample]:
    """OCR (EasyOCR) the ``kill_count`` ROI on each frame.

    Same monotonic-guard as player_count, inverted: a reading that DECREASES
    from the previous one is an OCR misread (this counter never decreases
    within a match) and is discarded rather than emitted.
    """
    raise NotImplementedError
