"""HP/shield bar reading and damage-popup detection.

The strongest single combat signal (spec: "被弾＝強シグナル"). Runs the
coarse pass at ``vision_detection.sample_fps`` across the whole video, then
re-runs at ``vision_detection.detail_fps`` in a window around any detected
bar-length change or popup, per ``vision_detection.detail_window_seconds``.
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
    """Measure HP/shield bar fill fraction per sampled frame.

    A sample is only worth emitting when it changes by more than
    ``config.hp_bar_change_threshold`` / ``shield_bar_change_threshold``
    from the previous sample (otherwise the timeline is dominated by noise);
    callers doing the detail re-pass rely on this to find the precise
    damage instant within the coarse window.
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
