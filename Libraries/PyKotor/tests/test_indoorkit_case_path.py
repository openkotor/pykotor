"""Regression tests for CaseAwarePath usage in indoor kit loading (PR #151)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from pykotor.tools.indoorkit import load_kits_unified


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Case-mismatch path semantics differ on Windows filesystems.",
)
def test_load_kits_unified_case_mismatched_kits_directory(tmp_path: Path) -> None:
    kits_dir = tmp_path / "MyKits"
    kits_dir.mkdir()
    v1 = {"name": "Legacy", "id": "legacy", "doors": [], "components": []}
    (kits_dir / "legacy.json").write_text(json.dumps(v1), encoding="utf-8")

    mismatched_path = tmp_path / "mykits"
    kits, tile_kits = load_kits_unified(mismatched_path)

    assert len(kits) == 1
    assert kits[0].id == "legacy"
    assert tile_kits == []
