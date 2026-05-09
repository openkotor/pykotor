"""Unit tests for ``area_designer_runtime`` (Kotor.NET ``Room`` / ``FixWalls`` / corner visibility)."""

from __future__ import annotations

from pykotor.common.tilekit import (
    CornerHookTemplate,
    KitTileRecord,
    QuaternionWXYZ,
    TileKit,
    WallHookTemplate,
)
from pykotor.tools.area_designer_runtime import (
    ADFloor,
    ADRoom,
    ADTile,
    ADWall,
    build_runtime_from_v01,
    fix_walls,
    inner_corner_visible,
    outer_corner_visible,
    runtime_to_v01,
)
from utility.common.geometry import Vector3


def _hook(px: float = 1.0, py: float = 0.0, pz: float = 0.0) -> WallHookTemplate:
    return WallHookTemplate(
        default_wall_id="wall_a",
        position=Vector3(px, py, pz),
        orientation=QuaternionWXYZ(),
    )


def test_fix_walls_pairs_across_tiles_when_hooks_coincide() -> None:
    kt = KitTileRecord(
        tile_id="cell",
        name="",
        default_floor_id="",
        default_ceiling_id="",
        wall_hooks=[_hook(1.0, 0.0, 0.0)],
    )
    room = ADRoom(position=Vector3(0.0, 0.0, 0.0), orientation_net=[0.0, 0.0, 0.0, 1.0])
    floor = ADFloor(kit_id="k", template_id="")

    t1 = ADTile(
        room=room,
        kit_id="k",
        template_id="cell",
        local_position=Vector3(0.0, 0.0, 0.0),
        orientation_net=[0.0, 0.0, 0.0, 1.0],
        floor=floor,
        kit_record=kt,
    )
    t1.walls.append(ADWall(parent_tile=t1, hook_index=0, kit_id="k", template_id="wall_a"))

    t2 = ADTile(
        room=room,
        kit_id="k",
        template_id="cell",
        local_position=Vector3(0.0, 0.0, 0.0),
        orientation_net=[0.0, 0.0, 0.0, 1.0],
        floor=floor,
        kit_record=kt,
    )
    t2.walls.append(ADWall(parent_tile=t2, hook_index=0, kit_id="k", template_id="wall_a"))

    room.tiles.extend([t1, t2])
    fix_walls(room)

    assert t1.walls[0].linked_tile is t2
    assert t2.walls[0].linked_tile is t1


def test_inner_corner_visible_only_when_adjacent_walls_unlinked() -> None:
    kt = KitTileRecord(
        tile_id="cell",
        name="",
        default_floor_id="",
        default_ceiling_id="",
        wall_hooks=[
            _hook(0.0, 0.0, 0.0),
            _hook(1.0, 0.0, 0.0),
        ],
    )
    room = ADRoom(position=Vector3(0.0, 0.0, 0.0), orientation_net=[0.0, 0.0, 0.0, 1.0])
    floor = ADFloor(kit_id="k", template_id="")
    tile = ADTile(
        room=room,
        kit_id="k",
        template_id="cell",
        local_position=Vector3(0.0, 0.0, 0.0),
        orientation_net=[0.0, 0.0, 0.0, 1.0],
        floor=floor,
        kit_record=kt,
    )
    tile.walls.append(ADWall(parent_tile=tile, hook_index=0, kit_id="k", template_id="w"))
    tile.walls.append(ADWall(parent_tile=tile, hook_index=1, kit_id="k", template_id="w"))

    ic = CornerHookTemplate(
        default_corner_id="c",
        adjacent=[0, 1],
        position=Vector3(0.0, 0.0, 0.0),
        orientation=QuaternionWXYZ(),
    )

    assert inner_corner_visible(ic, tile) is True

    dummy = ADTile(
        room=room,
        kit_id="k",
        template_id="other",
        local_position=Vector3(9.0, 9.0, 9.0),
        orientation_net=[0.0, 0.0, 0.0, 1.0],
        floor=floor,
        kit_record=None,
    )
    tile.walls[0].linked_tile = dummy
    assert inner_corner_visible(ic, tile) is False


