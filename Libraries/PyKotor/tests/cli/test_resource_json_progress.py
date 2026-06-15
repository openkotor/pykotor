"""Regression tests for installation JSON export progress (CI vs TTY)."""

from __future__ import annotations

from io import StringIO
from unittest.mock import MagicMock

import pytest

from pykotor.tools.resource_json import _ExportProgressReporter, _supports_live_progress


class _TtyStringIO(StringIO):
    """stderr that claims to be interactive (some CI runners still report TTY)."""

    def isatty(self) -> bool:  # noqa: D102
        return True


def test_supports_live_progress_true_for_tty_when_not_automation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(_TtyStringIO()) is True


@pytest.mark.parametrize("env_name", ("CI", "GITHUB_ACTIONS"))
@pytest.mark.parametrize("env_value", ("true", "1", "yes"))
def test_supports_live_progress_false_in_automation_despite_tty(
    monkeypatch: pytest.MonkeyPatch,
    env_name: str,
    env_value: str,
) -> None:
    monkeypatch.delenv("CI" if env_name == "GITHUB_ACTIONS" else "GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv(env_name, env_value)
    assert _supports_live_progress(_TtyStringIO()) is False


def test_export_progress_uses_logger_when_ci_even_if_stream_is_tty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Caplog/log aggregators must see percent lines; live \\r updates bypass logging."""
    monkeypatch.setenv("CI", "true")
    stream = _TtyStringIO()
    logger = MagicMock()
    reporter = _ExportProgressReporter(logger, total_resources=2, stream=stream)
    assert reporter.live_updates is False

    reporter.update(1, "a.txt")
    reporter.update(2, "b.txt")
    reporter.finish()

    assert "\r" not in stream.getvalue()
    logged = [
        c.args[1] for c in logger.info.call_args_list if len(c.args) == 2 and c.args[0] == "%s"
    ]
    assert any("50.00% Writing a.txt" in m for m in logged)
    assert any("100.00% Writing b.txt" in m for m in logged)


def test_export_progress_uses_stream_carriage_return_when_tty_and_not_ci(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    stream = _TtyStringIO()
    logger = MagicMock()
    reporter = _ExportProgressReporter(logger, total_resources=1, stream=stream)
    assert reporter.live_updates is True

    reporter.update(1, "only.txt")
    reporter.finish()

    written = stream.getvalue()
    assert written.startswith("\r")
    assert "100.00% Writing only.txt" in written
    logger.info.assert_not_called()
