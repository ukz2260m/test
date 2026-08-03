"""Remaining-player-count OCR (top-right corner counter)."""

from __future__ import annotations

from collections.abc import Iterable

from edit_cli.config.schema import VisionDetectionConfig
from edit_cli.ingest.ffmpeg_ops import SampledFrame
from edit_cli.models import PlayerCountSample
from edit_cli.vision.roi_calibration import CalibratedRois


def read_player_count(
    frames: Iterable[SampledFrame],
    rois: CalibratedRois,
    config: VisionDetectionConfig,
) -> list[PlayerCountSample]:
    """OCR the remaining-player counter in the ``player_count`` ROI.

    Only emits a sample when the parsed count DECREASES from the previous
    reading (monotonic non-increasing signal by game design) — an increase
    indicates an OCR misread and is discarded rather than emitted with low
    confidence, since it cannot correspond to a real game event.
    """
    raise NotImplementedError
