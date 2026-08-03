"""edit-cli entrypoints: analyze / export / run.

Argument parsing and wiring only — all real work happens in pipeline.py and
below. This file is intentionally thin so the CLI surface is stable while
pipeline internals are implemented module by module.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

DEFAULT_CONFIG_DIR = Path("config")
DEFAULT_PROFILE = "default"


@click.group()
def main() -> None:
    """Fortnite gameplay video -> Premiere timeline + subtitles, automated."""


def _common_options(f):
    f = click.option(
        "--config",
        "config_dir",
        type=click.Path(path_type=Path),
        default=DEFAULT_CONFIG_DIR,
        show_default=True,
        help="Path to the config/ directory (rois.yaml, thresholds.yaml, ...).",
    )(f)
    f = click.option(
        "--profile",
        "profile",
        default=DEFAULT_PROFILE,
        show_default=True,
        help="Profile name under config/profiles/<name>.yaml.",
    )(f)
    f = click.option(
        "--dry-run",
        is_flag=True,
        default=False,
        help="Validate config/inputs and print the planned actions without writing outputs.",
    )(f)
    return f


def _parse_facecam_mask(ctx, param, value: str | None) -> tuple[float, float, float, float] | None:
    if value is None:
        return None
    try:
        x, y, w, h = (float(v) for v in value.split(","))
    except ValueError as exc:
        raise click.BadParameter("expected 4 comma-separated fractions: x,y,w,h (each in [0,1])") from exc
    if not all(0.0 <= v <= 1.0 for v in (x, y, w, h)):
        raise click.BadParameter("x,y,w,h must each be within [0,1]")
    return (x, y, w, h)


_FACECAM_MASK_OPTION = click.option(
    "--facecam-mask",
    "facecam_mask",
    default=None,
    callback=_parse_facecam_mask,
    metavar="X,Y,W,H",
    help="Fractional [0,1] webcam-overlay box (e.g. streamer face cam) to exclude from HUD reads, e.g. 0.0,0.75,0.22,0.25.",
)


@main.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@_common_options
@click.option("--out", "out_path", type=click.Path(path_type=Path), default=None, help="Output analysis.json path (default: <input>.analysis.json).")
@click.option("--no-cache", is_flag=True, default=False, help="Force re-analysis even if a cache hit exists.")
@_FACECAM_MASK_OPTION
def analyze(
    input_path: Path,
    config_dir: Path,
    profile: str,
    dry_run: bool,
    out_path: Path | None,
    no_cache: bool,
    facecam_mask: tuple[float, float, float, float] | None,
) -> None:
    """Analyze INPUT_PATH (mp4) and write an intermediate analysis.json. No thresholds are applied here."""
    raise NotImplementedError


@main.command(name="calibrate-facecam")
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.option("--frame-time", type=float, default=30.0, show_default=True, help="Seconds into the video to grab the reference frame from.")
@click.option("--out", "out_path", type=click.Path(path_type=Path), default=None, help="Also write the resulting x,y,w,h to this file (one line, comma-separated).")
def calibrate_facecam(input_path: Path, frame_time: float, out_path: Path | None) -> None:
    """Interactively pick the facecam-overlay rectangle from one frame of INPUT_PATH.

    Opens a local window on a single extracted frame (no playback). Drag a
    box over the webcam overlay and press ENTER/SPACE to confirm, or Esc if
    there's no overlay to mask. Prints the resulting value to reuse as
    `--facecam-mask` on `analyze`/`run`.
    """
    raise NotImplementedError


@main.command(name="export")
@click.argument("analysis_path", type=click.Path(exists=True, path_type=Path))
@_common_options
@click.option("--out-dir", type=click.Path(path_type=Path), default=None, help="Output directory for xml/ass/decision.json (default: alongside analysis_path).")
@click.option("--format", "timeline_format", type=click.Choice(["fcp7xml", "edl"]), default="fcp7xml", show_default=True)
def export(analysis_path: Path, config_dir: Path, profile: str, dry_run: bool, out_dir: Path | None, timeline_format: str) -> None:
    """Generate XML/EDL + ASS + decision.json from an existing analysis.json. Never re-analyzes the source video."""
    raise NotImplementedError


@main.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@_common_options
@click.option("--out-dir", type=click.Path(path_type=Path), default=None)
@click.option("--no-cache", is_flag=True, default=False)
@click.option("--format", "timeline_format", type=click.Choice(["fcp7xml", "edl"]), default="fcp7xml", show_default=True)
@_FACECAM_MASK_OPTION
def run(
    input_path: Path,
    config_dir: Path,
    profile: str,
    dry_run: bool,
    out_dir: Path | None,
    no_cache: bool,
    timeline_format: str,
    facecam_mask: tuple[float, float, float, float] | None,
) -> None:
    """analyze + export in one step."""
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
