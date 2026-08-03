"""Storm/safe-zone status detection.

Two independent signals combined into one phase timeline:
  - ``storm_timer`` ROI: OCR'd "MM:SS" zone-countdown text. Present ==
    ``"zone_countdown"`` (circle stationary, about to move); absent while
    otherwise safe == ``"safe"``.
  - ``storm_warning`` ROI (full frame): purple damage-vignette color-mask
    area ratio against a rolling per-video baseline, thresholded by
    ``config.vignette_purple_area_ratio_threshold``. A confirmed hit ==
    ``"in_storm"``, de-duplicated within ``config.vignette_min_gap_seconds``
    (storm damage ticks at a fixed game interval, so repeated detections
    inside one tick interval are the same event, not a new one).
  - ``"closing"`` is inferred as the phase between a countdown reaching 0
    and either the next countdown appearing or an ``"in_storm"`` detection.

This is a corroborating signal, not a primary combat signal: its main
consumer is score.combat_score's storm-damage suppression, not the combat
score weight sum itself.
"""

from __future__ import annotations

from collections.abc import Iterable

from edit_cli.config.schema import StormDetectionConfig
from edit_cli.ingest.ffmpeg_ops import SampledFrame
from edit_cli.models import StormStatusEvent
from edit_cli.vision.roi_calibration import CalibratedRois


def detect_storm_status(
    frames: Iterable[SampledFrame],
    rois: CalibratedRois,
    config: StormDetectionConfig,
) -> list[StormStatusEvent]:
    """Detect zone-timer/storm-damage-vignette state per sampled frame and
    collapse consecutive identical phases into single events (one entry per
    phase TRANSITION, not one per frame).
    """
    raise NotImplementedError
