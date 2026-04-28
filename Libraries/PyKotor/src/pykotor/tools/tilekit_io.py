"""Load format_version 2 tile kits (Kotor.NET KitSerializer_V0_1 semantics) from disk."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING

from pykotor.common.indoorkit import KitComponentHook, KitDoor
from pykotor.common.stream import BinaryReader
from pykotor.common.tilekit import QuaternionWXYZ, TileKit, TileTemplate, TileTemplateKind
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
        except Exception:
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
        except Exception:
            continue
    return hooks


def _load_template_entry(
    data: dict,
    kind: TileTemplateKind,
    resref: str,
    base_path: Path,
    doors: list[KitDoor],
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
) -> TileTemplate:
    offset_l = data.get("offset", [0.0, 0.0, 0.0])
    if len(offset_l) < 3:
        offset_l = [0.0, 0.0, 0.0]
    offset = Vector3(float(offset_l[0]), float(offset_l[1]), float(offset_l[2]))
    quat = QuaternionWXYZ.from_json(data.get("rotation"))
    wok_path = base_path / f"{resref}.wok"
    mdl_path = base_path / f"{resref}.mdl"
    mdx_path = base_path / f"{resref}.mdx"
    wok: BWM | None = None
    # v2 templates may ship MDL-only (Kotor.NET); do not treat missing WOK/MDL/MDX as errors.
    wok_bytes = _load_binary(wok_path, kit_name=kit_name, kind="walkmesh", missing_files=None)
    if wok_bytes:
        wok = read_bwm(wok_bytes)
    mdl = _load_binary(mdl_path, kit_name=kit_name, kind="model", missing_files=None) or b""
    mdx = _load_binary(mdx_path, kit_name=kit_name, kind="mdx", missing_files=None) or b""
    th = _parse_doorhooks(data.get("doorhooks", []), doors)
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
    )


def _load_template_list(
    items: list[dict] | None,
    kind: TileTemplateKind,
    base_path: Path,
    doors: list[KitDoor],
    kit_name: str,
    missing_files: list[MissingFileInfo] | None,
) -> list[TileTemplate]:
    if not items:
        return []
    out: list[TileTemplate] = []
    for data in items:
        if not isinstance(data, dict):
            continue
        resref = str(data.get("resref") or data.get("id") or "")
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
            )
        )
    return out


def load_tile_kit_v2(
    path: os.PathLike | str,
    *,
    record_missing: bool = False,
) -> tuple[TileKit, list[MissingFileInfo]]:
    """Load a single v2 `tile_kit.json` file (or kit root json inside kits dir)."""
    p = Path(path)
    raw = json.loads(BinaryReader.load_file(p))
    if not isinstance(raw, dict) or raw.get("format_version") != 2:
        msg = "Not a v2 tile kit json"
        raise ValueError(msg)
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

    tpl = raw.get("templates") or {}
    kit.floors = _load_template_list(
        tpl.get("floors"),
        TileTemplateKind.FLOOR,
        base_path,
        kit.doors,
        name,
        mref,
    )
    kit.ceilings = _load_template_list(
        tpl.get("ceilings"),
        TileTemplateKind.CEILING,
        base_path,
        kit.doors,
        name,
        mref,
    )
    kit.walls = _load_template_list(
        tpl.get("walls"),
        TileTemplateKind.WALL,
        base_path,
        kit.doors,
        name,
        mref,
    )
    kit.corners = _load_template_list(
        tpl.get("corners"),
        TileTemplateKind.CORNER,
        base_path,
        kit.doors,
        name,
        mref,
    )
    kit.doorframes = _load_template_list(
        tpl.get("doorframes"),
        TileTemplateKind.DOORFRAME,
        base_path,
        kit.doors,
        name,
        mref,
    )
    return kit, missing
