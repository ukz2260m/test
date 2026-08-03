"""Structured logging: every failure log line carries which module and which
frame/second/word it was processing, per the spec's failure-diagnosis
requirement.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from collections.abc import Iterator


def configure_logging(verbose: bool = False, log_file: str | None = None) -> None:
    raise NotImplementedError


@contextmanager
def stage_context(module: str, **context: object) -> Iterator[None]:
    """Binds ``module`` plus arbitrary context (e.g. ``t=12.4``,
    ``frame_index=744``) onto any exception raised within the block, so the
    top-level CLI handler can report exactly where processing failed instead
    of a bare traceback.

    Usage::

        with stage_context("vision.hud_reader", t=frame.t):
            read_hp_shield_bar(frame)
    """
    raise NotImplementedError
