"""Path and file-type helpers for KotOR resources.

This module provides normalized path/suffix handling and predicates for
common KotOR file extensions (NSS, MOD, ERF, RIM, BIF, etc.) used across
tools and resource loading.
"""

from __future__ import annotations

from pathlib import PurePath
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import os


def normalize_ext(
    str_repr: os.PathLike | str,
) -> os.PathLike | str:
    if isinstance(str_repr, str):
        if not str_repr:
            return ""
        if str_repr[0] == ".":
            return f"stem{str_repr}"
        if "." not in str_repr:
            return f"stem.{str_repr}"
    return str_repr


def normalize_stem(
    str_repr: os.PathLike | str,
) -> os.PathLike | str:
    if isinstance(str_repr, str):
        if not str_repr:
            return ""
        if str_repr[-1:] == ".":
            return f"{str_repr}ext"
        if "." not in str_repr:
            return f"{str_repr}.ext"
    return str_repr


def is_nss_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has a NSS file extension."""
    return is_file_type(filepath, "nss")


def is_mod_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has a MOD file extension."""
    return is_file_type(filepath, "mod")


def is_erf_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has a ERF file extension."""
    return is_file_type(filepath, "erf")


def is_sav_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has a SAV file extension."""
    return is_file_type(filepath, "sav")


def is_any_erf_type_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has either an ERF, MOD, or SAV file extension."""
    return _suffix_in(filepath, _SUFFIX_ERF_TYPES)


def is_rim_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has a RIM file extension."""
    return _normalized_suffix(filepath) == ".rim"


def is_bif_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has a BIF file extension."""
    return _has_suffix(filepath, ".bif")


def is_bzf_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has a BZF file extension (lzma-compressed bif archive usually used on iOS)."""
    return _has_suffix(filepath, ".bzf")


def is_capsule_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has either an ERF, MOD, SAV, or RIM file extension."""
    return _suffix_in(filepath, _SUFFIX_CAPSULE)


def is_storage_file(
    filepath: os.PathLike | str,
) -> bool:
    """Returns true if the given filename has either an ERF, MOD, SAV, RIM, or BIF file extension."""
    return _suffix_in(filepath, _SUFFIX_STORAGE)
