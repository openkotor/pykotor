# IFO file format — BioWare Aurora Engine

*Official BioWare Aurora documentation (archived extract).*

---

## Table of contents

- [About this document](#about-this-document)
- [1. Introduction](#1-introduction)
- [2. Top-level struct](#2-top-level-struct)
  - [2.1 Fields created by toolset (Table 2.1)](#21-fields-created-by-toolset-table-21)
  - [2.2 Fields created by game (Table 2.2)](#22-fields-created-by-game-table-22)
- [3. Common lists and structs](#3-common-lists-and-structs)
  - [3.1 Mod_Area_List](#31-mod_area_list)
  - [3.2 Mod_CacheNSSList](#32-mod_cachensslist)
  - [3.3 Mod_HakList](#33-mod_haklist)
- [4. Save-game lists and structs](#4-save-game-lists-and-structs)
  - [4.1 EventQueue](#41-eventqueue)
  - [4.2 Mod_PlayerList](#42-mod_playerlist)
  - [4.3 Mod_Tokens](#43-mod_tokens)
  - [4.4 Mod_TURDList](#44-mod_turdlist)
  - [4.5 VarTable](#45-vartable)
- [See also](#see-also)

---

## About this document

**Source:** This documentation is extracted from the official BioWare Aurora Engine IFO Format PDF, archived in [`vendor/xoreos-docs/specs/bioware/IFO_Format.pdf`](https://github.com/xoreos/xoreos-docs/blob/master/specs/bioware/IFO_Format.pdf) (mirror: [`th3w1zard1/xoreos-docs/specs/bioware/IFO_Format.pdf`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/bioware/IFO_Format.pdf)). The original documentation was published on the now-defunct `nwn.bioware.com` developer site.

> **Note:** This official BioWare documentation was originally written for **Neverwinter Nights**, but the **IFO format is identical in KotOR**. All structures, fields, and behaviors described here apply to KotOR as well. Examples may reference NWN-specific features, but the core format is the same.

*BioWare Corp. · [bioware.com](http://www.bioware.com) · BioWare Aurora Engine — IFO file format*

---

## 1. Introduction

An **IFO** file is a module information file. Every NWN module (`.MOD` or `.NWM`) or savegame (`.SAV`) is an **Encapsulated Resource File (ERF)** that contains an IFO file named `module.ifo`.

The IFO file type is in BioWare’s **[Generic File Format (GFF)](Bioware-Aurora-GFF)**. This document assumes familiarity with GFF. Many GFF Fields in an IFO reference **two-dimensional array ([2DA](Bioware-Aurora-2DA))** files, so familiarity with the 2DA format is also assumed.

In the GFF header of an IFO file, the **FileType** value is **`"IFO "`** (four characters, space-padded per GFF convention).

---

## 2. Top-level struct

### 2.1 Fields created by toolset (Table 2.1)

When a module is saved by the toolset, the **top-level GFF Struct** of the `module.ifo` file has the Fields in the table below.

For **List** Fields, the table lists the **StructID** used by elements in that List.

Certain numeric Fields have **allowable ranges**; applications that set these values should respect those limits—there are no guarantees how the game or toolset treats invalid values.

#### Table 2.1: Basic fields in IFO top-level struct

| Label | Type | Description |
|-------|------|-------------|
| `Expansion_Pack` | WORD | Bit flags for which expansion packs are required to run this module. Once a bit is set, it is never unset. Bit 0 = Expansion 1, Bit 1 = Expansion 2, etc. |
| `Mod_Area_List` | List | Areas in the module. **StructID 6.** |
| `Mod_CacheNSSList` | List | Scripts the game should cache. **StructID 9.** |
| `Mod_Creator_ID` | INT | Deprecated; unused. Always **2**. |
| `Mod_CustomTlk` | CExoString | Name of a custom TLK file (no `.tlk` extension). Custom TLK files should live in the `tlk` folder under the main game install. For non-English languages that use `dialogF.tlk` in addition to `dialog.tlk`, the custom TLK must also have an `F.tlk` counterpart in `tlk`. To reference a string from the module’s custom TLK, set StrRef’s **`0x01000000`** bit; the app masks that bit off and uses the value as an index into the **custom** TLK instead of `dialog.tlk`. If the string is missing there, it falls back to the normal `dialog.tlk` StrRef. |
| `Mod_CutsceneList` | List | Deprecated; unused. |
| `Mod_DawnHour` | BYTE | Game hour when dawn begins (**0–23**). Area lighting transitions from night to day over **1** game hour. |
| `Mod_Description` | CExoLocString | Module description. |
| `Mod_DuskHour` | BYTE | Game hour when dusk begins (**0–23**). Area lighting transitions from day to night over **1** game hour. |
| `Mod_Entry_Area` | CResRef | Module starting area. |
| `Mod_Entry_Dir_X` | FLOAT | **X** component of the start location direction unit vector (cosine of bearing in the XY plane, CCW from +X). |
| `Mod_Entry_Dir_Y` | FLOAT | **Y** component (sine of that bearing). |
| `Mod_Entry_X` | FLOAT | Start location **X** inside the starting area. |
| `Mod_Entry_Y` | FLOAT | Start location **Y**. |
| `Mod_Entry_Z` | FLOAT | Start location **Z**. *(Placement: toolset refuses to save until the start is on a **walkable** tile; if it later becomes unwalkable—e.g. tileset/walkmesh changes—the game spawns at the **nearest walkable** point.)* |
| `Mod_Expan_List` | List | Deprecated; unused. |
| `Mod_GVar_List` | List | Deprecated; unused. |
| `Mod_Hak` | CExoString | *(Obsolete)* HAK file for the module, without the `.hak` extension. If `Mod_HakList` exists, this is ignored; otherwise it acts as the module’s HAK pak. |
| `Mod_HakList` | List | HAK files for the module. **Earlier** entries in the list have **higher** priority and override later HAKs. **StructID 8.** |
| `Mod_ID` | Binary | 16-byte arbitrary ID assigned when the toolset creates the module; not changed afterward by the toolset. The **game** may save **32** bytes instead of 16. Non-toolset apps may set this to all nulls when creating a new IFO. |
| `Mod_IsSaveGame` | BYTE | **0** = module saved by toolset; **1** = save game. |
| `Mod_MinGameVer` | CExoString | Minimum game/resource version in **`n.nn`** form (e.g. `"1.26"`, `"1.30"`). Game and toolset refuse to open the module if this exceeds the user’s version. Value may only increase or stay the same. If missing, default **`"1.22"`**. |
| `Mod_MinPerHour` | BYTE | Real-time **minutes per game hour** (**1–255**). |
| `Mod_Name` | CExoLocString | Module name. |
| `Mod_OnAcquirItem` | CResRef | `OnAcquireItem` event script. |
| `Mod_OnActvtItem` | CResRef | `OnActivateItem` event script. |
| `Mod_OnClientEntr` | CResRef | `OnClientEnter` event script. |
| `Mod_OnClientLeav` | CResRef | `OnClientLeave` event script. |
| `Mod_OnCutsnAbort` | CResRef | `OnCutsceneAbort` event script. |
| `Mod_OnHeartbeat` | CResRef | `OnHeartbeat` event script. |
| `Mod_OnModLoad` | CResRef | `OnModuleLoad` event script. |
| `Mod_OnModStart` | CResRef | `OnModuleStart` event script; deprecated. |
| `Mod_OnPlrDeath` | CResRef | `OnPlayerDeath` event script. |
| `Mod_OnPlrDying` | CResRef | `OnPlayerDying` event script. |
| `Mod_OnPlrEqItm` | CResRef | `OnPlayerEquipItem` event script. |
| `Mod_OnPlrLvlUp` | CResRef | `OnPlayerLevelUp` event script. |
| `Mod_OnPlrRest` | CResRef | `OnPlayerRest` event script. |
| `Mod_OnPlrUnEqItm` | CResRef | `OnPlayerUnEquipItem` event script. |
| `Mod_OnSpawnBtnDn` | CResRef | `OnPlayerRespawn` event script. |
| `Mod_OnUnAcreItem` | CResRef | `OnUnAcquireItem` event script. |
| `Mod_OnUsrDefined` | CResRef | `OnUserDefined` event script. |
| `Mod_StartDay` | BYTE | Starting day (**1–31**). |
| `Mod_StartHour` | BYTE | Starting hour (**0–23**). |
| `Mod_StartMonth` | BYTE | Starting month. The archived PDF gives range **1–24** (often treated as **1–12** for calendar months in practice). |
| `Mod_StartMovie` | CResRef | Movie in the `movies` folder played when the module starts. |
| `Mod_StartYear` | DWORD | Starting year. |
| `Mod_Tag` | CExoString | Module tag. |
| `Mod_Version` | DWORD | Module version; always **3**. |
| `Mod_XPScale` | BYTE | Percentage multiplier for XP from killing creatures. |

---

### 2.2 Fields created by game (Table 2.2)

When a module is **saved by the game**, additional top-level Fields appear as below.

#### Table 2.2: Save-game fields in IFO top-level struct

| Label | Type | Description |
|-------|------|-------------|
| `Creature List` | List | Deprecated; unused. |
| `EventQueue` | List | Queued game events at save time. **StructID 43981.** |
| `Mod_Effect_NxtId` | DWORD64 | Next Effect ID to assign. |
| `Mod_IsNWMFile` | BYTE | **1** if saved from an **NWM** file, **0** if from a **MOD** file. |
| `Mod_NextCharId0` | DWORD | Next character ID (part 0). |
| `Mod_NextCharId1` | DWORD | Next character ID (part 1). *(PDF shows “-”.)* |
| `Mod_NextObjId0` | DWORD | Next object ID (part 0). |
| `Mod_NextObjId1` | DWORD | Next object ID (part 1). *(PDF shows “-”.)* |
| `Mod_NWMResName` | CExoString | If saved from an NWM module, the **filename** of that NWM. |
| `Mod_PlayerList` | List | Players in the module. **StructID 48813.** |
| `Mod_Tokens` | List | Custom tokens. **StructID 7.** |
| `Mod_TURDList` | List | Temporary User Resource Data entries. **StructID 13634816.** |
| `Mod_VarTable` | List | Module variables and values. **StructID 0.** |

---

## 3. Common lists and structs

Descriptions of **Lists** in an IFO file. Each subsection is named for the **List Field’s Label** and gives the **StructID** of structs in that List.

### 3.1 Mod_Area_List

**Module area list** — all areas in the module.

#### Table 3.1: Fields in area list struct (StructID 6)

| Label | Type | Description |
|-------|------|-------------|
| `AreaName` | CResRef | ResRef of the area. The module must contain **three** files with this ResRef: **ARE**, **GIT**, and **GIC**. |
| `ObjectId` | DWORD | **ObjectID** of the area. *(Save game only; not written by the toolset.)* |

---

### 3.2 Mod_CacheNSSList

**Cached script list** — scripts the NWN server should cache (typically hot paths).

#### Table 3.2: Fields in cached script list struct (StructID 9)

| Label | Type | Description |
|-------|------|-------------|
| `ResRef` | CResRef | Script ResRef. Each script has NSS source and a compiled **NCS**. |

---

### 3.3 Mod_HakList

**HAK pak list** — HAKs used by the module, **highest priority first** (earlier entries override later ones).

#### Table 3.3: Fields in HAK pak list struct (StructID 8)

| Label | Type | Description |
|-------|------|-------------|
| `Mod_Hak` | CExoString | HAK filename **without** the `.hak` extension. |

---

## 4. Save-game lists and structs

Lists present after the **game** saves the module. Subsections use each List’s **Label**.

Most in-game entities have an **ObjectID**; ObjectIDs therefore appear often in save-game List structs.

### 4.1 EventQueue

**Event queue** — events in the module. See **§5** of [Bioware Aurora Common GFF Structs](Bioware-Aurora-CommonGFFStructs).

---

### 4.2 Mod_PlayerList

**Player list** — each element uses **StructID 48813**. The Player struct is large enough that it is **not** fully specified in the IFO document (it would need its own format spec).

---

### 4.3 Mod_Tokens

**Module custom tokens** — from NWScript:

```c
void SetCustomToken(int nCustomTokenNumber, string sTokenValue)
```

#### Table 4.3: Fields in a token struct (StructID 7)

| Label | Type | Description |
|-------|------|-------------|
| `Mod_TokensNumber` | DWORD | Token number (`nCustomTokenNumber`). |
| `Mod_TokensValue` | CExoString | Token value (`sTokenValue`). |

---

### 4.4 Mod_TURDList

**Temporary User Resource Data (TURD)** — stores information for players who joined and later **disconnected**. On rejoin, login name and PC name are matched against the TURD list to detect **returning** players and restore state from the TURD entry.

#### Table 4.4a: Fields in a TURD struct (StructID 13634816)

| Label | Type | Description |
|-------|------|-------------|
| `EffectList` | List | Effects. **StructID 2.** See **§4** of [Bioware Aurora Common GFF Structs](Bioware-Aurora-CommonGFFStructs). |
| `Mod_MapAreasData` | Binary | *(PDF: “-”.)* |
| `Mod_MapDataList` | List | **MapData** entries. **StructID 0**; struct contains the indented fields below. |
| `Mod_MapData` | Binary | *(PDF: “-”.)* |
| `ModMapNumAreas` | INT | *(PDF: “-”.)* |
| `TURD_AreaId` | DWORD | ObjectID of the area where the player logged out. |
| `TURD_CalendarDay` | DWORD | Calendar day when the TURD was created. |
| `TURD_CommntyName` | CExoString | Multiplayer login / community name. |
| `TURD_FirstName` | CExoLocString | PC first name. |
| `TURD_LastName` | CExoLocString | PC last name. |
| `TURD_OrientatX` | FLOAT | Logout orientation (with Y/Z). |
| `TURD_OrientatY` | FLOAT | |
| `TURD_OrientatZ` | FLOAT | |
| `TURD_PersonalRep` | List | Personal reputations others hold toward the player. **StructID 47787** — see [Table 4.4b](#table-44b-personal-reputation) below. |
| `TURD_PlayerID` | DWORD | ObjectID of the player. |
| `TURD_PositionX` | FLOAT | Logout position (with Y/Z). |
| `TURD_PositionY` | FLOAT | |
| `TURD_PositionZ` | FLOAT | |
| `TURD_RepList` | List | Reputation per faction. **StructID 43962**; contains nested fields below. |
| `TURD_RepAmount` | INT | Reputation with faction **X**, where **X** is the **index** of this list element (**0–100**). |
| `TURD_TimeOfDay` | DWORD | Time of day when the TURD was generated. |
| `VarTable` | List | Variables on the character. **StructID 0.** See [§4.5](#45-vartable). |

<a id="table-44b-personal-reputation"></a>

#### Table 4.4b: Personal reputation struct (StructID 47787)

| Label | Type | Description |
|-------|------|-------------|
| `TURD_PR_Amount` | INT | Reputation with the faction. |
| `TURD_PR_Day` | DWORD | *(PDF: “-”.)* |
| `TURD_PR_Decays` | BYTE | Boolean: decays. |
| `TURD_PR_Duration` | INT | Duration in **seconds**. |
| `TURD_PR_ObjId` | DWORD | ObjectID of the creature **holding** this personal-rep toward the TURD owner. |
| `TURD_PR_Time` | DWORD | *(PDF: “-”.)* |

---

### 4.5 VarTable

**Variable table** — scripting variables and values. See **§3** of [Bioware Aurora Common GFF Structs](Bioware-Aurora-CommonGFFStructs).

---

## See also

| Resource | Notes |
|----------|--------|
| [GFF-IFO](GFF-IFO) | KotOR module info implementation |
| [ERF-File-Format](ERF-File-Format) | MOD / SAV containers |
| [GFF-File-Format](GFF-File-Format) | GFF structure |
| [KEY-File-Format](KEY-File-Format) | Resource resolution |

---

*Edition notes: Per-page “BioWare Corp.” headers from the PDF are folded into the [about](#about-this-document) section. Table and section numbers match the archived BioWare IFO specification. Obvious PDF transcription issues are corrected (`tileIf` → “tile. If”; “same game” → “save game” where context is save vs toolset; duplicate “See See” → “See”). `Mod_StartMonth` range is left as in the source PDF (**1–24**) with a short note that it is engine-defined.*
