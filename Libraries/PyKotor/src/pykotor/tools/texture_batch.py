"""Headless TPC/TGA/PNG batch conversion and editor load helpers.

Used by HolocronToolset, pykotorcli-style tools, and KotorBlender. Converts ``.tpc``,
``.tga``, and ``.png`` via the shared TPC/TGA pipeline with Holocron-aligned TXI
sidecar behavior and small-TGA detection fallback.
"""

from __future__ import annotations

import os
import io
import logging

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Literal, Union

from pykotor.common.stream import BinaryReader
from pykotor.resource.formats.tpc import TPC, bytes_tpc, read_tpc, write_tpc
from pykotor.resource.formats.tpc.io_tga import TPCTGAReader
from pykotor.resource.formats.tpc.tga import TGAImage, read_tga, write_tga
from pykotor.resource.formats.tpc.tpc_auto import build_tpc_from_tga_bytes, build_tpc_from_tga_path
from pykotor.resource.type import ResourceType

PathLike = Union[str, os.PathLike[str]]
TextureFormat = Literal["tpc", "tga", "png"]
SUPPORTED_TEXTURE_SUFFIXES = (".tpc", ".tga", ".png")


@dataclass
class TextureBatchOutcome:
    """Tallies for :func:`batch_convert_textures`."""

    success_count: int = 0
    skipped_count: int = 0
    errors: List[str] = field(default_factory=list)
    outputs: List[Path] = field(default_factory=list)


def _require_pillow():
    """Import Pillow lazily so non-PNG texture workflows keep their small dependency surface."""
    try:
        from PIL import Image
    except ImportError as exc:
        msg = (
            "PNG texture conversion requires Pillow. Install the PyKotor textures/all extra "
            "(for example: pip install 'pykotor[textures]')."
        )
        raise RuntimeError(msg) from exc
    logging.getLogger("PIL").setLevel(logging.WARNING)
    return Image


def _find_txi_sidecar(path: Path) -> Path | None:
    txi_path = path.with_suffix(".txi")
    if txi_path.is_file():
        return txi_path
    parent = path.parent
    if not parent.is_dir():
        return None
    expected = txi_path.name.lower()
    for child in parent.iterdir():
        if child.is_file() and child.name.lower() == expected:
            return child
    return None


def _txi_source_or_empty(path: Path) -> Path | bytearray:
    txi_path = _find_txi_sidecar(path)
    return txi_path if txi_path is not None else bytearray()


def _load_tga_for_convert(path: Path) -> TPC:
    """Load a ``.tga`` like :func:`read_tpc`, including optional ``.txi`` sidecar.

    Falls back to :class:`TPCTGAReader` when ``detect_tpc`` misclassifies small TGAs.
    """
    try:
        return read_tpc(path, txi_source=_txi_source_or_empty(path))
    except ValueError:
        loaded = TPCTGAReader(path).load()
    txi_path = _find_txi_sidecar(path)
    if txi_path is not None:
        with BinaryReader.from_auto(txi_path) as f:
            loaded.txi = f.read_all().decode(encoding="ascii", errors="ignore")
    return loaded


def read_tpc_for_editor(
    filepath: PathLike,
    data: bytes | bytearray,
) -> TPC:
    """Load TPC/TGA from in-memory bytes with optional ``.txi`` beside ``filepath``.

    Matches Holocron ``TPCEditor.load`` for TPC/TGA: sidecar is
    ``Path(filepath).with_suffix('.txi')`` when present. Uses the same
    small-TGA fallback as :func:`_load_tga_for_convert` when auto-detect
    misreads raw bytes.
    """
    path = Path(os.fspath(filepath)).resolve()
    txi_path = _find_txi_sidecar(path)
    txi_src = txi_path if txi_path is not None else None
    try:
        return read_tpc(data, txi_source=txi_src)
    except ValueError:
        raw = bytes(data)
        loaded = TPCTGAReader(raw, 0, len(raw)).load()
        if txi_path is not None:
            with BinaryReader.from_auto(txi_path) as f:
                loaded.txi = f.read_all().decode(encoding="ascii", errors="ignore")
        return loaded


