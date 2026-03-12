"""Archive operations: list_archive, extract_resource (and search_archive)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp import types

from pykotor.extract.installation import SearchLocation
from pykotor.resource.type import ResourceType
from pykotor.tools.archives import list_bif, list_erf, list_key, list_rim
from pykotor.tools.finder import canonical_search_order

from kotormcp.schemas.inputs import ExtractResourceInput, ListArchiveInput
from kotormcp.state import load_installation, resolve_game
from kotormcp.utils.formatting import json_content


def get_tools() -> list[types.Tool]:
    """Return tool definitions for archive operations."""
    return [
        types.Tool(
            name="kotor_list_archive",
            description="List contents of any KEY/BIF/RIM/ERF/MOD with pagination. Read-only.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to archive file"},
                    "key_file": {"type": "string", "description": "Path to KEY file (for BIF listing)"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 500, "default": 50},
                    "offset": {"type": "integer", "minimum": 0, "default": 0},
                },
                "required": ["file_path"],
            },
        ),
        types.Tool(
            name="kotor_extract_resource",
            description="Extract a resource from the installation to a target path (resolution order). Writes to disk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {"type": "string"},
                    "resref": {"type": "string"},
                    "restype": {"type": "string"},
                    "output_path": {"type": "string"},
                },
                "required": ["game", "resref", "restype", "output_path"],
            },
        ),
    ]


def _parse_restype(restype_str: str) -> ResourceType:
    """Parse restype string to ResourceType."""
    ext = restype_str.strip().lstrip(".").lower()
    return ResourceType.from_extension(ext)


async def handle_list_archive(arguments: dict[str, Any]) -> types.CallToolResult:
    """List archive contents with pagination."""
    inp = ListArchiveInput.model_validate(arguments)
    path = Path(inp.file_path)
    if not path.exists():
        raise ValueError(f"Archive file not found: {path}")
    suffix = path.suffix.lower()
    items: list[dict[str, Any]] = []
    if suffix == ".key":
        bif_files, resources = list_key(path)
        for resref, restype_ext, bif_index, res_index in resources:
            items.append({
                "resref": resref,
                "type": restype_ext,
                "bif_index": bif_index,
                "res_index": res_index,
                "bif_file": bif_files[bif_index] if bif_index < len(bif_files) else None,
            })
    elif suffix == ".bif":
        key_path = Path(inp.key_file) if inp.key_file else path.parent / "chitin.key"
        for ar in list_bif(path, key_path=key_path if key_path.exists() else None):
            items.append({"resref": str(ar.resref), "type": ar.restype.extension, "size": ar.size})
    elif suffix in (".rim",):
        for ar in list_rim(path):
            items.append({"resref": str(ar.resref), "type": ar.restype.extension, "size": ar.size})
    elif suffix in (".erf", ".mod", ".sav", ".hak"):
        for ar in list_erf(path):
            items.append({"resref": str(ar.resref), "type": ar.restype.extension, "size": ar.size})
    else:
        raise ValueError(f"Unsupported archive type: {suffix}. Use .key, .bif, .rim, .erf, .mod, .sav, .hak")
    total = len(items)
    offset = inp.offset
    limit = inp.limit
    page = items[offset : offset + limit]
    has_more = total > offset + limit
    next_offset = offset + len(page) if has_more else None
    return json_content({
        "total": total,
        "count": len(page),
        "offset": offset,
        "items": page,
        "has_more": has_more,
        "next_offset": next_offset,
    })


async def handle_extract_resource(arguments: dict[str, Any]) -> types.CallToolResult:
    """Extract resource from installation to output path (resolution order)."""
    inp = ExtractResourceInput.model_validate(arguments)
    game = resolve_game(inp.game)
    if game is None:
        raise ValueError("Specify game (k1/k2).")
    installation = load_installation(game)
    order = canonical_search_order()
    restype = _parse_restype(inp.restype)
    if restype == ResourceType.INVALID:
        raise ValueError(f"Unknown resource type: {inp.restype}")
    result = installation.resource(inp.resref, restype, order=order)
    if result is None:
        raise ValueError(f"Resource {inp.resref}.{restype.extension} not found.")
    out_path = Path(inp.output_path)
    if out_path.suffix.lower() != f".{restype.extension}":
        out_path = out_path / f"{inp.resref}.{restype.extension}" if out_path.is_dir() else out_path.with_suffix(f".{restype.extension}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(result.data)
    return json_content({"status": "ok", "path": str(out_path), "bytes": len(result.data)})

