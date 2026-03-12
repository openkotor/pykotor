# ambientsound.2da

Part of the [2DA File Format Documentation](2DA-File-Format).

**Engine Usage**: Defines ambient sound effects for areas. The engine uses this file to play ambient sounds in areas.

**Row index**: Sound ID (integer)

**Column structure**:

| Column Name | type | Description |
|------------|------|-------------|
| `label` | string | Sound label |
| `sound` | *ResRef* | Sound file *ResRef* |
| `resource` | *ResRef* | Sound resource *ResRef* |
| `description` | [StrRef](TLK-File-Format#string-references-strref) | Sound description string reference |

**References**:

**PyKotor:**

- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:72`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L72) - [StrRef](TLK-File-Format#string-references-strref) column definition for ambientsound.2da (K1: description)
- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:184`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L184) - Sound *ResRef* column definition for ambientsound.2da (K1: resource)
- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:247`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L247) - [StrRef](TLK-File-Format#string-references-strref) column definition for ambientsound.2da (K2: description)
- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:376`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L376) - Sound *ResRef* column definition for ambientsound.2da (K2: resource)
- [`Libraries/PyKotor/src/pykotor/common/scriptdefs.py:6986-6988`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/common/scriptdefs.py#L6986-L6988) - AmbientSoundPlay function comment

### See also

- [2DA-File-Format](2DA-File-Format) -- 2DA structure; [2DA-ambientmusic](2DA-ambientmusic) -- Area music
- [GFF-ARE](GFF-ARE) -- Area sound refs; [WAV-File-Format](WAV-File-Format) -- Sound files; [TSLPatcher-2DAList-Syntax](TSLPatcher-2DAList-Syntax) -- Patching 2DA

---
