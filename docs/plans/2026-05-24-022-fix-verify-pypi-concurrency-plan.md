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
- `cancel-in-progress: false` in `.github/workflows/verify-pypi-regression.yml`. ✅
- PR: https://github.com/OpenKotOR/PyKotor/pull/274 (open, mergeable)
- Post-merge: confirm next Verify PyPI Regression run on master reaches `completed` (not cancelled).

---

## Verification (closeout)

| Check | Evidence | Result |
|-------|----------|--------|
| R1 no cancel | workflow diff | ✅ |
| R2 group retained | `verify-pypi-${{ github.ref }}` unchanged | ✅ |
| R3 matrix unchanged | no job step edits | ✅ |
| Master CI re-test | pending merge of PR #274 | ⏳ |

**Suggested merge stack:** #273 (forward-commits permissions) → #274 (this) → #270 (verify docs).

---

## Sources & References

- Workflow: `.github/workflows/verify-pypi-regression.yml`
- Plan 020: `docs/plans/2026-05-24-020-verify-pypi-regression-post-268-plan.md`
