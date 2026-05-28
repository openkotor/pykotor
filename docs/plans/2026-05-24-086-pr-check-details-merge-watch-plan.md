---
title: "feat: pr check details and merge watch shorthand"
type: feat
status: active
date: 2026-05-24
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# feat: PR Check Details + Merge Watch Shorthand (plan 086)

## Summary

Enrich `pr_merge_status` with check job URLs and in-progress counts, improve failed-state hints with `gh pr checks --failed`, add watch poll stderr, and `--lfg-merge-watch` shorthand.

---

## Problem Frame

Rollup only exposes check names — agents cannot jump to failing jobs. Watch mode is silent for minutes. Agents need another flag combo for merge-gate + poll.

---

## Requirements

- R1. `_summarize_pr_checks` adds `checks_in_progress`, `failed_check_details`, `pending_check_details` (name + detailsUrl + workflowName).
- R2. Failed `merge_hint` includes `gh pr checks <n> --failed` when PR number known.
- R3. `--lfg-merge-watch` expands to `--lfg-merge-gate --lfg-pr-watch`; `lfg_mode: merge_watch`.
- R4. `_watch_pr_merge_status` prints stderr poll summary each iteration.
- R5. Tests; bump `PLAN_TRACK_CAP` to `086`; update agent docs.

---

## Scope Boundaries

- Does not auto-open URLs or run `gh pr checks`.
- No workflow YAML changes.

---

## Test scenarios

- T1. Failed check details include detailsUrl.
- T2. Failed merge_hint mentions `gh pr checks`.
- T3. merge_watch mode and flag expansion.
