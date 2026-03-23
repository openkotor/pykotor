"""Shared batch-task contracts for Holocron-style tools backed by PyKotor.

Hosts (HolocronToolset, io_scene_kotor) should import these types from
``pykotor.toolset`` so batch logic can live in one place.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class ToolsetBatchOutcome:
    """Tallies for a directory or multi-file batch run."""

    success_count: int = 0
    skipped_count: int = 0
    errors: List[str] = field(default_factory=list)


class ToolsetBatchTask(ABC):
    """Abstract base for toolset batch operations (optional subclass hook)."""

    @abstractmethod
    def run(self) -> ToolsetBatchOutcome:
        raise NotImplementedError
