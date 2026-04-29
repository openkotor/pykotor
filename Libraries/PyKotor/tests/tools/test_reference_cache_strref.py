"""Regression tests for StrRef scanning and reference-cache wiring.

``pykotor.tools.reference_cache`` is used across diff and tooling flows. These tests
lock in scan behavior for 2DA / SSF / GFF inputs and the module-level scan cache helper.
"""

from __future__ import annotations

from pathlib import Path

from pykotor.common.language import LocalizedString
from pykotor.common.misc import Game
from pykotor.extract.file import FileResource
from pykotor.extract.twoda import TwoDARegistry
from pykotor.resource.formats.gff import GFF, GFFList, GFFStruct, bytes_gff
from pykotor.resource.formats.ssf.ssf_auto import bytes_ssf
from pykotor.resource.formats.ssf.ssf_data import SSF, SSFSound
from pykotor.resource.formats.twoda import TwoDA, bytes_2da
from pykotor.resource.type import ResourceType
from pykotor.tools import reference_cache as reference_cache_module
from pykotor.tools.reference_cache import (
    GFF_FIELD_TO_2DA_MAPPING,
    StrRefReferenceCache,
    clear_scan_cache,
)


def test_clear_scan_cache_empties_scan_results_store() -> None:
    """clear_scan_cache must drop all entries from the module-level scan cache."""
    reference_cache_module._SCAN_RESULTS_CACHE[("probe", 0, 0, 0.0)] = []
    try:
        clear_scan_cache()
        assert reference_cache_module._SCAN_RESULTS_CACHE == {}
    finally:
        clear_scan_cache()


def test_gff_field_to_2da_mapping_matches_twoda_registry() -> None:
    """GFF_FIELD_TO_2DA_MAPPING must stay aligned with TwoDARegistry (import-time wiring)."""
    TwoDARegistry.init_metadata()
    assert GFF_FIELD_TO_2DA_MAPPING == TwoDARegistry.gff_field_mapping()


def test_strref_cache_scans_2da_numeric_strref_cells() -> None:
    """2DA cells that are all digits in StrRef columns are recorded."""
    # ``classes.2da`` has multiple StrRef columns in metadata; the scanner visits each.
    table = TwoDA(["label", "name", "description"])
    table.add_row("0", {"name": "9001", "description": ""})
    data = bytes_2da(table, ResourceType.TwoDA)
    fr = FileResource(
        resname="classes",
        restype=ResourceType.TwoDA,
        size=len(data),
        offset=0,
        filepath=Path("classes.2da"),
    )
    cache = StrRefReferenceCache(Game.K1)
    cache.scan_resource(fr, data)
    assert cache.has_references(9001)
    refs = cache.get_references(9001)
    assert len(refs) == 1
    ident, locations = refs[0]
    assert ident.resname == "classes"
    assert locations == ["row_0.name"]


def test_strref_cache_ignores_non_numeric_2da_cells() -> None:
    """Non-digit StrRef column values must not populate the cache."""
    table = TwoDA(["label", "name", "description"])
    table.add_row("0", {"name": "not-a-strref", "description": ""})
    data = bytes_2da(table, ResourceType.TwoDA)
    fr = FileResource(
        resname="classes",
        restype=ResourceType.TwoDA,
        size=len(data),
        offset=0,
        filepath=Path("classes.2da"),
    )
    cache = StrRefReferenceCache(Game.K1)
    cache.scan_resource(fr, data)
    assert cache.get_statistics()["total_references"] == 0


def test_strref_cache_scans_ssf_sound_slots() -> None:
    ssf = SSF()  # type: ignore[no-untyped-call]
    ssf.set_data(SSFSound.BATTLE_CRY_1, 555)
    data = bytes_ssf(ssf)
    fr = FileResource(
        resname="creature",
        restype=ResourceType.SSF,
        size=len(data),
        offset=0,
        filepath=Path("creature.ssf"),
    )
    cache = StrRefReferenceCache(Game.K1)
    cache.scan_resource(fr, data)
    assert cache.has_references(555)
    refs = cache.get_references(555)
    assert len(refs) == 1
    _ident, locations = refs[0]
    assert "sound_0" in locations


def test_strref_cache_scans_gff_locstring_fields_including_list_items() -> None:
    gff_roundtrip = GFF()
    root_roundtrip = gff_roundtrip.root
    root_roundtrip.set_locstring("FirstName", LocalizedString(42))
    inner_rt = GFFStruct(1)
    inner_rt.set_locstring("Description", LocalizedString(77))
    lst_rt = GFFList()  # type: ignore[no-untyped-call]
    lst_rt.append(inner_rt)
    root_roundtrip.set_list("ItemList", lst_rt)
    payload = bytes_gff(gff_roundtrip)

    fr = FileResource(
        resname="testutc",
        restype=ResourceType.UTC,
        size=len(payload),
        offset=0,
        filepath=Path("test.utc"),
    )
    cache = StrRefReferenceCache(Game.K1)
    cache.scan_resource(fr, payload)

    assert cache.has_references(42)
    assert cache.has_references(77)
    locs_42 = cache.get_references(42)[0][1]
    locs_77 = cache.get_references(77)[0][1]
    assert "FirstName" in locs_42
    assert "ItemList[0].Description" in locs_77
