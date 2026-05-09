"""TPC/texture format detection and auto read/write dispatch (TPC, TGA, DDS, BMP).

Includes :func:`build_tpc_from_tga_bytes`, :func:`build_tpc_from_tga_path`, and the
TGA→TPC CLI entrypoint (``python -m pykotor.resource.formats.tpc``).
"""

from __future__ import annotations

import argparse
import io
import os
import struct
import sys

from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Sequence

from pykotor.common.stream import BinaryReader
from pykotor.resource.formats.tpc.io_bmp import TPCBMPWriter
from pykotor.resource.formats.tpc.io_dds import TPCDDSReader, TPCDDSWriter
from pykotor.resource.formats.tpc.io_tga import TPCTGAReader, TPCTGAWriter
from pykotor.resource.formats.tpc.io_tpc import TPCBinaryReader, TPCBinaryWriter
from pykotor.resource.formats.tpc.tga import TGAImage, read_tga
from pykotor.resource.formats.tpc.tpc_data import TPC, TPCLayer, TPCMipmap, TPCTextureFormat
from pykotor.resource.type import ResourceType
from pykotor.tools.path import CaseAwarePath

if TYPE_CHECKING:
    from pykotor.resource.type import SOURCE_TYPES, TARGET_TYPES


def detect_tpc(
    source: SOURCE_TYPES,
    offset: int = 0,
) -> ResourceType:
    """Returns what format the TPC data is believed to be in.

    This function performs a basic check and does not guarantee accuracy of the result or integrity of the data.

    Args:
    ----
        source: Source of the TPC data.
        offset: Offset into the source data.

    Raises:
    ------
        FileNotFoundError: If the file could not be found.
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be accessed.

    Returns:
    -------
        The format of the TPC data.
    """

    def do_check(sample: bytes) -> ResourceType:
        if sample.startswith(b"DDS "):
            return ResourceType.DDS

        if len(sample) >= 20:
            # BioWare DDS header heuristic: width/height/bpp/datasize (uint32 LE)
            width, height, bpp, data_size = struct.unpack_from("<IIII", sample, 0)
            if 0 < width < 0x8000 and 0 < height < 0x8000 and bpp in (3, 4):
                expected = (width * height) // 2 if bpp == 3 else width * height
                if data_size == expected:
                    return ResourceType.DDS

        if len(sample) < 100:  # noqa: PLR2004
            return ResourceType.TGA

        for i in range(15, min(len(sample), 100)):
            if sample[i] != 0:
                return ResourceType.TGA
        return ResourceType.TPC

    if isinstance(source, (str, os.PathLike)):
        suffix = CaseAwarePath(source).suffix.lower()
        if suffix == ".dds":
            return ResourceType.DDS

    file_format: ResourceType = ResourceType.INVALID
    try:
        if isinstance(source, (str, os.PathLike)):
            with BinaryReader.from_file(source, offset) as reader:
                file_format = do_check(bytes(reader.read_bytes(128)))
        elif isinstance(source, (bytes, bytearray)):
            file_format = do_check(bytes(source[:128]))
        elif isinstance(source, BinaryReader):
            file_format = do_check(bytes(source.read_bytes(128)))
            source.skip(-128)
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        raise
    except OSError:
        file_format = ResourceType.INVALID

    return file_format


