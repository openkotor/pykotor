"""Regression tests for CaseAwarePath-based KOTOR install directory detection."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

_INSTALL_DETECTORS = (
    ("pykotor.diff_tool.cli_utils", "is_kotor_install_dir"),
    ("pykotor.tools.patching", "is_kotor_install_dir"),
    ("pykotor.tslpatcher.diff.engine", "is_kotor_install_dir"),
)


@pytest.fixture(params=_INSTALL_DETECTORS, ids=[f"{module}.{name}" for module, name in _INSTALL_DETECTORS])
def is_kotor_install_dir(request):
    module_name, attr_name = request.param
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)


def test_detects_install_with_chitin_key(tmp_path: Path, is_kotor_install_dir) -> None:
    install = tmp_path / "KotorInstall"
    install.mkdir()
    (install / "chitin.key").write_bytes(b"")

    assert is_kotor_install_dir(install) is True


def test_rejects_folder_without_chitin_key(tmp_path: Path, is_kotor_install_dir) -> None:
    folder = tmp_path / "not_install"
    folder.mkdir()

    assert not is_kotor_install_dir(folder)


def test_rejects_regular_file(tmp_path: Path, is_kotor_install_dir) -> None:
    file_path = tmp_path / "file.txt"
    file_path.write_text("x", encoding="utf-8")

    assert not is_kotor_install_dir(file_path)


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Case-mismatch path semantics differ on Windows filesystems.",
)
def test_detects_case_mismatched_install_path(tmp_path: Path, is_kotor_install_dir) -> None:
    install = tmp_path / "GameInstall"
    install.mkdir()
    (install / "chitin.key").write_bytes(b"")

    assert is_kotor_install_dir(tmp_path / "gameinstall") is True


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Case-mismatch path semantics differ on Windows filesystems.",
)
def test_detects_case_mismatched_chitin_key(tmp_path: Path, is_kotor_install_dir) -> None:
    install = tmp_path / "install"
    install.mkdir()
    (install / "CHITIN.KEY").write_bytes(b"")

    assert is_kotor_install_dir(install) is True
