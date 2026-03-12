---
status: pending
priority: p2
issue_id: "001"
tags: [save-load, reverse-engineering, agdec-http, 1-1-parity, extract]
dependencies: []
---

# Exhaustive 1:1 Save/Load Python from agdec-http (Zero Omissions)

## Problem Statement

Deliver 1:1 exhaustive and complete Python code that matches K1 and TSL save/load behavior with **zero discrepancies** from what AgentDecompile (user-agdec-http) can provide. Current flow modules (`save_load_flow_k1.py`, `save_load_flow_tsl.py`) implement the high-level sequence and K1 disk threshold; gaps remain: (1) no byte-level or golden-SAV verification; (2) SaveGame uses GetDirectorySize comparison (path + existing dir size) not only free space; (3) error-path behavior (CreateDirectory2 failure → CleanDirectory retry, then SendServerToPlayerSaveLoad_Status failure) not mirrored; (4) TSL StallEventSaveGame full disassembly not yet mapped to Python; (5) LoadGame/LoadModule callees (LoadTableInfo 00565d20, Load 0052ade0) internal order and struct layout not exhaustively documented.

## Findings

- **Location:** `Libraries/PyKotor/src/pykotor/extract/save_load_flow_k1.py`, `save_load_flow_tsl.py`, `docs/reva_roadmap/SAVE_LOAD_ENGINE_BEHAVIOR.md`, `KOTOR_SAVE_LOAD_RE_REPORT.md`, `KOTOR_SAVE_LOAD_TSL_RE_REPORT.md`
- **Source:** Agent-Native Audit (`KOTOR_SAVE_LOAD_RE_AGENT_NATIVE_AUDIT.md`), user requirement "1:1 exhaustive and complete python code... zero omissions, placeholders, or simplifications"
- **Gaps:** No implementation phase for byte-exact verification; decompiler fallback yields disassembly only; TSL first-class phases added but StallEventSaveGame not fully translated; GetDirectorySize vs GetFreeDiskSpace logic in K1 SaveGame not fully mirrored

## Proposed Solutions

### Option 1: Full disassembly-to-Python with verification
- **Pros:** Achieves zero discrepancies; verifiable via golden SAV or byte-diff
- **Cons:** Requires golden SAV fixtures or engine run; effort large
- **Effort:** Large (> 8 hours)
- **Risk:** Medium (fixture availability, decompiler still unavailable)

### Option 2: Exhaustive step parity + documented assumptions
- **Pros:** Every branch and call order from get-function reflected in Python and SAVE_LOAD_ENGINE_BEHAVIOR.md; assumptions and no-ops explicitly listed
- **Cons:** Byte-exact verification deferred
- **Effort:** Medium (2–8 hours)
- **Risk:** Low

## Recommended Action

To be filled during triage.

## Technical Details

- **Affected Files:** `save_load_flow_k1.py`, `save_load_flow_tsl.py`, `SAVE_LOAD_ENGINE_BEHAVIOR.md`, RE reports, `savedata.py` (optional delegation)
- **Related Components:** extract/savedata, MCP user-agdec-http, docs/reva_roadmap
- **Database Changes:** No

## Resources

- Original finding: Agent-Native Audit (KOTOR_SAVE_LOAD_RE_AGENT_NATIVE_AUDIT.md), user request for exhaustive 1:1
- Related: KOTOR_SAVE_LOAD_RE_REPORT.md, KOTOR_SAVE_LOAD_TSL_RE_REPORT.md, docs/solutions/logic-errors/kotor-save-load-1-1-python-from-re.md

## Acceptance Criteria

- [ ] Every SaveGame/LoadGame step from get-function disassembly reflected in Python or explicitly no-op with comment
- [ ] K1 disk check: document or implement GetDirectorySize comparison if required for 1:1
- [ ] TSL StallEventSaveGame: full step list in SAVE_LOAD_ENGINE_BEHAVIOR.md and TSL flow module
- [ ] Tests pass (existing flow tests + any new verification)
- [ ] No placeholders or simplifications without a comment referencing binary behavior

## Work Log

(Empty – pending triage.)

## Notes

Source: Triage setup; pending todo created from audit and user request for exhaustive 1:1.
