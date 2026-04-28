"""Compile v2 tile_layout + TileKit into IndoorMap rooms (EmbeddedKit / synthetic component)."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

from pykotor.common.indoorkit import Kit, KitComponent, KitComponentHook, KitDoor
from pykotor.common.indoormap import IndoorMap, IndoorMapRoom, _ensure_embedded_kit
from pykotor.common.tilekit import TileKit
from pykotor.resource.formats.bwm.bwm_data import BWM
from pykotor.resource.generics.utd import UTD
from pykotor.tools.tile_bwm import generate_flat_floor_quad, merge_translated_bwms
from utility.common.geometry import Vector3

_EMBEDDED_TILE = "__tile_compiled__"


@dataclass
class TileLayout:
    """Grid of floor template ids for a v2 tile kit (PyKotor `.indoor` extension)."""

    format_version: int = 1
    kit_id: str = ""
    cell_size: float = 4.0
    grid_w: int = 0
    grid_h: int = 0
    floor_cells: list[str | None] = field(default_factory=list)

    def cell_index(self, ix: int, iy: int) -> int:
        return iy * self.grid_w + ix


def _default_door() -> KitDoor:
    utd = UTD()
    utd.resref.set_data("sw_door")
    utd.tag = "tile_default_door"
    return KitDoor(utdK1=utd, utdK2=utd, width=2.0, height=3.0)


def tile_layout_to_merged_bwm(
    layout: TileLayout,
    tile_kit: TileKit,
    *,
    z: float = 0.0,
) -> BWM:
    """Build one merged world-space BWM from the floor layer."""
    if layout.grid_w <= 0 or layout.grid_h <= 0:
        return BWM()
    cell = float(layout.cell_size)
    parts: list[tuple[BWM, float, float, float]] = []
    for iy in range(layout.grid_h):
        for ix in range(layout.grid_w):
            idx = layout.cell_index(ix, iy)
            if idx >= len(layout.floor_cells):
                continue
            tid = layout.floor_cells[idx]
            if not tid:
                continue
            tpl = tile_kit.template_by_id(tid)
            if tpl is None:
                continue
            wx = float(ix) * cell
            wy = float(iy) * cell
            if tpl.wok and tpl.wok.faces:
                b = deepcopy(tpl.wok)
                parts.append(
                    (b, wx + tpl.offset.x, wy + tpl.offset.y, z + tpl.offset.z),
                )
            else:
                b = generate_flat_floor_quad(
                    min_x=0.0,
                    min_y=0.0,
                    size_x=cell,
                    size_y=cell,
                    z=0.0,
                )
                parts.append((b, wx, wy, z + tpl.offset.z))
    if not parts:
        return BWM()
    return merge_translated_bwms(parts)


def apply_tile_layout_to_map(
    im: IndoorMap,
    layout: TileLayout,
    tile_kit: TileKit,
    kits: list[Kit],
    *,
    floor_z: float = 0.0,
) -> None:
    """Replace map rooms with one compiled floor room; persist `tile_layout` on the map.

    The merged walkmesh and first non-empty floor template MDL/MDX are stored in EmbeddedKit.
    """
    merged = tile_layout_to_merged_bwm(layout, tile_kit, z=floor_z)
    mdl, mdx = b"", b""
    for tid in layout.floor_cells:
        if not tid:
            continue
        tpl = tile_kit.template_by_id(tid)
        if tpl and len(tpl.mdl) >= 12:
            mdl, mdx = tpl.mdl, tpl.mdx
            break
    ek = _ensure_embedded_kit(kits)
    if not ek.doors:
        ek.doors.append(_default_door())
    ek.components[:] = [c for c in ek.components if c.id != _EMBEDDED_TILE]
    comp = KitComponent(ek, "Tile floor (compiled)", _EMBEDDED_TILE, merged, mdl, mdx)
    if tile_kit.floors:
        ref = tile_kit.floors[0]
        for hook in ref.doorhooks:
            if hook.door in ek.doors:
                d = hook.door
            elif ek.doors:
                d = ek.doors[0]
            else:
                continue
            comp.hooks.append(
                KitComponentHook(
                    Vector3(hook.position.x, hook.position.y, hook.position.z),
                    hook.rotation,
                    hook.edge,
                    d,
                )
            )
    ek.components.append(comp)
    im.rooms.clear()
    im.rooms.append(
        IndoorMapRoom(
            comp,
            Vector3(0.0, 0.0, 0.0),
            0.0,
            flip_x=False,
            flip_y=False,
        )
    )
    im.tile_layout = {
        "format_version": layout.format_version,
        "kit_id": layout.kit_id,
        "cell_size": layout.cell_size,
        "grid_w": layout.grid_w,
        "grid_h": layout.grid_h,
        "floor_cells": list(layout.floor_cells),
    }
    im.indoor_map_version = max(im.indoor_map_version, 2)
