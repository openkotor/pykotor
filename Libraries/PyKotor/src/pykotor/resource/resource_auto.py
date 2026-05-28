"""Unified read/write and type dispatch for KotOR resources.

This module provides read_resource, resource_to_bytes, and dismantle_generic so callers
can work with sources and high-level types (ARE, DLG, GIT, etc.) without format-specific imports.
"""

from __future__ import annotations

import os

from contextlib import suppress
from pathlib import PurePath
from typing import TYPE_CHECKING, Union

from pykotor.extract.file import ResourceIdentifier
from pykotor.resource.formats.bwm import bytes_bwm, read_bwm
from pykotor.resource.formats.bwm.bwm_data import BWM
from pykotor.resource.formats.erf import bytes_erf, read_erf
from pykotor.resource.formats.erf.erf_data import ERF
from pykotor.resource.formats.gff import GFFContent, bytes_gff, read_gff
from pykotor.resource.formats.gff.gff_data import GFF
from pykotor.resource.formats.lip import bytes_lip, read_lip
from pykotor.resource.formats.lip.lip_data import LIP
from pykotor.resource.formats.ltr import bytes_ltr, read_ltr
from pykotor.resource.formats.ltr.ltr_data import LTR
from pykotor.resource.formats.lyt import bytes_lyt, read_lyt
from pykotor.resource.formats.lyt.lyt_data import LYT
from pykotor.resource.formats.mdl import MDL, bytes_mdl, read_mdl
from pykotor.resource.formats.ncs import bytes_ncs, read_ncs
from pykotor.resource.formats.ncs.ncs_data import NCS
from pykotor.resource.formats.rim import bytes_rim, read_rim
from pykotor.resource.formats.rim.rim_data import RIM
from pykotor.resource.formats.ssf import bytes_ssf, read_ssf
from pykotor.resource.formats.ssf.ssf_data import SSF
from pykotor.resource.formats.tlk import bytes_tlk, read_tlk
from pykotor.resource.formats.tlk.tlk_data import TLK
from pykotor.resource.formats.tpc import bytes_tpc, read_tpc
from pykotor.resource.formats.tpc.tpc_data import TPC
from pykotor.resource.formats.twoda import bytes_2da, read_2da
from pykotor.resource.formats.twoda.twoda_data import TwoDA
from pykotor.resource.formats.vis import bytes_vis, read_vis
from pykotor.resource.formats.vis.vis_data import VIS
from pykotor.resource.generics.are import ARE, dismantle_are
from pykotor.resource.generics.dlg import DLG, dismantle_dlg
from pykotor.resource.generics.fac import FAC, dismantle_fac
from pykotor.resource.generics.git import GIT, dismantle_git
from pykotor.resource.generics.gui import GUI, dismantle_gui
from pykotor.resource.generics.ifo import IFO, dismantle_ifo
from pykotor.resource.generics.jrl import JRL, dismantle_jrl
from pykotor.resource.generics.pth import PTH, dismantle_pth
from pykotor.resource.generics.utc import UTC, dismantle_utc
from pykotor.resource.generics.utd import UTD, dismantle_utd
from pykotor.resource.generics.ute import UTE, dismantle_ute
from pykotor.resource.generics.uti import UTI, dismantle_uti
from pykotor.resource.generics.utm import UTM, dismantle_utm
from pykotor.resource.generics.utp import UTP, dismantle_utp
from pykotor.resource.generics.uts import UTS, dismantle_uts
from pykotor.resource.generics.utt import UTT, dismantle_utt
from pykotor.resource.generics.utw import UTW, dismantle_utw
from pykotor.resource.type import ResourceType

if TYPE_CHECKING:
    from pykotor.resource.type import SOURCE_TYPES


