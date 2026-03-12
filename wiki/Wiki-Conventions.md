# Wiki conventions

This page documents style and structure conventions for the PyKotor wiki. Follow these when adding or editing pages.

## Naming

- Use a consistent pattern for similar content: `Format-Name` (e.g. `GFF-ARE`, `2DA-File-Format`), `Tool-Feature` (e.g. `TSLPatcher-InstallList-Syntax`).
- Avoid mixing names for the same concept (e.g. use "GFF-ARE" consistently, not "ARE File" in one place and "GFF-ARE" in another).

## Headings

- **One H1 per page:** The page title is the only H1 (`#`). Use H2 (`##`) for main sections and H3 (`###`) for subsections.
- **No skipped levels:** Do not jump from H2 to H4; keep a strict hierarchy.
- **Sentence case:** Use sentence case for headings (e.g. "Key file purpose", not "Key File Purpose"). Capitalize the first word, proper nouns, and the first word after a colon.

## Links

- **Internal links:** Use extension-less links: `[Label](Page-Name)` or `[Label](Page-Name#section)`. Do not include `.md` in the target (e.g. use `](KEY-File-Format)`, not `](KEY-File-Format.md)`).
- **External links:** Use HTTPS when possible. For GitHub repos that have a mirror at th3w1zard1, use the format: primary repo link first, then `([Mirror: th3w1zard1/reponame](https://github.com/th3w1zard1/reponame))`. See [Home](Home) for examples.
- **Link text:** Use the page or section title or a short descriptive phrase, not "click here" or "this document".

## See also

- Put a **See also** section at the **end** of the page, using the heading `### See also` (sentence case).
- Include 3–8 links to closely related pages: sibling formats, parent concept, or tools that use the format.

## Content

- **One page per format or tool:** Keep each page focused on one format, one tool feature, or one task.
- **Link to official specs:** For formats with an official BioWare (or other) specification, link to it and document only extensions, quirks, or tool-specific behavior.
- **Avoid duplication:** Do not copy long specs or repeated concepts (e.g. resource resolution order, ResRef, override folder). Link to the canonical page instead:
  - **Resource resolution order:** [KEY-File-Format](KEY-File-Format#key-file-purpose) (and [Home](Home) Odyssey Engine Basics).
  - **ResRef:** [GFF-File-Format](GFF-File-Format#gff-data-types) (GFF data types).
  - **Override folder:** The game loads resources from the `override/` directory first; see [resource resolution order](KEY-File-Format#key-file-purpose).

## Verification

- After changing internal links to extension-less form, confirm in the wiki UI that links resolve correctly. If the wiki renderer requires `.md`, document that here and do not remove extensions.

---

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
