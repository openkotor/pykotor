# KotOR/TSL modding and engine concepts

This page defines core concepts used across the wiki. Format and tool pages link here to avoid duplicating long explanations.

## Resource resolution order

When the game needs a resource (by name and type), it looks in a fixed sequence until the resource is found. That sequence is:

1. **Override folder** (`override/` in the game directory)
2. **Currently loaded MOD/ERF files** (e.g. the module being played)
3. **Currently loaded save game** (when in-game; situational)
4. **BIF files** indexed by **KEY** (vanilla game data)
5. **Hardcoded defaults** (if the engine provides them)

So anything in `override/` or in a loaded MOD takes precedence over vanilla BIF content. Mods that only add or replace files often place them in override; installers like TSLPatcher and HoloPatcher write there and/or into MOD files. Full detail and engine behavior: [KEY-File-Format](KEY-File-Format#key-file-purpose), [Home](Home) (Odyssey Engine Basics --> Resource Resolution Order).

## ResRef (resource reference)

A **ResRef** is the resource’s name: a short string (up to 16 characters in KotOR, null-padded in binary). Together with a **resource type** (e.g. GFF, 2DA, NCS), the engine uses the ResRef to look up the resource via the resolution order above. Examples: `"danm13"` (area), `"nwscript"` (NSS), `"appearance"` (2DA). Definition and data type: [GFF-File-Format](GFF-File-Format#gff-data-types). KEY and BIF store ResRefs to map names to locations in BIFs; ERF/MOD store ResRefs inside the container.

## Override folder

The **override folder** is the directory named `override` in your KotOR or TSL game root. Files placed there are loaded before any BIF (vanilla) content. Modders use it for global replacements or additions: textures, models, scripts, 2DAs, dialog TLK, and GFF-based resources (creatures, items, etc.). Only one file per ResRef+type can be used at a time; if two mods put different files with the same name in override, one overwrites the other. For mergeable content (2DA, TLK), use an installer (TSLPatcher, HoloPatcher) that merges instead of overwriting. See [Mod-Creation-Best-Practices](Mod-Creation-Best-Practices#file-priority-and-where-to-put-your-files), [KEY-File-Format](KEY-File-Format#key-file-purpose).

## BIF and KEY

**BIF** (BioWare Index File) files are read-only containers that hold the bulk of vanilla game resources (models, textures, 2DAs, scripts, etc.). **KEY** (e.g. `chitin.key`) is the master index: it maps ResRef + resource type to which BIF file and which entry inside that BIF. The game does not use BIFs directly by name; it uses the KEY to find the right BIF and offset. Mods do not modify KEY or BIF; they add content via override or MOD so that the engine finds their files first. See [KEY-File-Format](KEY-File-Format), [BIF-File-Format](BIF-File-Format).

## MOD / ERF

**ERF** (Encapsulated Resource File) is a container format that stores both ResRefs and resource data in one file. **MOD** files (e.g. `module_name.mod`) are ERFs used for modules; **SAV** and **HAK** are other ERF variants. When a module is loaded, the engine can satisfy resource requests from that MOD before falling back to KEY/BIF. So module-specific content (area GFFs, module 2DAs, etc.) is often packed into a MOD; global content is often placed in override. See [ERF-File-Format](ERF-File-Format), [KEY-File-Format](KEY-File-Format#key-file-purpose).

## GFF (Generic File Format)

**GFF** is BioWare’s binary format for structured game data: areas (ARE), creatures (UTC), items (UTI), dialogues (DLG), placeables (UTP), and many others. Files are hierarchical (structs, fields, lists). The same GFF layout is used across Aurora/Odyssey games; KotOR and TSL use specific GFF types and field meanings. Modders edit GFF with tools (KotOR Tool, Holocron Toolset, K-GFF) or via TSLPatcher/HoloPatcher GFFList. See [GFF-File-Format](GFF-File-Format), [Bioware-Aurora-GFF](Bioware-Aurora-GFF).

## 2DA (two-dimensional array)

**2DA** files are tabular data: rows and columns used for items, spells, appearances, and most game configuration. The engine and GFF resources reference 2DA rows by index or label. Mods often add or edit rows (e.g. new appearance row, new spell); when multiple mods change the same 2DA, merging (e.g. via TSLPatcher 2DAList) avoids overwriting. See [2DA-File-Format](2DA-File-Format), [TSLPatcher-2DAList-Syntax](TSLPatcher-2DAList-Syntax).

### See also

- [KEY-File-Format](KEY-File-Format) — Resolution order, BIF index
- [GFF-File-Format](GFF-File-Format) — ResRef and GFF types
- [Mod-Creation-Best-Practices](Mod-Creation-Best-Practices) — Where to put files, merging
- [Home](Home) — Wiki hub and resource table
