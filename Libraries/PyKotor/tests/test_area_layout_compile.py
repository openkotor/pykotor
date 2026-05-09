from __future__ import annotations

from pykotor.common.arealayout import AreaLayout
from pykotor.common.tilekit import (
    QuaternionWXYZ,
    TileCellTemplate,
    TileKit,
    TileTemplate,
    TileTemplateKind,
    WallHookTemplate,
)
from pykotor.tools.area_mdl import area_layout_model_placements
from pykotor.tools.tilemap_compile import area_layout_to_merged_bwm
from utility.common.geometry import Vector3


def _compile_test_kit() -> TileKit:
    kit = TileKit(name="Compile Kit", kit_id="compile")
    kit.floors.append(TileTemplate(TileTemplateKind.FLOOR, "floor_a", "floor_a", name="Floor A", model="floor_a"))
    kit.ceilings.append(
        TileTemplate(TileTemplateKind.CEILING, "ceiling_a", "ceiling_a", name="Ceiling A", model="ceiling_a")
    )
    kit.walls.append(TileTemplate(TileTemplateKind.WALL, "wall_a", "wall_a", name="Wall A", model="wall_a"))
    kit.tiles.append(
        TileCellTemplate(
            template_id="tile_a",
            name="Tile A",
            default_floor_id="floor_a",
            default_ceiling_id="ceiling_a",
            wall_hooks=[
                WallHookTemplate("wall_a", Vector3(5.0, 0.0, 0.0), QuaternionWXYZ()),
                WallHookTemplate("wall_a", Vector3(-5.0, 0.0, 0.0), QuaternionWXYZ()),
                WallHookTemplate("wall_a", Vector3(0.0, 5.0, 0.0), QuaternionWXYZ()),
                WallHookTemplate("wall_a", Vector3(0.0, -5.0, 0.0), QuaternionWXYZ()),
            ],
        )
    )
    return kit


def test_area_layout_to_merged_bwm_generates_floor_quads_for_mdl_only_kit():
    kit = _compile_test_kit()
    layout = AreaLayout()
    room = layout.add_room_from_tile(kit, "tile_a")
    room.extend_tile_from_wall(kit, room.tiles[0], room.tiles[0].walls[0], "tile_a")

    bwm = area_layout_to_merged_bwm(layout, {"compile": kit})

    assert len(bwm.faces) == 4
    xs = [vertex.x for face in bwm.faces for vertex in (face.v1, face.v2, face.v3)]
    assert min(xs) == -5.0
    assert max(xs) == 15.0


def test_area_layout_model_placements_include_visible_walls_only():
    kit = _compile_test_kit()
    layout = AreaLayout()
    room = layout.add_room_from_tile(kit, "tile_a")
    room.extend_tile_from_wall(kit, room.tiles[0], room.tiles[0].walls[0], "tile_a")

    placements = area_layout_model_placements(layout, {"compile": kit})

    assert [placement.kind for placement in placements].count("floor") == 2
    assert [placement.kind for placement in placements].count("wall") == 6
    assert all(placement.template.template_id == "wall_a" for placement in placements if placement.kind == "wall")
