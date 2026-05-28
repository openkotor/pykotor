---
title: "feat: heartbeat_every json alias and flat_hb summary stderr"
type: feat
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: heartbeat_every JSON Alias and flat_hb Summary Stderr (plan 192)

## Summary

Add **`heartbeat_every`** to **`preflight_watch_summary`** JSON (alias of **`watch_heartbeat_polls`**) and compact gated summary stderr **`flat_keys_heartbeat_polls=`** to **`flat_hb=`**.

---

## Requirements

- R1. Summary JSON sets **`heartbeat_every`** when **`watch_heartbeat_polls > 0`**.
- R2. Gated summary stderr emits **`flat_hb=N`** instead of **`flat_keys_heartbeat_polls=N`**.
- R3. Heartbeat gate accepts **`heartbeat_every`** or **`watch_heartbeat_polls`** for interval.
- R4. Tests; **`PLAN_TRACK_CAP`** 192; closeout index **019–192**.

---

## Test scenarios

- T1. Summary JSON includes **`heartbeat_every`** when interval configured.
- T2. Summary stderr uses **`flat_hb=1`** when heartbeat count gated.
- T3. Plan patch expects **`019–192`**.
