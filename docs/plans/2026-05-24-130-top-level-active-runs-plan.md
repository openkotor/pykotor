---
title: "fix: top-level active_runs json and strict exit queued stderr"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level active_runs JSON and Strict Exit queued Stderr (plan 130)

## Summary

Plan 129 mirrored **`gh_watch_summary`** to top-level gate JSON. **`active_runs`** still requires drilling into **`lfg_agent_briefing`**. Briefing stderr emits **`queued=X.Xh`** but **`LFG exit:`** does not.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors **`active_runs`** to top-level status JSON.
- R2. **`_emit_lfg_strict_exit_stderr`** appends **`queued=X.Xh`** from briefing **`queue_context.max_queued_hours`**.
- R3. Tests; **`PLAN_TRACK_CAP`** 130; closeout doc bullet; plans index **019–130**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`active_runs`** when deferred with active runs.
- T2. Strict exit defer briefing → stderr contains **`queued=1.5h`**.
- T3. Plan patch expects **`019–130`**.
