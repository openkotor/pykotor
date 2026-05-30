---
title: "fix: investigate ci drift briefing wait on active runs"
type: fix
status: active
date: 2026-05-28
origin: docs/solutions/testing/verify-pypi-regression-closeout.md
---

# fix: Investigate CI Drift Active-Run Wait (plan 115)

## Summary

When `proceed_reason` is `investigate_ci_drift` but FC/verify runs are still active, agents should wait before `--lfg-refresh --dry-run`. Enrich drift briefing with structured fields and route to `--lfg-preflight-watch`.

---

## Problem Frame

Live: FC run IDs churn while queued; drift briefing only has text notes and suggests refresh dry-run prematurely.

---

## Requirements

- R1. `_build_ci_drift_detail` exposes doc vs live drift fields and `wait_recommended`.
- R2. `_build_drift_refresh_commands` lists refresh/closeout/preflight-watch commands.
- R3. `investigate_ci_drift` briefing includes `drift`, `refresh_commands`, active run refs, `monitor_commands` when waiting.
- R4. `_build_proceed_hint` prefers `--lfg-preflight-watch` when drift + active runs.
- R5. stderr `wait=true` and drift field hints; tests; `PLAN_TRACK_CAP` `115`; docs.

---

## Test scenarios

- T1. Drift + FC queued → `wait_recommended` true, command includes preflight-watch.
- T2. Drift + both terminal → `refresh_commands.closeout` present.
- T3. stderr includes `wait=true` when active.
