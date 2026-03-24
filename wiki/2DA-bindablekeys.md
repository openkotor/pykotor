# bindablekeys.2da

Part of the [2DA File Format Documentation](2DA-File-Format).

**Engine Usage**: Defines bindable key actions and their string references. The engine uses this file to determine key action names for the key binding interface.

**Row index**: Bindable key ID (integer)

**Column structure**:

| Column Name | type | Description |
|------------|------|-------------|
| `label` | string | Bindable key label |
| `keynamestrref` | [StrRef](TLK-File-Format#string-references-strref) | string reference for key name |
| Additional columns | Various | key binding properties |

**References**:

- [`Libraries/PyKotor/src/pykotor/extract/twoda.py:74`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/extract/twoda.py#L74) - [StrRef](TLK-File-Format#string-references-strref) column definition for `bindablekeys.2da`
