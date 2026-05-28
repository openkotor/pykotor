---
title: "fix: top-level queue_context and watch summary queued stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level queue_context and Watch Summary queued Stderr (plan 131)

## Summary

Plans 129–130 surfaced **`gh_watch_summary`** and **`active_runs`** at top-level gate JSON and **`queued=`** on strict exit. **`queue_context`** still requires drilling into **`lfg_agent_briefing`**, and watch summary stderr lacks aggregate **`queued=`**.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors **`queue_context`** to top-level status JSON.
- R2. **`preflight_watch_summary`** JSON includes **`queue_context`** from **`_build_defer_queue_context`**.
- R3. **`_format_preflight_watch_summary_line`** appends **`queued=`** and queue flags from summary **`queue_context`**.
- R4. Tests; **`PLAN_TRACK_CAP`** 131; closeout doc bullet; plans index **019–131**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`queue_context.max_queued_hours`** when deferred.
- T2. Watch summary JSON includes **`queue_context`**; one-liner has **`queued=1.5h`**.
- T3. Plan patch expects **`019–131`**.
