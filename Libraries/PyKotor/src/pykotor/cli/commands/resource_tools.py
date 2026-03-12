"""Resource conversion command implementations for Pykotorcli.

This module provides CLI commands for converting resources (textures, sounds, models)
using PyKotor utilities.
"""

from __future__ import annotations

import pathlib
import sys

from typing import TYPE_CHECKING

from pykotor.resource.formats.bwm import read_bwm, write_bwm, write_bwm_ascii
from pykotor.tools.resources import (
    convert_ascii_to_bwm,
    convert_ascii_to_mdl,
    convert_bwm_to_ascii,
    convert_clean_to_wav,
    convert_mdl_to_ascii,
    convert_tga_to_tpc,
    convert_tpc_to_tga,
    convert_wav_to_clean,
)

if TYPE_CHECKING:
    from argparse import Namespace

    from loggerplus import RobustLogger as Logger


def cmd_texture_convert(args: Namespace, logger: Logger) -> int:
    """Convert texture files (TPC<->TGA)."""
    input_path = pathlib.Path(args.input)

    try:
        if input_path.suffix.lower() == ".tpc":
            # TPC to TGA
            output_path = pathlib.Path(args.output) if args.output else input_path.with_suffix(".tga")
            txi_output = pathlib.Path(args.txi) if args.txi else None
            convert_tpc_to_tga(input_path, output_path, txi_output_path=txi_output)
            logger.info(f"Converted {input_path.name} to {output_path.name}")  # noqa: G004
        else:
            # TGA to TPC
            output_path = pathlib.Path(args.output) if args.output else input_path.with_suffix(".tpc")
            txi_path = pathlib.Path(args.txi) if args.txi else None
            convert_tga_to_tpc(
                input_path,
                output_path,
                txi_input_path=txi_path,
                target_format=None,  # Auto-detect format
            )
            logger.info(f"Converted {input_path.name} to {output_path.name}")  # noqa: G004
    except Exception:
        logger.exception(f"Failed to convert texture {input_path}")  # noqa: G004
        return 1
    else:
        return 0


def cmd_sound_convert(args: Namespace, logger: Logger) -> int:
    """Convert sound files (WAV<->clean WAV).

    References:
    ----------
        Based on swkotor.exe audio format:
        - WAV file loading with SFX header deobfuscation
        - "RIFF" format identifier @ 0x0074d324
        - "STREAMWAVES" directory @ 0x0074df34


    """
    input_path = pathlib.Path(args.input)
    output_path = pathlib.Path(args.output) if args.output else input_path.with_suffix(".wav")

    try:
        if args.to_clean:
            # WAV to clean (deobfuscated)
            convert_wav_to_clean(input_path, output_path)
            logger.info(f"Converted {input_path.name} to clean WAV: {output_path.name}")  # noqa: G004
        else:
            # Clean WAV to game format
            wav_type = args.type if hasattr(args, "type") else "SFX"
            convert_clean_to_wav(input_path, output_path, wav_type=wav_type)
            logger.info(f"Converted {input_path.name} to game WAV: {output_path.name}")  # noqa: G004
    except Exception:
        logger.exception(f"Failed to convert sound {input_path}")  # noqa: G004
        return 1
    else:
        return 0


def cmd_model_convert(args: Namespace, logger: Logger) -> int:
    """Convert model files (MDL<->ASCII).

    References:
    ----------
        Based on swkotor.exe model format:
        - LoadModel @ 0x00464200, @ 0x0061b380, @ 0x006823f0, @ 0x006842e0, @ 0x006903d0, @ 0x006910d0 - Model loading functions
        - UnloadModel @ 0x0060c8e0, @ 0x00646650, @ 0x006825f0 - Model unloading functions

        Derivations and Other Implementations:
        ----------
        https://github.com/th3w1zard1/mdlops/tree/master/
        https://github.com/th3w1zard1/kotorblender/tree/master/


    """
    input_path = pathlib.Path(args.input)

    try:
        if args.to_ascii:
            # Binary MDL to ASCII
            output_path = pathlib.Path(args.output) if args.output else input_path.with_suffix(".mdl")
            mdx_path = pathlib.Path(args.mdx) if args.mdx else None
            convert_mdl_to_ascii(input_path, output_path, mdx_path=mdx_path)
            logger.info(f"Converted {input_path.name} to ASCII: {output_path.name}")  # noqa: G004
        else:
            # ASCII MDL to binary
            output_mdl = pathlib.Path(args.output) if args.output else input_path.with_suffix(".mdl")
            mdx_output = pathlib.Path(args.mdx) if args.mdx else None
            convert_ascii_to_mdl(input_path, output_mdl, output_mdx_path=mdx_output)
            logger.info(f"Converted {input_path.name} to binary: {output_mdl.name}")  # noqa: G004
    except Exception:
        logger.exception(f"Failed to convert model {input_path}")  # noqa: G004
        return 1
    else:
        return 0


