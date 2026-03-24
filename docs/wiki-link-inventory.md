# Wiki Link Inventory (triaged)

Generated as part of the wiki accuracy program. Re-run:

`uv run python helper_scripts/wiki_scripts/validate_markdown_links.py`

## Summary

| Class                         | Description                                                                 |
| ----------------------------- | --------------------------------------------------------------------------- |
| **Internal / same-file**      | `validate_markdown_links.py` matches `test_markdown_validation.py`: markdown headings **and** explicit `<a id="…">` anchors (used heavily in `2DA-File-Format.md` for TOC targets). |
| **Fixed in baseline pass**    | HoloPatcher filename (`..md` → `.md`) + inbound links; NSS module/area SSOT + redirect stub; Home UTC + VFX slug encoding; BWM cross-links retargeted to current heading slugs; RIM → ERF subsection; KEY `### File Header`; ERF HAK + RIM sections; NSS→NCS engine-call anchor; Blender/MDL/UTC editor links; `reverse_engineering_findings` tone; Wiki-Conventions false positives. |
| **External**                  | Not covered by `validate_markdown_links.py`; use `check-broken-links` workflow + manual spot checks. |

## CI

`check-broken-links.yml` checks out **`submodules: recursive`**, runs **`python helper_scripts/wiki_scripts/validate_markdown_links.py`** (fails the job on broken internal wiki links), then optional external link-checker steps (**`continue-on-error: true`** on those follow-on steps).

## Next mechanical batch

1. Keep `2DA-File-Format.md` TOC anchors in sync: add or adjust `<a id="…">` rows when new table sections are added, or add real `##` headings whose slugs match the TOC.
2. Optionally tighten external link steps (remove `continue-on-error` / `|| true`) once noise is acceptable.
