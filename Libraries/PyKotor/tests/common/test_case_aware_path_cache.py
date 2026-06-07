"""Regression tests for CaseAwarePath directory cache and ambiguous case matching."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pytest

from pykotor.tools import path as path_mod
from pykotor.tools.path import CaseAwarePath, _choose_case_match, clear_cache


class TestChooseCaseMatch(unittest.TestCase):
    def test_prefers_exact_case_when_ambiguous(self) -> None:
        chosen = _choose_case_match("File", ["file", "File"], "/tmp")
        self.assertEqual(chosen, "File")

    def test_picks_best_character_overlap_when_no_exact(self) -> None:
        chosen = _choose_case_match("teSt", ["TEST", "tEst", "teSt"], "/tmp")
        self.assertEqual(chosen, "teSt")

    def test_single_match_returns_only_candidate(self) -> None:
        chosen = _choose_case_match("only", ["only"], "/tmp")
        self.assertEqual(chosen, "only")


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Case-mismatch path semantics differ on Windows filesystems.",
)
class TestCaseAwarePathCache:
    def test_clear_cache_empties_directory_lookup(self, tmp_path: Path) -> None:
        base = tmp_path / "BaseDir"
        base.mkdir()
        (base / "file.txt").write_text("a")

        path_mod._DIR_CACHE[str(tmp_path)] = (0, {"basedir": ["BaseDir"]})
        assert len(path_mod._DIR_CACHE) >= 1

        clear_cache()
        assert len(path_mod._DIR_CACHE) == 0

    def test_resolves_case_mismatched_directory_segment(self, tmp_path: Path) -> None:
        actual = tmp_path / "ActualCase"
        actual.mkdir()
        (actual / "data.txt").write_text("x")

        clear_cache()
        resolved = str(CaseAwarePath(tmp_path / "actualcase" / "data.txt"))
        assert resolved.endswith(str(actual / "data.txt"))

    def test_dir_cache_reused_for_repeated_resolution(self, tmp_path: Path) -> None:
        base = tmp_path / "CacheDir"
        base.mkdir()
        (base / "item.txt").write_text("a")

        clear_cache()
        CaseAwarePath(tmp_path / "cachedir" / "item.txt")
        size_after_first = len(path_mod._DIR_CACHE)

        CaseAwarePath(tmp_path / "cachedir" / "item.txt")
        assert len(path_mod._DIR_CACHE) == size_after_first


if __name__ == "__main__":
    unittest.main()
