"""Regression tests for resource JSON export progress reporting."""

from __future__ import annotations

import io
import logging
from typing import TextIO

import pytest

from pykotor.tools.resource_json import (
    _ExportProgressReporter,
    _format_progress_bar,
    _supports_live_progress,
)


class _FakeTTY(io.StringIO):
    def isatty(self) -> bool:  # noqa: D102
        return True


class _FakeNonTTY(io.StringIO):
    def isatty(self) -> bool:  # noqa: D102
        return False


@pytest.mark.parametrize("percent", [0.0, 50.0, 100.0])
def test_format_progress_bar_clamps_and_fills(percent: float) -> None:
    bar = _format_progress_bar(percent)
    assert len(bar) == 24
    assert set(bar) <= {"#", "-"}


@pytest.mark.parametrize("stream", [_FakeTTY(), _FakeNonTTY()])
def test_supports_live_progress_disabled_when_ci_env_set(
    stream: TextIO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CI", "true")
    assert _supports_live_progress(stream) is False


@pytest.mark.parametrize("stream", [_FakeTTY(), _FakeNonTTY()])
def test_supports_live_progress_disabled_when_github_actions_set(
    stream: TextIO,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "1")
    assert _supports_live_progress(stream) is False


def test_supports_live_progress_true_for_tty_without_ci(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTTY()) is True


def test_supports_live_progress_false_for_non_tty_without_ci(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeNonTTY()) is False


def test_export_progress_reporter_logs_to_logger_in_ci(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CI", "true")
    logger = logging.getLogger("test_resource_json_progress")
    reporter = _ExportProgressReporter(
        logger=logger,
        total_resources=2,
        stream=_FakeTTY(),
    )
    assert reporter.live_updates is False

    with caplog.at_level(logging.INFO, logger="test_resource_json_progress"):
        reporter.update(1, "test.2da")
        reporter.finish()

    assert any("Writing test.2da" in record.message for record in caplog.records)
