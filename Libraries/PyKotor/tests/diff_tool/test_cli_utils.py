"""Regression tests for diff_tool CLI path normalization and install detection."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from pykotor.diff_tool.cli_utils import is_kotor_install_dir, normalize_path_arg


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, None),
        ("", None),
        ("   ", None),
        ('"C:\\Games\\KOTOR"', r"C:\Games\KOTOR"),
        ("'C:/Games/KOTOR'", "C:/Games/KOTOR"),
        (r'C:\Program Files\Steam" C:\other', r"C:\Program Files\Steam"),
        (r'C:\Program Files\folder\\', r"C:\Program Files\folder"),
        ("C:/folder/", "C:/folder"),
    ],
)
def test_normalize_path_arg(raw: str | None, expected: str | None) -> None:
    assert normalize_path_arg(raw) == expected


def test_is_kotor_install_dir_false_when_not_directory(tmp_path: Path) -> None:
    key_file = tmp_path / "chitin.key"
    key_file.write_bytes(b"")
    assert is_kotor_install_dir(key_file) is False


def test_is_kotor_install_dir_false_without_chitin(tmp_path: Path) -> None:
    assert is_kotor_install_dir(tmp_path) is False


def test_is_kotor_install_dir_true_with_chitin_key(tmp_path: Path) -> None:
    (tmp_path / "chitin.key").write_bytes(b"")
    assert is_kotor_install_dir(tmp_path) is True


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Case-mismatch path semantics differ on Windows filesystems.",
)
def test_is_kotor_install_dir_case_mismatched_chitin_key(tmp_path: Path) -> None:
    install_dir = tmp_path / "GameRoot"
    install_dir.mkdir()
    (install_dir / "chitin.key").write_bytes(b"")

    mismatched = tmp_path / "gameroot"
    assert is_kotor_install_dir(mismatched) is True
