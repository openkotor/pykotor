# encdifficulty.2da

Part of the [2DA File Format Documentation](2DA-File-Format).

**Engine Usage**: Defines encounter difficulty levels for area encounters. The engine uses this file to determine encounter scaling and difficulty modifiers.

**Row index**: Difficulty ID (integer)

**Column structure**:

| Column Name | type | Description |
|------------|------|-------------|
| `label` | string | Difficulty label |
| Additional columns | Various | Difficulty modifiers and properties |

**References**:

- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:474`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L474) - TwoDARegistry definition
- [`Tools/HolocronToolset/src/toolset/data/installation.py:73`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Tools/HolocronToolset/src/toolset/data/installation.py#L73) - HTInstallation constant
- [`Tools/HolocronToolset/src/toolset/gui/editors/ute.py:101-104`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Tools/HolocronToolset/src/toolset/gui/editors/ute.py#L101-L104) - Encounter difficulty selection

### See also

- [2DA-File-Format](2DA-File-Format) -- 2DA structure; [GFF-UTE](GFF-UTE) -- Encounter difficulty index
- [Bioware-Aurora-Encounter](Bioware-Aurora-Encounter) -- Aurora encounter spec
- [TSLPatcher 2DAList Syntax](TSLPatcher-2DAList-Syntax) -- Patching 2DA

---
