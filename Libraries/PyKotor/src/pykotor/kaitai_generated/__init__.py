"""Vendored Kaitai Struct generated parsers from bioware-kaitai-formats.

Source: https://github.com/OldRepublicDevs/bioware-kaitai-formats (src/python/kaitai_generated).
Imports in sibling modules were rewritten to use relative imports for in-tree packaging.

PyKotor binary readers that currently delegate parsing here (with legacy fallback when
``KaitaiStructError`` is raised, and for TwoDA ``ValueError`` from the Kaitai path): SSF, TLK,
LIP, RIM, TwoDA.

Not wired to ``*BinaryReader.load()`` yet (layout mismatch, ASCII/text pipeline, or scope):
KEY, BIF, ERF, GFF, TPC, WAV, BWM, MDL, NCS, and related types. VIS/LYT/TXI
in this tree are primarily ASCII/text and still use the existing readers.

To refresh generated files, copy from upstream and run ``scripts/rewrite_kaitai_generated_imports.py``.
"""
