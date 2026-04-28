"""Headless 3D preview bridge: map a `TileKit` + `TileLayout` onto `pykotor.gl.scene.Scene`.

Kotor.NET (`GLEngine.Render`): dequeue GL thread work → viewport → clear → `GeometryRenderer.Render`,
which binds the standard shader, sets view/projection, then for each mesh descriptor binds textures
(two slots + placeholder) and draws.

PyKotor (`Scene.render`): sync caches → view/projection → main shader → iterate `RenderObject`s and
draw meshes (same conceptual pipeline; richer editor features).

Use inside a current OpenGL context (e.g. `QOpenGLWidget.paintGL`): call `upload_tile_kit_assets`,
then `populate_scene_tile_grid_floor_preview`, then `scene.render()`.
"""

from __future__ import annotations

import io

from pykotor.common.stream import BinaryReader
from pykotor.common.tilekit import TileKit
from pykotor.gl import eulerAngles, quat
from pykotor.gl.models.read_mdl import gl_load_stitched_model
from pykotor.gl.scene.scene import Scene
from pykotor.gl.shader import Texture
from pykotor.resource.formats.tpc.tpc_auto import read_tpc
from pykotor.tools.tilemap_compile import TileLayout
from utility.common.geometry import Vector3


def _quat_to_euler_v3(q_wxyz: object) -> Vector3:
    from pykotor.common.tilekit import QuaternionWXYZ

    if not isinstance(q_wxyz, QuaternionWXYZ):
        return Vector3()
    r = quat(q_wxyz.w, q_wxyz.x, q_wxyz.y, q_wxyz.z)
    e = eulerAngles(r)
    return Vector3(float(e.x), float(e.y), float(e.z))


def upload_tile_kit_assets(scene: Scene, tile_kit: TileKit) -> None:
    """Upload kit TGAs as TPC-derived textures and register template MDL/MDX in `scene.models`."""
    for resref, raw in tile_kit.textures.items():
        try:
            tpc = read_tpc(io.BytesIO(raw))
            scene.textures[resref] = Texture.from_tpc(tpc)
        except (OSError, ValueError):
            continue

    for tpl in tile_kit.all_templates():
        if len(tpl.mdl) < 12 or not tpl.mdx:
            continue
        try:
            mdl_r = BinaryReader.from_bytes(tpl.mdl, 12)
            mdx_r = BinaryReader.from_bytes(tpl.mdx)
            scene.models[tpl.resref] = gl_load_stitched_model(scene, mdl_r, mdx_r)
        except (OSError, ValueError, RuntimeError):
            continue


def populate_scene_tile_grid_floor_preview(
    scene: Scene,
    tile_kit: TileKit,
    layout: TileLayout,
    *,
    floor_z: float = 0.0,
    cell_override: float | None = None,
) -> None:
    """Place one `RenderObject` per non-empty floor cell (template `resref` model names)."""
    scene.objects.clear()
    scene.selection.clear()
    scene.invalidate_render_cache()

    cell = float(layout.cell_size if cell_override is None else cell_override)
    if layout.grid_w <= 0 or layout.grid_h <= 0:
        return

    for iy in range(layout.grid_h):
        for ix in range(layout.grid_w):
            idx = layout.cell_index(ix, iy)
            if idx >= len(layout.floor_cells):
                continue
            tid = layout.floor_cells[idx]
            if not tid:
                continue
            tpl = tile_kit.template_by_id(tid)
            if tpl is None or not tpl.resref:
                continue
            wx = float(ix) * cell + tpl.offset.x
            wy = float(iy) * cell + tpl.offset.y
            wz = floor_z + tpl.offset.z
            rot_euler = _quat_to_euler_v3(tpl.rotation)
            from pykotor.gl.scene.render_object import RenderObject  # noqa: PLC0415

            ro = RenderObject(tpl.resref, Vector3(wx, wy, wz), rot_euler)
            scene.objects[ro] = ro

    scene.invalidate_render_cache()
