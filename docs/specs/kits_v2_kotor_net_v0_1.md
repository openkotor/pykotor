# Indoor kit format v2 (Kotor.NET `KitSerializer_V0_1` semantic parity)

PyKotor `format_version: 2` JSON matches the **on-disk contract** used by Kotor.NET area-designer kit serialization (v0.1). This document is the compatibility reference; it does **not** require checking out or modifying the Kotor.NET `rework-area-designer` branch—copy field names and sample payloads from a read-only clone when drift is suspected.

## Top-level object

| Field | Type | Required | Notes |
|------|------|----------|--------|
| `format_version` | `integer` | Yes | Must be `2` for this spec. |
| `serializer` | `string` | No | e.g. `"Kotor.NET KitSerializer_V0_1"` (metadata only). |
| `name` | `string` | Yes | Human-readable kit name. |
| `id` | `string` | Yes | Directory name under `kits/` (same as v1). |
| `doors` | `array` | No | Same as v1: `utd_k1`, `utd_k2`, `width`, `height`. |
| `templates` | `object` | Yes | Categorized **tile** templates (not prebuilt rooms). |

## `templates` categories

Each category is an array of **template** objects. Templates are small MDL/MDX (and optional WOK) pieces: floors, ceilings, walls, corners, door frames.

| Category key | Role |
|-------------|------|
| `floors` | Walkable horizontal tiles. |
| `ceilings` | Ceiling geometry. |
| `walls` | Wall segments. |
| `corners` | Corner pieces. |
| `doorframes` | Doorway framing. |

## Template object

| Field | Type | Required | Notes |
|------|------|----------|--------|
| `id` | `string` | Yes | Unique within the kit. |
| `resref` | `string` | No | If omitted, `id` is used to resolve `resref.mdl` / `resref.mdx` / optional `resref.wok`. |
| `offset` | `[x, y, z]` | No | Local origin (float), default `[0,0,0]`. |
| `rotation` | `[w, x, y, z]` | No | **Unit quaternion** (float). Default identity `[1, 0, 0, 0]`. |
| `doorhooks` | `array` | No | Optional; same semantics as v1 `doorhooks` on components (`x`,`y`,`z`,`rotation`,`door` index, `edge`). |

On-disk layout under `kits/<id>/`:

- `templates` do **not** require `.wok` (Kotor.NET v0.1 may be MDL-only). PyKotor may **merge** per-piece WOKs when present, or **generate** walkable BWM at build from floor geometry (see implementation).

## v1 vs v2

- **v1** Holocron kits: top-level `components[]` with full room pieces and required `.wok` per component.
- **v2** tile kits: `templates` + `format_version: 2`; aimed at grid-based area design and optional procedural WOK.

## `.indoor` map: `tile_layout` (PyKotor extension)

Optional block on the indoor map JSON (alongside `rooms`):

- `format_version` (int): layout schema version.
- `kit_id`: which v2 `TileKit` the grid references.
- `cell_size`: world units per cell (float or `[sx, sy]`).
- `grid_w`, `grid_h`: integer dimensions.
- `floor_cells`: row-major list of `template_id` or `null` (length `grid_w * grid_h`).

The authoritative build path still produces **WOK/MDL** via `IndoorMap.build()`; `tile_layout` is compiled to placed geometry and merged walkmeshes as implemented in `pykotor.tools.tilemap_compile`.
