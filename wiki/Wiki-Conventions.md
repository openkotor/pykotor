# Wiki conventions

This page documents style and structure conventions for the PyKotor wiki. Follow these when adding or editing pages. These conventions apply to all edits—whether made by a human or by an AI agent—so that the wiki stays consistent and both can use it effectively.

## Wiki contents and entry points

- **Entry points:** [Home](Home) lists formats and tools and is the main index; [Concepts](Concepts) defines resource resolution, ResRef, override folder, and core format concepts. Use these to discover what the wiki contains and to navigate to format, tool, or how-to pages.
- **Page types:** The wiki contains format reference pages (one format per page), how-to/guide pages (steps and prerequisites), and tool-syntax or tool-readme pages. Match new pages to the appropriate template (Reference or How-to / guide).

## Naming

- Use a consistent pattern for similar content: `Format-Name` (e.g. `GFF-ARE`, `2DA-File-Format`), `Tool-Feature` (e.g. `TSLPatcher-InstallList-Syntax`).
- Avoid mixing names for the same concept (e.g. use "GFF-ARE" consistently, not "ARE File" in one place and "GFF-ARE" in another).

## Headings

- **One H1 per page:** The page title is the only H1 (`#`). Use H2 (`##`) for main sections and H3 (`###`) for subsections.
- **No skipped levels:** Do not jump from H2 to H4; keep a strict hierarchy.
- **Sentence case:** Use sentence case for headings (e.g. "Key file purpose", not "Key File Purpose"). Capitalize the first word, proper nouns, and the first word after a colon.
- **Anchor stability:** Heading anchors are usually derived from the heading text. Avoid changing headings that are linked from elsewhere; if you rename one, update in-page and cross-page links that use the old anchor, or the links will break.

## Links

- **Internal links:** Use extension-less links: `[Label](Page-Name)` or `[Label](Page-Name#section)`. Do not include `.md` in the target (e.g. use `](KEY-File-Format)`, not `](KEY-File-Format.md)`).
- **External links:** Use HTTPS when possible. For GitHub repos that have a mirror at th3w1zard1, use the format: **original repo link first**, then `([Mirror: th3w1zard1/reponame](https://github.com/th3w1zard1/reponame))`. Apply this in all **Vendor References**, **Vendor Implementations**, and tool lists (see [Home](Home) lines 383–407 and [NSS-File-Format](NSS-File-Format), [KEY-File-Format](KEY-File-Format), [NCS-File-Format](NCS-File-Format) for examples). If the project is original under th3w1zard1 (no upstream), link once without a mirror parenthetical. Validate external permalinks (e.g. GitHub line links) before adding; broken links reduce trust and tooling reliability.
- **Link text:** Use the page or section title or a short descriptive phrase, not "click here" or "this document".

## See also

- Put a **See also** section at the **end** of the page only, using the heading `### See also` (sentence case). Do not duplicate "See also" at the top of the page; keep a single block before the final closing line or after the last main section. If a page currently has See also near the top, move it to the end (cut/paste) to keep navigation consistent and avoid breaking in-page anchors.
- Include 3–8 links to closely related pages: sibling formats, parent concept, or tools that use the format.

## Content

