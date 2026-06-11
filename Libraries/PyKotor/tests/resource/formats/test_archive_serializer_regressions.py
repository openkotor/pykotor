"""Regression tests for archive JSON serialization and GFF-JSON edge cases."""

from __future__ import annotations

import base64
import json
import tempfile
from pathlib import Path

from pykotor.common.misc import ResRef
from pykotor.resource.formats.erf import write_erf
from pykotor.resource.formats.erf.erf_data import ERF, ERFType
from pykotor.resource.formats.gff import bytes_gff, read_gff
from pykotor.resource.formats.gff.gff_data import GFF, GFFFieldType
from pykotor.resource.formats.gff.io_gff_json import GFFJSONWriter
from pykotor.resource.type import ResourceType
from pykotor.resource.formats.erf import read_erf
from pykotor.tools.archive_serializer import (
    _resource_bytes_to_plaintext,
    archive_to_dict,
    dict_to_archive,
)


def test_archive_to_dict_mod_extension_uses_erf_path() -> None:
    """`.mod` must be treated as ERF-family so archive_to_dict does not mis-route to RIM/BIF."""
    erf = ERF(ERFType.MOD)
    buf = bytearray()
    write_erf(erf, buf)
    with tempfile.TemporaryDirectory() as tmp:
        mod_path = Path(tmp) / "empty.mod"
        mod_path.write_bytes(bytes(buf))
        d = archive_to_dict(mod_path, embed_plaintext=False)
    assert d["format"] == "erf"
    assert d["erf_type"] == ERFType.MOD.value
    assert d["resources"] == []


def test_resource_bytes_to_plaintext_gff_from_raw_bytes() -> None:
    """_resource_bytes_to_plaintext must accept raw GFF bytes (read_gff(data)), not only streams."""
    gff = GFF()
    gff.root.set_uint32("SomeField", 42)
    raw = bytes_gff(gff)
    plain = _resource_bytes_to_plaintext(raw, ResourceType.GFF)
    assert plain is not None
    encoding, payload = plain
    assert encoding == "gff_json"
    assert isinstance(payload, dict)
    assert payload["fields"]["SomeField"]["type"] == GFFFieldType.UInt32.value
    assert payload["fields"]["SomeField"]["value"] == 42


def test_gff_json_writer_binary_field_is_base64_ascii() -> None:
    """Binary GFF fields must serialize to JSON-safe base64 strings."""
    payload = b"\x00\xff\x01"
    gff = GFF()
    gff.root.set_binary("Bin", payload)
    out = bytearray()
    GFFJSONWriter(gff, out).write()
    data = json.loads(bytes(out).decode("utf-8"))
    encoded = data["fields"]["Bin"]["value"]
    assert encoded == base64.b64encode(payload).decode("ascii")
    assert isinstance(encoded, str)


def test_read_gff_accepts_bytes_for_plaintext_pipeline() -> None:
    """read_gff(bytes) is used by archive embedding; ensure minimal round-trip."""
    gff = GFF()
    gff.root.set_resref("Tag", ResRef("abc"))
    raw = bytes_gff(gff)
    loaded = read_gff(raw)
    _tag, ftype, value = next(iter(loaded.root))
    assert ftype == GFFFieldType.ResRef
    assert str(value) == "abc"


def test_erf_base64_roundtrip_preserves_gff_resource() -> None:
    """archive_to_dict -> dict_to_archive must preserve ERF resources (base64 encoding)."""
    gff = GFF()
    gff.root.set_uint32("Count", 7)
    original_gff = bytes_gff(gff)

    erf = ERF(ERFType.ERF)
    erf.set_data(ResRef("testitem"), ResourceType.UTI, original_gff)
    with tempfile.TemporaryDirectory() as tmp:
        erf_path = Path(tmp) / "test.erf"
        write_erf(erf, erf_path)
        archive_dict = archive_to_dict(erf_path, embed_plaintext=False)

    assert archive_dict["format"] == "erf"
    assert len(archive_dict["resources"]) == 1
    assert archive_dict["resources"][0]["data_encoding"] == "base64"

    rebuilt_bytes, extension = dict_to_archive(archive_dict)
    assert extension == "erf"

    rebuilt_erf = read_erf(rebuilt_bytes)
    resources = {
        (str(res.resref).lower(), res.restype): bytes(res.data)
        for res in rebuilt_erf
    }
    key = (str(ResRef("testitem")).lower(), ResourceType.UTI)
    assert key in resources
    assert resources[key] == original_gff
