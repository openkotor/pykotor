"""Tests for diff_tool CLI path utilities.

Covers normalize_path_arg (PowerShell quoting edge cases) and
is_kotor_install_dir (case-aware install detection).
"""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "Libraries" / "PyKotor" / "src"))
sys.path.insert(0, str(REPO_ROOT / "Libraries" / "Utility" / "src"))

from pykotor.diff_tool.cli_utils import is_kotor_install_dir, normalize_path_arg
from pykotor.tools.patching import is_kotor_install_dir as patching_is_kotor_install_dir
from pykotor.tslpatcher.diff.engine import is_kotor_install_dir as engine_is_kotor_install_dir


class TestNormalizePathArg:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            (None, None),
            ("", None),
            ("   ", None),
            ('"C:\\Games\\KOTOR"', "C:\\Games\\KOTOR"),
            ("'C:/Games/KOTOR'", "C:/Games/KOTOR"),
            ('  "C:\\Program Files\\KOTOR"  ', "C:\\Program Files\\KOTOR"),
            ('C:\\Program Files\\KOTOR\\', "C:\\Program Files\\KOTOR"),
            ('C:/Program Files/KOTOR/', "C:/Program Files/KOTOR"),
            ('C:\\path" C:\\other', "C:\\path"),
            ('C:\\path" more junk', "C:\\path"),
            ('path"with"quotes', "pathwithquotes"),
        ],
    )
    def test_normalize_path_arg(self, raw: str | None, expected: str | None) -> None:
        assert normalize_path_arg(raw) == expected


class TestIsKotorInstallDir:
    def test_valid_install_directory(self, tmp_path: pathlib.Path) -> None:
        (tmp_path / "chitin.key").write_bytes(b"key")
        assert is_kotor_install_dir(tmp_path) is True
        assert patching_is_kotor_install_dir(tmp_path) is True
        assert engine_is_kotor_install_dir(tmp_path) is True

    def test_directory_missing_chitin_key(self, tmp_path: pathlib.Path) -> None:
        assert is_kotor_install_dir(tmp_path) is False
        assert patching_is_kotor_install_dir(tmp_path) is False
        assert engine_is_kotor_install_dir(tmp_path) is False

    def test_file_path_is_not_install_dir(self, tmp_path: pathlib.Path) -> None:
        file_path = tmp_path / "chitin.key"
        file_path.write_bytes(b"key")
        assert is_kotor_install_dir(file_path) is False
        assert patching_is_kotor_install_dir(file_path) is False
        assert engine_is_kotor_install_dir(file_path) is False

    @unittest.skipIf(
        sys.platform == "win32",
        "Case-mismatch path semantics differ on Windows filesystems.",
    )
    def test_case_mismatched_chitin_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            install_dir = pathlib.Path(tmp) / "KotorInstall"
            install_dir.mkdir()
            (install_dir / "chitin.key").write_bytes(b"key")

            mismatched = pathlib.Path(tmp) / "kotorinstall"
            assert is_kotor_install_dir(mismatched) is True
            assert patching_is_kotor_install_dir(mismatched) is True
            assert engine_is_kotor_install_dir(mismatched) is True
