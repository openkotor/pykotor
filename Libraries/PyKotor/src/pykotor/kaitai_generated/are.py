# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from . import gff
if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Are(KaitaiStruct):
    """ARE (Area) files are GFF-based format files that store static area information including
    lighting, fog, grass, weather, script hooks, and map data. ARE files use the GFF (Generic File Format)
    binary structure with file type signature "ARE ".
    
    This format inherits the complete GFF structure from gff.ksy and adds ARE-specific
    validation and documentation.
    
    ARE Root Struct Fields (Common):
    - "Tag" (String): Unique area identifier
    - "Name" (LocalizedString): Area display name
    - "SunAmbientColor", "SunDiffuseColor" (UInt32): Lighting colors (BGR format)
    - "SunFogOn", "SunFogNear", "SunFogFar", "SunFogColor": Fog settings
    - "Grass_*": Grass rendering properties
    - "OnEnter", "OnExit", "OnHeartbeat", "OnUserDefined": Script hooks (ResRef)
    - "Map" (Struct): Minimap coordinate mapping
    - "Rooms" (List): Audio zones and weather regions
    
    KotOR 2 adds weather fields:
    - "ChanceRain", "ChanceSnow", "ChanceLightning" (Int32)
    - "Dirty*" fields for dust particle effects
    
    References:
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-ARE.md
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-File-Format.md
    - https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/are.py
    - https://github.com/seedhartha/reone/blob/master/src/libs/resource/parser/gff/are.cpp
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Are, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.gff_data = gff.Gff(self._io)


    def _fetch_instances(self):
        pass
        self.gff_data._fetch_instances()

    @property
    def file_type_valid(self):
        """Validates that this is an ARE file (file type must be "ARE ")."""
        if hasattr(self, '_m_file_type_valid'):
            return self._m_file_type_valid

        self._m_file_type_valid = self.gff_data.header.file_type == u"ARE "
        return getattr(self, '_m_file_type_valid', None)

    @property
    def root_struct_resolved(self):
        """Convenience access to the decoded GFF root struct (struct_array[0]).
        Use this to iterate all resolved fields (label + typed value), including:
        "Tag", "Name", "AlphaTest", "Map" (struct), "Rooms" (list), and all KotOR2/deprecated keys."""
        if hasattr(self, '_m_root_struct_resolved'):
            return self._m_root_struct_resolved

        self._m_root_struct_resolved = self.gff_data.root_struct_resolved
        return getattr(self, '_m_root_struct_resolved', None)

    @property
    def version_valid(self):
        """Validates GFF version is supported."""
        if hasattr(self, '_m_version_valid'):
            return self._m_version_valid

        self._m_version_valid =  ((self.gff_data.header.file_version == u"V3.2") or (self.gff_data.header.file_version == u"V3.3") or (self.gff_data.header.file_version == u"V4.0") or (self.gff_data.header.file_version == u"V4.1")) 
        return getattr(self, '_m_version_valid', None)


