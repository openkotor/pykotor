from __future__ import annotations

import pathlib
import shutil
import sys
import tempfile
import unittest

from unittest import TestCase

THIS_SCRIPT_PATH = pathlib.Path(__file__).resolve()
PYKOTOR_PATH = THIS_SCRIPT_PATH.parents[3].joinpath("src")
UTILITY_PATH = THIS_SCRIPT_PATH.parents[5].joinpath("Libraries", "Utility", "src")


def add_sys_path(p: pathlib.Path):
    working_dir = str(p)
    if working_dir not in sys.path:
        sys.path.append(working_dir)


if PYKOTOR_PATH.joinpath("pykotor").exists():
    add_sys_path(PYKOTOR_PATH)
if UTILITY_PATH.joinpath("utility").exists():
    add_sys_path(UTILITY_PATH)

from pykotor.extract.capsule import Capsule
from pykotor.resource.type import ResourceType

TEST_ERF_FILE = "Libraries/PyKotor/tests/test_files/capsule.mod"
TEST_RIM_FILE = "Libraries/PyKotor/tests/test_files/capsule.rim"


class TestCapsule(TestCase):
    def _assert_existing_resources(
        self, capsule: Capsule, resources: list[tuple[str, ResourceType, int]]
    ):
        for resource_name, resource_type, expected_length in resources:
            with self.subTest(resource_name=resource_name, resource_type=resource_type.name):
                assert capsule.contains(resource_name, resource_type, reload=True)
                resource = capsule.resource(resource_name, resource_type)
                assert len(resource) == expected_length
                assert resource[:4].decode() == f"{resource_type.extension.upper():<4}"[:4]

    def test_add_to_capsule_file(self):
        cases = [
            (
                TEST_RIM_FILE,
                "capsule.rim",
                "image",
                ResourceType.PNG,
                b"image data",
                [
                    ("m13aa", ResourceType.ARE, 4096),
                    ("m13aa", ResourceType.GIT, 51747),
                    ("module", ResourceType.IFO, 1655),
                ],
            ),
            (
                TEST_ERF_FILE,
                "capsule.mod",
                "sound",
                ResourceType.WAV,
                b"sound data",
                [
                    ("001ebo", ResourceType.ARE, 4865),
                    ("001ebo", ResourceType.GIT, 42565),
                    ("001ebo", ResourceType.PTH, 19788),
                ],
            ),
        ]

        for source_path, temp_name, resource_name, resource_type, resource_data, resources in cases:
            with self.subTest(source_path=source_path, resource_type=resource_type.name):
                with tempfile.TemporaryDirectory() as tmpdirname:
                    temp_capsule_path = pathlib.Path(tmpdirname).joinpath(temp_name)
                    shutil.copy(source_path, temp_capsule_path)

                    capsule = Capsule(temp_capsule_path)
                    capsule.add(resource_name, resource_type, resource_data)

                    assert len(capsule) == 4
                    self._assert_existing_resources(capsule, resources)

                    assert capsule.contains(resource_name, resource_type, reload=True)
                    assert capsule.resource(resource_name, resource_type) == resource_data

    def test_existing_capsule_contents(self):
        cases = [
            (
                TEST_ERF_FILE,
                [
                    ("001ebo", ResourceType.ARE, 4865),
                    ("001ebo", ResourceType.GIT, 42565),
                    ("001ebo", ResourceType.PTH, 19788),
                ],
            ),
            (
                TEST_RIM_FILE,
                [
                    ("m13aa", ResourceType.ARE, 4096),
                    ("m13aa", ResourceType.GIT, 51747),
                    ("module", ResourceType.IFO, 1655),
                ],
            ),
        ]

        for source_path, resources in cases:
            with self.subTest(source_path=source_path):
                capsule = Capsule(source_path)
                assert len(capsule) == 3
                self._assert_existing_resources(capsule, resources)


if __name__ == "__main__":
    unittest.main()
