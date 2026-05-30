---
title: "feat: lfg_flat_field_keys_present in gate JSON"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: lfg_flat_field_keys_present in Gate JSON (plan 181)

## Summary

Plan 178 added **`lfg_flat_field_values`** (full compact dict). Agents iterating keys still pay dict size cost. Add **`lfg_flat_field_keys_present`** — ordered key list of populated flat fields only — on status and preflight watch summary.

---

## Requirements

- R1. **`_build_lfg_flat_field_keys_present(flat_values)`** preserves **`LFG_FLAT_FIELD_KEYS`** order.
- R2. **`_apply_lfg_agent_briefing`** sets **`lfg_flat_field_keys_present`** when values exist; pops when cleared.
- R3. Watch summary mirror rebuilds present-keys from mirrored values.
- R4. Tests; **`PLAN_TRACK_CAP`** 181; closeout bullet; plans index **019–181**.

---

## Test scenarios

- T1. Apply briefing → present-keys list matches populated subset in canonical order.
- T2. Watch summary includes present-keys after mirror.
- T3. Plan patch expects **`019–181`**.
