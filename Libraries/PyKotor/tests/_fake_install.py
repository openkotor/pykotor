"""Utilities for creating minimal but valid fake KotOR installations for testing.

Used by conftest.py files when K1_PATH/K2_PATH env vars are not set or point to
invalid directories. The created installations are sufficient for:
- passing the Installation() constructor (needs chitin.key to exist)
- passing determine_game() heuristics (game-specific sentinel files/dirs)
- constructing HTInstallation (same as above)

All structure is written using the real PyKotor serialization layer so the files
are byte-for-byte valid and indistinguishable from real game files for the purposes
of the unit-test suite.
"""

from __future__ import annotations

import atexit
import logging
import shutil
import tempfile

from pathlib import Path

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level shared temp-dir that lives for the whole pytest session
# ---------------------------------------------------------------------------
_SESSION_TEMP_DIR: Path | None = None


def _get_session_temp_dir() -> Path:
    global _SESSION_TEMP_DIR  # noqa: PLW0603
    if _SESSION_TEMP_DIR is None:
        _SESSION_TEMP_DIR = Path(tempfile.mkdtemp(prefix="pykotor_fake_install_"))
        atexit.register(_cleanup_session_temp_dir)
        log.info("Created session-scoped fake install temp dir: %s", _SESSION_TEMP_DIR)
    return _SESSION_TEMP_DIR


def _cleanup_session_temp_dir() -> None:
    global _SESSION_TEMP_DIR  # noqa: PLW0603
    if _SESSION_TEMP_DIR is not None and _SESSION_TEMP_DIR.exists():
        shutil.rmtree(_SESSION_TEMP_DIR, ignore_errors=True)
        log.debug("Removed session fake install temp dir: %s", _SESSION_TEMP_DIR)
        _SESSION_TEMP_DIR = None


# ---------------------------------------------------------------------------
# Low-level writers (fallback if PyKotor imports fail)
# ---------------------------------------------------------------------------

def _write_key_file(path: Path) -> None:
    """Write a minimal valid empty chitin.key to *path*."""
    try:
        from pykotor.resource.formats.key.key_auto import write_key
        from pykotor.resource.formats.key.key_data import KEY

        write_key(KEY(), path)
    except Exception:
        # Emergency fallback: build a valid KEY V1 header by hand.
        # Layout: file_type(4) file_version(4) bif_count(4) key_count(4)
        #         file_table_offset(4) key_table_offset(4) build_year(4) build_day(4)
        #         reserved(32) = 64 bytes total header
        import struct
        header = struct.pack(
            "<4s4sIIII",
            b"KEY ",
            b"V1  ",
            0,    # bif_count
            0,    # key_count
            64,   # file_table_offset  (directly after header)
            64,   # key_table_offset
        )
        # build_year, build_day, reserved
        header += struct.pack("<II", 0, 0) + b"\x00" * 32
        path.write_bytes(header)


