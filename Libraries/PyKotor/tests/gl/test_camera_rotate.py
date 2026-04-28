"""Tests for Camera.rotate angle wrapping and pitch clamping.

Orbit-style rotation must keep yaw in [-pi, pi] and clamp or wrap pitch
depending on ``clamp``; regressions here break editor camera stability.

``pykotor.gl.scene`` pulls in the full resource stack; load ``camera.py``
directly after ``pykotor.gl`` so these tests run in minimal environments.
"""

from __future__ import annotations

import importlib.util
import math
import unittest
from pathlib import Path

import pytest

# PyGLM-backed vector/matrix types required by camera.py
try:
    import pykotor.gl  # noqa: F401
except ImportError:
    pytest.skip("pykotor.gl not available", allow_module_level=True)


def _camera_module():
    src = (
        Path(__file__).resolve().parents[2] / "src" / "pykotor" / "gl" / "scene" / "camera.py"
    )
    spec = importlib.util.spec_from_file_location("pykotor.gl.scene.camera_test_load", src)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load camera module from {src}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_camera = _camera_module()
Camera = _camera.Camera


class TestCameraRotate(unittest.TestCase):
    """Regression tests for Camera.rotate (yaw wrap, pitch clamp/wrap)."""

    def setUp(self) -> None:
        self.camera = Camera()
        self.camera.yaw = 0.0
        self.camera.pitch = math.pi / 2

    def test_yaw_wraps_to_neg_pi_pi_range(self) -> None:
        """Large yaw deltas must normalize to [-pi, pi]."""
        self.camera.rotate(yaw=3 * math.pi, pitch=0.0)
        self.assertGreater(self.camera.yaw, -math.pi - 1e-9)
        self.assertLess(self.camera.yaw, math.pi + 1e-9)
        self.assertAlmostEqual(abs(self.camera.yaw), math.pi, places=5)

    def test_pitch_wraps_when_clamp_false(self) -> None:
        """Without clamp, pitch uses the same wrap as yaw."""
        self.camera.rotate(yaw=0.0, pitch=2.5 * math.pi, clamp=False)
        self.assertGreater(self.camera.pitch, -math.pi - 1e-9)
        self.assertLess(self.camera.pitch, math.pi + 1e-9)

    def test_pitch_clamped_below_upper_with_default_limits(self) -> None:
        """Orbit clamp keeps pitch inside (lower+eps, upper-eps)."""
        self.camera.pitch = math.pi / 2
        self.camera.rotate(yaw=0.0, pitch=10.0, clamp=True)
        self.assertLess(self.camera.pitch, math.pi - 0.005)
        self.assertGreater(self.camera.pitch, 0.005)

    def test_pitch_clamped_when_limits_almost_coincide(self) -> None:
        """If limits are tighter than 2*orbit_epsilon, both clamp edges meet at midpoint."""
        lo, hi = 0.5, 0.51
        self.camera.pitch = 0.25
        self.camera.rotate(yaw=0.0, pitch=0.0, clamp=True, lower_limit=lo, upper_limit=hi)
        mid = (lo + hi) * 0.5
        self.assertAlmostEqual(self.camera.pitch, mid, places=10)
