# Indoor kit format v2 (Kotor.NET `KitSerializer_V0_1` parity)

PyKotor v2 tile kits now use the same JSON shape as Kotor.NET Area Designer `KitSerializer_V0_1` (`format: "0.1"`). The vendored Kotor.NET checkout is reference-only and must not be modified for PyKotor kit loading.

## Top-level object

| Field | Type | Required | Notes |
|------|------|----------|--------|
| `id` | `string` | Yes | Must match the `.kit` filename stem, matching Kotor.NET validation. |
| `version` | `integer` | Yes | Kit authoring version. |
| `name` | `string` | Yes | Human-readable kit name. |
| `format` | `string` | Yes | Kotor.NET v0.1 uses `"0.1"`. |
| `tiles` | `array` | Yes | Tile blueprints composed from floors, ceilings, wall hooks, and corner hooks. |
| `floors` | `array` | Yes | Floor model templates. |
| `ceilings` | `array` | Yes | Ceiling model templates. |
| `doorframes` | `array` | Yes | Doorframe model templates and door hooks. |
| `walls` | `array` | Yes | Wall model templates, optionally doorframe-capable. |
| `innerCorners` | `array` | Yes | Inner-corner model templates. |
| `outerCorners` | `array` | Yes | Outer-corner model templates. |
| `objects` | `array` | Yes | Object model templates. |

This replaces the earlier provisional PyKotor `format_version: 2` / `templates` grouping. The loader still accepts older checked-in fixtures where needed, but new authored kits should use this Kotor.NET-compatible shape.

## Quaternion Order

Kotor.NET uses `System.Numerics.Quaternion` and serializes `ToFloatArray()` as:

```json
[x, y, z, w]
```

PyKotor converts this at the boundary into its internal `QuaternionWXYZ` model. Do not write `[w, x, y, z]` in Kotor.NET v0.1 kit JSON.

## Tile Objects

Each `tiles[]` entry describes a tile blueprint, not a prebuilt room:

| Field | Type | Required | Notes |
|------|------|----------|--------|
| `id` | `string` | Yes | Tile template id. |
| `name` | `string` | Yes | Display name. |
| `defaultFloorID` | `string` | Yes | Template id in `floors`. |
| `defaultCeilingID` | `string` | No | Template id in `ceilings`; empty is allowed. |
| `wallHooks` | `array` | Yes | Wall hook transforms and default wall ids. |
| `innerCornerHooks` | `array` | Yes | Inner-corner hook transforms and adjacency wall indexes. |
| `outerCornerHooks` | `array` | Yes | Outer-corner hook transforms and adjacency wall indexes. |

Wall hook object:

```json
{
  "defaultWallID": "wall_a",
  "position": [1.0, 0.0, 0.0],
  "orientation": [0.0, 0.0, 0.0, 1.0]
}
```

Corner hook object:

```json
{
  "defaultInnerCornerID": "inner_a",
  "position": [1.0, 1.0, 0.0],
  "orientation": [0.0, 0.0, 0.0, 1.0],
  "adjacencies": [0, 1]
}
```

Use `defaultOuterCornerID` for outer-corner hooks.

## Model Templates

Floor, ceiling, wall, inner corner, outer corner, and object templates share:

| Field | Type | Required |
|------|------|----------|
| `id` | `string` | Yes |
| `name` | `string` | Yes |
| `model` | `string` | Yes |

Wall templates additionally support:

| Field | Type | Notes |
|------|------|-------|
| `doorframeID` | `string` or `null` | Empty or null means the wall is not door-capable. |

Doorframe templates additionally support:

```json
{
  "id": "doorframe_a",
  "name": "Doorframe A",
  "model": "doorframe_a",
  "hooks": [
    {
      "position": [0.0, 0.0, 0.0],
      "orientation": [0.0, 0.0, 0.0, 1.0]
    }
  ]
}
```

## Walkmesh and Build Behavior

Kotor.NET v0.1 kits do not require WOK/BWM assets and Kotor.NET export is MDL-only. PyKotor keeps builds playable by generating area BWM from composed floor tile geometry when per-piece walkmesh data is absent. If per-piece walkmeshes are present, PyKotor can merge them; otherwise it emits flat floor quads from tile hook extents.

## Area Layout

Area placement state is separate from kit serialization. See `docs/specs/area_layout_kotor_net_v0_1.md`.
