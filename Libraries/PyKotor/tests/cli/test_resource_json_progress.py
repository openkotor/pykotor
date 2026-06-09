"""Regression tests for JSON export progress reporting in CI/automation."""

from __future__ import annotations

import io
import logging

import pytest

from pykotor.tools.resource_json import (
    _ExportProgressReporter,
    _format_progress_bar,
    _supports_live_progress,
)


class _FakeTty(io.StringIO):
    def isatty(self) -> bool:
        return True


def test_format_progress_bar_clamps_percent() -> None:
    assert _format_progress_bar(-5.0) == "-" * len(_format_progress_bar(50.0))
    assert _format_progress_bar(150.0) == "#" * len(_format_progress_bar(50.0))


@pytest.mark.parametrize("env_name", ["CI", "GITHUB_ACTIONS"])
@pytest.mark.parametrize("env_value", ["true", "1", "yes", " TRUE "])
def test_supports_live_progress_disabled_in_automation_env(
    monkeypatch: pytest.MonkeyPatch,
    env_name: str,
    env_value: str,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv(env_name, env_value)
    assert _supports_live_progress(_FakeTty()) is False


def test_supports_live_progress_enabled_for_tty_outside_ci(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTty()) is True


def test_export_progress_reporter_logs_instead_of_live_updates_in_ci(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setenv("CI", "true")
    caplog.set_level(logging.INFO)
    reporter = _ExportProgressReporter(
        logger=logging.getLogger("test_resource_json_progress"),
        total_resources=10,
        stream=_FakeTty(),
    )

    assert reporter.live_updates is False
    reporter.update(1, "texture.tpc")
    assert caplog.records
    assert "texture.tpc" in caplog.records[0].message
