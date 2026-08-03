"""Seconds <-> frame <-> SMPTE timecode conversions.

The single source of truth for frame-accuracy: any module that needs to
snap a float-seconds value to a frame boundary (segment_builder,
keep_cut_decision, fcpxml_export) calls through here rather than doing its
own `round(t * fps)`, so the rounding rule is defined exactly once.
"""

from __future__ import annotations


def seconds_to_frame(seconds: float, fps: float) -> int:
    """Rounds to nearest frame (round-half-up), never truncates."""
    raise NotImplementedError


def frame_to_seconds(frame: int, fps: float) -> float:
    raise NotImplementedError


def seconds_to_smpte(seconds: float, fps: float) -> str:
    """``HH:MM:SS:FF``. Non-integer fps (e.g. 59.94) uses drop-frame timecode."""
    raise NotImplementedError


def snap_to_frame(seconds: float, fps: float) -> float:
    """``frame_to_seconds(seconds_to_frame(seconds, fps), fps)`` — the
    canonical snap-to-frame-boundary operation used before any value is
    written to XML/EDL.
    """
    raise NotImplementedError
