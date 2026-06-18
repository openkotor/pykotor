"""Regression tests for CaseAwarePath consumers added in case-aware application (#151)."""

from __future__ import annotations

import json
import os
import pathlib
import sys
import tempfile
import unittest

THIS_SCRIPT_PATH = pathlib.Path(__file__).resolve()
PYKOTOR_PATH = THIS_SCRIPT_PATH.parents[3].joinpath("src")
UTILITY_PATH = THIS_SCRIPT_PATH.parents[5].joinpath("Libraries", "Utility", "src")


def add_sys_path(p: pathlib.Path) -> None:
    working_dir = str(p)
    if working_dir not in sys.path:
        sys.path.append(working_dir)


if PYKOTOR_PATH.joinpath("pykotor").exists():
    add_sys_path(PYKOTOR_PATH)
if UTILITY_PATH.joinpath("utility").exists():
    add_sys_path(UTILITY_PATH)

from pykotor.diff_tool.cli_utils import is_kotor_install_dir as cli_is_kotor_install_dir
from pykotor.tools.indoorkit import load_kits_unified
from pykotor.tools.path import CaseAwarePath, clear_cache
from pykotor.tslpatcher.diff.engine import is_kotor_install_dir as engine_is_kotor_install_dir
from pykotor.tslpatcher.reader import ConfigReader


class TestIsKotorInstallDirCaseAware(unittest.TestCase):
    def test_exact_case_detects_installation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            install_dir = pathlib.Path(tmp) / "KotorInstall"
            install_dir.mkdir()
            (install_dir / "chitin.key").write_bytes(b"mock key")

            for checker in (cli_is_kotor_install_dir, engine_is_kotor_install_dir):
                with self.subTest(checker=checker.__module__):
                    self.assertTrue(checker(install_dir))

    @unittest.skipIf(
        sys.platform == "win32",
        "Case-mismatch path semantics differ on Windows filesystems.",
    )
    def test_case_mismatched_path_detects_installation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            install_dir = pathlib.Path(tmp) / "KotorInstall"
            install_dir.mkdir()
            (install_dir / "chitin.key").write_bytes(b"mock key")

            mismatched = pathlib.Path(tmp) / "kotorinstall"
            for checker in (cli_is_kotor_install_dir, engine_is_kotor_install_dir):
                with self.subTest(checker=checker.__module__):
                    self.assertTrue(checker(mismatched))

    def test_missing_chitin_key_is_not_installation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            install_dir = pathlib.Path(tmp) / "empty_dir"
            install_dir.mkdir()

            for checker in (cli_is_kotor_install_dir, engine_is_kotor_install_dir):
                with self.subTest(checker=checker.__module__):
                    self.assertFalse(checker(install_dir))


class TestConfigReaderCaseAwarePath(unittest.TestCase):
    @unittest.skipIf(
        sys.platform == "win32",
        "Case-mismatch path semantics differ on Windows filesystems.",
    )
    def test_from_filepath_resolves_case_mismatched_ini(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            mod_dir = pathlib.Path(tmp) / "ModData"
            mod_dir.mkdir()
            ini_path = mod_dir / "Changes.ini"
            ini_path.write_text(
                "[Settings]\nLookupGameFolder=0\nLookupGameNumber=1\n",
                encoding="utf-8",
            )

            reader = ConfigReader.from_filepath(mod_dir / "changes.ini")
            config = reader.load(reader.config)
            self.assertEqual(config.game_number, 1)


class TestIndoorKitCaseAwarePath(unittest.TestCase):
    @unittest.skipIf(
        sys.platform == "win32",
        "Case-mismatch path semantics differ on Windows filesystems.",
    )
    def test_load_kits_unified_resolves_case_mismatched_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kits_dir = pathlib.Path(tmp) / "KitsRoot"
            kits_dir.mkdir()
            kit_json = {"name": "Legacy", "id": "legacy", "doors": [], "components": []}
            (kits_dir / "legacy.json").write_text(json.dumps(kit_json), encoding="utf-8")

            kits, tile_kits = load_kits_unified(pathlib.Path(tmp) / "kitsroot")
            self.assertEqual(len(kits), 1)
            self.assertEqual(kits[0].id, "legacy")
            self.assertEqual(tile_kits, [])


class TestCaseAwarePathCache(unittest.TestCase):
    @unittest.skipIf(
        sys.platform == "win32",
        "Directory cache behavior is exercised on POSIX case-resolution paths.",
    )
    def test_clear_cache_allows_case_resolution_after_directory_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "MixedCase"
            root.mkdir()
            child = root / "nested"
            child.mkdir()

            first = str(CaseAwarePath(root.parent / "mixedcase" / "nested"))
            self.assertTrue(first.endswith(f"MixedCase{os.sep}nested"))

            child.rename(root / "Renamed")
            clear_cache()
            second = str(CaseAwarePath(root.parent / "mixedcase" / "renamed"))
            self.assertTrue(second.endswith(f"MixedCase{os.sep}Renamed"))
            self.assertNotEqual(first, second)


if __name__ == "__main__":
    try:
        import pytest
    except ImportError:  # pragma: no cover
        unittest.main()
    else:
        pytest.main(["-v", __file__])
