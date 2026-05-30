---
title: "fix: defer active_runs and closeout expected-after"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Defer Active Runs and Closeout Expected-After (plan 124)

## Summary

Live defer **`unchanged_active_runs`** with FC queued: agents need to know which runs block LFG and that **`--lfg-closeout`** follows terminal. Add **`active_runs`** to defer briefing/stderr/watch polls and prefer **`closeout`** in **`expected_after_terminal`** for closeout-style defer reasons.

---

## Requirements

- R1. `_build_active_runs_list(status)` shared helper; used by drift detail and defer briefing.
- R2. Defer briefing includes `active_runs`; stderr `active_runs=fc` (comma-separated).
- R3. Watch poll line includes `active_runs=` when any run active.
- R4. `_build_defer_post_terminal_commands` adds `closeout` for unchanged_active_runs / fc_active_closeout / verify_active_closeout.
- R5. `_build_defer_expected_after_terminal` order: prefetch_gate → closeout → gate → preflight.
- R6. Tests; `PLAN_TRACK_CAP` 124; closeout doc bullet.

---

## Test scenarios

- T1. FC-only active defer → briefing `active_runs=["fc"]`, stderr `active_runs=fc`.
- T2. unchanged_active_runs → `expected_after_terminal.action=closeout`.
- T3. Watch poll line includes `active_runs=fc`.
- T4. Plan patch expects `019–124`.
