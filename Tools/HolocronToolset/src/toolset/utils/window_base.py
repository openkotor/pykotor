from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from toolset.utils.window import add_recent_file as _add_recent_file, add_window as _add_window

if TYPE_CHECKING:
    from qtpy.QtWidgets import QDialog, QMainWindow


"""Compatibility wrappers around the canonical window registry in `toolset.utils.window`."""


def add_window(
    window: QDialog | QMainWindow,
) -> None:
    """Prevent Qt garbage collection while preserving legacy no-auto-show behavior."""
    _add_window(window, show=False)


def add_recent_file(
    file: Path,
) -> None:
    """Update the list of recent files."""
    _add_recent_file(file)
