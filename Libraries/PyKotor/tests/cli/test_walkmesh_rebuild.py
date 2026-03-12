"""Tests for walkmesh-rebuild CLI command."""

from __future__ import annotations

import pathlib

import pytest

from pykotor.cli.dispatch import cli_main
from pykotor.resource.formats.bwm import read_bwm

THIS_DIR = pathlib.Path(__file__).resolve().parent
# THIS_DIR = Libraries/PyKotor/tests/cli; parent = tests; parents[3] = repo root
REPO_ROOT = THIS_DIR.parents[3]
MODEL_203TELL_WOK = REPO_ROOT / "models" / "203tell.wok"
ASCII_203TEL = REPO_ROOT / "203tel.wok.ascii"
TESTS_DIR = THIS_DIR.parent
TEST_WOK_FILE = TESTS_DIR / "test_files" / "test.wok"


def _run_cli(argv: list[str]) -> int:
    return cli_main(argv)


def test_walkmesh_rebuild_binary_to_file(tmp_path: pathlib.Path) -> None:
    """walkmesh-rebuild with binary input writes rebuilt WOK to output."""
    if not TEST_WOK_FILE.exists():
        pytest.skip(f"Test file not found: {TEST_WOK_FILE}")
    out = tmp_path / "rebuilt.wok"
    exit_code = _run_cli(["walkmesh-rebuild", str(TEST_WOK_FILE), "-o", str(out)])
    assert exit_code == 0
    assert out.exists()
    bwm = read_bwm(out.read_bytes())
    orig = read_bwm(TEST_WOK_FILE.read_bytes())
    assert len(bwm.faces) == len(orig.faces)
    assert len(list(bwm.vertices())) == len(list(orig.vertices()))


def test_walkmesh_rebuild_overwrite(tmp_path: pathlib.Path) -> None:
    """walkmesh-rebuild without -o overwrites input when input is binary."""
    if not TEST_WOK_FILE.exists():
        pytest.skip(f"Test file not found: {TEST_WOK_FILE}")
    copy = tmp_path / "copy.wok"
    copy.write_bytes(TEST_WOK_FILE.read_bytes())
    exit_code = _run_cli(["walkmesh-rebuild", str(copy)])
    assert exit_code == 0
    bwm = read_bwm(copy.read_bytes())
    orig = read_bwm(TEST_WOK_FILE.read_bytes())
    assert len(bwm.faces) == len(orig.faces)


def test_walkmesh_rebuild_ascii_input_to_wok(tmp_path: pathlib.Path) -> None:
    """walkmesh-rebuild with ASCII input and no -o writes to stem.wok."""
    if not ASCII_203TEL.exists():
        pytest.skip(f"ASCII test file not found: {ASCII_203TEL}")
    out = tmp_path / "from_ascii.wok"
    exit_code = _run_cli(["walkmesh-rebuild", str(ASCII_203TEL), "-o", str(out)])
    assert exit_code == 0
    assert out.exists()
    bwm = read_bwm(out.read_bytes())
    assert len(bwm.faces) > 0


def test_walkmesh_rebuild_with_ascii_flag(tmp_path: pathlib.Path) -> None:
    """walkmesh-rebuild --ascii also writes an .ascii file."""
    if not TEST_WOK_FILE.exists():
        pytest.skip(f"Test file not found: {TEST_WOK_FILE}")
    out = tmp_path / "rebuilt.wok"
    exit_code = _run_cli(["walkmesh-rebuild", str(TEST_WOK_FILE), "-o", str(out), "--ascii"])
    assert exit_code == 0
    assert out.exists()
    ascii_path = out.with_suffix(out.suffix + ".ascii")
    assert ascii_path.exists()
    # ASCII can be loaded by read_bwm (auto-detect)
    bwm_from_ascii = read_bwm(ascii_path.read_bytes())
    assert len(bwm_from_ascii.faces) > 0


def test_walkmesh_rebuild_missing_input_returns_nonzero() -> None:
    """walkmesh-rebuild with missing input file returns non-zero."""
    exit_code = _run_cli(["walkmesh-rebuild", "/nonexistent/path.wok"])
    assert exit_code != 0
