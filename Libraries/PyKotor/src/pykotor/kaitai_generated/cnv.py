# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from . import gff
if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Cnv(KaitaiStruct):
    """CNV (Conversation) files are GFF-based format files that store conversation trees with entries, replies,
    links, and conversation metadata. CNV files use the GFF (Generic File Format) binary structure
    with file type signature "CNV ".
    
    This format inherits the complete GFF structure from gff.ksy and adds CNV-specific
    validation and documentation.
    
    CNV files are used by Eclipse Engine games (Dragon Age Origins, Dragon Age 2, Mass Effect, Mass Effect 2).
    They are similar to DLG files used by Odyssey and Aurora engines but adapted for Eclipse's conversation system.
    
    CNV Root Struct Fields:
    - NumWords (Int32): Word count for conversation
    - Skippable (UInt8): Whether conversation can be skipped
    - ConversationType (Int32): Conversation type identifier
    - EntryList (List): NPC dialogue lines (CNVEntry structs)
    - ReplyList (List): Player response options (CNVReply structs)
    - StartingList (List): Entry points (CNVLink structs)
    - StuntList (List): Special animations (CNVStunt structs)
    
    Each Entry/Reply contains:
    - Text (LocalizedString): Dialogue text
    - Script (ResRef): Conditional/action scripts
    - Camera settings, animations, links to other nodes
    
    References:
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-CNV.md
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-File-Format.md
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Cnv, self).__init__(_io)
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
        """Validates that this is a CNV file (file type must be "CNV ")."""
        if hasattr(self, '_m_file_type_valid'):
            return self._m_file_type_valid

        self._m_file_type_valid = self.gff_data.header.file_type == u"CNV "
        return getattr(self, '_m_file_type_valid', None)

    @property
    def version_valid(self):
        """Validates GFF version is supported."""
        if hasattr(self, '_m_version_valid'):
            return self._m_version_valid

        self._m_version_valid =  ((self.gff_data.header.file_version == u"V3.2") or (self.gff_data.header.file_version == u"V3.3") or (self.gff_data.header.file_version == u"V4.0") or (self.gff_data.header.file_version == u"V4.1")) 
        return getattr(self, '_m_version_valid', None)


