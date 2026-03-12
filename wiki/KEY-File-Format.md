# KotOR KEY file format Documentation

This document provides a detailed description of the KEY (KEY Table) file format used in Knights of the Old Republic (KotOR) games. KEY files serve as the master index for all [BIF files](BIF-File-Format) in the game.

## Table of Contents

- KotOR KEY File format Documentation
  - Table of Contents
  - [File structure overview](#file-structure-overview)
    - [KEY File Purpose](#key-file-purpose)
  - [Binary Format](#binary-format)
    - [File Header](#file-header)
    - [File Table](#file-table)
    - [Filename Table](#filename-table)
    - [KEY Table](#key-table)
  - [Resource ID Encoding](#resource-id-encoding)
  - [Implementation Details](#implementation-details)

---

## File structure overview

KEY files map resource names ([ResRefs](GFF-File-Format#gff-data-types)) and types to specific locations within [BIF containers](BIF-File-Format). KotOR uses `chitin.key` as the main KEY file which references all game [BIF files](BIF-File-Format). **Modder note:** Mods do not edit the KEY; they add content via the [override folder](Concepts#override-folder) or [MOD/ERF](Concepts#mod--erf) so the engine finds their resources first. See [Concepts](Concepts) and [Mod-Creation-Best-Practices](Mod-Creation-Best-Practices#file-priority-and-where-to-put-your-files).

### KEY File Purpose

The *KEY* file, specifically `chitin.key` in KotOR, serves as the master index for the game's resource system:

1. **Resource Lookup**: Maps *ResRef* + *Resource Type* --> [BIF](BIF-File-Format) location
2. **[BIF](BIF-File-Format) Registration**: Tracks all [BIF files](BIF-File-Format) and their install paths
3. **Resource Naming**: Provides the filename (*ResRef*) missing from [BIF files](BIF-File-Format)
4. **Drive Mapping**: Historical feature indicating which media ([CD](https://en.wikipedia.org/wiki/Compact_disc)/[HD](https://en.wikipedia.org/wiki/Hard_disk_drive)) contained each [BIF](BIF-File-Format)

**Resource Resolution Order:**

When the game needs a resource, it searches in the following order:

1. Override folder (`override/`)
2. Currently loaded [MOD/ERF](ERF-File-Format) files
3. Currently loaded `.sav` Save Entry (usually a folder; situational, dependent on the game)
4. [BIF files](BIF-File-Format) via [KEY](KEY-File-Format) lookup
5. Hardcoded defaults (if no resource found)

The *KEY* file only manages [BIF](BIF-File-Format) resources (step 4). Higher-priority locations can override *KEY*-indexed resources without modifying the *KEY* file. However, this is not recommended as it can lead to inconsistencies and is not a supported feature.

**How a resource request is satisfied:** The engine’s resource manager resolves a "demand" by first checking whether the resource is already loaded or cached. If not, it routes the request to one of several back ends depending on where the resource lives: directory (override or filesystem), encapsulated container ([MOD/ERF](ERF-File-Format)), resource file, or image ([BIF](BIF-File-Format)). Each back end is responsible for opening the correct file or container and returning the data; the *KEY* is used only when the source is the [BIF](BIF-File-Format) image set. So override and [MOD/ERF](ERF-File-Format) are tried before any *KEY*/[BIF](BIF-File-Format) lookup.

**Implementation:** [`Libraries/PyKotor/src/pykotor/resource/formats/key/`](https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/src/pykotor/resource/formats/key/)

**Vendor References:**

- **[reone](https://github.com/seedhartha/reone)** - Complete C++ *KEY* reader implementation (`src/libs/resource/format/keyreader.cpp`) ([Mirror: th3w1zard1/reone](https://github.com/th3w1zard1/reone))
- **[xoreos](https://github.com/xoreos/xoreos)** - Generic Aurora *KEY* implementation (`src/aurora/keyfile.cpp`), shared format across KotOR, NWN, and other Aurora games ([Mirror: th3w1zard1/xoreos](https://github.com/th3w1zard1/xoreos))
- **[KotOR.js](https://github.com/KobaltBlu/KotOR.js)** - TypeScript KEY parser (`src/resource/KEYObject.ts`) ([Mirror: th3w1zard1/KotOR.js](https://github.com/th3w1zard1/KotOR.js))
- **[Kotor.NET](https://github.com/NickHugi/Kotor.NET)** - .NET *KEY* reader/writer (`Kotor.NET/Formats/KotorKEY/`) ([Mirror: th3w1zard1/Kotor.NET](https://github.com/th3w1zard1/Kotor.NET))
- **[xoreos-tools](https://github.com/xoreos/xoreos-tools)** - Command-line *KEY* tools (`src/aurora/keyfile.cpp`) ([Mirror: th3w1zard1/xoreos-tools](https://github.com/th3w1zard1/xoreos-tools))

---

## [Binary Format](https://en.wikipedia.org/wiki/Binary_file)

The file header is 64 bytes in size:

| Name                | type    | offset | size | Description                                    |
| ------------------- | ------- | ------ | ---- | ---------------------------------------------- |
| File Type           | [Char](https://en.wikipedia.org/wiki/Character_(computer_science)) | `0` (`0x00`) | `4`    | Always `"KEY "` (space-padded)                 |
| File Version        | [Char](https://en.wikipedia.org/wiki/Character_(computer_science)) | `4` (`0x04`) | `4`    | `"V1  "` or `"V1.1"`                           |
| [BIF](BIF-File-Format) count           | UInt32  | `8` (`0x08`) | `4`    | Number of [BIF files](BIF-File-Format) referenced                 |
| KEY count           | UInt32  | `12` (`0x0C`) | `4`    | Number of *Resource Entries*                     |
| Offset to File Table | UInt32 | `16` (`0x10`) | `4`    | Offset to [BIF File](BIF-File-Format) Entries* Array               |
| Offset to KEY Table | UInt32 | `20` (`0x14`) | `4`    | Offset to *Resource Entries* Array               |
| Build Year          | UInt32  | `24` (`0x18`) | `4`    | Build Year (years since 1900)                 
| Build Day           | UInt32  | `28` (`0x1C`) | `4`    | Build Day (days since Jan 1)                   |
| Reserved            | [Byte](https://en.wikipedia.org/wiki/Byte) | `32` (`0x20`) | `32`   | Padding (usually zeros)                        |

**Note on Header Variations**: **[xoreos-docs](https://github.com/xoreos/xoreos-docs)** ([Mirror: th3w1zard1/xoreos-docs](https://github.com/th3w1zard1/xoreos-docs)): [`specs/torlack/key.html`](https://github.com/xoreos/xoreos-docs/blob/master/specs/torlack/key.html) (Tim Smith/Torlack's reverse-engineered documentation) shows the header ending at offset `0x0040` with unknown values at offset `0x0018`. The structure shown here (with *Build Year*/*Build Day* and *Reserved* fields) matches the actual *KotOR KEY* File Format.

**References**

**Vendor Implementations:**

- [`vendor/Kotor.NET/Kotor.NET/Formats/KotorKEY/KEYBinaryStructure.cs:13-114`](https://github.com/th3w1zard1/Kotor.NET/blob/master/Kotor.NET/Formats/KotorKEY/KEYBinaryStructure.cs#L13-L114) - .NET *KEY* Binary Structure
- [`vendor/xoreos-docs/specs/torlack/key.html`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/torlack/key.html) - Tim Smith (Torlack)'s reverse-engineered *KEY* Format Documentation (may show variant header structure)

### File Table

Each file entry is 12 bytes:

| Name            | Type   | Offset | Size | Description                                                      |
| --------------- | ------ | ------ | ---- | ---------------------------------------------------------------- |
| File Size       | UInt32 | `0` (0x00) | `4`    | Size of [BIF](BIF-File-Format) file on disk                                         |
| Filename Offset | UInt32 | `4` (0x04) | `4`    | Offset into filename table                                       |
| Filename Length | [UInt16](GFF-File-Format#gff-data-types) | `8` (0x08) | `2`    | Length of filename in bytes                                      |
| Drives          | [UInt16](GFF-File-Format#gff-data-types) | `10` (0x0A) | `2`    | Drive flags (`0x0001=HD0`, `0x0002=CD1`, etc.)                      |

**Drive Flags Explained:**

*Drive Flags* are a legacy feature from the multi-[CD](https://en.wikipedia.org/wiki/Compact_disc) distribution era:

| Flag Value | Meaning | Description |
| ---------- | ------- | ----------- |
| `0x0001` | `HD` ([Hard Drive](https://en.wikipedia.org/wiki/Hard_disk_drive)) | [BIF](BIF-File-Format) is installed on the hard drive |
| `0x0002` | `CD1` ([CD](https://en.wikipedia.org/wiki/Compact_disc) 1) | [BIF](BIF-File-Format) is on the first game disc |
| `0x0004` | `CD2` ([CD](https://en.wikipedia.org/wiki/Compact_disc) 2) | [BIF](BIF-File-Format) is on the second game disc |
| `0x0008` | `CD3` ([CD](https://en.wikipedia.org/wiki/Compact_disc) 3) | [BIF](BIF-File-Format) is on the third game disc |
| `0x0010` | `CD4` ([CD](https://en.wikipedia.org/wiki/Compact_disc) 4) | [BIF](BIF-File-Format) is on the fourth game disc |

**Modern Usage:**

In contemporary distributions ([Steam](https://store.steampowered.com/), [GOG](https://www.gog.com/), [digital](https://en.wikipedia.org/wiki/Digital_distribution)):

- All [BIF files](BIF-File-Format) use `0x0001` (`HD` Flag) since everything is installed locally
- The engine doesn't prompt for disc swapping
- Multiple flags can be combined (bitwise OR) if a [BIF](BIF-File-Format) could be on multiple sources (e.g. `0x0001 | 0x0002` ([HD](https://en.wikipedia.org/wiki/Hard_disk_drive) Flag | [CD1](https://en.wikipedia.org/wiki/Compact_disc) Flag) for a [BIF](BIF-File-Format) that is on both the hard drive and the first game disc)
- Mod tools typically set this to `0x0001` (`HD` Flag) for all files

The drive system was originally designed so the engine could:

- Prompt users to insert specific [CD](https://en.wikipedia.org/wiki/Compact_disc)s when needed resources weren't on the hard drive
- Optimize installation by allowing users to choose what to install vs. run from [CD](https://en.wikipedia.org/wiki/Compact_disc)
- Support partial installs to save disk space (common in the early 2000s)

**References**

**Vendor Implementations:**

- [`vendor/reone/src/libs/resource/format/keyreader.cpp:55-70`](https://github.com/th3w1zard1/reone/blob/master/src/libs/resource/format/keyreader.cpp#L55-L70) - File Table Parsing

### Filename Table

The *Filename Table* contains [null-terminated](https://en.cppreference.com/w/c/string/byte) strings:

| Name      | Type   | Description                                                      |
| --------- | ------ | ---------------------------------------------------------------- |
| Filenames | [char](GFF-File-Format#gff-data-types)[] | [null-terminated](https://en.cppreference.com/w/c/string/byte) [BIF](BIF-File-Format) Filenames (e.g., `data/[models](MDL-MDX-File-Format).bif`)         |

### *KEY* Table

Each *KEY* entry is `22` (`0x16`) bytes in size:

| Name        | Type     | Offset | Size | Description                                                      |
| ----------- | -------- | ------ | ---- | ---------------------------------------------------------------- |
| *ResRef*      | [char](GFF-File-Format#gff-data-types) | `0` (`0x00`) | `16`   | Resource Filename (null-padded, max 16 characters)                   |
| Resource Type | [UInt16](GFF-File-Format#gff-data-types) | `16` (`0x10`) | `2`    | Resource Type Identifier (e.g. `0x3F` for [TPC](TPC-File-Format))                                         |
| Resource ID | UInt32   | `18` (`0x12`) | `4`    | Encoded Resource Location (see [Resource ID Encoding](#resource-id-encoding)) (e.g. `0x00000005` for the 5th Resource in the 1st [BIF](BIF-File-Format)) |

**Critical Structure Packing Note:**

  The *KEY* entry structure must use **[byte](https://en.wikipedia.org/wiki/Byte) or [word](https://en.wikipedia.org/wiki/Word_(computer_architecture)) alignment** (1-[byte](https://en.wikipedia.org/wiki/Byte) or 2-[byte](https://en.wikipedia.org/wiki/Byte) packing). If the structure is packed with `4-[byte](https://en.wikipedia.org/wiki/Byte)` or `8-[byte](https://en.wikipedia.org/wiki/Byte)` alignment, the `UInt32` at offset `0x0012` (`18`) will be incorrectly placed at offset `0x0014` (`20`), causing incorrect *Resource ID* decoding.

On non-Intel platforms, this alignment requirement may cause alignment faults unless the compiler provides an "unaligned" type or special care is taken when accessing the `UInt32` field. The structure should be explicitly packed to ensure the `UInt32` starts at offset `18` (`0x12`) rather than being aligned to a `4-[byte](https://en.wikipedia.org/wiki/Byte)` or `8-[byte](https://en.wikipedia.org/wiki/Byte)` boundary.

**References**

**Vendor Implementations:**

- [`vendor/reone/src/libs/resource/format/keyreader.cpp:72-100`](https://github.com/th3w1zard1/reone/blob/master/src/libs/resource/format/keyreader.cpp#L72-L100) - *KEY* Entry Structure Parsing

---

## Resource ID Encoding

The *Resource ID* field encodes both the [BIF](BIF-File-Format) index and resource index within that [BIF](BIF-File-Format):

- **bits `31-20`**: [BIF](BIF-File-Format) Index (top 12 bits) - index into file table
- **bits `19-0`**: Resource Index (bottom 20 bits) - index within the [BIF](BIF-File-Format) file

**Decoding:**

```python
bif_index = (resource_id >> `20`) & `0xFFF`  # Extract Top 12 Bits
resource_index = resource_id & `0xFFFFF`   # Extract Bottom 20 Bits
```

**Encoding:**

```python
resource_id = (bif_index << `20`) | resource_index # Encode Resource ID
```

**Practical Limits:**

- Maximum [BIF](BIF-File-Format) Files: `4,096` (12-bit [BIF](BIF-File-Format) index)
- Maximum Resources per [BIF](BIF-File-Format) File: `1,048,576` (20-bit resource index)

These limits are more than sufficient for KotOR, which typically has:

- `~50-100` [BIF](BIF-File-Format) Files in a full installation
- `~100-10,000` Resources per [BIF](BIF-File-Format) File (largest [BIF](BIF-File-Format) Files are [texture](TPC-File-Format) packs)

**Example:**

Given *Resource ID* `0x00123456`:

```plaintext
Binary: 0000 0000 0001 0010 0011 0100 0101 0110
        |---- 12 bits -----|------ 20 bits ------|
BIF Index:     0x001 (BIF Index: `1`)
Resource Index: 0x23456 (Resource Index: `144,470` within that [BIF](BIF-File-Format) file)
```

The encoding allows a single 32-bit integer to precisely locate any resource in the entire [BIF](BIF-File-Format) system (e.g. `0x00123456` for the 5th resource in the 1st [BIF](BIF-File-Format) file).

**References**

**Vendor Implementations:**

- [`vendor/reone/src/libs/resource/format/keyreader.cpp:95-100`](https://github.com/th3w1zard1/reone/blob/master/src/libs/resource/format/keyreader.cpp#L95-L100) - Resource ID Decoding
- [`vendor/xoreos-docs/specs/torlack/key.html`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/torlack/key.html) - [BIF](BIF-File-Format) ID encoding explanation with example (`0x00400029` --> [BIF](BIF-File-Format) `#4`, Resource `#41` within that [BIF](BIF-File-Format) file)

---

## Implementation Details

**Binary Reading**: [`Libraries/PyKotor/src/pykotor/resource/formats/key/io_key.py`](https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/src/pykotor/resource/formats/key/io_key.py) - *KEY* File Binary Reading

**Binary Writing**: [`Libraries/PyKotor/src/pykotor/resource/formats/key/io_key.py`](https://github.com/OldRepublicDevs/PyKotor/tree/master/Libraries/PyKotor/src/pykotor/resource/formats/key/io_key.py) - *KEY* File Binary Writing

**KEY Class**: [`Libraries/PyKotor/src/pykotor/resource/formats/key/key_data.py:100-462`](https://github.com/OldRepublicDevs/PyKotor/blob/master/Libraries/PyKotor/src/pykotor/resource/formats/key/key_data.py#L100-L462) - *KEY* File High-level Organization Class

### See also

- [BIF File Format](BIF-File-Format) - Container format indexed by KEY
- [ERF File Format](ERF-File-Format) - Self-contained containers (MOD/SAV/HAK) and resolution order
- [GFF File Format](GFF-File-Format) - Common content type resolved via KEY/BIF
- [Bioware Aurora KeyBIF](Bioware-Aurora-KeyBIF) - Official BioWare KEY/BIF specification
- [Home](Home) - Resource resolution order and override folder
- [Community sources and archives](Home#community-sources-and-archives) -- DeadlyStream, forums for override and resolution troubleshooting

---

This documentation aims to provide a comprehensive overview of the *KotOR KEY* File Format, focusing on the detailed file structure and data formats used within the games.
