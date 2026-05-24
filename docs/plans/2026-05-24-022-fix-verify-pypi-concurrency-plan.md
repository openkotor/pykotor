---
title: "fix: verify pypi regression concurrency cancel storm"
type: fix
status: completed
date: 2026-05-24
origin: lfg-pypi-ci-residual
strategy_track: test-signal-quality
---

# fix: Verify PyPI Regression Concurrency Cancel Storm

## Summary

Master **Verify PyPI Regression** runs triggered by `workflow_run` (after Auto-Publish) repeatedly cancel each other because `concurrency.cancel-in-progress: true` groups all runs on the same ref.

## Problem Frame

Post-PR #268 merge, run [26362044155](https://github.com/OpenKotOR/PyKotor/actions/runs/26362044155) and successors were **cancelled** before completion, blocking plan 019/020 CI evidence on master.

## Requirements

- R1. Do not cancel in-progress Verify PyPI Regression runs when a new trigger arrives.
- R2. Preserve concurrency group per ref to avoid unbounded duplicate matrix fan-out on manual re-dispatch (optional: keep group, disable cancel only).
- R3. No change to test matrix or install steps in this slice.

## Implementation Units

- U1. **Disable cancel-in-progress**

**Files:**
- Modify: `.github/workflows/verify-pypi-regression.yml`

**Approach:** Set `cancel-in-progress: false` (matches `publish-pypi-auto.yml` pattern for post-publish verification).

**Verification:**
- Next master trigger completes without concurrency cancellation; plan 020 CI row can record green run URL.

---

## Sources & References

- Workflow: `.github/workflows/verify-pypi-regression.yml`
- Plan 020: `docs/plans/2026-05-24-020-verify-pypi-regression-post-268-plan.md`
