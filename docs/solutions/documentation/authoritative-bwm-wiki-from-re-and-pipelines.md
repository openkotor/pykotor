---
title: Authoritative BWM Wiki from RE and Pipelines
problem_type: documentation
component: wiki, BWM, walkmesh, Odyssey engine
symptoms: |
  wiki/BWM-File-Format.md was a short stub with no binary layout, no data conventions,
  and no single authoritative source. Format details were scattered across RE notes,
  community tooling, and in-repo implementation, leading to confusion for tooling
  and room transition workflows.
root_cause: |
  No single document defined the Odyssey BWM format from engine and community sources
  only. The plan explicitly excluded in-repo PyKotor implementation as authoritative
  to avoid circular reliance and to ground the spec in reverse engineering and
  vendor/community pipelines.
solution: |
  Produced wiki/BWM-File-Format.md as the single BWM reference: 136-byte header table,
  data types (little-endian), vertices, faces, materials, normals, distances, AABB
  tree (44-byte nodes, 0-based indices), adjacencies (face*3+edge), edges (8 bytes),
  perimeters (1-based loop ends). WOK vs PWK vs DWK, world_coords (0x08), transitions
  (LYT room index), authoring (KOTORMax primary for roomlinks, kotorblender,
  kaurora). docs/walkmesh.md now points only to the wiki. Game-Engine-BWM-AABB-
  Implementation.md references the BWM wiki as format spec and no longer cites
  PyKotor in References.
prevention: |
  Keep BWM-File-Format.md as the canonical format doc; cite only RE (vendor/swkotor)
  and community pipelines (KOTORMax, kotorblender, kaurora). Do not add PyKotor
  implementation links to the BWM wiki or the Game-Engine BWM doc References.
related_docs: |
  wiki/BWM-File-Format.md, wiki/Game-Engine-BWM-AABB-Implementation.md,
  docs/walkmesh.md, Area-Modding-and-Room-Transitions, Indoor-Map-Builder-Implementation-Guide
category: documentation
---

# Authoritative BWM Wiki from RE and Pipelines

This solution documents how the single authoritative BWM format page for the Odyssey engine (KotOR 1 and 2) was created using only reverse-engineered engine behavior and community tooling—without citing the in-repo PyKotor BWM implementation.

---

## Problem

- **wiki/BWM-File-Format.md** was a stub (~46 lines): types (WOK/PWK/DWK), purpose, related formats, and See also. It did not define binary layout, header offsets, data conventions, or engine behavior.
- Binary layout and engine behavior lived in **Game-Engine-BWM-AABB-Implementation.md** (RE) and in community context (KOTORMax, kotorblender, kaurora). Room transition and “can’t cross between rooms” issues were hard to debug because there was no single place describing format, `world_coords`, transition IDs, and authoring workflows.
- The plan required the BWM doc to **not** reference PyKotor code so the format spec is defined by the engine and pipelines only.

---

## Sources Used

| Source | Role |
|--------|------|
| **Game-Engine-BWM-AABB-Implementation.md** | Reverse-engineered engine (vendor/swkotor.c, vendor/swkotor.h): 136-byte header, `world_coords` at 0x08, AABB 44-byte nodes, 0-based indices, adjacency encoding, edges (8 bytes), perimeters (1-based). |
| **bwm_mdl_lyt_kotormax_context.md** | KOTORMax workflow: Export WOK, Room Linker, LYT/VIS, .mdl.ascii, Area Tools vs MDL Loading, door DWK; kotorblender gaps for room transitions. |
| **xoreos pathfinding wiki** | Walkmesh as nav mesh, A* and SSFA, face adjacency, relation to surfacemat.2da. |
| **NWN (nwn.fandom, nwn.wiki)** | .wok/.pwk/.dwk roles, 2.5D height mesh, surfacemat.2da; Odyssey is Aurora-derived. |
| **KOTORMax (GitHub, Deadly Stream)** | Room Linker, LYT/VIS, Export WOK, wokmat.ini, filename conventions. |
| **kotorblender** | WOK/PWK/DWK import/export; room linking on edges; community guidance that KOTORMax is preferred for room transitions. |
| **kaurora** | WOK import/export, room adjacency editing. |
| **reone / KotOR.js / xoreos-docs** | Checked for BWM readers; plan noted no dedicated BWM parser in these codebases for the format spec. |

---

## Outcome

- **wiki/BWM-File-Format.md** is the single authoritative BWM reference: opening (what BWM is, WOK/PWK/DWK), data types and conventions (little-endian, 136-byte header), full binary layout (header table with offsets, vertices, faces, materials, normals, distances, AABB tree, adjacencies, edges, perimeters), WOK vs PWK vs DWK, transitions and door placement, related formats, and authoring (KOTORMax primary for roomlinks, kotorblender, kaurora). Includes a concise summary of the “can’t cross between rooms” / roomlink confusion for future readers.
- **docs/walkmesh.md** points only to the wiki BWM page; no PyKotor implementation notes there.
- **wiki/Game-Engine-BWM-AABB-Implementation.md** References section now points to BWM-File-Format as the format spec and no longer lists PyKotor paths.

---

## References

- [BWM-File-Format](../../../wiki/BWM-File-Format.md)
- [Game-Engine-BWM-AABB-Implementation](../../../wiki/Game-Engine-BWM-AABB-Implementation.md)
- [Area-Modding-and-Room-Transitions](../../../wiki/Area-Modding-and-Room-Transitions.md)
- [Indoor-Map-Builder-Implementation-Guide](../../../wiki/Indoor-Map-Builder-Implementation-Guide.md)
