"""Regression: binary MDL read from a non-zero slice (BIF / chitin-style offset).

``MDLBinaryReader`` must open the stream at ``offset + 12`` (geometry base) without
an extra ``set_offset(+12)``, which double-counted ``offset`` and broke BIF-sourced MDLs.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pykotor.resource.formats.mdl import read_mdl


def _smallest_mdl_fixture() -> Path:
    candidates = (
        Path(__file__).resolve().parent.parent.parent / "test_files" / "mdl" / "m12aa_c04_cam.mdl",
        Path("Libraries/PyKotor/tests/test_files/mdl/m12aa_c04_cam.mdl"),
        Path("tests/test_files/mdl/m12aa_c04_cam.mdl"),
    )
    for path in candidates:
        if path.is_file():
            return path
    pytest.skip("MDL fixture m12aa_c04_cam.mdl not found")


def test_read_mdl_nonzero_slice_offset_matches_standalone_file() -> None:
    """Padded buffer + offset/size must parse identically to reading the file directly."""
    mdl_path = _smallest_mdl_fixture()
    raw = mdl_path.read_bytes()
    prefix = b"BIFSLICE" * 64  # arbitrary non-MDL padding before the resource
    composite = prefix + raw

    direct = read_mdl(mdl_path)
    sliced = read_mdl(composite, offset=len(prefix), size=len(raw))

    assert sliced.name == direct.name
    assert len(sliced.all_nodes()) == len(direct.all_nodes())
