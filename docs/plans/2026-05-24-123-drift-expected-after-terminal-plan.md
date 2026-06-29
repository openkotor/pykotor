---
title: "fix: drift expected-after-terminal and primary action"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Drift Expected-After-Terminal and Primary Action (plan 123)

## Summary

Live gate reports **`investigate_ci_drift`** with active FC/verify runs. Parity with defer briefing: add **`expected_after_terminal`**, **`primary_action: gate_watch`**, and **`queue_context`** on drift-wait paths; surface on stderr.

---

## Requirements

- R1. `_build_drift_expected_after(refresh_commands)` prefers closeout → refresh_dry_run → gate → preflight.
- R2. Drift briefing with `wait_recommended` sets `primary_action: gate_watch`, `expected_after_terminal`, and `queue_context`.
- R3. Drift briefing without wait sets `expected_after_terminal` to closeout when available.
- R4. Stderr for `investigate_ci_drift` includes `primary_action`, `expected_after`, and `queued=` when queue_context present.
- R5. Fix `expected_after` variable shadowing `action` in stderr emitter; tests; `PLAN_TRACK_CAP` 123; docs.

---

## Test scenarios

- T1. Active FC drift → `wait_recommended`, `primary_action=gate_watch`, `expected_after.action=refresh_dry_run`.
- T2. Terminal drift → `expected_after.action=closeout`.
- T3. stderr drift includes `expected_after=refresh_dry_run` and `primary_action=gate_watch`.
- T4. Plan patch expects `019–123`.
