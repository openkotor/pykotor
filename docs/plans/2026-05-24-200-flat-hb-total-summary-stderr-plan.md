---
title: "feat: flat_hb_total token on preflight watch summary stderr"
type: feat
status: active
date: 2026-05-29
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: flat_hb_total on Preflight Watch Summary Stderr (plan 200)

## Summary

Align preflight watch **summary stderr** with plan 199 JSON by emitting **`flat_hb_total=N`** instead of **`flat_hb=N`**. Poll lines keep compact **`flat_hb=N`**.

---

## Requirements

- R1. `_format_preflight_watch_summary_line` emits **`flat_hb_total=N`** when heartbeat summary gate passes.
- R2. Summary stderr omits legacy **`flat_hb=`** token.
- R3. Poll stderr unchanged (**`flat_hb=N`** cumulative).
- R4. Tests; **`PLAN_TRACK_CAP`** 200; closeout index **019–200**.

---

## Test scenarios

- T1. Summary line with heartbeats → **`flat_hb_total=1`** on stderr.
- T2. Early summary (unchanged < interval) omits **`flat_hb_total=`**.
- T3. Plan patch expects **`019–200`**.