def read_tpc(
    source: SOURCE_TYPES,
    offset: int = 0,
    size: int | None = None,
    txi_source: SOURCE_TYPES | None = None,
) -> TPC:
    """Returns an TPC instance from the source.

    The file format (TPC or TGA) is automatically determined before parsing the data.

    Args:
    ----
        source: The source of the data.
        offset: The byte offset of the file inside the data.
        size: Number of bytes to allowed to read from the stream. If not specified, uses the whole stream.
        txi_source: An optional source to the TXI data to use. If this is a filepath, it *must* exist on disk.

    Raises:
    ------
        FileNotFoundError: If the file could not be found.
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be accessed.
        ValueError: If the file was corrupted or the format could not be determined.

    Returns:
    -------
        An TPC instance.
    """
    file_format: ResourceType = detect_tpc(source, offset)

    loaded_tpc: TPC
    if file_format == ResourceType.TPC:
        loaded_tpc = TPCBinaryReader(source, offset, size or 0).load()
    elif file_format == ResourceType.TGA:
        loaded_tpc = TPCTGAReader(source, offset, size or 0).load()
    elif file_format == ResourceType.DDS:
        loaded_tpc = TPCDDSReader(source, offset, size or 0).load()
    else:
        msg = "Failed to determine the format of the TPC/TGA file."
        raise ValueError(msg)
    if txi_source is None and isinstance(source, (os.PathLike, str)):
        txi_path = CaseAwarePath(source).with_suffix(".txi")
        if not txi_path.is_file():
            return loaded_tpc
        txi_source = txi_path
    elif isinstance(txi_source, (os.PathLike, str)):
        txi_path = CaseAwarePath(txi_source).with_suffix(".txi")
        if not txi_path.is_file():
            return loaded_tpc
        txi_source = txi_path

    if txi_source is None:
        return loaded_tpc
    with BinaryReader.from_auto(txi_source) as f:
        loaded_tpc.txi = f.read_all().decode(encoding="ascii", errors="ignore")
    return loaded_tpc


def write_tpc(
    tpc: TPC,
    target: TARGET_TYPES,
    file_format: ResourceType = ResourceType.TPC,
):
    """Writes the TPC data to the target location with the specified format (TPC, TGA or BMP).

    Args:
    ----
        tpc: The TPC file being written.
        target: The location to write the data to.
        file_format: The file format.

    Raises:
    ------
        IsADirectoryError: If the specified path is a directory (Unix-like systems only).
        PermissionError: If the file could not be written to the specified destination.
        ValueError: If the specified format was unsupported.
    """
    if file_format == ResourceType.TGA:
        TPCTGAWriter(tpc, target).write()
    elif file_format == ResourceType.BMP:
        TPCBMPWriter(tpc, target).write()
    elif file_format == ResourceType.DDS:
        TPCDDSWriter(tpc, target).write()
    elif file_format == ResourceType.TPC:
        TPCBinaryWriter(tpc, target).write()
    else:
        msg = "Unsupported format specified; use TPC, TGA, DDS or BMP."
        raise ValueError(msg)


def bytes_tpc(
    tpc: TPC,
    file_format: ResourceType = ResourceType.TPC,
) -> bytes:
    """Returns the TPC data in the specified format (TPC, TGA, DDS or BMP) as a bytes object.

    This is a convenience method that wraps the write_tpc() method.

    Args:
    ----
        tpc: The target TPC object.
        file_format: The file format.

    Raises:
    ------
        ValueError: If the specified format was unsupported.

    Returns:
    -------
        The TPC data.
    """
    data = bytearray()
    write_tpc(tpc, data, file_format)
    return bytes(data)


def _has_alpha_channel(frame: TGAImage) -> bool:
    """Return True when any pixel in the frame has transparency."""
    return any(frame.data[i] != 0xFF for i in range(3, len(frame.data), 4))


def _is_grayscale(frame: TGAImage) -> bool:
    """Return True if the RGB channels are identical for every pixel."""
    data = frame.data
    for i in range(0, len(data), 4):
        r, g, b = data[i : i + 3]
        if r != g or g != b:
            return False
    return True


