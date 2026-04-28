# Indoor kit format v2 (Kotor.NET `KitSerializer_V0_1` semantic parity)

PyKotor accepts **two JSON shapes** that deserialize to the same `TileKit` model:

1. **PyKotor envelope:** `format_version: 2` with a nested `templates { ... }` object (Holocron extension for grouped categories + optional `offset` / `rotation` per template).
2. **Kotor.NET on-disk:** top-level `format: "0.1"` (constant `KitSerializer_V0_1.FormatID`), integer `version`, and **parallel arrays** `floors`, `ceilings`, `walls`, `doorframes`, `innerCorners`, `outerCorners`, `objects`, plus **`tiles`** for composable cell definitions.

This document is the compatibility reference; it does **not** require checking out or modifying the Kotor.NET `rework-area-designer` branch.

## Top-level object (Kotor.NET `0.1`)

| Field | Type | Required | Notes |
|------|------|----------|--------|
| `format` | `string` | Yes | Must be `"0.1"`. |
| `version` | `integer` | Yes | Kit revision (C# `Kit.Version`). |
| `name` | `string` | Yes | Human-readable kit name. |
| `id` | `string` | Yes | Must match the JSON filename stem (same rule as Kotor.NET). |
| `doors` | `array` | No | Same as v1 Holocron: `utd_k1`, `utd_k2`, `width`, `height`. |
| `tiles` | `array` | No | Floor-cell blueprints (`defaultFloorID`, wall/corner hooks). |
| `floors`, `ceilings`, `walls`, `doorframes`, `innerCorners`, `outerCorners`, `objects` | `array` | Yes\* | \*May be empty arrays. |

## Template entries (`floors` / …)

Each entry: `id`, `name`, **`model`** (MDL resref). PyKotor resolves `model.mdl` / `model.mdx` / optional `model.wok` under `kits/<id>/`.

## PyKotor envelope (`format_version: 2`)

| Field | Type | Required | Notes |
|------|------|----------|--------|
| `format_version` | `integer` | Yes | Must be `2`. |
| `serializer` | `string` | No | e.g. `"Kotor.NET KitSerializer_V0_1"`. |
| `templates` | `object` | Yes | `floors`, `ceilings`, `walls`, `corners`, `doorframes` (legacy single `corners` bucket). |

Template objects may use `resref` **or** `id` for disk assets; optional `offset`, `rotation`.

## Quaternions

- **Kotor.NET JSON** saves `System.Numerics.Quaternion` via `ToFloatArray()` → **`[x, y, z, w]`** on hooks.
- **PyKotor `TileTemplate.rotation`** and internal `QuaternionWXYZ` use **`(w, x, y, z)`**. Use `QuaternionWXYZ.from_kotor_net_float_array` when ingesting .NET hook arrays; use `from_json_wxyz` for PyKotor `rotation: [w,x,y,z]` on templates.

## `tiles[]` (composable cells)

Each tile: `id`, `name`, `defaultFloorID`, optional `defaultCeilingID`, `wallHooks`, `innerCornerHooks`, `outerCornerHooks` (Kotor.NET also has `CeilingHooks` in memory; serializer currently writes `ceilingHooks: []`).

Hook entries include `position: [x,y,z]` and `orientation` as **`[x,y,z,w]`** from .NET.

## `.indoor` map: `tile_layout` (PyKotor extension)

Optional block alongside `rooms`:

- `kit_id`, `cell_size`, `grid_w`, `grid_h`, `floor_cells` (row-major template ids).

Build still produces **WOK/MDL** via `IndoorMap.build()`; floor walkmesh merging uses `pykotor.tools.tilemap_compile`.

## 3D preview (PyKotor GL)

Kotor.NET: `GLEngine.Render` → clear → `GeometryRenderer` (shader + mesh descriptors). PyKotor: `pykotor.gl.scene.Scene.render()` with `RenderObject` instances. For kit grids, `pykotor.tools.tilekit_preview` uploads kit TGAs / registers MDL bytes on a `Scene`, places floor `RenderObject`s for each grid cell, then the Toolset calls `scene.render()` from `QOpenGLWidget.paintGL`.
