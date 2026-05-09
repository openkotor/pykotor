"""Kotor.NET ``relocate/Room.cs`` + ``RoomEntity`` runtime mirror (pure Python).

Provides the same structural behaviour as the C# AreaDesigner domain layer:

- ``Room.FixWalls`` interior edge pairing
- ``Wall.Visible``, ``DoorFrame.Visible``, ``InnerCorner.Visible``, ``OuterCorner.Visible``
- JSON ↔ runtime round-trip aligned with ``AreaSerializer_V0_1`` (plus optional ``objects[]``)

Rendering order matches ``AreaEntity.RenderRoom``: floors (per tile), walls, doorframes, inner corners,
outer corners, room objects — see ``iter_render_instances``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

from pykotor.common.tilekit import (
    CornerHookTemplate,
    KitTileRecord,
    QuaternionWXYZ,
    TileKit,
    TileTemplate,
)
from pykotor.gl import decompose, inverse, mat4_cast, quat, translate, vec3, vec4
from pykotor.gl import glm as glm_mod
from utility.common.geometry import Vector3

# Match ``Room.FixWalls``: ``Vector3.Distance(...) < 0.01f``
_LINK_EPS_SQ = (0.01) ** 2


def _multiply(a: Any, b: Any) -> Any:
    return a * b


def _template_for_resref(kit: TileKit, resref: str) -> TileTemplate | None:
    if not resref:
        return None
    for t in kit.all_templates():
        if t.resref == resref or t.template_id == resref:
            return t
    return None


def _kit_tile_record(kit: TileKit, tile_template_id: str) -> KitTileRecord | None:
    for tr in kit.tiles:
        if tr.tile_id == tile_template_id:
            return tr
    return None


def _v3(v: Vector3) -> Any:
    return vec3(float(v.x), float(v.y), float(v.z))


def _mat_rt(q: Any, pos: Vector3) -> Any:
    return mat4_cast(q) * translate(_v3(pos))


def _glm_quat_from_net_xyzw(seq: list[float] | None) -> Any:
    if not seq or len(seq) < 4:
        return quat(1.0, 0.0, 0.0, 0.0)
    x, y, z, w = (float(seq[0]), float(seq[1]), float(seq[2]), float(seq[3]))
    return quat(w, x, y, z)


def _glm_quat_from_wxyz(qw: QuaternionWXYZ) -> Any:
    return quat(qw.w, qw.x, qw.y, qw.z)


def _mat4_translation_xyz(m: Any) -> tuple[float, float, float]:
    return (float(m[3][0]), float(m[3][1]), float(m[3][2]))


def _dist_sq(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx * dx + dy * dy + dz * dz


@dataclass
class ADWall:
    """Runtime wall slot on a tile (``relocate/Wall``)."""

    parent_tile: ADTile
    hook_index: int
    kit_id: str
    template_id: str
    doorframe_enabled: bool = True
    linked_tile: ADTile | None = None

    @property
    def visible(self) -> bool:
        return self.linked_tile is None


@dataclass
class ADFloor:
    kit_id: str
    template_id: str


@dataclass
class ADObject:
    kit_id: str
    template_id: str
    position: Vector3
    orientation_net: list[float]


@dataclass
class ADTile:
    room: ADRoom
    kit_id: str
    template_id: str
    local_position: Vector3
    orientation_net: list[float]
    floor: ADFloor
    ceiling: ADFloor | None = None
    walls: list[ADWall] = field(default_factory=list)
    kit_record: KitTileRecord | None = None

    def world_matrix(self, m_room: Any) -> Any:
        q_tile = _glm_quat_from_net_xyzw(self.orientation_net)
        m_local = _mat_rt(q_tile, self.local_position)
        return _multiply(m_room, m_local)


@dataclass
class ADRoom:
    position: Vector3
    orientation_net: list[float]
    tiles: list[ADTile] = field(default_factory=list)
    objects: list[ADObject] = field(default_factory=list)

    def world_matrix(self) -> Any:
        q = _glm_quat_from_net_xyzw(self.orientation_net)
        return _mat_rt(q, self.position)


@dataclass
class ADArea:
    rooms: list[ADRoom] = field(default_factory=list)


def fix_walls(room: ADRoom) -> None:
    """Mirror ``Room.FixWalls``: pair walls from different tiles by world hook positions."""
    for w in _iter_walls(room):
        w.linked_tile = None

    samples: list[tuple[ADWall, tuple[float, float, float]]] = []
    m_room = room.world_matrix()
    for tile in room.tiles:
        m_tile = tile.world_matrix(m_room)
        kt = tile.kit_record
        if kt is None:
            continue
        for w in tile.walls:
            if w.hook_index >= len(kt.wall_hooks):
                continue
            hook = kt.wall_hooks[w.hook_index]
            qw = _glm_quat_from_wxyz(hook.orientation)
            m_hook = _mat_rt(qw, hook.position)
            m_wall = _multiply(m_tile, m_hook)
            samples.append((w, _mat4_translation_xyz(m_wall)))

    for a in range(len(samples)):
        wa, pa = samples[a]
        for b in range(a + 1, len(samples)):
            wb, pb = samples[b]
            if wa.parent_tile is wb.parent_tile:
                continue
            if _dist_sq(pa, pb) <= _LINK_EPS_SQ:
                wa.linked_tile = wb.parent_tile
                wb.linked_tile = wa.parent_tile


def _iter_walls(room: ADRoom) -> Iterator[ADWall]:
    for t in room.tiles:
        yield from t.walls


def inner_corner_visible(ic: CornerHookTemplate, tile: ADTile) -> bool:
    """``InnerCorner.Visible`` from ``Room.cs``."""
    if not ic.adjacent:
        return False
    return all(tile.walls[j].linked_tile is None for j in ic.adjacent)


def outer_corner_visible(oc: CornerHookTemplate, tile: ADTile) -> bool:
    """``OuterCorner.Visible`` from ``Room.cs`` (circuit test)."""
    adj = oc.adjacent
    if len(adj) != 2:
        return False
    w0, w1 = tile.walls[adj[0]], tile.walls[adj[1]]
    if w0.linked_tile is None or w1.linked_tile is None:
        return False
    lt0, lt1 = w0.linked_tile, w1.linked_tile
    parent = tile

    def neighbor_tiles(other: ADTile) -> set[ADTile]:
        out: set[ADTile] = set()
        for w in other.walls:
            if w.linked_tile is not None and w.linked_tile is not parent:
                out.add(w.linked_tile)
        return out

    set_a = neighbor_tiles(lt0)
    set_b = neighbor_tiles(lt1)
    circuit = bool(set_a & set_b)
    return not circuit


def build_runtime_from_v01(
    area: dict[str, Any],
    kits_by_id: dict[str, TileKit],
) -> ADArea:
    """Construct runtime model from ``format: \"0.1\"`` JSON (optionally with ``objects`` per room)."""
    out = ADArea()
    rooms = area.get("rooms")
    if not isinstance(rooms, list):
        return out

    for room_data in rooms:
        if not isinstance(room_data, dict):
            continue
        pos_l = room_data.get("position") or [0.0, 0.0, 0.0]
        if len(pos_l) < 3:
            pos_l = [0.0, 0.0, 0.0]
        room = ADRoom(
            position=Vector3(float(pos_l[0]), float(pos_l[1]), float(pos_l[2])),
            orientation_net=list(room_data.get("orientation") or [0.0, 0.0, 0.0, 1.0])[:4],
        )

        tiles_l = room_data.get("tiles")
        if isinstance(tiles_l, list):
            for tile_data in tiles_l:
                if not isinstance(tile_data, dict):
                    continue
                kit_id = str(tile_data.get("kitID", ""))
                template_id = str(tile_data.get("templateID", ""))
                kit = kits_by_id.get(kit_id)
                if kit is None:
                    continue
                kt = _kit_tile_record(kit, template_id)
                pos_t = tile_data.get("position") or [0.0, 0.0, 0.0]
                if len(pos_t) < 3:
                    pos_t = [0.0, 0.0, 0.0]
                ori_t = tile_data.get("orientation") or [0.0, 0.0, 0.0, 1.0]
                floor_block = tile_data.get("floor")
                fk, ftid = kit_id, ""
                if isinstance(floor_block, dict):
                    fk = str(floor_block.get("kitID", kit_id))
                    ftid = str(floor_block.get("templateID", ""))
                ceiling_ad: ADFloor | None = None
                ceiling_block = tile_data.get("ceiling")
                if isinstance(ceiling_block, dict):
                    ck = str(ceiling_block.get("kitID", ""))
                    ctid = str(ceiling_block.get("templateID", ""))
                    if ck or ctid:
                        ceiling_ad = ADFloor(kit_id=ck or kit_id, template_id=ctid)
                tile = ADTile(
                    room=room,
                    kit_id=kit_id,
                    template_id=template_id,
                    local_position=Vector3(float(pos_t[0]), float(pos_t[1]), float(pos_t[2])),
                    orientation_net=list(ori_t)[:4] if isinstance(ori_t, list) else [0.0, 0.0, 0.0, 1.0],
                    floor=ADFloor(kit_id=fk, template_id=ftid),
                    ceiling=ceiling_ad,
                    kit_record=kt,
                )

                walls_saved = tile_data.get("walls")
                if kt is not None and isinstance(walls_saved, list):
                    for i, wall_block in enumerate(walls_saved):
                        if not isinstance(wall_block, dict):
                            continue
                        if i >= len(kt.wall_hooks):
                            break
                        wk = str(wall_block.get("kitID", kit_id))
                        wtid = str(wall_block.get("templateID", ""))
                        tile.walls.append(
                            ADWall(
                                parent_tile=tile,
                                hook_index=i,
                                kit_id=wk,
                                template_id=wtid,
                            ),
                        )
                room.tiles.append(tile)

        objs = room_data.get("objects")
        if isinstance(objs, list):
            for od in objs:
                if not isinstance(od, dict):
                    continue
                op = od.get("position") or [0.0, 0.0, 0.0]
                if len(op) < 3:
                    op = [0.0, 0.0, 0.0]
                room.objects.append(
                    ADObject(
                        kit_id=str(od.get("kitID", "")),
                        template_id=str(od.get("templateID", "")),
                        position=Vector3(float(op[0]), float(op[1]), float(op[2])),
                        orientation_net=list(od.get("orientation") or [0.0, 0.0, 0.0, 1.0])[:4],
                    ),
                )

        fix_walls(room)
        out.rooms.append(room)

    return out


