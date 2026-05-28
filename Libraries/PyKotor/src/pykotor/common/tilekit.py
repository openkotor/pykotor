"""Tile-based indoor kit (format_version 2) data model (Kotor.NET KitSerializer_V0_1 semantics)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path

from pykotor.common.indoorkit import Kit, KitComponentHook, KitDoor, MDLMDXTuple
from pykotor.resource.formats.bwm.bwm_data import BWM
from utility.common.geometry import Vector3


class TileTemplateKind(IntEnum):
    FLOOR = 0
    CEILING = 1
    WALL = 2
    CORNER = 3
    DOORFRAME = 4
    INNER_CORNER = 5
    OUTER_CORNER = 6
    OBJECT = 7


@dataclass
class QuaternionWXYZ:
    """Unit quaternion (w, x, y, z) — JSON array order in v2 spec."""

    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_json(cls, data: list[float] | None) -> QuaternionWXYZ:
        if not data or len(data) < 4:
            return cls()
        return cls(float(data[0]), float(data[1]), float(data[2]), float(data[3]))

    @classmethod
    def from_xyzw_json(cls, data: list[float] | None) -> QuaternionWXYZ:
        """Load Kotor.NET/System.Numerics JSON order: x, y, z, w."""
        if not data or len(data) < 4:
            return cls()
        return cls(w=float(data[3]), x=float(data[0]), y=float(data[1]), z=float(data[2]))

    def to_xyzw_json(self) -> list[float]:
        """Return Kotor.NET/System.Numerics JSON order: x, y, z, w."""
        return [self.x, self.y, self.z, self.w]

    def __mul__(self, other: QuaternionWXYZ) -> QuaternionWXYZ:
        """Compose this rotation with ``other`` using Hamilton product."""
        return QuaternionWXYZ(
            w=self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            x=self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            y=self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            z=self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def rotate_vector(self, v: Vector3) -> Vector3:
        """Rotate *v* by this unit quaternion (Hamilton convention w,x,y,z)."""
        qx, qy, qz = self.x, self.y, self.z
        qw = self.w
        vx, vy, vz = v.x, v.y, v.z
        tx = 2 * (qy * vz - qz * vy)
        ty = 2 * (qz * vx - qx * vz)
        tz = 2 * (qx * vy - qy * vx)
        cx = qy * tz - qz * ty
        cy = qz * tx - qx * tz
        cz = qx * ty - qy * tx
        return Vector3(vx + qw * tx + cx, vy + qw * ty + cy, vz + qw * tz + cz)


@dataclass
class DoorFrameHookTemplate:
    position: Vector3 = field(default_factory=Vector3.from_null)
    orientation: QuaternionWXYZ = field(default_factory=QuaternionWXYZ)


@dataclass
class WallHookTemplate:
    default_wall_id: str
    position: Vector3 = field(default_factory=Vector3.from_null)
    orientation: QuaternionWXYZ = field(default_factory=QuaternionWXYZ)
    adjacent_walls: list[int] = field(default_factory=list)


@dataclass
class CornerHookTemplate:
    default_corner_id: str
    position: Vector3 = field(default_factory=Vector3.from_null)
    orientation: QuaternionWXYZ = field(default_factory=QuaternionWXYZ)
    adjacent: list[int] = field(default_factory=list)


@dataclass
class TileCellTemplate:
    """Kotor.NET tile template: a floor/ceiling plus wall and corner hook layout."""

    template_id: str
    name: str
    default_floor_id: str
    default_ceiling_id: str = ""
    wall_hooks: list[WallHookTemplate] = field(default_factory=list)
    inner_corner_hooks: list[CornerHookTemplate] = field(default_factory=list)
    outer_corner_hooks: list[CornerHookTemplate] = field(default_factory=list)


@dataclass
class TileTemplate:
    kind: TileTemplateKind
    template_id: str
    resref: str
    offset: Vector3 = field(default_factory=Vector3.from_null)
    rotation: QuaternionWXYZ = field(default_factory=QuaternionWXYZ)
    mdl: bytes = b""
    mdx: bytes = b""
    wok: BWM | None = None
    doorhooks: list[KitComponentHook] = field(default_factory=list)
    name: str = ""
    model: str = ""
    doorframe_id: str = ""
    hooks: list[DoorFrameHookTemplate] = field(default_factory=list)

    @property
    def has_walkmesh(self) -> bool:
        return self.wok is not None and bool(self.wok.faces)

    @property
    def can_be_door(self) -> bool:
        return bool(self.doorframe_id)


@dataclass
class TileKit:
    name: str
    kit_id: str
    version: int = 0
    doors: list[KitDoor] = field(default_factory=list)
    tiles: list[TileCellTemplate] = field(default_factory=list)
    floors: list[TileTemplate] = field(default_factory=list)
    ceilings: list[TileTemplate] = field(default_factory=list)
    walls: list[TileTemplate] = field(default_factory=list)
    corners: list[TileTemplate] = field(default_factory=list)
    doorframes: list[TileTemplate] = field(default_factory=list)
    inner_corners: list[TileTemplate] = field(default_factory=list)
    outer_corners: list[TileTemplate] = field(default_factory=list)
    objects: list[TileTemplate] = field(default_factory=list)
    formats_serializer: str = ""
    format_id: str = ""
    textures: dict[str, bytes] = field(default_factory=dict)
    lightmaps: dict[str, bytes] = field(default_factory=dict)
    txis: dict[str, bytes] = field(default_factory=dict)
    always: dict[Path, bytes] = field(default_factory=dict)
    side_padding: dict[int, dict[int, MDLMDXTuple]] = field(default_factory=dict)
    top_padding: dict[int, dict[int, MDLMDXTuple]] = field(default_factory=dict)
    skyboxes: dict[str, MDLMDXTuple] = field(default_factory=dict)

    def all_templates(self) -> list[TileTemplate]:
        return [
            *self.floors,
            *self.ceilings,
            *self.walls,
            *self.corners,
            *self.doorframes,
            *self.inner_corners,
            *self.outer_corners,
            *self.objects,
        ]

    def template_by_id(self, template_id: str) -> TileTemplate | None:
        for t in self.all_templates():
            if t.template_id == template_id:
                return t
        return None

    def as_runtime_kit(self) -> Kit:
        """Shell `Kit` for skybox/texture resolution in `IndoorMap.build` (no room components)."""
        k = Kit(self.name, self.kit_id)
        k.doors.extend(self.doors)
        k.textures.update(self.textures)
        k.lightmaps.update(self.lightmaps)
        k.txis.update(self.txis)
        k.always.update(self.always)
        k.side_padding.update(self.side_padding)
        k.top_padding.update(self.top_padding)
        k.skyboxes.update(self.skyboxes)
        return k
