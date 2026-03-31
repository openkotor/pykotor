# TSLPatcher Data Syntax

TSLPatcher's data-oriented sections are now documented on dedicated pages so each syntax family can be maintained independently. Use this page as the stable entry point for links that refer to `[2DAList]` and `[TLKList]` syntax.

## Contents

- [2DAList Syntax](#2dalist-syntax)
- [TLKList Syntax](#tlklist-syntax)

## When to use this page

Use this hub when you need to decide whether a change belongs in `[2DAList]` or `[TLKList]`, or when an older wiki link brought you here. For exact directives, examples, processing notes, and token usage, follow the dedicated guides below.

<a id="2dalist-syntax"></a>

## 2DAList Syntax

Use `[2DAList]` when a mod needs to merge changes into a [2DA](2DA-File-Format) table instead of replacing the whole file. The standalone guide covers row targeting, `ChangeRow`, `AddRow`, `CopyRow`, `AddColumn`, `2DAMEMORY` tokens, processing order, and troubleshooting.

Canonical page:

- [TSLPatcher 2DAList Syntax](TSLPatcher-2DAList-Syntax)

Typical uses:

- appending rows to `appearance.2da`, `spells.2da`, or similar tables
- storing row indices in `2DAMEMORY#` for later [GFF](GFF-File-Format), [SSF](Audio-and-Localization-Formats#ssf), or [NCS](NCS-File-Format) patches
- merging per-mod table edits without shipping whole-file overrides

<a id="tlklist-syntax"></a>

## TLKList Syntax

Use `[TLKList]` when a mod needs to append or patch [TLK](Audio-and-Localization-Formats#tlk) string entries. The standalone guide covers `StrRef#` creation, replacement behavior, processing order, and how those string references flow into later sections such as `[2DAList]`, `[GFFList]`, and `[SSFList]`.

Canonical page:

- [TSLPatcher TLKList Syntax](TSLPatcher-TLKList-Syntax)

Typical uses:

- adding new dialogue or item text to `dialog.tlk`
- creating `StrRef#` tokens for later use in [2DA](2DA-File-Format) and [GFF](GFF-File-Format) edits
- updating localized text without replacing the entire talk table

## Related sections

- [TSLPatcher GFFList Syntax](TSLPatcher-GFFList-Syntax)
- [TSLPatcher SSFList Syntax](TSLPatcher-SSFList-Syntax)
- [TSLPatcher InstallList Syntax](TSLPatcher-InstallList-Syntax)
- [TSLPatcher HACKList Syntax](TSLPatcher-HACKList-Syntax)
- [HoloPatcher README for Mod Developers](HoloPatcher-README-for-mod-developers)
- [TSLPatcher's Official Readme](TSLPatcher's-Official-Readme)
