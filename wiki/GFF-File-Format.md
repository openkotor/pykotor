# KotOR GFF file format Documentation

This document describes the GFF (Generic File Format) used in Knights of the Old Republic (KotOR) and The Sith Lords (TSL). GFF is BioWare's binary container for structured game data: areas, creatures, items, dialogues, placeables, triggers, and more. **Audience:** modders editing or creating GFF-based resources, and developers implementing read/write support.

**Official Bioware Documentation:** For the authoritative Bioware Aurora Engine GFF format specification, see [Bioware Aurora GFF Format](Bioware-Aurora-GFF) and [Bioware Aurora Common GFF Structs](Bioware-Aurora-CommonGFFStructs).

**For mod developers:** To modify GFF files in your mods, see the [TSLPatcher GFFList Syntax Guide](TSLPatcher-GFFList-Syntax). For general modding information, see [HoloPatcher README for Mod Developers](HoloPatcher-README-for-mod-developers.).

**Related formats:** GFF files often reference other formats such as [2DA files](2DA-File-Format) for configuration data, [TLK files](TLK-File-Format) for text strings, [MDL/MDX files](MDL-MDX-File-Format) for 3D [models](MDL-MDX-File-Format), and [NCS files](NCS-File-Format) for scripts. Loading any GFF (ARE, DLG, UTC, UTI, etc.) uses the same [resource resolution order](KEY-File-Format#key-file-purpose) as other resources: override, then loaded MOD/SAV, then KEY/BIF. **Modder note:** Tools like KotOR Tool, K-GFF, and Holocron Toolset edit GFF; TSLPatcher/HoloPatcher [GFFList](TSLPatcher-GFFList-Syntax) can add or modify fields but not remove structs—see [Mod-Creation-Best-Practices](Mod-Creation-Best-Practices#removing-gff-structs-when-patchers-cannot) for script-based removal. [Concepts](Concepts) defines GFF and related terms.

## Table of Contents

- [KotOR GFF file format Documentation](#kotor-gff-file-format-documentation)
  - Table of Contents
  - [File structure overview](#file-structure-overview)
    - [GFF as a Universal Container](#gff-as-a-universal-container)
  - [Binary format](#binary-format)
    - [file header](#file-header)
    - [Label array](#label-array)
    - [Struct array](#struct-array)
    - [field array](#field-array)
    - [field data](#field-data)
    - [field Indices (Multiple Element Map / MultiMap)](#field-indices-multiple-element-map--multimap)
    - [List indices](#list-indices)
  - [GFF data types](#gff-data-types)
  - [GFF structure](#gff-structure)
    - [GFFStruct](#gffstruct)
    - [GFFField](#gfffield)
    - [GFFList](#gfflist)
  - [GFF Generic types](#gff-generic-types)
    - [ARE (Area)](#are-area)
    - [DLG (Dialogue)](#dlg-dialogue)
    - [FAC (Faction)](#fac-faction)
    - [GIT (game instance template)](#git-game-instance-template)
    - [GUI (Graphical User Interface)](#gui-graphical-user-interface)
    - [IFO (module info)](#ifo-module-info)
    - [JRL (Journal)](#jrl-journal)
    - [PTH (Path)](#pth-path)
    - [UTC (Creature)](#utc-creature)
    - [UTD (Door)](#utd-door)
    - [UTE (Encounter)](#ute-encounter)
    - [UTI (Item)](#uti-item)
    - [UTM (Merchant)](#utm-merchant)
    - [UTP (Placeable)](#utp-placeable)
    - [UTS (Sound)](#uts-sound)
    - [UTT (Trigger)](#utt-trigger)
    - [UTW (Waypoint)](#utw-waypoint)
  - [Alternative Terminology (Historical)](#alternative-terminology-historical)
  - [field data Access Patterns](#field-data-access-patterns)
    - [Direct Access types](#direct-access-types)
    - [Indirect Access types](#indirect-access-types)
    - [Complex Access types](#complex-access-types)
  - [Implementation Details](#implementation-details)

---

## File Structure Overview

The GFF (Generic File Format) is a hierarchical, strongly-typed binary format developed by BioWare for storing structured game data. GFF files organize information as nested structs (records) which contain fields—fields may hold primitive values, references to additional structs, or lists of structs. The format is extensible and versioned: Knights of the Old Republic uses version V3.2, while later BioWare games employ V3.3, V4.0, V4.1, and others. Despite small changes, the core structure is consistent.

### GFF: BioWare's Data Container

Think of GFF as a "binary JSON" for BioWare engines—compact, fast, and precisely typed, suitable for saving and editing complex game data.

**Key Features:**

- **Strong Typing:** Every field stores data with an explicit type (e.g., int, string, struct), ensuring clarity and safety.
- **Efficiency:** The binary encoding minimizes file size and maximizes read/write speed—ideal for large, complex data sets.
- **Hierarchical Structure:** Data can be nested arbitrarily deep, representing parent/child and list relationships naturally.
- **Extensible Design:** New fields or lists can be added without breaking compatibility.
- **Direct Access:** Offsets and indices enable fast random-access to any structure within the file.

**Typical Applications:**

GFF underpins most major data files in the Aurora/Odyssey engine family:
- Character and creature blueprints ([UTC](GFF-File-Format#utc-creature), [UTD](GFF-File-Format#utd-door), [UTP](GFF-File-Format#utp-placeable), [UTE](GFF-File-Format#ute-encounter), etc.)
- Area layouts and definitions ([ARE](GFF-File-Format#are-area))
- Module instance data ([GIT](GFF-File-Format#git-game-instance-template))
- Module-level metadata ([IFO](GFF-File-Format#ifo-module-info))
- Dialogue trees ([DLG](GFF-File-Format#dlg-dialogue))
- Quest journals ([JRL](GFF-File-Format#jrl-journal))
- Pathfinding and waypoint routes ([PTH](GFF-File-Format#pth-path))
- User interface definitions ([GUI](GFF-File-Format#gui-graphical-user-interface))
- Faction relationships ([FAC](GFF-File-Format#fac-faction))
- Saved game states (various resource types within SAV containers)

Essentially, most files with extensions such as `.utc`, `.uti`, `.dlg`, `.are`, `.git`, `.ifo`, `.jrl`, `.pth`, `.gui`, and others are simply variations of GFF—distinguished by their type string and field schema, but all share the same structural foundation.

**Implementation:** [`Libraries/PyKotor/src/pykotor/resource/formats/gff/`](https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/)

**Vendor References:**

Repositories (original first, mirror second):
- **[reone](https://github.com/seedhartha/reone)** ([Mirror: th3w1zard1/reone](https://github.com/th3w1zard1/reone))
- **[xoreos](https://github.com/xoreos/xoreos)** ([Mirror: th3w1zard1/xoreos](https://github.com/th3w1zard1/xoreos))
- **[KotOR.js](https://github.com/KobaltBlu/KotOR.js)** ([Mirror: th3w1zard1/KotOR.js](https://github.com/th3w1zard1/KotOR.js))
- **[KotOR-Unity](https://github.com/reubenduncan/KotOR-Unity)** ([Mirror: th3w1zard1/KotOR-Unity](https://github.com/th3w1zard1/KotOR-Unity))
- **[Kotor.NET](https://github.com/NickHugi/Kotor.NET)** ([Mirror: th3w1zard1/Kotor.NET](https://github.com/th3w1zard1/Kotor.NET))
- **[xoreos-tools](https://github.com/xoreos/xoreos-tools)** ([Mirror: th3w1zard1/xoreos-tools](https://github.com/th3w1zard1/xoreos-tools))
- **[bioware-kaitai-formats](https://github.com/OldRepublicDevs/bioware-kaitai-formats)** - Kaitai Struct format specs for GFF and other BioWare formats.

### See Also

- [TSLPatcher GFFList Syntax](TSLPatcher-GFFList-Syntax) - Modding *GFF* files with *TSLPatcher*
- [2DA File Format](2DA-File-Format) - Configuration data referenced by *GFF* files
- [TLK File Format](TLK-File-Format) - Text strings used by *GFF* *LocalizedString* fields
- [Bioware Aurora GFF Format](Bioware-Aurora-GFF) - Official *BioWare* *GFF* specification

---

## Binary Format

### File Header

The *file header* is 56 bytes in size:

| Name                | Type    | Offset | Size | Description                                    |
| ------------------- | ------- | ------ | ---- | ---------------------------------------------- |
| *file type*           | [char](GFF-File-Format#gff-data-types) | 0 (0x00) | 4    | Content type (e.g., `"GFF "`, `"ARE "`, `"UTC "`) |
| *file Version*        | [char](GFF-File-Format#gff-data-types) | 4 (0x04) | 4    | Format version (`"V3.2"` for KotOR)           |
| *Struct array offset* | UInt32  | 8 (0x08) | 4    | Offset to struct array                        |
| *Struct count*        | UInt32  | 12 (0x0C) | 4    | Number of structs                              |
| *field array offset*  | UInt32  | 16 (0x10) | 4    | Offset to field array                         |
| *field count*         | UInt32  | 20 (0x14) | 4    | Number of fields                               |
| *Label array offset*   | UInt32  | 24 (0x18) | 4    | Offset to label array                         |
| *Label count*          | UInt32  | 28 (0x1C) | 4    | Number of labels                               |
| *field data offset*    | UInt32  | 32 (0x20) | 4    | Offset to field data section                  |
| *field data count*     | UInt32  | 36 (0x24) | 4    | Size of field data section in bytes           |
| *field indices offset* | UInt32  | 40 (0x28) | 4    | Offset to field indices array                 |
| *field indices count*  | UInt32  | 44 (0x2C) | 4    | Number of field indices                       |
| *List indices offset*  | UInt32  | 48 (0x30) | 4    | Offset to list indices array                  |
| *List indices count*   | UInt32  | 52 (0x34) | 4    | Number of list indices                        |

**References:**

**Vendor Implementations:**

- [`vendor/reone/src/libs/resource/format/gffreader.cpp:30-44`](https://github.com/th3w1zard1/reone/blob/master/src/libs/resource/format/gffreader.cpp#L30-L44) - File header parsing
- [`vendor/xoreos/src/aurora/gff3file.cpp:100-110`](https://github.com/th3w1zard1/xoreos/blob/master/src/aurora/gff3file.cpp#L100-L110) - File header parsing
- [`vendor/KotOR-Unity/Assets/Scripts/FileObjects/GFFObject.cs:18`](https://github.com/th3w1zard1/KotOR-Unity/blob/da59c0e3b16e351479e543d455bb39b6811f7239/Assets/Scripts/ResourceLoader/GFFLoader.cs#L18) - File header parsing
- [`vendor/Kotor.NET/Formats/KotorGFF/GFFReader.cs:100-110`](https://github.com/th3w1zard1/Kotor.NET/blob/master/Formats/KotorGFF/GFFReader.cs#L100-L110) - File header parsing
- [`vendor/KotOR.js/src/resource/GFFObject.ts:100-110`](https://github.com/th3w1zard1/KotOR.js/blob/master/src/resource/GFFObject.ts#L100-L110) - File header parsing
- [`vendor/bioware-kaitai-formats/src/python/kaitai_generated/gff.py:100-110`](https://github.com/th3w1zard1/bioware-kaitai-formats/blob/master/src/python/kaitai_generated/gff.py#L100-L110) - File header parsing
- [`vendor/PyKotor/Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py:100-110`](https://github.com/th3w1zard1/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py#L100-L110) - File header parsing
- [`vendor/PyKotor/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py:100-110`](https://github.com/th3w1zard1/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py#L100-L110) - File header parsing

### Label array

Labels are 16-[byte](https://en.wikipedia.org/wiki/Byte) [null-terminated](https://en.cppreference.com/w/c/string/byte) strings used as field names:

| Name   | type     | size | Description                                                      |
| ------ | -------- | ---- | ---------------------------------------------------------------- |
| Labels | [char](GFF-File-Format#gff-data-types) | 16×N | array of field name labels (null-padded to 16 bytes)            |

**References**

**Vendor Implementations:**

- [`vendor/reone/src/libs/resource/format/gffreader.cpp:151-154`](https://github.com/th3w1zard1/reone/blob/master/src/libs/resource/format/gffreader.cpp#L151-L154) - Label array reading

### Struct array

Each struct entry is 12 bytes:

| Name       | type   | offset | size | Description                                                      |
| ---------- | ------ | ------ | ---- | ---------------------------------------------------------------- |
| Struct ID  | [int32](GFF-File-Format#gff-data-types)  | 0 (0x00) | 4    | structure type identifier                                        |
| data/offset| UInt32 | 4 (0x04) | 4    | field index (if 1 field) or offset to field indices (if multiple) |
| field count| UInt32 | 8 (0x08) | 4    | Number of fields in this struct (0, 1, or >1)                   |

**References**

**Vendor Implementations:**

- [`vendor/reone/src/libs/resource/format/gffreader.cpp:40-62`](https://github.com/th3w1zard1/reone/blob/master/src/libs/resource/format/gffreader.cpp#L40-L62) - Struct array parsing

### field array

Each field entry is 12 bytes:

| Name        | type   | offset | size | Description                                                      |
| ----------- | ------ | ------ | ---- | ---------------------------------------------------------------- |
| field type  | UInt32 | 0 (0x00) | 4    | data type (see [GFF Data Types](#gff-data-types))              |
| Label index | UInt32 | 4 (0x04) | 4    | index into label array for field name                           |
| data/offset | UInt32 | 8 (0x08) | 4    | Inline data (simple types) or offset to field data (complex types) |

**References**

**Vendor Implementations:**

- [`vendor/reone/src/libs/resource/format/gffreader.cpp:67-76`](https://github.com/th3w1zard1/reone/blob/master/src/libs/resource/format/gffreader.cpp#L67-L76) - Field array parsing

### field data

Complex field types store their data in the field data section:

| field type        | Storage format                                                      |
| ----------------- | ------------------------------------------------------------------- |
| UInt64            | 8 bytes (uint64)                                                    |
| Int64             | 8 bytes (int64)                                                     |
| double            | 8 bytes (double)                                                    |
| string            | 4 bytes length + N bytes string data                                |
| ResRef            | 1 byte length + N bytes ResRef data (max 16 chars)                  |
| LocalizedString   | 4 bytes count + N×8 bytes (Language ID + [StrRef](TLK-File-Format#string-references-strref) pairs)              |
| Binary            | 4 bytes length + N bytes binary data                                 |
| Vector3           | 12 bytes (3×float)                                                   |
| Vector4           | 16 bytes (4×float)                                                   |

**References**

**Vendor Implementations:**

- [`vendor/reone/src/libs/resource/format/gffreader.cpp:78-146`](https://github.com/th3w1zard1/reone/blob/master/src/libs/resource/format/gffreader.cpp#L78-L146) - Field data and complex type reading

### field Indices (Multiple Element Map / MultiMap)

When a struct has multiple fields, the struct's data field contains an offset into the field indices array (also called the "Multiple Element Map" or "MultiMap" in [`vendor/xoreos-docs/specs/torlack/itp.html`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/torlack/itp.html)), which lists the field indices for that struct.

**Access Pattern**: When a struct has exactly one field, the struct's data field directly contains the field index. When a struct has more than one field, the data field contains a byte offset into the field indices array, which is an array of uint32 values listing the field indices.

**References**

**Vendor Implementations:**

- [`vendor/xoreos-docs/specs/torlack/itp.html`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/torlack/itp.html) - Entry/Entity table access patterns and MultiMap explanation

### List indices

Lists are stored as arrays of struct indices. The list field contains an offset into the list indices array, which contains the struct indices that make up the list.

**Access Pattern**: For a LIST type field, the field's data/offset value specifies a byte offset into the list indices table. At that offset, the first uint32 is the count of entries, followed by that many uint32 values representing the struct indices.

**References**

**Vendor Implementations:**

- [`vendor/xoreos-docs/specs/torlack/itp.html`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/torlack/itp.html) - LIST type access pattern

---

## GFF Data Types

GFF supports the following *field* types:

| Type ID | Name              | Size (inline) | Description                                                      |
| ------- | ----------------- | ------------- | ---------------------------------------------------------------- |
| 0       | Byte              | 1             | 8-bit unsigned integer                                           |
| 1       | Char              | 1             | 8-bit signed integer                                              |
| 2       | Word              | 2             | 16-bit unsigned integer                                          |
| 3       | Short             | 2             | 16-bit signed integer                                             |
| 4       | DWord             | 4             | 32-bit unsigned integer                                          |
| 5       | Int               | 4             | 32-bit signed integer                                             |
| 6       | DWord64           | 8             | 64-bit unsigned integer (stored in field data)                  |
| 7       | Int64              | 8             | 64-bit signed integer (stored in field data)                      |
| 8       | Float             | 4             | 32-bit floating point                                             |
| 9       | Double            | 8             | 64-bit floating point (stored in field data)                     |
| 10      | CExoString        | varies        | [Null-terminated string](https://en.cppreference.com/w/c/string/byte) string (stored in field data)                    |
| 11      | ResRef            | varies        | Resource reference (stored in field data, max 16 chars)          |
| 12      | CExoLocString     | varies        | Localized string (stored in field data)                           |
| 13      | Void              | varies        | Binary data blob (stored in field data)                          |
| 14      | Struct            | 4             | Nested struct (struct index stored inline)                       |
| 15      | List              | 4             | List of structs (offset to list indices stored inline)            |
| 16      | Orientation       | 16            | Quaternion (4×float, stored in field data as Vector4)            |
| 17      | Vector            | 12            | 3D vector (3×float, stored in field data)                       |
| 18      | [StrRef](TLK-File-Format#string-references-strref)            | 4             | string reference ([TLK](TLK-File-Format) [StrRef](TLK-File-Format#string-references-strref), stored inline as int32)             |

**References**

- [`Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py:73-108`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py#L73-L108) - GFF data type definitions

**Type Selection Guidelines:**

- Use **Byte/Char** for small integers (-128 to 255) and boolean flags
- Use **Word/Short** for medium integers such as IDs and counts
- Use **DWord/Int** for larger numeric values and most general fields
- Use **Float** for decimals that do not need high precision (positions, angles)
- Use **Double** when high-precision floating point is specifically required (rare for KotOR)
- Use **CExoString** for text fields not intended for translation
- Use **CExoLocString** for any player-facing text and translatable content
- Use **ResRef** for resource references (filenames without extensions)
- Use **Void** for binary blobs or unstructured data
- Use **Struct** for grouping related fields (nested objects)
- Use **List** for arrays of structs (e.g., inventory lists, reply chains)
- Use **Vector** for 3D spatial coordinates or directions
- Use **Orientation** for [quaternion](MDL-MDX-File-Format#node-header) orientations/rotations
- Use **[StrRef](TLK-File-Format#string-references-strref)** to point to strings in [dialog.tlk](TLK-File-Format)

**Storage Optimization:**

Primitive types (Byte, Char, Word, Short, DWord, Int, Float, Struct, List, StrRef) are stored *inline* in the field entry, meaning their value or reference (for Struct, List) is physically present in the field and does not incur extra indirection. More complex types (DWord64, Int64, Double, CExoString, ResRef, CExoLocString, Void, Orientation, Vector) are stored *externally* in the field data block, and the field entry only contains an offset pointing to the actual data. When designing custom GFF formats, use inline storage when possible for efficiency, as external/offset types introduce additional overhead in reading and writing.

---

## GFF Structure

### GFF Struct

A *GFF Struct* is a collection of named fields. Each *GFF Struct* has:

- **Struct ID**: Type identifier (often `0xFFFFFFFF` for generic structs)
- **Fields**: Dictionary mapping field names (labels) to field values

**References**

- [`Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py) - *GFF Struct*, *GFF Field*, *GFF List* implementation

### GFF Field

*GFF Fields* can be accessed using type-specific getter/setter methods, for example:

- `get_uint8(label)`, `set_uint8(label, value)`
- `get_int32(label)`, `set_int32(label, value)`
- `get_float(label)`, `set_float(label, value)`
- `get_string(label)`, `set_string(label, value)`
- `get_resref(label)`, `set_resref(label, value)`
- `get_locstring(label)`, `set_locstring(label, value)`
- `get_vector3(label)`, `set_vector3(label, value)`
- `get_struct(label)`, `set_struct(label, struct)`
- `get_list(label)`, `set_list(label, list)`

### GFF List

A *GFF List* is an ordered collection of structs.

**Common List Usage:**

*GFF Lists* are used extensively for variable-length arrays:

- **ItemList** in [UTC](GFF-File-Format#utc-creature) files: Character inventory items
- **Equip_ItemList** in [UTC](GFF-File-Format#utc-creature) files: Equipped items
- **EntryList** in [DLG](GFF-File-Format#dlg-dialogue) files: Dialogue entry [nodes](MDL-MDX-File-Format#node-structures)
- **ReplyList** in [DLG](GFF-File-Format#dlg-dialogue) files: Dialogue reply options
- **SkillList** in [UTC](GFF-File-Format#utc-creature) files: Character skills
- **FeatList** in [UTC](GFF-File-Format#utc-creature) files: Character feats
- **EffectList** in various files: Applied effects
- **Creature_List** in [GIT](GFF-File-Format#git-game-instance-template) files: Spawned creatures in area

When modifying *GFF Lists*, always maintain struct IDs and parent references to avoid breaking internal links.

---

## GFF Generic Types

*GFF (Generic file format)* files are used as containers for various game resource types. Each generic type has its own structure and field definitions.

### *ARE* (Area)

Module/Level area data. See [ARE (Area)](GFF-ARE) for detailed documentation.

### *DLG* (Dialogue)

Game Dialogue trees. See [DLG (Dialogue)](GFF-DLG) for detailed documentation.

### *FAC* (Faction)

Game Faction data. See [FAC (Faction)](GFF-FAC) for detailed documentation.

### *GIT* (Game Instance Template)

Game Instance Template. See [GIT (Game Instance Template)](GFF-GIT) for detailed documentation.

### *GUI* (Graphical User Interface)

Graphical User Interface. See [GUI (Graphical User Interface)](GFF-GUI) for detailed documentation.

### *IFO* (Module Info)

Game Module Info. See [IFO (Module Info)](GFF-IFO) for detailed documentation.

### *JRL* (Journal)

Journal entries. See [JRL (Journal)](GFF-JRL) for detailed documentation.

### *PTH* (Path)

Pathfinding routes. See [PTH (Path/Pathfinding Route)](GFF-PTH) for detailed documentation.

### *UTC* (Creature)

Creature templates. See [UTC (Creature Template)](GFF-UTC) for detailed documentation.

### *UTD* (Door)

Door templates. See [UTD (Door Template)](GFF-UTD) for detailed documentation.

### *UTE* (Encounter)

Encounter templates. See [UTE (Encounter Template)](GFF-UTE) for detailed documentation.

### *UTI* (Item)

Item templates. See [UTI (Item Template)](GFF-UTI) for detailed documentation.

### *UTM* (Merchant)

Merchant templates. See [UTM (Merchant Template)](GFF-UTM) for detailed documentation.

### *UTP* (Placeable)

Placeable templates. See [UTP (Placeable Template)](GFF-UTP) for detailed documentation.

### *UTS* (Sound)

Sound templates. See [UTS (Sound Template)](GFF-UTS) for detailed documentation.

### *UTT* (Trigger)

Trigger templates. See [UTT (Trigger Template)](GFF-UTT) for detailed documentation.

### *UTW* (Waypoint)

Waypoint templates. See [UTW (Waypoint Template)](GFF-UTW) for detailed documentation.

**Note**: The first entry in the *struct array* is always the root of the entire hierarchy. All other structs and fields can be accessed from this root entry.

**References**
- [`Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py) - GFF data model
- [`Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py) - GFF binary reading and writing

## Field Data Access Patterns

### Direct Access types

Simple types (*Byte*, *Char*, *Word*, *Short*, *DWord*, *Int*, *Double*, *Float*) store their values directly in the field entry's data/offset field (offset `0x0008` in the element structure). These values are stored in [little-endian](https://en.wikipedia.org/wiki/Endianness) (LE) format.

### Indirect Access types

Complex types require accessing data from the *field data section*:

- **UInt64, Int64, Double**: The field's data/offset contains a byte offset into the *field data section* where the 8-byte value is stored.
- **String (*CExoString*)**: The offset points to a uint32 length followed by the string bytes (not [null-terminated](https://en.cppreference.com/w/c/string/byte)).
- **ResRef**: The offset points to a uint8 length (max 16) followed by the *ResRef* bytes (not [null-terminated](https://en.cppreference.com/w/c/string/byte)).
- **LocalizedString (*CExoLocString*)**: The offset points to a structure containing:
  - uint32: Total size (not including this count)
  - int32: [StrRef](TLK-File-Format#string-references-strref) ID ([dialog.tlk](TLK-File-Format) reference, `-1` if none)
  - uint32: Number of language-specific strings
  - For each language string (if count > 0):
    - uint32: Language ID
    - uint32: string length in bytes
    - [char](GFF-File-Format#gff-data-types): string data
- **Void (*Binary*)**: The offset points to a uint32 length followed by the binary data bytes.
- **Vector3**: The offset points to 12 bytes (3×*float*) in the field data section.
- **Vector4 / Orientation**: The offset points to 16 bytes (4×*float*) in the field data section.

### Complex Access types

- **Struct (*CAPREF*)**: The field's data/offset contains a struct index (not an offset). This references a struct in the *struct array*.
- **List**: The field's data/offset contains a byte offset into the *list indices array*. At that offset, the first `uint32` is the entry count, followed by that many `uint32` struct indices.

**References**

- [`vendor/xoreos-docs/specs/torlack/itp.html`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/torlack/itp.html) - Detailed field data access patterns and code examples

- **Binary Reading**: [`Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py:26-419`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py#L26-L419)
- **Binary Writing**: [`Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py:421-800`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/io_gff.py#L421-L800)
- **GFF Class**: [`Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py:200-400`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py#L200-L400)
- **GFFStruct Class**: [`Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py:400-800`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/gff/gff_data.py#L400-L800)

### See also

- [TSLPatcher GFFList Syntax](TSLPatcher-GFFList-Syntax) -- Patching GFF via TSLPatcher
- [Bioware-Aurora-GFF](Bioware-Aurora-GFF) -- Aurora GFF specification
- [Community Sources and Archives](Home#community-sources-and-archives) -- DeadlyStream, Forums for *GFF* structure and modding examples

---

This documentation aims to provide a comprehensive overview of the KotOR *GFF* file format, focusing on the detailed file structure and data formats used within the games.
