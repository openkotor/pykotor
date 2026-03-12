"""Get command: extract a single resource from a KOTOR installation (resolution order)."""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from pykotor.extract.file import ResourceIdentifier
from pykotor.extract.installation import Installation, SearchLocation
from pykotor.tools.finder import canonical_search_order

if TYPE_CHECKING:
    from argparse import Namespace

    from loggerplus import RobustLogger as Logger


def _parse_order_arg(order_str: str | None) -> list[SearchLocation] | None:
    """Parse --order LOC1,LOC2,... into list of SearchLocation."""
    if not order_str or not order_str.strip():
        return None
    name_to_loc = {e.name: e for e in SearchLocation}
    order = []
    for part in order_str.strip().upper().split(","):
        part = part.strip()
        if part in name_to_loc:
            order.append(name_to_loc[part])
    return order if order else None


def cmd_get(args: Namespace, logger: Logger) -> int:
    """Extract the resource the engine would load (first in resolution order) to disk.

    Usage:
        pykotor get 203tell.wok --path "G:/.../KOTOR2" --output .
        pykotor get 203tel.lyt --path "G:/..." --order OVERRIDE,CHITIN
    """
    path = getattr(args, "path", None) or getattr(args, "installation", None)
    if not path:
        logger.error("No installation path. Use --path or --installation.")
        return 1

    resref_str = getattr(args, "resref", None) or getattr(args, "query", None)
    if not resref_str or not str(resref_str).strip():
        logger.error("No resource specified. Use: pykotor get <resref[.ext]> [--path PATH] [--output DIR]")
        return 1

    try:
        installation = Installation(pathlib.Path(path))
    except Exception:
        logger.exception("Invalid installation path")
        return 1

    ident = ResourceIdentifier.from_path(str(resref_str).strip())
    resname = ident.resname
    restype = ident.restype
    if restype.is_invalid or not restype.extension:
        logger.error("Could not determine resource type from '%s'. Include extension (e.g. 203tell.wok).", resref_str)
        return 1

    order = _parse_order_arg(getattr(args, "order", None))
    if order is None:
        order = canonical_search_order()

    result = installation.resource(resname, restype, order=order)
    if result is None:
        logger.warning(
            "Resource '%s.%s' not found. Searched in order: %s. Try: pykotor find %s --path %s",
            resname,
            restype.extension,
            ", ".join(s.name for s in order),
            resref_str,
            path,
        )
        return 1

    output = getattr(args, "output", None) or "."
    output_path = pathlib.Path(output).resolve()
    if output_path.is_dir() or (not output_path.exists() and not output_path.suffix):
        output_path = output_path / f"{resname}.{restype.extension}"
    elif output_path.suffix.lower() != f".{restype.extension}":
        output_path = output_path.parent / f"{output_path.stem}.{restype.extension}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(result.data)
    logger.info("Extracted %s.%s (%s bytes) to %s", resname, restype.extension, len(result.data), output_path)
    return 0
