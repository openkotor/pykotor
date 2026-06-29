---
title: "fix: mirror watch summary from top-level status"
type: fix
status: completed
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Mirror Preflight Watch Summary from Top-Level status (plan 170)

## Summary

`_apply_lfg_agent_briefing` already flattens defer briefing fields onto top-level **`status`** (plans 129–167). **`_watch_lfg_preflight_defer`** still copies the same fields from nested **`lfg_agent_briefing`** into **`preflight_watch_summary`**, diverging from gate JSON and deferred poll stderr which read **`status`** after apply.

---

## Requirements

- R1. Add **`_mirror_preflight_watch_summary_from_status(status, summary)`** that copies briefing mirrors from top-level **`status`**.
- R2. **`_watch_lfg_preflight_defer`** calls **`_apply_lfg_agent_briefing`** then the helper when deferred; remove duplicate briefing→summary copies.
- R3. **`active_runs`** / **`gh_watch_summary`** on summary prefer top-level **`status`** after briefing apply.
- R4. Tests; **`PLAN_TRACK_CAP`** 170; closeout bullet; plans index **019–170**.

---

## Implementation Units

- U1. Helper + watch defer refactor in `.github/scripts/local_verify_pypi_slice.py`
- U2. Tests in `Libraries/PyKotor/tests/test_utility/test_local_verify_checkpoint.py`
- U3. Closeout doc + plan index

---

## Test scenarios

- T1. Helper copies **`primary_action`**, **`verify_run_id`**, **`briefing_action`** from status onto summary.
- T2. Deferred watch timeout: **`preflight_watch_summary`** includes top-level mirrored **`primary_action=gate_watch`** (patched defer path).
- T3. Plan patch expects **`019–170`**.
