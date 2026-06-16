"""Regression tests for JSON export progress behavior in automation (CI)."""

from __future__ import annotations

import io

import pytest

from pykotor.tools.resource_json import _supports_live_progress


class _FakeTTYStream(io.StringIO):
    """stderr-like stream that claims to be a TTY (common in some CI runners)."""

    def isatty(self) -> bool:
        return True


def test_supports_live_progress_honors_tty_when_not_ci(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTTYStream()) is True


def test_supports_live_progress_ci_env_disables_even_if_stream_is_tty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CI", "true")
    assert _supports_live_progress(_FakeTTYStream()) is False


def test_supports_live_progress_github_actions_env_disables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setenv("GITHUB_ACTIONS", "1")
    assert _supports_live_progress(_FakeTTYStream()) is False


def test_supports_live_progress_non_tty_false_regardless_of_ci(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(io.StringIO()) is False
