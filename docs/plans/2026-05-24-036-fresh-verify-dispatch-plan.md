---
title: "verify: fresh verify-pypi dispatch after queue stall"
type: verify
status: completed
date: 2026-05-24
origin: lfg-pypi-regression-closeout
strategy_track: test-signal-quality
---

# verify: Fresh Verify PyPI Dispatch After Queue Stall

## Summary

Verify PyPI dispatch [26363187827](https://github.com/OpenKotOR/PyKotor/actions/runs/26363187827) and Forward Commits [26363271048](https://github.com/OpenKotOR/PyKotor/actions/runs/26363271048) remain **queued** with no runner progress since plan 035. Cancel the stale verify dispatch, re-dispatch on current master (`d54eda7e7`), re-run local smoke, and record fresh run URLs in plan 020/036. Leave FC 26363271048 queued (no `workflow_dispatch`; cancelling would lose the post-#283 trigger).

## Problem Frame

Runner backlog prevents CI green evidence. Stale verify dispatch may block the `workflow_dispatch` concurrency group. Fresh dispatch confirms post-#280 gate scheduling on current master tip.

## Requirements

- R1. Cancel stale verify dispatch 26363187827 if still queued without progress.
- R2. `gh workflow run verify-pypi-regression.yml --ref master` and capture new run ID.
- R3. Confirm new run has **Check trigger** job scheduled (not empty-cancelled).
- R4. Local `discover_tools.py --cli-only` and core import smoke pass.
- R5. Update plan 020 verify row with fresh dispatch URL; mark plan 036 completed.
- R6. Note FC 26363271048 status without cancelling (no retrigger path without non-docs push).

## Implementation Units

- U1. **CI dispatch** — cancel stale + fresh workflow_dispatch.
- U2. **Docs evidence** — plan 020, 036 verification tables.

## Test Scenarios

| ID | Scenario | Expected |
|----|----------|----------|
| T1 | Cancel stale dispatch | run cancelled |
| T2 | Fresh dispatch | gate job queued or running |
| T3 | Local CLI discovery | 3 tools |
| T4 | Local core imports | smoke pass |

## Verification

| Check | Evidence | Result |
|-------|----------|--------|
| Stale 26363187827 | cancelled | ✅ pass |
| Fresh dispatch | [26363420578](https://github.com/OpenKotOR/PyKotor/actions/runs/26363420578) — Check trigger queued | ✅ pass |
| FC 26363271048 | merge job queued (not cancelled; no workflow_dispatch) | ⏳ runner backlog |
| Local discovery | holopatcher, kotordiff, kotormcp | ✅ pass |
| Local core imports | pykotor smoke | ✅ pass |
| Plan 020 row | updated with 26363420578 | ✅ pass |

## Scope Boundaries

- Does not modify workflow YAML.
- Does not cancel Forward Commits 26363271048.
- Full matrix green deferred to runner availability.

## Sources & References

- Master tip: `d54eda7e7` (#284)
- Stale dispatch: https://github.com/OpenKotOR/PyKotor/actions/runs/26363187827
- FC post-#283: https://github.com/OpenKotOR/PyKotor/actions/runs/26363271048
- Plan 035: `docs/plans/2026-05-24-035-ci-queue-closeout-post-283-plan.md`
