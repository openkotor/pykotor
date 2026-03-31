# Wiki overhaul goals

This page defines the live completion goals for the PyKotor wiki overhaul. It exists in the wiki because the overhaul only counts when the goals are visible in the documentation tree itself and implemented in the pages readers actually use.

Use this page as the maintenance target when refining or reviewing the wiki.

## Target state

- **Links are accurate:** Internal wiki links resolve without `.md` suffixes, anchors remain stable, and reader-facing pages avoid stale or weakly explained external links.
- **Entry points are clear:** [Home](Home), [Concepts](Concepts), [Resource formats and resolution](Resource-Formats-and-Resolution), and [Reverse Engineering Findings](reverse_engineering_findings) act as distinct front doors instead of overlapping summaries.
- **Canonical pages own the explanation:** One page stays exhaustive for each major concept or format family. Companion pages summarize, scope, or route instead of duplicating.
- **Preserved sources stay preserved:** `Bioware-Aurora-*` pages and [TSLPatcher's Official Readme](TSLPatcher's-Official-Readme) remain source artifacts. New interpretation belongs on modern companion pages.
- **Archive material stays gated:** Contributor archives and migrated reverse-engineering notes remain available for provenance, but they do not become the default first-stop route for ordinary readers.
- **Claims are evidence-backed:** Behavior, binary layout, and workflow claims are stated with the level of confidence the evidence supports. Unknown or partly verified claims are labeled accordingly.
- **The live wiki is the source of truth:** Overhaul intent, routing, and implementation live in `wiki/`, not in detached planning artifacts elsewhere in the repository.

## Completion criteria

The overhaul is considered complete only when all of the following are true:

1. The main wiki hubs route readers cleanly by task and by depth.
2. Canonical format and concepts pages are the shortest path to the information most readers need.
3. Archive, migrated-note, and preserved-source pages are clearly marked as secondary or contributor-facing where appropriate.
4. Internal link validation passes for the live wiki after edits.
5. Further cleanup work can be described as ordinary maintenance rather than structural overhaul.

## Active priorities

1. Keep hub pages focused on routing, not duplicate explanation.
2. Tighten canonical pages that still drift into contributor-only detail or awkward scaffolding language.
3. Keep reverse-engineering archive pages clearly subordinate to [Reverse Engineering Findings](reverse_engineering_findings).
4. Resolve or isolate remaining TODO-marked reverse-engineering notes so readers can tell what is verified and what still needs dual-game confirmation.

## Working rules

- Put new routing, scope, or overhaul status notes in the live wiki rather than `docs/plans/`.
- When a page mixes reader-facing explanation with contributor appendices, keep the reader-facing explanation first and move provenance-heavy material lower.
- When two pages overlap, prefer reducing the summary page rather than expanding it.
- When evidence is incomplete, say so explicitly instead of smoothing it into a definitive claim.

### See also

- [Home](Home)
- [Concepts](Concepts)
- [Resource formats and resolution](Resource-Formats-and-Resolution)
- [Reverse Engineering Findings](reverse_engineering_findings)
- [Wiki Conventions](Wiki-Conventions)