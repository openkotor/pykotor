---
title: "fix: defer briefing includes monitor commands"
type: fix
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Defer Monitor Commands (plan 113)

## Summary

When LFG defers on active FC (`fc_active_pending` / `fc_active_closeout`), agents get run ids but must guess how to wait. Add structured **`monitor_commands`** to defer briefing (gh run watch + preflight retry).

---

## Problem Frame

Live: FC run `26546235822` queued; defer briefing has `fc_run_id`/`fc_run_url` (plan 112) but no copy-paste watch command. Agents re-poll preflight blindly.

---

## Requirements

- R1. `_build_defer_monitor_commands(briefing)` returns dict with `preflight_retry` and optional `watch_fc_run` / `watch_verify_run`.
- R2. Defer briefing attaches `monitor_commands` after active run refs.
- R3. Defer stderr includes `watch=` when `watch_fc_run` or `watch_verify_run` present.
- R4. Tests; `PLAN_TRACK_CAP` `113`; closeout + plan 020 docs.

---

## Test scenarios

- T1. FC queued defer → `monitor_commands.watch_fc_run` is `gh run watch {id} --exit-status`.
- T2. Defer with verify active → `monitor_commands.watch_verify_run` set.
- T3. stderr includes `watch=gh run watch`.
