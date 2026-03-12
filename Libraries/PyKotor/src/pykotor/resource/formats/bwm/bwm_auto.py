"""BWM (walkmesh) format detection and read/write dispatch (binary WOK)."""

from __future__ import annotations

import io
import os

from typing import TYPE_CHECKING

from pykotor.resource.formats.bwm.io_bwm import BWMBinaryReader, BWMBinaryWriter
from pykotor.resource.formats.bwm.io_bwm_ascii import BWMAsciiReader, BWMAsciiWriter
from pykotor.resource.type import ResourceType

if TYPE_CHECKING:
    from pykotor.resource.formats.bwm.bwm_data import BWM
    from pykotor.resource.type import SOURCE_TYPES, TARGET_TYPES

PEEK_SIZE = 256
BWM_MAGIC = b"BWM "


def _get_bwm_peek(
    source: SOURCE_TYPES,
    offset: int,
    size: int | None,
) -> bytes:
    """Read the first PEEK_SIZE bytes from source for format detection."""
    if isinstance(source, (bytes, bytearray)):
        data = bytes(source)
        start = offset
        end = offset + PEEK_SIZE if size is None else min(offset + (size or 0), offset + PEEK_SIZE)
        return data[start:end]
    if isinstance(source, memoryview):
        data = bytes(source)
        return data[offset : offset + PEEK_SIZE]
    if isinstance(source, (os.PathLike, str)):
        path = os.fspath(source) if isinstance(source, os.PathLike) else os.path.normpath(source)
        with open(path, "rb") as f:  # noqa: PTH123
            f.seek(offset)
            return f.read(PEEK_SIZE if size is None else min(size, PEEK_SIZE))
    # Stream-like: read then rewind
    stream = source
    peek = stream.read(PEEK_SIZE)  # type: ignore[union-attr]
    if hasattr(stream, "seek"):
        stream.seek(0)  # type: ignore[union-attr]
    return peek if isinstance(peek, bytes) else bytes(peek)


def _read_full_source(
    source: SOURCE_TYPES,
    offset: int,
    size: int | None,
) -> bytes:
    """Read full content from source for ASCII loading."""
    if isinstance(source, (bytes, bytearray)):
        data = bytes(source)
        if size is None:
            return data[offset:]
        return data[offset : offset + size]
    if isinstance(source, memoryview):
        data = bytes(source)
        return data[offset:] if size is None else data[offset : offset + size]
    if isinstance(source, (os.PathLike, str)):
        path = os.fspath(source) if isinstance(source, os.PathLike) else os.path.normpath(source)
        with open(path, "rb") as f:  # noqa: PTH123
            f.seek(offset)
            return f.read() if size is None else f.read(size)
    stream = source
    if hasattr(stream, "seek"):
        stream.seek(offset)  # type: ignore[union-attr]
    out = stream.read() if size is None else stream.read(size)  # type: ignore[union-attr]
    return out if isinstance(out, bytes) else bytes(out)


def _is_ascii_bwm(peek: bytes) -> bool:
    """Return True if peek looks like ASCII walkmesh (starts with 'node')."""
    try:
        decoded = peek.decode("latin-1").lstrip()
        return decoded.startswith("node")
    except UnicodeDecodeError:
        return False


def read_bwm(
    source: SOURCE_TYPES,
    offset: int = 0,
    size: int | None = None,
) -> BWM:
    """Returns an WOK instance from the source.

    Auto-detects binary (BWM magic) vs ASCII (starts with 'node') format.
    Supports .wok, .dwk, .pwk binary files and ASCII walkmesh files.

    Args:
    ----
        source: The source of the data (path, bytes, or stream).
        offset: The byte offset of the file inside the data
        size: Number of bytes to allowed to read from the stream. If not specified, uses the whole stream.

    Raises:
    ------
        FileNotFoundError: If the file could not be found.
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be accessed.
        ValueError: If the file was corrupted.

    Returns:
    -------
        An WOK instance.
    """
    peek = _get_bwm_peek(source, offset, size)
    if len(peek) >= 4 and peek[:4] == BWM_MAGIC:
        return BWMBinaryReader(source, offset, size or 0).load()
    if _is_ascii_bwm(peek):
        data = _read_full_source(source, offset, size)
        return BWMAsciiReader(io.BytesIO(data), 0, 0).load()
    return BWMBinaryReader(source, offset, size or 0).load()


def write_bwm(
    wok: BWM,
    target: TARGET_TYPES,
    file_format: ResourceType = ResourceType.WOK,
):
    """Writes the WOK data to the target location with the specified format (WOK only).

    Args:
    ----
        wok: The WOK file being written.
        target: The location to write the data to.
        file_format: The file format.

    Raises:
    ------
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be written to the specified destination.
        ValueError: If the specified format was unsupported.
    """
    if file_format == ResourceType.WOK:
        BWMBinaryWriter(wok, target).write()
    else:
        msg = "Unsupported format specified; use WOK."
        raise ValueError(msg)


def write_bwm_ascii(
    wok: BWM,
    target: TARGET_TYPES,
) -> None:
    """Writes the BWM to the target as ASCII walkmesh format.

    Args:
    ----
        wok: The BWM instance to write.
        target: The location to write (path, stream, or bytearray).

    Raises:
    ------
        IsADirectoryError: If the target is a directory.
        PermissionError: If the file could not be written.
        ValueError: If the data is invalid.
    """
    BWMAsciiWriter(wok, target).write()


def bytes_bwm(
    bwm: BWM,
    file_format: ResourceType = ResourceType.WOK,
) -> bytes:
    """Returns the BWM data in the specified format (WOK only) as a bytes object.

    This is a convenience method that wraps the write_bwm() method.

    Args:
    ----
        bwm: The target BWM.
        file_format: The file format.

    Raises:
    ------
        ValueError: If the specified format was unsupported.

    Returns:
    -------
        The BWM data.
    """
    data = bytearray()
    write_bwm(bwm, data, file_format)
    return bytes(data)
