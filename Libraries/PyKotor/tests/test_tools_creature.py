from __future__ import annotations

import pathlib
import sys
import unittest

from types import SimpleNamespace

THIS_SCRIPT_PATH = pathlib.Path(__file__).resolve()
PYKOTOR_PATH = THIS_SCRIPT_PATH.parents[2].joinpath("src")
UTILITY_PATH = THIS_SCRIPT_PATH.parents[4].joinpath("Libraries", "Utility", "src")


def add_sys_path(p: pathlib.Path):
    working_dir = str(p)
    if working_dir not in sys.path:
        sys.path.append(working_dir)


if PYKOTOR_PATH.joinpath("pykotor").exists():
    add_sys_path(PYKOTOR_PATH)
if UTILITY_PATH.joinpath("utility").exists():
    add_sys_path(UTILITY_PATH)

from pykotor.resource.formats.twoda import TwoDA
from pykotor.tools.creature import get_body_model


class TestGetBodyModel(unittest.TestCase):
    @staticmethod
    def _dummy_installation(name: str = "Test Creature") -> SimpleNamespace:
        return SimpleNamespace(
            string=lambda _: name,
            texture=lambda _: None,
        )

    @staticmethod
    def _dummy_baseitems() -> TwoDA:
        baseitems = TwoDA(["bodyvar", "defaultmodel"])
        baseitems.add_row("0", {"bodyvar": "a", "defaultmodel": "n_dummy"})
        return baseitems

    def test_falls_back_to_modela_when_race_is_empty(self):
        appearance = TwoDA(["modeltype", "race", "modela", "texa", "texaevil"])
        appearance.add_row(
            "0",
            {
                "modeltype": "",
                "race": "",
                "modela": "n_boma",
                "texa": "n_boma01",
                "texaevil": "n_bomaevil01",
            },
        )
        utc = SimpleNamespace(
            first_name=0,
            appearance_id=0,
            alignment=50,
            equipment={},
        )

        body_model, body_texture = get_body_model(
            utc,
            self._dummy_installation("Young Boma"),
            appearance=appearance,
            baseitems=self._dummy_baseitems(),
        )

        self.assertEqual(body_model, "n_boma")
        self.assertEqual(body_texture, "n_boma01")

    def test_falls_back_to_unknown_when_no_body_model_columns_resolve(self):
        appearance = TwoDA(["modeltype", "race", "modela", "texa", "texaevil"])
        appearance.add_row(
            "0",
            {
                "modeltype": "",
                "race": "",
                "modela": "",
                "texa": "",
                "texaevil": "",
            },
        )
        utc = SimpleNamespace(
            first_name=0,
            appearance_id=0,
            alignment=50,
            equipment={},
        )

        body_model, body_texture = get_body_model(
            utc,
            self._dummy_installation(),
            appearance=appearance,
            baseitems=self._dummy_baseitems(),
        )

        self.assertEqual(body_model, "unknown")
        self.assertIsNone(body_texture)


if __name__ == "__main__":
    unittest.main()
