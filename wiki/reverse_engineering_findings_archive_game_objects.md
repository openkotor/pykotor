# Game Object and Generic Structure Archives

KotOR game objects such as creatures, items, placeables, triggers, and related GFF-backed structures share a common runtime model. This archive preserves the supporting source links for the `common/`, `resource/generics/`, and related data-model modules behind that synthesis.

---

<a id="common_game_object_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — `common/game_object.py`

Verbatim lines removed from `Libraries/PyKotor/src/pykotor/common/game_object.py`. See `wiki/reverse_engineering_findings.md`.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (TypeScript game object)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/engine/GameObject.ts>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/engine/GameObject.ts>


---

<a id="common_misc_resref_class_docstring_pre_scrub"></a>

## Archived ResRef class docstring

Verbatim ast.get_docstring from `Libraries/PyKotor/src/pykotor/common/misc.py` (git HEAD) before scrub.

```
A string reference to a game resource.

ResRefs are the names of resources without the extension (the file stem).
They serve as identifiers for game resources stored in archives (BIF, ERF, RIM)
or as standalone files in the Override folder.

NOTE: ResRef Case-INSensitivity is critical for cross-platform compatibility

Used in:
-------
    - BioWare Archive/Container Files (BIF/ERF/MOD/RIM/SAV)
    - Filenames in the Override folder
    - GFF field values (ResRef field type)
    - Resource lookups and references throughout the engine

References:
----------
    Based on /K1/k1_win_gog_swkotor.exe GFF structure:
    - CResGFF::CreateGFFFile @ 0x00411260 - Creates GFF file structure

Derivations and Other Implementations:
----------
    - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Common/Data/ResRef.cs#L9-L72
    - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Common/Data/ResRef.cs#L9-L72
(ResRef class, max length 16)
    - Canonical (th3w1zard1/HoloPatcher.NET): https://github.com/th3w1zard1/HoloPatcher.NET/blob/600630e55e2b6a62e3ed84f8cd84a413baf7795d/src/TSLPatcher.Core/Common/ResRef.cs#L12-L132
(ResRef class with validation)
    - Canonical (th3w1zard1/HoloPatcher.NET): https://github.com/th3w1zard1/HoloPatcher.NET/blob/600630e55e2b6a62e3ed84f8cd84a413baf7795d/src/TSLPatcher.Core/Common/ResRef.cs#L15
(MaxLength constant = 16)
    - Canonical (th3w1zard1/HoloPatcher.NET): https://github.com/th3w1zard1/HoloPatcher.NET/blob/600630e55e2b6a62e3ed84f8cd84a413baf7795d/src/TSLPatcher.Core/Common/ResRef.cs#L15
(InvalidCharacters constant)
    - Upstream (Fair-Strides/KotOR-Bioware-Libs): https://github.com/Fair-Strides/KotOR-Bioware-Libs/tree/90ade1cace418f8e1130c53938d22e8acaa8bc41/KotOR_IO/File
    - Mirror (th3w1zard1/KotOR_IO): https://github.com/th3w1zard1/KotOR_IO/tree/8788712d037614f342e586b053b4645db19ff7a9/KotOR_IO/File
(ResRef GFF field type)
    - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/resource/ResourceTypes.ts
    - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/resource/ResourceTypes.ts
(Resource type definitions)
    - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Formats/AuroraFile.cs
    - Mirror (th3w1zard1/KotOR-dotNET): https://github.com/th3w1zard1/KotOR-dotNET/blob/1f212b52b72787dda8dca2514f05b70d7bae560e/AuroraFile.cs
(ResRef in C#)

Restrictions:
------------
    - ResRefs must be in ASCII format (non-ASCII characters are invalid)
    - ResRefs cannot exceed 16 characters in length (MAX_LENGTH = 16)
    - ResRefs cannot contain Windows filename invalid characters: '<>:"/\|?*'
    - Usable in case-insensitive applications (KOTOR was created for Windows case-insensitive filesystem)
    - (recommended) Stored as case-sensitive text for cross-platform compatibility
    - ResRefs are trimmed of whitespace (leading/trailing spaces removed)

Discrepancies:
-------------
    - reone lowercases ResRefs automatically (resref.h:37: boost::to_lower(_value))
    - PyKotor preserves case but uses casefold() for comparisons (case-insensitive equality)
    - HoloPatcher.NET preserves case but uses case-insensitive comparison (StringComparison.OrdinalIgnoreCase)
    - Kotor.NET preserves case without automatic lowercasing
    - Original engine: Windows case-insensitive filesystem, ResRefs stored as-is but matched case-insensitively
```


---

<a id="common_module_loader_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — `common/module_loader.py`

Verbatim lines removed from `Libraries/PyKotor/src/pykotor/common/module_loader.py`. See `wiki/reverse_engineering_findings.md`.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/Game.ts>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/Game.ts>


---

<a id="common_pathfinding_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — `common/pathfinding.py`

Verbatim lines removed from `Libraries/PyKotor/src/pykotor/common/pathfinding.py`. See `wiki/reverse_engineering_findings.md`.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (TypeScript pathfinding)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/pathfinding/Pathfinder.ts>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/pathfinding/Pathfinder.ts>


---

<a id="common_script_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — `common/script.py`

Verbatim lines removed from `Libraries/PyKotor/src/pykotor/common/script.py`. See `wiki/reverse_engineering_findings.md`.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (K1 script definitions)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/nwscript/NWScriptDefK1.ts>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/nwscript/NWScriptDefK1.ts>

