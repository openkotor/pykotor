"""Regression tests for diff_tool CLI path helpers (case-aware install detection)."""

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
        ('"C:/Games/KOTOR"', "C:/Games/KOTOR"),
        ("'C:/Games/KOTOR'", "C:/Games/KOTOR"),
        (
            'C:\\Program Files\\Steam\\steamapps\\common\\swkotor" C:\\other',
            "C:\\Program Files\\Steam\\steamapps\\common\\swkotor",
        ),
        ('C:\\Games\\KOTOR\\', "C:\\Games\\KOTOR"),
    ],
)
def test_normalize_path_arg_strips_quotes_and_mangled_powershell_paths(
    raw: str | None,
    expected: str | None,
) -> None:
    assert normalize_path_arg(raw) == expected


def test_is_kotor_install_dir_false_without_chitin_key(tmp_path: Path) -> None:
    install_dir = tmp_path / "kotor"
    install_dir.mkdir()
    assert is_kotor_install_dir(install_dir) is False


def test_is_kotor_install_dir_true_with_chitin_key(tmp_path: Path) -> None:
    install_dir = tmp_path / "kotor"
    install_dir.mkdir()
    (install_dir / "chitin.key").write_bytes(b"key")
    assert is_kotor_install_dir(install_dir) is True


@pytest.mark.skipif(sys.platform == "win32", reason="Case mismatch semantics differ on Windows filesystems.")
def test_is_kotor_install_dir_case_mismatched_install_path(tmp_path: Path) -> None:
    install_dir = tmp_path / "KOTOR"
    install_dir.mkdir()
    (install_dir / "chitin.key").write_bytes(b"key")

    mismatched = tmp_path / "kotor"
    assert is_kotor_install_dir(mismatched) is True


def test_tslpatcher_engine_is_kotor_install_dir_matches_cli_utils(tmp_path: Path) -> None:
    from pykotor.tslpatcher.diff.engine import is_kotor_install_dir as engine_is_install

    install_dir = tmp_path / "install"
    install_dir.mkdir()
    (install_dir / "chitin.key").write_bytes(b"key")

    assert engine_is_install(install_dir) == is_kotor_install_dir(install_dir)
