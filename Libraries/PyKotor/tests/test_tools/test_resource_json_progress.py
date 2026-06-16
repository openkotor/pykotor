"""Regression tests for installation JSON export progress (CI vs TTY behavior)."""

from __future__ import annotations

import io

import pytest

from pykotor.tools.resource_json import (
    _ExportProgressReporter,
    _format_progress_bar,
    _supports_live_progress,
)


class _ListLogger:
    """Minimal logger surface for ``_ExportProgressReporter`` (avoids RobustLogger singleton)."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    def info(self, message: str, *args: object) -> None:
        self.messages.append(message % args if args else message)


class _FakeTTYStream(io.StringIO):
    def isatty(self) -> bool:  # noqa: D401
        return True


def test_format_progress_bar_clamps_percent() -> None:
    assert "#" not in _format_progress_bar(-1.0)
    assert _format_progress_bar(200.0) == _format_progress_bar(100.0)


@pytest.mark.parametrize(
    ("env_name", "env_value"),
    [
        ("CI", "true"),
        ("CI", "1"),
        ("CI", " YES "),
        ("GITHUB_ACTIONS", "true"),
        ("GITHUB_ACTIONS", "1"),
    ],
)
def test_supports_live_progress_false_in_automation_env(
    monkeypatch: pytest.MonkeyPatch, env_name: str, env_value: str
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv(env_name, env_value)
    stream = _FakeTTYStream()
    assert _supports_live_progress(stream) is False


def test_supports_live_progress_false_without_tty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    stream = io.StringIO()
    assert stream.isatty() is False
    assert _supports_live_progress(stream) is False


def test_supports_live_progress_true_for_tty_outside_ci(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTTYStream()) is True


def test_export_progress_reporter_logs_to_logger_when_ci_disables_live_updates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: CI must not use carriage-return stderr spam; aggregators need logger.info."""
    monkeypatch.setenv("CI", "true")
    logger = _ListLogger()
    stream = _FakeTTYStream()
    reporter = _ExportProgressReporter(logger, total_resources=4, stream=stream)
    assert reporter.live_updates is False

    reporter.update(1, "a")
    reporter.update(2, "b")
    reporter.finish()

    messages = logger.messages
    assert any("25.00% Writing a" in m for m in messages)
    assert any("50.00% Writing b" in m for m in messages)
    assert stream.getvalue() == ""
