# TSLPatcher GFF Syntax

TSLPatcher's structure-oriented sections are now documented on dedicated pages. Use this page as the stable entry point for links that refer to `[GFFList]` and `[SSFList]` syntax.

## Contents

- [GFFList Syntax](#gfflist-syntax)
- [SSFList Syntax](#ssflist-syntax)

## When to use this page

Use this hub when you need to decide whether a patch belongs in `[GFFList]` or `[SSFList]`, or when an older internal link brought you here. For exact keys, field-path syntax, memory-token behavior, and examples, follow the dedicated guides below.

<a id="gfflist-syntax"></a>

## GFFList Syntax

Use `[GFFList]` when a mod needs to change fields inside a [GFF](GFF-File-Format) resource without replacing the entire file. The standalone guide covers field paths, `AddField#`, localized string syntax, vectors, nested structures, `2DAMEMORY` and `StrRef` tokens, destination handling, and common pitfalls.

Canonical page:

- [TSLPatcher GFFList Syntax](TSLPatcher-GFFList-Syntax)

Typical uses:

- editing `.uti`, `.utc`, `.dlg`, `.utp`, `.utt`, `.utw`, `.ifo`, `.git`, or `.jrl` fields
- writing `StrRef#` and `2DAMEMORY#` values into nested structures
- adding fields while preserving compatibility with other mods

<a id="ssflist-syntax"></a>

## SSFList Syntax

Use `[SSFList]` when a mod needs to patch [SSF](Audio-and-Localization-Formats#ssf) sound-set mappings without replacing the whole file. The standalone guide covers slot naming, `StrRef` usage, destination handling, and how SSF changes fit into the overall patch routine.

Canonical page:

- [TSLPatcher SSFList Syntax](TSLPatcher-SSFList-Syntax)

Typical uses:

- changing sound-set string references for creature and player voice events
- applying localized sound-set updates through [TLK](Audio-and-Localization-Formats#tlk) tokens
- modifying SSF assets while keeping the rest of the file intact

## Related sections

- [TSLPatcher 2DAList Syntax](TSLPatcher-2DAList-Syntax)
- [TSLPatcher TLKList Syntax](TSLPatcher-TLKList-Syntax)
- [TSLPatcher InstallList Syntax](TSLPatcher-InstallList-Syntax)
- [TSLPatcher HACKList Syntax](TSLPatcher-HACKList-Syntax)
- [HoloPatcher README for Mod Developers](HoloPatcher-README-for-mod-developers)
- [TSLPatcher's Official Readme](TSLPatcher's-Official-Readme)
