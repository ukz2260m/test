"""Smoke test: the CLI group loads and exposes the three subcommands.

This is intentionally the only test that can pass before module
implementation begins — everything else in tests/<module>/ is added
alongside that module's implementation.
"""

from click.testing import CliRunner

from edit_cli.cli import main


def test_help_lists_subcommands() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    for name in ("analyze", "export", "run"):
        assert name in result.output
