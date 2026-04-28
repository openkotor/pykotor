---
title: KOTOR/TSL Save/Load 1:1 Python from Binary RE
problem_type: logic-errors
component: extract/savedata, MCP (user-agdec-http), reverse engineering
symptoms: |
  No 1:1 Python implementation of K1/TSL save/load; engine order and steps were not
  documented; decompiler unavailable in AgentDecompile MCP so only disassembly was
  available for key functions.
root_cause: |
  PyKotor save/load logic did not follow the exact order of operations used by the
  K1 and TSL binaries. The engine uses a fixed sequence (e.g. disk check -> create
  dir -> screenshot -> SAVENFO/PARTYTABLE/GLOBALVARS/SAVEGAME.sav on save; on load:
  LoadTableInfo -> Load -> LoadModule). Deviating from that order can affect
  compatibility. The fix was to implement dedicated flows that mirror the engine
  step-by-step using reverse-engineering as the source of truth.
solution: |
  Implemented save_load_flow_k1.py and save_load_flow_tsl.py with engine-identical
  sequence; SAVE_LOAD_ENGINE_BEHAVIOR.md as single source of truth; RE reports for
  K1 and TSL; tests in test_save_load_flow_k1.py. K1 disk threshold from
  HasEnoughDiskSpaceForSaveGame: K1_MIN_FREE_BYTES_ENGINE = 26_214_400 (~25 MiB).
prevention: |
  Update SAVE_LOAD_ENGINE_BEHAVIOR.md and flow modules when changing save/load
  behavior; run test_save_load_flow_k1.py; use flow functions as single source of
  engine order; prefer SaveFolderEntry to delegate to flow when 1:1 required.
related_docs: |
  docs/reva_roadmap/SAVE_LOAD_ENGINE_BEHAVIOR.md, KOTOR_SAVE_LOAD_RE_REPORT.md,
  KOTOR_SAVE_LOAD_TSL_RE_REPORT.md, KOTOR_SAVE_LOAD_RE_AGENT_NATIVE_AUDIT.md,
  AGENTS.md, .cursor/plans/kotor_save_load_re_via_agdec_mcp_b9f4946a.plan.md
category: logic-errors
---

# KOTOR/TSL Save/Load 1:1 Python from Binary RE

Reverse-engineered K1 and TSL save/load from game binaries (`k1_win_gog_swkotor.exe`, `k2_win_gog_aspyr_swkotor2.exe`) via the user-agdec-http (AgentDecompile) MCP and implemented engine-identical Python flows in `save_load_flow_k1.py` and `save_load_flow_tsl.py` with matching sequence, disk check, paths, screenshot, and component order.

---

## Root cause

PyKotor's save/load logic did not follow the exact order of operations used by the K1 and TSL binaries. The engine uses a fixed sequence (e.g. disk check -> create dir -> screenshot -> SAVENFO/PARTYTABLE/GLOBALVARS/SAVEGAME.sav on save; on load: LoadTableInfo -> Load -> LoadModule). Deviating from that order can affect compatibility and behavior. The fix was to implement dedicated flows that mirror the engine step-by-step, using reverse-engineering as the source of truth.

---

## Solution

### Single source of truth

- **`docs/reva_roadmap/SAVE_LOAD_ENGINE_BEHAVIOR.md`** — Defines K1 save path (SaveGame), load path (LoadGame), DoSaveGameScreenShot, and TSL load (FUN_007b2f00) / save (StallEventSaveGame) with exact step order.
- **RE details:** `docs/reva_roadmap/KOTOR_SAVE_LOAD_RE_REPORT.md` (K1), `docs/reva_roadmap/KOTOR_SAVE_LOAD_TSL_RE_REPORT.md` (TSL offsets 0x1f0b4, 0x100fc, 0x1f254, etc.).

### K1 flow module — `Libraries/PyKotor/src/pykotor/extract/save_load_flow_k1.py`

- **Helpers:** `get_free_disk_space_k1(path)`, `get_directory_size_k1(path)` (GetDirectorySize @ 005e6650), `clean_directory_k1(path)` (CleanDirectory retry path), `create_directory_k1(path)`.
- **Constant:** `K1_MIN_FREE_BYTES_ENGINE = 26_214_400` (~25 MiB), from HasEnoughDiskSpaceForSaveGame @ 004b2520: `(free >> 14) >= 0x640`.
- **Save:** `run_k1_save_flow(entry, *, min_free_bytes=..., required_save_bytes=..., required_max_directory_bytes=..., skip_screenshot_if_path_equal=..., retry_create_after_clean=..., write_components=...)` — (1) free disk + optional [EDI+0x100c8] check, (2) create directory with optional clean+retry on failure, (3) GetDirectorySize vs required_max_directory_bytes, (4–7) path/network/alias (screenshot skip when path matches 0x73d71c), (8–9) write screenshot unless skipped, (10–12) write components in engine order; return 1/0.
- **Load:** `run_k1_load_flow(entry)` — (6) `partytable.load()` (LoadTableInfo @ this+0x1b770), (7) `save_info.load()`, `globals.load()` (Load @ this+0x100fc), (10) `sav.load()` (LoadModule); then read screenshot; return entry.