def _write_tlk_file(path: Path) -> None:
    """Write a minimal valid empty TLK to *path*."""
    try:
        from pykotor.common.language import Language
        from pykotor.resource.formats.tlk.tlk_auto import write_tlk
        from pykotor.resource.formats.tlk.tlk_data import TLK

        write_tlk(TLK(language=Language.ENGLISH), path)
    except Exception:
        # Emergency fallback: hand-craft a TLK V3.0 header with zero entries.
        # Layout: file_type(4) file_version(4) language_id(4) str_count(4)
        #         str_entries_offset(4) = 20 bytes; entries start at 20
        import struct
        header = struct.pack(
            "<4s4sII I",
            b"TLK ",
            b"V3.0",
            0,   # language_id  (0 = English)
            0,   # str_count
            20,  # str_entries_offset
        )
        path.write_bytes(header)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_minimal_k1_installation(base_dir: Path | None = None) -> Path:
    """Create a minimal K1 (swkotor) installation and return its root path.

    The installation:
    - satisfies ``Installation.__init__`` (chitin.key + dialog.tlk must exist)
    - causes ``determine_game()`` to return ``Game.K1`` (PC heuristics)
    - contains all canonical sub-directories expected by the test suite

    Args:
        base_dir: Parent directory to create ``fake_k1/`` inside.
                  Defaults to the module-level session temp dir.
    """
    root = (base_dir or _get_session_temp_dir()) / "fake_k1"
    if (root / "chitin.key").exists():
        return root  # already built

    root.mkdir(parents=True, exist_ok=True)

    # --- determine_game K1 PC sentinel files / directories ---
    (root / "streamwaves").mkdir(exist_ok=True)     # strongest K1-only signal
    (root / "swkotor.exe").touch()
    (root / "swkotor.ini").touch()
    (root / "rims").mkdir(exist_ok=True)
    (root / "utils").mkdir(exist_ok=True)

    # --- Standard Installation directory structure ---
    (root / "Data").mkdir(exist_ok=True)
    (root / "Modules").mkdir(exist_ok=True)
    (root / "Override").mkdir(exist_ok=True)
    (root / "StreamMusic").mkdir(exist_ok=True)
    (root / "StreamSounds").mkdir(exist_ok=True)
    (root / "TexturePacks").mkdir(exist_ok=True)
    (root / "Lips").mkdir(exist_ok=True)
    (root / "miles").mkdir(exist_ok=True)

    # Some heuristics check for specific data/*.bif paths
    (root / "data").mkdir(exist_ok=True)
    (root / "data" / "party.bif").touch()
    (root / "data" / "player.bif").touch()

    # Modules folder entries checked by heuristics
    (root / "modules").mkdir(exist_ok=True)
    (root / "modules" / "global.mod").touch()

    # --- Required binary files ---
    _write_key_file(root / "chitin.key")
    _write_tlk_file(root / "dialog.tlk")
    _write_tlk_file(root / "dialogf.tlk")

    log.info("Built minimal K1 fake installation at: %s", root)
    return root


def build_minimal_k2_installation(base_dir: Path | None = None) -> Path:
    """Create a minimal K2/TSL (swkotor2) installation and return its root path.

    The installation:
    - satisfies ``Installation.__init__``
    - causes ``determine_game()`` to return ``Game.K2`` (TSL PC heuristics)
    - contains all canonical sub-directories expected by the test suite

    Args:
        base_dir: Parent directory to create ``fake_k2/`` inside.
                  Defaults to the module-level session temp dir.
    """
    root = (base_dir or _get_session_temp_dir()) / "fake_k2"
    if (root / "chitin.key").exists():
        return root  # already built

    root.mkdir(parents=True, exist_ok=True)

    # --- determine_game K2 PC sentinel files / directories ---
    (root / "streamvoice").mkdir(exist_ok=True)     # strongest K2-only signal
    (root / "swkotor2.exe").touch()
    (root / "swkotor2.ini").touch()
    (root / "LocalVault").mkdir(exist_ok=True)
    (root / "LocalVault" / "test.bic").touch()
    (root / "LocalVault" / "testold.bic").touch()
    (root / "miles").mkdir(exist_ok=True)

    # Some heuristics check for specific data/*.bif paths
    (root / "data").mkdir(exist_ok=True)
    (root / "data" / "Dialogs.bif").touch()

    # --- Standard Installation directory structure ---
    (root / "Data").mkdir(exist_ok=True)
    (root / "Modules").mkdir(exist_ok=True)
    (root / "Override").mkdir(exist_ok=True)
    (root / "StreamMusic").mkdir(exist_ok=True)
    (root / "StreamSounds").mkdir(exist_ok=True)
    (root / "TexturePacks").mkdir(exist_ok=True)
    (root / "Lips").mkdir(exist_ok=True)

    # --- Required binary files ---
    _write_key_file(root / "chitin.key")
    _write_tlk_file(root / "dialog.tlk")
    _write_tlk_file(root / "dialogf.tlk")

    log.info("Built minimal K2 fake installation at: %s", root)
    return root
