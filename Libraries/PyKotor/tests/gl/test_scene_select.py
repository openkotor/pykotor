"""Tests for Scene.select: GITObject resolution and selection list behavior."""

from __future__ import annotations

import unittest
from types import MethodType

try:
    from pykotor.gl.scene import RenderObject
    from pykotor.gl.scene.scene import Scene
    from pykotor.resource.generics.git import GITWaypoint
except ImportError:
    import pytest

    pytest.skip("pykotor.gl.scene or git generics not available", allow_module_level=True)


class _SceneSelectStub:
    """Minimal scene stand-in: ``Scene()`` compiles shaders and needs a GL context.

    Binding the real ``Scene.select`` implementation exercises production logic
    (GITObject → RenderObject resolution) without headless shader validation failures.
    """

    def __init__(self) -> None:
        self.objects: dict[object, RenderObject] = {}
        self.selection: list[RenderObject] = []
        self._module = None  # SceneCache.build_cache returns immediately


class TestSceneSelect(unittest.TestCase):
    """Regression: select() accepts GITObject and resolves to the matching RenderObject."""

    def setUp(self):
        self.stub = _SceneSelectStub()
        self._select = MethodType(Scene.select, self.stub)
        self.waypoint_git = GITWaypoint(1.0, 2.0, 3.0)
        self.ro = RenderObject("waypoint", data=self.waypoint_git)
        self.stub.objects[self.waypoint_git] = self.ro

    def test_select_git_object_resolves_render_object(self):
        self.stub.selection.append(RenderObject("cursor"))
        self._select(self.waypoint_git, clear_existing=True)

        self.assertEqual(len(self.stub.selection), 1)
        self.assertIs(self.stub.selection[0], self.ro)

    def test_select_render_object_without_clear_appends(self):
        self._select(self.ro, clear_existing=True)
        other = RenderObject("waypoint")
        self._select(other, clear_existing=False)

        self.assertEqual(len(self.stub.selection), 2)
        self.assertIn(self.ro, self.stub.selection)
        self.assertIn(other, self.stub.selection)

    def test_select_unknown_git_leaves_selection_empty_when_clearing(self):
        orphan = GITWaypoint(9.0, 9.0, 9.0)
        self._select(orphan, clear_existing=True)

        self.assertEqual(len(self.stub.selection), 0)


if __name__ == "__main__":
    unittest.main()
