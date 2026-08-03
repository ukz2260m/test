# Data contracts

Two JSON documents flow between `analyze` and `export`. Both are versioned
(`schema_version`) so `export` can reject a stale `analysis.json` produced by
an older analyzer instead of failing confusingly deep in the pipeline.

```
edit-cli analyze input.mp4  --config config/ --profile default
    │
    ▼
analysis.json   (raw signals only — never re-derived without re-running analyze)
    │
    ▼
edit-cli export analysis.json --config config/ --profile default
    │  (re-reads thresholds.yaml / telop_style.yaml fresh every run — cheap, no re-analysis)
    ▼
output.xml / output.ass / decision.json
```

## `analysis.json` (produced by `analyze`, consumed by `export`)

Raw, immutable per-video signals. Contains **no thresholds and no keep/cut
decisions** — those are computed at export time so that re-running `export`
with a different `--config`/`--profile` never requires touching the video
again. Backed by `edit_cli.models.AnalysisResult` (pydantic).

```jsonc
{
  "schema_version": 1,
  "meta": {
    "source_path": "C:/clips/session1.mp4",
    "source_sha256": "…",
    "resolution": [1920, 1080],
    "fps": 60.0,
    "duration_seconds": 612.35,
    "analyzed_at": "2026-08-03T09:00:00Z",
    "tool_version": "0.1.0",
    "config_fingerprint": "…"   // hash of rois.yaml + glossary.txt used, for cache validation
  },
  "vision_events": {
    "hp_shield": [ { "t": 12.4, "hp": 0.62, "shield": 0.10, "delta_hp": -0.18, "delta_shield": 0.0, "confidence": 0.91 } ],
    "damage_popups": [ { "t": 12.5, "roi": "damage_popup", "confidence": 0.77 } ],
    "killfeed": [ { "t": 45.0, "text": "PlayerX eliminated PlayerY", "confidence": 0.85 } ],
    "player_count": [ { "t": 0.0, "count": 72, "confidence": 0.95 } ],
    "kill_count": [ { "t": 45.1, "count": 3, "confidence": 0.9 } ],   // own eliminations, distinct from killfeed
    "storm_status": [ { "t": 120.0, "phase": "in_storm", "confidence": 0.7 } ], // safe | zone_countdown | closing | in_storm
    "build_edit_ui": [ { "t": 30.1, "state": "editing", "confidence": 0.80 } ]
  },
  "audio_events": {
    "gunshot_onsets": [ { "t": 12.41, "confidence": 0.7 } ],
    "elim_sound": [ { "t": 45.02, "confidence": 0.66 } ],
    "build_sound": [ { "t": 30.0, "confidence": 0.6 } ],
    "hit_sound": [ { "t": 12.4, "confidence": 0.72 } ],
    "commentary_features": [ { "t_start": 12.0, "t_end": 13.0, "rms": 0.18, "rms_baseline": 0.09, "f0_mean": 210.0, "f0_baseline": 160.0 } ]
  },
  "speech": {
    "vad_segments": [ { "start": 10.8, "end": 14.2 } ],
    "words": [
      { "word": "え", "start": 12.30, "end": 12.42, "confidence": 0.55, "raw_word": "え", "corrected_word": "え" }
    ]
  },
  "filler_analysis": [
    {
      "word": "え", "start": 12.30, "end": 12.42, "class": "B",
      "features": { "gap_before": 0.45, "pitch_ratio": 1.42, "rms_ratio": 1.6, "combat_score_at_t": 0.71 },
      "rule_fired": "reaction:gap+pitch+combat"
    }
  ]
}
```

Every event carries a `confidence`; nothing is silently dropped for low
confidence at analyze time — thresholding on confidence is an export-time
decision (`thresholds.yaml`) so it can be tuned without re-analysis.

## `decision.json` (produced by `export`, alongside the XML/ASS)

The "why" for every cut and every filler removal, so thresholds can be
re-tuned by inspecting this file instead of re-watching the video. Backed by
`edit_cli.models.DecisionResult`.

```jsonc
{
  "schema_version": 1,
  "source_analysis": "analysis.json",
  "config_used": { "profile": "default", "thresholds_fingerprint": "…" },
  "combat_score_timeline": [ { "t": 12.0, "score": 0.71, "contributions": { "hp_shield_delta": 0.42, "gunshot_onset_density": 0.20, "...": "..." } } ],
  "combat_segments": [ { "start": 10.4, "end": 17.2, "reason": "hp_shield_delta+killfeed" } ],
  "kept_segments": [
    { "start": 10.4, "end": 17.2, "reason": "combat", "source_combat_segment": 0 },
    { "start": 40.0, "end": 48.0, "reason": "speech", "source_vad_segment": 3 }
  ],
  "cut_segments": [ { "start": 17.2, "end": 40.0, "reason": "silence>=1.5s & non-combat" } ],
  "filler_decisions": [
    { "word": "え", "start": 12.30, "end": 12.42, "class": "B", "action": "kept_emphasized", "rule_fired": "reaction:gap+pitch+combat" }
  ]
}
```

## Cache

`edit_cli.cache.analysis_cache` keys a stored `analysis.json` by
`(source_sha256, config_fingerprint, tool_version)`. `analyze` skips
re-running ingest/vision/audio/transcribe if a fresh cache entry exists
unless `--force` is passed (see `cli.py`). `export` never touches the cache
directly — it always trusts the `analysis.json` path given to it.