def read_resource(  # noqa: C901, PLR0911, PLR0912
    source: SOURCE_TYPES,
    resource_type: ResourceType | None = None,
) -> bytes:
    """Reads a resource from a source and returns it as bytes.

    This is a convenience method to make getting the resource's data easier.
    Can handle various formats (XML/CSV/JSON etc).

    Args:
    ----
        source: SOURCE_TYPES: The source of the resource
        resource_type: ResourceType | None: The type of the resource

    Returns:
    -------
        bytes: The resource data as bytes
    """
    source_path: os.PathLike | str | None = None
    with suppress(Exception):
        if isinstance(source, (os.PathLike, str)):
            source_path = source
            if not resource_type:
                _resname, resource_type = ResourceIdentifier.from_path(source).unpack()

    if not resource_type:
        return read_unknown_resource(source)

    try:  # dispatch by category/extension for maintainability
        ext_obj = PurePath(resource_type.extension)
        resource_ext = ext_obj.stem.lower() if "." in ext_obj.name else ext_obj.suffix.lower()[1:]

        # Category-based dispatch
        if resource_type.category == "Talk Tables":
            return bytes_tlk(read_tlk(source))
        if resource_type.category == "Walkmeshes":
            return bytes_bwm(read_bwm(source))
        if resource_type in {ResourceType.TGA, ResourceType.TPC}:
            return bytes_tpc(read_tpc(source))

        # Extension-based dispatch (O(1) lookup, single place to add new types)
        handler = _READ_RESOURCE_BY_EXT.get(resource_ext)
        if handler is not None:
            return handler(source)

        if ResourceType.from_extension(resource_ext) in (
            ResourceType.ERF,
            ResourceType.MOD,
            ResourceType.SAV,
        ):
            return bytes_erf(read_erf(source))
        if resource_type.extension.upper() in GFFContent.__members__:
            return bytes_gff(read_gff(source))
    except Exception as e:  # pylint: disable=W0718  # noqa: BLE001
        new_err = ValueError(
            f"Could not load resource '{source_path}' as resource type '{resource_type}"
        )
        print((new_err.__class__.__name__, str(new_err)))
        raise new_err from e

    msg = f"Resource type {resource_type!r} is not supported by this library."
    raise ValueError(msg)


def read_unknown_resource(  # noqa: PLR0911
    source: SOURCE_TYPES,
) -> bytes:
    with suppress(OSError, ValueError):
        return bytes_tlk(read_tlk(source))
    with suppress(OSError, ValueError):
        return bytes_ssf(read_ssf(source))
    with suppress(OSError, ValueError):
        return bytes_2da(read_2da(source))
    with suppress(OSError, ValueError):
        return bytes_lip(read_lip(source))
    with suppress(OSError, ValueError):
        return bytes_tpc(read_tpc(source))
    with suppress(OSError, ValueError):
        return bytes_erf(read_erf(source))
    with suppress(OSError, ValueError):
        return bytes_rim(read_rim(source))
    with suppress(OSError, ValueError):
        return bytes_ncs(read_ncs(source))
    with suppress(OSError, ValueError):
        return bytes_gff(read_gff(source))
    with suppress(OSError, ValueError):
        return bytes_mdl(read_mdl(source))
    with suppress(OSError, ValueError):
        return bytes_vis(read_vis(source))
    with suppress(OSError, ValueError):
        return bytes_lyt(read_lyt(source))
    with suppress(OSError, ValueError):
        return bytes_ltr(read_ltr(source))
    with suppress(OSError, ValueError):
        return bytes_bwm(read_bwm(source))
    msg = "Source resource data not recognized as any kotor file formats."
    raise ValueError(msg)


GFF_GENERICS = Union[ARE, DLG, GIT, IFO, JRL, PTH, UTC, UTD, UTE, UTM, UTP, UTS, UTW]


def dismantle_generic(  # noqa: PLR0911, C901, PLR0912, ANN201
    generic: GFF_GENERICS,
) -> GFF:
    """Returns a GFF object from a constructed obj.

    Args:
    ----
        generic: The constructed loaded object to deconstruct into GFF (e.g. DLG, PTH, IFO...)

    Returns:
    -------
        A deconstructed_gff
    """
    for generic_type, dismantler in _GENERIC_DISMANTLERS:
        if isinstance(generic, generic_type):
            return dismantler(generic)
    if isinstance(generic, GFF):
        return generic  # Guess whoever called this didn't get the memo.
    raise TypeError(
        f"Could not dismantle generic, invalid object passed ({generic}) of type '{type(generic).__name__}' was unexpected."
    )


def resource_to_bytes(  # noqa: PLR0912, C901, PLR0911
    resource: BWM | ERF | GFF | LIP | LTR | LYT | MDL | NCS | RIM | SSF | TLK | TPC | TwoDA | VIS | GFF_GENERICS,
) -> bytes:
    if isinstance(resource, GFF_GENERICS):
        return bytes_gff(dismantle_generic(resource))
    for resource_type, serializer in _RESOURCE_SERIALIZERS:
        if isinstance(resource, resource_type):
            return serializer(resource)
    raise TypeError(
        f"Invalid resource {resource} of type '{type(resource).__name__}' passed to `resource_to_bytes`."
    )