### TSL flow module — `Libraries/PyKotor/src/pykotor/extract/save_load_flow_tsl.py`

- **Helpers:** `get_free_disk_space_tsl(path)`, `create_directory_tsl(path)`.
- **Save:** `run_tsl_save_flow(entry, ...)` — Same logical order as K1: disk check, create dir, screenshot write, then `save_info.save()`, `partytable.save()`, `globals.save()`, `sav.save()`; return 1/0.
- **Load:** `run_tsl_load_flow(entry)` — `partytable.load()` (LoadTableInfo @ 0x1f0b4), then `save_info.load()`, `globals.load()` (Load @ 0x100fc), then `sav.load()` (LoadModule); then screenshot read; return entry.

### Tests — `Libraries/PyKotor/tests/extract/test_save_load_flow_k1.py`

- Disk space and directory helpers for K1 and TSL; `get_directory_size_k1` (empty/sums), `clean_directory_k1` (empties dir).
- Minimal save flow: return 1 and screenshot file content; skip-screenshot when `skip_screenshot_if_path_equal` matches; return 0 when `required_save_bytes` exceeds free or `required_max_directory_bytes` <= dir size.

### Integration

- `SaveFolderEntry.save()` / `load()` can delegate to `run_k1_save_flow` / `run_k1_load_flow` or `run_tsl_save_flow` / `run_tsl_load_flow` when engine-identical behavior is required.

---

## How to verify

From repo root:

```bash
uv run pytest Libraries/PyKotor/tests/extract/test_save_load_flow_k1.py -v --timeout=30
```

Expect: All tests in `test_save_load_flow_k1.py` pass (disk helpers, directory helpers, `run_k1_save_flow` and `run_tsl_save_flow` return 1 and write screenshot with minimal fixture). No game install or K1_PATH/K2_PATH required.

---

## Related documentation

- **AGENTS.md** — Reverse engineering (agdec-http MCP): Ghidra/binary workflow, tool usage, wiki policy.
- **docs/reva_roadmap/KOTOR_SAVE_LOAD_RE_REPORT.md** — K1 save/load RE report (function list, addresses, disassembly) via user-agdec-http.
- **docs/reva_roadmap/KOTOR_SAVE_LOAD_TSL_RE_REPORT.md** — TSL save/load RE report for `k2_win_gog_aspyr_swkotor2.exe`.
- **docs/reva_roadmap/KOTOR_SAVE_LOAD_RE_AGENT_NATIVE_AUDIT.md** — Agent-native audit of save/load RE plan and workflow.
- **docs/reva_roadmap/SAVE_LOAD_ENGINE_BEHAVIOR.md** — K1/TSL save/load engine behavior spec (1:1).
- **.cursor/plans/kotor_save_load_re_via_agdec_mcp_b9f4946a.plan.md** — Phased save/load RE plan (phases 1–11).
- **.cursor/skills/assembly-transpile-parity/SKILL.md** — Skill for decompile/transpile parity using subagents (disassembly -> Python/C with comparison).
- **wiki/reverse_engineering_findings.md** — RE findings; engine architecture, agdec-http usage.

---

## Prevention and testing

### Best practices

- When changing save/load behavior: update `docs/reva_roadmap/SAVE_LOAD_ENGINE_BEHAVIOR.md` and the corresponding flow module (`save_load_flow_k1.py` or `save_load_flow_tsl.py`); run `Libraries/PyKotor/tests/extract/test_save_load_flow_k1.py`.

### Avoiding drift

- Treat the **flow functions** as the single source of engine order; avoid duplicating or reordering steps in `SaveFolderEntry` or elsewhere.
- When 1:1 with the engine is required, have **SaveFolderEntry** call `run_k1_save_flow` / `run_k1_load_flow` (or TSL equivalents) instead of reimplementing the sequence.

### Test cases

- **Existing:** Disk space, directory creation, minimal save flow (screenshot write) for K1 and TSL.
- **Suggested:** Golden SAV roundtrip test (save then load, compare critical fields) when a fixture SAV folder is available.

### When to use flow modules vs SaveFolderEntry.save() / load()

- Use **flow modules** when you need engine-identical order and steps (e.g. tooling that must match the binary, RE validation, or 1:1 tests).
- Use **SaveFolderEntry.save()** / **load()** when you only need to read or write save data and strict engine ordering is not required.
- Prefer having `SaveFolderEntry` delegate to the flow functions when the caller needs 1:1 behavior.
