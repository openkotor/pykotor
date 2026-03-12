# doortypes.2da

Part of the [2DA File Format Documentation](2DA-File-Format).

**Engine Usage**: Defines door type configurations and their properties. The engine uses this file to determine door type names, [models](MDL-MDX-File-Format), and behaviors.

**Row index**: Door type ID (integer)

**Column structure**:

| Column Name | type | Description |
|------------|------|-------------|
| `label` | string | Door type label |
| `stringrefgame` | [StrRef](TLK-File-Format#string-references-strref) | string reference for door type name |
| `model` | *ResRef* | [model](MDL-MDX-File-Format) *ResRef* for the door type |
| Additional columns | Various | Door type properties |

**References**:

- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:78`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L78) - [StrRef](TLK-File-Format#string-references-strref) column definition for doortypes.2da
- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:177`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L177) - [model](MDL-MDX-File-Format) *ResRef* column definition for doortypes.2da

### See also

- [2DA-File-Format](2DA-File-Format) — 2DA structure; [GFF-UTD](GFF-UTD) — Door templates
- [GFF-GIT](GFF-GIT) — Door instances; [Bioware-Aurora-DoorPlaceableGFF](Bioware-Aurora-DoorPlaceableGFF) — Aurora spec
- [MDL-MDX-File-Format](MDL-MDX-File-Format), [TLK-File-Format](TLK-File-Format); [TSLPatcher 2DAList Syntax](TSLPatcher-2DAList-Syntax) — Patching 2DA

---