def _write_txi_sidecar_for_tga(image_path: Path, texture: TPC) -> None:
    """Write ``.txi`` next to ``.tga`` when the TPC carries TXI text (Holocron sidecar pattern)."""
    payload = str(texture.txi).strip()
    if not payload:
        return
    if not payload.endswith("\n"):
        payload += "\n"
    image_path.with_suffix(".txi").write_text(payload, encoding="ascii", errors="ignore")


def _read_txi_lines(path: Path) -> List[str]:
    txi_path = _find_txi_sidecar(path)
    if txi_path is None:
        return []
    return txi_path.read_text(encoding="ascii", errors="ignore").splitlines()


def _png_to_tga_bytes(path: Path) -> bytes:
    Image = _require_pillow()
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        tga = TGAImage(rgba.width, rgba.height, rgba.tobytes(), source_pixel_depth=32)
    out = io.BytesIO()
    write_tga(tga, out)
    return out.getvalue()


def _write_png_from_tga_bytes(raw_tga: bytes | bytearray, output_path: Path) -> None:
    Image = _require_pillow()
    tga = read_tga(io.BytesIO(bytes(raw_tga)))
    image = Image.frombytes("RGBA", (tga.width, tga.height), tga.data)
    image.save(output_path, "PNG")


def _infer_output_suffix(src: Path, to_format: TextureFormat | None) -> str:
    if to_format is not None:
        return f".{to_format}"
    if src.suffix.lower() == ".tpc":
        return ".tga"
    if src.suffix.lower() == ".tga":
        return ".tpc"
    if src.suffix.lower() == ".png":
        return ".tga"
    msg = f"Not a supported texture file: {src}"
    raise ValueError(msg)


def _resolve_output_path(
    src: Path,
    output: Path | None,
    to_format: TextureFormat | None,
    *,
    relative_base: Path | None = None,
) -> Path:
    suffix = _infer_output_suffix(src, to_format)
    if output is None:
        return src.with_suffix(suffix)
    if output.exists() and output.is_dir():
        if relative_base is not None:
            return output / src.relative_to(relative_base).with_suffix(suffix)
        return output / src.with_suffix(suffix).name
    if output.suffix:
        return output
    if relative_base is not None:
        return output / src.relative_to(relative_base).with_suffix(suffix)
    return output / src.with_suffix(suffix).name


def convert_single_texture(
    src: PathLike,
    *,
    output: PathLike | None = None,
    to_format: TextureFormat | None = None,
    relative_base: PathLike | None = None,
    overwrite: bool = False,
    write_txi_sidecar_for_tga: bool = True,
) -> Path:
    """Convert one ``.tpc``, ``.tga``, or ``.png`` texture.

    Default output mirrors the editor workflow: ``.tpc`` -> ``.tga``, ``.tga`` -> ``.tpc``,
    and ``.png`` -> ``.tga``. Pass ``to_format`` to force a target format.

    Returns:
        Path to the written file.

    Raises:
        FileNotFoundError: If ``src`` is missing.
        FileExistsError: If the destination exists and ``overwrite`` is False.
        ValueError: If the suffix or target format is unsupported.

    """
    path = Path(os.fspath(src)).resolve()
    if not path.is_file():
        raise FileNotFoundError(os.fspath(path))
    suf = path.suffix.lower()
    if suf not in SUPPORTED_TEXTURE_SUFFIXES:
        msg = f"Not a TPC, TGA, or PNG file: {path}"
        raise ValueError(msg)
    dst = _resolve_output_path(
        path,
        Path(os.fspath(output)) if output is not None else None,
        to_format,
        relative_base=Path(os.fspath(relative_base)).resolve() if relative_base else None,
    )
    out_suffix = dst.suffix.lower()
    if out_suffix not in SUPPORTED_TEXTURE_SUFFIXES:
        msg = f"Unsupported texture output format: {dst.suffix or dst}"
        raise ValueError(msg)
    if out_suffix == suf:
        msg = f"Input and output texture formats are both {suf}: {path}"
        raise ValueError(msg)
    if not overwrite and dst.exists():
        raise FileExistsError(os.fspath(dst))

    dst.parent.mkdir(parents=True, exist_ok=True)

    if suf == ".png":
        raw_tga = _png_to_tga_bytes(path)
        if out_suffix == ".tga":
            dst.write_bytes(raw_tga)
            return dst
        tpc = build_tpc_from_tga_bytes(
            raw_tga,
            txi_lines=_read_txi_lines(path),
            compression="auto",
            generate_mipmaps=True,
            alpha_test=1.0,
        )
        write_tpc(tpc, dst, file_format=ResourceType.TPC)
        return dst

    if suf == ".tpc":
        tpc = read_tpc(path, txi_source=_txi_source_or_empty(path))
    elif out_suffix == ".tpc":
        txi_side = path.with_suffix(".txi")
        txi_arg = txi_side if txi_side.is_file() else None
        tpc = build_tpc_from_tga_path(path, txi_path=txi_arg)
    else:
        tpc = _load_tga_for_convert(path)

    if out_suffix == ".png":
        _write_png_from_tga_bytes(bytes_tpc(tpc, ResourceType.TGA), dst)
        return dst

    out_fmt = ResourceType.TGA if out_suffix == ".tga" else ResourceType.TPC
    write_tpc(tpc, dst, file_format=out_fmt)
    if out_suffix == ".tga" and write_txi_sidecar_for_tga:
        _write_txi_sidecar_for_tga(dst, tpc)
    return dst


