---
title: "fix: queue flags on defer watch poll stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level Queue Flags on Defer Watch Poll stderr (plan 159)

## Summary

Plan 141 flattened **`max_queued_hours`**, **`queue_backlog`**, **`queue_backlog_warning`**, and **`queue_backlog_severe`** to top-level gate JSON. Deferred watch poll stderr still derives **`queued=`** / **`queue_backlog=`** / **`queue_warn=`** from **`_build_defer_queue_context`** before briefing apply instead of the top-level mirror.

---

## Requirements

- R1. **`_format_preflight_watch_poll_line`** emits **`queued=`** / queue flags from top-level flattened fields after **`_apply_lfg_agent_briefing`** when deferred.
- R2. Skip pre-briefing **`_build_defer_queue_context`** queue tokens when **`lfg_deferred`** to avoid duplicates.
- R3. Tests; **`PLAN_TRACK_CAP`** 159; closeout doc bullet; plans index **019–159**.

---

## Test scenarios

- T1. Preflight watch poll stderr includes **`queued=2.5h`** and **`queue_warn=true`** exactly once when deferred with warning-level backlog.
- T2. Gate watch poll stderr includes **`queue_backlog=true`** exactly once when deferred with severe backlog.
- T3. Plan patch expects **`019–159`**.
