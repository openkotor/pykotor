"""Compile v2 tile layouts into embedded rooms + merged walkmesh for IndoorMap.build."""

from __future__ import annotations

import logging
from copy import deepcopy
from dataclasses import dataclass

from pykotor.common.arealayout import AreaLayout, AreaRoom, AreaTile
from pykotor.common.indoorkit import KitComponent
from pykotor.common.indoormap import EmbeddedKit, IndoorMap, IndoorMapRoom, _ensure_embedded_kit
from pykotor.common.tilekit import TileKit
from pykotor.resource.formats.bwm.bwm_data import BWM
from pykotor.tools.tile_bwm import generate_flat_floor_quad, merge_translated_bwms, rotate_bwm_at_origin

from utility.common.geometry import Vector3


@dataclass
class TileLayout:
    kit_id: str
    cell_size: float
    grid_w: int
    grid_h: int
    floor_cells: list[str | None]

    def cell_index(self, x: int, y: int) -> int:
        return y * self.grid_w + x


def tile_layout_from_dict(data: dict) -> TileLayout | None:
    if not data:
        return None
    try:
        kit_id = str(data["kit_id"])
        cell_size = float(data["cell_size"])
        grid_w = int(data["grid_w"])
        grid_h = int(data["grid_h"])
        cells = data.get("floor_cells") or []
    except Exception:
        return None
    floor_cells: list[str | None] = []
    for c in cells:
        floor_cells.append(None if c is None else str(c))
    while len(floor_cells) < grid_w * grid_h:
        floor_cells.append(None)
    floor_cells = floor_cells[: grid_w * grid_h]
    return TileLayout(kit_id=kit_id, cell_size=cell_size, grid_w=grid_w, grid_h=grid_h, floor_cells=floor_cells)


def tile_layout_to_dict(layout: TileLayout) -> dict:
    return {
        "format_version": 1,
        "kit_id": layout.kit_id,
        "cell_size": layout.cell_size,
        "grid_w": layout.grid_w,
        "grid_h": layout.grid_h,
        "floor_cells": layout.floor_cells,
    }


def _world_xy_from_cell(layout: TileLayout, cx: int, cy: int) -> tuple[float, float]:
    ox = -(layout.grid_w * layout.cell_size) * 0.5
    oy = -(layout.grid_h * layout.cell_size) * 0.5
    return ox + cx * layout.cell_size, oy + cy * layout.cell_size


def tile_layout_to_merged_bwm(tile_kit: TileKit, layout: TileLayout):
    pieces: list[tuple] = []
    for cy in range(layout.grid_h):
        for cx in range(layout.grid_w):
            tid = layout.floor_cells[layout.cell_index(cx, cy)]
            if not tid:
                continue
            tpl = tile_kit.template_by_id(tid)
            if tpl is None:
                continue
            wx, wy = _world_xy_from_cell(layout, cx, cy)
            tx = wx + tpl.offset.x
            ty = wy + tpl.offset.y
            tz = tpl.offset.z
            if tpl.wok is not None and tpl.wok.faces:
                bwm_piece = rotate_bwm_at_origin(tpl.wok, tpl.rotation)
                pieces.append((bwm_piece, tx, ty, tz))
            else:
                flat = generate_flat_floor_quad(
                    min_x=wx,
                    min_y=wy,
                    size_x=layout.cell_size,
                    size_y=layout.cell_size,
                    z=tz,
                )
                pieces.append((flat, 0.0, 0.0, 0.0))
    if not pieces:
        return generate_flat_floor_quad(min_x=0.0, min_y=0.0, size_x=1.0, size_y=1.0, z=0.0)
    return merge_translated_bwms(pieces)


def _transform_bwm(
    bwm: BWM,
    *,
    room: AreaRoom,
    tile: AreaTile,
) -> BWM:
    out = deepcopy(bwm)
    for face in out.faces:
        for attr in ("v1", "v2", "v3"):
            vertex = getattr(face, attr)
            tile_space = tile.local_orientation.rotate_vector(vertex)
            tile_space = Vector3(
                tile_space.x + tile.local_position.x,
                tile_space.y + tile.local_position.y,
                tile_space.z + tile.local_position.z,
            )
            world = room.orientation.rotate_vector(tile_space)
            setattr(
                face,
                attr,
                Vector3(world.x + room.position.x, world.y + room.position.y, world.z + room.position.z),
            )
    return out


