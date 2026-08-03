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


@main.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@_common_options
@click.option("--out", "out_path", type=click.Path(path_type=Path), default=None, help="Output analysis.json path (default: <input>.analysis.json).")
@click.option("--no-cache", is_flag=True, default=False, help="Force re-analysis even if a cache hit exists.")
def analyze(input_path: Path, config_dir: Path, profile: str, dry_run: bool, out_path: Path | None, no_cache: bool) -> None:
    """Analyze INPUT_PATH (mp4) and write an intermediate analysis.json. No thresholds are applied here."""
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
def run(input_path: Path, config_dir: Path, profile: str, dry_run: bool, out_dir: Path | None, no_cache: bool, timeline_format: str) -> None:
    """analyze + export in one step."""
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
