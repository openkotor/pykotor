from __future__ import annotations

import pytest

from pykotor.common.arealayout import AreaLayout
from pykotor.common.tilekit import (
    CornerHookTemplate,
    QuaternionWXYZ,
    TileCellTemplate,
    TileKit,
    TileTemplate,
    TileTemplateKind,
    WallHookTemplate,
)
from pykotor.tools.area_layout_io import area_layout_from_dict, area_layout_to_dict
from utility.common.geometry import Vector3


def _layout_test_kit() -> TileKit:
    kit = TileKit(name="Layout Kit", kit_id="layout")
    kit.floors.append(TileTemplate(TileTemplateKind.FLOOR, "floor_a", "floor_a", name="Floor A", model="floor_a"))
    kit.ceilings.append(
        TileTemplate(TileTemplateKind.CEILING, "ceiling_a", "ceiling_a", name="Ceiling A", model="ceiling_a")
    )
    kit.walls.append(TileTemplate(TileTemplateKind.WALL, "wall_a", "wall_a", name="Wall A", model="wall_a"))
    kit.inner_corners.append(
        TileTemplate(TileTemplateKind.INNER_CORNER, "inner_a", "inner_a", name="Inner A", model="inner_a")
    )
    kit.outer_corners.append(
        TileTemplate(TileTemplateKind.OUTER_CORNER, "outer_a", "outer_a", name="Outer A", model="outer_a")
    )
    kit.tiles.append(
        TileCellTemplate(
            template_id="tile_a",
            name="Tile A",
            default_floor_id="floor_a",
            default_ceiling_id="ceiling_a",
            wall_hooks=[
                WallHookTemplate("wall_a", Vector3(5.0, 0.0, 0.0), QuaternionWXYZ()),
                WallHookTemplate("wall_a", Vector3(-5.0, 0.0, 0.0), QuaternionWXYZ()),
            ],
            inner_corner_hooks=[
                CornerHookTemplate("inner_a", Vector3(5.0, 5.0, 0.0), QuaternionWXYZ(), adjacent=[0, 1])
            ],
            outer_corner_hooks=[
                CornerHookTemplate("outer_a", Vector3(-5.0, -5.0, 0.0), QuaternionWXYZ(), adjacent=[0, 1])
            ],
        )
    )
    return kit


def test_area_layout_create_room_from_tile_instantiates_children():
    kit = _layout_test_kit()

    layout = AreaLayout()
    room = layout.add_room_from_tile(kit, "tile_a", position=Vector3(10.0, 20.0, 0.0))

    assert len(layout.rooms) == 1
    assert len(room.tiles) == 1
    tile = room.tiles[0]
    assert tile.kit_id == "layout"
    assert tile.template_id == "tile_a"
    assert tile.floor_template_id == "floor_a"
    assert tile.ceiling_template_id == "ceiling_a"
    assert len(tile.walls) == 2
    assert tile.walls[0].template_id == "wall_a"
    assert tile.walls[0].world_position(room).x == pytest.approx(15.0)
    assert len(tile.inner_corners) == 1
    assert len(tile.outer_corners) == 1


def test_area_layout_extend_tile_links_touching_walls():
    kit = _layout_test_kit()
    layout = AreaLayout()
    room = layout.add_room_from_tile(kit, "tile_a")
    first_tile = room.tiles[0]

    second_tile = room.extend_tile_from_wall(kit, first_tile, first_tile.walls[0], "tile_a")

    assert second_tile.local_position.x == pytest.approx(10.0)
    assert len(room.tiles) == 2
    assert first_tile.walls[0].linked_tile is second_tile
    assert second_tile.walls[1].linked_tile is first_tile
    assert first_tile.walls[0].visible is False
    assert second_tile.walls[1].visible is False
    assert first_tile.walls[1].visible is True


def test_area_layout_missing_template_reports_precise_error():
    kit = _layout_test_kit()
    kit.tiles[0].default_floor_id = "missing_floor"

    layout = AreaLayout()
    with pytest.raises(ValueError, match="Missing floor template missing_floor"):
        layout.add_room_from_tile(kit, "tile_a")


def test_area_layout_roundtrip_dict_preserves_tiles_and_wall_overrides():
    kit = _layout_test_kit()
    layout = AreaLayout()
    room = layout.add_room_from_tile(kit, "tile_a")
    room.tiles[0].walls[0].switch_template(kit, "wall_a")
    room.extend_tile_from_wall(kit, room.tiles[0], room.tiles[0].walls[0], "tile_a")

    data = area_layout_to_dict(layout)
    restored = area_layout_from_dict(data, {"layout": kit})

    assert data["format"] == "0.1"
    assert len(restored.rooms) == 1
    assert len(restored.rooms[0].tiles) == 2
    assert restored.rooms[0].tiles[1].local_position.x == pytest.approx(10.0)
    assert restored.rooms[0].tiles[0].walls[0].linked_tile is restored.rooms[0].tiles[1]
