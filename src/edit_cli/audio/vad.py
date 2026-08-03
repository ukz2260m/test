"""Voice activity detection: raw audio -> speech spans.

Feeds both transcribe.whisper_runner (only run Whisper where there's speech)
and score.keep_cut_decision (cut points must never fall inside a VAD span).
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.config.schema import VadConfig
from edit_cli.models import VadSegment


def detect_speech_segments(audio_path: Path, config: VadConfig) -> list[VadSegment]:
    """Run VAD on ``audio_path`` (mono WAV) and return padded speech spans.

    Adjacent raw spans separated by less than ``config.min_silence_seconds``
    are merged; spans shorter than ``config.min_speech_seconds`` are
    discarded; surviving spans are padded by ``config.speech_pad_seconds`` on
    each side (clamped to audio bounds) before being returned.
    """
    raise NotImplementedError
