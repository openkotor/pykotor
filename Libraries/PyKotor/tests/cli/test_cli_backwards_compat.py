"""Regression tests for CLI backwards compatibility.

Ensures existing commands remain registered and respond to --help after any
shared code or CLI changes (per KotorMCP redesign plan Phase 1.0).
"""

from __future__ import annotations

import argparse

import pytest

from pykotor.cli.argparser import create_parser
from pykotor.cli.dispatch import cli_main


def _get_registered_commands() -> list[str]:
    """Return canonical list of registered subcommand names (no aliases)."""
    parser = create_parser()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            # choices is dict of name -> subparser; use primary names only
            return sorted(action.choices.keys())
    return []


def test_all_commands_have_help() -> None:
    """Every registered subcommand must accept --help without error."""
    top_level_result = cli_main(["--help"])
    assert top_level_result == 0

    commands = _get_registered_commands()
    assert commands, "No subcommands registered"
    for name in commands:
        try:
            result = cli_main([name, "--help"])
            exit_code = result
        except SystemExit as e:
            exit_code = e.code if e.code is not None else 1
        assert exit_code == 0, f"Command '{name}' --help should exit 0, got {exit_code}"


def test_unknown_command_returns_nonzero() -> None:
    """Unknown command causes non-zero exit (argparse exits 2 before dispatch)."""
    with pytest.raises(SystemExit) as exc_info:
        cli_main(["nonexistent-command-xyz"])
    assert exc_info.value.code != 0
