"""Interactive facecam-mask selection.

Every streamer's webcam overlay sits in a different spot (and some use a
chroma-keyed / AI-segmented cutout instead of a solid rectangle), so there's
no single default worth hardcoding — the user picks it once per recording
setup with this tool, then reuses the printed value via
``analyze/run --facecam-mask``.

NOT a video preview/player (spec explicitly excludes that — Premiere's job).
This opens exactly ONE still frame in a local OpenCV window for a single
rectangle-drag selection, then exits. No playback, no scrubbing.

Known limitation: the result is a RECTANGLE. A chroma-keyed or
AI-background-removed facecam (a person-shaped cutout, not a solid box) is
only approximated — the bounding rectangle over-excludes the padding around
the silhouette. Per-pixel person segmentation is out of scope for Phase 1;
if that padding turns out to eat too much real HUD, the fix is picking a
tighter rectangle around just the actually-opaque part, not a smarter
selector.
"""

from __future__ import annotations

import numpy as np


def select_facecam_mask(frame: np.ndarray, window_name: str = "edit-cli: drag a box over the facecam, then ENTER (Esc = no mask)") -> tuple[float, float, float, float] | None:
    """Open a local ``cv2.selectROI`` window on ``frame`` for the user to
    drag a box over their facecam overlay.

    Returns:
        Fractional ``(x, y, w, h)`` in [0, 1], or ``None`` if the user
        cancels (Esc, or a zero-area selection) meaning "no mask" — this is
        deliberately how the caller (cli.py: calibrate_facecam) distinguishes
        "no facecam present" from a real mask.
    """
    raise NotImplementedError
