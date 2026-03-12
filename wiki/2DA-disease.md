# disease.2da

Part of the [2DA File Format Documentation](2DA-File-Format).

**Engine Usage**: Defines disease effect configurations. The engine uses this file to determine disease names, scripts, and properties.

**Row index**: Disease ID (integer)

**Column structure**:

| Column Name | type | Description |
|------------|------|-------------|
| `label` | string | Disease label |
| `name` | [StrRef](TLK-File-Format#string-references-strref) | string reference for disease name (KotOR 2) |
| `end_incu_script` | *ResRef* | Script *ResRef* for end incubation period |
| `24_hour_script` | *ResRef* | Script *ResRef* for 24-hour disease effect |
| Additional columns | Various | Disease properties |

**References**:

- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:255`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L255) - [StrRef](TLK-File-Format#string-references-strref) column definition for disease.2da (KotOR 2)
- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:238,431`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L238) - Script *ResRef* column definitions for disease.2da

### See also

- [2DA-File-Format](2DA-File-Format) — 2DA structure; [2DA-poison](2DA-poison) — Poison effects
- [NCS-File-Format](NCS-File-Format) — Disease scripts; [TLK-File-Format](TLK-File-Format) — StrRef; [TSLPatcher-2DAList-Syntax](TSLPatcher-2DAList-Syntax) — Patching 2DA

---
