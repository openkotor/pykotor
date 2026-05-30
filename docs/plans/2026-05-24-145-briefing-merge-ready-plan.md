---
title: "fix: top-level briefing merge ready json"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level briefing_merge_ready JSON (plan 145)

## Summary

Defer briefing always sets **`merge_ready: false`**, but top-level gate JSON omits it unless agents drill into **`lfg_agent_briefing`**. This completes defer-briefing field mirroring alongside **`briefing_action`**, **`briefing_reason`**, and **`briefing_notes`**.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors **`merge_ready`** to top-level **`briefing_merge_ready`** when present in briefing.
- R2. **`preflight_watch_summary`** JSON includes **`briefing_merge_ready`** on deferred watch end.
- R3. **`_emit_lfg_strict_exit_stderr`** appends **`merge_ready=false`** when briefing sets **`merge_ready`** false.
- R4. Watch summary one-liner includes **`merge_ready=false`** when present.
- R5. Tests; **`PLAN_TRACK_CAP`** 145; closeout doc bullet; plans index **019–145**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`briefing_merge_ready: false`** when deferred.
- T2. Watch summary JSON includes **`briefing_merge_ready`**.
- T3. Strict exit stderr includes **`merge_ready=false`**.
- T4. Plan patch expects **`019–145`**.
