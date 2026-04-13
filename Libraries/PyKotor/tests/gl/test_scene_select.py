"""Tests for Scene.select resolving GIT instances to RenderObjects."""

from __future__ import annotations

import unittest

from utility.common.geometry import Vector3

try:
    from pykotor.gl.scene.render_object import RenderObject
    from pykotor.gl.scene.scene import Scene
    from pykotor.resource.generics.git import GITWaypoint
except ImportError:
    import pytest

    pytest.skip("pykotor.gl not available", allow_module_level=True)


class TestSceneSelect(unittest.TestCase):
    """Scene.select accepts GITObject and finds the matching scene RenderObject."""

    def setUp(self):
        self.scene = Scene()
        self.waypoint = GITWaypoint(1.0, 2.0, 3.0)
        self.render_obj = RenderObject("waypoint", Vector3(), data=self.waypoint)
        self.other = RenderObject("waypoint", Vector3(9, 9, 9), data=GITWaypoint(4.0, 5.0, 6.0))

    def test_select_git_resolves_to_render_object(self):
        self.scene.objects[self.waypoint] = self.render_obj
        self.scene.selection.append(self.other)

        self.scene.select(self.waypoint, clear_existing=True)

        self.assertEqual(self.scene.selection, [self.render_obj])

    def test_select_git_without_render_object_leaves_selection_empty(self):
        self.scene.objects.clear()
        self.scene.select(self.waypoint, clear_existing=True)
        self.assertEqual(self.scene.selection, [])

    def test_select_git_append_without_clear_keeps_prior_selection(self):
        self.scene.objects[self.waypoint] = self.render_obj
        self.scene.selection.append(self.other)

        self.scene.select(self.waypoint, clear_existing=False)

        self.assertIn(self.other, self.scene.selection)
        self.assertIn(self.render_obj, self.scene.selection)
        self.assertEqual(len(self.scene.selection), 2)

    def test_select_render_object_direct(self):
        self.scene.objects[self.waypoint] = self.render_obj
        self.scene.select(self.render_obj, clear_existing=True)
        self.assertEqual(self.scene.selection, [self.render_obj])


if __name__ == "__main__":
    unittest.main()
