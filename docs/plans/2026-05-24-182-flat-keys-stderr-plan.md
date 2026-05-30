---
title: "feat: flat_keys stderr token for poll diffs"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: flat_keys Stderr Token for Poll Diffs (plan 182)

## Summary

Plan 181 added **`lfg_flat_field_keys_present`** JSON. Poll stderr has **`flat_fields=N`** count but not which keys changed. Add **`flat_keys=k1,k2,...`** to shared mirror stderr (prefers cached present-keys list).

---

## Requirements

- R1. **`_lfg_flat_field_keys_present_stderr(status)`** resolves present keys from cache or builds inline.
- R2. Mirror stderr appends **`flat_keys=`** comma list when non-empty (alongside **`flat_fields=N`**).
- R3. Tests; **`PLAN_TRACK_CAP`** 182; closeout bullet; plans index **019–182**.

---

## Test scenarios

- T1. Mirror helper with **`lfg_flat_field_keys_present`** → **`flat_keys=primary_action,fc_run_id`**.
- T2. Strict-exit stderr includes **`flat_keys=`** when top-level flat fields populated.
- T3. Plan patch expects **`019–182`**.
