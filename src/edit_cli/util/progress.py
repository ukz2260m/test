"""tqdm-based progress bar helpers, one per pipeline stage.

Centralized so every long-running loop (frame sampling, VAD, Whisper,
scoring) reports progress the same way, and so it can be disabled
uniformly (e.g. under `--dry-run` or when stdout isn't a TTY).
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


def track(iterable: Iterable[T], desc: str, total: int | None = None) -> Iterator[T]:
    raise NotImplementedError
