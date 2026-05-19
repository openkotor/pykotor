"""Regression tests for JSON export progress reporting (CI vs TTY)."""

from __future__ import annotations

from io import StringIO

import pytest

from pykotor.tools.resource_json import _supports_live_progress


class _FakeTtyStream(StringIO):
    """Stream that claims to be a TTY (some CI runners attach a pseudo-TTY to stderr)."""

    def isatty(self) -> bool:
        """Always True: simulates stderr on a pseudo-TTY."""
        return True


class _FakeNonTtyStream(StringIO):
    def isatty(self) -> bool:
        """Always False: simulates captured or redirected output."""
        return False


@pytest.mark.parametrize("ci_value", ("true", "1", "yes", "TRUE", " Yes "))
def test_supports_live_progress_false_when_ci_set(
    monkeypatch: pytest.MonkeyPatch,
    ci_value: str,
) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("CI", ci_value)
    assert _supports_live_progress(_FakeTtyStream()) is False


@pytest.mark.parametrize("gha_value", ("true", "1", "yes"))
def test_supports_live_progress_false_when_github_actions_set(
    monkeypatch: pytest.MonkeyPatch,
    gha_value: str,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setenv("GITHUB_ACTIONS", gha_value)
    assert _supports_live_progress(_FakeTtyStream()) is False


def test_supports_live_progress_uses_isatty_when_no_automation_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_FakeTtyStream()) is True
    assert _supports_live_progress(_FakeNonTtyStream()) is False


def test_supports_live_progress_false_without_isatty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    stream = StringIO()
    assert _supports_live_progress(stream) is False
