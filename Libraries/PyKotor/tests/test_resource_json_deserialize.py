"""Unit tests for embedded resource JSON deserialization (resource_json.py)."""

from __future__ import annotations

import base64

import pytest

from pykotor.resource.formats.gff import bytes_gff, read_gff
from pykotor.resource.formats.gff.gff_data import GFF, GFFFieldType
from pykotor.resource.type import ResourceType
from pykotor.tools.resource_json import (
    deserialize_embedded_resource_payload,
    direct_json_document_to_resource_bytes,
)


def test_deserialize_base64_roundtrip() -> None:
    payload = b"hello archive"
    encoded = base64.b64encode(payload).decode("ascii")

    result = deserialize_embedded_resource_payload("base64", encoded, ResourceType.TXT)

    assert result == payload


def test_deserialize_base64_rejects_non_string_payload() -> None:
    with pytest.raises(ValueError, match="Base64 payload must be a string"):
        deserialize_embedded_resource_payload("base64", 123, ResourceType.TXT)


def test_deserialize_gff_json_roundtrip() -> None:
    import json

    from pykotor.resource.formats.gff.io_gff_json import GFFJSONWriter

    gff = GFF()
    gff.root.set_uint32("Value", 99)
    out = bytearray()
    GFFJSONWriter(gff, out).write()
    payload = json.loads(bytes(out).decode("utf-8"))

    result = deserialize_embedded_resource_payload("gff_json", payload, ResourceType.GFF)
    loaded = read_gff(result)
    _label, ftype, value = next(iter(loaded.root))
    assert ftype == GFFFieldType.UInt32
    assert value == 99


def test_deserialize_unknown_encoding_raises() -> None:
    with pytest.raises(ValueError, match="Unknown embedded JSON encoding"):
        deserialize_embedded_resource_payload("not_a_codec", "data", ResourceType.TXT)


def test_direct_json_document_binary_wrapper() -> None:
    payload = b"\xde\xad\xbe\xef"
    document = {
        "format": "binary",
        "restype": "TXT",
        "encoding": "base64",
        "data_base64": base64.b64encode(payload).decode("ascii"),
    }

    result = direct_json_document_to_resource_bytes(document, ResourceType.TXT)

    assert result == payload


def test_direct_json_document_rejects_unsupported_format() -> None:
    with pytest.raises(ValueError, match="does not use a direct-wrapper format"):
        direct_json_document_to_resource_bytes({"format": "unknown"}, ResourceType.TXT)
