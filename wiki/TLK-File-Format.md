# KotOR TLK file format Documentation

This document provides a detailed description of the *TLK* (Talk Table) file format used in Knights of the Old Republic (KotOR) games. *TLK* files contain all text strings used in the game, both written and spoken, enabling easy localization by providing a lookup table from string reference numbers ([StrRef](TLK-File-Format#string-references-strref)) to localized text and associated voice-over audio files.

**For mod developers:** To modify TLK files in your mods, see the [TSLPatcher TLKList Syntax Guide](TSLPatcher-TLKList-Syntax). For general modding information, see [HoloPatcher README for Mod Developers](HoloPatcher-README-for-mod-developers.).

**Related formats:** *TLK* files are referenced by [GFF files](GFF-File-Format) (especially [DLG](GFF-File-Format#dlg-dialogue) [dialogue files](GFF-File-Format#dlg-dialogue)), [2DA files](2DA-File-Format) for item names and descriptions, and [SSF files](SSF-File-Format) for character sound sets.

## Table of Contents

- KotOR *TLK* File Format Documentation
  - [File Structure Overview](#file-structure-overview)
  - [Binary Format](#binary-format)
    - [File Header](#file-header)
    - [String Data Table](#string-data-table)
    - [String Entries](#string-entries)
  - [*TLK* Entry Structure](#tlkentry-structure)
  - [String References (*StrRef*)](#string-references-strref)
    - [Custom *TLK* Files](#custom-tlk-files)
  - [Localization](#localization)
  - [Implementation Details](#implementation-details)

---

## File structure overview

*TLK* files store localized strings in a binary format. The game loads `dialog.tlk` at startup and references strings throughout the game using [StrRef](TLK-File-Format#string-references-strref) numbers (array indices). String lookups use the same [resource resolution order](KEY-File-Format#key-file-purpose) as other resources (override, then module/SAV, then KEY/BIF), so custom *TLK*s in override or in a MOD take precedence over the base game `dialog.tlk`.

**Implementations:**
- [`Libraries/PyKotor/src/pykotor/resource/formats/tlk/`](https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/src/pykotor/resource/formats/tlk/)
- **[reone](https://github.com/seedhartha/reone)** ([Mirror: th3w1zard1/reone](https://github.com/th3w1zard1/reone))
- **[xoreos](https://github.com/xoreos/xoreos)** ([Mirror: th3w1zard1/xoreos](https://github.com/th3w1zard1/xoreos))
- **[KotOR.js](https://github.com/KobaltBlu/KotOR.js)** ([Mirror: th3w1zard1/KotOR.js](https://github.com/th3w1zard1/KotOR.js))
- **[KotOR-Unity](https://github.com/reubenduncan/KotOR-Unity)** ([Mirror: th3w1zard1/KotOR-Unity](https://github.com/th3w1zard1/KotOR-Unity))
- **[Kotor.NET](https://github.com/NickHugi/Kotor.NET)** ([Mirror: th3w1zard1/Kotor.NET](https://github.com/th3w1zard1/Kotor.NET))
- **[xoreos-tools](https://github.com/xoreos/xoreos-tools)** ([Mirror: th3w1zard1/xoreos-tools](https://github.com/th3w1zard1/xoreos-tools))

### See also

- [2DA File Format](2DA-File-Format) - Game tables with name/description *StrRef*s.
- [GFF File Format](GFF-File-Format) - Dialogue and templates that reference *TLK* strings.
- [SSF File Format](SSF-File-Format) - Sound sets that reference *TLK* entries.
- [TSLPatcher TLKList Syntax](TSLPatcher-TLKList-Syntax) - Modding *TLK* files with *TSLPatcher*.

---

## Binary format

### File Header

The file header is `20` (0x14) bytes in size:

| Name                | type    | offset | size | Description                                    |
| ------------------- | ------- | ------ | ---- | ---------------------------------------------- |
| file type           | [char](GFF-File-Format#gff-data-types) | 0 (0x00) | 4    | Always `"TLK "` (space-padded)                  |
| file Version        | [char](GFF-File-Format#gff-data-types) | 4 (0x04) | 4    | `"V3.0"` for KotOR, `"V4.0"` for Jade Empire  |
| Language ID         | [int32](GFF-File-Format#gff-data-types)   | 8 (0x08) | 4    | Language identifier (see [Localization](#localization)) |
| string count        | [int32](GFF-File-Format#gff-data-types)   | 12 (0x0C) | 4    | Number of string entries in the file           |
| string Entries offset | [int32](GFF-File-Format#gff-data-types) | 16 (0x10) | 4    | Offset to string entries array (typically `20` (0x14))  |

**Implementations:**

- **[reone](https://github.com/seedhartha/reone)** ([Mirror: th3w1zard1/reone](https://github.com/th3w1zard1/reone)): [`src/libs/resource/format/tlkreader.cpp:31-84`](https://github.com/seedhartha/reone/blob/master/src/libs/resource/format/tlkreader.cpp#L31-L84) - File header parsing

### String Data Table

The string data table contains metadata for each string entry. Each entry is `40` (0x28) bytes in size:

| Name              | Type      | Offset | Size | Description                                                      |
| ----------------- | --------- | ------ | ---- | ---------------------------------------------------------------- |
| flags             | UInt32    | 0 (0x00) | 4    | Bit flags: bit 0=text present, bit 1=sound present, bit 2=sound length present |
| Sound *ResRef*      | [char](GFF-File-Format#gff-data-types)  | 4 (0x04) | 16   | Voice-over audio filename ([null-terminated](https://en.cppreference.com/w/c/string/byte), max `16` chars)        |
| Volume Variance   | UInt32    | 20 (0x14) | 4    | Unused in KotOR (always `0`)                                      |
| Pitch Variance    | UInt32    | 24 (0x18) | 4    | Unused in KotOR (always `0`)                                      |
| offset to string  | UInt32    | 28 (0x1C) | 4    | Offset to string text (relative to string Entries offset)       |
| string size       | UInt32    | 32 (0x20) | 4    | Length of string text in bytes                                  |
| Sound Length      | [float](GFF-File-Format#gff-data-types)     | 36 (0x24) | 4    | Duration of voice-over audio in seconds                         |

**References**

- **[Kotor.NET](https://github.com/NickHugi/Kotor.NET)** ([Mirror: th3w1zard1/Kotor.NET](https://github.com/th3w1zard1/Kotor.NET)): [`Kotor.NET/Formats/KotorTLK/TLKBinaryStructure.cs:57-90`](https://github.com/NickHugi/Kotor.NET/blob/master/Kotor.NET/Formats/KotorTLK/TLKBinaryStructure.cs#L57-L90) - String data table structure

**Flag Bits:**

- **bit 0 (0x0001)**: Text present - string has text content
- **bit 1 (0x0002)**: Sound present - string has associated voice-over audio
- **bit 2 (0x0004)**: Sound length present - sound length field is valid

**Flag Combinations:**

Common flag patterns in KotOR *TLK* files:

| Flags | Hex | Description | Usage |
| ----- | --- | ----------- | ----- |
| `0x0001` | `0x01` | Text only | Menu options, item descriptions, non-voiced dialog |
| `0x0003` | `0x03` | Text + Sound | Voiced dialog lines (most common for party/NPC speech) |
| `0x0007` | `0x07` | Text + Sound + Length | Fully voiced with duration data (cutscenes, important dialog) |
| `0x0000` | `0x00` | Empty entry | Unused [StrRef](TLK-File-Format#string-references-strref) slots |

The engine uses these flags to determine:

- Whether to display subtitles (*Text present* flag)
- Whether to play voice-over audio (*Sound present* flag)
- How long to wait before auto-advancing dialog (*Sound length present* flag)

Missing flags are treated as `false` - if *Text present* is not set, the string is treated as empty even if text data exists.

### String Entries

String entries follow the *String Data Table*:

| Name         | Type   | Description                                                      |
| ------------ | ------ | ---------------------------------------------------------------- |
| Text String  | [char](GFF-File-Format#gff-data-types)[] | [Null-terminated string](https://en.cppreference.com/w/c/string/byte) data (UTF-8 or Windows-1252 encoded)     |

Text string is stored at the offset specified in the *String Data Table* entry. The encoding depends on the language ID (see [Localization](#localization)).

---

## *TLK* Entry Structure

Each *TLK* entry contains:

**References**
- [`Libraries/PyKotor/src/pykotor/resource/formats/tlk/tlk_data.py`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/tlk/tlk_data.py) - TLKEntry and TLK implementation

| Attribute        | type   | Description                                                      |
| ---------------- | ------ | ---------------------------------------------------------------- |
| `text`           | str    | Localized text string                                            |
| `voiceover`      | [ResRef](GFF-File-Format#gff-data-types) | Voice-over audio resref (max 16 characters) ([WAV file](WAV-File-Format))                            |
| `text_present`   | bool   | Whether text content exists                                      |
| `sound_present`  | bool   | Whether voice-over audio exists                                  |
| `soundlength_present` | bool | Whether sound length is valid                                    |
| `sound_length`   | float  | Duration of voice-over audio in seconds                         |

---

## String References (StrRef)

String references (*StrRef*) are integer indices into the TLK file's entry array:

- **StrRef 0**: First entry in the TLK file
- **StrRef -1**: No string reference (used to indicate missing/empty strings)
- **StrRef N**: Nth entry (0-based indexing)

The game uses *StrRef* values throughout the game's files such as [CExoLocString](Bioware-Aurora-GFF#cexolocstring) fields in [GFF](GFF-File-Format) files, [NSS](NSS-File-Format) scripts, and other resources to reference localized text. When displaying text, the game looks up the *StrRef* in `dialog.tlk` and displays the corresponding text.

## Localization

*TLK* files support multiple languages through the Language ID field:

| Language ID | Language | Encoding      |
| ----------- | -------- | ------------- |
| 0           | English  | Windows-1252  |
| 1           | French   | Windows-1252  |
| 2           | German   | Windows-1252  |
| 3           | Italian  | Windows-1252  |
| 4           | Spanish  | Windows-1252  |
| 5           | Polish   | Windows-1250  |

**Note**: KotOR games typically ignore the Language ID field in the `dialog.tlk`. The field is primarily used by modding tools to identify the language.

**Note**: *Windows-1252* is a single byte encoding, meaning only ***256*** characters are supported. This occasionally is known as "ISO-8859-1" or *cp1252*.

### Bi-Lingual Implementation

The Polish localization version of the first KotOR game supports bi-lingual localization using two *TLK* files:

1. `dialog.tlk` - Primary game text
2. `dialogf.tlk` - Female-specific variants (KotOR1 Polish only)

---

---

## Implementation Details

**Binary Reading**: [`Libraries/PyKotor/src/pykotor/resource/formats/tlk/io_tlk.py:19-115`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/tlk/io_tlk.py#L19-L115)

**Binary Writing**: [`Libraries/PyKotor/src/pykotor/resource/formats/tlk/io_tlk.py:117-178`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/tlk/io_tlk.py#L117-L178)

**TLK Class**: [`Libraries/PyKotor/src/pykotor/resource/formats/tlk/tlk_data.py:56-291`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/tlk/tlk_data.py#L56-L291)

### See also

- [TSLPatcher TLKList Syntax](TSLPatcher-TLKList-Syntax) -- Patching *TLK* files.
- [2DA-File-Format](2DA-File-Format), [GFF-File-Format](GFF-File-Format) -- *StrRef* consumers; [NSS-File-Format](NSS-File-Format) -- Script strings.
- [Official BioWare Aurora TalkTable Specification](Bioware-Aurora-TalkTable) -- Official BioWare Aurora TalkTable specification.
- [Community Sources and Archives](Home#community-sources-and-archives) -- DeadlyStream, forums for *TLK*/*StrRef* modding and string references.

---

This documentation aims to provide a comprehensive overview of the KotOR *TLK* file format, focusing on the detailed file structure and data formats used within the games.
