# Item (UTI) format — BioWare Aurora Engine

*Official BioWare Aurora documentation (archived extract).*

---

## Table of contents

- [About this document](#about-this-document)
- [1. Introduction](#1-introduction)
  - [1.1 Overview](#11-overview)
  - [1.2 Terminology](#12-terminology)
- [2. Item struct](#2-item-struct)
  - [2.1 Common item fields](#21-common-item-fields)
    - [2.1.1 Fields in all items (Table 2.1.1)](#211-fields-in-all-items-table-211)
    - [2.1.2 Additional fields by ModelType](#212-additional-fields-by-modeltype)
    - [2.1.3 ItemProperty fields (Table 2.1.3)](#213-itemproperty-fields-table-213)
  - [2.2 Item blueprint fields (Table 2.2)](#22-item-blueprint-fields-table-22)
  - [2.3 Item instance fields (Table 2.3)](#23-item-instance-fields-table-23)
  - [2.4 Item game instance fields (Table 2.4)](#24-item-game-instance-fields-table-24)
- [3. InventoryObject struct](#3-inventoryobject-struct)
  - [3.1 Common fields (Table 3.1)](#31-common-fields-table-31)
  - [3.2 Blueprint fields (Table 3.2)](#32-blueprint-fields-table-32)
  - [3.3 Instance fields](#33-instance-fields)
  - [3.4 Game instance fields](#34-game-instance-fields)
- [4. Calculations and procedures](#4-calculations-and-procedures)
  - [4.1 Icon and model part availability](#41-icon-and-model-part-availability)
  - [4.2 Property availability](#42-property-availability)
  - [4.3 Property description construction](#43-property-description-construction)
  - [4.4 Cost calculation](#44-cost-calculation)
  - [4.5 Required lore and level](#45-required-lore-and-level)
- [5. Item-related 2DA files](#5-item-related-2da-files)
  - [5.1 Base items (`baseitems.2da`)](#51-base-items-baseitems2da)
  - [5.2 Item property definitions (`itempropdef.2da`)](#52-item-property-definitions-itempropdef2da)
  - [5.3 Item property availability (`itemprops.2da`)](#53-item-property-availability-itemprops2da)
  - [5.4 Item property subtype tables](#54-item-property-subtype-tables)
  - [5.5 Item cost tables](#55-item-cost-tables)
  - [5.6 Item param tables](#56-item-param-tables)
  - [5.7 Miscellaneous item tables](#57-miscellaneous-item-tables)
- [See also](#see-also)

---

## About this document

**Source:** Official BioWare Aurora Engine Item Format PDF, archived in [`vendor/xoreos-docs/specs/bioware/Item_Format.pdf`](https://github.com/xoreos/xoreos-docs/blob/master/specs/bioware/Item_Format.pdf) (mirror: [`th3w1zard1/xoreos-docs/.../Item_Format.pdf`](https://github.com/th3w1zard1/xoreos-docs/blob/master/specs/bioware/Item_Format.pdf)). Originally published on `nwn.bioware.com`.

> **Note:** Written for **Neverwinter Nights**; the **Item (UTI) format is identical in KotOR**. NWN-specific examples may appear, but the core GFF layout and procedures match KotOR.

*BioWare Corp. · [bioware.com](http://www.bioware.com) · BioWare Aurora Engine — Item format*

---

## 1. Introduction

### 1.1 Overview

An **item** can sit in an area or in a **container** (creature, placeable, store, etc.).

Items use **[GFF](Bioware-Aurora-GFF)**. This document assumes GFF literacy.

- **Blueprints** — GFF files with extension **`.uti`** and **`FileType`** **`"UTI "`**.
- **Instances** — **Item** structs inside a module’s **GIT** files.

### 1.2 Terminology

| Term | Meaning |
|------|---------|
| **icon** | 2D inventory image; may be one texture or composed from parts. |
| **model** | 3D representation (ground vs equipped may differ; some items have no equipped model). |

---

## 2. Item struct

GFF **Item** struct fields differ between **blueprints** and **instances**. **List** fields note the **StructID** of list elements.

### 2.1 Common item fields

#### 2.1.1 Fields in all items (Table 2.1.1)

Present on **all** Item structs (blueprint, instance, toolset, or game).

| Label | Type | Description |
|-------|------|-------------|
| `AddCost` | DWORD | Additional cost. |
| `BaseItem` | INT | Row index in `baseitems.2da`. |
| `Charges` | BYTE | Charges **remaining** (no separate “max charges” field). |
| `Cost` | DWORD | Item cost. |
| `Cursed` | BYTE | **1** = cannot remove from container (undroppable / unsellable / unpickpocketable); **0** = removable. |
| `DescIdentified` | CExoLocString | Identified description. |
| `Description` | CExoLocString | Unidentified description. |
| `LocName` | CExoLocString | Name in toolset palette, Item Properties dialog, and in-game when **identified**. |
| `Plot` | BYTE | **1** = plot item (cannot be sold); **0** = normal. |
| `PropertiesList` | List | **ItemProperty** structs. **StructID 0.** See [§2.1.3](#213-itemproperty-fields-table-213). |
| `StackSize` | WORD | **1** if base item is unstackable; else stack count **≥ 1** (e.g. 50 arrows). |
| `Stolen` | BYTE | **1** if stolen; **0** if not. |
| `Tag` | CExoString | Item tag (up to **32** characters). |
| `TemplateResRef` | CResRef | **Blueprint:** should match UTI filename. **Instance:** ResRef of source blueprint. |

#### 2.1.2 Additional fields by ModelType

`BaseItem` selects a `baseitems.2da` row; **`ModelType`** controls appearance (see [§4.1](#41-icon-and-model-part-availability)). Besides [Table 2.1.1](#211-fields-in-all-items-table-211), include the rows from the tables below that match the item’s ModelType.

**Table 2.1.2.1 — Layered (ModelType **1**) and Armor (ModelType **3**)**

| Label | Type | Description |
|-------|------|-------------|
| `Cloth1Color` | BYTE | Row index into `pal_cloth01.tga` for **cloth1** PLT layer. |
| `Cloth2Color` | BYTE | **cloth2** PLT layer. |
| `Leather1Color` | BYTE | Row index into `pal_leath01.tga` for **leather1**. |
| `Leather2Color` | BYTE | **leather2**. |
| `Metal1Color` | BYTE | Row index into `pal_armor01.tga` for **metal1**. |
| `Metal2Color` | BYTE | **metal2**. |

**Table 2.1.2.2 — Simple (ModelType **0**) and Layered (ModelType **1**)**

| Label | Type | Description |
|-------|------|-------------|
| `ModelPart1` | BYTE | Part number. |

**Table 2.1.2.3 — Composite (ModelType **2**)**

| Label | Type | Description |
|-------|------|-------------|
| `ModelPart1` | BYTE | Part number. |
| `ModelPart2` | BYTE | Part number. |
| `ModelPart3` | BYTE | Part number. |

**Table 2.1.2.4 — Armor (ModelType **3**)**

| Label | Type | Description |
|-------|------|-------------|
| `ArmorPart_Belt` | BYTE | Index into `parts_belt.2da`. |
| `ArmorPart_LBicep` | BYTE | `parts_bicep.2da` |
| `ArmorPart_LFArm` | BYTE | `parts_forearm.2da` |
| `ArmorPart_LFoot` | BYTE | `parts_foot.2da` |
| `ArmorPart_LHand` | BYTE | `parts_hand.2da` |
| `ArmorPart_LShin` | BYTE | `parts_shin.2da` |
| `ArmorPart_LShoul` | BYTE | `parts_shoulder.2da` |
| `ArmorPart_LThigh` | BYTE | `parts_legs.2da` |
| `ArmorPart_Neck` | BYTE | `parts_neck.2da` |
| `ArmorPart_Pelvis` | BYTE | `parts_pelvis.2da` |
| `ArmorPart_RBicep` | BYTE | `parts_bicep.2da` |
| `ArmorPart_RFArm` | BYTE | `parts_forearm.2da` |
| `ArmorPart_RFoot` | BYTE | `parts_foot.2da` |
| `ArmorPart_RHand` | BYTE | `parts_hand.2da` |
| `ArmorPart_Robe` | BYTE | `parts_robe.2da` |
| `ArmorPart_RShin` | BYTE | `parts_shin.2da` |
| `ArmorPart_RShoul` | BYTE | `parts_shoulder.2da` |
| `ArmorPart_RThigh` | BYTE | `parts_legs.2da` |
| `ArmorPart_Torso` | BYTE | `parts_torso.2da` |

#### 2.1.3 ItemProperty fields (Table 2.1.3)

Each element of **`PropertiesList`** (**StructID 0**):

| Label | Type | Description |
|-------|------|-------------|
| `ChanceAppear` | BYTE | Obsolete; always **100**. |
| `CostTable` | BYTE | Index into `iprp_costtable.2da`. Must match **`CostTableResRef`** on the `itempropdef.2da` row indexed by **`PropertyName`**. Required. |
| `CostValue` | WORD | Index into the **cost** 2DA named by the **`Name`** column of `iprp_costtable.2da` at row **`CostTable`**. Required. |
| `Param1` | BYTE | Index into `iprp_paramtable.2da` (params table). **−1** / no parameters: see below. |
| `Param1Value` | BYTE | Index into the params 2DA whose ResRef is **`TableResRef`** on the `iprp_paramtable.2da` row **`Param1`**. Defaults to **0** if unused. |
| `Param2` | BYTE | Obsolete (was second param table ref). |
| `Param2Value` | BYTE | Obsolete. |
| `PropertyName` | WORD | Index into **`itempropdef.2da`**. Required. |
| `Subtype` | WORD | Index into subtype 2DA whose ResRef is **`SubTypeResRef`** on the `itempropdef.2da` row **`PropertyName`**. **0** if no subtype table. |

**When are there no `Param1` parameters?**

- **If Subtype is used:** no params if the subtype table has **no** `Param1ResRef` column, or that column is **`****`** on the row indexed by **`Subtype`**.
- **If no Subtype:** no params if **`itempropdef.2da`** has **`****`** in **`Param1ResRef`** on the row indexed by **`PropertyName`**.

### 2.2 Item blueprint fields (Table 2.2)

Top-level UTI struct: [Table 2.1.1](#211-fields-in-all-items-table-211) **plus**:

| Label | Type | Description |
|-------|------|-------------|
| `Comment` | CExoString | Designer comment. |
| `PaletteID` | BYTE | Item palette tree node ID. |
| `TemplateResRef` | CResRef | Must match the **UTI filename**; tools may validate this instead of the file ResRef. If you rename the file outside the toolset, update this field. |

### 2.3 Item instance fields (Table 2.3)

GIT **Item** instance: [Table 2.1.1](#211-fields-in-all-items-table-211) **plus**:

| Label | Type | Description |
|-------|------|-------------|
| `TemplateResRef` | CResRef | Blueprint ResRef this instance was created from. |
| `XOrientation` | FLOAT | X component of orientation unit vector. |
| `YOrientation` | FLOAT | Y component. |
| `XPosition` | FLOAT | Position in area. |
| `YPosition` | FLOAT | |
| `ZPosition` | FLOAT | |

An Item instance inside an **InventoryObject** (see [§3](#3-inventoryobject-struct)) **does not** add these extra fields beyond what InventoryObject + Item rules require.

### 2.4 Item game instance fields (Table 2.4)

After the **game** saves GIT, the Item instance also has:

| Label | Type | Description |
|-------|------|-------------|
| `ObjectId` | DWORD | Engine object ID. |
| `VarTable` | List | Script variables. **StructID 0.** See **§3** of [Bioware Aurora Common GFF Structs](Bioware-Aurora-CommonGFFStructs). |

**`INVALID_OBJECT_ID`** = **`0x7F000000`**.

---

## 3. InventoryObject struct

**InventoryObject** structs live in a container’s **`ItemList`**. Creatures, items, and placeables can be containers.

Toolset items normally have **no** `ItemList`; save games / GIT / IFO / **BIC** may. The game may set each list element’s **StructID** to its **index** in `ItemList`.

### 3.1 Common fields (Table 3.1)

| Label | Type | Description |
|-------|------|-------------|
| `Repos_PosX` | WORD | Grid X. |
| `Repos_PosY` | WORD | Grid Y. |

### 3.2 Blueprint fields (Table 3.2)

[Table 3.1](#31-common-fields-table-31) **plus**:

| Label | Type | Description |
|-------|------|-------------|
| `InventoryRes` | CResRef | UTI blueprint ResRef. |

### 3.3 Instance fields

InventoryObject instance = [Table 3.1](#31-common-fields-table-31) plus Item instance fields from [Tables 2.1.1 and 2.3](#211-fields-in-all-items-table-211).

### 3.4 Game instance fields

GIT InventoryObject game instance = [Table 3.1](#31-common-fields-table-31) plus Item fields from [2.1.1, 2.3, and 2.4](#211-fields-in-all-items-table-211). For placement in container UI: **`XOrientation`** = **1.0**; **`YOrientation`** and positions = **0.0**.

**BIC** matches save-game InventoryObjects **except** it omits [Table 2.4](#24-item-game-instance-fields-table-24) fields.

---

## 4. Calculations and procedures

### 4.1 Icon and model part availability

Model and icon ResRefs end with a **3-digit zero-padded** number, e.g. `helm_001.mdl`, `iwaxbt_t_011.tga`.

**Tokens**

- **`<ItemClass>`** — from `baseitems.2da`.
- **`<number>`** — part number.

If a model is missing, use **`DefaultModel`** from `baseitems.2da`. If an icon is missing, use **`DefaultIcon`**.

Icon pixel size: **32 × `InvSlotWidth`** by **32 × `InvSlotHeight`** (from `baseitems.2da`).

#### 4.1.1 Simple (ModelType 0)

```text
Model  = <ItemClass>*<number>.mdl      e.g. it_torch_001.mdl
Icon   = i<ItemClass>*<number>.tga     e.g. iit_torch_001.tga
```

Usually one shared model; icons vary. Toolset offers icons for existing TGAs from **`MinRange`–`MaxRange`**.

#### 4.1.2 Layered (ModelType 1)

```text
Model  = <ItemClass>_<number>.mdl     e.g. helm_001.mdl
Icon   = i<ItemClass>*<number>.plt     e.g. ihelm_001.plt
```

Scan PLT icons from **`MinRange`–`MaxRange`**; if icon exists, assume matching MDL exists (exception: **helmets** — verify **MDL**).

#### 4.1.3 Composite (ModelType 2)

```text
Model  = <ItemClass>*<position>*<number>.mdl   e.g. waxbt_b_011.mdl
Icon   = i<Model ResRef>.tga
```

**`<position>`** = **`b`** (bottom), **`m`** (middle), **`t`** (top) — e.g. pommel / hilt / blade.

For weapons, the three digits split into **shape** (first two) and **color** (last digit): `011`, `021`, `031` same color; `011`, `012`, `013` same shape.

**Color range per layer:** scan icons from MinRange–MaxRange; first hit gives min color (last digit); continue until color changes — previous color was max.

**Shapes:** scan `012`, `022`, … (step **10**). If `082` exists, assume `083`, `084` exist for that shape.

Composite icon paint order: **bottom → middle → top** (overlapping).

#### 4.1.4 Armor (ModelType 3)

```text
Model  = p<gender><race><phenotype>*<bodypart><number>.mdl   e.g. pmh0_chest001.mdl
Icon   = ip<gender>_<bodypart><number>.plt                   e.g. ipm_chest001.plt
```

- **`<gender>`** = **`m`** or **`f`**
- **`<bodypart>`** — see **`capart.2da`** (belt, bicepl, bicepr, chest, footl, footr, forel, forer, handl, handr, legl, legr, neck, pelvis, shinl, shinr, shol, shor, …)

Full armor icon draw order: **pelvis, chest, belt, right shoulder, left shoulder, robe** (others have no icons).

**Table 4.1.4 — Body part → `parts_*.2da`**

| Body part(s) | 2DA |
|--------------|-----|
| belt | `parts_belt` |
| bicepl, bicepr | `parts_bicep` |
| chest | `parts_chest` |
| footl, footr | `parts_foot` |
| forel, forer | `parts_forearm` |
| handl, handr | `parts_hand` |
| legl, legr | `parts_legs` |
| neck | `parts_neck` |
| pelvis | `parts_pelvis` |
| robe | `parts_robe` |
| shinl, shinr | `parts_shin` |
| shol, shor | `parts_shoulder` |

If a `parts_<part>.2da` row has **`ACBONUS`** ≠ **`****`**, that row index is a selectable part. Part **000** can mean “empty” piece (no geometry). Toolset sorts by **`ACBONUS`** then row index (for non-chest, used for sorting only, not AC). **Robes** can hide other parts via **`HIDE<PART>`** columns in `parts_robe.2da` (**1** = hidden).

### 4.2 Property availability

Use **`PropColumn`** from `baseitems.2da` → find the column in **`itemprops.2da`** whose name starts with that number (e.g. **`16_Misc`**). Value **1** = property row available for that base item; **`****`** = not available. Rows align with **`itempropdef.2da`**.

*Example:* base item **12** (amulet) has **`PropColumn` 16** → read column **`16_Misc`** in `itemprops.2da`.

### 4.3 Property description construction

Toolset format:

```text
PropertyName : Subtype [CostValue] [Param1: Param1Value]
```

Examples: `Damage Bonus vs. Racial Type: Dragon [1 Damage] [Type: Acid]` — game uses similar text **without** square brackets.

#### 4.3.1 PropertyName

StrRef from column **0** (**Name**) of **`itempropdef.2da`** at row **`PropertyName`**.

#### 4.3.2 Subtype

**`SubTypeResRef`** on that row: if **`****`**, omit subtype text. Else load subtype 2DA, index **`Subtype`**, read name StrRef.

#### 4.3.3 CostTable value

**`CostTableResRef`** on `itempropdef.2da` row = index into **`iprp_costtable.2da`** → **`Name`** = cost-table ResRef. Index **`CostValue`** in that table → **`Name`** StrRef (e.g. `1 Damage`).

#### 4.3.4 Param

Resolve param table index from subtype’s **`Param1ResRef`** if present; else from **`itempropdef.2da`** **`Param1ResRef`**. Index **`iprp_paramtable.2da`** → **`Name`** StrRef (param label) and **`TableResRef`** (param 2DA). Index **`Param1Value`** in that param 2DA → value StrRef.

### 4.4 Cost calculation

```text
ItemCost = [ BaseCost + 1000*(Multiplier² − NegMultiplier²) + SpellCosts ] * MaxStack * BaseMult + AdditionalCost
```

- **`BaseMult`** — **`ItemMultiplier`** (`baseitems.2da`).
- **`AdditionalCost`** — Item **`AddCost`**.

#### 4.4.1 Base cost

**Non-armor:** **`BaseCost`** column (`baseitems.2da`).

**Armor:** use **`armor.2da`** cost for armor whose base AC comes from **`parts_chest.2da`** **`ACBONUS`** at the chest **`ArmorPart`** index.

#### 4.4.2 Multipliers

- **`Multiplier`** — sum of **positive** item-property costs.
- **`NegMultiplier`** — sum of **negative** property costs.
- **Cast Spell** (**`PropertyName` = 15**) is **excluded** here; it goes into **`SpellCosts`**.

Per property:

```text
ItemPropertyCost = PropertyCost + SubtypeCost + CostValue
```

Add to **`Multiplier`** or **`NegMultiplier`** by sign. **Params do not change** property cost.

- **`PropertyCost`** — **`Cost`** float on **`itempropdef.2da`** row **`PropertyName`** (`****` → 0).
- **`SubtypeCost`** — only if **`PropertyCost` = 0**: **`Cost`** on subtype 2DA row **`Subtype`**. If **`PropertyCost` > 0**, **`SubtypeCost` = 0**.
- **`CostValue`** — cost 2DA **`Cost`** at row **`CostValue`**, where the 2DA ResRef comes from **`iprp_costtable.2da`** via **`CostTable`**.

#### 4.4.3 Cast spell costs

```text
CastSpellCost = (PropertyCost + CostValue) * SubtypeCost
```

Same term resolution as non-cast spells. Then weight:

- Most expensive Cast Spell: **×100%**
- Second most: **×75%**
- All others: **×50%**

Sum → **`SpellCosts`**; plug into top-level formula.

### 4.5 Required lore and level

- **Character level to use item:** **1 +** smallest row index in **`itemvalue.2da`** where **`MAXSINGLEITEMVALUE`** ≥ item cost.
- **Lore DC to identify:** row index in **`skillvsitemcost.2da`** where **`DeviceCostMax`** is the smallest value still **≥** item cost.

---

## 5. Item-related 2DA files

### 5.1 Base items (`baseitems.2da`)

Defines item **types**; many stats are fixed per row (not from `PropertiesList`).

#### Column reference (Table 5.1)

| Column | Type | Description |
|--------|------|-------------|
| `Name` | Integer | StrRef — base type display name. |
| `Label` | String | Programmer label. |
| `InvSlotWidth` | Integer | Icon width in grid cells. |
| `InvSlotHeight` | Integer | Icon height in grid cells. |
| `EquipableSlots` | Integer | Bitmask — see [EquipableSlots flags](#equipableslots-flags). |
| `ModelType` | Integer | **0** simple, **1** layered, **2** composite, **3** armor — see [§4.1](#41-icon-and-model-part-availability). |
| `ItemClass` | String | Base ResRef for icon/model naming. |
| `GenderSpecific` | Integer | **0** same art all genders; **1** differs. |
| `Part1EnvMap` / `Part2EnvMap` / `Part3EnvMap` | Integer | **1** env-map that part; **0** off. |
| `DefaultModel` | String | Fallback MDL ResRef. |
| `Container` | Integer | **0** not container; **1** container. |
| `WeaponWield` | Integer | Wield style (`****`, 1, 4–11 — see PDF). |
| `WeaponType` | Integer | Damage type 0–4. |
| `WeaponSize` | Integer | 1 tiny … 5 huge. |
| `RangedWeapon` | Integer | `****` or index. |
| `PrefAttackDist` | Float | Preferred attack distance for weapons. |
| `MinRange` / `MaxRange` | Integer | Part scan range (0–999). |
| `NumDice` / `DieToRoll` | Integer | Weapon damage dice; `****` if N/A. |
| `CritThread` / `CritHitMult` | Integer | Threat / multiplier; `****` if N/A. |
| `Category` | Integer | 0–19 item category (melee, ranged, armor, …). |
| `BaseCost` | Integer | Base cost term. |
| `Stacking` | Integer | Max stack size. |
| `ItemMultiplier` | Integer | Cost formula multiplier ([§4.4](#44-cost-calculation)). |
| `Description` | Integer | StrRef when unidentified / no per-item description. |
| `InvSoundType` | Integer | 0–9 inventory drag sound class; ResRef pattern **`XX_YYYYY`** (`XX` = **PU** or **DR**). |
| `MaxProps` / `MinProps` | Integer | Cast-spell property limits. |
| `PropColumn` | Integer | Selects **`itemprops.2da`** column prefix ([§4.2](#42-property-availability)). |
| `StorePanel` | Integer | Store tab (armor, weapons, potions, …). |
| `ReqFeat0`–`ReqFeat4` | Integer | Required feats (`****` = none). |
| `AC_Enchant` | Integer | AC bonus type 0–4. |
| `BaseAC` | Integer | Equipped AC (**shields**; not armor chest AC). |
| `ArmorCheckPen` | Integer | ACP. |
| `BaseItemStatRef` | Integer | StrRef — item stat block. |
| `ChargesStarting` | Integer | Default charges. |
| `RotateOnGround` | Integer | Ground orientation 0–2. |
| `TenthLBS` | Integer | Weight in tenths of pounds. |
| `WeaponMatType` | Integer | Index into `weaponsounds.2da`. |
| `AmmunitionType` | Integer | Ammo kind (`****` or 0–6). |
| `QBBehaviour` | Integer | Quickbar behavior 0–2. |
| `ArcaneSpellFailure` | Integer | ASF % or `****`. |
| `%AnimSlashL` / `%AnimSlashR` / `%AnimSlashS` | Integer | Melee anim weights (see PDF). |
| `StorePanelSort` | Integer | 0–99 store ordering. |
| `ILRStackSize` | Integer | Sometimes used instead of **`StackSize`** in cost calc. |

<a id="equipableslots-flags"></a>

#### EquipableSlots flags

| Bit | Slot |
|-----|------|
| `0x1` | HEAD |
| `0x2` | CHEST |
| `0x4` | BOOTS |
| `0x8` | ARMS |
| `0x10` | RIGHTHAND |
| `0x20` | LEFTHAND |
| `0x40` | CLOAK |
| `0x80` | LEFTRING |
| `0x100` | RIGHTRING |
| `0x200` | NECK |
| `0x400` | BELT |
| `0x800` | ARROWS |
| `0x1000` | BULLETS |
| `0x2000` | BOLTS |

`CanRotateIcon`: **1** = may rotate 90° on quickbar; **0** = fixed.

#### `WeaponWield` values

| Value | Meaning |
|-------|---------|
| `****` | Cannot wield, or melee weapon held one/two hands by creature size. |
| 1 | Non-weapon |
| 4 | Pole |
| 5 | Bow |
| 6 | Crossbow |
| 7 | Shield |
| 8 | Two-bladed |
| 9 | Creature weapon |
| 10 | Sling |
| 11 | Thrown |

#### `Category` values

| Value | Category |
|-------|----------|
| 0 | none |
| 1 | melee |
| 2 | ranged |
| 3 | shield |
| 4 | armor |
| 5 | helmet |
| 6 | ammo |
| 7 | thrown |
| 8 | staves |
| 9 | potion |
| 10 | scroll |
| 11 | thieves' tools |
| 12 | misc |
| 13 | wands |
| 14 | rods |
| 15 | traps |
| 16 | misc unequippable |
| 17 | container |
| 19 | healers |

#### `InvSoundType` (inventory drag sound class)

| Value | Class |
|-------|--------|
| 0 | Armor |
| 1 | Shield |
| 2 | Wood melee |
| 3 | Metal melee |
| 4 | Ranged |
| 5 | Ammo |
| 6 | Potion |
| 7 | Paper |
| 8 | Treasure |
| 9 | Generic |

ResRef pattern: **`XX_YYYYY`** where **`XX`** = **PU** (pickup/equip) or **DR** (drop/unequip); **`YYYYY`** is fixed per class above.

### 5.2 Item property definitions (`itempropdef.2da`)

| Column | Type | Description |
|--------|------|-------------|
| `Name` | Integer | StrRef — property name. |
| `Label` | String | Label. |
| `SubTypeResRef` | String | Subtype 2DA ResRef (`****` if none). |
| `Cost` | Float | Property cost ([§4.4](#44-cost-calculation)). |
| `CostTableResRef` | Integer | Row in **`iprp_costtable.2da`**. |
| `Param1ResRef` | Integer | `****` or index into **`iprp_paramtable.2da`**. |
| `GameStrRef` | Integer | Partial in-game string. |
| `Description` | Integer | StrRef — description. |

### 5.3 Item property availability (`itemprops.2da`)

Dynamic columns **`<number>_<string>`**: **`number`** matches **`PropColumn`** from `baseitems.2da`. **1** = property available; **`****`** = not. Rows pair with **`itempropdef.2da`**. **`StringRef`** should match **`Name`** StrRef in `itempropdef.2da`.

> **2DA quirk:** Extra unlabeled columns may appear **before** **`Label`**; **`Label`** is treated as last real column. **Insert** new columns before **`Label`**, do not append.

### 5.4 Item property subtype tables

**Table 5.4 — common subtype columns**

| Column | Type | Description |
|--------|------|-------------|
| `Name` | String | StrRef — subtype name. |
| `Label` | String | Label. |
| `Cost` | Float | Required if `itempropdef.2da` **`Cost`** is `****`. |
| `Param1ResRef` | Integer | Param table index, or `****` → fall back to `itempropdef.2da`. |

**Extra columns (by file)**

| File | Extra column(s) | Description |
|------|-----------------|-------------|
| `iprp_ammotype.2da` | `AmmoType` | Index into `baseitems.2da`. |
| `iprp_feats.2da` | `FeatIndex` | Index into `feat.2da`. |
| `iprp_spells.2da` | `CasterLvl`, `InnateLvl`, `SpellIndex`, `PotionUse`, `WandUse`, `GeneralUse`, `Icon` | Spell/potion/wand usage and icon. |
| `spellshl.2da` | `Letter` | Unused. |

### 5.5 Item cost tables

**Registry:** **`iprp_costtable.2da`** lists cost-table 2DAs ( **`Name`** = ResRef of the cost table).

| Column | Type | Description |
|--------|------|-------------|
| `Name` | String | Cost-table 2DA ResRef. |
| `Label` | String | Label. |
| `ClientLoad` | Integer | **0** / **1** load scope. |

<a id="table-551-cost-table-columns"></a>

**Table 5.5.1 — columns present in every cost-table 2DA**

| Column | Type | Description |
|--------|------|-------------|
| `Cost` | Float | Cost contribution ([§4.4](#44-cost-calculation)). |
| `Name` | Integer | StrRef — entry label (`****` = row not assignable to **`CostValue`**). |
| `Label` | String | Label. |

**Table 5.5.2–5.5.17 — extra columns per cost-table 2DA** (all include [Table 5.5.1](#table-551-cost-table-columns) columns unless noted)

| Cost-table 2DA | Additional column(s) | Description |
|----------------|----------------------|-------------|
| `iprp_ammocost` | `Arrow`, `Bolt`, `Bullet` | ResRef of UTI blueprint to spawn that ammo (`****` if none). |
| `iprp_bonuscost` | `Value` | Bonus amount (ability, etc.). |
| `iprp_chargecost` | `PotionCost`, `WandCost` | Use instead of **`Cost`** for potions / wands. |
| `damagecost` | `NumDice`, `Die`, `Rank`, `GameString` | Dice damage; **`Rank`** orders strength; **`GameString`** e.g. `1d4`. |
| `damvulcost` | `Value` | Damage vulnerability **%**. |
| `immuncost` | `Value` | Immunity **%**. |
| `meleecost` | `Value` | Bonus to damage, AC, attack, enhancement, saves, etc. |
| `monstcost` | `NumDice`, `Die` | Dice (monster-related). |
| `neg5cost`, `neg10cost` | `Value` | Penalty to ability, AC, skill, etc. |
| `onhitcost` | `Value` | On-hit effect **DC**. |
| `redcost` | `Value` (float) | Multiply container weight by this and subtract from normal weight. |
| `resistcost` | `Amount` | Damage resistance (HP). |
| `soakcost` | `Amount` | Damage reduction soak (HP) when attack bonus requirement met. |
| `spellcost` | `SpellIndex` | Index into `spells.2da`. |
| `srcost` | `Value` | Spell resistance amount. |
| `weightcost` | `Value` (float) | Multiply item weight for modified weight. |

### 5.6 Item param tables

**Registry:** **`iprp_paramtable.2da`**

| Column | Type | Description |
|--------|------|-------------|
| `Name` | Integer | StrRef — parameter label. |
| `Label` | String | Programmer label *(archived PDF typo: “Lable”)*. |
| `TableResRef` | String | Param 2DA ResRef. |

**Param tables** include **`Name`** (StrRef) and **`Label`**. Extras: **`onhitdur`** (`EffectChance`, `DurationRounds`); **`weightinc`** (`Value` float pounds).

### 5.7 Miscellaneous item tables

#### 5.7.1 Item valuation

**`itemvalue.2da`**

| Column | Description |
|--------|-------------|
| `LABEL` | Level label; row **i** ↔ level **i+1**. |
| `DESIREDTREASURE` | Always **0**. |
| `MAXSINGLEITEMVALUE` | Max item cost usable at that level. |
| `TOTALVALUEFILTER` | Unused. |

**`skillvsitemcost.2da`**

| Column | Description |
|--------|-------------|
| `DeviceCostMax` | Max item cost identifiable at Lore check = row index. |
| `SkillReq_Class` / `SkillReq_Race` / `SkillReq_Align` | Use Magic Device ranks for edge cases (see PDF). |

#### 5.7.2 Armor statistics

**`capart.2da`:** `NAME`, `MDLNAME` (body-part token), `NODENAME` (attach node).

**`armor.2da`:** `ACBONUS`, `DEXBONUS`, `ACCHECK`, `ARCANEFAILURE%`, `WEIGHT`, `COST`, `DESCRIPTIONS`, `BASEITEMSTATREF`.

#### 5.7.3 Weapon combat sounds

**`weaponsounds.2da`** — material columns (`Leather0/1`, `Chain0/1`, …) hold hit WAV ResRefs; special cases for Stone/Wood/Chitin/etc. **`Parry0`**, **`Critical0`**, miss columns.

**Creature / placeable** routing via `appearance.2da` → `appearancesndset.2da` / `placeables.2da` → `placeableobjsnds.2da` → **`ArmorType`** column names in `weaponsounds.2da` with random **`0`/`1`** suffix. **`defaultacsounds.2da`** maps chest armor to **`ArmorType`**.

---

## See also

| Resource | Notes |
|----------|--------|
| [GFF-UTI](GFF-UTI) | KotOR item GFF |
| [GFF-File-Format](GFF-File-Format) | GFF data types |
| [2DA-baseitems](2DA-baseitems), [2DA-ammunitiontypes](2DA-ammunitiontypes) | Item / ammo tables |
| [KEY-File-Format](KEY-File-Format) | Resource resolution |

---

*Edition notes: Per-page BioWare letterheads removed. **§5.5** intro in the PDF incorrectly names `iprp_paramtable.2da` as the cost-table registry; this edition uses **`iprp_costtable.2da`** for §5.5 and **`iprp_paramtable.2da`** for §5.6. Minor OCR-style fixes: GIT sentence “contains does not contain” → “does not contain”; **`PropertyName`** typo “2PropertyName”; “them item” → “the item”; “contructed” → “constructed”; “sheields” → “shields”; “Mulitply/muliply” → “Multiply”; duplicate “additional” in a table title; “Sise” → “Size” where meant.*
