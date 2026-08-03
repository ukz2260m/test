"""Pydantic models validating each config/*.yaml file's shape.

Every module that reads a threshold, weight, or ROI does so through an
instance of one of these models (obtained via ``config.loader.load_config``),
never by indexing a raw dict. Keeps ``config/*.yaml`` typo-safe and gives a
single place to see every tunable the system has.
"""

from __future__ import annotations

from pydantic import BaseModel, model_validator


# --------------------------------------------------------------------------
# rois.yaml
# --------------------------------------------------------------------------


class RoiBox(BaseModel):
    """Fractional [x, y, w, h], relative to full frame, 0.0-1.0.

    Authored in YAML as a plain 4-element list (``[x, y, w, h]``) for
    readability; accepted here as either that list form or an explicit
    ``{x, y, w, h}`` mapping.
    """

    x: float
    y: float
    w: float
    h: float

    @model_validator(mode="before")
    @classmethod
    def _from_sequence(cls, value: object) -> object:
        if isinstance(value, (list, tuple)):
            if len(value) != 4:
                raise ValueError("RoiBox sequence must have exactly 4 elements: [x, y, w, h]")
            x, y, w, h = value
            return {"x": x, "y": y, "w": w, "h": h}
        return value


class ResolutionRoiConfig(BaseModel):
    calibration_template: str
    anchor_search_region: RoiBox
    regions: dict[str, RoiBox]


class RoisConfig(BaseModel):
    schema_version: int
    resolutions: dict[str, ResolutionRoiConfig]


# --------------------------------------------------------------------------
# thresholds.yaml
# --------------------------------------------------------------------------


class CombatScoreWeights(BaseModel):
    vision: dict[str, float]
    audio: dict[str, float]
    commentary: dict[str, float]


class CombatScoreNormalization(BaseModel):
    method: str
    sigmoid_k: float


class CombatScoreConfig(BaseModel):
    window_seconds: float
    smoothing_seconds: float
    weights: CombatScoreWeights
    normalization: CombatScoreNormalization
    combat_threshold: float
    storm_damage_suppression_factor: float


class SegmentBuilderConfig(BaseModel):
    pre_margin_seconds: float
    post_margin_seconds: float
    merge_gap_seconds: float


class KeepCutDecisionConfig(BaseModel):
    min_cut_silence_seconds: float
    cut_point_safety_margin_seconds: float


class GunshotOnsetConfig(BaseModel):
    band_hz: tuple[float, float]
    onset_sensitivity: float
    min_gap_seconds: float


class SoundMatchConfig(BaseModel):
    match_threshold: float


class CommentaryEventConfig(BaseModel):
    volume_spike_ratio: float
    pitch_spike_ratio: float


class AudioEventsConfig(BaseModel):
    gunshot_onset: GunshotOnsetConfig
    elim_sound: SoundMatchConfig
    build_sound: SoundMatchConfig
    hit_sound: SoundMatchConfig
    commentary: CommentaryEventConfig


class VadConfig(BaseModel):
    aggressiveness: int
    min_speech_seconds: float
    min_silence_seconds: float
    speech_pad_seconds: float


class FillerConfig(BaseModel):
    enabled: bool
    reaction_gap_threshold: float
    pitch_rise_threshold: float
    volume_spike_ratio: float
    combat_score_bias_threshold: float
    ambiguous_action: str  # "keep" | "remove"
    filler_words: list[str]
    reaction_words: list[str]


class VisionDetectionConfig(BaseModel):
    sample_fps: float
    detail_fps: float
    detail_window_seconds: float
    hp_bar_change_threshold: float
    shield_bar_change_threshold: float
    shield_hue_range: tuple[float, float]
    health_hue_range: tuple[float, float]
    min_saturation: float
    ocr_min_confidence: float
    template_match_min_confidence: float


class StormDetectionConfig(BaseModel):
    timer_ocr_min_confidence: float
    vignette_purple_area_ratio_threshold: float
    vignette_min_gap_seconds: float


class ThresholdsConfig(BaseModel):
    schema_version: int
    combat_score: CombatScoreConfig
    segment_builder: SegmentBuilderConfig
    keep_cut_decision: KeepCutDecisionConfig
    audio_events: AudioEventsConfig
    vad: VadConfig
    filler: FillerConfig
    vision_detection: VisionDetectionConfig
    storm_detection: StormDetectionConfig


# --------------------------------------------------------------------------
# corrections.yaml
# --------------------------------------------------------------------------


class CorrectionRule(BaseModel):
    type: str  # "literal" | "regex"
    pattern: str
    replacement: str
    word_boundary: bool = False


class CorrectionsConfig(BaseModel):
    schema_version: int
    rules: list[CorrectionRule]


# --------------------------------------------------------------------------
# telop_style.yaml
# --------------------------------------------------------------------------


class AssStyle(BaseModel):
    fontname: str
    fontsize: int
    primary_colour: str
    outline_colour: str
    back_colour: str
    bold: int
    italic: int
    outline: int
    shadow: int
    alignment: int
    margin_l: int
    margin_r: int
    margin_v: int
    extra_override_tags: str = ""


class TelopStyleConfig(BaseModel):
    schema_version: int
    emphasis: dict[str, bool]  # {"enabled": bool}
    styles: dict[str, AssStyle]  # keys: "normal", "emphasis"


# --------------------------------------------------------------------------
# Glossary (plain text, not YAML) — parsed shape only
# --------------------------------------------------------------------------


class GlossaryConfig(BaseModel):
    terms: list[str]


# --------------------------------------------------------------------------
# Aggregate: everything a pipeline run needs
# --------------------------------------------------------------------------


class ResolvedConfig(BaseModel):
    """Result of loading + profile-merging all config/*.yaml files.

    This is what ``config.loader.load_config`` returns and what every other
    module accepts as a parameter — never a raw path or dict.
    """

    rois: RoisConfig
    thresholds: ThresholdsConfig
    corrections: CorrectionsConfig
    telop_style: TelopStyleConfig
    glossary: GlossaryConfig
    profile_name: str
    fingerprint: str  # hash of all resolved config content, used for cache keys
