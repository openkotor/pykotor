"""Binary ERF (encapsulated resource) read/write: header, key list, resource data."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pykotor.resource.formats.erf.erf_data import ERF, ERFType
from pykotor.resource.type import ResourceReader, ResourceType, ResourceWriter, autoclose

if TYPE_CHECKING:
    from pykotor.resource.type import SOURCE_TYPES, TARGET_TYPES

_MAX_SANE_COUNT = 65536
_MAX_SANE_LANG_COUNT = 32


def _load_erf_from_kaitai(data: bytes) -> ERF:
    parsed = Erf.from_bytes(data)
    h = parsed.header
    file_size = len(data)
    erf_type: ERFType | None = next((x for x in ERFType if x.value == h.file_type), None)
    if erf_type is None:
        msg = f"Not a valid ERF file: '{h.file_type}'"
        raise ValueError(msg)
    erf = ERF(erf_type)
    entry_count = h.entry_count
    offset_to_keys = h.offset_to_key_list
    offset_to_resources = h.offset_to_resource_list
    offset_to_localized_strings = h.offset_to_localized_string_list
    language_count = h.language_count

    erf.build_year = h.build_year
    erf.build_day = h.build_day
    erf.description_strref = int(h.description_strref)

    if entry_count > _MAX_SANE_COUNT:
        msg = f"ERF entry_count {entry_count} exceeds sanity limit; file may be malformed or truncated."
        raise ValueError(msg)

    if offset_to_keys >= file_size and entry_count > 0:
        msg = f"ERF offset_to_keys {offset_to_keys} is beyond file size {file_size}; file is malformed."
        raise ValueError(msg)

    if offset_to_resources >= file_size and entry_count > 0:
        msg = f"ERF offset_to_resources {offset_to_resources} is beyond file size {file_size}; file is malformed."
        raise ValueError(msg)

    if language_count > 0 and offset_to_localized_strings > 0:
        if language_count > _MAX_SANE_LANG_COUNT:
            msg = (
                f"ERF language_count {language_count} exceeds sanity limit; file may be malformed."
            )
            raise ValueError(msg)
        lsl = parsed.localized_string_list
        if lsl is not None:
            for e in lsl.entries:
                erf.localized_strings[e.language_id] = e.string_data

    kl = parsed.key_list
    rl = parsed.resource_list
    if entry_count == 0:
        return erf
    if kl is None or rl is None or len(kl.entries) != entry_count or len(rl.entries) != entry_count:
        msg = "ERF key/resource list size mismatch."
        raise ValueError(msg)

    for i in range(entry_count):
        ke = kl.entries[i]
        resref_str = ke.resref.split("\0", 1)[0].rstrip("\0")
        restype_id = int(ke.resource_type)
        off = int(rl.entries[i].offset_to_data)
        sz = int(rl.entries[i].resource_size)
        if off + sz > file_size:
            msg = f"ERF resource {i} extends past file (offset={off}, size={sz}, file={file_size})."
            raise ValueError(msg)
        erf.set_data(resref_str, ResourceType.from_id(restype_id), data[off : off + sz])

    return erf


def _load_erf_legacy(reader: BinaryReader, file_size: int) -> ERF:
    file_type: str = reader.read_string(4)
    file_version: str = reader.read_string(4)

    if file_version != "V1.0":
        msg = f"ERF version '{file_version}' is unsupported."
        raise ValueError(msg)

    erf_type: ERFType | None = next(
        (x for x in ERFType if x.value == file_type),
        None,
    )
    if erf_type is None:
        msg = f"Not a valid ERF file: '{file_type}'"
        raise ValueError(msg)

    erf = ERF(erf_type)

    language_count: int = reader.read_uint32()
    localized_string_size: int = reader.read_uint32()
    entry_count: int = reader.read_uint32()
    offset_to_localized_strings: int = reader.read_uint32()
    offset_to_keys: int = reader.read_uint32()
    offset_to_resources: int = reader.read_uint32()

    erf.build_year = reader.read_uint32()
    erf.build_day = reader.read_uint32()
    erf.description_strref = reader.read_uint32()

    if offset_to_keys == 0:
        offset_to_keys = 160

    if offset_to_resources == 0:
        offset_to_resources = offset_to_keys + (entry_count * 24)

    if entry_count > _MAX_SANE_COUNT:
        msg = f"ERF entry_count {entry_count} exceeds sanity limit; file may be malformed or truncated."
        raise ValueError(msg)

    if offset_to_keys >= file_size and entry_count > 0:
        msg = f"ERF offset_to_keys {offset_to_keys} is beyond file size {file_size}; file is malformed."
        raise ValueError(msg)

    if offset_to_resources >= file_size and entry_count > 0:
        msg = f"ERF offset_to_resources {offset_to_resources} is beyond file size {file_size}; file is malformed."
        raise ValueError(msg)

    if language_count > 0 and offset_to_localized_strings > 0:
        if language_count > _MAX_SANE_LANG_COUNT:
            msg = (
                f"ERF language_count {language_count} exceeds sanity limit; file may be malformed."
            )
            raise ValueError(msg)
        reader.seek(offset_to_localized_strings)
        block_end = offset_to_localized_strings + localized_string_size
        for _ in range(language_count):
            if reader.position() >= block_end:
                break
            lang_id = reader.read_uint32()
            str_size = reader.read_uint32()
            remaining_block = block_end - reader.position()
            if str_size > remaining_block:
                msg = f"ERF localized string size {str_size} exceeds remaining block size {remaining_block}."
                raise ValueError(msg)
            text = reader.read_string(str_size, encoding="windows-1252")
            erf.localized_strings[lang_id] = text

    resrefs: list[str] = []
    restypes: list[int] = []
    reader.seek(offset_to_keys)
    for _ in range(entry_count):
        resref_str = reader.read_string(16).rstrip("\0")
        resrefs.append(resref_str)
        reader.read_uint32()
        restypes.append(reader.read_uint16())
        reader.skip(2)

    resoffsets: list[int] = []
    ressizes: list[int] = []
    reader.seek(offset_to_resources)
    for _ in range(entry_count):
        resoffsets.append(reader.read_uint32())
        ressizes.append(reader.read_uint32())

    for i in range(entry_count):
        reader.seek(resoffsets[i])
        resdata: bytes = reader.read_bytes(ressizes[i])
        erf.set_data(resrefs[i], ResourceType.from_id(restypes[i]), resdata)

    return erf


class ERFBinaryReader(ResourceReader):
    """Reads ERF (Encapsulated Resource File) files.
    
    ERF files are container formats that store multiple game resources. Used for MOD files,
    save games, and other resource collections.
    
    References:
    ----------
        vendor/reone/src/libs/resource/format/erfreader.cpp:26-72 (ERF reading)
        vendor/reone/src/libs/resource/format/erfwriter.cpp (ERF writing)
        vendor/xoreos-tools/src/unerf.cpp:108-145 (password/decryption support)
    
    Missing Features:
    ----------------
        - ResRef lowercasing (reone lowercases at erfreader.cpp:63)
        - ERF password/decryption support (xoreos-tools supports at unerf.cpp:108-145)
    """
    def __init__(
        self,
        source: SOURCE_TYPES,
        offset: int = 0,
        size: int = 0,
    ):
        super().__init__(source, offset, size)
        self._erf: ERF | None = None

    @autoclose
    def load(self, *, auto_close: bool = True) -> ERF:  # noqa: FBT001, FBT002, ARG002
        """Load ERF file.

        Args:
        ----
            self: The ERF object

        Returns:
        -------
            ERF: The loaded ERF object

        Processing Logic:
        ----------------
            - Read file header and validate file type and version
            - Read entry count and offsets to keys and resources sections
            - Read keys section into lists of ref, id, type
            - Read resources section into lists of offsets and sizes
            - Seek to each resource and read data into ERF object.
        """
        file_type: str = self._reader.read_string(4)
        file_version: str = self._reader.read_string(4)

        if file_version != "V1.0":
            msg = f"ERF version '{file_version}' is unsupported."
            raise ValueError(msg)

        erf_type: ERFType | None = next(
            (x for x in ERFType if x.value == file_type),
            None,
        )
        if erf_type is None:
            msg = f"Not a valid ERF file: '{file_type}'"
            raise ValueError(msg)

        self._erf = ERF(erf_type)

        self._reader.skip(8)
        entry_count: int = self._reader.read_uint32()
        self._reader.skip(4)
        offset_to_keys: int = self._reader.read_uint32()
        offset_to_resources: int = self._reader.read_uint32()
        self._reader.skip(8)
        description_strref: int = self._reader.read_uint32()
        if description_strref == 0 and file_type == ERFType.MOD.value:  # estimated guess based on observed files
            self._erf.is_save = True

        resrefs: list[str] = []
        resids: list[int] = []
        restypes: list[int] = []
        self._reader.seek(offset_to_keys)
        for _ in range(entry_count):
            # vendor/reone/src/libs/resource/format/erfreader.cpp:62-72
            # reone lowercases resrefs at line 63
            resref_str = self._reader.read_string(16).rstrip("\0")
            resrefs.append(resref_str.lower())
            resids.append(self._reader.read_uint32())
            restypes.append(self._reader.read_uint16())
            self._reader.skip(2)

        resoffsets: list[int] = []
        ressizes: list[int] = []
        self._reader.seek(offset_to_resources)
        for _ in range(entry_count):
            resoffsets.append(self._reader.read_uint32())
            ressizes.append(self._reader.read_uint32())

        for i in range(entry_count):
            self._reader.seek(resoffsets[i])
            resdata: bytes = self._reader.read_bytes(ressizes[i])
            self._erf.set_data(resrefs[i], ResourceType.from_id(restypes[i]), resdata)

        return self._erf


class ERFBinaryWriter(ResourceWriter):
    FILE_HEADER_SIZE = 160
    KEY_ELEMENT_SIZE = 24
    RESOURCE_ELEMENT_SIZE = 8

    def __init__(
        self,
        erf: ERF,
        target: TARGET_TYPES,
    ):
        super().__init__(target)
        self.erf: ERF = erf

    @autoclose
    def write(self, *, auto_close: bool = True):  # noqa: FBT001, FBT002, ARG002  # pyright: ignore[reportUnusedParameters]
        entry_count: int = len(self.erf)
        offset_to_keys: int = ERFBinaryWriter.FILE_HEADER_SIZE
        offset_to_resources: int = offset_to_keys + ERFBinaryWriter.KEY_ELEMENT_SIZE * entry_count
        offset_to_localized_strings: int = 0x0
        description_strref_dword_value: int = 0xFFFFFFFF
        if self.erf.is_save:
            # might matter.
            offset_to_localized_strings = 0xA0
            description_strref_dword_value = 0x00000000
        elif self.erf.erf_type is ERFType.ERF:
            # default, also doesn't matter
            offset_to_localized_strings = 0x69
            description_strref_dword_value = 0xCDCDCDCD
        elif self.erf.erf_type is ERFType.MOD:
            # mod's aren't in the vanilla game, doesn't matter
            offset_to_localized_strings = 0x0
            description_strref_dword_value = 0xFFFFFFFF

        self._writer.write_string(self.erf.erf_type.value)
        self._writer.write_string("V1.0")
        self._writer.write_uint32(language_count)
        self._writer.write_uint32(localized_string_block_size)
        self._writer.write_uint32(entry_count)
        self._writer.write_uint32(offset_to_localized_strings)
        self._writer.write_uint32(offset_to_keys)
        self._writer.write_uint32(offset_to_resources)
        self._writer.write_uint32(self.erf.build_year)
        self._writer.write_uint32(self.erf.build_day)
        self._writer.write_uint32(description_strref)
        self._writer.write_bytes(b"\0" * 116)

        # Write Localized Strings
        for lang_id, text in sorted_langs:
            encoded_text = text.encode("windows-1252")
            self._writer.write_uint32(lang_id)
            self._writer.write_uint32(len(encoded_text))
            self._writer.write_bytes(encoded_text)

        for resid, resource in enumerate(self.erf):
            self._writer.write_string(str(resource.resref), string_length=16)
            self._writer.write_uint32(resid)
            self._writer.write_uint16(resource.restype.type_id)
            self._writer.write_uint16(0)
        data_offset: int = offset_to_resources + ERFBinaryWriter.RESOURCE_ELEMENT_SIZE * entry_count
        for resource in self.erf:
            self._writer.write_uint32(data_offset)
            self._writer.write_uint32(len(resource.data))
            data_offset += len(resource.data)

        for resource in self.erf:
            self._writer.write_bytes(resource.data)
