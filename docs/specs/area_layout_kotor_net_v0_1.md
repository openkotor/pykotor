# Area layout format (Kotor.NET `AreaSerializer_V0_1` parity)

PyKotor stores Kotor.NET-style composed tile layouts separately from kit definitions. The layout references template ids from loaded tile kits and can be edited from either the 2D or 3D ModuleDesigner views.

## Top-level object

| Field | Type | Required | Notes |
|------|------|----------|-------|
| `format` | `string` | Yes | `"0.1"`. |
| `rooms` | `array` | Yes | Room instances. |

## Room object

| Field | Type | Required | Notes |
|------|------|----------|-------|
| `position` | `[x, y, z]` | Yes | Room world translation. |
| `orientation` | `[x, y, z, w]` | Yes | Kotor.NET/System.Numerics quaternion order. |
| `tiles` | `array` | Yes | Tile instances local to the room. |
| `objects` | `array` | No | Placed kit objects local to the room. |

## Tile object

| Field | Type | Required | Notes |
|------|------|----------|-------|
| `kitID` | `string` | Yes | Tile kit id. |
| `templateID` | `string` | Yes | Template id in kit `tiles[]`. |
| `position` | `[x, y, z]` | Yes | Tile local translation. |
| `orientation` | `[x, y, z, w]` | Yes | Tile local quaternion. |
| `floor` | `object` | Yes | `{ "kitID": "...", "templateID": "..." }`. |
| `ceiling` | `object` | Yes | Same shape; template may be empty. |
| `walls` | `array` | Yes | Wall template overrides by hook index. |

On load, PyKotor instantiates floor, ceiling, wall, inner-corner, outer-corner, and doorframe children from the referenced kit. `Room.fix_walls()`-style linking hides touching walls when hook world positions match within tolerance.

## Object instance

| Field | Type | Required | Notes |
|------|------|----------|-------|
| `kitID` | `string` | Yes | Tile kit id. |
| `templateID` | `string` | Yes | Template id in kit `objects[]`. |
| `position` | `[x, y, z]` | Yes | Object local translation. |
| `orientation` | `[x, y, z, w]` | Yes | Object local quaternion. |

## Build behavior

`IndoorMap` persists this layout under `area_layout` and `pykotor.tools.tilemap_compile.apply_area_layout_to_map()` compiles it into an embedded build room. `area_layout_to_merged_bwm()` emits playable area walkmesh data from the same layout state used by ModuleDesigner rendering. MDL-only kits receive generated flat floor quads from floor/tile hook bounds.