def test_outer_corner_requires_circuit_negative() -> None:
    """Smoke-test outer-corner predicate shape (full circuit logic lives in ``outer_corner_visible``)."""
    kt = KitTileRecord(
        tile_id="cell",
        name="",
        default_floor_id="",
        default_ceiling_id="",
        wall_hooks=[
            _hook(0.0, 0.0, 0.0),
            _hook(1.0, 0.0, 0.0),
        ],
    )
    room = ADRoom(position=Vector3(0.0, 0.0, 0.0), orientation_net=[0.0, 0.0, 0.0, 1.0])
    floor = ADFloor(kit_id="k", template_id="")
    center = ADTile(
        room=room,
        kit_id="k",
        template_id="cell",
        local_position=Vector3(0.0, 0.0, 0.0),
        orientation_net=[0.0, 0.0, 0.0, 1.0],
        floor=floor,
        kit_record=kt,
    )
    center.walls.append(ADWall(parent_tile=center, hook_index=0, kit_id="k", template_id="w"))
    center.walls.append(ADWall(parent_tile=center, hook_index=1, kit_id="k", template_id="w"))

    oc = CornerHookTemplate(
        default_corner_id="o",
        adjacent=[0, 1],
        position=Vector3(0.0, 0.0, 0.0),
        orientation=QuaternionWXYZ(),
    )

    assert outer_corner_visible(oc, center) is False


def test_runtime_json_round_trip_minimal_room_without_tiles() -> None:
    area_js = {
        "format": "0.1",
        "rooms": [
            {
                "position": [1.0, 2.0, -3.5],
                "orientation": [0.1, 0.2, 0.3, 0.9330127],
                "tiles": [],
            },
        ],
    }
    r = build_runtime_from_v01(area_js, {})
    back = runtime_to_v01(r)
    assert back["format"] == "0.1"
    assert len(back["rooms"]) == 1
    assert back["rooms"][0]["position"] == [1.0, 2.0, -3.5]
    assert len(back["rooms"][0]["tiles"]) == 0


def test_runtime_round_trip_tile_with_kit() -> None:
    kt = KitTileRecord(
        tile_id="cell01",
        name="",
        default_floor_id="floor1",
        default_ceiling_id="",
        wall_hooks=[_hook(1.0, 0.0, 0.0)],
    )
    kit = TileKit(name="testkit", kit_id="sandral")
    kit.tiles.append(kt)

    area_js = {
        "format": "0.1",
        "rooms": [
            {
                "position": [0.0, 0.0, 0.0],
                "orientation": [0.0, 0.0, 0.0, 1.0],
                "tiles": [
                    {
                        "kitID": "sandral",
                        "templateID": "cell01",
                        "position": [0.5, 0.0, 0.0],
                        "orientation": [0.0, 0.0, 0.0, 1.0],
                        "floor": {"kitID": "sandral", "templateID": "floor1"},
                        "walls": [{"kitID": "sandral", "templateID": "wall_a"}],
                    },
                ],
            },
        ],
    }
    r = build_runtime_from_v01(area_js, {"sandral": kit})
    assert len(r.rooms) == 1
    assert len(r.rooms[0].tiles) == 1
    tile = r.rooms[0].tiles[0]
    assert tile.local_position.x == 0.5
    assert tile.floor.template_id == "floor1"
    assert len(tile.walls) == 1

    back = runtime_to_v01(r)
    t0 = back["rooms"][0]["tiles"][0]
    assert t0["kitID"] == "sandral"
    assert t0["templateID"] == "cell01"
    assert t0["position"] == [0.5, 0.0, 0.0]
    assert t0["floor"] == {"kitID": "sandral", "templateID": "floor1"}
    assert t0["walls"] == [{"kitID": "sandral", "templateID": "wall_a"}]