def runtime_to_v01(area: ADArea) -> dict[str, Any]:
    """Serialize to ``AreaSerializer_V0_1``-shaped JSON (includes ``objects`` when present)."""
    rooms_out: list[dict[str, Any]] = []
    for room in area.rooms:
        pos = room.position
        tiles_js: list[dict[str, Any]] = []
        for tile in room.tiles:
            floor = tile.floor
            walls_js = [{"kitID": w.kit_id, "templateID": w.template_id} for w in tile.walls]
            ceil_js = {"kitID": "", "templateID": ""}
            if tile.ceiling:
                ceil_js = {"kitID": tile.ceiling.kit_id, "templateID": tile.ceiling.template_id}
            tiles_js.append(
                {
                    "kitID": tile.kit_id,
                    "templateID": tile.template_id,
                    "position": [tile.local_position.x, tile.local_position.y, tile.local_position.z],
                    "orientation": list(tile.orientation_net),
                    "floor": {"kitID": floor.kit_id, "templateID": floor.template_id},
                    "ceiling": ceil_js,
                    "walls": walls_js,
                },
            )
        rd: dict[str, Any] = {
            "position": [pos.x, pos.y, pos.z],
            "orientation": list(room.orientation_net),
            "tiles": tiles_js,
        }
        if room.objects:
            rd["objects"] = [
                {
                    "kitID": o.kit_id,
                    "templateID": o.template_id,
                    "position": [o.position.x, o.position.y, o.position.z],
                    "orientation": list(o.orientation_net),
                }
                for o in room.objects
            ]
        rooms_out.append(rd)

    return {"format": "0.1", "rooms": rooms_out}