- (K2 script definitions)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/nwscript/NWScriptDefK2.ts>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/nwscript/NWScriptDefK2.ts>


---

<a id="generics_are_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — resource/generics/are.py

Verbatim lines removed from Libraries/PyKotor/src/pykotor/resource/generics/are.py (Kotor.NET / KotOR.js field anchors). Normative layout: wiki/GFF-ARE.md. See wiki/reverse_engineering_findings.md.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L13>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L13>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L140>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L140>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L14>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L14>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L145>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L145>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L15-L17>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L15-L17>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L18>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L18>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L150>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L150>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L21>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L21>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L166>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L166>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L34>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L34>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L35-L75>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L35-L75>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L171-L246>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L171-L246>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L69-L79>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L69-L79>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L251-L281>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L251-L281>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L75-L78>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L75-L78>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L246-L250>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L246-L250>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L22-L31>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L22-L31>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L24-L32>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L24-L32>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L23-L33>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L23-L33>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L37-L46>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L37-L46>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L188-L200>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L188-L200>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L83>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L83>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L63-L66>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L63-L66>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L122>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L122>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L70-L72>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L70-L72>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L286-L297>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L286-L297>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L60-L80>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L60-L80>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L258>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L258>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L81>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L81>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L84-L94>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L84-L94>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L96>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L96>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L120>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L120>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L82>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L82>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L19-L68>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L19-L68>

- (various deprecated flags)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L155-L276>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L155-L276>

