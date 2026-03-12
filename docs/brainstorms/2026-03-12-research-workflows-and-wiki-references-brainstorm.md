---
date: 2026-03-12
topic: research-workflows-and-wiki-references
---

# Research Workflows and Wiki References

## What We're Building

A clear way to (1) keep wiki vendor permalinks valid, (2) add and maintain code references across the wiki using GitHub and repo research, and (3) integrate best-practices-researcher, repo-research-analyst, parallel-deep-research, and parallel-web-search into the PyKotor workflow so they are used at the right time and their outputs land in the right place.

## Why This Approach

- **Vendor permalinks:** Wiki links to external repos (reone, xoreos, Kotor.NET, KotOR.js, etc.) must point at existing paths and the correct default branch. Using GitHub MCP (e.g. `get_repository_tree`, `list_branches`) avoids rate limits from bulk web fetches and gives a single source of truth.
- **References in wiki:** GitHub code search (e.g. `search_code` on `repo:OldRepublicDevs/PyKotor`) surfaces format readers, GFF usage, and toolset usage; that can drive consistent "References" and "See also" sections across format and tool docs.
- **Research workflows:** Subagent and parallel-cli outputs are most useful when triggers, output locations, and citation style are defined once and reused (plans, wiki, AGENTS.md).

## Key Decisions

### 1. Vendor permalink validation

- **Use GitHub MCP, not bulk web fetch:** Direct fetch of GitHub blob URLs often hits 429. Prefer **user-github-code-research-read** MCP:
  - `list_branches` (owner, repo) → confirm default branch (`master` vs `main`).
  - `get_repository_tree` (owner, repo, path_filter, recursive) → confirm paths exist (e.g. `src/libs/resource/format` for reone).
