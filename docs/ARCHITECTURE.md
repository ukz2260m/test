# Architecture

## Directory structure

```
edit-cli/
  pyproject.toml
  config/
    rois.yaml               # HUD ROI defs per resolution (fractional coords + calibration template)
    thresholds.yaml         # combat score weights, segment margins, filler thresholds, VAD/audio-event params
    glossary.txt            # Fortnite terms for Whisper initial_prompt
    corrections.yaml        # post-transcription replacement rules
    telop_style.yaml        # ASS styles (normal / emphasis) + emphasis on/off
    profiles/
      default.yaml          # no-op profile (documents override schema)
      highlights_only.yaml  # example: stricter cutting profile
    templates/               # calibration reference images (added during vision impl)
  src/edit_cli/
    cli.py                   # click entrypoints: analyze / export / run
    pipeline.py              # orchestration: wires ingest->vision/audio/transcribe (analyze), score->export (export)
    models.py                 # pydantic models: AnalysisResult, DecisionResult, and their sub-schemas (see docs/DATA_CONTRACTS.md)
    config/
      schema.py               # pydantic models for each config/*.yaml file
      loader.py                # load + validate + profile-merge config, compute fingerprint
    ingest/
      probe.py                 # ffprobe wrapper -> resolution/fps/duration
      ffmpeg_ops.py             # audio extraction, frame sampling via ffmpeg
    vision/
      roi_calibration.py       # template-match calibration -> absolute ROI pixel boxes per video
      hud_reader.py             # HP/shield bar reading + damage popup detection
      killfeed.py                # killfeed OCR/detection (EasyOCR)
      player_count.py            # remaining-player-count OCR (EasyOCR)
      kill_count.py               # own elimination counter OCR (EasyOCR)
      storm_status.py             # zone-timer OCR + storm-damage vignette detection
      build_edit_ui.py           # build/edit UI state-change detection
    audio/
      vad.py                     # voice activity detection -> speech spans
      events.py                   # gunshot/elim/build/hit acoustic event detection
      features.py                  # F0 + RMS feature extraction, rolling baselines
    transcribe/
      whisper_runner.py           # faster-whisper large-v3, word-level timestamps, glossary prompt injection
      glossary.py                  # loads glossary.txt / corrections.yaml, applies post-processing
      filler_classifier.py         # class A/B filler classification (see thresholds.yaml: filler)
    score/
      combat_score.py              # per-second weighted combat score timeline
      segment_builder.py            # margin + merge -> combat_segments
      keep_cut_decision.py          # combat_segments + VAD + silence rule -> kept/cut segments, cut-point snapping
    export/
      fcpxml_export.py              # FCP7 XML / EDL writer (frame-accurate)
      ass_export.py                  # ASS subtitle writer (normal/emphasis styles)
      json_export.py                  # decision.json writer + analysis.json read/write (schema-validated)
    cache/
      analysis_cache.py               # content-hash + config-fingerprint keyed analysis cache
    util/
      logging_setup.py                 # structured logging: module + frame/second context on failure
      progress.py                       # tqdm-based progress bar helpers
      timecode.py                       # seconds<->frame<->SMPTE timecode conversions
  tests/
    ingest/ vision/ audio/ transcribe/ score/ export/ fixtures/
  scripts/
    build_exe.ps1 / build_exe.spec       # PyInstaller packaging (final phase)
  docs/
    ARCHITECTURE.md
    DATA_CONTRACTS.md
```

## Pipeline flow

```
analyze:
  ingest.probe          -> VideoMeta (resolution, fps, duration)
  ingest.ffmpeg_ops      -> extracted audio (wav) + sampled frames (5fps, +detail passes near events)
  vision.roi_calibration -> per-video absolute ROI boxes (from rois.yaml template match)
  vision.*                -> vision_events (hp/shield, damage popups, killfeed, player_count,
                             kill_count, storm_status, build_edit_ui)
  audio.vad + audio.events + audio.features -> speech.vad_segments, audio_events, commentary_features
  transcribe.whisper_runner -> speech.words (word-level, glossary-biased)
  transcribe.glossary        -> corrected_word per word (corrections.yaml)
  transcribe.filler_classifier -> filler_analysis (class A/B + features + rule_fired)
  => models.AnalysisResult -> analysis.json (cached by content+config hash)

export:
  models.AnalysisResult (load + validate analysis.json)
  score.combat_score      -> combat_score_timeline (thresholds.yaml weights; kill_count weighted
                             like HP/shield loss; storm_status "in_storm" buckets suppress
                             hp_shield_delta/hit_sound contributions instead of counting as combat)
  score.segment_builder    -> combat_segments (margins + merge)
  score.keep_cut_decision   -> kept_segments / cut_segments (never mid-speech; drops class-A fillers; keeps class-B)
  => models.DecisionResult
  export.fcpxml_export      -> output.xml (frame-accurate, from kept_segments)
  export.ass_export          -> output.ass (words minus dropped class-A fillers, emphasis on class-B)
  export.json_export          -> decision.json
```

## Key invariants enforced across module boundaries

1. **No hardcoded coordinates or magic numbers.** Every threshold/coordinate
   is read from `config/*.yaml` via `config.loader`. Code review should reject
   any literal that isn't a mathematical/algorithmic constant (e.g. `0.5` for
   a probability midpoint is fine; a pixel offset is not).
2. **analyze never sees thresholds; export never touches the video.** This is
   what makes "adjust `combat_threshold` and re-run" cheap (spec requirement).
3. **Cut points never fall inside a word span or VAD speech span.**
   `score.keep_cut_decision` is the single place boundary-snapping happens;
   no other module invents a cut point.
4. **Every automated decision is traceable.** `filler_analysis[].rule_fired`
   and `combat_score_timeline[].contributions` exist so a human can audit
   *why* a word was dropped or a second was called "combat" without reading
   code.
5. **Each module is independently runnable/testable** — no module reaches
   into another module's internals; they only exchange the pydantic models
   in `models.py`.
6. **OCR engine: EasyOCR** for all text/digit ROIs (killfeed, player_count,
   kill_count, storm_timer). HP/shield bars are NOT OCR'd — they're read as
   bar-fill-length (pixel/color measurement), which is faster and more
   robust than reading numbers off a bar even if the HUD displays them.
