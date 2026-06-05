from __future__ import annotations

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
from pykotor.tools.patching import is_kotor_install_dir as patching_is_kotor_install_dir
from pykotor.tslpatcher.diff.engine import is_kotor_install_dir as engine_is_kotor_install_dir


class TestIsKotorInstallDir(unittest.TestCase):
    _IMPLEMENTATIONS = (
        ("cli_utils", cli_is_kotor_install_dir),
        ("patching", patching_is_kotor_install_dir),
        ("diff_engine", engine_is_kotor_install_dir),
    )

    def test_detects_install_with_exact_case(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "KotorInstall"
            root.mkdir()
            (root / "chitin.key").write_bytes(b"key")

            for name, is_install in self._IMPLEMENTATIONS:
                with self.subTest(implementation=name):
                    self.assertTrue(is_install(root))

    def test_rejects_directory_without_chitin_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "NotInstall"
            root.mkdir()

            for name, is_install in self._IMPLEMENTATIONS:
                with self.subTest(implementation=name):
                    self.assertFalse(is_install(root))

    def test_rejects_file_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = pathlib.Path(tmp) / "not_a_dir"
            file_path.write_bytes(b"x")

            for name, is_install in self._IMPLEMENTATIONS:
                with self.subTest(implementation=name):
                    self.assertFalse(is_install(file_path))

    @unittest.skipIf(
        sys.platform == "win32",
        "Case mismatch semantics differ on Windows filesystems.",
    )
    def test_detects_install_with_case_mismatched_chitin_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "KotorInstall"
            root.mkdir()
            (root / "CHITIN.KEY").write_bytes(b"key")

            for name, is_install in self._IMPLEMENTATIONS:
                with self.subTest(implementation=name):
                    self.assertTrue(is_install(root))

    @unittest.skipIf(
        sys.platform == "win32",
        "Case mismatch semantics differ on Windows filesystems.",
    )
    def test_detects_install_with_case_mismatched_root_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "KotorInstall"
            root.mkdir()
            (root / "chitin.key").write_bytes(b"key")

            mismatched_root = root.parent / "kotorinstall"

            for name, is_install in self._IMPLEMENTATIONS:
                with self.subTest(implementation=name):
                    self.assertTrue(is_install(mismatched_root))


if __name__ == "__main__":
    unittest.main()
