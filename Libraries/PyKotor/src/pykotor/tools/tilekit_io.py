"""Load indoor kit format_version 2 (tile templates, Kotor.NET KitSerializer_V0_1 semantics)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from pykotor.common.stream import BinaryReader
from pykotor.common.tilekit import QuaternionWXYZ, TileKit, TileTemplate, TileTemplateKind
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
    for file in sorted(f for f in kits_path.iterdir() if f.suffix.lower() == ".json"):
        tk = load_tile_kit_v2_json_file(file, missing_files=missing_files)
        if tk is not None:
            out.append(tk)
    return out
