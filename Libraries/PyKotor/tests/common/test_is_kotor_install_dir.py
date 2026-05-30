"""Regression tests for KOTOR install directory detection via CaseAwarePath."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

import pytest

from pykotor.diff_tool import cli_utils
from pykotor.tools import patching
from pykotor.tslpatcher.diff import engine

InstallDirChecker = Callable[[Path], bool | None]

_CHECKERS: tuple[tuple[str, InstallDirChecker], ...] = (
    ("cli_utils", cli_utils.is_kotor_install_dir),
    ("patching", patching.is_kotor_install_dir),
    ("diff_engine", engine.is_kotor_install_dir),
)


@pytest.mark.parametrize("checker", [c for _, c in _CHECKERS], ids=[n for n, _ in _CHECKERS])
def test_is_kotor_install_dir_true_when_chitin_key_present(
    checker: InstallDirChecker,
    tmp_path: Path,
) -> None:
    (tmp_path / "chitin.key").write_bytes(b"")
    assert checker(tmp_path) is True


@pytest.mark.parametrize("checker", [c for _, c in _CHECKERS], ids=[n for n, _ in _CHECKERS])
def test_is_kotor_install_dir_false_without_chitin_key(
    checker: InstallDirChecker,
    tmp_path: Path,
) -> None:
    assert checker(tmp_path) is False


@pytest.mark.parametrize("checker", [c for _, c in _CHECKERS], ids=[n for n, _ in _CHECKERS])
def test_is_kotor_install_dir_false_for_missing_path(
    checker: InstallDirChecker,
    tmp_path: Path,
) -> None:
    assert checker(tmp_path / "does-not-exist") is False


@pytest.mark.parametrize("checker", [c for _, c in _CHECKERS], ids=[n for n, _ in _CHECKERS])
def test_is_kotor_install_dir_false_for_file_path(
    checker: InstallDirChecker,
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "not-a-dir"
    file_path.write_bytes(b"")
    assert checker(file_path) is False


@pytest.mark.parametrize("checker", [c for _, c in _CHECKERS], ids=[n for n, _ in _CHECKERS])
@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Case-mismatch path semantics differ on Windows filesystems.",
)
def test_is_kotor_install_dir_case_mismatched_install_path(
    checker: InstallDirChecker,
    tmp_path: Path,
) -> None:
    install_dir = tmp_path / "KotorInstall"
    install_dir.mkdir()
    (install_dir / "chitin.key").write_bytes(b"")

    assert checker(tmp_path / "kotorinstall") is True


@pytest.mark.parametrize("checker", [c for _, c in _CHECKERS], ids=[n for n, _ in _CHECKERS])
@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Case-mismatch path semantics differ on Windows filesystems.",
)
def test_is_kotor_install_dir_case_mismatched_chitin_key_name(
    checker: InstallDirChecker,
    tmp_path: Path,
) -> None:
    (tmp_path / "CHITIN.KEY").write_bytes(b"")
    assert checker(tmp_path) is True
