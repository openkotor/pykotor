# KotOR/TSL modding and engine concepts

This page defines core concepts used across the wiki. Format and tool pages link here to avoid duplicating long explanations.

## Resource Resolution Order

When the game needs a resource (by *ResRef* and **resource type**), it looks in a fixed sequence until the resource is found:

1. **Override folder** (`override/` in the game directory)
2. **Currently loaded MOD/ERF/[RIM](RIM-File-Format) module archives** (e.g. the module being played)
3. **Currently loaded save game** (when in-game; situational — often exposed as a loaded SAV / save-side container)
4. **BIF files** indexed by **KEY** (vanilla game data)
5. **Hardcoded defaults** (if the engine provides them)

So anything in `override/` or in a loaded [MOD](ERF-File-Format)/[ERF](ERF-File-Format)/[RIM](RIM-File-Format) set takes precedence over vanilla BIF content. Mods that only add or replace files often place them in override; installers like TSLPatcher and HoloPatcher write there and/or into MOD files or module [RIM](RIM-File-Format) archives.

### How the *resource manager* resolves a request

The engine’s *resource manager* resolves a **demand** by first checking whether the resource is already loaded or cached. If not, it routes the request to a back end depending on where the resource lives: directory (override or filesystem), encapsulated container ([MOD/ERF](ERF-File-Format) or [RIM](RIM-File-Format)), resource file, or BIF *image*. Each back end opens the correct file or container and returns the data. The [KEY](KEY-File-Format) is consulted only when the source is the BIF set (step 4 above). Override, MOD/ERF, and loaded module [RIM](RIM-File-Format) archives are always tried before any [**KEY**](KEY-File-Format)/[**BIF**](BIF-File-Format) lookup.

### Role of the [**KEY**](KEY-File-Format) file

The [**KEY**](KEY-File-Format) (e.g. `chitin.key`) maps *ResRef* + resource type to a location inside a [BIF](BIF-File-Format). It does not implement steps 1–3; higher-priority sources can shadow KEY-indexed assets without editing the KEY. For the binary layout of KEY files, see [KEY-File-Format](KEY-File-Format).

## ResRef (Resource Reference)

