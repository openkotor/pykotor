---
title: "feat: flat_unchanged summary stderr and json alias"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: flat_unchanged Summary Stderr and JSON Alias (plan 194)

## Summary

Compact preflight/gate watch **summary** stderr: emit **`flat_unchanged=N`** (replacing **`unchanged_flat_keys_polls=`**) and add matching **`flat_unchanged`** JSON alias on **`preflight_watch_summary`**.

---

## Requirements

- R1. Summary JSON sets **`flat_unchanged`** when **`unchanged_flat_keys_polls > 0`**.
- R2. Summary stderr emits **`flat_unchanged=N`** instead of **`unchanged_flat_keys_polls=`**.
- R3. Heartbeat gate resolves unchanged count via **`flat_unchanged`** or **`unchanged_flat_keys_polls`**.
- R4. Tests; **`PLAN_TRACK_CAP`** 194; closeout index **019–194**.

---

## Test scenarios

- T1. Summary stderr includes **`flat_unchanged=3`**, not long key.
- T2. Summary JSON includes **`flat_unchanged`** alias.
- T3. Plan patch expects **`019–194`**.
