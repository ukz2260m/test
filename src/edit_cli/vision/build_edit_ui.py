"""Building/editing UI state-change detection (piece selector HUD)."""

from __future__ import annotations

from collections.abc import Iterable

from edit_cli.config.schema import VisionDetectionConfig
from edit_cli.ingest.ffmpeg_ops import SampledFrame
from edit_cli.models import BuildEditUiEvent
from edit_cli.vision.roi_calibration import CalibratedRois


def detect_build_edit_ui(
    frames: Iterable[SampledFrame],
    rois: CalibratedRois,
    config: VisionDetectionConfig,
) -> list[BuildEditUiEvent]:
    """Detect transitions in the ``build_edit_ui`` ROI.

    ``state`` is one of ``"idle" | "building" | "editing"``, inferred from
    which sub-elements of the ROI are highlighted/visible. A weak combat
    signal on its own (spec weight is low) — mainly useful as corroboration
    for gunfights that happen mid-build.
    """
    raise NotImplementedError
