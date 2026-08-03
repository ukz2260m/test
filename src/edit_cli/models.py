"""Shared data contracts exchanged between pipeline stages.

These pydantic models are the ONLY way modules pass analysis/decision data
to each other and to disk (``analysis.json`` / ``decision.json``). See
``docs/DATA_CONTRACTS.md`` for the authoritative schema description and
worked examples.

Nothing in here performs analysis; this module is pure data shape.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

ANALYSIS_SCHEMA_VERSION = 1
DECISION_SCHEMA_VERSION = 1

FillerClass = Literal["A", "B"]


# --------------------------------------------------------------------------
# analysis.json
# --------------------------------------------------------------------------


class VideoMeta(BaseModel):
    source_path: str
    source_sha256: str
    resolution: tuple[int, int]
    fps: float
    duration_seconds: float
    analyzed_at: str
    tool_version: str
    config_fingerprint: str


class HpShieldSample(BaseModel):
    t: float
    hp: float
    shield: float
    delta_hp: float
    delta_shield: float
    confidence: float


class DamagePopupEvent(BaseModel):
    t: float
    roi: str
    confidence: float
    value: int | None = None


class KillfeedEvent(BaseModel):
    t: float
    text: str
    confidence: float


class PlayerCountSample(BaseModel):
    t: float
    count: int
    confidence: float


class KillCountSample(BaseModel):
    """Own elimination counter (distinct from ``killfeed``, which logs
    eliminations by anyone visible in the killfeed, not just the player)."""

    t: float
    count: int
    confidence: float


StormPhase = Literal["safe", "zone_countdown", "closing", "in_storm"]


class StormStatusEvent(BaseModel):
    """Zone/storm state. ``"in_storm"`` entries are what
    ``score.combat_score`` uses to suppress HP-loss false positives."""

    t: float
    phase: StormPhase
    confidence: float


class BuildEditUiEvent(BaseModel):
    t: float
    state: str
    confidence: float


class VisionEvents(BaseModel):
    hp_shield: list[HpShieldSample] = []
    damage_popups: list[DamagePopupEvent] = []
    killfeed: list[KillfeedEvent] = []
    player_count: list[PlayerCountSample] = []
    kill_count: list[KillCountSample] = []
    storm_status: list[StormStatusEvent] = []
    build_edit_ui: list[BuildEditUiEvent] = []


class AcousticEvent(BaseModel):
    t: float
    confidence: float


class CommentaryFeatureWindow(BaseModel):
    t_start: float
    t_end: float
    rms: float
    rms_baseline: float
    f0_mean: float
    f0_baseline: float


class AudioEvents(BaseModel):
    gunshot_onsets: list[AcousticEvent] = []
    elim_sound: list[AcousticEvent] = []
    build_sound: list[AcousticEvent] = []
    hit_sound: list[AcousticEvent] = []
    commentary_features: list[CommentaryFeatureWindow] = []


class VadSegment(BaseModel):
    start: float
    end: float


class Word(BaseModel):
    word: str
    start: float
    end: float
    confidence: float
    raw_word: str
    corrected_word: str


class SpeechResult(BaseModel):
    vad_segments: list[VadSegment] = []
    words: list[Word] = []


class FillerFeatures(BaseModel):
    gap_before: float
    pitch_ratio: float
    rms_ratio: float
    combat_score_at_t: float


class FillerAnalysisEntry(BaseModel):
    word: str
    start: float
    end: float
    cls: FillerClass
    features: FillerFeatures
    rule_fired: str

    model_config = {"populate_by_name": True}


class AnalysisResult(BaseModel):
    schema_version: int = ANALYSIS_SCHEMA_VERSION
    meta: VideoMeta
    vision_events: VisionEvents
    audio_events: AudioEvents
    speech: SpeechResult
    filler_analysis: list[FillerAnalysisEntry] = []


# --------------------------------------------------------------------------
# decision.json
# --------------------------------------------------------------------------


class CombatScoreSample(BaseModel):
    t: float
    score: float
    contributions: dict[str, float]


class CombatSegment(BaseModel):
    start: float
    end: float
    reason: str


class KeptSegment(BaseModel):
    start: float
    end: float
    reason: Literal["combat", "speech"]
    source_combat_segment: int | None = None
    source_vad_segment: int | None = None


class CutSegment(BaseModel):
    start: float
    end: float
    reason: str


class FillerDecision(BaseModel):
    word: str
    start: float
    end: float
    cls: FillerClass
    action: Literal["dropped", "kept_plain", "kept_emphasized"]
    rule_fired: str

    model_config = {"populate_by_name": True}


class ConfigUsed(BaseModel):
    profile: str
    thresholds_fingerprint: str


class DecisionResult(BaseModel):
    schema_version: int = DECISION_SCHEMA_VERSION
    source_analysis: str
    config_used: ConfigUsed
    combat_score_timeline: list[CombatScoreSample] = []
    combat_segments: list[CombatSegment] = []
    kept_segments: list[KeptSegment] = []
    cut_segments: list[CutSegment] = []
    filler_decisions: list[FillerDecision] = []
