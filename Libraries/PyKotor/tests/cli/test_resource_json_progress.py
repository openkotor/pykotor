"""Regression tests for JSON export progress (CI must not use raw TTY \\r updates)."""

from __future__ import annotations

import io
from typing import TextIO, cast

import pytest

from pykotor.tools.resource_json import _supports_live_progress


class _FakeTTY(io.StringIO):
    """stderr-like stream that claims to be a TTY (common in some CI runners)."""

    def isatty(self) -> bool:
        return True


def test_supports_live_progress_false_when_ci_env_true(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CI", "true")
    assert _supports_live_progress(_FakeTTY()) is False


def test_supports_live_progress_false_when_ci_env_truthy_variants(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    for value in ("1", "yes", "TRUE", " Yes "):
        monkeypatch.setenv("CI", value)
        assert _supports_live_progress(_FakeTTY()) is False, value


def test_supports_live_progress_false_when_github_actions_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setenv("GITHUB_ACTIONS", "1")
    assert _supports_live_progress(_FakeTTY()) is False


def test_supports_live_progress_true_for_tty_when_ci_env_cleared(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTTY()) is True


def test_supports_live_progress_false_when_stream_not_a_tty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(io.StringIO()) is False


def test_supports_live_progress_false_without_isatty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)

    class _StreamWithoutIsatty:
        pass

    assert _supports_live_progress(cast(TextIO, _StreamWithoutIsatty())) is False