def iter_render_instances(
    area: ADArea,
    kits_by_id: dict[str, TileKit],
    *,
    show_walls: bool = True,
    show_doors: bool = True,
    show_corners: bool = True,
    show_ceilings: bool = False,
    show_objects: bool = True,
    respect_adjacency_visibility: bool = True,
) -> Iterator[tuple[str, Any]]:
    """Yield ``(resref, world_mat4)`` in ``AreaEntity.RenderRoom`` order."""

    def add_model(resref: str, world: Any) -> Iterator[tuple[str, Any]]:
        if resref:
            yield (resref, world)

    for room in area.rooms:
        m_room = room.world_matrix()
        # --- Floors (per tile, tile iteration order) ---
        for tile in room.tiles:
            kit = kits_by_id.get(tile.kit_id)
            if kit is None:
                continue
            ftpl = _template_for_resref(kit, tile.floor.template_id)
            if ftpl is not None and ftpl.resref:
                yield from add_model(ftpl.resref, tile.world_matrix(m_room))

            if show_ceilings and tile.ceiling and tile.ceiling.template_id:
                ckit = kits_by_id.get(tile.ceiling.kit_id) or kit
                ctpl = _template_for_resref(ckit, tile.ceiling.template_id)
                if ctpl is not None and ctpl.resref:
                    yield from add_model(ctpl.resref, tile.world_matrix(m_room))

        # --- Walls + doorframes ---
        if show_walls:
            for tile in room.tiles:
                kit = kits_by_id.get(tile.kit_id)
                kt = tile.kit_record
                if kit is None or kt is None:
                    continue
                m_tile = tile.world_matrix(m_room)
                for i, w in enumerate(tile.walls):
                    if respect_adjacency_visibility and not w.visible:
                        continue
                    if i >= len(kt.wall_hooks):
                        continue
                    wkit = kits_by_id.get(w.kit_id) or kit
                    wtpl = _template_for_resref(wkit, w.template_id)
                    if wtpl is None or not wtpl.resref:
                        continue
                    hook = kt.wall_hooks[i]
                    q_h = _glm_quat_from_wxyz(hook.orientation)
                    m_hook = _mat_rt(q_h, hook.position)
                    m_wall = _multiply(m_tile, m_hook)
                    yield from add_model(wtpl.resref, m_wall)
                    if (
                        show_doors
                        and w.doorframe_enabled
                        and wtpl.doorframe_id
                        and wtpl.doorframe_hooks
                        and (df := _template_for_resref(wkit, wtpl.doorframe_id)) is not None
                    ):
                        dh = wtpl.doorframe_hooks[-1]
                        q_df = _glm_quat_from_wxyz(dh.orientation)
                        m_df_loc = _mat_rt(q_df, dh.position)
                        m_df = _multiply(m_wall, m_df_loc)
                        yield from add_model(df.resref, m_df)

        # --- Corners ---
        if show_corners:
            for tile in room.tiles:
                kit = kits_by_id.get(tile.kit_id)
                kt = tile.kit_record
                if kit is None or kt is None:
                    continue
                m_tile = tile.world_matrix(m_room)
                for ic in kt.inner_corner_hooks:
                    if respect_adjacency_visibility and not inner_corner_visible(ic, tile):
                        continue
                    itpl = _template_for_resref(kit, ic.default_corner_id)
                    if itpl is None or not itpl.resref:
                        continue
                    q_h = _glm_quat_from_wxyz(ic.orientation)
                    m_h = _multiply(m_tile, _mat_rt(q_h, ic.position))
                    yield from add_model(itpl.resref, m_h)
                for oc in kt.outer_corner_hooks:
                    if respect_adjacency_visibility and not outer_corner_visible(oc, tile):
                        continue
                    otpl = _template_for_resref(kit, oc.default_corner_id)
                    if otpl is None or not otpl.resref:
                        continue
                    q_h = _glm_quat_from_wxyz(oc.orientation)
                    m_h = _multiply(m_tile, _mat_rt(q_h, oc.position))
                    yield from add_model(otpl.resref, m_h)

        # --- Objects (room scope), ``AreaExporter`` uses local transform then ``RoomToMDL`` —
        # ``AreaEntity`` applies ``LocalTransform`` only; we apply ``room`` like PyKotor preview. ---
        if show_objects:
            for obj in room.objects:
                okit = kits_by_id.get(obj.kit_id)
                if okit is None:
                    continue
                otpl = _template_for_resref(okit, obj.template_id)
                if otpl is None or not otpl.resref:
                    continue
                q_o = _glm_quat_from_net_xyzw(obj.orientation_net)
                m_obj_local = _mat_rt(q_o, obj.position)
                m_obj = _multiply(m_room, m_obj_local)
                yield from add_model(otpl.resref, m_obj)


