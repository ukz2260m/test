"""ffmpeg wrappers: audio extraction and sparse frame sampling.

All heavy lifting (VAD, transcription, HUD reading) happens on extracted
artifacts produced here, never by re-reading the source MP4 repeatedly.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class ExtractedAudio:
    """One audio stream extracted to a working WAV file.

    ``track`` distinguishes game audio / mic when the source has separate
    tracks (spec: "分離トラックがある場合も対応"); ``"mixed"`` when not.
    """

    path: Path
    track: str  # "mixed" | "game" | "mic"
    sample_rate: int


def extract_audio(input_path: Path, work_dir: Path) -> list[ExtractedAudio]:
    """Extract audio track(s) from ``input_path`` into ``work_dir`` as WAV.

    Returns one ``ExtractedAudio`` per detected track (game+mic separately
    when the container provides them; a single "mixed" entry otherwise).
    """
    raise NotImplementedError


@dataclass(frozen=True)
class SampledFrame:
    t: float
    frame: np.ndarray  # BGR, HxWx3


def sample_frames(input_path: Path, fps: float, start: float = 0.0, end: float | None = None) -> Iterator[SampledFrame]:
    """Yield decoded frames from ``input_path`` at ``fps``, in ``[start, end)``.

    Used for both the coarse full-video pass (thresholds.yaml:
    vision_detection.sample_fps) and the detail re-analysis pass around a
    detected event (vision_detection.detail_fps / detail_window_seconds) —
    callers pass a narrow ``[start, end)`` window for the latter.
    """
    raise NotImplementedError
