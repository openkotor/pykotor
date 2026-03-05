"""Runtime smoke tests for the Toolset <-> Blender IPC bridge."""

from __future__ import annotations

import os
import shutil
import time

from pathlib import Path

import pytest

from toolset.blender.detection import detect_blender, install_kotorblender, launch_blender_with_ipc
from toolset.blender.ipc_client import BlenderCommands, BlenderIPCClient


def _resolve_blender_binary() -> Path | None:
    env_value = os.environ.get("BLENDER_BIN")
    if env_value:
        path = Path(env_value).expanduser()
        return path if path.is_file() else None

    workspace_binary = Path("/workspace/.tools/blender-4.2.0/blender")
    if workspace_binary.is_file():
        return workspace_binary

    detected = shutil.which("blender")
    return Path(detected) if detected else None


@pytest.fixture
def blender_runtime_bridge():
    blender_binary = _resolve_blender_binary()
    if blender_binary is None:
        pytest.skip("No Blender runtime available for bridge smoke tests")

    blender_info = detect_blender(custom_path=blender_binary)
    if not blender_info.is_valid:
        pytest.skip(f"Blender runtime is not usable: {blender_info.error}")

    success, message = install_kotorblender(blender_info, verify_ipc=False)
    if not success:
        pytest.skip(f"kotorblender installation failed in test environment: {message}")

    process = launch_blender_with_ipc(
        blender_info,
        ipc_port=7531,
        installation_path="/workspace",
        background=True,
        capture_output=True,
    )
    if process is None:
        pytest.skip("Unable to launch Blender runtime for smoke tests")

    client = BlenderIPCClient(port=7531)
    commands = BlenderCommands(client)

    try:
        for _attempt in range(40):
            if client.connect(timeout=1.0):
                break
            time.sleep(0.25)
        else:
            stdout = ""
            if process.stdout is not None:
                process.terminate()
                stdout = process.communicate(timeout=10)[0]
            pytest.fail(f"Timed out waiting for Blender IPC server.\nStdout:\n{stdout}")

        yield commands
    finally:
        if client.is_connected:
            client.disconnect()
        if process.poll() is None:
            process.terminate()
            process.communicate(timeout=10)


def test_blender_bridge_ping_and_version(blender_runtime_bridge: BlenderCommands):
    assert blender_runtime_bridge.ping() is True
    version_info = blender_runtime_bridge.get_version()
    assert isinstance(version_info, dict)
    assert version_info["kotorblender"] == "4.0.4"
    assert version_info["bridge"] == "holocron-ipc"


def test_blender_bridge_module_roundtrip(blender_runtime_bridge: BlenderCommands):
    room_position = {"x": 0.0, "y": 0.0, "z": 0.0}
    walkmesh_faces = [
        {
            "v1": {"x": -2.0, "y": -2.0, "z": 0.0},
            "v2": {"x": 2.0, "y": -2.0, "z": 0.0},
            "v3": {"x": 2.0, "y": 2.0, "z": 0.0},
            "material": 4,
            "trans1": None,
            "trans2": None,
            "trans3": None,
        },
        {
            "v1": {"x": -2.0, "y": -2.0, "z": 0.0},
            "v2": {"x": 2.0, "y": 2.0, "z": 0.0},
            "v3": {"x": -2.0, "y": 2.0, "z": 0.0},
            "material": 4,
            "trans1": None,
            "trans2": None,
            "trans3": None,
        },
    ]
    instance = {
        "type": "GITCreature",
        "resref": "n_testnpc",
        "position": {"x": 1.0, "y": 0.5, "z": 0.0},
        "bearing": 0.0,
        "runtime_id": 101,
    }

    assert blender_runtime_bridge.load_module(
        lyt_data={"rooms": [{"model": "m_testroom", "position": room_position}], "doorhooks": [], "tracks": [], "obstacles": []},
        git_data={"creatures": [instance], "cameras": [], "doors": [], "placeables": [], "waypoints": [], "sounds": [], "stores": [], "triggers": [], "encounters": []},
        installation_path="/workspace",
        module_root="m_test",
        walkmeshes=[{"model": "m_testroom", "faces": walkmesh_faces}],
    )

    assert blender_runtime_bridge.select_instances(["GITCreature:n_testnpc"]) is True
    assert blender_runtime_bridge.get_selection() == ["GITCreature:n_testnpc"]

    added_name = blender_runtime_bridge.add_instance(
        {
            "type": "GITPlaceable",
            "resref": "plc_test",
            "position": {"x": 2.0, "y": 2.0, "z": 0.0},
            "bearing": 0.25,
            "runtime_id": 202,
        }
    )
    assert added_name == "GITPlaceable:plc_test"
    assert blender_runtime_bridge.update_instance(added_name, {"bearing": 1.0}) is True

    saved = blender_runtime_bridge.save_changes()
    assert isinstance(saved, dict)
    assert saved["lyt"]["rooms"][0]["model"] == "m_testroom"
    assert len(saved["git"]["creatures"]) == 1
    assert len(saved["git"]["placeables"]) == 1

    assert blender_runtime_bridge.remove_instance(added_name) is True
    assert blender_runtime_bridge.unload_module() is True