- **Goal:** This wiki aims to be **complete, comprehensive, accurate, specific, and accessible** for any use--modders, developers, and researchers. Prefer linking to canonical pages (KEY-File-Format, GFF-File-Format, official BioWare specs) and to PyKotor/vendor code; cite community sources (DeadlyStream, LucasForums archives) where they add consensus or history.
- **One page per format or tool:** Keep each page focused on one format, one tool feature, or one task.
- **Link to official specs:** For formats with an official BioWare (or other) specification, link to it and document only extensions, quirks, or tool-specific behavior.
- **Single source of truth (SSOT):** Do not duplicate long specs or repeated concepts. Link to the canonical page instead:
  - **Concepts (single overview):** [Concepts](Concepts) -- definitions for resource resolution order, ResRef, override folder, BIF/KEY, MOD/ERF, GFF, 2DA.
  - **Resource resolution order:** [KEY-File-Format](KEY-File-Format#key-file-purpose) (and [Home](Home) Odyssey Engine Basics).
  - **ResRef:** [GFF-File-Format](GFF-File-Format#gff-data-types) (GFF data types).
  - **Override folder:** [Concepts](Concepts#override-folder) or [resource resolution order](KEY-File-Format#key-file-purpose).
- **Section order (long format pages):** Use a consistent order: Overview → Structure / fields → Examples (optional) → See also. Add a short on-page table of contents at the top where it helps navigation.
- **Format reference pages:** Include a clear **Structure / fields** (or equivalent) section. Where the format has a fixed or deterministic layout, state total length, offset base (e.g. "offsets from file start"), or byte ranges so that parsers and validators can use the page reliably.
- **Implementation and references:** On format and tool pages, add **Implementation** (PyKotor paths) and **Reference** (vendor, specs) sections where missing. Use PyKotor link form: `[path](https://github.com/OldRepublicDevs/PyKotor/blob/master/path#Lx-Ly)`. For vendor links: original repo first, then `(Mirror: th3w1zard1/repo)(url)` when a mirror exists; if the project is th3w1zard1-original with no upstream, one link only.
- **Cross-links:** Formats loaded by ResRef should link to [KEY-File-Format](KEY-File-Format) for resource resolution and to [GFF-File-Format](GFF-File-Format#gff-data-types) for ResRef where relevant.
- **Community and historical context:** When adding or refining format or tool pages, link to [Community sources and archives](Home#community-sources-and-archives) (DeadlyStream, LucasForums Container, Mixmojo) where relevant for consensus, tutorials, or historical discussion.

## Verification

- After changing internal links to extension-less form, confirm in the wiki UI that links resolve correctly. If the wiki renderer requires `.md`, document that here and do not remove extensions.
- **Link targets:** Internal link targets (e.g. `Page-Name` in `](Page-Name)`) must match the exact wiki page name (case and hyphenation). Agents and scripts can verify by resolving links against existing page filenames (e.g. `*.md` in the wiki directory) or by running a link checker.

---

## Checklist for new or edited pages

- [ ] One H1 only; headings in sentence case; no skipped levels.
- [ ] Internal links extension-less; external links HTTPS; mirror format for GitHub where applicable.
- [ ] Single "See also" at end with 3–8 links.
- [ ] No duplicated long specs; link to canonical page (Concepts, KEY-File-Format, GFF-File-Format) instead.
- [ ] Format pages: use Reference template; include Structure/fields and, when relevant, length or offset base.

Use this checklist for both human and agent-generated edits.

## Templates

Use these section outlines when creating new pages so structure stays consistent.

### Reference (file format)

```markdown
# [Format name] file format

Brief overview (what the format is, where it is used).

## Structure / fields

(File layout, data types, tables.)

## Examples

(Optional: short examples or code snippets.)

### See also

- [Related format or tool](Page-Name)
- [Parent concept](Other-Page)
```

### How-to / guide

```markdown
# [Task or feature name]

Goal: one sentence describing what the reader will achieve.

## Prerequisites

(Optional: tools, prior reading.)

## Steps

1. First step.
2. Second step.

### See also

- [Related guide](Page-Name)
```

### See also

- [Home](Home) -- Wiki overview and format index
- [Concepts](Concepts) -- Resource resolution, ResRef, override, BIF/KEY, MOD/ERF, GFF, 2DA
- [KEY-File-Format](KEY-File-Format), [GFF-File-Format](GFF-File-Format), [2DA-File-Format](2DA-File-Format) -- Canonical format pages
- [TSLPatcher's-Official-Readme](TSLPatcher's-Official-Readme), [HoloPatcher-README-for-mod-developers](HoloPatcher-README-for-mod-developers) -- Tool docs
