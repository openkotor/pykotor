"""Tests for shared resource source resolution (merge/diff CLI and tooling)."""

from __future__ import annotations

import sys
import unittest

from pathlib import Path

THIS_SCRIPT_PATH = Path(__file__).resolve()
PYKOTOR_PATH = THIS_SCRIPT_PATH.parents[2].joinpath("src")


def add_sys_path(p: pathlib.Path) -> None:
    working_dir = str(p)
    if working_dir not in sys.path:
        sys.path.append(working_dir)


if PYKOTOR_PATH.joinpath("pykotor").exists():
    add_sys_path(PYKOTOR_PATH)


from pykotor.common.misc import Game
from pykotor.extract.path_source import detect_source_path_type, parse_game_arg, resolve_resource_source


class TestParseGameArg(unittest.TestCase):
    def test_none_and_blank(self) -> None:
        self.assertIsNone(parse_game_arg(None))
        self.assertIsNone(parse_game_arg(""))
        self.assertIsNone(parse_game_arg("   "))

    def test_k1_aliases(self) -> None:
        self.assertEqual(parse_game_arg("k1"), Game.K1)
        self.assertEqual(parse_game_arg("KOTOR"), Game.K1)
        self.assertEqual(parse_game_arg("kotor1"), Game.K1)

    def test_k2_aliases(self) -> None:
        self.assertEqual(parse_game_arg("k2"), Game.K2)
        self.assertEqual(parse_game_arg("TSL"), Game.K2)
        self.assertEqual(parse_game_arg("kotor2"), Game.K2)

    def test_unknown_returns_none(self) -> None:
        self.assertIsNone(parse_game_arg("not-a-game"))
        self.assertIsNone(parse_game_arg("k3"))


class TestDetectSourcePathType(unittest.TestCase):
    def test_missing_plain_file_is_file(self) -> None:
        path = Path("/nonexistent/path/file.txt")
        self.assertEqual(detect_source_path_type(path), "file")

    def test_missing_capsule_extension_is_capsule(self) -> None:
        path = Path("/nonexistent/module.rim")
        self.assertEqual(detect_source_path_type(path), "capsule")

    def test_game_root_directory(self) -> None:
        with tempfile_game_root() as root:
            self.assertEqual(detect_source_path_type(root), "game_root")

    def test_plain_folder_without_chitin(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            folder = Path(tmp) / "data"
            folder.mkdir()
            self.assertEqual(detect_source_path_type(folder), "folder")

    def test_existing_rim_is_capsule_when_standalone(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            rim_path = Path(tmp) / "standalone.rim"
            rim_path.write_bytes(b"\0" * 16)
            self.assertEqual(detect_source_path_type(rim_path), "capsule")


class TestResolveResourceSource(unittest.TestCase):
    def test_folder_source_has_kind_folder(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            folder = Path(tmp) / "resources"
            folder.mkdir()
            resolved = resolve_resource_source(folder)
            self.assertEqual(resolved.kind, "folder")
            self.assertIsNone(resolved.installation)
            self.assertEqual(resolved.folders, (folder,))

    def test_game_root_sets_installation(self) -> None:
        with tempfile_game_root() as root:
            resolved = resolve_resource_source(root)
            self.assertEqual(resolved.kind, "game_root")
            self.assertIsNotNone(resolved.installation)


def tempfile_game_root():
    """Context manager yielding a minimal game root directory with chitin.key."""
    from tempfile import TemporaryDirectory

    class _Ctx:
        def __enter__(self) -> Path:
            self._tmp = TemporaryDirectory()
            root = Path(self._tmp.name) / "game"
            root.mkdir()
            (root / "chitin.key").write_bytes(b"fake")
            (root / "swkotor.exe").write_bytes(b"fake")
            self.path = root
            return root

        def __exit__(self, *exc: object) -> None:
            self._tmp.cleanup()

    return _Ctx()


if __name__ == "__main__":
    unittest.main()
