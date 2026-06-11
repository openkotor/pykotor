"""Unit tests for installation validation utilities (validation.py)."""

from __future__ import annotations

from pathlib import Path

import pytest

from pykotor.common.misc import Game
from pykotor.extract.installation import SearchLocation
from pykotor.resource.type import ResourceType
from pykotor.tools.validation import (
    check_2da_file,
    check_missing_resources_referenced,
    check_txi_files,
    get_installation_summary,
    validate_installation,
)


class _FakeLocation:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath


class FakeInstallation:
    def __init__(self, path: Path, *, locations_map: dict | None = None) -> None:
        self._path = path
        self._locations_map = locations_map or {}

    def path(self) -> Path:
        return self._path

    def locations(self, identifiers, search_locations):  # noqa: ANN001, ARG002
        results: dict = {}
        for ident in identifiers:
            key = (ident.resname, ident.restype)
            if key in self._locations_map:
                results[ident] = self._locations_map[key]
        return results

    def module_path(self) -> Path:
        return self._path / "modules"

    def override_path(self) -> Path:
        return self._path / "override"


class FakeModule:
    def __init__(self, textures: set[str], lightmaps: set[str]) -> None:
        self._textures = textures
        self._lightmaps = lightmaps

    def models(self):
        return []


def test_validate_installation_reports_missing_essential_2das(tmp_path: Path) -> None:
    install = FakeInstallation(tmp_path)
    (tmp_path / "chitin.key").write_bytes(b"")

    result = validate_installation(install)

    assert result["valid"] is False
    assert "appearance.2da" in result["missing_files"]
    assert "baseitems.2da" in result["missing_files"]
    assert result["errors"] == []


def test_validate_installation_passes_when_essential_2das_present(tmp_path: Path) -> None:
    appearance = tmp_path / "appearance.2da"
    baseitems = tmp_path / "baseitems.2da"
    classes = tmp_path / "classes.2da"
    genericdoors = tmp_path / "genericdoors.2da"
    locations_map = {
        ("appearance", ResourceType.TwoDA): [_FakeLocation(appearance)],
        ("baseitems", ResourceType.TwoDA): [_FakeLocation(baseitems)],
        ("classes", ResourceType.TwoDA): [_FakeLocation(classes)],
        ("genericdoors", ResourceType.TwoDA): [_FakeLocation(genericdoors)],
    }
    install = FakeInstallation(tmp_path, locations_map=locations_map)

    result = validate_installation(install)

    assert result["valid"] is True
    assert result["missing_files"] == []
    assert result["errors"] == []


def test_validate_installation_reports_missing_install_path(tmp_path: Path) -> None:
    missing = tmp_path / "gone"
    install = FakeInstallation(missing)

    result = validate_installation(install, check_essential_files=False)

    assert result["valid"] is False
    assert any("does not exist" in err for err in result["errors"])


def test_check_txi_files_returns_paths_per_texture(tmp_path: Path) -> None:
    txi_path = tmp_path / "override" / "lda_bark04.txi"
    txi_path.parent.mkdir(parents=True)
    txi_path.write_text("upperleft 0 0", encoding="utf-8")
    locations_map = {
        ("lda_bark04", ResourceType.TXI): [_FakeLocation(txi_path)],
        ("missing_tex", ResourceType.TXI): [],
    }
    install = FakeInstallation(tmp_path, locations_map=locations_map)

    results = check_txi_files(
        install,
        ["lda_bark04", "missing_tex"],
        search_locations=[SearchLocation.OVERRIDE],
    )

    assert results["lda_bark04"] == [txi_path]
    assert results["missing_tex"] == []


def test_check_2da_file_found_and_not_found(tmp_path: Path) -> None:
    twoda_path = tmp_path / "genericdoors.2da"
    twoda_path.write_text("2DA V2.0\n", encoding="utf-8")
    locations_map = {
        ("genericdoors", ResourceType.TwoDA): [_FakeLocation(twoda_path)],
        ("missing", ResourceType.TwoDA): [],
    }
    install = FakeInstallation(tmp_path, locations_map=locations_map)

    found, paths = check_2da_file(install, "genericdoors")
    missing_found, missing_paths = check_2da_file(install, "missing")

    assert found is True
    assert paths == [twoda_path]
    assert missing_found is False
    assert missing_paths == []


def test_check_missing_resources_referenced(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = FakeModule(textures={"lda_bark04"}, lightmaps={"m03af_01a_lm13"})

    def fake_get_module_referenced_resources(mod):  # noqa: ANN001
        assert mod is module
        return module._textures, module._lightmaps

    monkeypatch.setattr(
        "pykotor.tools.validation.get_module_referenced_resources",
        fake_get_module_referenced_resources,
    )

    results = check_missing_resources_referenced(
        module,
        missing_textures=["lda_bark04", "not_used"],
        missing_lightmaps=["m03af_01a_lm13", "absent_lm"],
    )

    assert results["lda_bark04"] is True
    assert results["not_used"] is False
    assert results["m03af_01a_lm13"] is True
    assert results["absent_lm"] is False


def test_get_installation_summary_counts_modules_and_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    modules = tmp_path / "modules"
    override = tmp_path / "override"
    modules.mkdir()
    override.mkdir()
    (modules / "danm13.rim").write_bytes(b"rim")
    (modules / "danm13.mod").write_bytes(b"mod")
    (override / "foo.uti").write_bytes(b"uti")

    appearance = tmp_path / "appearance.2da"
    baseitems = tmp_path / "baseitems.2da"
    classes = tmp_path / "classes.2da"
    genericdoors = tmp_path / "genericdoors.2da"
    locations_map = {
        ("appearance", ResourceType.TwoDA): [_FakeLocation(appearance)],
        ("baseitems", ResourceType.TwoDA): [_FakeLocation(baseitems)],
        ("classes", ResourceType.TwoDA): [_FakeLocation(classes)],
        ("genericdoors", ResourceType.TwoDA): [_FakeLocation(genericdoors)],
    }
    install = FakeInstallation(tmp_path, locations_map=locations_map)

    monkeypatch.setattr(
        "pykotor.extract.installation.Installation.determine_game",
        lambda _path: Game.K1,
    )

    summary = get_installation_summary(install)

    assert summary["path"] == str(tmp_path)
    assert summary["game"] == "K1"
    assert summary["valid"] is True
    assert summary["module_count"] == 2
    assert summary["override_file_count"] == 1
    assert summary["missing"] == []
