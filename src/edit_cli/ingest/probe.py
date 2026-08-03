"""ffprobe wrapper: reads container metadata needed before any analysis starts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VideoMeta:
    width: int
    height: int
    fps: float
    duration_seconds: float
    has_separate_tracks: bool
    audio_track_count: int


def probe(input_path: Path) -> VideoMeta:
    """Run ffprobe on ``input_path`` and return its stream metadata.

    Raises FileNotFoundError if ffmpeg/ffprobe is not on PATH, and
    ``ValueError`` if the container has no video stream or an unsupported
    resolution (i.e. no matching entry in config/rois.yaml — checked later
    by vision.roi_calibration, not here; this function is resolution-agnostic).
    """
    raise NotImplementedError
