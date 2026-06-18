"""Unit tests for pykotor.diff_tool.cli_utils path normalization helpers."""

from __future__ import annotations

import pathlib
import sys
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

from pykotor.diff_tool.cli_utils import normalize_path_arg


class TestNormalizePathArg(unittest.TestCase):
    def test_none_and_empty_return_none(self) -> None:
        self.assertIsNone(normalize_path_arg(None))
        self.assertIsNone(normalize_path_arg(""))
        self.assertIsNone(normalize_path_arg("   "))

    def test_strips_surrounding_quotes(self) -> None:
        self.assertEqual(normalize_path_arg('"C:\\Games\\KOTOR"'), "C:\\Games\\KOTOR")
        self.assertEqual(normalize_path_arg("'C:/Games/KOTOR'"), "C:/Games/KOTOR")

    def test_strips_trailing_backslash_before_quote_escape(self) -> None:
        self.assertEqual(
            normalize_path_arg(r'"C:\Program Files\Steam\steamapps\common\swkotor\"'),
            r"C:\Program Files\Steam\steamapps\common\swkotor",
        )

    def test_mangled_powershell_quote_space_path(self) -> None:
        mangled = (
            r'C:\Program Files\Steam\steamapps\common\swkotor" '
            r'C:\Program Files\Steam\steamapps\common\swkotor'
        )
        self.assertEqual(
            normalize_path_arg(mangled),
            r"C:\Program Files\Steam\steamapps\common\swkotor",
        )

    def test_removes_embedded_quotes(self) -> None:
        self.assertEqual(
            normalize_path_arg('C:\\"Games"\\KOTOR'),
            r"C:\Games\KOTOR",
        )


if __name__ == "__main__":
    try:
        import pytest
    except ImportError:  # pragma: no cover
        unittest.main()
    else:
        pytest.main(["-v", __file__])
