# edit-cli

Automates the first pass of Fortnite gameplay-commentary video editing:
finds combat scenes, transcribes commentary accurately, and outputs a
Premiere-ready timeline + subtitles.

- Input: recorded MP4 (commentary + game audio, 1080p/1440p, 60fps)
- Output: FCP7 XML (or EDL) for Premiere, ASS subtitles, and a JSON file
  explaining every keep/cut and every filler-word decision
- Windows, uses ffmpeg, GPU optional

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the directory layout
and pipeline, and [`docs/DATA_CONTRACTS.md`](docs/DATA_CONTRACTS.md) for the
`analysis.json` / `decision.json` schemas.

## CLI

```
edit-cli analyze <input.mp4> [--config config/] [--profile default] [--dry-run] [--facecam-mask x,y,w,h]
edit-cli export <analysis.json> [--config config/] [--profile default] [--dry-run]
edit-cli run <input.mp4> [--config config/] [--profile default] [--dry-run] [--facecam-mask x,y,w,h]
edit-cli calibrate-facecam <input.mp4>   # interactively pick --facecam-mask by dragging a box on one frame
```

`analyze` and `export` are separate on purpose: re-tuning `config/thresholds.yaml`
and re-running `export` never re-analyzes the video.

## Status

Scaffold stage: directory structure, config schemas, and module interfaces
are in place; module logic is implemented incrementally (see
`docs/ARCHITECTURE.md` for implementation order: vision → audio →
transcribe → score → export), each confirmed with the user before moving on.

## Development

```
pip install -e ".[dev]"
pytest
```

## Packaging (Windows exe)

Planned final step, via PyInstaller — see `scripts/` once module
implementation is complete.
