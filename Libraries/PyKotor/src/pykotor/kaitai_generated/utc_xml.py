# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class UtcXml(KaitaiStruct):
    """Human-readable XML representation of UTC (Creature Template) binary files.
    Uses GFF XML structure with <gff3> root element.
    
    Binary format reference: ../utc/utc.ksy
    
    References:
    - PyKotor wiki (GFF-UTC.md, GFF-File-Format.md)
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(UtcXml, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.xml_content = (self._io.read_bytes_full()).decode(u"UTF-8")


    def _fetch_instances(self):
        pass


