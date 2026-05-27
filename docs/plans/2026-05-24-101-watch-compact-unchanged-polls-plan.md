---
title: "feat: compact unchanged pr watch poll stderr"
type: feat
status: active
date: 2026-05-27
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: Compact Unchanged PR Watch Polls (plan 101)

## Summary

During long runner queue backlogs, merge-watch emits identical full poll lines every 30s. Agents need a compact **unchanged** stderr line when CI progress metrics are flat, plus a summary **`unchanged_polls`** count.

---

## Problem Frame

Queue waits can span hours with `complete=4%` and `pending=27` unchanged. Verbose poll lines waste context window without adding signal.

---

## Requirements

- R1. When consecutive watch snapshots share the same progress key (`completion_percent`, pending, in_progress, success, failed), stderr uses `unchanged complete=X% pending=N` instead of the full counts line.
- R2. Queue backlog still appends `queue_age=` on compact lines when available.
- R3. `pr_watch_summary.unchanged_polls` counts flat polls.
- R4. Tests; bump `PLAN_TRACK_CAP` to `101`; update closeout + AGENTS + plan 020.

---

## Scope Boundaries

- Does not skip polls or change watch exit semantics.
- Full poll line still emitted when any progress key field changes.

---

## Test scenarios

- T1. Two identical snapshots → second poll line contains `unchanged`.
- T2. Progress change → full poll line restored.
- T3. Summary reports `unchanged_polls` correctly.