def iter_texture_paths(
    root: PathLike,
    *,
    recursive: bool,
    source_formats: set[TextureFormat] | None = None,
) -> List[Path]:
    """List supported texture files under ``root`` (file or directory)."""
    p = Path(os.fspath(root)).resolve()
    allowed_suffixes = (
        tuple(f".{fmt}" for fmt in source_formats) if source_formats else SUPPORTED_TEXTURE_SUFFIXES
    )
    if p.is_file():
        return [p] if p.suffix.lower() in allowed_suffixes else []
    if not p.is_dir():
        return []
    out: List[Path] = []
    if recursive:
        for child in p.rglob("*"):
            if child.is_file() and child.suffix.lower() in allowed_suffixes:
                out.append(child)
    else:
        for child in p.iterdir():
            if child.is_file() and child.suffix.lower() in allowed_suffixes:
                out.append(child)
    return sorted(out)


def batch_convert_textures(
    paths: PathLike | list[PathLike],
    *,
    output: PathLike | None = None,
    to_format: TextureFormat | None = None,
    recursive: bool = False,
    overwrite: bool = False,
    source_formats: set[TextureFormat] | None = None,
    write_txi_sidecar_for_tga: bool = True,
) -> TextureBatchOutcome:
    """Batch-convert supported texture files under directories or explicit file inputs.

    Skips outputs that already exist when ``overwrite`` is False.
    Collects per-file error strings and continues.
    """
    outcome = TextureBatchOutcome()
    roots = paths if isinstance(paths, list) else [paths]
    targets: List[tuple[Path, Path | None]] = []
    for root in roots:
        root_path = Path(os.fspath(root)).resolve()
        relative_base = root_path if root_path.is_dir() else None
        targets.extend(
            (target, relative_base)
            for target in iter_texture_paths(
                root, recursive=recursive, source_formats=source_formats
            )
        )
    output_path = Path(os.fspath(output)) if output is not None else None
    for src, relative_base in targets:
        dst = _resolve_output_path(src, output_path, to_format, relative_base=relative_base)
        if not overwrite and dst.exists():
            outcome.skipped_count += 1
            continue
        try:
            written = convert_single_texture(
                src,
                output=output_path,
                to_format=to_format,
                relative_base=relative_base,
                overwrite=overwrite,
                write_txi_sidecar_for_tga=write_txi_sidecar_for_tga,
            )
            outcome.success_count += 1
            outcome.outputs.append(written)
        except OSError as exc:
            outcome.errors.append(f"{src}: {exc}")
        except (RuntimeError, ValueError) as exc:
            outcome.errors.append(f"{src}: {exc}")
    return outcome
