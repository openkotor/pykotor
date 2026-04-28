"""Regression tests for camera angle wrapping (orbit / free-rotate paths)."""

from __future__ import annotations

import math
import unittest

try:
    from pykotor.gl.scene.camera import Camera, _wrap_angle_pi
except ImportError:
    import pytest

    pytest.skip("pykotor.gl not available", allow_module_level=True)


class TestWrapAnglePi(unittest.TestCase):
    """_wrap_angle_pi must keep angles in (-pi, pi] for stable comparisons."""

    def test_zero_and_small_angles_unchanged(self):
        self.assertAlmostEqual(_wrap_angle_pi(0.0), 0.0)
        self.assertAlmostEqual(_wrap_angle_pi(0.25), 0.25)
        self.assertAlmostEqual(_wrap_angle_pi(-0.5), -0.5)

    def test_pi_boundary(self):
        # pi maps to -pi (equivalent direction, canonical range endpoint)
        self.assertAlmostEqual(_wrap_angle_pi(math.pi), -math.pi)

    def test_wraps_positive_overflow(self):
        self.assertAlmostEqual(_wrap_angle_pi(3 * math.pi), -math.pi)
        self.assertAlmostEqual(_wrap_angle_pi(2 * math.pi + 0.1), 0.1, places=5)

    def test_wraps_negative_overflow(self):
        # Same direction as +pi; canonical endpoint is -pi for this input
        self.assertAlmostEqual(_wrap_angle_pi(-3 * math.pi), -math.pi)
        self.assertAlmostEqual(_wrap_angle_pi(-2 * math.pi - 0.2), -0.2, places=5)


class TestCameraRotateWrapping(unittest.TestCase):
    """Camera.rotate must not drift yaw/pitch out of a stable range."""

    def test_rotate_yaw_wraps_large_positive_delta(self):
        cam = Camera(yaw=0.0, pitch=math.pi / 2)
        cam.rotate(yaw=4 * math.pi, pitch=0.0, clamp=False)
        self.assertAlmostEqual(cam.yaw, 0.0, places=5)

    def test_rotate_yaw_wraps_large_negative_delta(self):
        cam = Camera(yaw=0.0, pitch=math.pi / 2)
        cam.rotate(yaw=-4 * math.pi, pitch=0.0, clamp=False)
        self.assertAlmostEqual(cam.yaw, 0.0, places=5)

    def test_rotate_pitch_wraps_when_not_clamped(self):
        cam = Camera(yaw=0.0, pitch=math.pi / 2)
        cam.rotate(yaw=0.0, pitch=10 * math.pi, clamp=False)
        self.assertAlmostEqual(cam.pitch, math.pi / 2, places=5)

    def test_rotate_clamp_collapsed_limits_snaps_to_mid_pitch(self):
        """When lower_limit >= upper_limit after epsilon, both clamp to midpoint."""
        cam = Camera(yaw=0.0, pitch=math.pi / 2)
        cam.rotate(
            yaw=0.0,
            pitch=0.5,
            clamp=True,
            lower_limit=math.pi / 2,
            upper_limit=math.pi / 2,
        )
        self.assertAlmostEqual(cam.pitch, math.pi / 2, places=5)


if __name__ == "__main__":
    unittest.main()
