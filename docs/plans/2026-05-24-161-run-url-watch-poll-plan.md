---
title: "fix: run URLs on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level Run URLs on Defer Watch Poll stderr (plan 161)

## Summary

Plan 138 flattened **`verify_run_url`** / **`fc_run_url`** to top-level gate JSON and watch summary JSON. Deferred watch poll stderr still omits URL tokens even though run IDs are mirrored (plan 156).

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** emits truncated **`verify_run_url=`** / **`fc_run_url=`** from top-level mirrors after **`_apply_lfg_agent_briefing`** when deferred.
- R2. Reuse stderr truncation helper (96 chars) consistent with **`briefing_command=`** / **`queue_note=`**.
- R3. Tests; **`PLAN_TRACK_CAP`** 161; closeout doc bullet; plans index **019–161**.

---

## Test scenarios

- T1. Preflight watch poll stderr includes **`verify_run_url=`** and **`fc_run_url=`** when deferred and runs are active.
- T2. Gate watch poll stderr includes the same URL tokens.
- T3. Plan patch expects **`019–161`**.
