"""Merge and generate BWM walkmeshes for v2 tile-based indoor maps."""

from __future__ import annotations

from copy import deepcopy

from pykotor.resource.formats.bwm.bwm_data import BWM, BWMFace, BWMType
from utility.common.geometry import SurfaceMaterial, Vector3


def merge_translated_bwms(sources: list[tuple[BWM, float, float, float]]) -> BWM:
    """Merge multiple BWMs into one area walkmesh, each translated by (tx, ty, tz) in world space.

    Vertices are copied per face to avoid shared-mutation issues. Empty input yields an empty
    area BWM (caller may substitute a generated floor).
    """
    out = BWM()
    out.walkmesh_type = BWMType.AreaModel
    for bwm, tx, ty, tz in sources:
        if not bwm.faces:
            continue
        b = deepcopy(bwm)
        b.translate(tx, ty, tz)
        out.faces.extend(b.faces)
    return out


def generate_flat_floor_quad(
    *,
    min_x: float,
    min_y: float,
    size_x: float,
    size_y: float,
    z: float = 0.0,
    material: SurfaceMaterial = SurfaceMaterial.STONE,
) -> BWM:
    """Two walkable triangles covering an axis-aligned rectangle in the X/Y plane at fixed Z.

    Used when a floor tile has no WOK; coarse stand-in for procedural walkmesh. KotOR area
    walkmeshes are consumed in world space; match your tile compiler's placement convention.
    """
    b = BWM()
    b.walkmesh_type = BWMType.AreaModel
    v0 = Vector3(min_x, min_y, z)
    v1 = Vector3(min_x + size_x, min_y, z)
    v2 = Vector3(min_x + size_x, min_y + size_y, z)
    v3 = Vector3(min_x, min_y + size_y, z)
    f1 = BWMFace(v0, v1, v2)
    f2 = BWMFace(v0, v2, v3)
    f1.material = material
    f2.material = material
    b.faces.append(f1)
    b.faces.append(f2)
    return b
