"""Regression tests for diff_tool CLI path helpers."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest
from pathlib import Path

THIS_SCRIPT_PATH = pathlib.Path(__file__).resolve()
PYKOTOR_PATH = THIS_SCRIPT_PATH.parents[2].joinpath("src")


def add_sys_path(p: pathlib.Path) -> None:
    working_dir = str(p)
    if working_dir not in sys.path:
        sys.path.append(working_dir)


if PYKOTOR_PATH.joinpath("pykotor").exists():
    add_sys_path(PYKOTOR_PATH)

from pykotor.diff_tool.cli_utils import (  # noqa: E402  # pyright: ignore[reportMissingImports]
    is_kotor_install_dir,
    normalize_path_arg,
)
from pykotor.tools.patching import is_kotor_install_dir as patching_is_kotor_install_dir  # noqa: E402
from pykotor.tslpatcher.diff.engine import (  # noqa: E402
    is_kotor_install_dir as engine_is_kotor_install_dir,
)


class TestNormalizePathArg(unittest.TestCase):
    def test_none_and_blank_inputs(self) -> None:
        self.assertIsNone(normalize_path_arg(None))
        self.assertIsNone(normalize_path_arg(""))
        self.assertIsNone(normalize_path_arg("   "))

    def test_strips_surrounding_quotes(self) -> None:
        self.assertEqual(normalize_path_arg('"C:\\KOTOR"'), "C:\\KOTOR")
        self.assertEqual(normalize_path_arg("'/opt/kotor'"), "/opt/kotor")

    def test_fixes_powershell_quote_escape_mangling(self) -> None:
        mangled = 'C:\\Program Files\\KOTOR" C:\\other\\path'
        self.assertEqual(normalize_path_arg(mangled), "C:\\Program Files\\KOTOR")

    def test_strips_trailing_slashes_and_embedded_quotes(self) -> None:
        self.assertEqual(normalize_path_arg('C:\\path\\'), "C:\\path")
        self.assertEqual(normalize_path_arg('C:\\path"'), "C:\\path")


class TestIsKotorInstallDir(unittest.TestCase):
    def test_detects_install_with_exact_chitin_key_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Kotor"
            root.mkdir()
            (root / "chitin.key").write_bytes(b"")

            self.assertTrue(is_kotor_install_dir(root))
            self.assertTrue(patching_is_kotor_install_dir(root))
            self.assertTrue(engine_is_kotor_install_dir(root))

    def test_rejects_directory_without_chitin_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            self.assertFalse(is_kotor_install_dir(root))
            self.assertFalse(patching_is_kotor_install_dir(root))
            self.assertFalse(engine_is_kotor_install_dir(root))

    @unittest.skipIf(
        sys.platform == "win32",
        "Case-mismatch path semantics differ on Windows filesystems.",
    )
    def test_detects_install_with_case_mismatched_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "GameDir"
            root.mkdir()
            (root / "CHITIN.KEY").write_bytes(b"")

            mismatched = root.parent / "gamedir"
            self.assertTrue(is_kotor_install_dir(mismatched))
            self.assertTrue(patching_is_kotor_install_dir(mismatched))
            self.assertTrue(engine_is_kotor_install_dir(mismatched))


if __name__ == "__main__":
    unittest.main()
