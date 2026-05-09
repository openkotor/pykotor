"""Serialize and load Kotor.NET-style headless area layouts."""

from __future__ import annotations

from pykotor.common.arealayout import AreaLayout, AreaRoom
from pykotor.common.tilekit import QuaternionWXYZ, TileKit, TileTemplateKind
from utility.common.geometry import Vector3


def _vector3_from_json(data: list[float] | None) -> Vector3:
    if not data or len(data) < 3:
        return Vector3.from_null()
    return Vector3(float(data[0]), float(data[1]), float(data[2]))


def _vector3_to_json(value: Vector3) -> list[float]:
    return [value.x, value.y, value.z]


def _kit_lookup(kits: dict[str, TileKit], kit_id: str) -> TileKit:
    try:
        return kits[kit_id]
    except KeyError as exc:
        raise ValueError(f"Missing kit {kit_id}") from exc


def area_layout_to_dict(layout: AreaLayout) -> dict:
    return {
        "format": "0.1",
        "rooms": [
            {
                "position": _vector3_to_json(room.position),
                "orientation": room.orientation.to_xyzw_json(),
                "tiles": [
                    {
                        "kitID": tile.kit_id,
                        "templateID": tile.template_id,
                        "position": _vector3_to_json(tile.local_position),
                        "orientation": tile.local_orientation.to_xyzw_json(),
                        "floor": {
                            "kitID": tile.kit_id,
                            "templateID": tile.floor_template_id,
                        },
                        "ceiling": {
                            "kitID": tile.kit_id,
                            "templateID": tile.ceiling_template_id,
                        },
                        "walls": [
                            {
                                "kitID": tile.kit_id,
                                "templateID": wall.template_id,
                            }
                            for wall in tile.walls
                        ],
                    }
                    for tile in room.tiles
                ],
                "objects": [
                    {
                        "kitID": area_object.kit_id,
                        "templateID": area_object.template_id,
                        "position": _vector3_to_json(area_object.local_position),
                        "orientation": area_object.local_orientation.to_xyzw_json(),
                    }
                    for area_object in room.objects
                ],
            }
            for room in layout.rooms
        ],
    }


def area_layout_from_dict(data: dict, kits: dict[str, TileKit]) -> AreaLayout:
    layout = AreaLayout()
    for room_data in data.get("rooms", []) or []:
        room = AreaRoom(
            position=_vector3_from_json(room_data.get("position")),
            orientation=QuaternionWXYZ.from_xyzw_json(room_data.get("orientation")),
        )
        layout.rooms.append(room)
        for tile_data in room_data.get("tiles", []) or []:
            kit = _kit_lookup(kits, str(tile_data.get("kitID") or ""))
            tile = room.add_tile(
                kit,
                str(tile_data.get("templateID") or ""),
                position=_vector3_from_json(tile_data.get("position")),
                orientation=QuaternionWXYZ.from_xyzw_json(tile_data.get("orientation")),
            )
            floor_data = tile_data.get("floor") or {}
            floor_id = str(floor_data.get("templateID") or tile.floor_template_id)
            if floor_id:
                floor_template = kit.template_by_id(floor_id)
                if floor_template is None or floor_template.kind != TileTemplateKind.FLOOR:
                    raise ValueError(f"Missing floor template {floor_id}")
                tile.floor_template_id = floor_id

            ceiling_data = tile_data.get("ceiling") or {}
            ceiling_id = str(ceiling_data.get("templateID") or tile.ceiling_template_id)
            if ceiling_id:
                ceiling_template = kit.template_by_id(ceiling_id)
                if ceiling_template is None or ceiling_template.kind != TileTemplateKind.CEILING:
                    raise ValueError(f"Missing ceiling template {ceiling_id}")
                tile.ceiling_template_id = ceiling_id

            for wall, wall_data in zip(tile.walls, tile_data.get("walls", []) or []):
                wall_kit = _kit_lookup(kits, str(wall_data.get("kitID") or tile.kit_id))
                wall.switch_template(wall_kit, str(wall_data.get("templateID") or wall.template_id))
        for object_data in room_data.get("objects", []) or []:
            object_kit = _kit_lookup(kits, str(object_data.get("kitID") or ""))
            room.add_object(
                object_kit,
                str(object_data.get("templateID") or ""),
                position=_vector3_from_json(object_data.get("position")),
                orientation=QuaternionWXYZ.from_xyzw_json(object_data.get("orientation")),
            )
        room.fix_walls()
    return layout
