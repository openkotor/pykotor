"""Regression tests for JSON export progress reporting in CI and automation."""

from __future__ import annotations

from io import StringIO
from typing import cast

import pytest
from loggerplus import RobustLogger

from pykotor.tools.resource_json import (
    _ExportProgressReporter,
    _supports_live_progress,
)


class _TtyStream(StringIO):
    """A text stream that claims to be a TTY (like stderr under ``script`` or some CI runners)."""

    def isatty(self) -> bool:
        return True


class _RecordingLogger:
    """Minimal logger duck-type; ``RobustLogger`` subclasses are unsafe in tests (singleton metaclass)."""

    __slots__ = ("messages",)

    def __init__(self) -> None:
        self.messages: list[str] = []

    def info(self, message: str, *args: object) -> None:
        self.messages.append(message % args if args else message)


def test_supports_live_progress_false_when_ci_set_even_if_stream_is_tty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CI", "true")
    assert _supports_live_progress(_TtyStream()) is False


def test_supports_live_progress_false_when_github_actions_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setenv("GITHUB_ACTIONS", "1")
    assert _supports_live_progress(_TtyStream()) is False


def test_supports_live_progress_true_for_tty_when_ci_not_truthy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("CI", "false")
    assert _supports_live_progress(_TtyStream()) is True


def test_export_progress_reporter_logs_via_logger_when_ci_disables_live_tty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When CI is set, progress must go through the logger so aggregators see milestones."""
    monkeypatch.setenv("CI", "true")
    stream = _TtyStream()
    assert _supports_live_progress(stream) is False

    recording = _RecordingLogger()
    reporter = _ExportProgressReporter(
        cast(RobustLogger, recording), total_resources=2, stream=stream
    )
    assert not reporter.live_updates

    reporter.update(1, "first.res")
    reporter.update(2, "second.res")
    reporter.finish()

    assert stream.getvalue() == ""
    messages = recording.messages
    assert any("50.00% Writing first.res" in m for m in messages)
    assert any("100.00% Writing second.res" in m for m in messages)