- **Validated so far:** `th3w1zard1/reone` and `th3w1zard1/xoreos-docs` use **master**; paths under `src/libs/resource/format` exist in reone. Wiki links using `blob/master/` for these repos are correct.
- **Wiki convention:** Use `blob/master/` for th3w1zard1/* repos unless a repo’s default branch is known to be `main`. For OldRepublicDevs/PyKotor, confirm default branch and use that in permalinks (or use commit SHA for stability).
- **Optional follow-up:** A script or CI step could, for each vendor URL pattern in the wiki, call MCP to verify path and branch and report broken links (no automated rewrite).

### 2. References and code research (GitHub MCP)

- **search_code** on `repo:OldRepublicDevs/PyKotor` with format-related terms (GFF, 2DA, TLK, etc.) returns many candidate paths (e.g. `Libraries/PyKotor/src/pykotor/tslpatcher/mods/gff.py`, `resource/formats/`, `extract/twoda.py`, `Tools/HolocronToolset/...`). Use this to:
  - Add **References** sections to format docs that currently lack them (e.g. GFF-*, SSF, LIP, ERF, BIF, NCS).
  - Add **Implementation** or **PyKotor** subsection with a single primary path when the page describes one main implementation.
  - Keep **Vendor References** (reone, xoreos, KotOR.js, Kotor.NET, KotOR-Unity) as today; validate paths with `get_repository_tree` when adding new ones.
- **Pattern for wiki:** `[path or description](https://github.com/OldRepublicDevs/PyKotor/blob/<branch>/path#Lx-Ly)` for PyKotor; same for vendor repos with `blob/master/` where validated. End each format page with **See also** (3–8 internal wiki links, extension-less).

### 3. Best-practices-researcher (Cursor subagent)

- **When:** Before defining "how we should do X" (docs structure, format doc template, API style, conventions). Once per topic to get a target direction.
- **Inputs:** Topic (e.g. "GFF format documentation structure", "Diátaxis for file-format reference pages"); optional scope (wiki-only vs code+wiki) and constraints.
- **Output:** Bullets (must-have vs recommended), linked sources, optional short checklist for wiki (e.g. "One H1 per page", "See also at end").
- **Where it goes:** Plan "Target direction" or "Best practices" section; wiki conventions (e.g. Wiki-Conventions.md); References in format docs. Do not paste long narrative into wiki—summarize and link.

### 4. Repo-research-analyst (Cursor subagent)

- **When:** Start of a plan or brainstorm that touches repo structure, wiki, or code conventions; or when an exact file/list/line audit is needed to make a plan implementable.
- **Inputs:** Codebase-focused ask (e.g. "list wiki files and See Also usage", "where are GFF readers used", "what conventions does AGENTS.md enforce"); scope (e.g. `wiki/`, `Libraries/PyKotor/`).
- **Output:** Existing patterns, file lists, line ranges, conventions. May reference AGENTS.md, .cursorrules, code.
- **Where it goes:** Plan "Current state" or "Implementation data"; wiki **References** and **See also** (internal links only at end); code pointers (path + line range). Do not cite the analyst or tool names in the wiki (per AGENTS.md).

### 5. Parallel deep research (parallel-cli research)

- **When:** Only when the user explicitly asks for "deep research", "exhaustive", "comprehensive report", or "thorough investigation". For normal lookups use parallel-web-search.
- **Where results go:** Dated files, e.g. `docs/brainstorms/YYYY-MM-DD-topic-slug.md` (and `.json` from `-o`). Not in `wiki/` unless polished and user-facing.
- **In wiki:** One-line summary + link to the report; no large paste. Optional "Further reading" or "Background" with 1–2 sentence summary + link.

### 6. Parallel web search (parallel-cli search)

- **When:** Default for lookups, fact-checking, "research X" when the user does not ask for "deep" or "exhaustive".
- **Citing in wiki:** Inline `[Source Title](URL)` for every factual claim; mandatory **Sources** section at end listing every URL used. Use only URLs from the search output.
- **Output:** `-o slug.json`; mention path in response for follow-up. Optional: turn search into a dated doc in `docs/brainstorms/` and link from wiki.

### 7. Integration order for plan-first work

1. **Repo-research-analyst** → "Current state" / "Implementation data".
2. **Best-practices-researcher** → "Target direction" / standards.
3. Plan steps → implementation.
4. Wiki updated with References / See also / code pointers as needed; deep or web research cited per above.

## Open Questions

- **Automation:** Add a script or CI job that uses GitHub MCP to validate vendor permalinks (list branches + get tree for each linked repo/path) and report 404s or branch renames?

## Resolved Questions

- Use GitHub MCP for permalink validation instead of bulk mcp_web_fetch (avoids 429, single source of truth).
- reone and xoreos-docs use `master`; wiki links with `blob/master/` for these are valid.
- **PyKotor default branch:** OldRepublicDevs/PyKotor uses `master`; wiki permalinks using `blob/master/` are correct.
- **th3w1zard1/kotor:** Repo exists; default branch `master`; `docs/2da.md` present. Wiki links to `vendor/kotor/docs/2da.md` (e.g. in 2DA-File-Format.md) are valid.
- Deep research only on explicit user request; web search is default for research/lookups.
- Wiki stays conceptual; no tool names or raw RE dumps (AGENTS.md). Analyst output used in plans and for References, not cited by name in wiki.

## Summary Table

| Goal | Use | Output goes to |
|------|-----|----------------|
| "How should we do X?" (standards, structure) | best-practices-researcher | Plan "Target direction"; wiki conventions/References |
| "What do we have?" (files, patterns) | repo-research-analyst | Plan "Current state"; wiki References/See also |
| Quick lookup, citation, current info | parallel-web-search | Wiki "See also" + Sources; AGENTS.md; plan in-line citations |
| Exhaustive report on a topic | parallel-deep-research | `docs/brainstorms/` or `docs/research/`; optional short summary + link in plan/wiki |
| Validate vendor links | GitHub MCP (list_branches, get_repository_tree) | No automated rewrite; report broken links |
| Add References to wiki | GitHub MCP search_code + get_repository_tree | References / Implementation / Vendor subsections; See also at end |

---

*Brainstorm merged from repo-research-analyst and best-practices-researcher subagent outputs; vendor permalink and References strategy from GitHub MCP checks and wiki grep.*
