"""Model-placement helpers for Kotor.NET-style area layouts."""

from __future__ import annotations

from dataclasses import dataclass

from pykotor.common.arealayout import AreaLayout
from pykotor.common.tilekit import QuaternionWXYZ, TileKit, TileTemplate
from pykotor.resource.formats.mdl.mdl_auto import read_mdl, write_mdl
from pykotor.resource.formats.mdl.mdl_data import MDLNode
from pykotor.resource.type import ResourceType
from pykotor.tools import model as model_tools
from pykotor.tools.tile_mdl import quaternion_yaw_degrees
from utility.common.geometry import Vector3


@dataclass
class AreaModelPlacement:
    kind: str
    template: TileTemplate
    position: Vector3
    orientation: QuaternionWXYZ


def _template(kit: TileKit, template_id: str) -> TileTemplate | None:
    return kit.template_by_id(template_id)


def _compose(*parts: QuaternionWXYZ) -> QuaternionWXYZ:
    result = QuaternionWXYZ()
    for part in parts:
        result = result * part
    return result


def _prefix_node_tree_names(node: MDLNode, prefix: str) -> None:
    raw = prefix + node.name
    node.name = raw[:32]
    for child in node.children:
        _prefix_node_tree_names(child, prefix)


def area_layout_model_placements(layout: AreaLayout, kits: dict[str, TileKit]) -> list[AreaModelPlacement]:
    placements: list[AreaModelPlacement] = []
    for room in layout.rooms:
        for tile in room.tiles:
            kit = kits.get(tile.kit_id)
            if kit is None:
                continue

            tile_orientation = _compose(room.orientation, tile.local_orientation)
            floor = _template(kit, tile.floor_template_id)
            if floor is not None:
                placements.append(AreaModelPlacement("floor", floor, tile.world_position(room), tile_orientation))

            ceiling = _template(kit, tile.ceiling_template_id)
            if ceiling is not None:
                placements.append(AreaModelPlacement("ceiling", ceiling, tile.world_position(room), tile_orientation))

            for wall in tile.walls:
                if not wall.visible:
                    continue
                wall_template = _template(kit, wall.template_id)
                if wall_template is not None:
                    placements.append(
                        AreaModelPlacement(
                            "wall",
                            wall_template,
                            wall.world_position(room),
                            _compose(room.orientation, tile.local_orientation, wall.local_orientation),
                        )
                    )
                if wall.doorframe is not None and wall.doorframe.visible:
                    door_template = _template(kit, wall.doorframe.template_id)
                    if door_template is not None:
                        placements.append(
                            AreaModelPlacement(
                                "doorframe",
                                door_template,
                                wall.world_position(room),
                                _compose(room.orientation, tile.local_orientation, wall.local_orientation),
                            )
                        )

            for corner in tile.inner_corners:
                if corner.visible:
                    template = _template(kit, corner.template_id)
                    if template is not None:
                        placements.append(
                            AreaModelPlacement(
                                "inner_corner",
                                template,
                                corner.world_position(room),
                                _compose(room.orientation, tile.local_orientation, corner.local_orientation),
                            )
                        )

            for corner in tile.outer_corners:
                if corner.visible:
                    template = _template(kit, corner.template_id)
                    if template is not None:
                        placements.append(
                            AreaModelPlacement(
                                "outer_corner",
                                template,
                                corner.world_position(room),
                                _compose(room.orientation, tile.local_orientation, corner.local_orientation),
                            )
                        )
        for area_object in room.objects:
            kit = kits.get(area_object.kit_id)
            if kit is None:
                continue
            template = _template(kit, area_object.template_id)
            if template is not None:
                placements.append(
                    AreaModelPlacement(
                        "object",
                        template,
                        area_object.world_position(room),
                        _compose(room.orientation, area_object.local_orientation),
                    )
                )
    return placements


def area_layout_to_merged_mdl_mdx(layout: AreaLayout, kits: dict[str, TileKit]) -> tuple[bytes, bytes]:
    """Merge all area layout model placements into one room model when MDLs are available."""

    placements = [
        placement
        for placement in area_layout_model_placements(layout, kits)
        if len(placement.template.mdl) >= 12
    ]
    if not placements:
        return b"", b""

    transformed: list[tuple[bytes | bytearray, bytes, int]] = []
    for index, placement in enumerate(placements):
        template = placement.template
        position = Vector3(
            placement.position.x + template.offset.x,
            placement.position.y + template.offset.y,
            placement.position.z + template.offset.z,
        )
        orientation = placement.orientation * template.rotation
        transformed.append(
            (
                model_tools.transform(template.mdl, position, quaternion_yaw_degrees(orientation)),
                template.mdx,
                index,
            )
        )

    if len(transformed) == 1:
        mdl, mdx, _index = transformed[0]
        return bytes(mdl), bytes(mdx)

    try:
        base_mdl, base_mdx, _base_index = transformed[0]
        merged = read_mdl(base_mdl, source_ext=base_mdx)
        for mdl_b, mdx_b, index in transformed[1:]:
            piece = read_mdl(mdl_b, source_ext=mdx_b)
            prefix = f"a{index}_"
            to_attach = piece.root.children if piece.root.children else [piece.root]
            for child in to_attach:
                _prefix_node_tree_names(child, prefix)
                merged.root.children.append(child)

        mdl_buf = bytearray()
        mdx_buf = bytearray()
        write_mdl(merged, mdl_buf, ResourceType.MDL, target_ext=mdx_buf)
        return bytes(mdl_buf), bytes(mdx_buf)
    except Exception:
        first = transformed[0]
        return bytes(first[0]), bytes(first[1])
