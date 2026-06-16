"""Regression tests for JSON export progress reporting (CI vs TTY)."""

from __future__ import annotations

import io

import pytest

from pykotor.tools.resource_json import _ExportProgressReporter, _supports_live_progress


class _FakeTTYStream:
    """stderr-like stream that claims to be a TTY (common in some CI containers)."""

    def __init__(self) -> None:
        self.writes: list[str] = []

    def isatty(self) -> bool:
        return True

    def write(self, s: str) -> None:
        self.writes.append(s)

    def flush(self) -> None:
        pass


class _CaptureInfoLogger:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def info(self, message: str, *args) -> None:
        self.messages.append(message % args if args else message)


@pytest.mark.parametrize(
    ("env_name", "env_value"),
    (
        ("CI", "true"),
        ("CI", "1"),
        ("GITHUB_ACTIONS", "yes"),
        ("GITHUB_ACTIONS", "TRUE"),
    ),
)
def test_supports_live_progress_false_when_automation_env_set(
    monkeypatch: pytest.MonkeyPatch, env_name: str, env_value: str
) -> None:
    """Live \\r progress must be off in CI so milestones go through the logger."""
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv(env_name, env_value)
    stream = _FakeTTYStream()
    assert _supports_live_progress(stream) is False


def test_supports_live_progress_true_for_tty_when_not_ci(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    stream = _FakeTTYStream()
    assert _supports_live_progress(stream) is True


def test_supports_live_progress_false_for_non_tty_stream(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(io.StringIO()) is False


def test_export_progress_reporter_logs_via_logger_in_ci_not_stream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When CI is set, progress must not write carriage-return frames to the stream."""
    monkeypatch.setenv("CI", "true")
    stream = _FakeTTYStream()
    logger = _CaptureInfoLogger()
    reporter = _ExportProgressReporter(logger, total_resources=2, stream=stream)
    assert reporter.live_updates is False

    reporter.update(1, "first.res")
    reporter.update(2, "second.res")
    reporter.finish()

    assert not stream.writes
    assert any("50.00% Writing first.res" in m for m in logger.messages)
    assert any("100.00% Writing second.res" in m for m in logger.messages)
