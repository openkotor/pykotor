# KEY and BIF file formats — BioWare Aurora Engine

*Official BioWare Aurora documentation (archived extract).*

---

## Table of contents

- [About this document](#about-this-document)
- [1. Introduction](#1-introduction)
  - [1.1 Conventions](#11-conventions)
  - [1.2 Resource management](#12-resource-management)
  - [1.3 Resource types](#13-resource-types)
    - [Table 1.3.1: Resource types](#table-131-resource-types)
    - [Table 1.3.2: Resource content types](#table-132-resource-content-types)
- [2. KEY file format](#2-key-file-format)
  - [2.1 KEY file structure](#21-key-file-structure)
  - [2.2 Header (Table 2.2)](#22-header-table-22)
  - [2.3 File table (Table 2.3)](#23-file-table-table-23)
  - [2.4 Filename table (Table 2.4)](#24-filename-table-table-24)
  - [2.5 Key table (Table 2.5)](#25-key-table-table-25)
- [3. BIF file format](#3-bif-file-format)
  - [3.1 BIF structure](#31-bif-structure)
  - [3.2 Header (Table 3.2)](#32-header-table-32)
  - [3.3 Variable resource table (Table 3.3)](#33-variable-resource-table-table-33)
  - [3.4 Fixed resource table (Table 3.4)](#34-fixed-resource-table-table-34)
  - [3.5 Variable resource data](#35-variable-resource-data)
  - [3.6 Fixed resource data](#36-fixed-resource-data)
- [See also](#see-also)

---

## About this document

**Source:** Official BioWare Aurora Engine Key/BIF Format PDF, archived in [`vendor/xoreos-docs/specs/bioware/KeyBIF_Format.pdf`](https://github.com/xoreos/xoreos-docs/blob/master/specs/bioware/KeyBIF_Format.pdf) (mirror: [`th3w1zard1/xoreos-docs/.../KeyBIF_Format.pdf`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/bioware/KeyBIF_Format.pdf)). Originally published on `nwn.bioware.com`.

> **Note:** Written for **Neverwinter Nights**; **KEY and BIF are identical in KotOR**. NWN-centric examples (e.g. `chitin.key`, HAK) still illustrate the same binary layout.

*BioWare Corp. · [bioware.com](http://www.bioware.com) · BioWare Aurora Engine — Key and BIF*

---

## 1. Introduction

BioWare games pack many resources into **`.bif`** archives. **`.key`** files describe what those BIFs contain and how to look resources up.

### 1.1 Conventions

All formats in this document are **little-endian** (Intel byte order): for multi-byte integers, the **least significant byte is first**.

**Example:** **258** (`0x0102`) as a 32-bit value is stored as:

`0x02`, `0x01`, `0x00`, `0x00`

**Integer terms**

| Term | Meaning |
|------|---------|
| **WORD** | 16-bit unsigned |
| **DWORD** | 32-bit unsigned |

### 1.2 Resource management

The game and toolset resolve a resource by **ResRef** (filename, ≤ **16** characters) and **ResType** (type id). The resource manager loads from **override folders**, **BIF**/**HAK**/folders, etc. If multiple copies exist, **precedence rules** pick one.

**Source kinds** (any number of each):

1. **Key table** — a **`.key`** file (e.g. `chitin.key`, `xp1.key`, `patch.key`) indexing **`.bif`** files (e.g. under `data\`).
2. **Directories** — plain folders of loose files (e.g. `override`, `modules\temp0`).
3. **Encapsulated files** — **[ERF](Bioware-Aurora-ERF)**-family archives (HAK, ERF in `texturepacks`, etc.).

**Precedence**

- Among sources of the **same** kind, **later** registration **wins** over **earlier** (e.g. temp module folder after override).
- Across kinds: **encapsulated** **>** **directories** **>** **key tables**, regardless of add order.

**Example:** Added in order: `chitin.key`, `patch.key`, `override`, `textures_tpa.erf`, `modules\temp0`, `customcontent.hak`. Lowest → highest priority:

`chitin.key` → `patch.key` → `override` → `modules\temp0` → `textures_tpa.erf` → `customcontent.hak`

So a script `ns_test00` in both the module and `customcontent.hak` uses the **HAK** copy.

### 1.3 Resource types

Resources have a **ResType** id. Inside BIF/ERF they are stored **without** the file extension; type is implied by **ResType**.

Reserved ranges: **0–2999**, **9000–9999**, and **`0xFFFF`** (per BioWare spec). Other values are available for defined types.

#### Table 1.3.1: Resource types

| ResType | Ext. | Content type | Description |
|---------|------|--------------|-------------|
| `0xFFFF` | — | — | Invalid |
| 1 | bmp | binary | Windows BMP |
| 3 | tga | binary | TGA image |
| 4 | wav | binary | WAV audio |
| 6 | plt | binary | BioWare PLT (layered textures, e.g. PC skins) |
| 7 | ini | text (ini) | Windows INI |
| 10 | txt | text | Plain text |
| 2002 | mdl | mdl | Aurora model |
| 2009 | nss | text | NWScript source |
| 2010 | ncs | binary | NWScript compiled |
| 2012 | are | gff | Area (`.are`); paired **GIT** + **GIC** same ResRef in a module |
| 2013 | set | text (ini) | Tileset |
| 2014 | ifo | gff | Module info — [IFO](Bioware-Aurora-IFO) |
| 2015 | bic | gff | Character / creature |
| 2016 | wok | mdl | Walkmesh |
| 2017 | 2da | text | Two-dimensional array |
| 2022 | txi | text | Extra texture info |
| 2023 | git | gff | Game instance (instances + scriptable area state) |
| 2025 | uti | gff | Item blueprint |
| 2027 | utc | gff | Creature blueprint |
| 2029 | dlg | gff | Conversation |
| 2030 | itp | gff | Tile/blueprint palette |
| 2032 | utt | gff | Trigger blueprint |
| 2033 | dds | binary | Compressed texture |
| 2035 | uts | gff | Sound blueprint |
| 2036 | ltr | binary | Letter-combo probabilities (name generation) |
| 2037 | gff | gff | Generic GFF when no dedicated extension (ITP, UTC, UTI, IFO, ARE, GIT, …) |
| 2038 | fac | gff | Faction |
| 2040 | ute | gff | Encounter blueprint |
| 2042 | utd | gff | Door blueprint |
| 2044 | utp | gff | Placeable blueprint |
| 2045 | dft | text (ini) | Default values (area properties UI) |
| 2046 | gic | gff | Instance comments (toolset; not used by game) |
| 2047 | gui | gff | GUI layout |
| 2051 | utm | gff | Store / merchant blueprint |
| 2052 | dwk | mdl | Door walkmesh |
| 2053 | pwk | mdl | Placeable walkmesh |
| 2056 | jrl | gff | Journal — [Journal](Bioware-Aurora-Journal) |
| 2058 | utw | gff | Waypoint blueprint |
| 2060 | ssf | binary | Sound set — see SSF format doc |
| 2064 | ndb | binary | Script debugger |
| 2065 | ptm | gff | Plot manager / plot instance |
| 2066 | ptt | gff | Plot wizard blueprint |

#### Table 1.3.2: Resource content types

| Content type | Description |
|--------------|-------------|
| **binary** | Opaque binary; format varies. |
| **text** | Plain text. Prefer **CR+LF** line endings for broadest compatibility. |
| **text (ini)** | Windows INI (text subset). |
| **gff** | [Generic File Format (GFF)](Bioware-Aurora-GFF). |
| **mdl** | Aurora model (ASCII or binary). |

---

## 2. KEY file format

A **KEY** indexes resources stored across one or more **BIF** files: which BIFs exist, their paths, and **ResRef + ResType → location**.

### 2.1 KEY file structure

**Figure 2.1: KEY layout**

```text
Start of file
├── Header
├── File Table        @ OffsetToFileTable
├── Filename Table    (paths referenced by File Table)
└── Key Entries Table @ OffsetToKeyTable
```

### 2.2 Header (Table 2.2)

| Value | Type | Description |
|-------|------|-------------|
| `FileType` | 4 `char` | **`"KEY "`** |
| `FileVersion` | 4 `char` | **`"V1  "`** |
| `BIFCount` | DWORD | Number of BIF files indexed |
| `KeyCount` | DWORD | Total resource entries across those BIFs |
| `OffsetToFileTable` | DWORD | Byte offset to **File Table** from file start |
| `OffsetToKeyTable` | DWORD | Byte offset to **Key Entry Table** from file start |
| `Build Year` | DWORD | Years since **1900** |
| `Build Day` | DWORD | Days since **January 1** |
| `Reserved` | 32 bytes | Reserved |

### 2.3 File table (Table 2.3)

**`BIFCount`** entries; each **File Entry** describes one BIF.

| Value | Type | Description |
|-------|------|-------------|
| `FileSize` | DWORD | Size of the BIF file |
| `FilenameOffset` | DWORD | Byte offset into **Filename Table** (start of path string) |
| `FilenameSize` | WORD | Length of filename in **characters** |
| `Drives` | WORD | Drive bitmask (e.g. bit **0** = install / “HD0” volume for relative paths) |

### 2.4 Filename table (Table 2.4)

Concatenated **non-null-terminated** path strings. Each **File Entry**’s `FilenameOffset` / `FilenameSize` selects one path. Paths are **relative** to the drive/volume implied by **`Drives`**. Each filename must be **unique** (e.g. `data\2da.bif`).

| Value | Type | Description |
|-------|------|-------------|
| `Filename` | variable | Characters only (no `NUL` terminator in KEY) |

### 2.5 Key table (Table 2.5)

**`KeyCount`** entries; each row is one resource in some BIF.

| Value | Type | Description |
|-------|------|-------------|
| `ResRef` | 16 × `char` | Resource name **without** extension; must be **unique** per KEY’s namespace |
| `ResourceType` | WORD | [ResType](#table-131-resource-types) |
| `ResID` | DWORD | Packed location id (see below) |

**`ResID` encoding** (`<<` = left shift):

- **Variable resource** (normal case today):

```text
ResID = (x << 20) + y
```

  - **`x`** = index of BIF in **File Table**
  - **`y`** = index in that BIF’s **Variable Resource Table**

- **Fixed resource** (format supports; rarely used in shipped data):

```text
ResID = (x << 20) + (y << 14)
```

  - **`y`** = index in BIF **Fixed** resource table

---

## 3. BIF file format

A **BIF** holds **raw resource bytes**. It does **not** store ResRefs; the **KEY** maps names to BIF entries.

### 3.1 BIF structure

**Figure 3.1: BIF layout**

```text
Start of file
├── Header
├── Variable Resource Table     @ Variable Table Offset (typically 20)
├── [Fixed Resource Table]      (if Fixed Resource Count > 0; see §3.4)
├── Variable Resource Data
└── [Fixed Resource Data]
```

### 3.2 Header (Table 3.2)

| Value | Type | Description |
|-------|------|-------------|
| `FileType` | 4 `char` | **`"BIFF"`** (standard BIF). KotOR also uses compressed archives with **`"BZF "`** — see [BIF-File-Format](BIF-File-Format). |
| `Version` | 4 `char` | **`"V1  "`** for BIF; **`"V1.0"`** for BZF in KotOR. |
| `Variable Resource Count` | DWORD | Entries in variable table |
| `Fixed Resource Count` | DWORD | Entries in fixed table (often **0**) |
| `Variable Table Offset` | DWORD | Byte offset to **Variable Resource Table** (commonly **20**) |

### 3.3 Variable resource table (Table 3.3)

One entry per variable resource.

| Value | Type | Description |
|-------|------|-------------|
| `ID` | DWORD | Packed id: **`(x << 20) + y`** where **`y`** = index of **this** entry in the BIF. On retail CDs often **`x = y`**; in patch BIFs often **`x = 0`**. Loaders generally key off lookup via KEY, not **`x`** inside the BIF. |
| `Offset` | DWORD | Byte offset from **start of BIF** into **Variable Resource Data** |
| `File Size` | DWORD | Length of this resource in bytes |
| `Resource Type` | DWORD | [ResType](#table-131-resource-types) |

### 3.4 Fixed resource table (Table 3.4)

> **Note:** Fixed resources are **not implemented** in shipped tooling/data: header fields exist, but there is **no** standard fixed table payload in practice. If **`Fixed Resource Count` = 0**, **Variable Resource Data** follows the variable table immediately.

*Conceptual* fixed entry (for completeness):

| Value | Type | Description |
|-------|------|-------------|
| `ID` | DWORD | **`(x << 20) + (y << 14)`** — **`x`** = BIF index in KEY File Table, **`y`** = fixed entry index |
| `Offset` | DWORD | Offset into **Fixed Resource Data** |
| `PartCount` | DWORD | Part count |
| `File Size` | DWORD | Total size |
| `Resource Type` | DWORD | ResType |

### 3.5 Variable resource data

Raw bytes for each variable resource, addressed by **`Offset`** / **`File Size`** in [Table 3.3](#33-variable-resource-table-table-33).

### 3.6 Fixed resource data

Would store fixed-resource parts if fixed resources were used ([§3.4](#34-fixed-resource-table-table-34)).

---

## See also

| Resource | Notes |
|----------|--------|
| [KEY-File-Format](KEY-File-Format) | KotOR KEY layout and resolution order |
| [BIF-File-Format](BIF-File-Format) | KotOR BIF notes |
| [ERF-File-Format](ERF-File-Format) | MOD / RIM / HAK |
| [GFF-File-Format](GFF-File-Format) | GFF-based resource types |

---

*Edition notes: Per-page BioWare headers removed. Typos from the extract corrected (**whereever** → wherever, **resouce** → resource, **mutliple** → multiple, **it’s** → **its** where possessive, **relative to the the** → **relative to the**). **BIF** signature **`BIFF`** / **`V1  `** matches the BioWare PDF; KotOR **BZF** compression is noted per [BIF-File-Format](BIF-File-Format). Table **1.3.1** ends at the rows in this PDF extract (through **2066**).*
