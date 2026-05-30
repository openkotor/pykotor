---
title: "fix: queue_note on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: queue_note on Defer Watch Poll stderr (plan 150)

## Summary

Plan 146 flattened **`queue_backlog_note`** to top-level gate JSON and added truncated **`queue_note=`** on strict exit and watch summary one-liners. Deferred **watch poll** stderr still omits **`queue_note=`**, so agents polling **`--lfg-gate-watch`** miss runner backlog context until the watch ends.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** appends truncated **`queue_note=`** when **`queue_backlog_note`** is present after **`_apply_lfg_agent_briefing`** (gate and preflight poll labels).
- R2. Tests for preflight and gate poll lines with deferred briefing carrying queue backlog note.
- R3. **`PLAN_TRACK_CAP`** 150; closeout doc bullet; plans index **019–150**.

---

## Test scenarios

- T1. Preflight watch poll stderr includes **`queue_note=`** when deferred with checkpoint queue backlog note.
- T2. Gate watch poll stderr includes **`queue_note=`** on the same fixture.
- T3. Plan patch expects **`019–150`**.