def _split_flipbook(image: TGAImage, num_x: int, num_y: int) -> list[TGAImage]:
    if num_x <= 0 or num_y <= 0:
        raise ValueError("Flipbook requires positive --numx and --numy values")

    if image.width % num_x != 0 or image.height % num_y != 0:
        raise ValueError("Image dimensions are not divisible by the requested flipbook grid")

    frame_width = image.width // num_x
    frame_height = image.height // num_y
    frames: list[TGAImage] = []
    stride = image.width * 4
    for tile_y in range(num_y):
        for tile_x in range(num_x):
            buffer = bytearray(frame_width * frame_height * 4)
            for row in range(frame_height):
                src_offset = ((tile_y * frame_height) + row) * stride + tile_x * frame_width * 4
                dst_offset = row * frame_width * 4
                buffer[dst_offset : dst_offset + frame_width * 4] = image.data[
                    src_offset : src_offset + frame_width * 4
                ]
            frames.append(
                TGAImage(
                    width=frame_width,
                    height=frame_height,
                    data=bytes(buffer),
                    source_pixel_depth=image.source_pixel_depth,
                ),
            )
    return frames


def _split_cubemap(image: TGAImage) -> list[TGAImage]:
    if image.height % image.width != 0 or image.height // image.width != 6:
        raise ValueError("Cubemap source must be stacked vertically with height == 6 * width")

    face_height = image.height // 6
    stride = image.width * 4
    faces: list[TGAImage] = []
    for face in range(6):
        buffer = bytearray(image.width * face_height * 4)
        for row in range(face_height):
            src = (face * face_height + row) * stride
            dst = row * image.width * 4
            buffer[dst : dst + image.width * 4] = image.data[src : src + image.width * 4]
        faces.append(
            TGAImage(
                width=image.width,
                height=face_height,
                data=bytes(buffer),
                source_pixel_depth=image.source_pixel_depth,
            ),
        )
    return faces


def _ensure_line(lines: list[str], key: str, value: str) -> None:
    """Append a TXI directive if it is not already present."""
    lower = key.lower()
    if any(entry.lower().startswith(lower) for entry in lines):
        return
    lines.append(f"{key} {value}")


def _compose_txi_lines(
    user_lines: Sequence[str] | None,
    *,
    cube: bool,
    num_x: int,
    num_y: int,
    fps: float,
) -> list[str]:
    lines = [line.rstrip() for line in user_lines or [] if line.strip()]

    if cube:
        _ensure_line(lines, "cube", "1")

    if num_x > 0 and num_y > 0 and fps > 0:
        _ensure_line(lines, "proceduretype", "cycle")
        _ensure_line(lines, "numx", str(num_x))
        _ensure_line(lines, "numy", str(num_y))
        _ensure_line(lines, "fps", f"{fps:g}")

    return lines


def _create_layer(
    frame: TGAImage,
    *,
    generate_mipmaps: bool,
) -> TPCLayer:
    layer = TPCLayer()
    if generate_mipmaps:
        layer.set_single(
            frame.width,
            frame.height,
            frame.data,
            TPCTextureFormat.RGBA,
            rgba_mipmap_ndix=True,
        )
    else:
        layer.mipmaps = [
            TPCMipmap(
                width=frame.width,
                height=frame.height,
                tpc_format=TPCTextureFormat.RGBA,
                data=bytearray(frame.data),
            ),
        ]
    return layer


def _select_target_format(
    compression: str,
    *,
    grayscale: bool,
    has_alpha: bool,
    source_pixel_depth: int,
) -> TPCTextureFormat:
    if compression == "auto":
        if source_pixel_depth <= 8:
            return TPCTextureFormat.Greyscale
        if source_pixel_depth == 24:
            return TPCTextureFormat.DXT1
        return TPCTextureFormat.DXT5
    if compression == "none":
        if grayscale:
            return TPCTextureFormat.Greyscale
        return TPCTextureFormat.RGBA if has_alpha else TPCTextureFormat.RGB
    if compression == "dxt1":
        return TPCTextureFormat.DXT1
    if compression == "dxt5":
        return TPCTextureFormat.DXT5
    raise ValueError(f"Unsupported compression mode: {compression}")