def _tile_floor_bounds(tile: AreaTile, *, default_tile_size: float = 10.0) -> tuple[float, float, float, float]:
    points = [wall.local_position for wall in tile.walls]
    points.extend(corner.local_position for corner in tile.inner_corners)
    points.extend(corner.local_position for corner in tile.outer_corners)
    if not points:
        half = default_tile_size * 0.5
        return -half, -half, default_tile_size, default_tile_size

    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)
    if abs(max_x - min_x) < 1e-6:
        min_x = -default_tile_size * 0.5
        max_x = default_tile_size * 0.5
    if abs(max_y - min_y) < 1e-6:
        min_y = -default_tile_size * 0.5
        max_y = default_tile_size * 0.5
    return min_x, min_y, max_x - min_x, max_y - min_y


def area_layout_to_merged_bwm(layout: AreaLayout, tile_kits: dict[str, TileKit]) -> BWM:
    """Generate/merge a playable BWM from Kotor.NET-style layout floor geometry."""

    pieces: list[tuple[BWM, float, float, float]] = []
    for room in layout.rooms:
        for tile in room.tiles:
            kit = tile_kits.get(tile.kit_id)
            if kit is None:
                continue
            floor = kit.template_by_id(tile.floor_template_id)
            if floor is not None and floor.wok is not None and floor.wok.faces:
                local = rotate_bwm_at_origin(floor.wok, floor.rotation)
            else:
                min_x, min_y, size_x, size_y = _tile_floor_bounds(tile)
                local = generate_flat_floor_quad(min_x=min_x, min_y=min_y, size_x=size_x, size_y=size_y)
            pieces.append((_transform_bwm(local, room=room, tile=tile), 0.0, 0.0, 0.0))
    if not pieces:
        return generate_flat_floor_quad(min_x=0.0, min_y=0.0, size_x=1.0, size_y=1.0)
    return merge_translated_bwms(pieces)


def _embedded_area_component(
    embedded_kit: EmbeddedKit,
    layout: AreaLayout,
    tile_kits: dict[str, TileKit],
    *,
    room_name: str,
) -> KitComponent:
    from pykotor.tools.area_mdl import area_layout_to_merged_mdl_mdx

    merged_bwm = area_layout_to_merged_bwm(layout, tile_kits)
    mdl, mdx = area_layout_to_merged_mdl_mdx(layout, tile_kits)
    return KitComponent(
        embedded_kit,
        name=room_name,
        component_id="__area_layout__",
        bwm=merged_bwm,
        mdl=mdl,
        mdx=mdx,
    )


def apply_area_layout_to_map(
    indoor: IndoorMap,
    layout: AreaLayout,
    tile_kits: dict[str, TileKit],
    kits: list,
    *,
    replace_existing_area_room: bool = True,
) -> None:
    """Compile a Kotor.NET-style area layout into one embedded room for playable builds."""

    from pykotor.tools.area_layout_io import area_layout_to_dict

    ek = _ensure_embedded_kit(kits)
    comp = _embedded_area_component(ek, layout, tile_kits, room_name="Area layout")

    if replace_existing_area_room:
        indoor.rooms = [room for room in indoor.rooms if room.component.id != "__area_layout__"]

    room = IndoorMapRoom(
        comp,
        Vector3.from_null(),
        0.0,
        flip_x=False,
        flip_y=False,
    )
    indoor.rooms.insert(0, room)
    indoor.area_layout = area_layout_to_dict(layout)
    indoor.indoor_map_version = max(indoor.indoor_map_version, 3)


