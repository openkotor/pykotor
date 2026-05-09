"""Kotor.NET AreaDesigner area JSON (`AreaSerializer` / `AreaSerializer_V0_1`).

Mirrors `Kotor.DevelopmentKit.AreaDesigner.relocate.AreaSerialization.AreaSerializer`:
**load** dispatches on `format`; **save** always writes `AreaSerializer_V0_1` (same as .NET).

PyKotor `.indoor` maps may embed the same payload under `IndoorMap.area_designer_v01`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypedDict


class _FloorRefDict(TypedDict):
    kitID: str
    templateID: str


class _WallRefDict(TypedDict):
    kitID: str
    templateID: str


class _TileDict(TypedDict, total=False):
    kitID: str
    templateID: str
    position: list[float]
    orientation: list[float]
    floor: _FloorRefDict
    ceiling: _FloorRefDict
    walls: list[_WallRefDict]


class _RoomDict(TypedDict, total=False):
    position: list[float]
    orientation: list[float]
    tiles: list[_TileDict]


class AreaDesignerFileV01(TypedDict, total=False):
    format: str
    rooms: list[_RoomDict]


FORMAT_ID = "0.1"


def load_area_designer(path: Path | str) -> AreaDesignerFileV01:
    """Load an Area Designer JSON file; dispatch on ``format`` like `AreaSerializer.Load`."""
    p = Path(path)
    raw = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = "Area file must be a JSON object"
        raise ValueError(msg)
    fmt = raw.get("format")
    if fmt != FORMAT_ID:
        msg = f"Unsupported area format {fmt!r} (expected '{FORMAT_ID}')"
        raise ValueError(msg)
    return raw  # type: ignore[return-value]


def save_area_designer(path: Path | str, data: AreaDesignerFileV01) -> None:
    """Write area JSON (`AreaSerializer.Save` → `AreaSerializer_V0_1`)."""
    save_area_designer_v01(path, data)


def load_area_designer_v01(path: Path | str) -> AreaDesignerFileV01:
    """Alias for `load_area_designer` (v0.1 is the only supported on-disk version today)."""
    return load_area_designer(path)


def save_area_designer_v01(path: Path | str, data: AreaDesignerFileV01) -> None:
    """Write an Area Designer JSON file (pretty-printed, UTF-8)."""
    p = Path(path)
    out: dict[str, Any] = dict(data)
    out["format"] = FORMAT_ID
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def empty_area_designer_v01() -> AreaDesignerFileV01:
    """Return an empty area matching a new `Area` in Kotor.NET (`AreaDesignerViewModel.NewArea`)."""
    return {"format": FORMAT_ID, "rooms": []}