- (RoomName String property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L105>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L105>

- (room name)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleRoom.ts>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleRoom.ts>

- (DisableWeather Byte property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L102>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L102>

- (room_struct.set_uint8("DisableWeather", room.weather)) (room_struct.set_uint8("DisableWeather", room.weather)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleArea.ts#L463>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleArea.ts#L463>

- (EnvAudio Int32 property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L103>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L103>

- (audio.environmentAudio = 0)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleArea.ts#L138>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleArea.ts#L138>

- (ForceRating Int32 property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L104>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L104>

- (room_struct.set_int32("ForceRating", room.force_rating)) (room_struct.set_int32("ForceRating", room.force_rating)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleArea.ts#L464>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleArea.ts#L464>

- (AmbientScale Single property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L101>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/ARE.cs#L101>

- (room_struct.set_single("AmbientScale", room.ambient_scale)) (room_struct.set_single("AmbientScale", room.ambient_scale)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleArea.ts#L459>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleArea.ts#L459>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L105>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L105>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L102>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L102>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L103>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L103>

- (reference)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleArea.ts#L138>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleArea.ts#L138>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L104>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L104>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L101>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorARE/ARE.cs#L101>


---

<a id="generics_git_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — resource/generics/git.py

Verbatim lines removed from Libraries/PyKotor/src/pykotor/resource/generics/git.py (Kotor.NET / KotOR_IO anchors). Normative GFF layout: wiki/GFF-GIT.md. See wiki/reverse_engineering_findings.md (resource/generics/git.py).



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (GIT class and AreaProperties class)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs>

- Formats/GFF FileTypes/GIT.cs (GIT class)
  - Upstream (Fair-Strides/KotOR-Bioware-Libs): <https://github.com/Fair-Strides/KotOR-Bioware-Libs/tree/8788712d037614f342e586b053b4645db19ff7a9/KotOR_IO/File>
  - Mirror (th3w1zard1/KotOR_IO): <https://github.com/th3w1zard1/KotOR_IO/tree/8788712d037614f342e586b053b4645db19ff7a9/KotOR_IO/File>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L29-L37>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L29-L37>

- (CameraInfo class)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L42>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L42>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L48>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L48>

- (CreatureInfo class)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L53-L57>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L53-L57>

- (DoorInfo class)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L72>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L72>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L73-L74>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L73-L74>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L66>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L66>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L67>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L67>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L65>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L65>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L68>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L68>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L64>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorGIT/GIT.cs#L64>


---

<a id="generics_ifo_init_url_comments_pre_scrub"></a>

## Archived `IFO.__init__` URL comments

Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L15>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L15>

- (id: Uint8Array = new Uint8Array(16)) (id: Uint8Array = new Uint8Array(16)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L100>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L100>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L20>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L20>

- (localized module name)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L105>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L105>

- (areaName from Mod_Area_list[0].Area_Name)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L243>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L243>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L25>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L25>

- (entryArea = Mod_Entry_Area)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L270>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L270>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L29-L30>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L29-L30>

- (entryDirectionX/Y)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L271-L272>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L271-L272>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L26-L28>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L26-L28>

- (entryX/Y/Z)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L273-L275>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L273-L275>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L21>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L21>

- (tag: string)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L110>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L110>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L18>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L18>

- (voId: string)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L115>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L115>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L40-L54>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L40-L54>

- (scriptResRefs Map)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L59>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L59>

- (reference)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L16-L55>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorIFO/IFO.cs#L16-L55>

- (various deprecated fields)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/Module.ts#L160-L268>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/Module.ts#L160-L268>


---

<a id="generics_utc_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — resource/generics/utc.py

Verbatim lines removed from Libraries/PyKotor/src/pykotor/resource/generics/utc.py (Kotor.NET / KotOR.js UTC field anchors). Normative layout: wiki/GFF-UTC.md. See wiki/reverse_engineering_findings.md.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (UTC parser)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/AuroraParsers/UTCObject.cs>
  - Mirror (th3w1zard1/KotOR-dotNET): <https://github.com/th3w1zard1/KotOR-dotNET/blob/1f212b52b72787dda8dca2514f05b70d7bae560e/AuroraParsers/UTCObject.cs>

- (Creature module object)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleCreature.ts>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleCreature.ts>

- (UTC class definition)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTC/UTC.cs>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTC/UTC.cs>

- (ResRef property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L15>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L15>

- (inherited from ModuleObject)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L73>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L73>

- (Tag property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L18>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L18>

- (Comment property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L19>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L19>

- (comment field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L96>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L96>

- (Conversation property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L16>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L16>

- (FirstName property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L21>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L21>

- (LastName property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L22>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L22>

- (SubraceID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L25>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L25>

- (PerceptionID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L27>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L27>

- (RaceID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L24>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L24>

- (AppearanceID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L28>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L28>

- (GenderID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L29>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L29>

- (FactionID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L30>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L30>

- (WalkRateID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L31>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L31>

- (SoundsetID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L32>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L32>

- (PortraitID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L26>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L26>

- (BodyVariation property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L38>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L38>

- (bodyVariation field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L82>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L82>

- (TextureVariation property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L39>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L39>

- (NotReorientating property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L41>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L41>

- (PartyInteract property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L42>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L42>

- (NoPermanentDeath property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L43>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L43>

- (Min1HP property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L44>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L44>

- (Plot property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L45>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L45>

- (Interruptable property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L46>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L46>

- (IsPC property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L47>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L47>

- (Disarmable property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L48>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L48>

- (disarmable field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L100>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L100>

- (Alignment property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L52>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L52>

- (ChallengeRating property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L54>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L54>

- (challengeRating field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L94>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L94>

- (Blindspot property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L55>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L55>

- (MultiplierSet property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L56>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L56>

- (NaturalAC property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L58>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L58>

- (ReflexBonus property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L59>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L59>

- (refbonus field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L91>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L91>

- (WillBonus property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L60>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L60>

- (willbonus field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L92>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L92>

- (FortitudeBonus property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L61>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L61>

- (fortbonus field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L90>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L90>

- (Strength property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L79>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L79>

- (str field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L88>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L88>

- (Dexterity property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L80>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L80>

- (dex field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L86>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L86>

- (Constitution property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L81>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L81>

- (con field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L85>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L85>

- (Intelligence property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L82>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L82>

- (int field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L87>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L87>

- (Wisdom property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L83>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L83>

- (wis field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L89>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L89>

- (Charisma property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L84>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L84>

- (cha field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L84>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L84>

- (CurrentHP property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L64>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L64>

- (currentHitPoints field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L98>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L98>

- (MaxHP property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L65>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L65>

- (HP property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L63>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L63>

- (FP property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L67>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L67>

- (currentForce field)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleCreature.ts#L97>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleCreature.ts#L97>

- (MaxFP property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L68>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L68>

- (OnEndDialog property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L87>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L87>

- (OnBlocked property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L88>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L88>

- (OnHeartbeat property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L89>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L89>

- (OnNotice property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L90>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L90>

- (OnSpell property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L91>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L91>

- (OnAttack property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L92>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L92>

- (OnDamaged property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L93>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L93>

- (OnDisturbed property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L94>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L94>

- (OnEndRound property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L95>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L95>

- (OnDialog property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L96>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L96>

- (OnSpawn property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L97>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L97>

- (OnRested property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L98>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L98>

- (OnDeath property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L99>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L99>

- (OnUserDefined property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L100>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L100>

- (IgnoreCreaturePath property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L49>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L49>

- (Hologram property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L50>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L50>

- (PaletteID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L36>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L36>

- (bodyBag field)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L81>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L81>

- (deity field)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L99>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs#L99>

- (Classes property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs:101+>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTC.cs:101+>

- (ResRef property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTC/UTC.cs#L15>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTC/UTC.cs#L15>

- (FirstName property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTC/UTC.cs#L21>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTC/UTC.cs#L21>

- (skillList.Get(0).Get("Rank")) (skillList.Get(0)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTC/UTCCompiler.cs#L96>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTC/UTCCompiler.cs#L96>


---

<a id="generics_utd_class_docstring_pre_scrub"></a>

## Archived UTD class docstring

Verbatim ast.get_docstring from `Libraries/PyKotor/src/pykotor/resource/generics/utd.py` (git HEAD) before this scrub.

```
Stores door data.

UTD files are GFF-based format files that store door definitions including
lock/unlock mechanics, HP, scripts, and appearance.

References:
----------
    CSWSDoor::LoadDoor @ (K1: 0x0058a1f0, TSL: 0x006531e0 legacy PC / 0x00765620 Aspyr)
    Main UTD GFF parser; called from LoadDoorExternal (K1: 0x0058c5f0, TSL: 0x00765270) and LoadFromTemplate (K1: 0x0058b3d0, TSL: 0x007672c0). LoadDoors (K1: 0x0050a0e0, TSL: 0x0071b8a0) loads area doors.
    Defaults when field missing: Static 0, Conversation ""; other root fields use object state or 0/""/0.0. Omit OK.

    GFF Field Structure (from LoadDoor analysis):
        - Root struct fields:
            - "Appearance" (DWORD) - Door appearance type identifier
            - "GenericType" (BYTE) - Generic door type
            - "OpenState" (BYTE) - Initial open state (0=closed, 1=opened, 2=locked, 3=unlocked)
            - "AutoRemoveKey" (BYTE) - Whether key is auto-removed after use
            - "Bearing" (FLOAT) - Door bearing/rotation
            - "Faction" (DWORD) - Faction identifier
            - "Fort" (BYTE) - Fortitude save
            - "Will" (BYTE) - Will save
            - "Ref" (BYTE) - Reflex save
            - "HP" (SHORT) - Hit points
            - "CurrentHP" (SHORT) - Current hit points
            - "Invulnerable" (BYTE) - Whether door is invulnerable
            - "Plot" (BYTE) - Whether door is plot-critical
            - "Static" (BYTE) - Whether door is static
            - "Min1HP" (BYTE) - Whether door has minimum 1 HP
            - "KeyName" (CExoString) - Key name/ResRef
            - "KeyRequired" (BYTE) - Whether key is required
            - "OpenLockDC" (BYTE) - Open lock difficulty class
            - "CloseLockDC" (BYTE) - Close lock difficulty class
            - "SecretDoorDC" (BYTE) - Secret door detection difficulty class
            - "Tag" (CExoString) - Door tag identifier
            - "Conversation" (CResRef) - Conversation dialog ResRef
            - "PortraitId" (WORD) - Portrait ID (0xffff = use Portrait ResRef)
            - "Portrait" (CResRef) - Portrait resource reference (if PortraitId == 0xffff)
            - "Hardness" (BYTE) - Hardness value
            - "LocName" (CExoLocString) - Localized door name
            - "Description" (CExoLocString) - Door description
            - Script fields:
                - "OnClosed" (CResRef) - Script executed when door closes
                - "OnDamaged" (CResRef) - Script executed when door is damaged
                - "OnDeath" (CResRef) - Script executed when door is destroyed
                - "OnDisarm" (CResRef) - Script executed when trap is disarmed
                - "OnHeartbeat" (CResRef) - Script executed on heartbeat

    Note: UTD files are GFF format files with specific structure definitions (GFFContent.UTD)

Derivations and Other Implementations:
----------
    - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L11-L68
    - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L11-L68
(UTD class definition)
    - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/module/ModuleDoor.ts#L55-L167
    - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/module/ModuleDoor.ts#L55-L167
(Door module object)

Attributes:
----------
    resref: "TemplateResRef" field. The resource reference for this door template.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L59
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L59
(TemplateResRef property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L144
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L144
(templateResRef field)

    tag: "Tag" field. Tag identifier for this door.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L58
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L58
(Tag property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L143
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L143
(tag field)

    name: "LocName" field. Localized name of the door.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L33
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L33
(LocName property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L133
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L133
(locName field)

    auto_remove_key: "AutoRemoveKey" field. Whether key is removed after use.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L15
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L15
(AutoRemoveKey property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L120
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L120
(autoRemoveKey field)

    conversation: "Conversation" field. ResRef to dialog file for this door.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L18
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L18
(Conversation property)

    faction_id: "Faction" field. Faction identifier.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L22
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L22
(Faction property)

    plot: "Plot" field. Whether door is plot-critical.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L54
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L54
(Plot property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L139
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L139
(plot field)

    min1_hp: "Min1HP" field. Whether door HP cannot go below 1. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L34
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L34
(Min1HP property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L136
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L136
(min1HP field)

    key_required: "KeyRequired" field. Whether a key is required to unlock.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L29
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L29
(KeyRequired property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L131
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L131
(keyRequired field)

    lockable: "Lockable" field. Whether door can be locked.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L31
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L31
(Lockable property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L134
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L134
(lockable field)

    locked: "Locked" field. Whether door is currently locked.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L32
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L32
(Locked property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L135
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L135
(locked field)

    unlock_dc: "OpenLockDC" field. Difficulty class to unlock door.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L49
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L49
(OpenLockDC property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L137
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L137
(openLockDC field)

    key_name: "KeyName" field. Tag of the key item required.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L28
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L28
(KeyName property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L130
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L130
(keyName field)

    animation_state: "AnimationState" field. Current animation state. Always 0 in files.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L13
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L13
(AnimationState property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L118
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L118
(animationState field)
        Note: This field is always 0 in files (verified against engine binaries)

    maximum_hp: "HP" field. Maximum hit points.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L26
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L26
(HP property)

    current_hp: "CurrentHP" field. Current hit points.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L19
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L19
(CurrentHP property)

    hardness: "Hardness" field. Damage reduction value.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L25
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L25
(Hardness property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L128
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L128
(hardness field)

    fortitude: "Fort" field. Fortitude save value. Always 0 in files.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L23
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L23
(Fort property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L125
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L125
(fort field)

    appearance_id: "GenericType" field. Door appearance type identifier.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L24
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L24
(GenericType property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L126
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L126
(genericType field)

    static: "Static" field. Whether door is static (non-interactive).
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L57
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L57
(Static property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L142
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L142
(static field)

    on_closed: "OnClosed" field. Script to run when door closes. Always empty in files.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L36
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L36
(OnClosed property)
        Note: Verified against engine binaries

    on_damaged: "OnDamaged" field. Script to run when door is damaged. Always empty in files.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L37
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L37
(OnDamaged property)
        Note: Verified against engine binaries

    on_death: "OnDeath" field. Script to run when door is destroyed.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L38
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L38
(OnDeath property)

    on_heartbeat: "OnHeartbeat" field. Script to run on heartbeat.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L41
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L41
(OnHeartbeat property)

    on_lock: "OnLock" field. Script to run when door is locked. Always empty in files.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L42
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L42
(OnLock property)
        Note: Verified against engine binaries

    on_melee: "OnMeleeAttacked" field. Script to run when door is melee attacked. Always empty in files.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L43
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L43
(OnMeleeAttacked property)
        Note: Verified against engine binaries

    on_open: "OnOpen" field. Script to run when door opens.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L44
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L44
(OnOpen property)

    on_unlock: "OnUnlock" field. Script to run when door is unlocked. Always empty in files.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L47
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L47
(OnUnlock property)
        Note: Verified against engine binaries

    on_user_defined: "OnUserDefined" field. Script to run on user-defined event.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L48
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L48
(OnUserDefined property)

    on_click: "OnClick" field. Script to run when door is clicked.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L35
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L35
(OnClick property)

    on_open_failed: "OnFailToOpen" field. Script to run when door fails to open. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L40
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L40
(OnFailToOpen property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L390
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L390
(used in unlock failure handling)

    comment: "Comment" field. Developer comment. Used in toolset only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L17
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L17
(Comment property)
        Note: Verified against engine binaries

    unlock_diff: "OpenLockDiff" field. Unlock difficulty modifier. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L50
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L50
(OpenLockDiff property)
        Reference: NorthernLights/AuroraUTD.cs:65 (OpenLockDiff field)

    unlock_diff_mod: "OpenLockDiffMod" field. Additional unlock difficulty modifier. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L51
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L51
(OpenLockDiffMod property as sbyte)
        Reference: NorthernLights/AuroraUTD.cs:66 (OpenLockDiffMod field as Char)
        Note: Type discrepancy - reone uses char/int, Kotor.NET uses sbyte, PyKotor uses int

    open_state: "OpenState" field. Current open state (closed/open1/open2). KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L52
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L52
(OpenState property)
        Reference: NorthernLights/AuroraUTD.cs:67 (OpenState field)
        Reference: sotor/src/save/read.rs:488 (OpenState in save games)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L56
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L56
(openState field)

    not_blastable: "NotBlastable" field. Whether door cannot be blasted. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L67
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L67
(NotBlastable property)
        Reference: NorthernLights/AuroraUTD.cs:64 (NotBlastable field)

    palette_id: "PaletteID" field. Palette identifier. Used in toolset only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L53
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L53
(PaletteID property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L138
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L138
(paletteID field)
        Note: Verified against engine binaries

    description: "Description" field. Localized description. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L20
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L20
(Description property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L123
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L123
(description field)
        Note: Verified against engine binaries

    lock_dc: "CloseLockDC" field. Difficulty class to lock door. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L16
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L16
(CloseLockDC property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L121
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L121
(closeLockDC field)
        Note: Verified against engine binaries

    interruptable: "Interruptable" field. Whether door can be interrupted. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L27
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L27
(Interruptable property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L129
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L129
(interruptable field)
        Note: Verified against engine binaries

    portrait_id: "PortraitId" field. Portrait identifier. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L55
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L55
(PortraitId property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L140
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L140
(portraitId field)
        Note: Verified against engine binaries

    trap_detectable: "TrapDetectable" field. Whether trap is detectable. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L60
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L60
(TrapDetectable property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L146
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L146
(trapDetectable field)
        Note: Verified against engine binaries

    trap_detect_dc: "TrapDetectDC" field. Difficulty class to detect trap. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L61
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L61
(TrapDetectDC property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L145
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L145
(trapDetectDC field)
        Note: Verified against engine binaries

    trap_disarmable: "TrapDisarmable" field. Whether trap is disarmable. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L62
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L62
(TrapDisarmable property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L147
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L147
(trapDisarmable field)
        Note: Verified against engine binaries

    trap_disarm_dc: "DisarmDC" field. Difficulty class to disarm trap. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L21
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L21
(DisarmDC property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L124
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L124
(disarmDC field)
        Note: Verified against engine binaries

    trap_flag: "TrapFlag" field. Whether door has a trap. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L63
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L63
(TrapFlag property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L148
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L148
(trapFlag field)
        Note: Verified against engine binaries

    trap_one_shot: "TrapOneShot" field. Whether trap fires once. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L64
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L64
(TrapOneShot property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L149
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L149
(trapOneShot field)
        Note: Verified against engine binaries

    trap_type: "TrapType" field. Type of trap. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L65
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L65
(TrapType property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L150
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L150
(trapType field)
        Note: Verified against engine binaries

    unused_appearance: "Appearance" field. Appearance identifier. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L14
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L14
(Appearance property)
        Note: Verified against engine binaries

    reflex: "Ref" field. Reflex save value. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L56
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L56
(Ref property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L141
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L141
(ref field)
        Note: Verified against engine binaries

    willpower: "Will" field. Will save value. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L66
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L66
(Will property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L151
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L151
(will field)
        Note: Verified against engine binaries

    on_disarm: "OnDisarm" field. Script to run when trap is disarmed. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L39
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L39
(OnDisarm property)
        Note: Verified against engine binaries

    on_power: "OnSpellCastAt" field. Script to run when spell is cast at door. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L45
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L45
(OnSpellCastAt property)
        Note: Verified against engine binaries

    on_trap_triggered: "OnTrapTriggered" field. Script to run when trap triggers. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L46
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L46
(OnTrapTriggered property)
        Note: Verified against engine binaries

    loadscreen_id: "LoadScreenID" field. Load screen identifier. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L30
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTD/UTD.cs#L30
(LoadScreenID property)
        Reference:
        - Upstream (KobaltBlu/KotOR.js): https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/ModuleDoor.ts#L132
        - Mirror (th3w1zard1/KotOR.js): https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/ModuleDoor.ts#L132
(loadScreenID field)
        Note: Verified against engine binaries
```


---

<a id="generics_ute_class_docstrings_pre_scrub"></a>

## Archived UTE / UTECreature class docstrings

## `UTE`

```
Stores encounter data.

UTE files are GFF-based format files that store encounter definitions including
creature spawn lists, difficulty, respawn settings, and script hooks.

Root fields cover spawn limits, faction, reset/respawn flags, script hooks, and a
``CreatureList`` of template ResRefs with CR and spawn flags. It has been observed that
KotOR II adds ``GuaranteedCount`` per creature row; KotOR I does not use that field when
loading encounters. Loader symbols/addresses are migrated to
``wiki/reverse_engineering_findings.md``.

Note: UTE uses ``GFFContent.UTE``.

Attributes:
----------
    resref: "TemplateResRef" field. The resource reference for this encounter template.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L15
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L15
(TemplateResRef property)

    tag: "Tag" field. Tag identifier for this encounter.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L13
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L13
(Tag property)

    comment: "Comment" field. Developer comment.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L33
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L33
(Comment property)

    active: "Active" field. Whether encounter is active.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L16
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L16
(Active property)

    difficulty_id: "DifficultyIndex" field. Difficulty index identifier.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L18
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L18
(DifficultyIndex property)

    faction_id: "Faction" field. Faction identifier.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L19
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L19
(Faction property)

    max_creatures: "MaxCreatures" field. Maximum number of creatures to spawn.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L20
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L20
(MaxCreatures property)

    player_only: "PlayerOnly" field. Whether encounter only triggers for player.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L21
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L21
(PlayerOnly property)

    rec_creatures: "RecCreatures" field. Recommended number of creatures.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L22
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L22
(RecCreatures property)

    reset: "Reset" field. Whether encounter resets after completion.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L23
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L23
(Reset property)

    reset_time: "ResetTime" field. Time in seconds before reset.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L24
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L24
(ResetTime property)

    respawns: "Respawns" field. Number of times encounter can respawn.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L25
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L25
(Respawns property)

    single_shot: "SpawnOption" field. Whether encounter spawns only once.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L26
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L26
(SpawnOption property)

    on_entered: "OnEntered" field. Script to run when encounter area is entered.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L27
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L27
(OnEntered property)

    on_exit: "OnExit" field. Script to run when leaving encounter area.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L28
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L28
(OnExit property)

    on_exhausted: "OnExhausted" field. Script to run when encounter is exhausted.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L29
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L29
(OnExhausted property)

    on_heartbeat: "OnHeartbeat" field. Script to run on heartbeat.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L30
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L30
(OnHeartbeat property)

    on_user_defined: "OnUserDefined" field. Script to run on user-defined event.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L31
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L31
(OnUserDefined property)

    creatures: List of UTECreature objects representing spawnable creatures.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L34
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L34
(Creatures property)

    palette_id: "PaletteID" field. Palette identifier. Used in toolset only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L32
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L32
(PaletteID property)

    name: "LocalizedName" field. Localized name. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L14
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L14
(LocalizedName property)

    unused_difficulty: "Difficulty" field. Difficulty value. Not used by the game engine.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L17
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L17
(Difficulty property)
```

## `UTECreature`

```
Stores data for a creature that can be spawned by an encounter.

Each ``CreatureList`` row stores template ResRef, CR, ``SingleSpawn``, optional
``GuaranteedCount`` (TSL), and toolset ``Appearance`` (not used by KotOR I encounter load).
Binary-level notes are migrated to ``wiki/reverse_engineering_findings.md``.

Attributes:
----------
    appearance_id: "Appearance" field. Appearance type identifier for this creature.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L39
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L39
(Appearance property)

    challenge_rating: "CR" field. Challenge rating value.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L40
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L40
(CR property)

    resref: "ResRef" field. Resource reference to creature template (UTC file).
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L41
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L41
(ResRef property)

    single_spawn: "SingleSpawn" field. Whether this creature spawns only once.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L42
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L42
(SingleSpawn property)

    guaranteed_count: "GuaranteedCount" field. Guaranteed spawn count. KotOR 2 only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L43
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTE/UTE.cs#L43
(GuaranteedCount property)
```


---

<a id="generics_utp_class_docstring_pre_scrub"></a>

## Archived UTP class docstring

Verbatim ast.get_docstring from `Libraries/PyKotor/src/pykotor/resource/generics/utp.py` (git HEAD) before this scrub.

```
Stores placeable data.

UTP files are GFF-based format files that store placeable object definitions including
lock/unlock mechanics, HP, inventory, scripts, and appearance.

References:
----------
    Based on unified K1 (swkotor.exe) and TSL (swkotor2.exe) UTP implementation.
    Addresses: (K1: swkotor.exe, TSL: swkotor2.exe). TSL addresses: resolve in REVA when
    PyKotorGhidraProject.gpr is open (project may be locked by another process).

    - CSWSPlaceable::LoadPlaceable (main UTP GFF parser)
        K1: 0x00585670, TSL: 0x006a1680 (LoadPlaceableFromGFF, legacy PC)
        Loads all placeable fields from GFF structure.
        Signature: LoadPlaceable(CSWSPlaceable* this, CResGFF* param_1, CResStruct* param_2, int param_3).
        Called from LoadPlaceables and LoadFromTemplate.

    - CSWSPlaceable::SavePlaceable (UTP GFF writer)
        K1: 0x00586a70, TSL: TODO
        Writes all placeable fields to GFF structure.

    - LoadPlaceables / LoadFromTemplate (callers)
        K1: LoadPlaceables 0x0050a7b0, LoadFromTemplate 0x00587a70; TSL: TODO

    - GFF field label string references (K1; TSL at different addresses, TODO):
        K1: "Appearance" 0x00746efc, "HasInventory" 0x007496e0, "Lockable" 0x007496f8,
        "KeyName" 0x0074979c, "OpenLockDC" 0x007497a4, "CloseLockDC" 0x007496c8.

    GFF Field Structure (from LoadPlaceable analysis):
        - Root struct fields:
            - "Tag" (CExoString) - Placeable tag identifier
            - "TemplateResRef" (CResRef) - Template resource reference
            - "LocName" (CExoLocString) - Localized placeable name
            - "AutoRemoveKey" (BYTE) - Whether key is auto-removed after use
            - "Faction" (DWORD) - Faction identifier
            - "Invulnerable" (BYTE) - Whether placeable is invulnerable
            - "Plot" (BYTE) - Whether placeable is plot-critical
            - "Min1HP" (BYTE) - Whether placeable has minimum 1 HP
            - "PartyInteract" (BYTE) - Whether party can interact
            - "OpenLockDC" (BYTE) - Open lock difficulty class
            - "KeyName" (CExoString) - Key name/ResRef
            - "TrapDisarmable" (BYTE) - Whether trap is disarmable
            - "TrapDetectable" (BYTE) - Whether trap is detectable
            - "DisarmDC" (BYTE) - Disarm difficulty class
            - "TrapDetectDC" (BYTE) - Trap detection difficulty class
            - "TrapFlag" (BYTE) - Trap flag
            - "TrapOneShot" (BYTE) - Whether trap is one-shot
            - "TrapType" (BYTE) - Trap type identifier
            - "Useable" (BYTE) - Whether placeable is usable
            - "Static" (BYTE) - Whether placeable is static
            - "Appearance" (DWORD) - Appearance type identifier
            - "HP" (SHORT) - Hit points
            - "CurrentHP" (SHORT) - Current hit points
            - "Hardness" (BYTE) - Hardness value
            - "Fort" (BYTE) - Fortitude save
            - "Will" (BYTE) - Will save
            - "Ref" (BYTE) - Reflex save
            - "Lockable" (BYTE) - Whether placeable is lockable
            - "Locked" (BYTE) - Whether placeable is locked
            - "HasInventory" (BYTE) - Whether placeable has inventory
            - "KeyRequired" (BYTE) - Whether key is required
            - "CloseLockDC" (BYTE) - Close lock difficulty class
            - "PortraitId" (WORD) - Portrait ID (0xffff = use Portrait ResRef)
            - "Portrait" (CResRef) - Portrait resource reference (if PortraitId == 0xffff)
            - "Conversation" (CResRef) - Conversation dialog ResRef
            - "BodyBag" (BYTE) - Body bag type
            - "DieWhenEmpty" (BYTE) - Whether placeable dies when inventory empty
            - "GroundPile" (BYTE) - Ground pile flag
            - "LightState" (BYTE) - Light state (on/off)
            - "Description" (CExoLocString) - Placeable description
            - "ItemList" (GFFList) - List of inventory items (if HasInventory)

    Note: UTP files are GFF format files with specific structure definitions (GFFContent.UTP)

Derivations and Other Implementations:
----------
    - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L12-L75
    - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L12-L75
(UTP class definition)

Attributes:
----------
    resref: "TemplateResRef" field. The resource reference for this placeable template.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L64
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L64
(TemplateResRef property)

    tag: "Tag" field. Tag identifier for this placeable.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L63
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L63
(Tag property)

    name: "LocName" field. Localized name of the placeable.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L35
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L35
(LocName property)

    appearance_id: "Appearance" field. Placeable appearance type identifier.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L15
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L15
(Appearance property)

    has_inventory: "HasInventory" field. Whether placeable has an inventory.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L27
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L27
(HasInventory property)

    inventory: List of InventoryItem objects in this placeable's inventory.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L74
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L74
(Inventory property)

    not_blastable: "NotBlastable" field. Whether placeable cannot be blasted. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L37
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L37
(NotBlastable property)
        Reference: NorthernLights/AuroraUTP.cs:67 (NotBlastable field)

    unlock_diff: "OpenLockDiff" field. Unlock difficulty modifier. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L55
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L55
(OpenLockDiff property)
        Reference: NorthernLights/AuroraUTP.cs:68 (OpenLockDiff field)

    unlock_diff_mod: "OpenLockDiffMod" field. Additional unlock difficulty modifier. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L56
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L56
(OpenLockDiffMod property as sbyte)
        Reference: NorthernLights/AuroraUTP.cs:69 (OpenLockDiffMod field as Char)
        Note: Type discrepancy - reone uses char/int, Kotor.NET uses sbyte, PyKotor uses int

    on_open_failed: "OnFailToOpen" field. Script to run when placeable fails to open. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L43
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L43
(OnFailToOpen property)

    lock_dc: "CloseLockDC" field. Difficulty class to lock placeable. KotOR 2 Only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L18
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L18
(CloseLockDC property)

    palette_id: "PaletteID" field. Palette identifier. Used in toolset only.
        Reference:
        - Upstream (NickHugi/Kotor.NET): https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L57
        - Mirror (th3w1zard1/Kotor.NET): https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTP/UTP.cs#L57
(PaletteID property)

    Note: UTP shares many fields with UTD (door). See UTD documentation for common fields
    like auto_remove_key, conversation, faction_id, plot, min1_hp, key_required, lockable,
    locked, unlock_dc, key_name, animation_state, maximum_hp, current_hp, hardness,
    fortitude, on_closed, on_damaged, on_death, on_heartbeat, on_lock, on_melee_attack,
    on_open, on_force_power, on_unlock, on_user_defined, static, useable, party_interact,
    on_end_dialog, on_inventory, on_used, comment, description, interruptable, portrait_id,
    trap_detectable, trap_detect_dc, trap_disarmable, trap_disarm_dc, trap_flag,
    trap_one_shot, trap_type, will, on_disarm, on_trap_triggered, bodybag_id, type_id.
```


---

<a id="resource_generics_dlg_links_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — `resource/generics/dlg/links.py`

Verbatim lines removed from `Libraries/PyKotor/src/pykotor/resource/generics/dlg/links.py`. See `wiki/reverse_engineering_findings.md`.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (DLG link structure)
  - Upstream (KobaltBlu/KotOR.js): <https://github.com/KobaltBlu/KotOR.js/blob/ea9491d5c783364cf285f178434b84405bee3608/src/resource/DLGLink.ts>
  - Mirror (th3w1zard1/KotOR.js): <https://github.com/th3w1zard1/KotOR.js/blob/0067b672a124bbbdaf4006dd0a5d6c2751523195/src/resource/DLGLink.ts>

- (DLG link structure)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorDLG/DLG.cs>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorDLG/DLG.cs>


---

<a id="resource_generics_utm_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — `resource/generics/utm.py`

Verbatim lines removed from `Libraries/PyKotor/src/pykotor/resource/generics/utm.py`. See `wiki/reverse_engineering_findings.md`.

Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (UTM structure)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTM/UTM.cs>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTM/UTM.cs>

- (UTM parsing)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTM/UTMDecompiler.cs>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/Kotor.NET/Resources/KotorUTM/UTMDecompiler.cs>

- (GFF format implementation)
  - Upstream (Fair-Strides/KotOR-Bioware-Libs): <https://github.com/Fair-Strides/KotOR-Bioware-Libs/blob/90ade1cace418f8e1130c53938d22e8acaa8bc41/GFF.pm>
  - Mirror (th3w1zard1/KotOR-Bioware-Libs): <https://github.com/th3w1zard1/KotOR-Bioware-Libs/blob/90ade1cace418f8e1130c53938d22e8acaa8bc41/GFF.pm>


---

<a id="resource_generics_uts_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — `resource/generics/uts.py`

Verbatim lines removed from `Libraries/PyKotor/src/pykotor/resource/generics/uts.py`. See `wiki/reverse_engineering_findings.md`.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (TemplateResRef property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L15>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L15>

- (Tag property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L13>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L13>

- (Active property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L16>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L16>

- (Continuous property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L17>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L17>

- (Looping property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L18>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L18>

- (Positional property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L19>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L19>

- (RandomPosition property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L20>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L20>

- (Random property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L21>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L21>

- (Elevation property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L22>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L22>

- (MaxDistance property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L23>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L23>

- (MinDistance property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L24>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L24>

- (RandomRangeX property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L25>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L25>

- (RandomRangeY property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L26>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L26>

- (Interval property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L27>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L27>

- (IntervalVrtn property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L28>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L28>

- (PitchVariation property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L29>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L29>

- (Priority property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L30>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L30>

- (Volume property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L33>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L33>

- (VolumeVrtn property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L34>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L34>

- (Sounds property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L35>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L35>

- (Comment property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L37>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L37>

- (PaletteID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L36>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L36>

- (LocName property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L14>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L14>

- (Hours property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L31>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L31>

- (Times property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L32>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTS.cs#L32>


---

<a id="resource_generics_utw_github_urls_pre_scrub"></a>

## Archived GitHub URL lines — `resource/generics/utw.py`

Verbatim lines removed from `Libraries/PyKotor/src/pykotor/resource/generics/utw.py`. See `wiki/reverse_engineering_findings.md`.



Canonical upstream and **th3w1zard1** mirror/fork permalinks (`blob` / `tree` + commit) follow [Home](Home) cross-references. Resolved via GitHub API (`master` / `main` tip) on 2026-03-25.

When upstream and mirror SHAs differ, line anchors may not match both trees.

- (TemplateResRef property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L15>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L15>

- (Tag property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L16>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L16>

- (LocalizedName property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L17>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L17>

- (HasMapNote property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L19>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L19>

- (MapNote property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L20>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L20>

- (MapNoteEnabled property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L21>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L21>

- (Appearance property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L13>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L13>

- (PaletteID property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L22>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L22>

- (Comment property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L23>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L23>

- (LinkedTo property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L14>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L14>

- (Description property)
  - Upstream (NickHugi/Kotor.NET): <https://github.com/NickHugi/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L18>
  - Mirror (th3w1zard1/Kotor.NET): <https://github.com/th3w1zard1/Kotor.NET/blob/6dca4a6a1af2fee6e36befb9a6f127c8ba04d3e2/UTW.cs#L18>


---