def cmd_walkmesh_rebuild(args: Namespace, logger: Logger) -> int:
    """Rebuild BWM AABB/adjacency/edges from geometry (read then write regenerates derived data)."""
    input_path = pathlib.Path(args.input)

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")  # noqa: G004
        return 1

    # Default output: overwrite input for binary; for .ascii input use same stem with .wok
    if args.output is not None:
        output_path = pathlib.Path(args.output)
    elif input_path.suffix.lower() == ".ascii":
        output_path = input_path.with_suffix("").with_suffix(".wok")
    else:
        output_path = input_path

    try:
        # ---- Input and format ----
        input_size = input_path.stat().st_size
        with input_path.open("rb") as f:
            peek = f.read(min(256, input_size))
        if len(peek) >= 4 and peek[:4] == b"BWM ":
            format_name = "binary (BWM magic)"
        elif peek.decode("latin-1", errors="ignore").lstrip().startswith("node"):
            format_name = "ASCII (node block)"
        else:
            format_name = "binary (assumed)"
        logger.info(f"Input: {input_path} ({input_size} bytes)")  # noqa: G004
        logger.info(f"Detected format: {format_name}")  # noqa: G004

        # ---- Load ----
        logger.info("Loading walkmesh...")  # noqa: G004
        bwm = read_bwm(input_path)
        verts = bwm.vertices()
        walkable = [f for f in bwm.faces if f.material.walkable()]
        unwalkable = [f for f in bwm.faces if not f.material.walkable()]
        n_faces = len(bwm.faces)
        n_walkable = len(walkable)
        n_unwalkable = len(unwalkable)
        type_name = getattr(bwm.walkmesh_type, "name", str(bwm.walkmesh_type))

        logger.info(  # noqa: G004
            f"Loaded: {len(verts)} vertices, {n_faces} faces ({n_walkable} walkable, {n_unwalkable} unwalkable), type={type_name}",
        )

        # Count faces with at least one transition (door/area edge)
        n_with_trans = sum(
            1 for f in bwm.faces if f.trans1 is not None or f.trans2 is not None or f.trans3 is not None
        )
        if n_with_trans:
            logger.info(f"Faces with transitions (doors/area links): {n_with_trans} (preserved as-is)")  # noqa: G004

        # ---- What we regenerate ----
        logger.info("Regenerating derived data from geometry:")  # noqa: G004
        logger.info("  - AABB tree (spatial acceleration; WOK only)")  # noqa: G004
        logger.info("  - Adjacency table (which face borders which, by shared edges)")  # noqa: G004
        logger.info("  - Perimeter edges (boundary edges with no walkable neighbor)")  # noqa: G004
        logger.info("  - Perimeter loop markers (where each boundary loop ends)")  # noqa: G004
        logger.info("  - Face normals and planar distances (from vertex positions)")  # noqa: G004
        logger.info("Transitions (trans1/trans2/trans3) on faces are preserved and re-emitted on the edge list.")  # noqa: G004

        # ---- Write ----
        logger.info(f"Writing binary to: {output_path} (AABB tree, adjacency, perimeter edges, and loop markers from geometry)...")  # noqa: G004
        sys.stdout.flush()
        sys.stderr.flush()
        write_bwm(bwm, output_path)
        out_size = output_path.stat().st_size
        logger.info(f"Wrote: {out_size} bytes. Rebuilt walkmesh: {output_path}")  # noqa: G004

        if getattr(args, "ascii", False):
            ascii_path = output_path.with_suffix(output_path.suffix + ".ascii")
            write_bwm_ascii(bwm, ascii_path)
            logger.info(f"Wrote ASCII: {ascii_path}")  # noqa: G004
    except Exception:
        logger.exception(f"Failed to rebuild walkmesh {input_path}")  # noqa: G004
        return 1
    return 0


def cmd_walkmesh_convert(args: Namespace, logger: Logger) -> int:
    """Convert walkmesh BWM/WOK to/from ASCII.

    Usage:
        pykotor walkmesh-convert --input 203tell.wok --to-ascii
        pykotor walkmesh-convert --input 203tell.wok.ascii --to-binary
    """
    input_path = pathlib.Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")  # noqa: G004
        return 1

    to_ascii = getattr(args, "to_ascii", False)
    to_binary = getattr(args, "to_binary", False)
    if to_ascii and to_binary:
        logger.error("Specify only one of --to-ascii or --to-binary")
        return 1
    if not to_ascii and not to_binary:
        # Auto-detect from extension
        if input_path.suffix.lower() == ".ascii":
            to_binary = True
        else:
            to_ascii = True

    if args.output:
        output_path = pathlib.Path(args.output)
    elif to_ascii:
        output_path = input_path.with_suffix(input_path.suffix + ".ascii")
    else:
        output_path = input_path.with_suffix("").with_suffix(".wok") if input_path.suffix.lower() == ".ascii" else input_path.with_suffix(".wok")

    try:
        if to_ascii:
            convert_bwm_to_ascii(input_path, output_path)
            logger.info(f"Converted {input_path.name} to ASCII: {output_path}")  # noqa: G004
        else:
            convert_ascii_to_bwm(input_path, output_path)
            logger.info(f"Converted {input_path.name} to binary: {output_path}")  # noqa: G004
    except Exception:
        logger.exception(f"Failed to convert walkmesh {input_path}")  # noqa: G004
        return 1
    return 0
