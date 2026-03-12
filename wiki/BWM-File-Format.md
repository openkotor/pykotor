# KotOR BWM File Format Documentation

This document describes the BWM (Binary WalkMesh) file format used by the **Odyssey engine** (Knights of the Old Republic and The Sith Lords). The format is used for pathfinding, collision, and area transitions. Content is based on reverse-engineered engine behavior and community tooling (KOTORMax, kotorblender, Kaurora); no in-repo implementation is cited as authoritative.

**Related formats:** BWM files are used with [GFF ARE](GFF-ARE) (area properties, walkmesh references), [LYT](LYT-File-Format) (room positions; **room order in LYT = transition ID** for perimeter edges), [VIS](VIS-File-Format) (visibility), [surfacemat.2da](2DA-surfacemat) (material IDs and walkability), and [MDL/MDX](MDL-MDX-File-Format) (room geometry; embedded AABB/walkmesh data for camera collision).

This document does **not** cite or rely on any in-repo implementation. It is based on reverse-engineered engine behavior, community tooling (KOTORMax, kotorblender, Kaurora), and the Aurora/NWN lineage. Terms are defined below; industry-standard and engine-lineage context is given so the *how* and *why* of the format are clear.

---

## Table of Contents

- [What is a BWM File?](#what-is-a-bwm-file)
- [Glossary and terminology](#glossary-and-terminology)
- [Client–server architecture and dual walkmesh sources](#client%e2%80%93server-architecture-and-dual-walkmesh-sources)
- [Why the format is structured this way](#why-the-format-is-structured-this-way)
- [Relationship to MDL and resource resolution](#relationship-to-mdl-and-resource-resolution)
- [Data Types and Conventions](#data-types-and-conventions)
- [File Structure Overview](#file-structure-overview)
- [Binary Format](#binary-format)
  - [File Header](#file-header)
  - [Vertices](#vertices)
  - [Faces](#faces)
  - [Materials, Normals, Distances](#materials-normals-distances)
  - [AABB Tree](#aabb-tree)
  - [Walkable Adjacencies](#walkable-adjacencies)
  - [Edges](#edges)
  - [Perimeters](#perimeters)
- [WOK vs PWK vs DWK](#wok-vs-pwk-vs-dwk)
- [Transitions and Door Placement](#transitions-and-door-placement)
- [Related Formats and Engine Behavior](#related-formats-and-engine-behavior)
- [Authoring and Tooling](#authoring-and-tooling)
- [See also](#see-also)

---

## What is a BWM File?

A BWM file stores **walkmesh** data: a simplified triangle mesh that defines where characters can walk, where they cannot, and surface height. The Odyssey engine uses it for:

- **Pathfinding** -- Adjacency data lets the engine find routes between walkable faces (e.g. A* and funnel algorithms; see xoreos pathfinding wiki).
- **Collision** -- Prevents characters from passing through walls or non-walkable terrain.
- **Spatial queries** -- AABB tree for ray casting (clicks, projectiles) and point-in-triangle tests.
- **Area transitions** -- Perimeter edges carry a **transition ID** (the 0-based index of the adjacent room in the area’s room list from the [LYT](LYT-File-Format)); crossing such an edge moves the player to that room.

**BWM types:**

| Type | Extension | Use | Coordinates | Pathfinding | AABB tree |
|------|-----------|-----|-------------|-------------|-----------|
| **WOK** | .wok | Area/room walkmesh | World | Yes | Yes |
| **PWK** | .pwk | Placeable | Local | Collision-only | Typically no |
| **DWK** | .dwk | Door (closed/open1/open2) | Local | Collision-only | Typically no |

Area rooms have **two** walkmesh-related sources: (1) the **standalone WOK** -- pathfinding, room transitions, adjacency, perimeters; (2) **AABB/walkmesh data in the room MDL** -- used for camera collision. Both should be consistent. WOK is the primary source for pathfinding and room-to-room transitions; the MDL-embedded data is required for correct camera collision (reverse-engineered engine and community sources). The reason for this split is rooted in the engine’s client–server lineage; see [Client–server architecture and dual walkmesh sources](#client%e2%80%93server-architecture-and-dual-walkmesh-sources).

---

## Glossary and terminology

The following terms are used throughout this document and in community tooling. Where relevant, the closest **industry or game-engine equivalent** is noted so the Odyssey behavior can be related to broader practice.

- **Walkmesh** — A simplified 2.5D triangle mesh that defines where characters can walk, surface height, and boundaries. In game-engine literature this is often called a **navigation mesh** (navmesh) or **walkable surface mesh**. The Odyssey engine uses it for pathfinding, collision, and area transitions. *Source: reverse-engineered engine; see also xoreos pathfinding wiki, NWN/Aurora documentation.*

- **BWM (Binary WalkMesh)** — The on-disk format for walkmesh data: a single file (e.g. `.wok`, `.pwk`, `.dwk`) with a 136-byte header and tables for vertices, faces, materials, AABB tree, adjacencies, edges, and perimeters. No version other than `V1.0` is used by the Odyssey engine.

- **AABB (Axis-Aligned Bounding Box)** — A box whose edges are aligned with the world X, Y, Z axes, defined by a minimum and maximum corner (two vectors). In real-time rendering and collision, AABBs are used for fast overlap and ray tests. The Odyssey engine stores an **AABB tree** (binary spatial tree of AABB nodes) inside the BWM and inside the room MDL; the tree is used for ray casting (e.g. mouse picks, projectiles) and point-in-mesh queries. *Industry context: AABB trees are standard in real-time collision and culling; see e.g. Ericson, "Real-Time Collision Detection"; Akenine-Möller et al., "Real-Time Rendering."*

- **AABB tree (in BWM)** — A binary tree of 44-byte nodes stored at `aabb_offset`. Each node has min/max bounds, left/right child indices (0-based, or -1 for none), and a "most significant plane" field used for traversal order. The root index is in the header at `aabb_root`. The engine traverses this tree for ray-vs-mesh and point-in-triangle tests. The tree is **not** a separate file; it is part of the BWM binary. *Source: reverse-engineered engine (vendor/swkotor.c, vendor/swkotor.h).*

- **Adjacency (walkable)** — For each walkable triangle face, the engine stores which neighboring face (if any) shares each of the three edges. Stored as a flat array: `adjacency[face_index * 3 + edge_index]` = `adjacent_face_index * 3 + adjacent_edge_index`, or -1 if the edge is on the boundary. This is the standard **edge-adjacency** structure used in pathfinding (e.g. A* on a triangle graph). *Industry context: Navmesh pathfinding (e.g. "AI for Games" by Millington) uses face adjacency; Odyssey encodes it explicitly for the pathfinder.*

- **Perimeter** — A closed loop of boundary edges of the walkmesh—edges that have no adjacent walkable face. Stored as 1-based loop-end indices: e.g. first loop is edges 0..N-1, second is N..M-1. Perimeters define the outline of the walkable region and, for room WOKs, which edges are **transition edges** (crossing moves the player to another room).

- **Transition ID** — A 0-based index written on a perimeter edge in the edge table. It identifies the **adjacent room** in the area’s room list (the order of rooms in the [LYT](LYT-File-Format)). When the player crosses that edge, the engine uses the transition ID to switch the active room. Thus transition ID = LYT room index for the room being entered.

- **Roomlink** — Community term for the assignment of transition IDs to perimeter edges so that both sides of a seam between two rooms point to the correct room. "Reassigning roomlinks" means updating the edge table so that the boundary between room A and room B has the correct transition ID on each side. Done in layout-aware tools (e.g. KOTORMax Room Linker), not by hand-editing mesh alone.

- **surfacemat.2da** — A [2DA](2DA-File-Format) table that defines surface types by row index. The walkmesh stores a **material index** per face; at runtime the engine looks up that row in surfacemat.2da to determine walkability, line-of-sight blocking, footstep sounds, etc. So walkability is **data-driven**, not hardcoded in the BWM. *Source: reverse-engineered engine (e.g. C2DA__GetINTEntry on surfacemat "Walk" column).*

- **world_coords** — A header field at offset 0x08. `0` = vertices are in **local** (object) space; the engine will transform them by the object’s matrix (used for PWK/DWK). `1` = vertices are already in **world** space (used for WOK). For area room WOKs, build pipelines must output world-space vertices and set `world_coords = 1` after applying the room’s LYT position.

- **WOK / PWK / DWK** — File extensions for the same BWM format used in different roles: **WOK** = area/room walkmesh (world space, pathfinding, transitions); **PWK** = placeable walkmesh (local space, collision); **DWK** = door walkmesh (local space, often three states: closed, open1, open2). The engine distinguishes usage by context (area vs placeable vs door), not by a type byte inside the file; the main distinction in the file is `world_coords`.

- **Resref** — Resource reference: the short name (e.g. `m01aa_room0`) used to look up a file in the game’s resource system. The area GFF (ARE) references room walkmeshes by resref (e.g. `m01aa_room0` → `m01aa_room0.wok`). Resolution order is the same as for other resources (KEY, BIF, override, etc.); see [KEY-File-Format](KEY-File-Format). The BWM file is **not** referenced by byte offset or file index from another format; it is loaded as a separate resource by name.

---

## Client–server architecture and dual walkmesh sources

The Odyssey engine (KotOR 1 and 2) is derived from the **Aurora engine**, which in turn inherited much from the **Neverwinter Nights (NWN)** codebase. NWN was built as a **client–server** game: a server authoritative model with a client that renders and handles input. That client–server split left traces in the Odyssey executable: debug strings and logic still reflect "client" and "server" concepts inside the same process.

Community and reverse-engineering discussion (e.g. from the KOTORMax/walkmesh context documented in `bwm_mdl_lyt_kotormax_context.md`) summarizes the consequence for walkmeshes as follows:

- **Two distinct walkmesh-related data sources** exist for an area room: (1) The **standalone WOK file** (BWM format), referenced by the area (e.g. by resref in the ARE or via the room list). This file contains the full BWM: vertices, faces, materials, **AABB tree**, **adjacencies**, **edges**, and **perimeters** (including transition IDs for room boundaries). (2) **AABB/walkmesh data embedded inside the room’s MDL**. The room model (e.g. `m01aa_room0.mdl`) can contain a block of AABB (or walkmesh) data used by the engine for **camera collision** and possibly other client-side spatial queries.

- **Which is "client" and which is "server"?** The exact mapping is not definitively documented in a single place. Community consensus (e.g. Wizard in the referenced Discord conversation) is that **one walkmesh is used for client-side computation** (e.g. camera collision) and **one for server-side** (e.g. pathfinding and movement). It is often stated that the **WOK** is the one used for pathfinding/transitions (and thus "server" in the original sense), and that **camera collision** depends on the data **inside the MDL**. So in practice: **WOK** → pathfinding, room transitions, adjacency, perimeters; must be present and consistent for movement and crossing between rooms. **MDL-embedded AABB/walkmesh** → required for correct **camera collision**; without it, the camera may pass through geometry even if the WOK is correct.

- **Implication for authors:** When creating or modifying a room, both the WOK and the room MDL’s walkmesh/AABB data should be updated and kept consistent. Export pipelines (e.g. KOTORMax with "Export WOK File" enabled) produce both the standalone WOK and the MDL (with embedded data). Reusing only one or the other can lead to correct pathfinding but broken camera collision, or vice versa.

This section is included so that the **why** behind "two sources" is clear: it is not an arbitrary design choice but a consequence of the Aurora/NWN client–server lineage and the way the Odyssey executable still separates certain collision and pathfinding responsibilities.

---

## Why the format is structured this way

- **Aurora / NWN lineage** — The Odyssey engine reuses concepts and formats from the Aurora engine (Neverwinter Nights). In NWN, walkmeshes are used for 2.5D movement, pathfinding, and tile/placeable/door collision. The BWM layout (header, vertices, faces, materials, AABB, adjacency, edges, perimeters) reflects this heritage: a single binary format that supports both spatial queries (AABB tree) and pathfinding (adjacency, perimeters with transition IDs).

- **2.5D and height** — Vertices are 3D (X, Y, Z), but movement and pathfinding are effectively 2.5D: the engine cares about height for stepping and line-of-sight, but the graph of walkable faces is built from triangles in the X–Y plane with Z for elevation. So the format stores full 3D vertices and normals/distances for proper spatial and hit tests.

- **Material masks** — The engine uses **bitmasks** (one bit per material ID) to filter which faces are walkable, block LOS, or pass "walk check." That’s why material indices are small integers and must be preserved: they index into surfacemat.2da and into these bitmask positions. The BWM does not store walkability directly; it stores material IDs. Walkability is resolved at runtime from the 2DA.

- **Adjacency for pathfinding** — Pathfinding (e.g. A* or similar) runs over the graph of walkable faces. Each face has up to three neighbors; the adjacency table stores exactly that. Boundary edges (no neighbor) become perimeter edges and can carry a transition ID for room changes. So the format explicitly supports both "walk within a room" and "cross to another room" without extra structures.

- **AABB tree for ray cast and point query** — Click-to-move, projectiles, and camera collision need fast ray–mesh and point-in-mesh tests. An AABB tree (binary space partition over axis-aligned boxes) is a standard solution. The engine writes a 44-byte node format and a root index so it can traverse the tree without storing pointers (indices are 0-based into the node array). The "most significant plane" field is used to choose traversal order for ray-direction heuristics.

- **Perimeters and 1-based loop ends** — Boundary edges are grouped into closed loops (e.g. the outer boundary of the walkable floor, or holes). Storing 1-based loop-end indices is a compact way to describe "loop 1 is edges 0..N-1, loop 2 is N..M-1" without repeating edge counts. The engine uses these loops to know which edges are boundaries and which of those boundaries are transition edges (with a transition ID).

- **No versioning beyond V1.0** — For KotOR 1 and 2, only one BWM version is used. The header magic and version string are fixed; there are no format variants or version checks beyond that in the documented engine behavior.

---

## Relationship to MDL and resource resolution

- **BWM as a separate resource** — A BWM file (e.g. `m01aa_room0.wok`) is a **standalone resource**. The area (ARE) or the game logic references it by **resref** (e.g. `m01aa_room0`), and the engine loads it through the usual resource system (KEY, BIF, override order). There is **no** offset or index from inside a BWM file that points into an MDL, and **no** offset inside an MDL that points into a BWM file. The relationship is by **naming and usage**: the same logical room has a room model (MDL) and a room walkmesh (WOK), both identified by the same base name, but they are separate files and separate loads.

- **MDL’s own AABB/walkmesh block** — The room MDL (see [MDL-MDX-File-Format](MDL-MDX-File-Format)) can contain an embedded block of AABB or walkmesh-related data. That block is **part of the MDL format**, not part of the BWM format. The engine uses it (in particular for camera collision) independently of the WOK. So for a given room you have: One **WOK** (BWM): pathfinding, transitions, adjacency, perimeters. One **MDL** (with optional AABB/walkmesh block): rendering and camera collision. They are **not** linked by file offsets or by a KEY/BIF-style index. They are linked by **convention** (same resref base name) and by **authoring** (tools that export both so they stay in sync).

- **KEY/BIF and resource resolution** — Resource lookup works the same for BWMs as for other assets: the game resolves a resref (e.g. `m01aa_room0`) to a container (KEY/BIF or override), then loads the appropriate type (e.g. WOK). The BWM format does not define or reference KEY or BIF structures; it is just one of the resource types that the engine can load by name. So "does BWM link to MDL offsets like KEY/BIF?" — no: KEY/BIF are the **mechanism** that resolve names to files; BWM and MDL are two different resource types that are associated by name and usage, not by cross-file offsets.

**What is in the MDL (embedded walkmesh / AABB block)?** The [MDL-MDX](MDL-MDX-File-Format) format can include a block of AABB or walkmesh-related data embedded in the model file. That block is part of the MDL layout (nodes, geometry, animations, etc.), not part of the BWM layout. The engine uses this embedded data for **camera collision** and possibly other client-side spatial queries. The BWM file does not reference this block, and the MDL block does not reference the BWM file by offset or index. So: the MDL contains *its own* spatial/walkmesh data; the WOK is a *separate* file loaded by resref. Both are needed for a fully correct room (pathfinding + camera collision), and both should be kept in sync by the authoring pipeline. For the exact MDL node and data layout, see the MDL-MDX wiki and the Game Engine BWM/AABB Implementation doc.

---

## Data Types and Conventions

- **Byte order:** All multi-byte integers and floats are **little-endian** (Intel byte order).
- **Header size:** The file header is exactly **136 bytes (0x88)**. Data tables follow at the offsets given in the header.
- **Magic and version:** Header starts with magic `"BWM "` (4 bytes) and version `"V1.0"` (4 bytes). No other format version field is used for Odyssey.

---

## File Structure Overview

Layout order (engine write order per reverse-engineered source):

1. **Header** (136 bytes) -- counts, offsets, `world_coords`, `aabb_root`
2. **Vertices** -- at `vertex_offset`
3. **Faces** -- at `face_offset`
4. **Materials** -- at `materials_offset`
5. **Normals** -- at `normals_offset`
6. **Distances** -- at `distances_offset`
7. **AABB nodes** -- at `aabb_offset`
8. **Adjacencies** -- at `adjacency_offset`
9. **Edges** -- at `edge_offset`
10. **Perimeters** -- at `perimeter_offset`

---

## Binary Format

### File Header

Total size: **136 bytes (0x88)**. Offsets are from the start of the file.

| Name | Type | Offset (hex) | Offset (dec) | Description |
|------|------|--------------|--------------|-------------|
| magic | char[4] | 0x00 | 0 | `"BWM "` |
| version | char[4] | 0x04 | 4 | `"V1.0"` |
| world_coords | int32 | 0x08 | 8 | `0` = local (PWK/DWK), `1` = world (WOK). Engine uses this to decide whether to transform vertices. **Critical for area WOK:** when building a module, exported room WOK must have `world_coords = 1` after baking LYT translation; otherwise the engine can treat vertices as local and apply transforms again (player may spawn with no walkable face). See [Indoor Map Builder Implementation Guide](Indoor-Map-Builder-Implementation-Guide). |
| relative_use_positions | Vector[2] | 0x0C | 12 | Relative use positions (2 × 12 bytes) |
| absolute_use_positions | Vector[2] | 0x24 | 36 | Absolute use positions (2 × 12 bytes) |
| position | Vector | 0x3C | 60 | Position (12 bytes) |
| vertex_count | uint32 | 0x48 | 72 | Number of vertices |
| vertex_offset | uint32 | 0x4C | 76 | File offset to vertex data |
| face_count | uint32 | 0x50 | 80 | Number of faces (triangles) |
| face_offset | uint32 | 0x54 | 84 | File offset to face data |
| materials_offset | uint32 | 0x58 | 88 | File offset to materials |
| normals_offset | uint32 | 0x5C | 92 | File offset to normals |
| distances_offset | uint32 | 0x60 | 96 | File offset to distances |
| aabb_count | uint32 | 0x64 | 100 | Number of AABB nodes |
| aabb_offset | uint32 | 0x68 | 104 | File offset to AABB tree |
| aabb_root | uint32 | 0x6C | 108 | Root node index (0-based) for AABB tree |
| adjacency_count | uint32 | 0x70 | 112 | Number of walkable faces (for adjacency table) |
| adjacency_offset | uint32 | 0x74 | 116 | File offset to adjacency data |
| edge_count | uint32 | 0x78 | 120 | Number of edges |
| edge_offset | uint32 | 0x7C | 124 | File offset to edge data |
| perimeter_count | uint32 | 0x80 | 128 | Number of perimeter loop markers |
| perimeter_offset | uint32 | 0x84 | 132 | File offset to perimeter data |

*Source: reverse-engineered engine (vendor/swkotor.c, vendor/swkotor.h).*

**Vector:** Three single-precision floats (X, Y, Z), 12 bytes total.

---

### Vertices

At `vertex_offset`. Each vertex is three single-precision floats (X, Y, Z), 12 bytes. Total size: `vertex_count * 12` bytes. Coordinate space is determined by `world_coords` in the header (world for WOK, local for PWK/DWK). Vertex indices in the face table are 0-based into this array. The engine does not transform these at load time when `world_coords == 1`; when `world_coords == 0` it applies the object’s matrix at runtime for PWK/DWK. So for area rooms, vertices must already be in world space when the WOK is written (e.g. after baking the room’s LYT position in a build pipeline).

---

### Faces

At `face_offset`. Each face is a triangle: three vertex indices and a material index. The exact layout (byte size and field order) is defined by the engine and matches the structures used in the reverse-engineered load/write code; see [Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation) for the runtime face representation. The important points for the format are:

- Each face references three vertices (0-based indices into the vertex array). Winding order (which side is "up") is consistent with the normal and with adjacency: an edge shared with a neighbor is stored in the same vertex order on both sides so that "left" and "right" neighbor are well-defined.
- Each face has a **material index** used at runtime to look up surface type and walkability in [surfacemat.2da](2DA-surfacemat). The engine builds bitmasks from these indices (e.g. `walkable_material_mask |= (1 << material_id)`). So the face table is the source of per-triangle material IDs; the adjacency table then tells the pathfinder which faces are connected and thus walkable from each other.
- Face index (0-based) is used in adjacency encoding: `adjacency[face_index * 3 + edge_index]` and in the edge table's `face_index * 3 + local_edge_index` encoding. So the order of faces in the file is significant and must match the order assumed by the adjacency and edge tables.

The BWM does not store "walkable" as a boolean per face; walkability is derived at runtime from the material index and [surfacemat.2da](2DA-surfacemat). Non-walkable faces still appear in the mesh and in the AABB tree for collision and ray cast; the pathfinder simply ignores faces whose material is not in the walkable mask.

---

### Materials, Normals, Distances

At `materials_offset`, `normals_offset`, `distances_offset`. The engine uses material indices as **bit positions** in runtime masks (`walkable_material_mask`, `los_material_mask`, etc.). Walkability is resolved at runtime from [surfacemat.2da](2DA-surfacemat) (reverse-engineered engine). Material IDs must be preserved; valid range is typically [0, 22]. Normals and distances are used for spatial and hit tests (e.g. plane equations, distance-to-plane). The exact layout of these tables is defined by the engine's load logic; the important invariant is that material index per face drives both collision filtering and the 2DA lookup for walkability and surface type.

---

### AABB Tree

At `aabb_offset`. Used for fast spatial queries (ray casting, point-in-triangle).

- **Node size:** **44 bytes (0x2C)** per node.
- **Node layout:** Min bounds (Vector), max bounds (Vector), right child index (uint32), left child index (uint32), most significant plane (int32).
- **Child indices:** **0-based** array indices into the AABB array. No child = `0xFFFFFFFF` (-1).
- **Root:** Header field `aabb_root` (offset 0x6C) is the 0-based index of the root node.
- **Most significant plane:** Split axis / leaf hint. Values observed: 0 (leaf), 1-3 (positive X/Y/Z), -2 to -4 (negative X/Y/Z). Engine uses this for traversal order (direction heuristic).

---

### Walkable Adjacencies

At `adjacency_offset`. Flat array of **int32**; size **adjacency_count × 3** (one per edge of each walkable face).

- **Indexing:** `adjacency[face_idx * 3 + edge_idx]`
- **Value:** `adjacent_face_idx * 3 + adjacent_edge_idx`, or `-1` (0xFFFFFFFF) if no neighbor.
- **Bidirectional:** If face A edge 0 connects to ***face B*** edge 2, then `adjacency[A*3+0] = B*3+2` and `adjacency[B*3+2] = A*3+0`. Required for pathfinding.

---

### Edges

At `edge_offset`. Each *edge* is **8 bytes**:

| Field | Type | Description |
|-------|------|-------------|
| index | uint32 | Encoded as `face_index * 3 + local_edge_index` |
| transition | int32 | Transition ID (0-based [LYT](LYT-File-Format) *room index*) for perimeter edges, or -1 (0xFFFFFFFF) |

*Perimeter edges* (edges with no adjacent walkable face) that form a room boundary carry the **transition ID** of the *adjacent* room (the 0-based index of that room in the area’s [LYT](LYT-File-Format) room list).

---

### Perimeters

At `perimeter_offset`. Array of **uint32** giving **1-based loop end indices** for boundary edge loops.

- `perimeters[0] = N` → first loop is edges 0 to N-1
- `perimeters[1] = M` → second loop is edges N to M-1
- etc.

### Load order and write order

The engine writes BWM data in a fixed order (see [Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation)): header first, then vertices, faces, materials, normals, distances, then AABB nodes, then adjacencies, then edges, then perimeters. The header stores **File Offsets** to each table so that the loader can seek to the correct position. When building a BWM, writers must emit data in this order and fill the header offsets accordingly. The BWM file does not use a “chunk” or “tag” format; it is a fixed header plus contiguous tables at specified offsets, similar to many binary mesh formats in game engines.

### Edge cases and validation

- **AABB tree:** Child indices must be 0-based and valid (or -1 for no child). A degenerate tree (e.g. all leaves, or inconsistent left/right) can cause incorrect ray or point queries; community tools (e.g. KOTORMax) have historically had to “set up arrows that point inwards to the very next AABB/face” at seams so the tree remains consistent. If the tree is malformed, the engine may traverse incorrectly and camera collision or click-to-move can fail.
- **Adjacency:** Must be **bidirectional**: if face A edge 0 is adjacent to face B edge 2, then both `adjacency[A*3+0] = B*3+2` and `adjacency[B*3+2] = A*3+0` must hold. Perimeter edges (boundary of the walkable region) have adjacency -1. Pathfinding assumes this encoding; one-way or missing links cause pathfinding failures.
- **Perimeters:** Loop-end indices must form valid closed loops (no out-of-range edge indices). Each perimeter edge should appear in exactly one loop. Transition IDs on perimeter edges must be in range [0, N-1] where N is the number of rooms in the area’s LYT, or -1 for non-transition boundaries.
- **Vertices:** No duplicate or degenerate triangles are required to be filtered by the format; the engine may tolerate them for collision but pathfinding and transitions rely on correct adjacency and perimeter data.

---

## WOK vs PWK vs DWK

| | WOK | PWK | DWK |
|---|-----|-----|-----|
| **Coordinates** | World (`world_coords = 1`) | Local (`world_coords = 0`) | Local (`world_coords = 0`) |
| **Typical use** | Area/room | [Placeable](GFF-UTP) | [Door](GFF-UTD) (closed/open1/open2) |
| **Pathfinding** | Yes ([adjacency](BWM-File-Format#walkable-adjacencies), [perimeters](Game-Engine-BWM-AABB-Implementation#perimeters), [transitions](Transitions-and-Door-Placement)) | *Collision-only* | *Collision-only* |
| **AABB tree** | Yes | *Typically no* | *Typically no* |
| **Transform** | Vertices used as-is | *Engine applies object matrix at runtime* | *Engine applies door matrix at runtime* |

When building a module from an *indoor map*, each exported room *WOK* must have vertices in world space and **`world_coords = 1`** after the [LYT](LYT-File-Format) room transform is baked; see [Indoor Map Builder Implementation Guide](Indoor-Map-Builder-Implementation-Guide).

---

## Transitions and Door Placement

- **Transition ID** on a perimeter edge = **0-based index** of the adjacent room in the area’s [LYT](LYT-File-Format) room list. Crossing that edge moves the player to that room.
- **Roomlinks** in community tooling refer to assigning these transition IDs so both sides of a seam point to the correct room. If rooms are added, removed, or reordered in the [LYT](LYT-File-Format), transition IDs must be reassigned; visual alignment alone is not enough. See [Area Modding and Room Transitions](Area-Modding-and-Room-Transitions).
- **Doors:** A functioning door requires a door model, door walkmesh (DWK) with closed/open1/open2 states, correct surface material on the threshold, and roomlinks connecting both rooms. Door walkmesh node naming (e.g. `_wg_closed`, `_wg_open1`, `_wg_open2`) matters for the engine. Community workflow: KOTORMax Room Linker and “Export WOK File” enabled when exporting.

---

## Related Formats and Engine Behavior

- **[LYT](LYT-File-Format):** Room order in the [LYT](LYT-File-Format) defines the 0-based room index used as the transition ID on perimeter edges.
- **[VIS](VIS-File-Format):** Visibility graph; used with the same area/room set. Does not control collision or transitions.
- **[GFF-ARE](GFF-ARE):** Area file; references *WOK/PWK/DWK* by ResRef. Resource resolution follows the usual [KEY/BIF/override order](KEY-File-Format).
- **[surfacemat.2da](2DA-surfacemat):** Each walkmesh face has a material index; the engine looks up walkability and surface type in this table at runtime.
- **[Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation):** Coordinate handling and AABB traversal.
- **[MDL-MDX](MDL-MDX-File-Format):** *Room models* can contain embedded *AABB/walkmesh* data used for camera collision; both *WOK* and *MDL* walkmesh data should be consistent. The *MDL* does not contain “pointers” or offsets into the *WOK*; it contains its own spatial data block. Consistency is a content-authoring requirement, not a format-level link.

For coordinate handling, *AABB* traversal, and write order, see [Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation).

### Industry and standards context

- **AABB and spatial trees:** Axis-aligned bounding boxes (AABBs) and AABB trees are standard in real-time collision and culling [1][2]. Ericson’s *Real-Time Collision Detection* (Morgan Kaufmann Series in Interactive 3D Technology) covers AABB representation, AABB trees, and spatial partitioning in depth [1]. *Real-Time Rendering* (Akenine-Möller et al.) treats acceleration structures including BVH/AABB for ray tracing and culling [2]. The Odyssey engine’s 44-byte AABB node and 0-based child indices follow this pattern.
- **Navigation meshes:** Walkable-surface meshes and face adjacency for pathfinding are standard in game AI [3][4][5]. Millington’s *Artificial Intelligence for Games* (Routledge) includes pathfinding over navigation meshes and graph representations [3]. The xoreos project documents walkmesh-based pathfinding (A* plus Simple Stupid Funnel Algorithm) for Aurora-derived engines including KotOR [4]. GDC talks such as “Math for Game Developers: Generating and using Navigation Meshes” cover generation and use of nav meshes [5]. The BWM adjacency encoding (face index × 3 + edge index) is an explicit edge-adjacency representation for a triangle mesh.
- **Data-driven surface types:** Using a table to define walkability and surface properties by ID is a common pattern. In Neverwinter Nights (Aurora), [surfacemat.2da](2DA-surfacemat) defines Walk, LineOfSight, and surface names (e.g. footstep sounds) [6][7]. The Odyssey engine defers to surfacemat.2da rather than hardcoding in the BWM.
- **NWN / Aurora lineage:** Neverwinter Nights and the Aurora engine use `.wok` (tile), `.pwk` (placeable), `.dwk` (door) and surfacemat.2da; the Odyssey BWM format and usage are derived from that lineage [6][7][8]. The NWN wiki describes the walkmesh as a 2.5D height mesh governing walkability, footstep sounds, and line of sight [6]. The nwn.wiki surfacemat.2da reference documents the 2DA layout and Walk/LineOfSight columns [7]. xoreos-docs and the xoreos pathfinding wiki provide engine and KotOR/NWN context [4][8]. Binary layout for Odyssey is engine-specific and documented here and in [Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation).

**References (official or high-quality sources):**

1. Christer Ericson, *Real-Time Collision Detection*, Morgan Kaufmann Series in Interactive 3D Technology, 2005. Official companion site (TOC, errata, references): [realtimecollisiondetection.net](https://realtimecollisiondetection.net/books/rtcd/).
2. Tomas Akenine-Möller, Eric Haines, Naty Hoffman, *Real-Time Rendering*, 4th ed., A K Peters/CRC Press, 2018. Official site (sample chapters, collision detection chapter): [realtimerendering.com](https://www.realtimerendering.com/).
3. Ian Millington, *Artificial Intelligence for Games*, 3rd ed., CRC Press/Routledge, 2019. Publisher: [Routledge – AI for Games](https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9780367670566).
4. xoreos project, “Pathfinding,” wiki (navigation mesh, A*, SSFA, KotOR/NWN). [wiki.xoreos.org – Pathfinding](https://wiki.xoreos.org/index.php?title=Pathfinding).
5. GDC Vault, “Math for Game Developers: Generating and using Navigation Meshes,” Ben Sunshine-Hill (Havok). [gdcvault.com](https://www.gdcvault.com/play/1025908/Math-for-Game-Developers-Generating).
6. NWNWiki (Fandom), “Walkmesh” – .wok/.pwk/.dwk roles, 2.5D height mesh, walkability. [nwn.fandom.com/wiki/Walkmesh](https://nwn.fandom.com/wiki/Walkmesh).
7. nwn.wiki, “surfacemat.2da” – NWN:EE 2DA layout, Walk/LineOfSight/Name columns. [nwn.wiki – surfacemat.2da](https://nwn.wiki/display/NWN1/surfacemat.2da).
8. xoreos-docs (GitHub), documentation for xoreos engine development; Aurora/KotOR resource and engine context. [github.com/xoreos/xoreos-docs](https://github.com/xoreos/xoreos-docs).
9. Routledge/CRC, *Real-Time Collision Detection* (Ericson), publisher page. [Routledge – Real-Time Collision Detection](https://www.routledge.com/Real-Time-Collision-Detection/Ericson/p/book/9781558607323).
10. GDC Vault, “Down with Nav Meshes: The Next Generation of Navigation Data,” AI Summit (alternatives and evolution of nav data). [gdcvault.com](https://www.gdcvault.com/play/1027984/AI-Summit-Down-with-Nav).

---

## Authoring and Tooling

The canonical format is defined by the Odyssey engine and this document. The following are **community implementations** for creating and editing *BWM/WOK* data.

### KOTORMax (GMax / 3ds Max)

- **Primary tool** for area walkmeshes and **room transitions** in practice. Supports [LYT](LYT-File-Format)/[VIS](VIS-File-Format) import and export, **Room Linker** (roomlinks/transition edges), and **Export WOK File** (must be enabled when exporting room walkmesh).
- Workflow: Convert room MDL to ASCII (e.g. with MDLEdit) → load area via **Area Tools** (not MDL Loading) with [LYT](LYT-File-Format)so room order is correct → edit walkmesh (OdysseyWalkmesh modifier, type Area, materials via e.g. wokmat.ini) → reassign roomlinks at seams → export with **Export WOK File** checked → compile ASCII to binary (e.g. MDLEdit). File naming: use `.mdl.ascii` and match the "Use .ascii By Default" filter to avoid "No appropriate import module found."
- **Do not** load the [LYT](LYT-File-Format) through the MDL Loading panel (it expects model ASCII); load the layout through **Area Tools**. Room transition IDs = [LYT](LYT-File-Format) room order; if you add or move rooms, roomlinks must be reassigned in KOTORMax.
- Community references: [KOTORMax on Deadly Stream](https://deadlystream.com/files/file/1151-kotormax/), [Adding existing rooms to a module](https://deadlystream.com/topic/8517-adding-existing-rooms-to-a-module/), [K1 Creating a new room](https://deadlystream.com/topic/11729-k1-creating-a-new-room-in-an-existing-module/).

### KotorBlender

- Blender add-on (e.g. [OldRepublicDevs/kotorblender](https://github.com/OldRepublicDevs/kotorblender)) for WOK/PWK/DWK import and export and room linking on edges.
- Community guidance: KotorBlender has **gaps for finalizing room-to-room transitions**; for reliable crossing between rooms, KOTORMax (or another roomlink-capable workflow) is preferred. Vertex-paint–based or hash-based approaches may work in some cases but can cause edge-case failures in-game. Use KotorBlender for geometry work; use KOTORMax for layout-aware roomlink editing when crossing matters.

### Common authoring mistakes

- **Skipping roomlinks:** Editing only mesh or materials and never reassigning transition IDs on perimeter edges. Result: visually aligned rooms that still block crossing.
- **Loading LYT from the wrong panel:** In KOTORMax, loading the `.lyt` from MDL Loading (which expects model ASCII) causes "invalid ascii." Load the layout from **Area Tools** so room order and roomlink context are correct.
- **Leaving "Export WOK File" disabled:** The MDL is exported but the standalone `.wok` is not updated; the game keeps using the old WOK, so pathfinding and transitions do not reflect your edits.
- **Wrong coordinate space for room WOK:** Exporting a room WOK with `world_coords = 0` or with vertices still in local space. The engine then transforms them again and the player can spawn with no valid walkable face. For area rooms, WOK must have world-space vertices and `world_coords = 1` after the room's LYT position is baked.
- **Filename/extension mismatch:** In KOTORMax, the import filter ("Use .ascii By Default") expects a specific extension (e.g. `.mdl.ascii`). If the file has a different name or extension (e.g. `203tell-mdledit.mdl.ascii`), the dialog may not show it or the importer may reject it. Rename to a clean base name and correct extension and use KOTORMax's Import rollout, not GMax's generic File → Import.
- **Assuming Blender alone fixes transitions:** KotorBlender has known gaps for room-to-room transitions; vertex-paint or hash-based linking can fail. For reliable crossing, use KOTORMax (or another layout-aware roomlink tool) for the final roomlink step.
- **Merging two rooms into one walkmesh:** The engine expects **separate** room walkmeshes with a **seam** where the transition edge carries the transition ID. One combined walkmesh does not define a room boundary and will not trigger a room change.
- **Hand-editing roomlinks in ASCII without layout:** Room transition IDs are [LYT](LYT-File-Format) room indices. If you edit raw values without loading the area layout, you can easily assign wrong IDs or break bidirectional consistency. Use the Room Linker (or equivalent) in the context of the full area.

### Kaurora

- Can import/export WOK and edit room adjacency (e.g. [KAurora on Deadly Stream](https://deadlystream.com/files/file/703-kaurora/)). Useful for inspecting and editing room links and walkmesh data.

### Summary of the common “can’t cross between rooms” issue

If two room models line up visually but the player still cannot walk from one to the other, the cause is usually **not** the visible geometry. It is the **room-to-room walkmesh links** (transition IDs on perimeter edges). In KotOR indoor areas, crossing depends on:

1. Rooms positioned correctly in the area layout ([LYT](LYT-File-Format)).
2. Each room’s walkmesh edge physically aligned with the neighboring room.
3. **Roomlinks reassigned** so perimeter edges carry the correct transition ID (LYT room index). This must be done in a layout-aware tool (e.g. KOTORMax Area Tools), especially after adding or rearranging rooms.
4. Area LYT and VIS include the new or changed rooms.
5. The exported room includes an updated WOK (**Export WOK File** enabled).
6. ASCII compiled back to binary (e.g. MDLEdit).

Lining up meshes, combining walkmeshes, or repainting materials **does not** fix crossing without correct roomlinks. Load the area via the layout workflow (e.g. KOTORMax Area Tools), then reassign which edge links to which room.

### The KOTORMax / walkmesh conversation summarized (why tooling is confusing)

The following is a structured summary of the community and tooling confusion documented in `bwm_mdl_lyt_kotormax_context.md`. It is included so that future readers have a single place that explains *why* walkmesh authoring is difficult and what actually has to be fixed.

**Typical problem:** A modder has two room models that line up visually but the player cannot walk from one room into the other. They try aligning meshes, combining walkmeshes, or repainting materials—none of which fixes the issue.

**Root cause:** Crossing between rooms is not determined by visible geometry or walkmesh shape alone. It is determined by **roomlinks**: the transition IDs on perimeter edges of the walkmesh. Those IDs must point to the correct adjacent room (the 0-based LYT room index). If the layout changes (rooms added, removed, or reordered), the original roomlinks no longer match and must be reassigned in a layout-aware tool (e.g. KOTORMax Room Linker). Visual alignment is necessary but not sufficient.

**Client–server and two walkmesh sources:** The Odyssey engine inherits a client–server split from the Aurora/NWN lineage. As a result there are two walkmesh-related data sources for a room: (1) the **standalone WOK** (pathfinding, room transitions, adjacency, perimeters); (2) **AABB/walkmesh data inside the room MDL** (used for camera collision). Community consensus is that camera collision will not work correctly without the MDL-embedded data; the WOK alone is not enough for that. So authors must keep both in sync: export both the WOK and the MDL with embedded walkmesh/AABB when changing a room.

**KOTORMax vs KotorBlender:** KotorBlender can import/export WOK and do some room linking, but community guidance is that it has **gaps** for finalizing room-to-room transitions—vertex-paint or hash-based approaches can fail in edge cases. KOTORMax (GMax/3ds Max) has been the battle-tested tool for roomlinks and layout for over a decade and was what the original developers used. For reliable crossing, the recommended workflow is to use KOTORMax for layout and roomlink editing, and to use KotorBlender only for geometry work if at all.

**Area Tools vs MDL Loading:** In KOTORMax, the **Area Tools** panel is for loading the **area layout** (LYT, and optionally VIS and models). The **MDL Loading** panel is for loading **ASCII model files** (e.g. `.mdl.ascii`). If you try to open a `.lyt` file from MDL Loading, you get “invalid ascii” because the LYT is not a model file. You must load the LYT from **Area Tools** so that room order and layout context are correct. Room transition IDs are the LYT room indices; that context only makes sense when the area is loaded as a layout.

**Export WOK File:** When exporting a room from KOTORMax, a preference **“Export WOK File”** must be **enabled** (it is off by default in some setups). If it is disabled, the exporter updates the MDL but does not write the standalone `.wok` file, so the area’s pathfinding and room transitions still use the old WOK. This is a very common cause of “I edited the walkmesh but nothing changed in-game.”

**Filename and extension:** KOTORMax’s import file dialog is filtered by a “Use .ascii By Default” setting. If the filter expects `.mdl.ascii` and your file is named something like `203tell-mdledit.mdl.ascii` or has a different extension, the dialog may not show it or the importer may reject it. The fix is to rename the file to a clean base name with the correct extension (e.g. `203tell.mdl.ascii`) and to use KOTORMax’s own Import rollout, not GMax’s generic File → Import. MDLEdit outputs ASCII with a naming pattern that may include extra suffixes; strip those so the base name matches the model name and the extension matches the filter.

**What does *not* fix room crossing:** Lining up meshes; combining two walkmeshes into one; repainting all faces to a walkable material; hand-editing roomlink values in ASCII without going through the proper area/layout workflow; or importing only one room model and hoping the engine will infer adjacency. The engine relies on the transition ID on each perimeter edge. If that ID is wrong or missing, the player cannot cross even when the geometry looks correct.

**What *does* fix it:** (1) Load the **full area** via **Area Tools** (LYT, and models in the same folder if you want them loaded with the layout). (2) Position the new or modified room correctly in the layout. (3) Align the walkmesh **threshold** (the shared edge between the two rooms) so there is no gap, no overlap, and no height mismatch. (4) Use the **Room Linker** (or equivalent) to **reassign roomlinks** so the boundary edges of each room point to the other room’s LYT index. (5) Enable **Export WOK File** and export the room(s). (6) Export updated LYT/VIS if the layout changed. (7) Compile all ASCII to binary (e.g. MDLEdit) and place the resulting WOK and MDL in the module or override. (8) Test in-game; if crossing still fails, verify both sides’ roomlinks and the room order in the LYT.

**Doors:** A functioning door (not just an open threshold) also requires a door model, door walkmesh (DWK) with the correct node names (e.g. `_wg_closed`, `_wg_open1`, `_wg_open2`), the right surface material on the threshold, and roomlinks connecting both rooms. Room-to-room traversal and door object behavior are related but separate: fixing the seam fixes crossing; a full door may need additional scripting and door hooks.

**Why this is documented here:** The original Discord conversation and the various KOTORMax guides scattered across Deadly Stream and forums are the primary source for this workflow. It is easy to get lost in extension quirks, panel names, and the difference between “looks right” and “actually linked.” This section condenses that into one place so that the **how** and **why** of BWM authoring and room transitions are clear, and so the relationship between the format (BWM), the engine (client–server, two sources), and the tools (Area Tools, Room Linker, Export WOK) is explicit.

---

## See also

- [Area Modding and Room Transitions](Area-Modding-and-Room-Transitions) -- What must agree for room crossing
- [LYT File Format](LYT-File-Format) -- Room order and room definitions (room index = transition ID)
- [VIS File Format](VIS-File-Format) -- Visibility graph
- [Indoor Area Room Layout and Walkmesh Guide](Indoor-Area-Room-Layout-and-Walkmesh-Guide) -- Workflow for layout, walkmesh, and roomlinks
- [Indoor Map Builder Implementation Guide](Indoor-Map-Builder-Implementation-Guide) -- BWM coordinate space and build-time WOK export
- [Indoor Map Builder User Guide](Indoor-Map-Builder-User-Guide) -- End-user walkmesh and room placement
- [Kit Structure Documentation](Kit-Structure-Documentation) -- WOK/DWK/PWK in kits, door hooks from edges
- [Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation) -- Coordinate handling and AABB traversal
- [GFF-ARE](GFF-ARE) -- Area files that reference walkmeshes
- [2DA-surfacemat](2DA-surfacemat) -- Material IDs and walkability
- [MDL-MDX File Format](MDL-MDX-File-Format) -- Embedded AABB/walkmesh in room models

---

## References and further reading

**Reverse-engineered engine (primary for binary layout and behavior):**  
Vendor/local sources `vendor/swkotor.c` and `vendor/swkotor.h` (Ghidra decompilation of `swkotor.exe` / `swkotor2.exe`). This wiki and [Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation) summarize the structures (e.g. `CSWWalkMeshHeader`, `CSWRoomSurfaceMesh`, AABB node, adjacency encoding, edge and perimeter layout).

**Industry and standards (concepts, not Odyssey-specific):**  
- Ericson, *Real-Time Collision Detection* (Morgan Kaufmann) — AABB trees, spatial partitioning, ray casting.  
- Akenine-Möller et al., *Real-Time Rendering* — BVH and AABB for ray tracing and culling.  
- Millington, *Artificial Intelligence for Games* — Navmesh pathfinding, face adjacency, A* on graphs.  
- GDC and similar talks on navigation meshes and pathfinding in game engines.

**Aurora / NWN lineage:**  
- nwn.fandom.com, nwn.wiki — Neverwinter Nights walkmesh, .wok/.pwk/.dwk, surfacemat.2da, 2.5D movement. Odyssey is Aurora-derived; KotOR WOK differs in detail but the roles (tile/placeable/door, world vs local) are analogous.  
- xoreos pathfinding wiki — Walkmesh as nav mesh, A* and SSFA, face adjacency, relation to surfacemat.2da. No dedicated BWM binary spec in xoreos-docs; this wiki and the Game Engine BWM doc are the format reference.

**Community tooling and discussion:**  
- [KOTORMax (Deadly Stream)](https://deadlystream.com/files/file/1151-kotormax/), [OldRepublicDevs/KOTORMax](https://github.com/OldRepublicDevs/KOTORMax) — GMax/3ds Max; Area Tools, Room Linker, Export WOK, LYT/VIS.  
- [kotorblender](https://github.com/OldRepublicDevs/kotorblender) — Blender add-on; WOK/PWK/DWK import/export; community notes on gaps for room transitions.  
- [KAurora (Deadly Stream)](https://deadlystream.com/files/file/703-kaurora/) — WOK import/export, room adjacency.  
- Deadly Stream forums (e.g. "Adding existing rooms to a module," "K1 Creating a new room") — Workflow for roomlinks, Area Tools vs MDL Loading, Export WOK, filename/extension issues.  
- Context document `bwm_mdl_lyt_kotormax_context.md` (in repo) — Discord conversation and AI-derived summary on client–server, two walkmesh sources, KOTORMax workflow, and the "can't cross between rooms" fix.
