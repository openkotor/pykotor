"""Regression tests for diff_tool.cli_utils path normalization."""

from __future__ import annotations

import pytest

from pykotor.diff_tool.cli_utils import normalize_path_arg


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, None),
        ("", None),
        ("   ", None),
        ("/tmp/kotor", "/tmp/kotor"),
        ('"/tmp/kotor"', "/tmp/kotor"),
        ("'/tmp/kotor'", "/tmp/kotor"),
        (r'C:\Games\KOTOR\ ', r"C:\Games\KOTOR"),
        (r'C:\Games\KOTOR\" C:\Other', r"C:\Games\KOTOR"),
    ],
)
def test_normalize_path_arg_strips_quotes_and_whitespace(
    raw: str | None,
    expected: str | None,
) -> None:
    assert normalize_path_arg(raw) == expected


def test_normalize_path_arg_removes_embedded_quotes() -> None:
    assert normalize_path_arg('C:\\"Games\\"KOTOR') == r"C:\Games\KOTOR"
