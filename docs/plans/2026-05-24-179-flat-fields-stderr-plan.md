---
title: "feat: flat_fields stderr token for poll scans"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: flat_fields Stderr Token for Poll Scans (plan 179)

## Summary

Plan 178 added **`lfg_flat_field_values`** JSON. Poll and strict-exit stderr still lack a quick populated-field count. Add **`flat_fields=N`** to **`_lfg_briefing_mirror_stderr_parts`** (prefers cached **`lfg_flat_field_values`**, else builds count inline).

---

## Requirements

- R1. **`_lfg_flat_field_stderr_count(status)`** returns len of cached values or **`_build_lfg_flat_field_values`**.
- R2. Mirror stderr appends **`flat_fields=N`** when **N > 0**.
- R3. Poll, strict-exit, watch-summary, and briefing stderr inherit via shared helper.
- R4. Tests; **`PLAN_TRACK_CAP`** 179; closeout bullet; plans index **019–179**.

---

## Test scenarios

- T1. Mirror helper with **`lfg_flat_field_values`** → **`flat_fields=3`** (example count).
- T2. Strict exit / deferred poll stderr includes **`flat_fields=`** after apply-shaped status.
- T3. Plan patch expects **`019–179`**.
