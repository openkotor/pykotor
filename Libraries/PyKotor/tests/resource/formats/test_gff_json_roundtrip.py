"""Regression tests for GFF JSON toolset format (GFFJSONWriter / read_gff JSON path)."""

from __future__ import annotations

import json

from pykotor.resource.formats.gff import GFF, bytes_gff, read_gff
from pykotor.resource.formats.gff.gff_data import GFFFieldType
from pykotor.resource.type import ToolsetFormat


def test_write_gff_json_roundtrips_through_read_gff() -> None:
    """write_gff(..., GFF_JSON) must stay aligned with read_gff auto-detect for `{` documents."""
    gff = GFF()
    gff.root.set_uint32("SomeField", 0xDEADBEEF)

    raw_json = bytes_gff(gff, ToolsetFormat.GFF_JSON)
    assert raw_json.lstrip().startswith(b"{")
    parsed = json.loads(raw_json.decode("utf-8"))
    assert parsed["fields"]["SomeField"]["type"] == GFFFieldType.UInt32.value
    assert parsed["fields"]["SomeField"]["value"] == 0xDEADBEEF

    loaded = read_gff(raw_json)
    assert loaded.root.get_uint32("SomeField") == 0xDEADBEEF
