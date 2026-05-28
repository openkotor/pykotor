---
title: "fix: merge_ready on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: briefing_merge_ready on Defer Watch Poll stderr (plan 155)

## Summary

Plan 145 flattened **`briefing_merge_ready`** to top-level gate JSON and added **`merge_ready=`** on strict exit and watch summary one-liners. Deferred watch poll stderr still omits **`merge_ready=`**, so agents polling **`--lfg-gate-watch`** cannot see merge-readiness on each poll.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** appends **`merge_ready=`** when briefing carries **`merge_ready`** after **`_apply_lfg_agent_briefing`**.
- R2. Tests for preflight and gate poll lines with deferred **`merge_ready=false`**.
- R3. **`PLAN_TRACK_CAP`** 155; closeout doc bullet; plans index **019–155**.

---

## Test scenarios

- T1. Preflight watch poll stderr includes **`merge_ready=false`** when deferred.
- T2. Gate watch poll stderr includes **`merge_ready=false`** on the same fixture.
- T3. Plan patch expects **`019–155`**.
