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


from pykotor.common.misc import Game
from pykotor.tools.heuristics import determine_game


class TestHeuristics(unittest.TestCase):
    def test_determine_game_with_exact_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "GameDir"
            root.mkdir(parents=True)
            (root / "swkotor.exe").write_bytes(b"")

            game = determine_game(root)
            self.assertEqual(game, Game.K1)

    @unittest.skipIf(sys.platform == "win32", "Case mismatch semantics differ on Windows filesystems.")
    def test_determine_game_with_case_mismatched_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "GameDir"
            root.mkdir(parents=True)
            (root / "swkotor.exe").write_bytes(b"")

            game = determine_game(root.parent / "gamedir")
            self.assertEqual(game, Game.K1)


if __name__ == "__main__":
    unittest.main()
