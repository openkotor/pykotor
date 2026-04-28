"""Stable operations API for the indoor Area Designer runtime (Kotor.NET ``Room`` / ``Tile`` parity).

Prefer importing from here in Toolset code so call sites stay decoupled from
``area_designer_runtime`` internals.
"""

from __future__ import annotations

from pykotor.tools.area_designer_runtime import (
    ADArea,
    ADObject,
    ADRoom,
    ADTile,
    ADWall,
    add_object_to_room,
    add_room_with_tile,
    build_runtime_from_v01,
    fix_walls,
    inner_corner_visible,
    iter_render_instances,
    outer_corner_visible,
    runtime_to_v01,
    switch_wall_template,
    tile_extend_wall,
)

__all__ = [
    "ADArea",
    "ADObject",
    "ADRoom",
    "ADTile",
    "ADWall",
    "add_object_to_room",
    "add_room_with_tile",
    "build_runtime_from_v01",
    "fix_walls",
    "inner_corner_visible",
    "iter_render_instances",
    "outer_corner_visible",
    "runtime_to_v01",
    "switch_wall_template",
    "tile_extend_wall",
]