def _build_texture(
    frames: Sequence[TGAImage],
    *,
    compression: str,
    generate_mipmaps: bool,
    txi_lines: Sequence[str],
    cube: bool,
    num_x: int,
    num_y: int,
    alpha_test: float,
) -> TPC:
    if not frames:
        raise ValueError("At least one frame is required to build a texture")

    has_alpha = any(_has_alpha_channel(frame) for frame in frames)
    grayscale = all(_is_grayscale(frame) for frame in frames)
    source_pixel_depth = frames[0].source_pixel_depth

    tpc = TPC()
    tpc.layers = [_create_layer(frame, generate_mipmaps=generate_mipmaps) for frame in frames]
    tpc._format = TPCTextureFormat.RGBA  # noqa: SLF001
    tpc.alpha_test = alpha_test

    target_format = _select_target_format(
        compression,
        grayscale=grayscale,
        has_alpha=has_alpha,
        source_pixel_depth=source_pixel_depth,
    )
    if target_format != TPCTextureFormat.RGBA:
        tpc.convert(target_format)
    else:
        tpc._format = TPCTextureFormat.RGBA  # noqa: SLF001

    payload = "\n".join(txi_lines).strip()
    if payload:
        tpc.txi = payload

    if cube:
        if len(tpc.layers) != 6:
            raise ValueError(f"Cubemap textures must provide 6 faces, found {len(tpc.layers)}")
        tpc.is_cube_map = True
    elif tpc._txi.features.cube:  # noqa: SLF001
        tpc.is_cube_map = True

    flipbook_layers = num_x * num_y
    if flipbook_layers > 0:
        if flipbook_layers != len(tpc.layers):
            raise ValueError(
                f"Flipbook metadata (numx*numy={flipbook_layers}) does not match layer count {len(tpc.layers)}",
            )
        tpc.is_animated = True
    elif tpc._txi.features.is_flipbook:  # noqa: SLF001
        tpc.is_animated = True

    return tpc


def build_tpc_from_tga_bytes(
    raw_tga: bytes | bytearray,
    *,
    txi_lines: Sequence[str] | None = None,
    compression: str = "auto",
    generate_mipmaps: bool = True,
    alpha_test: float = 1.0,
) -> TPC:
    """Build a KotOR-ready ``TPC`` from raw uncompressed TGA bytes (Holocron-style defaults).

    Same compression / mipmap / header rules as :func:`build_tpc_from_tga_path`, without
    reading from disk. Optional ``txi_lines`` are merged like a ``.txi`` sidecar (already
    split into lines; no ``_compose_txi_lines`` cube/flipbook injection unless present).
    """
    base_image = read_tga(io.BytesIO(bytes(raw_tga)))
    composed = _compose_txi_lines(
        [line.rstrip() for line in (txi_lines or ()) if line.strip()],
        cube=False,
        num_x=0,
        num_y=0,
        fps=0.0,
    )
    return _build_texture(
        [base_image],
        compression=compression,
        generate_mipmaps=generate_mipmaps,
        txi_lines=composed,
        cube=False,
        num_x=0,
        num_y=0,
        alpha_test=alpha_test,
    )


