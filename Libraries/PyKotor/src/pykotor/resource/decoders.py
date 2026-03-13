"""Central restype -> decoder registry for resource bytes -> domain objects.

Reused by Installation, ModuleResource, and InstallationWorkspace so decode
logic lives in one place. Decoders accept bytes and return the typed domain object
(e.g. read_utc(data) -> UTC).
"""

from __future__ import annotations

from typing import Any, Callable

from pykotor.resource.formats.bwm import read_bwm
from pykotor.resource.formats.gff import read_gff
from pykotor.resource.formats.lyt import read_lyt
from pykotor.resource.formats.tpc import read_tpc
from pykotor.resource.formats.vis import read_vis
from pykotor.resource.generics.are import read_are
from pykotor.resource.generics.dlg import read_dlg
from pykotor.resource.generics.git import read_git
from pykotor.resource.generics.ifo import read_ifo
from pykotor.resource.generics.pth import read_pth
from pykotor.resource.generics.utc import read_utc
from pykotor.resource.generics.utd import read_utd
from pykotor.resource.generics.ute import read_ute
from pykotor.resource.generics.uti import read_uti
from pykotor.resource.generics.utm import read_utm
from pykotor.resource.generics.utp import read_utp
from pykotor.resource.generics.uts import read_uts
from pykotor.resource.generics.utt import read_utt
from pykotor.resource.generics.utw import read_utw
from pykotor.resource.type import ResourceType

# Decoder: bytes -> domain object (GFF, UTC, LYT, etc.)
_DECODER_REGISTRY: dict[ResourceType, Callable[[bytes], Any]] = {
    ResourceType.ARE: read_are,
    ResourceType.DLG: read_dlg,
    ResourceType.GIT: read_git,
    ResourceType.IFO: read_ifo,
    ResourceType.LYT: read_lyt,
    ResourceType.NCS: lambda data: data,
    ResourceType.PTH: read_pth,
    ResourceType.TPC: read_tpc,
    ResourceType.TGA: read_tpc,
    ResourceType.UTD: read_utd,
    ResourceType.UTE: read_ute,
    ResourceType.UTI: read_uti,
    ResourceType.UTM: read_utm,
    ResourceType.UTP: read_utp,
    ResourceType.UTS: read_uts,
    ResourceType.UTT: read_utt,
    ResourceType.UTW: read_utw,
    ResourceType.UTC: read_utc,
    ResourceType.VIS: read_vis,
    ResourceType.WOK: read_bwm,
    ResourceType.GFF: read_gff,
}


def get_decoder(restype: ResourceType) -> Callable[[bytes], Any] | None:
    """Return the decoder for the given ResourceType, or None if none is registered."""
    return _DECODER_REGISTRY.get(restype)
