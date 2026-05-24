---
title: "verify: ci queue closeout post-283"
type: verify
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# verify: CI Queue Closeout Post-#283

## Summary

PR #283 merged `paths-ignore: docs/**` on Forward Commits and Auto-Publish. Runner backlog still holds six+ queued FC runs from pre-#283 docs merges and a stack of Verify PyPI `workflow_run` triggers (some **pending** with `jobs: []` while concurrency waits). Cancel superseded runs, keep one `workflow_dispatch` verify run, record evidence in plan 020/031/034, and re-run local discovery smoke.

## Problem Frame

- Forward Commits runs 26362988041–26363209835 are **queued** on docs-only pushes; they no longer represent actionable work after #283.
- Verify PyPI `workflow_run` run 26363272590 is **pending** with empty `jobs` (concurrency wait before gate materializes); dispatch run 26363187827 has **Check trigger** queued (post-#280 fix valid).
- Plan 034 landed; closeout needs updated verification tables, not more workflow YAML unless a regression appears.

## Requirements

- R1. Cancel stale queued Forward Commits runs triggered by docs-only merges (keep post-#283 run 26363271048 if still queued).
- R2. Cancel superseded Verify PyPI `workflow_run` runs that are pending with empty jobs or duplicate cancelled noise; retain dispatch 26363187827.
- R3. Local `discover_tools.py --cli-only` and core import smoke pass.
- R4. Update `docs/plans/2026-05-24-020-verify-pypi-regression-post-268-plan.md` verification table with post-#283 CI state.
- R5. Update plan 034 verification with cancel evidence; mark plan 035 `completed`.

## Implementation Units

- U1. **CI hygiene** — `gh run cancel` on enumerated stale run IDs (no workflow edits).
- U2. **Docs evidence** — plan 020, 034, 035 verification tables.

## Test Scenarios

| ID | Scenario | Expected |
|----|----------|----------|
| T1 | Cancel docs-era FC runs | runs show `cancelled` |
| T2 | Cancel empty-pending verify workflow_run | queue drained |
| T3 | Local CLI discovery | 3 tools JSON |
| T4 | Local core imports | pykotor smoke pass |
| T5 | Dispatch 26363187827 | gate job present (queued or running) |

## Verification

| Check | Evidence | Result |
|-------|----------|--------|
| Stale FC queue | Cancelled 26363209835, 26363169705, 26363111619, 26363039605, 26362988041 | ✅ pass |
| Verify workflow_run noise | Cancelled pending empty 26363272590 | ✅ pass |
| Verify dispatch | [26363187827](https://github.com/OpenKotOR/PyKotor/actions/runs/26363187827) — Check trigger queued | ✅ pass |
| Forward Commits post-#283 | [26363271048](https://github.com/OpenKotOR/PyKotor/actions/runs/26363271048) queued | ⏳ runner backlog |
| Local discovery | holopatcher, kotordiff, kotormcp | ✅ pass |
| Local core imports | pykotor smoke via PYTHONPATH | ✅ pass |
| Plan 020 row | post-#283 evidence URLs | ✅ pass |

## Scope Boundaries

- Does not wait for full PyPI matrix green (runner backlog external).
- Does not remove `workflow_run` trigger (deferred unless empty-job regression recurs after queue drain).
- No game-engine or product code changes.

## Sources & References

- Master tip: `f8e9de37f` (#283)
- FC queued: 26363271048, 26363209835, 26363169705, 26363111619, 26363039605, 26362988041
- Verify dispatch: https://github.com/OpenKotOR/PyKotor/actions/runs/26363187827
- Verify workflow_run pending empty: https://github.com/OpenKotOR/PyKotor/actions/runs/26363272590
- Plan 034: `docs/plans/2026-05-24-034-skip-ci-on-docs-only-pushes-plan.md`