def reconcile_area_layout_for_build(
    indoor: IndoorMap,
    *,
    tile_kits: list[TileKit],
    kits: list,
    logger: logging.Logger | None = None,
) -> bool:
    """Compile persisted ``area_layout`` metadata into an embedded room if needed."""

    if not getattr(indoor, "area_layout", None):
        return False
    if any(room.component.id == "__area_layout__" for room in indoor.rooms):
        return False

    from pykotor.tools.area_layout_io import area_layout_from_dict

    tile_kit_lookup = {tile_kit.kit_id: tile_kit for tile_kit in tile_kits}
    try:
        layout = area_layout_from_dict(indoor.area_layout, tile_kit_lookup)
    except ValueError as exc:
        if logger is not None:
            logger.warning("area_layout present but invalid; skipping reconcile: %s", exc)
        return False

    apply_area_layout_to_map(indoor, layout, tile_kit_lookup, kits)
    if logger is not None:
        logger.info("Reconciled area_layout into embedded __area_layout__ room.")
    return True


def _embedded_floor_component(
    embedded_kit: EmbeddedKit,
    tile_kit: TileKit,
    merged_bwm,
    layout: TileLayout,
    *,
    room_name: str,
) -> KitComponent:
    from pykotor.tools.tile_mdl import tile_layout_to_merged_mdl_mdx

    mdl, mdx = tile_layout_to_merged_mdl_mdx(tile_kit, layout)
    if len(mdl) < 12:
        mdl = next((t.mdl for t in tile_kit.floors if t.mdl), b"")
        mdx = next((t.mdx for t in tile_kit.floors if t.mdx), b"")
    return KitComponent(
        embedded_kit,
        name=room_name,
        component_id="__tile_floor__",
        bwm=merged_bwm,
        mdl=mdl,
        mdx=mdx,
    )


def apply_tile_layout_to_map(
    indoor: IndoorMap,
    tile_kit: TileKit,
    layout: TileLayout,
    kits: list,
    *,
    replace_existing_tile_room: bool = True,
) -> None:
    """Add or replace one embedded room representing the merged tile floor walkmesh.

    Pass the same ``kits`` list used for :meth:`IndoorMap.build` so the embedded kit exists there.
    """
    ek = _ensure_embedded_kit(kits)

    merged = tile_layout_to_merged_bwm(tile_kit, layout)
    comp = _embedded_floor_component(ek, tile_kit, merged, layout, room_name="Tile floor")

    if replace_existing_tile_room:
        indoor.rooms = [r for r in indoor.rooms if r.component.id != "__tile_floor__"]

    room = IndoorMapRoom(
        comp,
        Vector3.from_null(),
        0.0,
        flip_x=False,
        flip_y=False,
    )
    indoor.rooms.insert(0, room)
    indoor.tile_layout = tile_layout_to_dict(layout)
    indoor.indoor_map_version = max(indoor.indoor_map_version, 2)


def reconcile_tile_layout_for_build(
    indoor: IndoorMap,
    *,
    tile_kits: list[TileKit],
    kits: list,
    logger: logging.Logger | None = None,
) -> bool:
    """If ``tile_layout`` is set but no ``__tile_floor__`` room exists, compile the grid once.

    Use after loading a ``.indoor`` file so CLI and Toolset builds match maps that only
    persisted layout metadata. Returns ``True`` when :func:`apply_tile_layout_to_map` ran.
    """
    if not indoor.tile_layout:
        return False
    if any(r.component.id == "__tile_floor__" for r in indoor.rooms):
        return False
    layout = tile_layout_from_dict(indoor.tile_layout)
    if layout is None:
        if logger is not None:
            logger.warning("tile_layout present but invalid; skipping tile floor reconcile.")
        return False
    tk = next((t for t in tile_kits if t.kit_id == layout.kit_id), None)
    if tk is None:
        if logger is not None:
            logger.warning(
                "tile_layout kit_id %r not found among loaded tile kits; skipping reconcile.",
                layout.kit_id,
            )
        return False
    apply_tile_layout_to_map(indoor, tk, layout, kits)
    if logger is not None:
        logger.info("Reconciled tile_layout into embedded __tile_floor__ room for kit %r.", tk.kit_id)
    return True
