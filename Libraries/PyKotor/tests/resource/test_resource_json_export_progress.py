"""Regression tests for installation JSON export progress and stream scanning."""

from __future__ import annotations

import logging
from io import StringIO
from pathlib import Path

import pytest
from loggerplus import RobustLogger

from pykotor.common.language import Language
from pykotor.resource.formats.rim import RIM, write_rim
from pykotor.resource.formats.tlk import TLK, write_tlk
from pykotor.resource.type import ResourceType
from pykotor.tools.resource_json import (
    _ExportProgressReporter,
    _supports_live_progress,
    export_installation_to_json_tree,
)


_LOGGER = logging.getLogger(__name__)


class _TTYStringIO(StringIO):
    """StringIO that claims to be a TTY (for live progress path)."""

    def isatty(self) -> bool:
        return True


def test_supports_live_progress_false_when_ci_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CI", "true")
    stream = _TTYStringIO()
    assert _supports_live_progress(stream) is False


def test_supports_live_progress_false_when_github_actions_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    stream = _TTYStringIO()
    assert _supports_live_progress(stream) is False


def test_supports_live_progress_honors_stream_isatty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert _supports_live_progress(StringIO()) is False
    assert _supports_live_progress(_TTYStringIO()) is True


def test_export_progress_reporter_skips_when_total_zero() -> None:
    log = logging.getLogger(f"{__name__}.zero_total")
    rep = _ExportProgressReporter(logger=log, total_resources=0, stream=StringIO())
    assert rep.enabled is False
    rep.update(1, "should_not_crash")
    rep.finish()


def test_export_progress_reporter_logs_buckets_when_not_live(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Automation/CI must emit percentage lines through the logger (not only ``\\r`` stderr)."""
    monkeypatch.setenv("CI", "true")
    with caplog.at_level(logging.INFO, logger=_LOGGER.name):
        rep = _ExportProgressReporter(logger=_LOGGER, total_resources=4, stream=StringIO())
        assert rep.live_updates is False
        rep.update(1, "first")
        rep.update(2, "second")
        rep.update(3, "third")
        rep.update(4, "fourth")
        rep.finish()
    messages = [r.getMessage() for r in caplog.records]
    assert any("25.00%" in m and "Writing first" in m for m in messages)
    assert any("50.00%" in m and "Writing second" in m for m in messages)
    assert any("75.00%" in m and "Writing third" in m for m in messages)
    assert any("100.00%" in m and "Writing fourth" in m for m in messages)


def test_export_progress_reporter_tty_writes_carriage_returns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    stream = _TTYStringIO()
    log = logging.getLogger(f"{__name__}.tty_parent")
    rep = _ExportProgressReporter(logger=log, total_resources=2, stream=stream)
    assert rep.live_updates is True
    rep.update(1, "alpha")
    rep.update(2, "beta")
    rep.finish()
    assert stream.getvalue().count("\r") >= 1


def test_export_installation_to_json_includes_streamsounds_and_streamwaves(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """``_iter_stream_resources`` must walk music, sounds, and waves/voice roots."""
    install_path = tmp_path / "K1"
    install_path.mkdir()
    (install_path / "Override").mkdir()
    (install_path / "Modules").mkdir()
    (install_path / "StreamMusic").mkdir()
    (install_path / "StreamSounds").mkdir()
    (install_path / "StreamWaves").mkdir()
    (install_path / "chitin.key").write_bytes(b"")
    (install_path / "swkotor.exe").write_bytes(b"")

    tlk = TLK(Language.ENGLISH)
    tlk.add("x", "y")
    write_tlk(tlk, install_path / "dialog.tlk", ResourceType.TLK)
    (install_path / "Override" / "hello.nss").write_text("void main() {}\n", encoding="utf-8")
    rim = RIM()
    rim.set_data("notes", ResourceType.TXT, b"module notes")
    write_rim(rim, install_path / "Modules" / "testmod_s.rim")

    (install_path / "StreamMusic" / "intro.wav").write_bytes(b"RIFFmusic")
    (install_path / "StreamSounds" / "door.wav").write_bytes(b"RIFFdoor")
    (install_path / "StreamWaves" / "pc.wav").write_bytes(b"RIFFpc")

    output_path = tmp_path / "out"
    caplog.clear()
    assert export_installation_to_json_tree(install_path, output_path, RobustLogger()) == 0
    assert any(
        record.getMessage() == "Discovered 6 resources to export" for record in caplog.records
    )

    rel_json = {p.relative_to(output_path).as_posix() for p in output_path.rglob("*.json")}
    assert "StreamMusic/intro.wav.json" in rel_json
    assert "StreamSounds/door.wav.json" in rel_json
    assert "StreamWaves/pc.wav.json" in rel_json
