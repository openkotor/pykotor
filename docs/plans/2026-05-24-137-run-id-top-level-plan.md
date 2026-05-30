---
title: "fix: top-level verify and fc run id json"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Top-Level verify_run_id and fc_run_id JSON (plan 137)

## Summary

Defer briefing exposes **`verify_run_id`** / **`fc_run_id`**, and stderr carries **`verify_run=`** / **`fc_run=`**, but top-level gate JSON omits run IDs unless agents drill into **`lfg_agent_briefing`**.

---

## Requirements

- R1. **`_apply_lfg_agent_briefing`** mirrors **`verify_run_id`** and **`fc_run_id`** to top-level status JSON when set.
- R2. **`preflight_watch_summary`** JSON includes both run IDs on deferred watch end.
- R3. Tests; **`PLAN_TRACK_CAP`** 137; closeout doc bullet; plans index **019–137**.

---

## Test scenarios

- T1. Gate JSON top-level includes **`verify_run_id`** and **`fc_run_id`** when deferred with active runs.
- T2. Watch summary JSON includes both run IDs.
- T3. Plan patch expects **`019–137`**.
