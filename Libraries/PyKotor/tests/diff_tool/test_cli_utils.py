"""Regression tests for diff_tool CLI path normalization and install detection."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

THIS_SCRIPT_PATH = pathlib.Path(__file__).resolve()
PYKOTOR_PATH = THIS_SCRIPT_PATH.parents[2].joinpath("src")
UTILITY_PATH = THIS_SCRIPT_PATH.parents[4].joinpath("Libraries", "Utility", "src")


def add_sys_path(p: pathlib.Path) -> None:
    working_dir = str(p)
    if working_dir not in sys.path:
        sys.path.append(working_dir)


if PYKOTOR_PATH.joinpath("pykotor").exists():
    add_sys_path(PYKOTOR_PATH)
if UTILITY_PATH.joinpath("utility").exists():
    add_sys_path(UTILITY_PATH)

from pykotor.diff_tool.cli_utils import (  # noqa: E402
    is_kotor_install_dir,
    normalize_path_arg,
)


class TestNormalizePathArg(unittest.TestCase):
    def test_none_and_empty(self) -> None:
        self.assertIsNone(normalize_path_arg(None))
        self.assertIsNone(normalize_path_arg(""))
        self.assertIsNone(normalize_path_arg("   "))

    def test_strips_surrounding_quotes(self) -> None:
        self.assertEqual(
            normalize_path_arg('"C:\\Program Files\\KOTOR"'),
            "C:\\Program Files\\KOTOR",
        )
        self.assertEqual(
            normalize_path_arg("'C:/Games/KOTOR'"),
            "C:/Games/KOTOR",
        )

    def test_strips_trailing_slashes_after_quote_removal(self) -> None:
        self.assertEqual(
            normalize_path_arg('"C:\\Program Files\\KOTOR\\"'),
            "C:\\Program Files\\KOTOR",
        )

    def test_mangled_powershell_quote_space_path(self) -> None:
        mangled = 'C:\\Steam\\steamapps\\common\\swkotor" C:\\Other\\path'
        self.assertEqual(
            normalize_path_arg(mangled),
            "C:\\Steam\\steamapps\\common\\swkotor",
        )

    def test_removes_embedded_quotes(self) -> None:
        self.assertEqual(
            normalize_path_arg('C:\\"broken"\\path'),
            "C:\\broken\\path",
        )


class TestIsKotorInstallDir(unittest.TestCase):
    def test_valid_installation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "chitin.key").write_bytes(b"key")
            self.assertTrue(is_kotor_install_dir(root))

    def test_missing_chitin_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.assertFalse(is_kotor_install_dir(root))

    def test_file_path_is_not_install(self) -> None:
        with tempfile.NamedTemporaryFile() as tmp_file:
            self.assertFalse(is_kotor_install_dir(pathlib.Path(tmp_file.name)))

    @unittest.skipIf(
        sys.platform == "win32",
        "Case-mismatch path semantics differ on Windows filesystems.",
    )
    def test_case_mismatched_chitin_key_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "KotorInstall"
            root.mkdir()
            (root / "chitin.key").write_bytes(b"key")

            mismatched = pathlib.Path(tmp) / "kotorinstall"
            self.assertTrue(is_kotor_install_dir(mismatched))


if __name__ == "__main__":
    unittest.main()
