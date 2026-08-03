"""FCP7 XML (and EDL) writer: kept_segments -> a Premiere-importable sequence.

Frame-accurate by construction: all internal segment math is done in
seconds (float) but every value actually written to the XML/EDL is first
snapped to a frame boundary via util.timecode using the source fps, so
Premiere's cut points land exactly on frames (spec acceptance criterion).
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.models import KeptSegment


def write_fcp7_xml(kept_segments: list[KeptSegment], source_path: Path, fps: float, out_path: Path) -> None:
    """Write an FCP7 XML sequence referencing ``source_path`` with one clip
    per ``kept_segments`` entry, in order, back-to-back on the timeline
    (no gaps in the OUTPUT sequence — gaps only existed in the source).
    """
    raise NotImplementedError


def write_edl(kept_segments: list[KeptSegment], source_path: Path, fps: float, out_path: Path) -> None:
    """Write a CMX3600 EDL as an alternative import path."""
    raise NotImplementedError
