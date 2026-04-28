"""Bridge Kotor.NET AreaDesigner scene graph to `pykotor.gl.scene.Scene`.

`AreaEntity.GetMeshDescriptors` draws **floors, walls, doorframes, inner corners, outer corners**
(per tile), then **objects** at room scope (`Room.Objects`). `AreaExporter.RoomToMDL` stitches the
same categories (ceilings commented out in .NET).

Doorframe world pose matches `DoorFrame` in `Room.cs`: ``LocalTransform`` uses **only the last**
template hook (`Template.Hooks.Last()`).

When ``respect_adjacency_visibility`` is set (Toolset default), wall pairing follows ``Room.FixWalls``
(interior walls hidden), ``InnerCorner.Visible`` / ``OuterCorner.Visible`` from ``Room.cs`` (via
``area_designer_runtime``).

Also supports PyKotor `TileLayout` (floors only) for `.indoor` `tile_layout`.
"""

from __future__ import annotations

import io
from typing import TYPE_CHECKING, Any

from pykotor.common.stream import BinaryReader
from pykotor.common.tilekit import (
    KitTileRecord,
    QuaternionWXYZ,
    TileKit,
    TileTemplate,
)
from pykotor.gl import eulerAngles, mat4_cast, quat, translate, vec3
from pykotor.gl.models.read_mdl import gl_load_stitched_model
from pykotor.tools.area_designer_runtime import build_runtime_from_v01, iter_render_instances
from pykotor.gl.scene.render_object import RenderObject
from pykotor.gl.scene.scene import Scene
from pykotor.gl.shader import Texture
from pykotor.resource.formats.tpc.tpc_auto import read_tpc
from pykotor.tools.tilemap_compile import TileLayout
from utility.common.geometry import Vector3

if TYPE_CHECKING:
    pass


def _quat_to_euler_v3(q_wxyz: QuaternionWXYZ) -> Vector3:
    r = quat(q_wxyz.w, q_wxyz.x, q_wxyz.y, q_wxyz.z)
    e = eulerAngles(r)
    return Vector3(float(e.x), float(e.y), float(e.z))


def _v3(v: Vector3) -> Any:
    return vec3(float(v.x), float(v.y), float(v.z))


def _quat_from_net_xyzw(seq: list[float] | None) -> Any:
    """System.Numerics JSON order ``[x, y, z, w]``."""
    if not seq or len(seq) < 4:
        return quat(1.0, 0.0, 0.0, 0.0)
    x, y, z, w = (float(seq[0]), float(seq[1]), float(seq[2]), float(seq[3]))
    return quat(w, x, y, z)


def _quat_from_py_wxyz(q: QuaternionWXYZ) -> Any:
    return quat(q.w, q.x, q.y, q.z)


def _mat_rt(q: Any, pos: Vector3) -> Any:
    """Match C# ``Matrix4x4.CreateFromQuaternion * CreateFromTranslation``."""
    return mat4_cast(q) * translate(_v3(pos))


def _multiply(a: Any, b: Any) -> Any:
    return a * b


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


def _template_for_resref(kit: TileKit, resref: str) -> TileTemplate | None:
    for t in kit.all_templates():
        if t.resref == resref or t.template_id == resref:
            return t
    return None


def _kit_tile_record(kit: TileKit, tile_template_id: str) -> KitTileRecord | None:
    for tr in kit.tiles:
        if tr.tile_id == tile_template_id:
            return tr
    return None


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
            ro = RenderObject(tpl.resref, Vector3(wx, wy, wz), rot_euler)
            scene.objects[ro] = ro

    scene.invalidate_render_cache()


def populate_scene_from_area_designer_v01(
    scene: Scene,
    area: dict[str, Any],
    kits_by_id: dict[str, TileKit],
    *,
    show_walls: bool = True,
    show_doors: bool = True,
    show_corners: bool = True,
    show_ceilings: bool = False,
    show_objects: bool = True,
    respect_adjacency_visibility: bool = True,
) -> None:
    """Populate `scene.objects` like `AreaEntity.GetMeshDescriptors` (Kotor.NET).

    Expects `area` JSON with ``format: \"0.1\"`` and ``rooms[]`` as saved by `AreaSerializer_V0_1`.

    Delegates to :func:`build_runtime_from_v01` and :func:`iter_render_instances` so preview matches
    the Area Designer runtime (``Room.FixWalls``, wall/corner visibility).
    """
    scene.objects.clear()
    scene.selection.clear()
    scene.invalidate_render_cache()

    runtime = build_runtime_from_v01(area, kits_by_id)

    def add_model(resref: str, world: Any) -> None:
        if not resref:
            return
        ro = RenderObject(resref)
        ro.set_transform(world)
        scene.objects[ro] = ro

    for resref, world in iter_render_instances(
        runtime,
        kits_by_id,
        show_walls=show_walls,
        show_doors=show_doors,
        show_corners=show_corners,
        show_ceilings=show_ceilings,
        show_objects=show_objects,
        respect_adjacency_visibility=respect_adjacency_visibility,
    ):
        add_model(resref, world)

    scene.invalidate_render_cache()
