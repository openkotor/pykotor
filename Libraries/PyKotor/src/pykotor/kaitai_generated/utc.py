# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from . import gff
if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Utc(KaitaiStruct):
    """UTC (Creature Template) files are GFF-based format files that store creature definitions
    including stats, appearance, inventory, feats, and script hooks. UTC files are used to
    define NPCs, party members, enemies, and the player character in Knights of the Old Republic.
    
    This format inherits the complete GFF structure from gff.ksy and adds UTC-specific
    validation and documentation.
    
    UTC Root Struct Fields (Common):
    - "TemplateResRef" (ResRef): Blueprint identifier
    - "Tag" (String): Unique instance identifier
    - "FirstName", "LastName" (LocalizedString): Creature name
    - "Appearance_Type" (UInt32): Appearance ID (appearance.2da)
    - "PortraitId" (UInt16): Portrait index (portraits.2da)
    - "Gender", "Race" (UInt8/UInt16): Character attributes
    - "Str", "Dex", "Con", "Int", "Wis", "Cha" (UInt8): Ability scores
    - "HitPoints", "MaxHitPoints", "ForcePoints" (Int16): Health/Force stats
    - "ClassList" (List): Character classes with levels
    - "FeatList" (List): Known feats
    - "SkillList" (List): Skill ranks
    - "ItemList" (List): Inventory items
    - "Equip_ItemList" (List): Equipped items with slots
    - Script hooks: "ScriptAttacked", "ScriptDamaged", "ScriptDeath", etc. (ResRef)
    
    References:
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-UTC.md
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-File-Format.md
    - https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/generics/utc.py
    - https://github.com/seedhartha/reone/blob/master/src/libs/resource/parser/gff/utc.cpp
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Utc, self).__init__(_io)
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
        """Validates that this is a UTC file (file type must be "UTC ")."""
        if hasattr(self, '_m_file_type_valid'):
            return self._m_file_type_valid

        self._m_file_type_valid = self.gff_data.header.file_type == u"UTC "
        return getattr(self, '_m_file_type_valid', None)

    @property
    def version_valid(self):
        """Validates GFF version is supported."""
        if hasattr(self, '_m_version_valid'):
            return self._m_version_valid

        self._m_version_valid =  ((self.gff_data.header.file_version == u"V3.2") or (self.gff_data.header.file_version == u"V3.3") or (self.gff_data.header.file_version == u"V4.0") or (self.gff_data.header.file_version == u"V4.1")) 
        return getattr(self, '_m_version_valid', None)


