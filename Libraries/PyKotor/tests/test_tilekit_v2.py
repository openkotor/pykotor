"""Tests for indoor kit v2 (tile) loading and tile layout compilation."""

from __future__ import annotations

from pathlib import Path

import pytest

from pykotor.common.indoormap import IndoorMap
from pykotor.tools.indoorkit import kits_for_indoor_build, load_kits_unified
from pykotor.tools.tilekit_io import load_tile_kit_v2_json_file
from pykotor.tools.tilemap_compile import (
    TileLayout,
    apply_tile_layout_to_map,
    tile_layout_from_dict,
    tile_layout_to_dict,
)


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "kits_v2"


def test_load_tile_kit_v2_minimal_no_geometry():
    p = FIXTURES / "minimal_tiles.json"
    tk = load_tile_kit_v2_json_file(p, missing_files=None)
    assert tk is not None
    assert tk.kit_id == "minimal_tiles"
    assert len(tk.floors) == 1
    assert tk.floors[0].template_id == "floor_a"
    assert tk.floors[0].mdl == b"" and tk.floors[0].mdx == b""
    assert tk.floors[0].wok is None


def test_load_kits_unified_skips_v2_for_v1_list(tmp_path: Path):
    import json
    import shutil

    v1 = {"name": "Legacy", "id": "legacy", "doors": [], "components": []}
    (tmp_path / "legacy.json").write_text(json.dumps(v1), encoding="utf-8")
    shutil.copy(FIXTURES / "minimal_tiles.json", tmp_path / "minimal_tiles.json")

    kits, tile_kits = load_kits_unified(tmp_path)
    assert len(kits) == 1 and kits[0].id == "legacy"
    assert len(tile_kits) == 1 and tile_kits[0].kit_id == "minimal_tiles"


def test_tile_layout_roundtrip_dict():
    layout = TileLayout(
        kit_id="minimal_tiles",
        cell_size=5.0,
        grid_w=2,
        grid_h=1,
        floor_cells=["floor_a", None],
    )
    d = tile_layout_to_dict(layout)
    back = tile_layout_from_dict(d)
    assert back is not None
    assert back.kit_id == layout.kit_id
    assert back.floor_cells == layout.floor_cells


def test_apply_tile_layout_embedded_room_and_map_version():
    p = FIXTURES / "minimal_tiles.json"
    tk = load_tile_kit_v2_json_file(p)
    assert tk is not None

    layout = TileLayout(
        kit_id=tk.kit_id,
        cell_size=4.0,
        grid_w=1,
        grid_h=1,
        floor_cells=["floor_a"],
    )
    indoor = IndoorMap()
    kits = kits_for_indoor_build([], [tk])
    apply_tile_layout_to_map(indoor, tk, layout, kits)

    assert indoor.indoor_map_version >= 2
    assert indoor.tile_layout is not None
    assert any(r.component.id == "__tile_floor__" for r in indoor.rooms)

def test_indoor_map_load_rejects_empty_object():
    """Guardrail: corrupted maps must not silently succeed."""
    m = IndoorMap()
    with pytest.raises(ValueError):
        m.load(b"{}", [])
