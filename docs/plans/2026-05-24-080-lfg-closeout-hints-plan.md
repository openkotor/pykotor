---
title: "feat: lfg closeout hints and terminal doc sync"
type: feat
status: completed
date: 2026-05-24
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: LFG Closeout Hints + Terminal Doc Sync (plan 080)

## Summary

Align agent hints with plan 079 `--lfg-gate`, add machine-readable `lfg_mode`, extend help/examples, and run terminal doc closeout now that verify/FC runs succeeded.

---

## Problem Frame

Plans 074–079 built the agent loop, but deferred `proceed_hint` still recommends the long monitor+strict form, JSON lacks a mode field, and CI has reached terminal success while solution doc Last CI check still shows queued runs.

---

## Requirements

- R1. `_build_proceed_hint` deferred path recommends `--lfg-gate`.
- R2. JSON includes `lfg_mode` (`gate` | `preflight` | `refresh` | `closeout` | null).
- R3. `--lfg-closeout` shorthand for `--lfg-refresh` without dry-run (doc write + dispatch path).
- R4. Argparse epilog lists lfg commands; bump `PLAN_TRACK_CAP` to `080`.
- R5. Execute terminal doc sync via `--lfg-closeout` when `update_monitoring_docs` is actionable.
- R6. Unit tests for hint, mode, closeout flag expansion.

---

## Scope Boundaries

- No workflow YAML changes.
- No merge of PR #308 in this plan.

---

## Implementation Units

- U1. **Hint + mode + closeout flag**
  - Modify: `.github/scripts/local_verify_pypi_slice.py`
  - Test: `Libraries/PyKotor/tests/test_utility/test_local_verify_checkpoint.py`
  - deferred hint → `--lfg-gate`; set `lfg_mode`; add `--lfg-closeout`

- U2. **Docs + AGENTS**
  - Modify: `docs/solutions/testing/verify-pypi-regression-closeout.md`, `AGENTS.md`
  - Agent loop step for `--lfg-closeout`

- U3. **Terminal sync**
  - Run `--lfg-closeout` when live gh reports terminal success; commit resulting doc updates

---

## Test scenarios

- T1. deferred proceed_hint contains `--lfg-gate`.
- T2. `--lfg-closeout` sets lfg_refresh + write, not dry_run.
- T3. JSON `lfg_mode` is `closeout` when flag set.