def quat_yaw_pi() -> Any:
    """``Quaternion.CreateFromYawPitchRoll(0, 0, PI)`` for ``Tile.Extend``."""
    return quat(0.0, 0.0, 0.0, -1.0)  # 180° about Z in common game coords — matches yaw roll 0,0,pi z-up


def tile_extend_wall(
    tile: ADTile,
    wall_index: int,
    new_tile_template_id: str,
    kits_by_id: dict[str, TileKit],
) -> ADTile:
    """Mirror ``Tile.Extend`` / ``Wall.Extend`` from ``Room.cs`` (new tile in same room)."""
    kit = kits_by_id.get(tile.kit_id)
    if kit is None:
        msg = f"Unknown kit {tile.kit_id!r}"
        raise ValueError(msg)
    kt_src = tile.kit_record
    if kt_src is None:
        msg = "Source tile has no kit tile record"
        raise ValueError(msg)
    new_tpl_rec = _kit_tile_record(kit, new_tile_template_id)
    if new_tpl_rec is None:
        msg = f"Unknown tile template {new_tile_template_id!r} in kit {tile.kit_id!r}"
        raise ValueError(msg)

    if wall_index < 0 or wall_index >= len(tile.walls):
        msg = f"Wall index {wall_index} out of range"
        raise ValueError(msg)
    wall = tile.walls[wall_index]
    # Matching wall on new tile: same wall **template id** as source wall's slot default was designed for;
    # C# matches ``x.Template.ID == wall.Template.ID`` on **WallTemplate.ID**.
    candidate_idx: int | None = None
    for j, wn in enumerate(new_tpl_rec.wall_hooks):
        dw = _template_for_resref(kit, wn.default_wall_id)
        if dw is not None and dw.template_id == wall.template_id:
            candidate_idx = j
            break
    if candidate_idx is None:
        # Fallback: first hook with same default wall template id string
        for j, wn in enumerate(new_tpl_rec.wall_hooks):
            if wn.default_wall_id == wall.template_id:
                candidate_idx = j
                break
    if candidate_idx is None:
        msg = "Could not find compatible wall hook on new tile template for Extend"
        raise ValueError(msg)

    adjacent_hook = new_tpl_rec.wall_hooks[candidate_idx]
    room = tile.room
    hook_old = kt_src.wall_hooks[wall_index]
    q_wall = _glm_quat_from_wxyz(hook_old.orientation)
    q_adj = _glm_quat_from_wxyz(adjacent_hook.orientation)
    q_yaw = quat_yaw_pi()

    m_room = room.world_matrix()
    m_tile_old = tile.world_matrix(m_room)
    q_tile_world = _decompose_rotation(m_tile_old)
    q_room_world = _decompose_rotation(m_room)

    # ``Tile.Extend``: wall.LocalOrientation / adjacent.Hook.LocalOrientation * yaw * Orientation / Parent.Orientation
    q_local = q_wall * inverse(q_adj) * q_yaw * q_tile_world * inverse(q_room_world)

    q_tile_old = _glm_quat_from_net_xyzw(tile.orientation_net)
    t_add = _transform_vec3_by_quat(q_tile_old, hook_old.position)
    t_sub = _transform_vec3_by_quat(q_local, adjacent_hook.position)
    new_pos = tile.local_position + t_add - t_sub

    ceil_ad: ADFloor | None = None
    if new_tpl_rec.default_ceiling_id:
        ceil_ad = ADFloor(kit_id=tile.kit_id, template_id=new_tpl_rec.default_ceiling_id)

    new_tile = ADTile(
        room=room,
        kit_id=tile.kit_id,
        template_id=new_tile_template_id,
        local_position=new_pos,
        orientation_net=_net_xyzw_from_glm_quat(q_local),
        floor=ADFloor(kit_id=tile.kit_id, template_id=new_tpl_rec.default_floor_id or ""),
        ceiling=ceil_ad,
        kit_record=new_tpl_rec,
    )
    # Populate walls from kit hooks + default templates
    for i, _wh in enumerate(new_tpl_rec.wall_hooks):
        dw = _template_for_resref(kit, _wh.default_wall_id)
        tid = dw.template_id if dw is not None else _wh.default_wall_id
        kid = dw.kit_id if dw is not None else tile.kit_id
        new_tile.walls.append(
            ADWall(parent_tile=new_tile, hook_index=i, kit_id=kid, template_id=tid),
        )

    room.tiles.append(new_tile)
    fix_walls(room)
    return new_tile


