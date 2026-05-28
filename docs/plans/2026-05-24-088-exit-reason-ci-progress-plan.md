---
title: "feat: lfg exit reason and pr ci progress"
type: feat
status: active
date: 2026-05-24
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: LFG Exit Reason + PR CI Progress (plan 088)

## Summary

Add machine-readable `lfg_exit_reason`, `pr_ci_progress` rollup metrics, and watch early-stop on merge conflicts.

---

## Problem Frame

`lfg_exit_code` alone lacks semantic context. Agents cannot see CI completion fraction. Watch ignores conflict state.

---

## Requirements

- R1. `pr_ci_progress` on `pr_merge_status` with terminal/remaining counts and percent.
- R2. `lfg_exit_reason` alongside `lfg_exit_code` when strict flags active.
- R3. Watch stops with `lfg_pr_watch_result: conflicts` on `pr_merge_conflicts`.
- R4. Tests; bump `PLAN_TRACK_CAP` to `088`; update agent docs.

---

## Scope Boundaries

- Does not change exit code values.
- No workflow YAML changes.

---

## Test scenarios

- T1. pr_ci_progress percent from mixed checks.
- T2. lfg_exit_reason maps exit 3 to blocked reason.
- T3. watch conflicts early exit.
