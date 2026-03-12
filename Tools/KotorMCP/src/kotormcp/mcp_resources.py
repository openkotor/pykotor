"""MCP resources: kotor:// URI scheme for passive context injection.

URIs:
  kotor://k1/resource/{resref}.{ext}   - Resolved via installation (resolution order)
  kotor://k2/resource/{resref}.{ext}
  kotor://k1/2da/{table_name}          - 2DA table as JSON
  kotor://k2/2da/{table_name}
  kotor://k1/tlk/{strref}              - TLK string by reference
  kotor://k2/tlk/{strref}
  kotor://k1/override/                 - Override directory listing (template)
  kotor://k2/override/
"""

from __future__ import annotations

import base64
import json
from typing import Any
from urllib.parse import unquote

from pykotor.common.misc import Game
from pykotor.resource.type import ResourceType

from kotormcp.state import load_installation, resolve_game


def _game_from_uri_authority(authority: str) -> Game | None:
    """Map URI authority (host) to Game."""
    return resolve_game("k1" if authority == "k1" else "k2" if authority == "k2" else None)


def parse_kotor_uri(uri: str) -> dict[str, Any] | None:
    """Parse kotor:// URI into components. Returns dict with game, type, path, etc. or None if invalid."""
    if not uri.startswith("kotor://"):
        return None
    parts = uri[8:].split("/", 2)  # after "kotor://"
    if len(parts) < 2:
        return None
    authority, resource_type = parts[0].lower(), parts[1].lower()
    path = unquote(parts[2]) if len(parts) > 2 else ""
    game = _game_from_uri_authority(authority)
    if game is None:
        return None
    return {"game": game, "type": resource_type, "path": path, "uri": uri}


async def list_resources() -> list[dict[str, Any]]:
    """Return list of MCP resource templates (kotor:// URIs) for discovery.

    Returns static template URIs; clients request actual content via read_resource.
    """
    templates = [
        {"uri": "kotor://k1/resource/{resref}.{ext}", "name": "K1 Resource", "description": "Resolve resource by resref.ext (resolution order)", "mimeType": "application/octet-stream"},
        {"uri": "kotor://k2/resource/{resref}.{ext}", "name": "K2 Resource", "description": "Resolve resource by resref.ext (resolution order)", "mimeType": "application/octet-stream"},
        {"uri": "kotor://k1/2da/{table_name}", "name": "K1 2DA Table", "description": "2DA table as JSON", "mimeType": "application/json"},
        {"uri": "kotor://k2/2da/{table_name}", "name": "K2 2DA Table", "description": "2DA table as JSON", "mimeType": "application/json"},
        {"uri": "kotor://k1/tlk/{strref}", "name": "K1 TLK String", "description": "TLK string by strref", "mimeType": "text/plain"},
        {"uri": "kotor://k2/tlk/{strref}", "name": "K2 TLK String", "description": "TLK string by strref", "mimeType": "text/plain"},
    ]
    return templates


async def read_resource(uri: str) -> dict[str, Any]:
    """Read kotor:// resource and return content (text or base64 blob)."""
    parsed = parse_kotor_uri(uri)
    if not parsed:
        raise ValueError(f"Invalid kotor:// URI: {uri}")
    game = parsed["game"]
    resource_type = parsed["type"]
    path = parsed["path"]
    installation = load_installation(game)
    if resource_type == "resource":
        # path = resref.ext
        from pykotor.extract.file import ResourceIdentifier
        from pykotor.extract.installation import SearchLocation
        from pykotor.tools.finder import canonical_search_order

        ident = ResourceIdentifier.from_path(path)
        if ident.restype == ResourceType.INVALID:
            raise ValueError(f"Unknown resource type in URI path: {path}")
        order = canonical_search_order()
        result = installation.resource(ident.resname, ident.restype, order=order)
        if result is None:
            raise ValueError(f"Resource not found: {path}")
        return {"uri": uri, "mimeType": "application/octet-stream", "blob": base64.b64encode(result.data).decode("ascii")}
    if resource_type == "2da":
        from io import BytesIO
        from pykotor.extract.installation import SearchLocation
        from pykotor.resource.formats.twoda.twoda_auto import read_2da

        table_name = path.strip() or "appearance"
        order = [SearchLocation.OVERRIDE, SearchLocation.MODULES, SearchLocation.CHITIN]
        result = installation.resource(table_name, ResourceType.TwoDA, order=order)
        if result is None:
            raise ValueError(f"2DA table not found: {table_name}")
        table = read_2da(BytesIO(result.data))
        headers = table.get_headers()
        rows = []
        for i in range(min(table.get_height(), 500)):
            rows.append({h: table.get_cell_safe(i, h, "") for h in headers})
        data = {"columns": headers, "row_count": table.get_height(), "rows": rows}
        return {"uri": uri, "mimeType": "application/json", "text": json.dumps(data, indent=2)}
    if resource_type == "tlk":
        strref = int(path.strip()) if path.strip().isdigit() else -1
        text = installation.talktable().string(strref)
        return {"uri": uri, "mimeType": "text/plain", "text": text}
    raise ValueError(f"Unsupported resource type in URI: {resource_type}")
