# Journal (JRL) format — BioWare Aurora Engine

*Official BioWare Aurora documentation (archived extract).*

---

## Table of contents

- [About this document](#about-this-document)
- [1. Introduction](#1-introduction)
- [2. Journal system structs](#2-journal-system-structs)
  - [2.1 Top-level struct (Table 2.1)](#21-top-level-struct-table-21)
  - [2.2 JournalCategory struct (Table 2.2)](#22-journalcategory-struct-table-22)
  - [2.3 JournalEntry struct (Table 2.3)](#23-journalentry-struct-table-23)
- [See also](#see-also)

---

## About this document

**Source:** Official BioWare Aurora Engine Journal Format PDF, archived in [`vendor/xoreos-docs/specs/bioware/Journal_Format.pdf`](https://github.com/xoreos/xoreos-docs/blob/master/specs/bioware/Journal_Format.pdf) (mirror: [`th3w1zard1/xoreos-docs/.../Journal_Format.pdf`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/bioware/Journal_Format.pdf)). Originally published on `nwn.bioware.com`.

> **Note:** Written for **Neverwinter Nights**; the **Journal (JRL) format is identical in KotOR**. NWN-specific UI wording may appear, but the GFF layout is the same.

*BioWare Corp. · [bioware.com](http://www.bioware.com) · BioWare Aurora Engine — Journal system*

---

## 1. Introduction

A **journal** tracks the player’s progress in each **plot** they have started and describes the **current step** of each plot.

Journal data lives in **`module.jrl`** inside a module or save game. The file uses **[GFF](Bioware-Aurora-GFF)**; this document assumes you already know GFF basics.

In the GFF header, the **FileType** string for a journal file is **`"JRL "`** (four characters, space-padded).

> **Correction:** An older extract of this page said the FileType was for `repute.fac`; that was a **transcription error**. The journal resource is **`module.jrl`** with **`FileType`** **`"JRL "`**. Faction data uses a separate **FAC** resource (see [FAC (faction)](GFF-File-Format#fac-faction) in the KotOR GFF overview).

---

## 2. Journal system structs

GFF layout of **`module.jrl`**. For **List** fields, **StructID** equals the element’s **index** in that list.

### 2.1 Top-level struct (Table 2.1)

#### Table 2.1: Journal top-level struct

| Label | Type | Description |
|-------|------|-------------|
| `Categories` | List | **JournalCategory** structs. **StructID = list index.** |

---

### 2.2 JournalCategory struct (Table 2.2)

Fields on each **JournalCategory** in **`Categories`**.

#### Table 2.2: Fields in JournalCategory struct (StructID = list index)

| Label | Type | Description |
|-------|------|-------------|
| `Comment` | CExoString | Builder / designer comments. |
| `EntryList` | List | **JournalEntry** structs. **StructID = list index.** |
| `Name` | CExoLocString | Localized category title (in-game journal UI). |
| `Picture` | WORD | **Unused.** Always **`0xFFFF`**. |
| `Priority` | DWORD | Display priority; see [Priority values](#priority-values). |
| `Tag` | CExoString | Script identifier for this category. **Tags must be unique** across categories. |
| `XP` | DWORD | XP granted when the category is **completed** (player reaches an entry with **`End` = 1**; see [Table 2.3](#23-journalentry-struct-table-23)). |

<a id="priority-values"></a>

#### Priority values (`Priority` field)

| Value | Meaning |
|-------|---------|
| 0 | Highest |
| 1 | High |
| 2 | Medium |
| 3 | Low |
| 4 | Lowest |

---

### 2.3 JournalEntry struct (Table 2.3)

Each **JournalEntry** is one step under a category’s **`EntryList`**.

#### Table 2.3: Fields in JournalEntry struct (StructID = list index)

| Label | Type | Description |
|-------|------|-------------|
| `End` | WORD | **1** if this entry is an **endpoint** for its category (there may be **multiple** endings). |
| `ID` | DWORD | Entry ID used by **scripts** to read/write current progress. Must be **unique within the category**; IDs need not be contiguous or sorted. |
| `Text` | CExoLocString | Localized body text shown in-game under the category. |

---

## See also

| Resource | Notes |
|----------|--------|
| [GFF-JRL](GFF-JRL) | KotOR journal GFF |
| [GFF-File-Format](GFF-File-Format) | GFF structure and types |
| [NSS-File-Format](NSS-File-Format) | Journal-related scripting |
| [KEY-File-Format](KEY-File-Format) | Resource resolution |

---

*Edition notes: Repeated per-page BioWare headers are folded into [About](#about-this-document). Table numbers match the BioWare Journal PDF. **FileType** line corrected from the erroneous `repute.fac` reference to **`module.jrl` / `"JRL "`**.*
