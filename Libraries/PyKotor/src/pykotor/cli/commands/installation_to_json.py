"""Export all resources from a KotOR installation to JSON files."""

from __future__ import annotations

import base64
import json
import shutil

from pathlib import Path
from typing import TYPE_CHECKING

from pykotor.cli.commands.format_convert import resource_data_to_json_bytes
from pykotor.cli.commands.get_cmd import _resolve_installation_path
from pykotor.extract.file import FileResource, clear_file_data_cache
from pykotor.extract.installation import Installation

if TYPE_CHECKING:
    from argparse import Namespace

    from loggerplus import RobustLogger as Logger


def _iter_stream_resources(installation: Installation) -> list[FileResource]:
    resources: list[FileResource] = []
    for path_getter in (
        installation.streammusic_path,
        installation.streamsounds_path,
        installation.streamvoice_path,
    ):
        try:
            folder_path = path_getter()
        except Exception:
            continue
        if not folder_path.exists():
            continue
        for file_path in folder_path.rglob("*"):
            if file_path.is_file():
                resources.append(FileResource.from_path(file_path))
    return resources


def _iter_all_installation_resources(installation: Installation, logger: Logger) -> list[FileResource]:
    resources: list[FileResource] = []
    seen: set[tuple[str, int, int, str, str]] = set()

    def add(resource: FileResource) -> None:
        key = (
            str(resource.filepath()),
            resource.offset(),
            resource.size(),
            resource.resname().lower(),
            resource.restype().extension.lower() if resource.restype().extension else resource.restype().name.lower(),
        )
        if key in seen:
            return
        seen.add(key)
        resources.append(resource)

    root_tlk = installation.path() / "dialog.tlk"
    if root_tlk.is_file():
        add(FileResource.from_path(root_tlk))
    root_tlk_f = installation.path() / "dialogf.tlk"
    if root_tlk_f.is_file():
        add(FileResource.from_path(root_tlk_f))

    try:
        for resource in installation.override_resources():
            add(resource)
    except Exception as exc:
        logger.warning("Skipping override resources: %s: %s", exc.__class__.__name__, exc)

    try:
        for module_name in installation.modules_list():
            for resource in installation.module_resources(module_name):
                add(resource)
    except Exception as exc:
        logger.warning("Skipping module resources: %s: %s", exc.__class__.__name__, exc)

    try:
        for lip_name in installation.lips_list():
            for resource in installation.lip_resources(lip_name):
                add(resource)
    except Exception as exc:
        logger.warning("Skipping lip resources: %s: %s", exc.__class__.__name__, exc)

    try:
        for texturepack_name in installation.texturepacks_list():
            for resource in installation.texturepack_resources(texturepack_name):
                add(resource)
    except Exception as exc:
        logger.warning("Skipping texturepack resources: %s: %s", exc.__class__.__name__, exc)

    try:
        for resource in installation.core_resources():
            add(resource)
    except Exception as exc:
        logger.warning("Skipping core resources: %s: %s", exc.__class__.__name__, exc)

    try:
        for resource in _iter_stream_resources(installation):
            add(resource)
    except Exception as exc:
        logger.warning("Skipping stream resources: %s: %s", exc.__class__.__name__, exc)

    return resources


def _resource_output_path(output_root: Path, installation_path: Path, resource: FileResource) -> Path:
    filepath = Path(resource.filepath())
    try:
        relative_source = filepath.relative_to(installation_path)
    except ValueError:
        relative_source = Path(filepath.name)

    target_path = relative_source / resource.filename() if (resource.inside_capsule or resource.inside_bif) else relative_source
    return output_root / target_path.with_suffix(f"{target_path.suffix}.json" if target_path.suffix else ".json")


def _build_fallback_payload(installation_path: Path, resource: FileResource, data: bytes) -> bytes:
    filepath = Path(resource.filepath())
    try:
        relative_source = filepath.relative_to(installation_path)
    except ValueError:
        relative_source = Path(filepath.name)

    payload = {
        "resource": resource.filename(),
        "resname": resource.resname(),
        "restype": resource.restype().name,
        "extension": resource.restype().extension,
        "source_path": relative_source.as_posix(),
        "container_path": relative_source.as_posix() if (resource.inside_capsule or resource.inside_bif) else None,
        "offset": resource.offset(),
        "size": len(data),
        "encoding": "base64",
        "data_base64": base64.b64encode(data).decode("ascii"),
    }
    return json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"


def cmd_installation_to_json(args: Namespace, logger: Logger) -> int:
    installation_path = _resolve_installation_path(args, logger)
    if installation_path is None:
        return 1

    output_root = Path(getattr(args, "output", "installation-json")).resolve()
    if getattr(args, "clean", False) and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    try:
        installation = Installation(installation_path)
    except Exception:
        logger.exception("Invalid installation path")
        return 1

    resources = _iter_all_installation_resources(installation, logger)
    total_resources = len(resources)
    logger.info("Exporting %s resource(s) from %s to %s", total_resources, installation_path, output_root)

    supported_count = 0
    fallback_count = 0
    error_count = 0

    for index, resource in enumerate(resources, start=1):
        destination = _resource_output_path(output_root, Path(installation_path), resource)
        destination.parent.mkdir(parents=True, exist_ok=True)

        try:
            data = resource.data()
            try:
                json_bytes = resource_data_to_json_bytes(data, resource.restype())
                supported_count += 1
            except ValueError:
                json_bytes = _build_fallback_payload(Path(installation_path), resource, data)
                fallback_count += 1
            destination.write_bytes(json_bytes)
        except Exception as exc:
            error_count += 1
            error_payload = {
                "resource": resource.filename(),
                "source_path": str(resource.filepath()),
                "error": f"{exc.__class__.__name__}: {exc}",
            }
            destination.write_text(json.dumps(error_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        if index % 500 == 0 or index == total_resources:
            logger.info(
                "Processed %s/%s resources (%s supported, %s fallback, %s errors)",
                index,
                total_resources,
                supported_count,
                fallback_count,
                error_count,
            )
            clear_file_data_cache()

    logger.info(
        "Installation export complete: %s supported JSON, %s fallback JSON, %s error JSON",
        supported_count,
        fallback_count,
        error_count,
    )
    return 0 if error_count == 0 else 2