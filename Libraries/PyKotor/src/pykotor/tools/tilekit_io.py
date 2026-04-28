"""Load format_version 2 tile kits (Kotor.NET `KitSerializer_V0_1` semantics) from disk."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

from pykotor.common.indoorkit import KitComponentHook, KitDoor
from pykotor.common.stream import BinaryReader
from pykotor.common.tilekit import (
    CornerHookTemplate,
    DoorframeHookTemplate,
    KitTileRecord,
    QuaternionWXYZ,
    TileKit,
    TileTemplate,
    TileTemplateKind,
    WallHookTemplate,
)
from pykotor.resource.formats.bwm import read_bwm
from pykotor.resource.formats.bwm.bwm_data import BWM
from pykotor.resource.generics.utd import read_utd
from utility.common.geometry import Vector3

if TYPE_CHECKING:
    import os

    MissingFileInfo = tuple[str, Path, str]

_NUM_RE = re.compile(r"(\d+)")


def _get_nums(s: str) -> list[int]:
    return [int(m.group(1)) for m in _NUM_RE.finditer(s)]


def _load_binary(
    file_path: Path,
    *,
    kit_name: str,
    kind: str,
    missing_files: list[MissingFileInfo] | None,
) -> bytes | None:
    if missing_files is None:
        return BinaryReader.load_file(file_path) if file_path.is_file() else None
    if not file_path.is_file():
        missing_files.append((kit_name, file_path, kind))
        return None
    try:
        return BinaryReader.load_file(file_path)
    except FileNotFoundError:
        missing_files.append((kit_name, file_path, kind))
        return None


def _load_textures_txi(
    folder_path: Path,
    target: dict[str, bytes],
    txis: dict[str, bytes],
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
    kind: str,
    use_upper_txi_name: bool,
) -> None:
    if not folder_path.is_dir():
        return
    for tga_file in (f for f in folder_path.iterdir() if f.suffix.lower() == ".tga"):
        resref = tga_file.stem.upper()
        raw = _load_binary(tga_file, kit_name=kit_name, kind=kind, missing_files=missing_files)
        if raw is not None:
            target[resref] = raw
        txi_stem = resref if use_upper_txi_name else tga_file.stem
        txi_path = folder_path / f"{txi_stem}.txi"
        txis[resref] = BinaryReader.load_file(txi_path) if txi_path.is_file() else b""


def _load_skyboxes_tilekit(
    kit: TileKit,
    skyboxes_path: Path,
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
) -> None:
    if not skyboxes_path.is_dir():
        return
    for skybox_str in (f.stem.upper() for f in skyboxes_path.iterdir() if f.suffix.lower() == ".mdl"):
        mdl_path = skyboxes_path / f"{skybox_str}.mdl"
        mdx_path = skyboxes_path / f"{skybox_str}.mdx"
        mdl = _load_binary(mdl_path, kit_name=kit_name, kind="skybox model", missing_files=missing_files)
        mdx = _load_binary(mdx_path, kit_name=kit_name, kind="skybox model", missing_files=missing_files)
        if mdl and mdx:
            from pykotor.common.indoorkit import MDLMDXTuple  # noqa: PLC0415

            kit.skyboxes[skybox_str] = MDLMDXTuple(mdl, mdx)


def _load_doorway_padding_tilekit(
    kit: TileKit,
    doorway_path: Path,
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
) -> None:
    if not doorway_path.is_dir():
        return
    from pykotor.common.indoorkit import MDLMDXTuple  # noqa: PLC0415

    for padding_id in (f.stem for f in doorway_path.iterdir() if f.suffix.lower() == ".mdl"):
        mdl_path = doorway_path / f"{padding_id}.mdl"
        mdx_path = doorway_path / f"{padding_id}.mdx"
        mdl = _load_binary(mdl_path, kit_name=kit_name, kind="doorway padding", missing_files=missing_files)
        mdx = _load_binary(mdx_path, kit_name=kit_name, kind="doorway padding", missing_files=missing_files)
        if mdl is None or mdx is None:
            continue
        nums = _get_nums(padding_id)
        if len(nums) < 2:
            continue
        door_id, padding_size = nums[0], nums[1]
        tup = MDLMDXTuple(mdl, mdx)
        if padding_id.lower().startswith("side"):
            kit.side_padding.setdefault(door_id, {})[padding_size] = tup
        if padding_id.lower().startswith("top"):
            kit.top_padding.setdefault(door_id, {})[padding_size] = tup


def _load_doors_tilekit(
    kit: TileKit,
    doors_json: list[dict],
    base_path: Path,
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
) -> None:
    for door_json in doors_json:
        try:
            utd_k1_path = base_path / f"{door_json['utd_k1']}.utd"
            utd_k2_path = base_path / f"{door_json['utd_k2']}.utd"
        except (KeyError, TypeError, ValueError):
            continue
        try:
            utd_k1 = read_utd(utd_k1_path)
            utd_k2 = read_utd(utd_k2_path)
        except FileNotFoundError as e:
            if missing_files is not None:
                missing_files.append((kit_name, Path(e.filename or ""), "door utd"))
            continue
        w = float(door_json.get("width", 2.0))
        h = float(door_json.get("height", 3.0))
        kit.doors.append(KitDoor(utd_k1, utd_k2, w, h))


def _parse_doorhooks(
    doorhooks_json: list[dict],
    doors: list[KitDoor],
) -> list[KitComponentHook]:
    hooks: list[KitComponentHook] = []
    for h in doorhooks_json:
        try:
            pos = Vector3(float(h["x"]), float(h["y"]), float(h["z"]))
            rot = float(h["rotation"])
            di = int(h["door"])
            edge = int(h["edge"])
            if di < 0 or di >= len(doors):
                continue
            hooks.append(KitComponentHook(pos, rot, edge, doors[di]))
        except (KeyError, TypeError, ValueError, IndexError):
            continue
    return hooks


def _vec3_from_json(seq: object) -> Vector3:
    if not isinstance(seq, (list, tuple)) or len(seq) < 3:
        return Vector3.from_null()
    return Vector3(float(seq[0]), float(seq[1]), float(seq[2]))


def _parse_kotor_net_orient(data: object) -> QuaternionWXYZ:
    if isinstance(data, list) and len(data) >= 4:
        return QuaternionWXYZ.from_kotor_net_float_array([float(x) for x in data[:4]])
    return QuaternionWXYZ()


def _parse_kotor_net_orient_wxyz(data: object) -> QuaternionWXYZ:
    if isinstance(data, list) and len(data) >= 4:
        return QuaternionWXYZ.from_json_wxyz([float(x) for x in data[:4]])
    return QuaternionWXYZ()


def _load_template_entry(
    data: dict,
    kind: TileTemplateKind,
    resref: str,
    base_path: Path,
    doors: list[KitDoor],
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
    *,
    kotor_net_json: bool,
) -> TileTemplate:
    offset_l = data.get("offset", [0.0, 0.0, 0.0])
    if not isinstance(offset_l, (list, tuple)) or len(offset_l) < 3:
        offset_l = [0.0, 0.0, 0.0]
    offset = Vector3(float(offset_l[0]), float(offset_l[1]), float(offset_l[2]))
    rot_raw = data.get("rotation")
    quat = (
        _parse_kotor_net_orient(rot_raw)
        if kotor_net_json
        else _parse_kotor_net_orient_wxyz(rot_raw)
    )
    wok_path = base_path / f"{resref}.wok"
    mdl_path = base_path / f"{resref}.mdl"
    mdx_path = base_path / f"{resref}.mdx"
    wok: BWM | None = None
    wok_bytes = _load_binary(wok_path, kit_name=kit_name, kind="walkmesh", missing_files=None)
    if wok_bytes:
        wok = read_bwm(wok_bytes)
    mdl = _load_binary(mdl_path, kit_name=kit_name, kind="model", missing_files=None) or b""
    mdx = _load_binary(mdx_path, kit_name=kit_name, kind="mdx", missing_files=None) or b""
    th = _parse_doorhooks(data.get("doorhooks", []), doors)
    df_hooks_raw = data.get("hooks") or []
    df_hooks: list[DoorframeHookTemplate] = []
    if isinstance(df_hooks_raw, list):
        for h in df_hooks_raw:
            if not isinstance(h, dict):
                continue
            try:
                pos = _vec3_from_json(h.get("position"))
                orient = _parse_kotor_net_orient(h.get("orientation"))
                df_hooks.append(DoorframeHookTemplate(position=pos, orientation=orient))
            except (TypeError, ValueError):
                continue
    doorframe_id = data.get("doorframeID")
    if doorframe_id is not None:
        doorframe_id = str(doorframe_id)
    return TileTemplate(
        kind=kind,
        template_id=str(data.get("id", resref)),
        resref=resref,
        offset=offset,
        rotation=quat,
        mdl=mdl,
        mdx=mdx,
        wok=wok,  # type: ignore[arg-type]
        doorhooks=th,
        doorframe_hooks=df_hooks,
        doorframe_id=doorframe_id,
    )


def _load_template_list(
    items: list[dict] | None,
    kind: TileTemplateKind,
    base_path: Path,
    doors: list[KitDoor],
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
    *,
    kotor_net_json: bool,
) -> list[TileTemplate]:
    if not items:
        return []
    out: list[TileTemplate] = []
    for data in items:
        if not isinstance(data, dict):
            continue
        resref = str(data.get("model") or data.get("resref") or data.get("id") or "")
        if not resref:
            continue
        out.append(
            _load_template_entry(
                data,
                kind,
                resref,
                base_path,
                doors,
                kit_name,
                missing_files,
                kotor_net_json=kotor_net_json,
            )
        )
    return out


def _parse_kit_tiles(raw_tiles: object, *, kotor_net_json: bool) -> list[KitTileRecord]:
    if not isinstance(raw_tiles, list):
        return []
    tiles: list[KitTileRecord] = []
    for t in raw_tiles:
        if not isinstance(t, dict):
            continue
        try:
            tid = str(t["id"])
            name = str(t.get("name", tid))
            default_floor = str(t["defaultFloorID"])
        except (KeyError, TypeError, ValueError):
            continue
        default_ceiling = ""
        dc = t.get("defaultCeilingID")
        if dc is not None:
            default_ceiling = str(dc)
        wall_hooks: list[WallHookTemplate] = []
        for h in t.get("wallHooks") or []:
            if not isinstance(h, dict):
                continue
            try:
                dw = str(h["defaultWallID"])
            except (KeyError, TypeError, ValueError):
                continue
            pos = _vec3_from_json(h.get("position"))
            orient = _parse_kotor_net_orient(h.get("orientation")) if kotor_net_json else _parse_kotor_net_orient_wxyz(h.get("orientation"))
            wall_hooks.append(WallHookTemplate(default_wall_id=dw, position=pos, orientation=orient))

        def parse_corner_hooks(key: str, id_key: str) -> list[CornerHookTemplate]:
            out: list[CornerHookTemplate] = []
            for h in t.get(key) or []:
                if not isinstance(h, dict):
                    continue
                try:
                    cid = str(h[id_key])
                except (KeyError, TypeError, ValueError):
                    continue
                adj = h.get("adjacencies")
                adj_list: list[int] = []
                if isinstance(adj, list):
                    adj_list = [int(x) for x in adj if isinstance(x, (int, float))]
                pos = _vec3_from_json(h.get("position"))
                orient = _parse_kotor_net_orient(h.get("orientation")) if kotor_net_json else _parse_kotor_net_orient_wxyz(h.get("orientation"))
                out.append(
                    CornerHookTemplate(
                        default_corner_id=cid,
                        adjacent=adj_list,
                        position=pos,
                        orientation=orient,
                    )
                )
            return out

        inner_h = parse_corner_hooks("innerCornerHooks", "defaultInnerCornerID")
        outer_h = parse_corner_hooks("outerCornerHooks", "defaultOuterCornerID")

        tiles.append(
            KitTileRecord(
                tile_id=tid,
                name=name,
                default_floor_id=default_floor,
                default_ceiling_id=default_ceiling,
                wall_hooks=wall_hooks,
                inner_corner_hooks=inner_h,
                outer_corner_hooks=outer_h,
                ceiling_hooks=[],
            )
        )
    return tiles


def _is_v2_tile_kit_dict(raw: dict) -> bool:
    if raw.get("format_version") == 2:
        return True
    fmt = raw.get("format")
    return isinstance(fmt, str) and fmt.strip() == "0.1"


def load_tile_kit_v2(
    path: os.PathLike | str,
    *,
    record_missing: bool = False,
) -> tuple[TileKit, list[MissingFileInfo]]:
    """Load a v2 tile kit JSON (PyKotor `format_version: 2` or Kotor.NET `format: \"0.1\"`)."""
    p = Path(path)
    raw_any = json.loads(BinaryReader.load_file(p))
    if not isinstance(raw_any, dict) or not _is_v2_tile_kit_dict(raw_any):
        msg = "Not a v2 tile kit json (expect format_version 2 or format 0.1)"
        raise ValueError(msg)
    raw = raw_any
    kotor_net_json = raw.get("format_version") != 2

    kit_id = str(raw.get("id") or p.stem)
    name = str(raw.get("name", kit_id))
    base_path = p.parent if p.parent.name == kit_id else p.parent / kit_id
    if not base_path.is_dir():
        base_path = p.parent

    missing: list[MissingFileInfo] = []
    mref: list[MissingFileInfo] | None = missing if record_missing else None
    kit = TileKit(
        name=name,
        kit_id=kit_id,
        formats_serializer=str(raw.get("serializer", "")),
        kotor_net_format_id=str(raw.get("format", "")) if isinstance(raw.get("format"), str) else "",
    )
    _load_doors_tilekit(kit, raw.get("doors", []), base_path, name, mref)
    _load_textures_txi(
        base_path / "textures",
        kit.textures,
        kit.txis,
        name,
        mref,
        "texture",
        use_upper_txi_name=True,
    )
    _load_textures_txi(
        base_path / "lightmaps",
        kit.lightmaps,
        kit.txis,
        name,
        mref,
        "lightmap",
        use_upper_txi_name=False,
    )
    if (base_path / "always").is_dir():
        for f in (base_path / "always").iterdir():
            b = _load_binary(f, kit_name=name, kind="always file", missing_files=mref)
            if b is not None:
                kit.always[f] = b
    _load_skyboxes_tilekit(kit, base_path / "skyboxes", name, mref)
    _load_doorway_padding_tilekit(kit, base_path / "doorway", name, mref)

    if kotor_net_json:
        kit.floors = _load_template_list(
            raw.get("floors"),
            TileTemplateKind.FLOOR,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=True,
        )
        kit.ceilings = _load_template_list(
            raw.get("ceilings"),
            TileTemplateKind.CEILING,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=True,
        )
        kit.walls = _load_template_list(
            raw.get("walls"),
            TileTemplateKind.WALL,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=True,
        )
        kit.doorframes = _load_template_list(
            raw.get("doorframes"),
            TileTemplateKind.DOORFRAME,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=True,
        )
        kit.inner_corners = _load_template_list(
            raw.get("innerCorners"),
            TileTemplateKind.INNER_CORNER,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=True,
        )
        kit.outer_corners = _load_template_list(
            raw.get("outerCorners"),
            TileTemplateKind.OUTER_CORNER,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=True,
        )
        kit.objects = _load_template_list(
            raw.get("objects"),
            TileTemplateKind.OBJECT,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=True,
        )
        kit.tiles = _parse_kit_tiles(raw.get("tiles"), kotor_net_json=True)
    else:
        tpl = raw.get("templates") or {}
        kit.floors = _load_template_list(
            tpl.get("floors"),
            TileTemplateKind.FLOOR,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=False,
        )
        kit.ceilings = _load_template_list(
            tpl.get("ceilings"),
            TileTemplateKind.CEILING,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=False,
        )
        kit.walls = _load_template_list(
            tpl.get("walls"),
            TileTemplateKind.WALL,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=False,
        )
        kit.corners = _load_template_list(
            tpl.get("corners"),
            TileTemplateKind.CORNER,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=False,
        )
        kit.doorframes = _load_template_list(
            tpl.get("doorframes"),
            TileTemplateKind.DOORFRAME,
            base_path,
            kit.doors,
            name,
            mref,
            kotor_net_json=False,
        )
        kit.tiles = _parse_kit_tiles(raw.get("tiles"), kotor_net_json=False)
    return kit, missing
