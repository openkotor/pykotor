"""Regression tests for JSON export progress reporting under automation."""

from __future__ import annotations

import pytest

from pykotor.tools.resource_json import _supports_live_progress


class _FakeTTYStream:
    """Stream that claims to be a TTY (some CI runners attach a pseudo-TTY to stderr)."""

    def isatty(self) -> bool:
        return True


class _FakeNonTTYStream:
    def isatty(self) -> bool:
        return False


def test_supports_live_progress_honors_ci_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """When CI is set, disable carriage-return live updates so logger-based progress is visible."""
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTTYStream()) is True

    for ci_value in ("true", "True", "1", "yes", " YES "):
        monkeypatch.setenv("CI", ci_value)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        assert _supports_live_progress(_FakeTTYStream()) is False

    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setenv("GITHUB_ACTIONS", "1")
    assert _supports_live_progress(_FakeTTYStream()) is False


def test_supports_live_progress_false_without_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeNonTTYStream()) is False
