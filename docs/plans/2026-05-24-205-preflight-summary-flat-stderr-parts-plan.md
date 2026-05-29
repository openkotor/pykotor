---
title: "refactor: extract preflight watch summary flat stderr parts"
type: refactor
status: active
date: 2026-05-29
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# refactor: Extract Preflight Watch Summary Flat Stderr Parts (plan 205)

## Summary

Extract **`_preflight_watch_summary_flat_stderr_parts`** from **`_format_preflight_watch_summary_line`**, pairing with plan 204’s poll-line flat stderr helper.

---

## Requirements

- R1. Summary line defers flat unchanged/heartbeat tokens to **`_preflight_watch_summary_flat_stderr_parts`**.
- R2. No stderr behavior change.
- R3. Tests; **`PLAN_TRACK_CAP`** 205; closeout index **019–205**.

---

## Test scenarios

- T1. Direct helper test for unchanged + heartbeat branches.
- T2. Existing summary-line tests still pass.
- T3. Plan patch expects **`019–205`**.
