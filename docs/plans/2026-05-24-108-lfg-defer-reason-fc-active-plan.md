---
title: "fix: semantic lfg defer reason for fc active pending"
type: fix
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Semantic LFG Defer Reason for FC Active Pending (plan 108)

## Summary

When plan 107 defers because FC is still active, agents get generic `deferred` / `blocked: deferred` and stderr says "monitoring checkpoint unchanged" — misleading while FC is queued with SHA mismatch. Expose **`lfg_defer_reason: fc_active_pending`**, richer pending notes, and targeted proceed hints.

---

## Problem Frame

Live: FC queued on `bcb5586`, verify terminal, `lfg_deferred: true`. Stderr and exit reason do not distinguish FC-active-pending from unchanged-checkpoint defer.

---

## Requirements

- R1. Add `_resolve_lfg_defer_reason` mapping checkpoint defer text to `fc_active_pending`, `unchanged_active_runs`, or `deferred`.
- R2. Set `lfg_defer_reason` on status when `defer_lfg_pr` is true.
- R3. Include `queued_hours` in `fc_stale_gap_pending_note` when available.
- R4. `_apply_lfg_defer` stderr uses checkpoint `defer_reason`, not generic unchanged text.
- R5. Exit **2** `lfg_exit_reason` compounds defer reason (e.g. `deferred:fc_active_pending`).
- R6. `proceed_hint` for `fc_active_pending` → `--lfg-preflight` with poll comment.
- R7. Briefing `reason` uses `lfg_defer_reason`; tests; `PLAN_TRACK_CAP` `108`; docs.

---

## Scope Boundaries

- Does not poll/wait for FC automatically.
- Does not change classify git logic.

---

## Test scenarios

- T1. FC active defer → `lfg_defer_reason` is `fc_active_pending`.
- T2. Pending note includes queued hours when present on FC run.
- T3. `_compute_lfg_exit_reason` exit 2 → `deferred:fc_active_pending`.
- T4. Proceed hint for fc_active_pending mentions `--lfg-preflight`.
