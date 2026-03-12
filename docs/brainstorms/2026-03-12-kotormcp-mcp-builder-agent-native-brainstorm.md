---
date: 2026-03-12
topic: kotormcp-mcp-builder-agent-native
---

# KotorMCP: MCP builder, security audit, and agent-native alignment

## What we're building

Align KotorMCP and the PyKotor CLI with:

1. **MCP builder quality** — Tool naming, `inputSchema`/`outputSchema`, annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`), "Use when" and parameter descriptions, truncation contract (`truncated: true`, `continuation_hint`), consistent error messages.
2. **MCP security audit** — When KotorMCP is added to a workspace (e.g. `.cursor/mcp.json`): stdio-only, no 0.0.0.0 binding; path_safety for extract/write; governance note (no shadow MCPs, approval for server installation); destructive tools clearly marked and allowlisted.
3. **Agent-native architecture** — Action parity (every Toolset action agent-achievable), context injection (resolution order + tool index available to agents), capability discovery ("when to use which tool"), shared workspace (agent and user same installation paths).

**Current state (post recent implementation):**

- **Done:** Phase 2.8 refs (kotor_list_references, kotor_find_referrers, kotor_find_strref_referrers, kotor_describe_dlg, kotor_describe_jrl, kotor_describe_resource_refs), kotor_installation_info, get_installation_summary(), path_safety.py (get + extract), reference_config in PyKotor + Toolset re-export, references.py (extract_references, find_referrers), Installation.locations() using canonical_search_order().
- **Pending (from audits + plan):** Optional `source`/`location_filter` on get and kotor_extract_resource; MCP resource `kotor://docs/resolution-order` (and optionally capabilities); `truncated: true` + `continuation_hint` in JSON when hitting 25K; "Use when" and input descriptions on all tools; MCP annotations on every tool; DLG root scripts (EndConversation, EndConverAbort, VO_ResRef) in reference extraction; CLI discoverability (grouping, examples, did-you-mean); write/convert/script tools (kotor_convert_resource, kotor_compile_script, kotor_decompile_script, kotor_write_override, kotor_create_archive) wired and path-safe.

## Why this approach

- Audits (agent-native review, consolidated audit, CLI redesign, redesign agent-native review) already enumerated gaps and priorities. This brainstorm captures **scope and order** so the next plan or implementation pass is unambiguous.
- MCP builder skill requires annotations and outputSchema on every tool; current KotorMCP has none. Security audit requires governance and path_safety before advertising the server. Agent-native requires onboarding (resolution order + tool index) so agents can discover capabilities.
- Single document ties together "what to build next" across three lenses (builder, security, agent-native) without duplicating the full plan.

## Key decisions

- **Parity first, then polish.** Close remaining parity gaps (source/location_filter, onboarding doc resource, truncation metadata) before a full MCP builder pass (annotations on all 20+ tools, outputSchema everywhere). Rationale: agents need "extract from this location" and "how do I use this server" before they need strict schema annotations.
- **Onboarding:** Prefer one MCP resource (`kotor://docs/resolution-order` or `kotor://docs/capabilities`) that returns one-page text: resolution order, tool index with one-line "Use when" per tool, and "when to use which tool." Optional: document a required system-prompt snippet for host implementers so both MCP resource and prompt can coexist.
- **Security:** Path_safety is implemented for get and extract. When adding KotorMCP to `.cursor/mcp.json`, document: use stdio (local command); do not bind 0.0.0.0; destructive tools (extract, write_override, create_archive) are allowlisted via path_safety. Add a short governance note (e.g. in AGENTS.md or KotorMCP README): "MCP server installation requires approval; no shadow/unmanaged MCPs."
- **DLG root + VO:** Include EndConversation, EndConverAbort, VO_ResRef (and Sound) in reference_config and extract_references so "follow connections from a DLG" is complete (per redesign agent-native review Critical #2).

## Resolved questions

1. **Annotations scope:** Add `readOnlyHint`/`destructiveHint`/`idempotentHint`/`openWorldHint` to **all** tools in the polish phase (after parity items). Do not limit to write tools—one consistent pass so every tool is annotated.
2. **"When to use" location:** **Both.** Implement onboarding resource first (kotor://docs/capabilities or resolution-order) so agents have one place to read; then add one line "Use when …" to every tool's `description` so `list_tools` is also self-explanatory.

## Resolved / recommendation

- **Order of work:** (1) source/location_filter + docs resource + truncation metadata + actionable extract error; (2) DLG root/VO in reference_config + references.py; (3) "Use when" in every tool description; (4) MCP annotations (readOnlyHint/destructiveHint) on every tool; (5) outputSchema where high value (e.g. list_resources, find_resource, installation_info); (6) CLI discoverability and write/convert/script wiring as separate tasks.
- **Governance:** One short subsection in AGENTS.md or KotorMCP README: how to add KotorMCP (stdio, path_safety), and that MCP server installation should be approved (no shadow MCPs).

## Next steps

- Implementation plan (or continue with existing plan checkboxes) for: source-param, docs-resource, truncation-meta, reference_config DLG root, tool descriptions, then annotations on all tools.
