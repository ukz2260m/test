"""HP/shield bar reading and damage-popup detection.

The strongest single combat signal (spec: "被弾＝強シグナル"). Runs the
coarse pass at ``vision_detection.sample_fps`` across the whole video, then
re-runs at ``vision_detection.detail_fps`` in a window around any detected
bar-length change or popup, per ``vision_detection.detail_window_seconds``.

HP and shield are read from a SINGLE ``vitals_bar`` ROI (not two separately
positioned boxes) by COLOR classification, not by a hardcoded pixel split:
measured samples show shield rendered as a cyan/blue fill and health as a
green-yellow fill, stacked directly on top of each other with no fixed gap.
A position-based split line would be one config edit away from breaking on
any HUD-scale setting or color customization (Fortnite lets players recolor
these bars); classifying each pixel run by hue is robust to both. The two
target hue ranges are still config, not code — see
``thresholds.yaml: vision_detection`` (to be extended with
``shield_hue_range`` / ``health_hue_range`` when this is implemented).
"""

from __future__ import annotations

from collections.abc import Iterable

from edit_cli.config.schema import VisionDetectionConfig
from edit_cli.ingest.ffmpeg_ops import SampledFrame
from edit_cli.models import DamagePopupEvent, HpShieldSample
from edit_cli.vision.roi_calibration import CalibratedRois


def read_hp_shield(
    frames: Iterable[SampledFrame],
    rois: CalibratedRois,
    config: VisionDetectionConfig,
) -> list[HpShieldSample]:
    """Measure shield/health bar fill fraction per sampled frame from the
    ``vitals_bar`` ROI, splitting shield vs. health by color (see module
    docstring) rather than by a fixed sub-region.

    A sample is only worth emitting when it changes by more than
    ``config.hp_bar_change_threshold`` / ``shield_bar_change_threshold``
    from the previous sample (otherwise the timeline is dominated by noise);
    callers doing the detail re-pass rely on this to find the precise
    damage instant within the coarse window.

    If ``rois.facecam_mask`` overlaps ``vitals_bar`` (see
    ``roi_calibration.overlap_ratio``), samples are still emitted but with
    ``confidence`` capped at 0 rather than a color read that may just be
    reading webcam pixels — never silently trusted.
    """
    raise NotImplementedError


def detect_damage_popups(
    frames: Iterable[SampledFrame],
    rois: CalibratedRois,
    config: VisionDetectionConfig,
) -> list[DamagePopupEvent]:
    """Detect damage-number popups within the ``damage_popup`` ROI.

    Popup OCR confidence below ``config.ocr_min_confidence`` is still
    emitted (never silently dropped — spec: keep low-confidence signal,
    threshold at export/score time) with that confidence recorded.
    """
    raise NotImplementedError
