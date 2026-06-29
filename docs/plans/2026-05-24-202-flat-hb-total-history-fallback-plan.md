---
title: "feat: derive flat_hb_total from watch history fallback"
type: feat
status: active
date: 2026-05-29
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: flat_hb_total History Fallback in Watch Summary (plan 202)

## Summary

Add **`_max_preflight_flat_hb_total`** to read peak cumulative heartbeat count from **`preflight_watch_history`**, and use it as a fallback when building **`preflight_watch_summary`** if **`preflight_flat_keys_heartbeats`** is unset.

---

## Requirements

- R1. **`_max_preflight_flat_hb_total(history)`** prefers **`flat_hb_total`**, falls back to **`flat_hb`** per snapshot.
- R2. **`_build_preflight_watch_summary`** uses history fallback when status counter is zero.
- R3. Tests; **`PLAN_TRACK_CAP`** 202; closeout index **019–202**.

---

## Test scenarios

- T1. History-only status with heartbeat snapshots → summary **`flat_hb_total=2`**.
- T2. Status counter present still wins over history.
- T3. Plan patch expects **`019–202`**.
