"""Headless Kotor.NET-style area layout state for tile-grid module design."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from pykotor.common.tilekit import (
    CornerHookTemplate,
    QuaternionWXYZ,
    TileCellTemplate,
    TileKit,
    TileTemplate,
    TileTemplateKind,
    WallHookTemplate,
)
from utility.common.geometry import Vector3


def _add(a: Vector3, b: Vector3) -> Vector3:
    return Vector3(a.x + b.x, a.y + b.y, a.z + b.z)


def _sub(a: Vector3, b: Vector3) -> Vector3:
    return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)


def _distance(a: Vector3, b: Vector3) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def _template_by_kind(kit: TileKit, template_id: str, kind: TileTemplateKind) -> TileTemplate:
    template = kit.template_by_id(template_id)
    if template is None or template.kind != kind:
        label = kind.name.lower().replace("_", " ")
        raise ValueError(f"Missing {label} template {template_id}")
    return template


def _tile_cell_template(kit: TileKit, template_id: str) -> TileCellTemplate:
    for template in kit.tiles:
        if template.template_id == template_id:
            return template
    raise ValueError(f"Missing tile template {template_id}")


@dataclass
class AreaDoorFrame:
    wall: AreaWall
    template_id: str
    enabled: bool = True

    @property
    def visible(self) -> bool:
        return self.enabled


@dataclass
class AreaWall:
    tile: AreaTile
    template_id: str
    local_position: Vector3
    local_orientation: QuaternionWXYZ
    linked_tile: AreaTile | None = None
    doorframe: AreaDoorFrame | None = None

    @property
    def visible(self) -> bool:
        return self.linked_tile is None

    def switch_template(self, kit: TileKit, template_id: str) -> None:
        template = _template_by_kind(kit, template_id, TileTemplateKind.WALL)
        self.template_id = template.template_id
        self.doorframe = AreaDoorFrame(self, template.doorframe_id) if template.can_be_door else None

    def world_position(self, room: AreaRoom) -> Vector3:
        return room.world_point(self.tile.local_point(self.local_position))


@dataclass
class AreaCorner:
    tile: AreaTile
    template_id: str
    local_position: Vector3
    local_orientation: QuaternionWXYZ
    adjacent_walls: list[int] = field(default_factory=list)
    outer: bool = False

    @property
    def visible(self) -> bool:
        if self.outer:
            return len(self.adjacent_walls) == 2 and all(
                self.tile.walls[index].linked_tile is not None for index in self.adjacent_walls
            )
        return bool(self.adjacent_walls) and all(
            self.tile.walls[index].linked_tile is None for index in self.adjacent_walls
        )

    def world_position(self, room: AreaRoom) -> Vector3:
        return room.world_point(self.tile.local_point(self.local_position))


@dataclass
class AreaObject:
    kit_id: str
    template_id: str
    local_position: Vector3 = field(default_factory=Vector3.from_null)
    local_orientation: QuaternionWXYZ = field(default_factory=QuaternionWXYZ)

    def world_position(self, room: AreaRoom) -> Vector3:
        return room.world_point(self.local_position)


@dataclass
class AreaTile:
    kit_id: str
    template_id: str
    local_position: Vector3 = field(default_factory=Vector3.from_null)
    local_orientation: QuaternionWXYZ = field(default_factory=QuaternionWXYZ)
    floor_template_id: str = ""
    ceiling_template_id: str = ""
    walls: list[AreaWall] = field(default_factory=list)
    inner_corners: list[AreaCorner] = field(default_factory=list)
    outer_corners: list[AreaCorner] = field(default_factory=list)

    def local_point(self, point: Vector3) -> Vector3:
        return _add(self.local_position, self.local_orientation.rotate_vector(point))

    def world_position(self, room: AreaRoom) -> Vector3:
        return room.world_point(self.local_position)


@dataclass
class AreaRoom:
    position: Vector3 = field(default_factory=Vector3.from_null)
    orientation: QuaternionWXYZ = field(default_factory=QuaternionWXYZ)
    tiles: list[AreaTile] = field(default_factory=list)
    objects: list[AreaObject] = field(default_factory=list)

    def world_point(self, point: Vector3) -> Vector3:
        return _add(self.position, self.orientation.rotate_vector(point))

    def add_tile(
        self,
        kit: TileKit,
        template_id: str,
        *,
        position: Vector3 | None = None,
        orientation: QuaternionWXYZ | None = None,
    ) -> AreaTile:
        template = _tile_cell_template(kit, template_id)
        _template_by_kind(kit, template.default_floor_id, TileTemplateKind.FLOOR)
        if template.default_ceiling_id:
            _template_by_kind(kit, template.default_ceiling_id, TileTemplateKind.CEILING)

        tile = AreaTile(
            kit_id=kit.kit_id,
            template_id=template.template_id,
            local_position=position or Vector3.from_null(),
            local_orientation=orientation or QuaternionWXYZ(),
            floor_template_id=template.default_floor_id,
            ceiling_template_id=template.default_ceiling_id,
        )
        tile.walls = [self._wall_from_hook(kit, tile, hook) for hook in template.wall_hooks]
        tile.inner_corners = [
            self._corner_from_hook(kit, tile, hook, TileTemplateKind.INNER_CORNER, outer=False)
            for hook in template.inner_corner_hooks
        ]
        tile.outer_corners = [
            self._corner_from_hook(kit, tile, hook, TileTemplateKind.OUTER_CORNER, outer=True)
            for hook in template.outer_corner_hooks
        ]
        self.tiles.append(tile)
        self.fix_walls()
        return tile

    def extend_tile_from_wall(
        self,
        kit: TileKit,
        tile: AreaTile,
        wall: AreaWall,
        template_id: str,
    ) -> AreaTile:
        template = _tile_cell_template(kit, template_id)
        candidate = self._best_adjacent_wall_hook(template, wall)
        new_orientation = tile.local_orientation
        new_position = _sub(
            _add(tile.local_position, tile.local_orientation.rotate_vector(wall.local_position)),
            new_orientation.rotate_vector(candidate.position),
        )
        return self.add_tile(kit, template_id, position=new_position, orientation=new_orientation)

    def fix_walls(self, *, tolerance: float = 0.01) -> None:
        walls = [wall for tile in self.tiles for wall in tile.walls]
        for wall in walls:
            wall.linked_tile = None

        for index_a, tile_a in enumerate(self.tiles):
            for tile_b in self.tiles[index_a + 1 :]:
                for wall_a in tile_a.walls:
                    for wall_b in tile_b.walls:
                        if _distance(wall_a.world_position(self), wall_b.world_position(self)) < tolerance:
                            wall_a.linked_tile = tile_b
                            wall_b.linked_tile = tile_a

    def add_object(
        self,
        kit: TileKit,
        template_id: str,
        *,
        position: Vector3 | None = None,
        orientation: QuaternionWXYZ | None = None,
    ) -> AreaObject:
        template = _template_by_kind(kit, template_id, TileTemplateKind.OBJECT)
        area_object = AreaObject(
            kit_id=kit.kit_id,
            template_id=template.template_id,
            local_position=position or Vector3.from_null(),
            local_orientation=orientation or QuaternionWXYZ(),
        )
        self.objects.append(area_object)
        return area_object

    def _wall_from_hook(self, kit: TileKit, tile: AreaTile, hook: WallHookTemplate) -> AreaWall:
        template = _template_by_kind(kit, hook.default_wall_id, TileTemplateKind.WALL)
        wall = AreaWall(tile, template.template_id, hook.position, hook.orientation)
        wall.switch_template(kit, template.template_id)
        return wall

    def _corner_from_hook(
        self,
        kit: TileKit,
        tile: AreaTile,
        hook: CornerHookTemplate,
        kind: TileTemplateKind,
        *,
        outer: bool,
    ) -> AreaCorner:
        template = _template_by_kind(kit, hook.default_corner_id, kind)
        return AreaCorner(
            tile=tile,
            template_id=template.template_id,
            local_position=hook.position,
            local_orientation=hook.orientation,
            adjacent_walls=list(hook.adjacent),
            outer=outer,
        )

    def _best_adjacent_wall_hook(self, template: TileCellTemplate, wall: AreaWall) -> WallHookTemplate:
        candidates = [hook for hook in template.wall_hooks if hook.default_wall_id == wall.template_id]
        if not candidates:
            raise ValueError(f"Tile template {template.template_id} has no wall hook for {wall.template_id}")
        return min(candidates, key=lambda hook: _distance(_add(hook.position, wall.local_position), Vector3.from_null()))


@dataclass
class AreaLayout:
    rooms: list[AreaRoom] = field(default_factory=list)

    def add_room_from_tile(
        self,
        kit: TileKit,
        template_id: str,
        *,
        position: Vector3 | None = None,
        orientation: QuaternionWXYZ | None = None,
    ) -> AreaRoom:
        room = AreaRoom(position=position or Vector3.from_null(), orientation=orientation or QuaternionWXYZ())
        room.add_tile(kit, template_id)
        self.rooms.append(room)
        return room

    def to_dict(self) -> dict:
        from pykotor.tools.area_layout_io import area_layout_to_dict

        return area_layout_to_dict(self)