A **ResRef** is the resource’s name: a short string (up to ***16 characters*** in *KotOR*). Together with a **Resource Type** (numeric ID; see [Resource Type Identifiers](Resource-Formats-and-Resolution#resource-type-identifiers) and [GFF-File-Format](GFF-File-Format#gff-data-types)), the engine uses the *ResRef* to look up the resource via the [resource resolution order](#resource-resolution-order) above.

## Override Folder

The **override folder** is the directory named `override` in your KotOR or TSL game root. Files placed there are loaded before any BIF (vanilla) content. Modders use it for global replacements or additions: textures, models, scripts, 2DAs, dialog TLK, and GFF-based resources (creatures, items, etc.). Only one file per ResRef+type can be used at a time; if two mods put different files with the same name in override, one overwrites the other. For mergeable content (2DA, TLK), use an installer (TSLPatcher, HoloPatcher) that merges instead of overwriting. See [Mod-Creation-Best-Practices](Mod-Creation-Best-Practices#file-priority-and-where-to-put-your-files) and [Resource resolution order](#resource-resolution-order) above.

## [**BIF**](BIF-File-Format) and [**KEY**](KEY-File-Format)

[**BIF**](BIF-File-Format) (BioWare Index File) files are read-only containers that hold the bulk of vanilla game resources (models, textures, 2DAs, scripts, etc.). [**KEY**](KEY-File-Format) (e.g. `chitin.key`) is the master index: it maps *ResRef* + resource type to which BIF file and which entry inside that BIF. The game does not use BIFs directly by name; it uses the KEY to find the right BIF and offset. Mods do not modify KEY or BIF; they add content via override or MOD so that the engine finds their files first. See [KEY-File-Format](KEY-File-Format), [BIF-File-Format](BIF-File-Format).

## [**MOD**](ERF-File-Format) / [**ERF**](ERF-File-Format) / [**RIM**](RIM-File-Format)

[**ERF** (Encapsulated Resource File)](ERF-File-Format) is a container format that stores both *ResRef*s and resource data in one file. [**MOD**](ERF-File-Format) files (e.g. `module_name.mod`) are ERFs used for modules; [**SAV**](ERF-File-Format) for saves. [**RIM**](RIM-File-Format) (resource image) is the **stock** module archive format (`.rim`, often paired with `_s.rim` in the PC versions of the game); it uses a **different** on-disk layout than ERF--see [RIM-File-Format](RIM-File-Format) and [RIM versus ERF](ERF-File-Format#rim-versus-erf). When a module is loaded, the engine can satisfy resource requests from the active [MOD](ERF-File-Format) and/or [RIM](RIM-File-Format) set before falling back to [**KEY**](KEY-File-Format)/[**BIF**](BIF-File-Format); a `.mod` in `modules/` typically overrides the matching `.rim` pair. Module-specific content ([area GFFs](GFF-ARE), [module 2DAs](2DA-File-Format), etc.) ships in [RIM](RIM-File-Format) archives or is packed into a MOD for mods; global content is often placed in override. See [ERF-File-Format](ERF-File-Format), [RIM-File-Format](RIM-File-Format), and [Resource resolution order](#resource-resolution-order) above.

## [**GFF** (Generic File Format)](GFF-File-Format)

[**GFF**](GFF-File-Format) is BioWare’s binary format for structured game data: areas (ARE), creatures (UTC), items (UTI), dialogues (DLG), placeables (UTP), and many others. Files are hierarchical (structs, fields, lists). The same GFF layout is used across Aurora/Odyssey games; KotOR and TSL use specific GFF types and field meanings. Modders edit GFF with tools (KotOR Tool, Holocron Toolset, K-GFF) or via [TSLPatcher/HoloPatcher `[GFFList]` implementation](TSLPatcher-GFFList-Syntax). See [GFF-File-Format](GFF-File-Format), [Bioware-Aurora-GFF](Bioware-Aurora-GFF).

## [**2DA** (Two-Dimensional Array)](2DA-File-Format)

[**2DA**](2DA-File-Format) files are tabular data: rows and columns used for items, [spells](2DA-spells), [appearances](2DA-appearance), and most game configuration. The engine and [GFF](GFF-File-Format) resources reference [*2DA*](2DA-File-Format) rows by index or label. Mods often add or edit rows (e.g. new appearance row, new spell); when multiple mods change the same [*2DA*](2DA-File-Format), merging (e.g. via [*TSLPatcher*'s](TSLPatcher's-Official-Readme) `[2DAList]` implementation) avoids overwriting. See [2DA-File-Format](2DA-File-Format), [TSLPatcher-2DAList-Syntax](TSLPatcher-2DAList-Syntax).

## Resource Type Identifiers

The canonical **hex resource type ID** table (*Aurora* / *Odyssey* family, including rows unused in *KotOR*) lives on **[Resource formats and resolution — Resource Type Identifiers](Resource-Formats-and-Resolution#resource-type-identifiers)**. That page is the wiki SSOT for the numeric IDs and their four-character labels.

## Language IDs (*KotOR*)

Language IDs are a small integer enum shared across *Infinity*/*Aurora*/*Odyssey*/*Eclipse*-era engines (TLK headers, [ERF](ERF-File-Format) localized string lists, [GFF](GFF-File-Format) `LocalizedString` substrings, etc.). Newer *BioWare* titles added values but usually stay backward compatible with 0–5.

Use this table as the **wiki SSOT** for numeric IDs and typical text encodings. Official *BioWare* PDFs duplicate the same numbering in places like [Bioware-Aurora-TalkTable](Bioware-Aurora-TalkTable) and [Bioware-Aurora-LocalizedStrings](Bioware-Aurora-LocalizedStrings).

| Language | ID | Typical encoding | Description |
| -------- | -- | ---------------- | ----- |
| English  | 0  | Windows-1252     | Default for Western `dialog.tlk` and many legacy Aurora payloads |
| French   | 1  | Windows-1252     | |
| German   | 2  | Windows-1252     | |
| Italian  | 3  | Windows-1252     | |
| Spanish  | 4  | Windows-1252     | |
| Polish   | 5  | Windows-1250     | *KotOR 1 Polish* retail (**`cp-1250`**); see also **`dialogf.tlk`** in [TSLPatcher `[TLKList]` implementation](TSLPatcher-TLKList-Syntax) |
| Korean   | 6  | UTF-8            | Aurora TLK / tooling enum value; **not** used in shipped *KotOR 1/2* retail `dialog.tlk` sets |
| Chinese  | 7  | UTF-8            | Same as Korean row |
| Japanese | 8  | UTF-8            | Same as Korean row |

**Where the ID appears:** [TLK-File-Format](TLK-File-Format) file header and tooling; [ERF-File-Format](ERF-File-Format) localized description list per language; [GFF-File-Format](GFF-File-Format) `LocalizedString` embedded strings. KotOR often ignores the TLK header language field and loads the `dialog.tlk` that matches the installation—see [TLK-File-Format](TLK-File-Format#localization).

**Reference**:

- **[xoreos-docs](https://github.com/xoreos/xoreos-docs)** ([Mirror: th3w1zard1/xoreos-docs](https://github.com/th3w1zard1/xoreos-docs))
- [`specs/torlack/basics.html`](https://github.com/xoreos/xoreos-docs/blob/master/specs/torlack/basics.html) — Torlack’s Aurora basics (NWN-focused; IDs apply to *KotOR*).

### See also

- [Resource formats and resolution](Resource-Formats-and-Resolution) -- Format index, resolution order, hex resource type table
- [Home](Home) -- Wiki hub (formats, tools, tutorials)
- [KEY-File-Format](KEY-File-Format) -- KEY file format (e.g. `chitin.key`)
- [GFF-File-Format](GFF-File-Format) -- GFF file format (e.g. `area.gff`)
- [Mod-Creation-Best-Practices](Mod-Creation-Best-Practices) -- Best practices for modding
- [TLK-File-Format](TLK-File-Format) -- TLK file format (e.g. `dialog.tlk`)
