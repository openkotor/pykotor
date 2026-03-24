# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from . import gff
if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Pt(KaitaiStruct):
    """PT (Party Table) files are GFF-based format files that store party and game state information
    for Odyssey Engine games (KotOR and KotOR 2). PT files use the GFF (Generic File Format) binary
    structure with file type signature "PT  ".
    
    This format inherits the complete GFF structure from gff.ksy and adds PT-specific
    validation and documentation.
    
    PT files are typically named "PARTYTABLE.res" and are stored in savegame.sav ERF archives.
    They contain comprehensive party and game state information including:
    - Party composition (current members, available NPCs, leader)
    - Resources (gold/credits, XP pool, components, chemicals)
    - Journal entries with states, dates, and times
    - Pazaak cards and side decks for the mini-game
    - UI state (last panel, messages, tutorial windows shown)
    - AI state (follow mode, AI enabled, solo mode)
    - K2-specific: Influence values per companion
    
    PT Root Struct Fields (Common):
    - "PT_PCNAME" (String): Player character name
    - "PT_GOLD" (Int32): Credits/gold amount
    - "PT_XP_POOL" (Int32): Experience points
    - "PT_PLAYEDSECONDS" (UInt32): Total playtime in seconds
    - "PT_NUM_MEMBERS" (Int32): Party member count
    - "PT_CONTROLLED_NPC", "PT_SOLOMODE", "PT_AISTATE", "PT_FOLLOWSTATE" (Int32): AI/party state
    - "PT_MEMBERS" (List): Party member ResRefs and leader flags
    - "PT_AVAIL_NPCS" (List): Available NPCs for recruitment
    - "PT_INFLUENCE" (List): Influence values (KotOR 2 only)
    - "PT_PAZAAKCARDS", "PT_PAZSIDELIST" (List): Pazaak card collections
    - Journal/message lists: "PT_FB_MSG_LIST", "PT_DLG_MSG_LIST", "PT_COM_MSG_LIST"
    
    Based on swkotor2.exe: SavePartyTable @ 0x0057bd70
    
    References:
    - https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/savedata.py
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-PT.md
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-File-Format.md
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Pt, self).__init__(_io)
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
        """Validates that this is a PT file (file type must be "PT  ")."""
        if hasattr(self, '_m_file_type_valid'):
            return self._m_file_type_valid

        self._m_file_type_valid = self.gff_data.header.file_type == u"PT  "
        return getattr(self, '_m_file_type_valid', None)

    @property
    def version_valid(self):
        """Validates GFF version is supported."""
        if hasattr(self, '_m_version_valid'):
            return self._m_version_valid

        self._m_version_valid =  ((self.gff_data.header.file_version == u"V3.2") or (self.gff_data.header.file_version == u"V3.3") or (self.gff_data.header.file_version == u"V4.0") or (self.gff_data.header.file_version == u"V4.1")) 
        return getattr(self, '_m_version_valid', None)


