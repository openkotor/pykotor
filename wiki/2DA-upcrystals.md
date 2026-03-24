# upcrystals.2da

Part of the [2DA File Format Documentation](2DA-File-Format).

**Engine Usage**: Defines upgrade crystal configurations. The engine uses this file to determine crystal [model](MDL-MDX-File-Format) variations for lightsaber upgrades.

**Row index**: Upgrade Crystal ID (integer)

**Column structure**:

| Column Name | type | Description |
|------------|------|-------------|
| `label` | string | Upgrade crystal label |
| `shortmdlvar` | *ResRef* | Short [model](MDL-MDX-File-Format) variation *ResRef* |
| `longmdlvar` | *ResRef* | Long [model](MDL-MDX-File-Format) variation *ResRef* |
| `doublemdlvar` | *ResRef* | double-bladed [model](MDL-MDX-File-Format) variation *ResRef* |
| Additional columns | Various | Crystal properties |

**References**:

- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:172`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L172) - [model](MDL-MDX-File-Format) *ResRef* column definitions for upcrystals.2da

---
