---
title: "fix: skip legacy run ids on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Skip Legacy verify=/fc= on Defer Watch Poll stderr (plan 162)

## Summary

Plan 156 mirrored **`verify_run=`** / **`fc_run=`** from top-level gate JSON on deferred watch poll stderr. The pre-briefing loop still emits legacy **`verify=`** / **`fc=`** run ID tokens, duplicating the canonical fields on every deferred poll line.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** skips legacy **`verify=`** / **`fc=`** run ID tokens when **`lfg_deferred`** (same gate as plan 157 status dedupe).
- R2. Non-deferred poll lines keep legacy **`verify=`** / **`fc=`** for backward compatibility.
- R3. Tests; **`PLAN_TRACK_CAP`** 162; closeout doc bullet; plans index **019–162**.

---

## Test scenarios

- T1. Deferred preflight watch poll stderr includes **`verify_run=`** / **`fc_run=`** exactly once each and omits legacy **`verify=`** / **`fc=`** tokens.
- T2. Gate watch poll stderr matches the same dedupe behavior.
- T3. Non-deferred poll fixture still emits legacy **`verify=`** / **`fc=`** when applicable.
- T4. Plan patch expects **`019–162`**.
