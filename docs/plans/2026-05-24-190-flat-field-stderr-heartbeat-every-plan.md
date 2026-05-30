---
title: "feat: flat-field stderr helper and heartbeat_every poll token"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: Flat-Field Stderr Helper and heartbeat_every Poll Token (plan 190)

## Summary

Extract **`_lfg_flat_field_mirror_stderr_parts`** next to flat-field stderr helpers and emit **`heartbeat_every=N`** on gate-watch poll lines when flat keys are unchanged.

---

## Requirements

- R1. **`_lfg_briefing_mirror_stderr_parts`** delegates flat-field tokens to **`_lfg_flat_field_mirror_stderr_parts`**.
- R2. Unchanged or heartbeat flat-key poll lines append **`heartbeat_every=N`** when interval **> 0**.
- R3. Tests; **`PLAN_TRACK_CAP`** 190; closeout index **019–190**.

---

## Test scenarios

- T1. Shared helper emits **`flat_fields=`** / **`flat_keys=`**.
- T2. Compact unchanged poll line includes **`heartbeat_every=12`**.
- T3. Plan patch expects **`019–190`**.
