"""GL scene package: camera, render objects, frustum culling, and module designer scene."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pykotor.gl.scene.camera import Camera
from pykotor.gl.scene.frustum import CullingStats, Frustum
from pykotor.gl.models.mdl import Boundary
from pykotor.gl.scene.render_object import RenderObject

if TYPE_CHECKING:
    from pykotor.gl.scene.scene import Scene

__all__ = ["Boundary", "Camera", "CullingStats", "Frustum", "RenderObject", "Scene"]


def __getattr__(name: str) -> Any:
    """Lazy-load Scene so `import pykotor.gl.scene.camera` avoids heavy PyOpenGL/install deps."""
    if name == "Scene":
        from pykotor.gl.scene.scene import Scene as _Scene

        globals()["Scene"] = _Scene
        return _Scene
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
