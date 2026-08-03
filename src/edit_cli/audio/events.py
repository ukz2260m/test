"""Acoustic event detection: gunshot onset density, elim/build/hit sounds.

Operates on the GAME audio track when separate tracks are available
(config: ingest.ffmpeg_ops.ExtractedAudio.track == "game"), falling back to
the mixed track otherwise — mixing in commentary voice would corrupt onset
detection.
"""

from __future__ import annotations

from pathlib import Path

from edit_cli.config.schema import AudioEventsConfig
from edit_cli.models import AcousticEvent


def detect_gunshot_onsets(audio_path: Path, config: AudioEventsConfig) -> list[AcousticEvent]:
    """Onset-detect within ``config.gunshot_onset.band_hz``, at
    ``config.gunshot_onset.onset_sensitivity``, de-duplicated within
    ``config.gunshot_onset.min_gap_seconds``. Emits raw onsets — density
    (onsets/second) is computed downstream by score.combat_score, not here.
    """
    raise NotImplementedError


def detect_elim_sound(audio_path: Path, config: AudioEventsConfig) -> list[AcousticEvent]:
    """Match the elimination stinger sound; threshold: config.elim_sound.match_threshold."""
    raise NotImplementedError


def detect_build_sound(audio_path: Path, config: AudioEventsConfig) -> list[AcousticEvent]:
    """Match building-placement sound; threshold: config.build_sound.match_threshold."""
    raise NotImplementedError


def detect_hit_sound(audio_path: Path, config: AudioEventsConfig) -> list[AcousticEvent]:
    """Match the "you hit an enemy" marker sound; threshold: config.hit_sound.match_threshold."""
    raise NotImplementedError
