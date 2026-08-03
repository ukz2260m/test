"""Killfeed appearance detection (top-right elimination log entries)."""

from __future__ import annotations

from collections.abc import Iterable

from edit_cli.config.schema import VisionDetectionConfig
from edit_cli.ingest.ffmpeg_ops import SampledFrame
from edit_cli.models import KillfeedEvent
from edit_cli.vision.roi_calibration import CalibratedRois


def detect_killfeed(
    frames: Iterable[SampledFrame],
    rois: CalibratedRois,
    config: VisionDetectionConfig,
) -> list[KillfeedEvent]:
    """Detect new killfeed entries appearing in the ``killfeed`` ROI.

    Emits one event per NEW entry (de-duplicated against the previous
    sample's OCR'd text via fuzzy match, not raw pixel diff — killfeed
    entries scroll/fade). ``text`` is the raw OCR'd line for audit purposes;
    downstream scoring only uses presence/timing, not content.

    If ``rois.facecam_mask`` occludes the ``killfeed`` region (see
    ``roi_calibration.is_occluded``), no events are emitted for that frame
    rather than OCR'ing webcam pixels as text.
    """
    raise NotImplementedError
