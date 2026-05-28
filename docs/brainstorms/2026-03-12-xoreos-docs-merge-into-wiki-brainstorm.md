---
date: 2026-03-12
topic: xoreos-docs-merge-into-wiki
---

# Merge Odyssey/KotOR/Jade Empire Content from vendor/xoreos-docs into Wiki

## What We're Building

Bring all **Odyssey / KotOR / Jade Empire**–relevant information from the local `vendor/xoreos-docs` submodule into the repo `wiki/` so that:

- The wiki is the single, comprehensive source for KotOR/Odyssey/Jade format and engine documentation.
- Content is findable and maintainable in one place (wiki Markdown); optional continued use of xoreos-docs for PDFs and binary templates only.
- Help system and readers do not depend on having the xoreos-docs submodule for core KotOR/Odyssey/Jade content.

**Current state (from repo research):**

- **vendor/xoreos-docs** contains: `specs/bioware/*.pdf` (official Aurora), `specs/torlack/*.html` (mod, bif, key, ncs, plt, itp, binmdl, basics), `specs/kotor_mdl.html`, `templates/JadeMDL.bt` (Jade Empire MDL), and other specs (trn, nds, foxpro) that are not KotOR/Odyssey/Jade.
- **Wiki today:** Already cites and links to xoreos-docs (original + mirror). Bioware PDF content is **extracted** into `Bioware-Aurora-*.md`. Torlack basics are linked from Home; NCS, KEY, ERF, MDL, etc. reference Torlack and kotor_mdl. MDL-MDX-File-Format explicitly merges kotor_mdl.html and torlack/binmdl.html into its narrative. So the wiki is partly integrated and partly link-only.
- **Help:** `help_paths.py` and `generate_help_contents.py` use both `wiki/` and `vendor/xoreos-docs` as bases; xoreos-docs is included as a second tree (“Xoreos Documentation”), not inlined into wiki.

**Scope for “Odyssey/KotOR/Jade Empire”:**

- **KotOR/Odyssey:** Torlack specs that apply to KotOR (mod, bif, key, ncs, plt, itp, binmdl, basics), `kotor_mdl.html`, and Bioware PDFs (already in wiki as Bioware-Aurora-*).
- **Jade Empire:** `templates/JadeMDL.bt` (010 Editor binary template); no prose doc in xoreos-docs. Optional: one short wiki page describing Jade Empire MDL and pointing to the template.

---

## Approaches Considered

### Approach A: Gap-fill (recommended)

**Description:** Audit xoreos-docs for Odyssey/KotOR/Jade material that is **missing or only linked** in the wiki. Add that content into existing format pages or new wiki pages (e.g. Torlack tables/sections not yet merged, KotOR-specific notes from basics.html, any Torlack spec that has no wiki equivalent). Keep xoreos-docs as submodule for PDFs and binary templates; links to GitHub xoreos-docs remain for attribution.

**Pros:** Minimal duplication; builds on existing “cite + integrate where needed” pattern; avoids large HTML->Markdown conversions; YAGNI-friendly.

**Cons:** Some readers may still open xoreos-docs HTML for raw specs; requires a one-time audit to find gaps.

**Best when:** You want the wiki to be complete and authoritative without committing to full conversion or moving files.

---

### Approach B: Full content conversion

**Description:** Convert **all** relevant Torlack HTML (mod, bif, key, ncs, plt, itp, binmdl, basics) and any other KotOR/Odyssey/Jade prose into wiki Markdown. Wiki holds the full text; format pages either absorb the content or link to new wiki pages (e.g. `wiki/specs/torlack/Key-File-Format-Torlack.md`). xoreos-docs remains for Bioware PDFs and binary templates (e.g. JadeMDL.bt) and as upstream source.

**Pros:** Wiki is the single source of truth for prose; no dependency on reading HTML in vendor; good for search and long-term maintenance.

**Cons:** Significant one-time conversion and ongoing sync if xoreos-docs upstream changes; possible duplication with existing format pages unless we carefully merge.

**Best when:** You want to stop depending on vendor HTML for reading and search, and are willing to own the converted content.

---

### Approach C: Structural merge (copy files under wiki)

**Description:** Copy (or move) the relevant xoreos-docs **files** into a path under `wiki/` (e.g. `wiki/xoreos-docs/` or `wiki/vendor/xoreos-docs/`), preserving HTML (and .bt). Help and links then point to the wiki tree; the submodule is no longer required for those files. Optionally add a minimal index page in the wiki that links to these files.

**Pros:** Single tree for help; no HTML->Markdown conversion; files stay in their original format.

**Cons:** Wiki would contain non-Markdown (HTML, .bt); less consistent with the rest of the wiki; duplicate of upstream if submodule is kept.

**Best when:** You want one directory tree for “all docs” without changing file formats.

---

## Why Recommend Approach A (Gap-fill)

- The wiki **already** integrates the most critical content (Bioware PDFs, kotor_mdl + binmdl in MDL page, and many Torlack references). The main risk is **gaps**, not “nothing is there.”
- Gap-fill is the smallest change that achieves “all Odyssey/KotOR/Jade information is in the wiki”: add what’s missing, and optionally one Jade Empire MDL page + link to JadeMDL.bt.
- Full conversion (B) or structural merge (C) can be done later if we discover that gap-fill is insufficient (e.g. users need full Torlack text in wiki, or a single tree is required).

---

## Key Decisions (to confirm with your choice)

- **Merge strategy:** Choose A (gap-fill), B (full content conversion), or C (structural merge). Recommendation: **A**.
- **Jade Empire:** Either (1) add a short wiki page “Jade Empire MDL” that describes the format and links to xoreos-docs `templates/JadeMDL.bt`, or (2) only link to the template from an existing MDL or “External Documentation” section. No prose exists in xoreos-docs for Jade beyond the .bt file.
- **Attribution:** Whatever we merge or convert, keep clear attribution to xoreos-docs and Torlack (Tim Smith) in the wiki (already the pattern in Home and format pages).
- **Submodule:** After merge, keep `vendor/xoreos-docs` as submodule for Bioware PDFs and binary templates unless we explicitly choose to copy those under wiki (not recommended for PDFs).

---

## Open Questions

1. **Which approach do you want?** (A = gap-fill, B = full content conversion, C = structural merge, or a variant.)
2. **Jade Empire:** Do you want a dedicated short wiki page for Jade Empire MDL (with link to JadeMDL.bt), or is a link from Home / External Documentation enough?
3. **Torlack “basics”:**
   - `specs/torlack/basics.html` is NWN-centric (chitin.key, dialog.tlk, nwn.ini) but aligns with KotOR (chitin.key, dialog.tlk, kotor.ini). Should we add a “KotOR/Odyssey data file basics” section to the wiki (e.g. under KEY-File-Format or Home) that adapts this content, or keep only the current link to xoreos-docs?

---

## Next Steps

- Once you answer the open questions (reply with approach + Jade + basics preference), this document can be updated with **Resolved Questions** and the chosen approach.
- Then run **`/workflows:plan`** to produce an implementation plan (audit checklist for A, conversion/mapping tasks for B, or copy/link tasks for C).
