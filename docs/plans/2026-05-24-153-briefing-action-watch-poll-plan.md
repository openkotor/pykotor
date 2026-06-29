---
title: "fix: briefing action on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: briefing_action on Defer Watch Poll stderr (plan 153)

## Summary

Plan 142 flattened **`briefing_action`** to top-level gate JSON and added **`action=`** on strict exit and watch summary one-liners. Deferred watch poll stderr still omits **`action=`**, so agents polling **`--lfg-gate-watch`** cannot see the briefing action (e.g. **`defer`**) on each poll.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** appends **`action=`** when top-level **`briefing_action`** is set after **`_apply_lfg_agent_briefing`**.
- R2. Tests for preflight and gate poll lines with deferred **`action=defer`**.
- R3. **`PLAN_TRACK_CAP`** 153; closeout doc bullet; plans index **019–153**.

---

## Test scenarios

- T1. Preflight watch poll stderr includes **`action=defer`** when deferred.
- T2. Gate watch poll stderr includes **`action=defer`** on the same fixture.
- T3. Plan patch expects **`019–153`**.