def _decompose_rotation(m: Any) -> Any:
    """Extract quaternion rotation from a 4×4 transform (PyGLM ``decompose``)."""
    scale = glm_mod.vec3()
    rotation = glm_mod.quat()
    translation = glm_mod.vec3()
    skew = glm_mod.vec3()
    persp = glm_mod.vec4()
    decompose(m, scale, rotation, translation, skew, persp)
    return rotation


def _transform_vec3_by_quat(q: Any, v: Vector3) -> Vector3:
    """``Vector3.Transform(v, q)`` (System.Numerics): rotate vector by unit quaternion."""
    mm = mat4_cast(q)
    r = mm * vec4(float(v.x), float(v.y), float(v.z), 1.0)
    return Vector3(float(r.x), float(r.y), float(r.z))


def _net_xyzw_from_glm_quat(q: Any) -> list[float]:
    """glm quat (w,x,y,z) → .NET ``[x,y,z,w]``."""
    return [float(q.x), float(q.y), float(q.z), float(q.w)]


def switch_wall_template(
    wall: ADWall,
    wall_template_id: str,
    kits_by_id: dict[str, TileKit],
) -> None:
    """Mirror ``Wall.SwitchTemplate`` — updates kit/template refs and doorframe presence."""
    kit = kits_by_id.get(wall.kit_id)
    if kit is None:
        msg = f"Unknown kit {wall.kit_id!r}"
        raise ValueError(msg)
    wtpl = _template_for_resref(kit, wall_template_id)
    if wtpl is None:
        msg = f"Unknown wall template {wall_template_id!r}"
        raise ValueError(msg)
    wall.template_id = wtpl.template_id
    wall.kit_id = kit.kit_id  # TileKit.kit_id matches wall kit from template
    wall.doorframe_enabled = bool(wtpl.doorframe_id)


