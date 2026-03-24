# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from . import gff
if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Utt(KaitaiStruct):
    """UTT (Trigger Template) files define trigger zones and their properties.
    
    This format inherits the complete GFF structure from gff.ksy.
    
    UTT Root Struct Fields:
    - TemplateResRef (ResRef): Blueprint identifier
    - Tag (String): Instance identifier
    - LocalizedName (LocalizedString): Trigger name
    - Geometry (List): Trigger zone vertices
    - TriggerType, Cursor, Faction: Trigger behavior
    - Script hooks: OnClick, OnDisarm, OnHeartbeat, OnTrapTriggered, OnUserDefined
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Utt, self).__init__(_io)
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
        if hasattr(self, '_m_file_type_valid'):
            return self._m_file_type_valid

        self._m_file_type_valid = self.gff_data.header.file_type == u"UTT "
        return getattr(self, '_m_file_type_valid', None)

    @property
    def version_valid(self):
        if hasattr(self, '_m_version_valid'):
            return self._m_version_valid

        self._m_version_valid =  ((self.gff_data.header.file_version == u"V3.2") or (self.gff_data.header.file_version == u"V3.3")) 
        return getattr(self, '_m_version_valid', None)


