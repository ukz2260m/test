"""Startup HUD calibration: turns config/rois.yaml fractional boxes into
absolute pixel ROIs for THIS video, via template matching.

No other module may compute or hardcode pixel coordinates — every consumer
(hud_reader, killfeed, player_count, kill_count, storm_status, build_edit_ui)
takes a ``CalibratedRois`` instance produced here.
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
    facecam_mask: PixelBox | None = None  # from `analyze --facecam-mask`, see apply_facecam_mask


def calibrate(
    frame: np.ndarray,
    roi_config: ResolutionRoiConfig,
    min_confidence: float,
    facecam_mask_fractional: tuple[float, float, float, float] | None = None,
) -> CalibratedRois:
    """Locate ``roi_config.calibration_template`` in ``frame`` within
    ``roi_config.anchor_search_region``, then derive absolute pixel boxes for
    every entry in ``roi_config.regions`` relative to the matched anchor.

    Args:
        frame: a representative decoded frame (BGR), typically sampled a few
            seconds into the video to skip intro black frames.
        roi_config: the resolution-specific block from config/rois.yaml.
        min_confidence: thresholds.yaml: vision_detection.template_match_min_confidence.
        facecam_mask_fractional: optional ``(x, y, w, h)`` in [0,1], from the
            CLI ``--facecam-mask`` option (see cli.py). Converted to a pixel
            ``PixelBox`` the same way every other region is, and attached to
            the returned ``CalibratedRois`` for callers to check via
            ``overlap_ratio``.

    Raises:
        CalibrationError: if the template match confidence is below
            ``min_confidence`` — surfaced to the CLI with guidance to update
            config/rois.yaml/templates for this HUD layout, never silently
            falls back to raw fractional coordinates.
    """
    raise NotImplementedError


class CalibrationError(RuntimeError):
    """Raised when ROI calibration cannot find its anchor with sufficient confidence."""


def overlap_ratio(a: PixelBox, b: PixelBox) -> float:
    """Fraction of ``a``'s area covered by its intersection with ``b``, in [0, 1].

    Used by every vision detector to check ``rois.facecam_mask`` before
    trusting a region's read: ``overlap_ratio(rois.regions["vitals_bar"],
    rois.facecam_mask) > 0`` means at least part of that ROI is a webcam
    overlay, not real HUD pixels.
    """
    raise NotImplementedError


def is_occluded(region: PixelBox, facecam_mask: PixelBox | None, min_overlap: float = 0.15) -> bool:
    """True if ``facecam_mask`` is set and covers more than ``min_overlap`` of
    ``region``. Every vision.* read function calls this before emitting a
    real reading; when True it emits (or skips, per that function's own
    docstring) with confidence forced to 0 instead of trusting webcam pixels.
    """
    raise NotImplementedError
