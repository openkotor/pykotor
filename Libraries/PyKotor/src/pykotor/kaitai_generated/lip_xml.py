# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class LipXml(KaitaiStruct):
    """LIP XML format is a human-readable XML representation of LIP (Lipsync) binary files.
    Provides easier editing than binary LIP format.
    
    References:
    - https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/src/pykotor/resource/formats/lip/lip.py
    - https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/src/pykotor/resource/formats/lip/io_lip_xml.py
    - https://github.com/seedhartha/reone/tree/master/src/libs/graphics/format/lipreader.cpp
    - https://github.com/OldRepublicDevs/PyKotor/wiki/LIP-File-Format.md
    - https://github.com/xoreos/xoreos/tree/master/src/graphics/aurora/lipfile.cpp
    
    - ../GFF/GFF
    - ../GFF/XML/GFF_XML
    - ../LIP/LIP
    """
    def __init__(self, _io, _parent=None, _root=None):
        super(LipXml, self).__init__(_io)
        self._parent = _parent
        self._root = _root or self
        self._read()

    def _read(self):
        self.xml_content = (self._io.read_bytes_full()).decode(u"UTF-8")


    def _fetch_instances(self):
        pass


