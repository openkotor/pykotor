"""Regression tests for `indoor-kit-migrate-v1-to-v2` CLI (file I/O and exit codes)."""

from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

from pykotor.cli.commands.indoor_kit_migrate import cmd_indoor_kit_migrate_v1_to_v2


class _StubLogger:
    """Command handlers expect RobustLogger; subclassing it forwards unknown attrs — avoid that."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def info(self, message: str, *args: object) -> None:
        pass

    def error(self, message: str, *args: object) -> None:
        self.errors.append(message % args if args else message)

    def warning(self, message: str, *args: object) -> None:
        pass

    def exception(self, message: str, *args: object) -> None:
        self.errors.append(message % args if args else message)


def _v1_doc() -> dict[str, object]:
    return {
        "name": "Legacy",
        "id": "legacy",
        "doors": [],
        "components": [{"name": "Room", "id": "rm01"}],
    }


def test_cmd_indoor_kit_migrate_writes_v2_json(tmp_path: Path) -> None:
    inp = tmp_path / "kit_v1.json"
    out = tmp_path / "out" / "kit_v2.json"
    inp.write_text(json.dumps(_v1_doc()), encoding="utf-8")

    logger = _StubLogger()
    args = Namespace(input=str(inp), output=str(out))
    assert cmd_indoor_kit_migrate_v1_to_v2(args, logger) == 0

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload.get("format_version") == 2
    assert payload["templates"]["floors"][0]["id"] == "rm01"
    assert not logger.errors


def test_cmd_indoor_kit_migrate_missing_input_returns_one(tmp_path: Path) -> None:
    missing = tmp_path / "nope.json"
    out = tmp_path / "out.json"
    logger = _StubLogger()
    args = Namespace(input=str(missing), output=str(out))
    assert cmd_indoor_kit_migrate_v1_to_v2(args, logger) == 1
    assert any("not found" in e.lower() for e in logger.errors)
    assert not out.exists()


def test_cmd_indoor_kit_migrate_rejects_v2_input(tmp_path: Path) -> None:
    """v2 documents are rejected by the migrator; CLI must surface error and not write output."""
    inp = tmp_path / "v2.json"
    doc = {"format_version": 2, "name": "x", "id": "y", "doors": [], "components": []}
    inp.write_text(json.dumps(doc), encoding="utf-8")
    out = tmp_path / "out.json"
    logger = _StubLogger()
    args = Namespace(input=str(inp), output=str(out))
    assert cmd_indoor_kit_migrate_v1_to_v2(args, logger) == 1
    assert any("format_version" in e.lower() for e in logger.errors)
    assert not out.exists()


def test_cmd_indoor_kit_migrate_malformed_json_returns_one(tmp_path: Path) -> None:
    """Rejected JSON must return 1; ``ValueError`` is raised before v2 validation for bad syntax."""
    inp = tmp_path / "bad.json"
    inp.write_text("{ not json", encoding="utf-8")
    out = tmp_path / "out.json"
    logger = _StubLogger()
    args = Namespace(input=str(inp), output=str(out))
    assert cmd_indoor_kit_migrate_v1_to_v2(args, logger) == 1
    assert logger.errors
    # json.loads raises JSONDecodeError (subclass of ValueError) — first handler logs raw message
    assert any("expecting" in e.lower() for e in logger.errors)
