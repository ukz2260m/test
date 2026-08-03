"""ASS subtitle writer.

Timestamps are written against the ORIGINAL source timeline, not the
post-cut output timeline — Premiere re-times the imported XML sequence
against source media, and the ASS track is expected to be dropped onto the
same cut sequence, so it must share the source's absolute time base. If a
future revision needs output-timeline ASS instead, that remapping belongs
here (kept_segments defines the mapping) — not sprinkled elsewhere.
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.config.schema import TelopStyleConfig
from edit_cli.models import FillerDecision, Word


def write_ass(
    words: list[Word],
    filler_decisions: list[FillerDecision],
    style: TelopStyleConfig,
    out_path: Path,
) -> None:
    """Render ``words`` into an ASS file, grouped into readable telop spans.

    Words whose ``FillerDecision.action == "dropped"`` are excluded from the
    rendered text. Spans containing any word with ``action ==
    "kept_emphasized"`` use ``style.styles["emphasis"]``
    (only if ``style.emphasis["enabled"]``, else falls back to "normal");
    all other spans use ``style.styles["normal"]``.
    """
    raise NotImplementedError
