---
title: "refactor: extract preflight summary unchanged flat stderr parts"
type: refactor
status: active
date: 2026-05-29
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# refactor: Extract Preflight Summary Unchanged Flat Stderr Parts (plan 213)

## Summary

Extract **`_preflight_watch_summary_unchanged_flat_stderr_parts`** from **`_preflight_watch_summary_flat_stderr_parts`**, composing plans 210–212 gate helpers for unchanged-block tokens.

---

## Requirements

- R1. Unchanged block helper emits **`flat_unchanged`**, gated **`max_flat_unchanged`**, gated **`heartbeat_every`**.
- R2. Summary flat stderr delegates unchanged block to helper, then appends **`flat_hb_total`**.
- R3. No behavior change; tests; **`PLAN_TRACK_CAP`** 213; index **019–213**.

---

## Test scenarios

- T1. Direct unchanged-block helper test with peak **<** total.
- T2. Existing summary flat stderr tests pass.
- T3. Plan patch expects **`019–213`**.
