"""Startup HUD calibration: turns config/rois.yaml fractional boxes into
absolute pixel ROIs for THIS video, via template matching.

No other module may compute or hardcode pixel coordinates — every consumer
(hud_reader, killfeed, player_count, build_edit_ui) takes a ``CalibratedRois``
instance produced here.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from edit_cli.config.schema import ResolutionRoiConfig


@dataclass(frozen=True)
class PixelBox:
    x: int
    y: int
    w: int
    h: int


@dataclass(frozen=True)
class CalibratedRois:
    resolution: tuple[int, int]
    anchor_offset: tuple[int, int]   # detected offset of the template match, for logging/debug
    anchor_confidence: float
    regions: dict[str, PixelBox]


def calibrate(frame: np.ndarray, roi_config: ResolutionRoiConfig, min_confidence: float) -> CalibratedRois:
    """Locate ``roi_config.calibration_template`` in ``frame`` within
    ``roi_config.anchor_search_region``, then derive absolute pixel boxes for
    every entry in ``roi_config.regions`` relative to the matched anchor.

    Args:
        frame: a representative decoded frame (BGR), typically sampled a few
            seconds into the video to skip intro black frames.
        roi_config: the resolution-specific block from config/rois.yaml.
        min_confidence: thresholds.yaml: vision_detection.template_match_min_confidence.

    Raises:
        CalibrationError: if the template match confidence is below
            ``min_confidence`` — surfaced to the CLI with guidance to update
            config/rois.yaml/templates for this HUD layout, never silently
            falls back to raw fractional coordinates.
    """
    raise NotImplementedError


class CalibrationError(RuntimeError):
    """Raised when ROI calibration cannot find its anchor with sufficient confidence."""
