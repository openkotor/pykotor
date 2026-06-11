"""Unit tests for extract/write path safety (path_safety.py).

Guards against path traversal and writes outside allowed bases for CLI get and MCP extract.
"""

from __future__ import annotations

import os

from pathlib import Path

import pytest

from pykotor.tools.path_safety import (
    MAX_PATH_LENGTH,
    get_extract_base,
    resolve_and_validate_under_base,
    validate_extract_output_path,
)


def test_resolve_accepts_path_under_base(tmp_path: Path) -> None:
    base = tmp_path / "extract"
    base.mkdir()
    target = base / "nested" / "out.txt"

    resolved = resolve_and_validate_under_base(target, base)

    assert resolved == target.resolve()
    assert resolved.relative_to(base.resolve())


def test_resolve_accepts_nonexistent_output_under_base(tmp_path: Path) -> None:
    base = tmp_path / "extract"
    base.mkdir()
    target = base / "new" / "resource.tlk"

    resolved = resolve_and_validate_under_base(target, base, allow_nonexistent=True)

    assert resolved == target.resolve()


def test_resolve_rejects_path_outside_base(tmp_path: Path) -> None:
    base = tmp_path / "allowed"
    base.mkdir()
    outside = tmp_path.parent / "escape.txt"

    with pytest.raises(ValueError, match="outside allowed base"):
        resolve_and_validate_under_base(outside, base)


def test_resolve_rejects_traversal_via_parent_segments(tmp_path: Path) -> None:
    base = tmp_path / "allowed"
    base.mkdir()
    traversal = base / ".." / ".." / "etc" / "passwd"

    with pytest.raises(ValueError, match="outside allowed base"):
        resolve_and_validate_under_base(traversal, base)


def test_resolve_rejects_overlong_path(tmp_path: Path) -> None:
    base = tmp_path / "allowed"
    base.mkdir()
    long_name = "a" * (MAX_PATH_LENGTH + 1)
    long_path = base / long_name

    with pytest.raises(ValueError, match="Path length exceeds maximum"):
        resolve_and_validate_under_base(long_path, base)


def test_resolve_strict_requires_existing_path(tmp_path: Path) -> None:
    base = tmp_path / "allowed"
    base.mkdir()
    missing = base / "does_not_exist.txt"

    with pytest.raises(FileNotFoundError):
        resolve_and_validate_under_base(missing, base, allow_nonexistent=False)


def test_get_extract_base_uses_env_when_set(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    extract_dir = tmp_path / "custom_extract"
    extract_dir.mkdir()
    monkeypatch.setenv("PYKOTOR_EXTRACT_DIR", str(extract_dir))

    assert get_extract_base() == extract_dir.resolve()


def test_get_extract_base_falls_back_to_cwd(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PYKOTOR_EXTRACT_DIR", raising=False)
    assert get_extract_base() == Path.cwd()


def test_validate_extract_output_path_uses_provided_base(tmp_path: Path) -> None:
    base = tmp_path / "base"
    base.mkdir()
    target = base / "out" / "file.gff"

    resolved = validate_extract_output_path(target, base=base)

    assert resolved == target.resolve()


def test_validate_extract_output_path_rejects_escape(tmp_path: Path) -> None:
    base = tmp_path / "base"
    base.mkdir()

    with pytest.raises(ValueError, match="outside allowed base"):
        validate_extract_output_path(tmp_path.parent / "outside.txt", base=base)
