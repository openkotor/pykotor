---
title: "feat: merge conflicts gate and lfg exit code"
type: feat
status: active
date: 2026-05-24
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: Merge Conflicts Gate + LFG Exit Code (plan 087)

## Summary

Handle PR merge conflicts in rollup, add pending watch gh hint, and expose `lfg_exit_code` in JSON for strict gate modes.

---

## Problem Frame

Pending hints lack `gh pr checks --watch`. `mergeable: CONFLICTING` is ignored. Agents parsing JSON cannot see exit code before process exits.

---

## Requirements

- R1. `mergeable: CONFLICTING` sets `lfg_merge_blocked: pr_merge_conflicts` and blocks merge.
- R2. Pending `merge_hint` includes `gh pr checks <n> --watch`.
- R3. JSON includes `lfg_exit_code` when `--strict-defer-exit` or `--strict-pr-ci-exit` is active.
- R4. Tests; bump `PLAN_TRACK_CAP` to `087`; update agent docs.

---

## Scope Boundaries

- Does not run gh commands automatically.
- No workflow YAML changes.

---

## Test scenarios

- T1. CONFLICTING mergeable blocks ready state.
- T2. Pending hint includes `--watch`.
- T3. lfg_exit_code is 3 when PR CI pending under merge-gate.
