"""faster-whisper large-v3 word-level transcription, glossary-biased.

Runs only within/near VAD speech spans (audio.vad output), not blindly over
the whole file, to keep 10-minute-video processing time practical.
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.models import VadSegment, Word


def build_initial_prompt(glossary_terms: list[str]) -> str:
    """Join glossary terms into a Whisper ``initial_prompt`` string.

    Kept under Whisper's practical prompt-length budget: if
    ``glossary_terms`` is large, this truncates deterministically (documented
    in the implementation) rather than silently dropping random entries.
    """
    raise NotImplementedError


def transcribe(
    audio_path: Path,
    vad_segments: list[VadSegment],
    initial_prompt: str,
    model_name: str = "large-v3",
) -> list[Word]:
    """Run word-level Whisper transcription restricted to ``vad_segments``.

    Every word carries Whisper's per-word confidence unmodified —
    thresholding/filtering on confidence is NOT done here (spec: low
    confidence words are kept and surfaced, not dropped). ``raw_word`` ==
    ``corrected_word`` at this stage; correction happens in
    ``transcribe.glossary.apply_corrections``.
    """
    raise NotImplementedError
