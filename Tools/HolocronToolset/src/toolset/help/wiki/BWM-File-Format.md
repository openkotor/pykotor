# KotOR BWM File Format Documentation

This document provides a detailed description of the BWM (Binary WalkMesh) file format used in Knights of the Old Republic (KotOR) games.

## What is a BWM File?

A BWM file is a file format used by BioWare games to store walkmesh data. A walkmesh is a simplified 3D model made of triangles that defines where characters can walk, where they cannot walk, and how high the ground is at different locations.

**BWM files come in three types:**

- **WOK (Area Walkmesh)**: Used for entire areas/modules. Contains vertices in world coordinates, includes an AABB tree for fast spatial queries, has walkable adjacency information, and perimeter edges for transitions between areas.
- **PWK (Placeable Walkmesh)**: Used for placeable objects (chests, tables, etc.). Contains vertices in local coordinates (relative to the placeable's position), collision-only (no pathfinding), typically no AABB tree.
- **DWK (Door Walkmesh)**: Used for doors. Similar to PWK, contains vertices in local coordinates, collision-only, typically no AABB tree.

Area rooms can have **two** walkmesh-related data sources: (1) the **WOK file** (standalone BWM)—used for room transitions (adjacency, perimeters, transition IDs); (2) **AABB/walkmesh data embedded in the room MDL**—used by the engine for camera collision in some code paths. Both must be consistent for correct behavior.

**What walkmeshes do:**

Walkmeshes serve multiple critical functions in KotOR:

- **Pathfinding**: NPCs and the player use walkmeshes to navigate areas, with adjacency data enabling pathfinding algorithms to find routes between walkable faces
- **Collision Detection**: The engine uses walkmeshes to prevent characters from walking through walls, objects, and impassable terrain
- **Spatial Queries**: AABB trees enable efficient ray casting (mouse clicks, projectiles) and point-in-triangle tests (determining which face a character stands on)
- **Area Transitions**: Edge transitions link walkmeshes to door connections and area boundaries, enabling seamless movement between rooms

**Related formats:** BWM files are used in conjunction with:
- [GFF ARE files](GFF-File-Format#are-area) which define area properties and contain references to walkmesh files.
- [LYT](LYT-File-Format) files that position rooms (WOK per room)
- [Area MDL Models](MDL-MDX-File-Format) that contain embedded walkmesh/AABB data used for camera collision and related spatial queries

See also: [Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation) for coordinate handling and traversal behavior.

---

This document describes the KotOR BWM file format: on-disk layout, data types, and how the engine uses the data for pathfinding, collision, and transitions.

### See also

- [GFF-ARE](GFF-ARE) - Area files that reference WOK/PWK/DWK walkmeshes
- [LYT File Format](LYT-File-Format) - Layout files that position rooms (WOK per room)
- [VIS File Format](VIS-File-Format) - Visibility graph used with area walkmeshes
- [Indoor Map Builder Implementation Guide](Indoor-Map-Builder-Implementation-Guide) - Generates and processes BWM files
- [Game Engine BWM/AABB Implementation](Game-Engine-BWM-AABB-Implementation) - Coordinate handling and AABB traversal
- [2DA-surfacemat](2DA-surfacemat) - Material IDs and walkability

