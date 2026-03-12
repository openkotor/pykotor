# iprp_damagetype.2da

Part of the [2DA File Format Documentation](2DA-File-Format).

**Engine Usage**: Maps item property values to damage type flags. The engine uses this file to determine damage type calculations for item properties.

**Row index**: Item Property Value (integer)

**Column structure**:

| Column Name | type | Description |
|------------|------|-------------|
| `label` | string | Property value label |
| Additional columns | Various | Damage type mappings |

**References**:

- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:481`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L481) - TwoDARegistry definition
- [`Tools/HolocronToolset/src/toolset/data/installation.py:80`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Tools/HolocronToolset/src/toolset/data/installation.py#L80) - HTInstallation constant

### See also

- [2DA-File-Format](2DA-File-Format) -- 2DA structure; [2DA-itemprops](2DA-itemprops), [2DA-itempropdef](2DA-itempropdef) -- Item property 2DA
- [GFF-UTI](GFF-UTI) -- Item properties; [TSLPatcher-2DAList-Syntax](TSLPatcher-2DAList-Syntax) -- Patching 2DA

---
