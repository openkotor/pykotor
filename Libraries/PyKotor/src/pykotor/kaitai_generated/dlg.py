# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from . import gff
if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Dlg(KaitaiStruct):
    """DLG (Dialogue) files are GFF-based format files that store conversation trees with entries, replies,
    links, and conversation metadata for Odyssey and Aurora engines.
    
    This format inherits the complete GFF structure from gff.ksy and adds DLG-specific
    validation and documentation.
    
    DLG files contain:
    - Root struct with conversation metadata (NumWords, Skippable, ConversationType, etc.)
    - EntryList: Array of dialogue entries (NPC lines)
    - ReplyList: Array of reply options (player responses)
    - StartingList: Array of entry points into conversation tree
    - StuntList: Array of cutscene/animation sequences
    
    References:
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-DLG.md
    - https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/src/pykotor/resource/generics/dlg/
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Dlg, self).__init__(_io)
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
        """Validates DLG file type."""
        if hasattr(self, '_m_file_type_valid'):
            return self._m_file_type_valid

        self._m_file_type_valid = self.gff_data.header.file_type == u"DLG "
        return getattr(self, '_m_file_type_valid', None)

    @property
    def version_valid(self):
        """Validates GFF version."""
        if hasattr(self, '_m_version_valid'):
            return self._m_version_valid

        self._m_version_valid =  ((self.gff_data.header.file_version == u"V3.2") or (self.gff_data.header.file_version == u"V3.3") or (self.gff_data.header.file_version == u"V4.0") or (self.gff_data.header.file_version == u"V4.1")) 
        return getattr(self, '_m_version_valid', None)


