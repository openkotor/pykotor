"""Unit tests for JSON export progress reporting (CI vs TTY behavior)."""

from __future__ import annotations

import logging
from io import StringIO

import pytest
from loggerplus import RobustLogger

from pykotor.tools.resource_json import _ExportProgressReporter, _supports_live_progress


class _FakeTTYStream(StringIO):
    """stderr-like stream that claims to be a TTY (as in some CI runners)."""

    def isatty(self) -> bool:  # noqa: D102
        return True


def test_supports_live_progress_false_when_ci_set_even_if_stream_is_tty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CI", "true")
    stream = _FakeTTYStream()
    assert _supports_live_progress(stream) is False


def test_supports_live_progress_false_when_github_actions_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "yes")
    stream = _FakeTTYStream()
    assert _supports_live_progress(stream) is False


def test_supports_live_progress_ci_values_are_case_and_whitespace_insensitive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CI", " TRUE ")
    assert _supports_live_progress(_FakeTTYStream()) is False
    monkeypatch.setenv("CI", "1")
    assert _supports_live_progress(_FakeTTYStream()) is False


def test_supports_live_progress_true_for_tty_when_not_in_ci(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTTYStream()) is True


def test_supports_live_progress_false_for_non_tty_stream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(StringIO()) is False


def test_export_progress_reporter_logs_via_logger_when_ci_disables_live_updates(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Regression: CI must not use \\r stderr progress; log aggregators need logger.info lines."""
    monkeypatch.setenv("CI", "true")
    stream = _FakeTTYStream()
    reporter = _ExportProgressReporter(RobustLogger(), 1, stream=stream)
    assert reporter.live_updates is False

    with caplog.at_level(logging.INFO):
        reporter.update(1, "dialog.tlk")
        reporter.finish()

    messages = [record.getMessage() for record in caplog.records]
    assert any("100.00% Writing dialog.tlk" in message for message in messages)
    assert stream.getvalue() == ""


def test_export_progress_reporter_writes_to_stream_for_tty_outside_ci(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    stream = _FakeTTYStream()
    reporter = _ExportProgressReporter(RobustLogger(), 2, stream=stream)
    assert reporter.live_updates is True

    reporter.update(1, "first.res")
    reporter.update(2, "second.res")
    reporter.finish()

    out = stream.getvalue()
    assert "\r" in out
    assert "first.res" in out
    assert "second.res" in out
