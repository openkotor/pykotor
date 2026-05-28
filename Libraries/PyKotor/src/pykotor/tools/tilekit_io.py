"""Load indoor kit format_version 2 (tile templates, Kotor.NET KitSerializer_V0_1 semantics)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from pykotor.common.stream import BinaryReader
from pykotor.common.tilekit import (
    CornerHookTemplate,
    DoorFrameHookTemplate,
    QuaternionWXYZ,
    TileCellTemplate,
    TileKit,
    TileTemplate,
    TileTemplateKind,
    WallHookTemplate,
)
from pykotor.resource.formats.bwm import read_bwm
from pykotor.resource.generics.utd import read_utd

from pykotor.common.indoorkit import KitComponentHook, KitDoor

from utility.common.geometry import Vector3

if TYPE_CHECKING:
    import os

    MissingFileInfo = tuple[str, Path, str]


def _optional_binary(path: Path, *, kit_name: str, kind: str, missing: list[MissingFileInfo] | None) -> bytes:
    if missing is not None and not path.is_file():
        return b""
    try:
        return BinaryReader.load_file(path)
    except FileNotFoundError:
        if missing is not None:
            missing.append((kit_name, path, kind))
        return b""


def _optional_wok(path: Path, *, kit_name: str, missing: list[MissingFileInfo] | None):
    if not path.is_file():
        return None
    try:
        return read_bwm(path)
    except Exception:
        if missing is not None:
            missing.append((kit_name, path, "tile walkmesh"))
        return None


def _vector3_from_json(data: list[float] | tuple[float, ...] | None) -> Vector3:
    if not data or len(data) < 3:
        return Vector3.from_null()
    return Vector3(float(data[0]), float(data[1]), float(data[2]))


def _model_resref(model: str, fallback: str) -> str:
    if not model:
        return fallback
    path = Path(model)
    return path.with_suffix("").as_posix()


def _template_from_kotor_net_json(
    data: dict,
    *,
    kind: TileTemplateKind,
    base_path: Path,
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
) -> TileTemplate | None:
    template_id = str(data.get("id") or "")
    if not template_id:
        return None
    name = str(data.get("name") or template_id)
    model = str(data.get("model") or template_id)
    resref = _model_resref(model, template_id)
    mdl = _optional_binary(base_path / f"{resref}.mdl", kit_name=kit_name, kind="tile mdl", missing=missing_files)
    mdx = _optional_binary(base_path / f"{resref}.mdx", kit_name=kit_name, kind="tile mdx", missing=missing_files)
    wok = _optional_wok(base_path / f"{resref}.wok", kit_name=kit_name, missing=missing_files)

    hooks = [
        DoorFrameHookTemplate(
            position=_vector3_from_json(hook.get("position")),
            orientation=QuaternionWXYZ.from_xyzw_json(hook.get("orientation")),
        )
        for hook in data.get("hooks", []) or []
        if isinstance(hook, dict)
    ]
    return TileTemplate(
        kind=kind,
        template_id=template_id,
        resref=resref,
        mdl=mdl,
        mdx=mdx,
        wok=wok,
        name=name,
        model=model,
        doorframe_id=str(data.get("doorframeID") or ""),
        hooks=hooks,
    )


def _parse_wall_hooks(data: list[dict]) -> list[WallHookTemplate]:
    hooks: list[WallHookTemplate] = []
    for hook in data or []:
        if not isinstance(hook, dict):
            continue
        default_wall_id = str(hook.get("defaultWallID") or "")
        if not default_wall_id:
            continue
        hooks.append(
            WallHookTemplate(
                default_wall_id=default_wall_id,
                position=_vector3_from_json(hook.get("position")),
                orientation=QuaternionWXYZ.from_xyzw_json(hook.get("orientation")),
                adjacent_walls=[int(value) for value in hook.get("adjacencies", []) or []],
            )
        )
    return hooks


def _parse_corner_hooks(data: list[dict], *, id_key: str) -> list[CornerHookTemplate]:
    hooks: list[CornerHookTemplate] = []
    for hook in data or []:
        if not isinstance(hook, dict):
            continue
        default_corner_id = str(hook.get(id_key) or "")
        if not default_corner_id:
            continue
        hooks.append(
            CornerHookTemplate(
                default_corner_id=default_corner_id,
                position=_vector3_from_json(hook.get("position")),
                orientation=QuaternionWXYZ.from_xyzw_json(hook.get("orientation")),
                adjacent=[int(value) for value in hook.get("adjacencies", []) or []],
            )
        )
    return hooks


def load_kotor_net_kit_v0_1_from_dict(
    kit_json: dict,
    *,
    base_path: Path,
    kit_name: str,
    missing_files: list[MissingFileInfo] | None = None,
) -> TileKit:
    kit_id = str(kit_json["id"])
    tk = TileKit(
        name=str(kit_json["name"]),
        kit_id=kit_id,
        version=int(kit_json.get("version") or 0),
        formats_serializer="Kotor.NET KitSerializer_V0_1",
        format_id=str(kit_json.get("format") or "0.1"),
    )

    for tile_json in kit_json.get("tiles", []) or []:
        if not isinstance(tile_json, dict):
            continue
        template_id = str(tile_json.get("id") or "")
        if not template_id:
            continue
        tk.tiles.append(
            TileCellTemplate(
                template_id=template_id,
                name=str(tile_json.get("name") or template_id),
                default_floor_id=str(tile_json.get("defaultFloorID") or ""),
                default_ceiling_id=str(tile_json.get("defaultCeilingID") or ""),
                wall_hooks=_parse_wall_hooks(tile_json.get("wallHooks", []) or []),
                inner_corner_hooks=_parse_corner_hooks(
                    tile_json.get("innerCornerHooks", []) or [],
                    id_key="defaultInnerCornerID",
                ),
                outer_corner_hooks=_parse_corner_hooks(
                    tile_json.get("outerCornerHooks", []) or [],
                    id_key="defaultOuterCornerID",
                ),
            )
        )

    template_groups: list[tuple[str, TileTemplateKind, list[TileTemplate]]] = [
        ("floors", TileTemplateKind.FLOOR, tk.floors),
        ("ceilings", TileTemplateKind.CEILING, tk.ceilings),
        ("walls", TileTemplateKind.WALL, tk.walls),
        ("doorframes", TileTemplateKind.DOORFRAME, tk.doorframes),
        ("innerCorners", TileTemplateKind.INNER_CORNER, tk.inner_corners),
        ("outerCorners", TileTemplateKind.OUTER_CORNER, tk.outer_corners),
        ("objects", TileTemplateKind.OBJECT, tk.objects),
    ]
    for key, kind, target in template_groups:
        for item_json in kit_json.get(key, []) or []:
            if not isinstance(item_json, dict):
                continue
            template = _template_from_kotor_net_json(
                item_json,
                kind=kind,
                base_path=base_path,
                kit_name=kit_name,
                missing_files=missing_files,
            )
            if template is not None:
                target.append(template)

    return tk


def _parse_hooks(
    kit: TileKit,
    hook_jsons: list[dict],
) -> list[KitComponentHook]:
    hooks: list[KitComponentHook] = []
    for hook_json in hook_jsons:
        try:
            position = Vector3(hook_json["x"], hook_json["y"], hook_json["z"])
            rotation = float(hook_json["rotation"])
            door = kit.doors[int(hook_json["door"])]
            edge = int(hook_json["edge"])
        except Exception:
            continue
        hooks.append(KitComponentHook(position, rotation, edge, door))
    return hooks


def load_tile_kit_v2_from_dict(
    kit_json: dict,
    *,
    base_path: Path,
    kit_name: str,
    missing_files: list[MissingFileInfo] | None = None,
) -> TileKit | None:
    if str(kit_json.get("format") or "") == "0.1" and "tiles" in kit_json:
        return load_kotor_net_kit_v0_1_from_dict(
            kit_json,
            base_path=base_path,
            kit_name=kit_name,
            missing_files=missing_files,
        )

    fmt = kit_json.get("format_version")
    if fmt != 2:
        return None

    kit_id = str(kit_json.get("id") or base_path.name)
    tk = TileKit(
        name=str(kit_json["name"]),
        kit_id=kit_id,
        formats_serializer=str(kit_json.get("serializer") or ""),
    )

    for door_json in kit_json.get("doors", []):
        utd_k1_path = base_path / f"{door_json['utd_k1']}.utd"
        utd_k2_path = base_path / f"{door_json['utd_k2']}.utd"
        try:
            utd_k1 = read_utd(utd_k1_path)
            utd_k2 = read_utd(utd_k2_path)
        except FileNotFoundError as e:
            if missing_files is not None:
                missing_files.append((kit_name, Path(e.filename or ""), "door utd"))
                continue
            raise
        tk.doors.append(KitDoor(utd_k1, utd_k2, door_json["width"], door_json["height"]))

    tpl_groups: list[tuple[str, TileTemplateKind]] = [
        ("floors", TileTemplateKind.FLOOR),
        ("ceilings", TileTemplateKind.CEILING),
        ("walls", TileTemplateKind.WALL),
        ("corners", TileTemplateKind.CORNER),
        ("doorframes", TileTemplateKind.DOORFRAME),
    ]

    templates_root = kit_json.get("templates") or {}
    if not isinstance(templates_root, dict):
        return tk

    for key, kind in tpl_groups:
        for tpl_json in templates_root.get(key, []) or []:
            if not isinstance(tpl_json, dict):
                continue
            tid = str(tpl_json.get("id") or "")
            if not tid:
                continue
            resref = str(tpl_json.get("resref") or tid)
            off = tpl_json.get("offset") or [0.0, 0.0, 0.0]
            offset = Vector3(float(off[0]), float(off[1]), float(off[2]))
            rot = QuaternionWXYZ.from_json(tpl_json.get("rotation"))

            mdl_path = base_path / f"{resref}.mdl"
            mdx_path = base_path / f"{resref}.mdx"
            wok_path = base_path / f"{resref}.wok"

            mdl = _optional_binary(mdl_path, kit_name=kit_name, kind="tile mdl", missing=missing_files)
            mdx = _optional_binary(mdx_path, kit_name=kit_name, kind="tile mdx", missing=missing_files)
            wok = _optional_wok(wok_path, kit_name=kit_name, missing=missing_files)

            tt = TileTemplate(
                kind=kind,
                template_id=tid,
                resref=resref,
                offset=offset,
                rotation=rot,
                mdl=mdl,
                mdx=mdx,
                wok=wok,
                doorhooks=_parse_hooks(tk, tpl_json.get("doorhooks", []) or []),
            )

            if kind == TileTemplateKind.FLOOR:
                tk.floors.append(tt)
            elif kind == TileTemplateKind.CEILING:
                tk.ceilings.append(tt)
            elif kind == TileTemplateKind.WALL:
                tk.walls.append(tt)
            elif kind == TileTemplateKind.CORNER:
                tk.corners.append(tt)
            else:
                tk.doorframes.append(tt)

    return tk


def load_tile_kit_v2_json_file(
    json_path: Path,
    *,
    missing_files: list[MissingFileInfo] | None = None,
) -> TileKit | None:
    raw = BinaryReader.load_file(json_path)
    kit_json = json.loads(raw)
    if not isinstance(kit_json, dict):
        return None
    kit_id = str(kit_json.get("id") or json_path.stem)
    if str(kit_json.get("format") or "") == "0.1" and kit_id != json_path.stem:
        msg = f"Kit ID {kit_id} does not match filename {json_path.name}."
        raise ValueError(msg)
    base_path = json_path.parent / kit_id
    kit_name = str(kit_json.get("name") or kit_id)
    return load_tile_kit_v2_from_dict(
        kit_json, base_path=base_path, kit_name=kit_name, missing_files=missing_files
    )


def load_tile_kits_v2_from_folder(
    path: os.PathLike | str,
    *,
    missing_files: list[MissingFileInfo] | None = None,
) -> list[TileKit]:
    kits_path = Path(path).absolute()
    out: list[TileKit] = []
    if not kits_path.is_dir():
        return out
    for file in sorted(f for f in kits_path.iterdir() if f.suffix.lower() in {".json", ".kit"}):
        tk = load_tile_kit_v2_json_file(file, missing_files=missing_files)
        if tk is not None:
            out.append(tk)
    return out


def _vector3_to_json(value: Vector3) -> list[float]:
    return [value.x, value.y, value.z]


def _template_to_kotor_net_json(template: TileTemplate) -> dict:
    data = {
        "id": template.template_id,
        "name": template.name or template.template_id,
        "model": template.model or template.resref,
    }
    if template.kind == TileTemplateKind.WALL:
        data["doorframeID"] = template.doorframe_id
    if template.kind == TileTemplateKind.DOORFRAME:
        data["hooks"] = [
            {
                "position": _vector3_to_json(hook.position),
                "orientation": hook.orientation.to_xyzw_json(),
            }
            for hook in template.hooks
        ]
    return data


def tile_kit_v2_to_kotor_net_dict(tile_kit: TileKit) -> dict:
    """Serialize the headless kit model using Kotor.NET KitSerializer_V0_1 keys."""

    return {
        "id": tile_kit.kit_id,
        "version": tile_kit.version,
        "name": tile_kit.name,
        "format": tile_kit.format_id or "0.1",
        "tiles": [
            {
                "id": tile.template_id,
                "name": tile.name or tile.template_id,
                "defaultFloorID": tile.default_floor_id,
                "defaultCeilingID": tile.default_ceiling_id,
                "wallHooks": [
                    {
                        "defaultWallID": hook.default_wall_id,
                        "position": _vector3_to_json(hook.position),
                        "orientation": hook.orientation.to_xyzw_json(),
                    }
                    for hook in tile.wall_hooks
                ],
                "innerCornerHooks": [
                    {
                        "defaultInnerCornerID": hook.default_corner_id,
                        "position": _vector3_to_json(hook.position),
                        "orientation": hook.orientation.to_xyzw_json(),
                        "adjacencies": hook.adjacent,
                    }
                    for hook in tile.inner_corner_hooks
                ],
                "outerCornerHooks": [
                    {
                        "defaultOuterCornerID": hook.default_corner_id,
                        "position": _vector3_to_json(hook.position),
                        "orientation": hook.orientation.to_xyzw_json(),
                        "adjacencies": hook.adjacent,
                    }
                    for hook in tile.outer_corner_hooks
                ],
            }
            for tile in tile_kit.tiles
        ],
        "floors": [_template_to_kotor_net_json(template) for template in tile_kit.floors],
        "ceilings": [_template_to_kotor_net_json(template) for template in tile_kit.ceilings],
        "doorframes": [_template_to_kotor_net_json(template) for template in tile_kit.doorframes],
        "walls": [_template_to_kotor_net_json(template) for template in tile_kit.walls],
        "innerCorners": [_template_to_kotor_net_json(template) for template in tile_kit.inner_corners],
        "outerCorners": [_template_to_kotor_net_json(template) for template in tile_kit.outer_corners],
        "objects": [_template_to_kotor_net_json(template) for template in tile_kit.objects],
    }
