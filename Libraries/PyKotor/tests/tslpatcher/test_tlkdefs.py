from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

THIS_SCRIPT_PATH = pathlib.Path(__file__).resolve()
PYKOTOR_PATH = THIS_SCRIPT_PATH.parents[3].joinpath("src")
UTILITY_PATH = THIS_SCRIPT_PATH.parents[5].joinpath("Libraries", "Utility", "src")


def add_sys_path(p: pathlib.Path):
    working_dir = str(p)
    if working_dir not in sys.path:
        sys.path.append(working_dir)


if PYKOTOR_PATH.joinpath("pykotor").exists():
    add_sys_path(PYKOTOR_PATH)
if UTILITY_PATH.joinpath("utility").exists():
    add_sys_path(UTILITY_PATH)


from pykotor.tslpatcher.tlkdefs import detect_patch_type


class TestTLKDefs(unittest.TestCase):
    def test_detect_patch_type_aspyr_indicator(self):
        with tempfile.TemporaryDirectory() as tmp:
            game_dir = pathlib.Path(tmp) / "GameDir"
            game_dir.mkdir()
            (game_dir / "KOTOR.app").mkdir()

            assert detect_patch_type(game_dir) == "aspyr"

    @unittest.skipIf(sys.platform == "win32", "Case-mismatch path semantics differ on Windows filesystems.")
    def test_detect_patch_type_case_mismatched_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            game_dir = pathlib.Path(tmp) / "GameDir"
            game_dir.mkdir()
            (game_dir / "KOTOR.app").mkdir()

            assert detect_patch_type(pathlib.Path(tmp) / "gamedir") == "aspyr"


if __name__ == "__main__":
    unittest.main()
