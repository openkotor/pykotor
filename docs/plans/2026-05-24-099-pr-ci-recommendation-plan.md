---
title: "feat: pr ci recommendation and queue poll context"
type: feat
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: PR CI Recommendation + Queue Poll Context (plan 099)

## Summary

Agents need a structured **`pr_ci_recommendation`** (action/reason/command), a top-level **`pr_queue_backlog_note`**, and richer watch poll stderr (queue age, rollup delta).

---

## Problem Frame

Merge-gate JSON is comprehensive but agents must infer next steps from multiple fields. Watch polls omit queue age and crosscheck delta already available on gate JSON.

---

## Requirements

- R1. `pr_ci_recommendation` with `action`, `reason`, `command` when track complete.
- R2. `pr_queue_backlog_note` when `queue_backlog` (aligns with closeout defer guidance at severe).
- R3. Watch poll stderr adds `queue_age=` and `rollup_delta=` when available.
- R4. Tests; bump `PLAN_TRACK_CAP` to `099`; update docs.

---

## Scope Boundaries

- Does not auto-run watch or merge.

---

## Test scenarios

- T1. Recommendation `watch_queue` during queue backlog.
- T2. Recommendation `defer_external` when severe backlog.
- T3. Recommendation `merge` when `pr_merge_ready`.
