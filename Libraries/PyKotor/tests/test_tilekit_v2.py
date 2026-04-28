"""Tests for v2 tile kits, merge BWM, and tile layout compile."""

from __future__ import annotations

from pathlib import Path

from pykotor.common.indoorkit import Kit
from pykotor.common.indoormap import EmbeddedKit, IndoorMap
from pykotor.resource.formats.bwm.bwm_data import BWM
from pykotor.tools.indoorkit import load_kits_unified, load_tile_kit_v2
from pykotor.tools.tile_bwm import merge_translated_bwms
from pykotor.tools.tilemap_compile import (
    TileLayout,
    apply_tile_layout_to_map,
    tile_layout_to_merged_bwm,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "kits_v2"


def test_load_minimal_v2_tile_kit() -> None:
    json_path = FIXTURES / "minimal_tiles.json"
    tk, missing = load_tile_kit_v2(json_path, record_missing=True)
    assert isinstance(tk, object)
    assert tk.kit_id == "minimal_tiles"
    assert len(tk.floors) == 1
    assert tk.floors[0].template_id == "floor_plain"
    assert not missing  # no door assets required


def test_load_kits_unified_picks_v2() -> None:
    kits, tile_kits = load_kits_unified(FIXTURES)
    assert isinstance(kits, list)
    assert len(tile_kits) >= 1
    assert any(tk.kit_id == "minimal_tiles" for tk in tile_kits)


def test_tile_layout_merged_bwm_2x2() -> None:
    tk, _ = load_tile_kit_v2(FIXTURES / "minimal_tiles.json", record_missing=False)
    lo = TileLayout(
        format_version=1,
        kit_id=tk.kit_id,
        cell_size=2.0,
        grid_w=2,
        grid_h=2,
        floor_cells=["floor_plain", "floor_plain", "floor_plain", "floor_plain"],
    )
    bwm = tile_layout_to_merged_bwm(lo, tk, z=0.0)
    assert len(bwm.faces) == 8
    assert isinstance(bwm, BWM)


def test_apply_tile_layout_creates_embedded_room() -> None:
    tk, _ = load_tile_kit_v2(FIXTURES / "minimal_tiles.json", record_missing=False)
    im = IndoorMap()
    lo = TileLayout(
        kit_id=tk.kit_id,
        cell_size=4.0,
        grid_w=1,
        grid_h=1,
        floor_cells=["floor_plain"],
    )
    kits_merged: list[Kit] = []
    apply_tile_layout_to_map(im, lo, tk, kits_merged)
    assert len(im.rooms) == 1
    assert im.tile_layout is not None
    assert im.tile_layout.get("kit_id") == "minimal_tiles"
    assert isinstance(im.rooms[0].component.kit, EmbeddedKit)


def test_merge_translated_empty() -> None:
    b = merge_translated_bwms([])
    assert b.faces == []
