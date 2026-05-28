---
title: "feat: lfg_flat_field_values compact gate JSON"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: lfg_flat_field_values Compact Gate JSON (plan 178)

## Summary

Plan 177 exported **`lfg_flat_field_keys`** as a legend. Agents still scan many top-level keys. Add **`lfg_flat_field_values`** — a dict of only populated flattened fields — on status and preflight watch summary after apply/mirror.

---

## Requirements

- R1. **`_build_lfg_flat_field_values(status)`** collects non-empty values for keys in **`LFG_FLAT_FIELD_KEYS`** (bools included when present).
- R2. **`_apply_lfg_agent_briefing`** sets **`lfg_flat_field_values`** when non-empty; pops when cleared.
- R3. **`_mirror_preflight_watch_summary_from_status`** rebuilds values from mirrored summary fields.
- R4. Tests; **`PLAN_TRACK_CAP`** 178; closeout bullet; plans index **019–178**.

---

## Test scenarios

- T1. Apply drift briefing → **`lfg_flat_field_values`** includes **`wait_recommended`**, **`ci_drift`**, run refs; omits unset keys.
- T2. Watch summary mirror includes compact values dict.
- T3. Plan patch expects **`019–178`**.
