# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from . import gff
if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Gui(KaitaiStruct):
    """GUI (Graphical User Interface) files define UI layouts, controls, and properties.
    
    This format inherits the complete GFF structure from gff.ksy.
    
    GUI Root Struct Fields:
    - CONTROLS (List): UI control elements (buttons, labels, listboxes, etc.)
    - Each control contains:
      - CONTROLTYPE (Int32): Control type (button=4, label=5, listbox=9, etc.)
      - TAG (String): Control identifier
      - X, Y, WIDTH, HEIGHT (Int32): Position and size
      - TEXT (Struct): Text properties with STRREF, color, alignment
      - BORDER (Struct): Border properties
      - EXTENT (Struct): Dimensions
      - Various control-specific fields
    
    References:
    - https://github.com/OldRepublicDevs/PyKotor/wiki/GFF-GUI.md
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(Gui, self).__init__(_io)
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

        self._m_file_type_valid = self.gff_data.header.file_type == u"GUI "
        return getattr(self, '_m_file_type_valid', None)

    @property
    def version_valid(self):
        if hasattr(self, '_m_version_valid'):
            return self._m_version_valid

        self._m_version_valid =  ((self.gff_data.header.file_version == u"V3.2") or (self.gff_data.header.file_version == u"V3.3") or (self.gff_data.header.file_version == u"V4.0") or (self.gff_data.header.file_version == u"V4.1")) 
        return getattr(self, '_m_version_valid', None)


