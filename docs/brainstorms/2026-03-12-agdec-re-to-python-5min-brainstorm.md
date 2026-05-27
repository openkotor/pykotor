---
date: 2026-03-12
topic: agdec-re-to-python-5min
---

# AgentDecompile RE -> Python in ~5 Minutes (Skills/Agents/Tooling)

## What We're Building

Tooling (skills, agents, subagents, or scripts) that make "decompile/disassemble all functions called during save/load -> write exact Python equivalent" **fast and repeatable** — target **~5 minutes** instead of 8+ hours. The user flow: run something; get engine-identical Python (e.g. `save_load_flow_k1.py` / `save_load_flow_tsl.py`) and passing tests without manual RE and manual translation.

Scope: save/load only for now (K1/TSL). Pattern could later extend to other subsystems (e.g. resource resolution, BIF/KEY).

## Why This Hurts Today (8+ Hours)

- **No bulk get-function:** Each function = one MCP call (60–90s timeout); call tree built by recursing manually.
- **No get-call-graph:** Call graph assembled from repeated `get-function` responses.
- **Decompiler often unavailable:** Disassembly-only -> manual translation to Python.
- **No single pipeline:** Discovery -> report -> implementation -> verification are separate steps; not scriptable end-to-end.

## Key Decisions

- **Cache-first:** Do full RE (discover + disassemble save/load functions) **once** and persist results (e.g. JSON per function: disassembly, callers, callees, signature). "5 minutes" = load cache -> generate Python -> run tests. Full RE only when binary or function set changes.
- **Fixed function list for save/load:** Use a known list of addresses (from existing RE reports / plan) for K1 and TSL so we don't rediscover every time; optional "refresh list" step when adding new binaries or areas.
- **Single pipeline artifact:** One script or MCP-adjacent tool that: (1) optionally builds/refreshes cache from agdec-http, (2) reads cache, (3) generates Python from cache (template or constrained LLM using assembly-transpile-parity), (4) runs flow tests. So "RE -> Python" is one command after cache exists.
- **Skills/agents role:** A **skill** documents the workflow (when to use cache, when to refresh, how to run the pipeline). **Subagents** can run the parity/comparison step (assembly-transpile-parity already does this). No need for a net-new "agent" type; improve **discovery + batch** so the main agent (or a script) can do "get all -> emit" in few steps.

## Approaches Considered

### Approach A: RE cache + codegen script (recommended)

**What:** Repo script (e.g. `Tools/RE/agdec_save_load_cache.py` or under `helper_scripts/`) that: (1) takes a list of function addresses (from plan/RE report), (2) calls agdec-http `get-function` for each (or a new batch API if added), (3) writes a cache (JSON/directory per function). Second script or mode: read cache -> emit Python using a deterministic template or one LLM pass with assembly-transpile-parity -> run `pytest test_save_load_flow_k1.py`. First run = build cache (slow, one-time). Later runs = generate + test (~5 min).

**Pros:** Clear separation (cache vs codegen); no MCP server changes required if we accept sequential get-function for cache build; works with current agdec-http.  
**Cons:** Cache build still sequential until agdec has batch get-function; template may not cover every branch (can fall back to LLM + parity skill).

**Best when:** You want the fastest path to "one command -> Python + tests" without changing the MCP server.

### Approach B: Skill + subagent only (no cache)

**What:** A skill that instructs the agent to: (1) list save/load addresses from a pinned list in the skill or in AGENTS.md, (2) call get-function for each in parallel (multiple subagents or batched MCP calls), (3) assemble behavior doc, (4) run assembly-transpile-parity (subagent A -> Python, subagent B -> alternate, compare), (5) write code and run tests. No persistent cache; every "5 min" run re-fetches.

**Pros:** No new scripts; uses existing assembly-transpile-parity; parallel get-function could reduce wall time.  
**Cons:** Still limited by MCP round-trips and timeouts; "5 min" only if parallelization and small scope; no offline/cache for when Ghidra/agdec unavailable.

**Best when:** You prefer not to add repo scripts and are okay with repeated MCP calls each time.

### Approach C: Extend agdec-http with batch-get + repo pipeline

**What:** Add a tool to the AgentDecompile MCP server (e.g. `batch-get-functions` taking a list of addresses, returning disassembly/callers/callees in one or few responses). Repo script: (1) call batch-get for save/load list, (2) write cache, (3) codegen from cache, (4) run tests. Cache build becomes one or few round-trips -> true ~5 min even for "full" RE from scratch if batch is fast.

**Pros:** Minimal per-function latency; single pipeline from "binary + address list" to "Python + tests"; scales to larger function sets.  
**Cons:** Requires changing the MCP server (out-of-repo); dependency on that server's maintainers.

**Best when:** You control or can contribute to the agdec-http server and want the most scalable solution.

## Why Approach A (Cache + Codegen Script)

- **YAGNI:** We don't need to change the MCP server to get most of the gain; cache + script gets "5 min" for the common case (regenerate from known list).
- **Fits repo:** We already have a save/load function list and RE reports; the script consumes that list and the plan's outputs.
- **Upgrade path:** If agdec-http later adds batch-get, the script can switch to it and cache build becomes fast too.

## Open Questions

- **"5 minutes" scope:** Is it (a) full RE from scratch in 5 min, (b) regenerate from cache + test in 5 min, or (c) first run builds cache once, then every later run ~5 min? (Current design assumes (c).)
- **Where the cache lives:** Repo (e.g. `docs/reva_roadmap/agdec_cache/`) vs local-only (e.g. `.cursor/` or user dir) to avoid large checked-in JSON.
- **Codegen method:** Purely template-based from disassembly (deterministic but brittle) vs one LLM pass with assembly-transpile-parity (flexible, needs review) vs hybrid (template for structure, LLM for complex blocks).

## Next Steps

-> Resolve open questions (especially 5-min scope and cache location).  
-> Run `/workflows:plan` to implement the chosen approach (e.g. cache script + codegen + skill update).
