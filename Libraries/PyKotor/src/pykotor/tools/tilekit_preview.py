"""Bridge Kotor.NET AreaDesigner scene graph to `pykotor.gl.scene.Scene`.

`RoomEntity` / `AreaEntity` in Kotor.NET gather mesh descriptors per tile (floor), wall,
doorframe, corners, and objects with transforms (`Transform = Local * Parent` chain).

PyKotor matches that draw order by placing `RenderObject`s with `set_transform(mat4)` built from
the same quaternion × translation factors as `Matrix4x4.CreateFromQuaternion *
Matrix4x4.CreateTranslation` in C# (rotation × translation in GLM).

Also supports the simpler PyKotor `TileLayout` grid (floors only) for `.indoor` `tile_layout`.
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
from pykotor.gl import eulerAngles, mat4, mat4_cast, quat, translate, vec3
from pykotor.gl.models.read_mdl import gl_load_stitched_model
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
) -> None:
    """Populate `scene.objects` like `AreaEntity.GetMeshDescriptors` (Kotor.NET).

    Expects `area` JSON with ``format: \"0.1\"`` and ``rooms[]`` as saved by `AreaSerializer_V0_1`.
    """
    scene.objects.clear()
    scene.selection.clear()
    scene.invalidate_render_cache()

    rooms = area.get("rooms")
    if not isinstance(rooms, list):
        scene.invalidate_render_cache()
        return

    def add_model(resref: str, world: Any) -> None:
        if not resref:
            return
        ro = RenderObject(resref)
        ro.set_transform(world)
        scene.objects[ro] = ro

    for room_data in rooms:
        if not isinstance(room_data, dict):
            continue
        pos_l = room_data.get("position") or [0.0, 0.0, 0.0]
        if len(pos_l) < 3:
            pos_l = [0.0, 0.0, 0.0]
        room_pos = Vector3(float(pos_l[0]), float(pos_l[1]), float(pos_l[2]))
        q_room = _quat_from_net_xyzw(room_data.get("orientation"))
        m_room = _mat_rt(q_room, room_pos)

        tiles = room_data.get("tiles")
        if not isinstance(tiles, list):
            continue

        for tile_data in tiles:
            if not isinstance(tile_data, dict):
                continue
            kit_id = str(tile_data.get("kitID", ""))
            template_id = str(tile_data.get("templateID", ""))
            kit = kits_by_id.get(kit_id)
            if kit is None:
                continue

            pos_l = tile_data.get("position") or [0.0, 0.0, 0.0]
            if len(pos_l) < 3:
                pos_l = [0.0, 0.0, 0.0]
            tile_pos = Vector3(float(pos_l[0]), float(pos_l[1]), float(pos_l[2]))
            q_tile = _quat_from_net_xyzw(tile_data.get("orientation"))
            m_tile_local = _mat_rt(q_tile, tile_pos)
            # Column vectors: world = parent * local (matches C# child * parent multiply order).
            m_tile = _multiply(m_room, m_tile_local)

            kt = _kit_tile_record(kit, template_id)

            floor_block = tile_data.get("floor")
            if isinstance(floor_block, dict):
                fk = str(floor_block.get("kitID", kit_id))
                ftid = str(floor_block.get("templateID", ""))
                fkit = kits_by_id.get(fk) or kit
                ftpl = _template_for_resref(fkit, ftid)
                if ftpl is not None and ftpl.resref:
                    add_model(ftpl.resref, m_tile)

            if show_ceilings and isinstance(tile_data.get("ceiling"), dict):
                ck = str(tile_data["ceiling"].get("kitID", ""))
                ctid = str(tile_data["ceiling"].get("templateID", ""))
                if ck and ctid:
                    ckit = kits_by_id.get(ck) or kit
                    ctpl = _template_for_resref(ckit, ctid)
                    if ctpl is not None and ctpl.resref:
                        add_model(ctpl.resref, m_tile)

            walls_saved = tile_data.get("walls")
            if show_walls and isinstance(walls_saved, list) and kt is not None:
                for i, wall_block in enumerate(walls_saved):
                    if not isinstance(wall_block, dict):
                        continue
                    wk = str(wall_block.get("kitID", kit_id))
                    wtid = str(wall_block.get("templateID", ""))
                    wkit = kits_by_id.get(wk) or kit
                    wtpl = _template_for_resref(wkit, wtid)
                    if wtpl is None or not wtpl.resref:
                        continue
                    if i >= len(kt.wall_hooks):
                        continue
                    hook = kt.wall_hooks[i]
                    q_h = _quat_from_py_wxyz(hook.orientation)
                    m_hook = _mat_rt(q_h, hook.position)
                    m_wall = _multiply(m_tile, m_hook)
                    add_model(wtpl.resref, m_wall)
                    if (
                        show_doors
                        and wtpl.doorframe_id
                        and wtpl.doorframe_hooks
                        and (df := _template_for_resref(wkit, wtpl.doorframe_id)) is not None
                    ):
                        for dh in wtpl.doorframe_hooks:
                            q_df = _quat_from_py_wxyz(dh.orientation)
                            m_df_loc = _mat_rt(q_df, dh.position)
                            m_df = _multiply(m_wall, m_df_loc)
                            add_model(df.resref, m_df)

            if show_corners and kt is not None:
                for ic in kt.inner_corner_hooks:
                    itpl = _template_for_resref(kit, ic.default_corner_id)
                    if itpl is None or not itpl.resref:
                        continue
                    q_h = _quat_from_py_wxyz(ic.orientation)
                    m_h = _multiply(m_tile, _mat_rt(q_h, ic.position))
                    add_model(itpl.resref, m_h)
                for oc in kt.outer_corner_hooks:
                    otpl = _template_for_resref(kit, oc.default_corner_id)
                    if otpl is None or not otpl.resref:
                        continue
                    q_h = _quat_from_py_wxyz(oc.orientation)
                    m_h = _multiply(m_tile, _mat_rt(q_h, oc.position))
                    add_model(otpl.resref, m_h)

        objects_l = room_data.get("objects")
        if isinstance(objects_l, list):
            for od in objects_l:
                if not isinstance(od, dict):
                    continue
                ok = str(od.get("kitID", ""))
                otid = str(od.get("templateID", ""))
                okit = kits_by_id.get(ok)
                if okit is None:
                    continue
                otpl = _template_for_resref(okit, otid)
                if otpl is None or not otpl.resref:
                    continue
                opos_l = od.get("position") or [0.0, 0.0, 0.0]
                if len(opos_l) < 3:
                    opos_l = [0.0, 0.0, 0.0]
                o_pos = Vector3(float(opos_l[0]), float(opos_l[1]), float(opos_l[2]))
                q_o = _quat_from_net_xyzw(od.get("orientation"))
                m_obj_local = _mat_rt(q_o, o_pos)
                m_obj = _multiply(m_room, m_obj_local)
                add_model(otpl.resref, m_obj)

    scene.invalidate_render_cache()
