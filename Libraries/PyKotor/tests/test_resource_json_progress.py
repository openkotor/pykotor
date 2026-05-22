"""Regression tests for JSON export progress reporting (CI vs TTY)."""

from __future__ import annotations

from io import StringIO

import pytest

from pykotor.tools.resource_json import _supports_live_progress


class _FakeTTYStream:
    """Minimal stream that reports as a TTY (like stderr under ``script``)."""

    def isatty(self) -> bool:
        return True


def test_supports_live_progress_true_when_tty_and_not_ci(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTTYStream()) is True


@pytest.mark.parametrize(
    ("env_name", "env_value"),
    [
        ("CI", "true"),
        ("CI", "1"),
        ("CI", "yes"),
        ("GITHUB_ACTIONS", "true"),
        ("GITHUB_ACTIONS", "1"),
    ],
)
def test_supports_live_progress_false_in_ci_even_if_stream_is_tty(
    monkeypatch: pytest.MonkeyPatch,
    env_name: str,
    env_value: str,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv(env_name, env_value)
    assert _supports_live_progress(_FakeTTYStream()) is False


def test_supports_live_progress_false_when_not_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(StringIO()) is False