def add_room_with_tile(
    area: ADArea,
    *,
    kit_id: str,
    tile_template_id: str,
    position: Vector3,
    orientation_net: list[float],
    kits_by_id: dict[str, TileKit],
) -> ADRoom:
    """Create a room with a single tile (minimal ``AddRoomMode`` / ``Room(RoomTemplate)`` analogue)."""
    kit = kits_by_id.get(kit_id)
    if kit is None:
        msg = f"Unknown kit {kit_id!r}"
        raise ValueError(msg)
    kt = _kit_tile_record(kit, tile_template_id)
    if kt is None:
        msg = f"Unknown tile template {tile_template_id!r}"
        raise ValueError(msg)

    room = ADRoom(position=position, orientation_net=list(orientation_net)[:4])
    ceil_ad: ADFloor | None = None
    if kt.default_ceiling_id:
        ceil_ad = ADFloor(kit_id=kit_id, template_id=kt.default_ceiling_id)
    tile = ADTile(
        room=room,
        kit_id=kit_id,
        template_id=tile_template_id,
        local_position=Vector3(0.0, 0.0, 0.0),
        orientation_net=[0.0, 0.0, 0.0, 1.0],
        floor=ADFloor(kit_id=kit_id, template_id=kt.default_floor_id or ""),
        ceiling=ceil_ad,
        kit_record=kt,
    )
    for i, _wh in enumerate(kt.wall_hooks):
        dw = _template_for_resref(kit, _wh.default_wall_id)
        tid = dw.template_id if dw is not None else _wh.default_wall_id
        kid = dw.kit_id if dw is not None else kit_id
        tile.walls.append(ADWall(parent_tile=tile, hook_index=i, kit_id=kid, template_id=tid))
    room.tiles.append(tile)
    fix_walls(room)
    area.rooms.append(room)
    return room


def add_object_to_room(
    room: ADRoom,
    *,
    kit_id: str,
    template_id: str,
    position: Vector3,
    orientation_net: list[float],
) -> None:
    """Append a room-scoped placeable (``Room.AddObject``)."""
    room.objects.append(
        ADObject(
            kit_id=kit_id,
            template_id=template_id,
            position=position,
            orientation_net=list(orientation_net)[:4],
        ),
    )