def build_tpc_from_tga_path(
    tga_path: Path,
    *,
    txi_path: Path | None = None,
    compression: str = "auto",
    generate_mipmaps: bool = True,
    alpha_test: float = 1.0,
) -> TPC:
    """Build a KotOR-ready ``TPC`` from an uncompressed TGA (same defaults as :func:`run_cli`).

    Uses :func:`read_tga` on the file (single image; no ``--cube`` / flipbook splitting).
    When ``txi_path`` is ``None``, a ``.txi`` beside ``tga_path`` is picked up if present,
    matching Holocron / CLI sidecar behavior.

    Args:
        tga_path: Path to a ``.tga`` file.
        txi_path: Optional explicit ``.txi`` path; if omitted, uses ``tga_path`` with
            ``.txi`` suffix when that file exists.
        compression: Same values as CLI ``--compression`` (``auto``, ``none``, ``dxt1``, ``dxt5``).
        generate_mipmaps: When false, only the base mip is kept (CLI ``--no-mipmaps``).
        alpha_test: Stored in the TPC header (CLI ``--alpha-test``).

    Returns:
        Loaded :class:`TPC` instance ready for :func:`write_tpc` / :class:`TPCBinaryWriter`.
    """
    tga_path = Path(tga_path)
    if not tga_path.is_file():
        msg = f"TGA file not found: {tga_path}"
        raise FileNotFoundError(msg)

    raw_tga = tga_path.read_bytes()

    txi_file = Path(txi_path) if txi_path is not None else tga_path.with_suffix(".txi")
    raw_lines: list[str] = []
    if txi_file.is_file():
        raw_lines = txi_file.read_text(encoding="utf-8", errors="ignore").splitlines()

    return build_tpc_from_tga_bytes(
        raw_tga,
        txi_lines=raw_lines,
        compression=compression,
        generate_mipmaps=generate_mipmaps,
        alpha_test=alpha_test,
    )


def _load_txi_lines(path: Path | None) -> list[str]:
    if not path:
        return []
    if not path.exists():
        raise FileNotFoundError(f"TXI file '{path}' not found")
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()


def _write_sidecar_txi(path: Path, texture: TPC) -> None:
    payload = str(texture.txi).strip()
    if not payload:
        return
    if not payload.endswith("\n"):
        payload += "\n"
    path.write_text(payload, encoding="ascii", errors="ignore")


def run_cli(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description="Convert TGA images into BioWare TPC textures.")
    parser.add_argument("--input", "-i", type=Path, required=True, help="Source TGA image")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Destination TPC file")
    parser.add_argument("--txi", type=Path, help="Optional TXI file to merge into the texture")
    parser.add_argument(
        "--emit-txi", action="store_true", help="Write the generated TXI data alongside the TPC"
    )
    parser.add_argument(
        "--compression",
        choices=["auto", "dxt1", "dxt5", "none"],
        default="auto",
        help="Compression strategy",
    )
    parser.add_argument("--numx", type=int, default=0, help="Flipbook columns")
    parser.add_argument("--numy", type=int, default=0, help="Flipbook rows")
    parser.add_argument("--fps", type=float, default=0.0, help="Flipbook playback rate")
    parser.add_argument(
        "--cube",
        action="store_true",
        help="Treat the input as a cubemap (six faces stacked vertically)",
    )
    parser.add_argument("--no-mipmaps", action="store_true", help="Do not generate mipmaps")
    parser.add_argument(
        "--alpha-test", type=float, default=1.0, help="Alpha test threshold (stored in header)"
    )

    args = parser.parse_args(list(argv))

    if not args.input.exists():
        raise FileNotFoundError(f"TGA file '{args.input}' not found")

    with args.input.open("rb") as handle:
        base_image = read_tga(handle)

    if args.cube:
        frames = _split_cubemap(base_image)
    elif args.numx and args.numy:
        frames = _split_flipbook(base_image, args.numx, args.numy)
    else:
        frames = [base_image]

    txi_lines = _compose_txi_lines(
        _load_txi_lines(args.txi),
        cube=args.cube,
        num_x=args.numx,
        num_y=args.numy,
        fps=args.fps,
    )

    texture = _build_texture(
        frames,
        compression=args.compression,
        generate_mipmaps=not args.no_mipmaps,
        txi_lines=txi_lines,
        cube=args.cube,
        num_x=args.numx,
        num_y=args.numy,
        alpha_test=args.alpha_test,
    )

    write_tpc(texture, args.output, ResourceType.TPC)

    if args.emit_txi:
        txi_path = args.output.with_suffix(".txi")
        _write_sidecar_txi(txi_path, texture)

    return 0


def main() -> None:
    try:
        raise SystemExit(run_cli(sys.argv[1:]))
    except BrokenPipeError:  # pragma: no cover - convenience for pipelines
        pass
