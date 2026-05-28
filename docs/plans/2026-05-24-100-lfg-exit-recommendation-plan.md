---
title: "feat: lfg exit reason reflects pr ci recommendation"
type: feat
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: LFG Exit Reason + Recommendation (plan 100)

## Summary

Strict merge-gate exit **3** still reports `lfg_exit_reason: pr_checks_pending` while `pr_ci_recommendation.action` is `watch_queue` or `defer_external`. Agents must read two fields. Compound the recommendation into `lfg_exit_reason` and stderr.

---

## Problem Frame

Plan 099 added structured routing but `lfg_exit_reason` (plan 088) was not updated. Strict-mode agents parsing only `lfg_exit_reason` miss queue vs severe-defer semantics.

---

## Requirements

- R1. When exit code **3** and `pr_ci_recommendation.action` differs from blocked state, set `lfg_exit_reason` to `{blocked}:{action}` (e.g. `pr_checks_pending:watch_queue`).
- R2. Stderr strict exit line includes compound reason when present.
- R3. Extend `LFG_EXIT_CODES[3]` legend for recommendation suffixes.
- R4. Tests; bump `PLAN_TRACK_CAP` to `100`; update closeout + AGENTS.

---

## Scope Boundaries

- Does not change exit code values or merge blocked field names.
- Does not auto-run recommended commands.

---

## Test scenarios

- T1. Exit 3 + pending + watch_queue → `pr_checks_pending:watch_queue`.
- T2. Exit 3 + pending + defer_external → `pr_checks_pending:defer_external`.
- T3. Exit 3 + failed checks → unchanged `pr_checks_failed` (no compound when action matches blocked semantics).
