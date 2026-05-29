---
title: "refactor: preflight max_flat_unchanged summary resolver"
type: refactor
status: active
date: 2026-05-29
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# refactor: Preflight max_flat_unchanged Summary Resolver (plan 209)

## Summary

Add **`_preflight_max_flat_unchanged`** resolver and use it in **`_preflight_watch_summary_flat_stderr_parts`** instead of inline **`summary.get("max_flat_unchanged")`**.

---

## Requirements

- R1. Resolver returns positive **`max_flat_unchanged`** from summary JSON.
- R2. Summary flat stderr uses resolver for gated **`max_flat_unchanged=`** token.
- R3. No behavior change; tests; **`PLAN_TRACK_CAP`** 209; index **019–209**.

---

## Test scenarios

- T1. Resolver returns peak streak from summary dict.
- T2. Summary stderr still emits **`max_flat_unchanged=1`** when peak < total.
- T3. Plan patch expects **`019–209`**.
