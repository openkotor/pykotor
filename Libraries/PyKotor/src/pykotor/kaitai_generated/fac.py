# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from . import gff
if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Fac(KaitaiStruct):
    """FAC (Faction) files are GFF-based format files that store faction relationships,
    reputation values, and faction metadata.
    
    This format inherits the complete GFF structure from gff.ksy and adds FAC-specific
    validation and documentation.
    
    FAC Root Struct Fields:
    - FactionName (String): Faction identifier
    - FactionParentID (UInt16): Parent faction ID
    - FactionGlobal (UInt16): Global faction flag
    - RepList (List): Reputation values with other factions
      - FactionID (UInt32): Target faction ID
      - FactionRep (UInt32): Reputation value (0-100)
    
    References:
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-FAC.md
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-File-Format.md
    - https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/fac.py
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Fac, self).__init__(_io)
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
        """Validates FAC file type."""
        if hasattr(self, '_m_file_type_valid'):
            return self._m_file_type_valid

        self._m_file_type_valid = self.gff_data.header.file_type == u"FAC "
        return getattr(self, '_m_file_type_valid', None)

    @property
    def version_valid(self):
        """Validates GFF version."""
        if hasattr(self, '_m_version_valid'):
            return self._m_version_valid

        self._m_version_valid =  ((self.gff_data.header.file_version == u"V3.2") or (self.gff_data.header.file_version == u"V3.3") or (self.gff_data.header.file_version == u"V4.0") or (self.gff_data.header.file_version == u"V4.1")) 
        return getattr(self, '_m_version_valid', None)


