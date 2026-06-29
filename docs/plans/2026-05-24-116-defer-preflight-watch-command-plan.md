---
title: "fix: defer fc-active command routes to preflight-watch"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Defer Preflight-Watch Command (plan 116)

## Summary

When deferred on active FC (`fc_active_pending`), `monitor_commands` includes `preflight_watch` but `command`/`proceed_hint` still suggest manual `--lfg-preflight` retry. Route primary command to **`--lfg-preflight-watch`**.

---

## Problem Frame

Live: `fc_active_pending`; agents get watch_fc_run but command says re-run preflight manually.

---

## Requirements

- R1. `_defer_preflight_watch_recommended` true for fc/verify active defer reasons.
- R2. `_build_proceed_hint` uses `--lfg-preflight-watch` for those defers.
- R3. Defer briefing sets `watch_recommended` and `command` to preflight-watch.
- R4. Defer stderr includes `watch_recommended=true`; tests; `PLAN_TRACK_CAP` `116`; docs.

---

## Test scenarios

- T1. fc_active_pending proceed_hint → preflight-watch.
- T2. Defer briefing command matches preflight_watch monitor command.
- T3. stderr includes watch_recommended=true.
