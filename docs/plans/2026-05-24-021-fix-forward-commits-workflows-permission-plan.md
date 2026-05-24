---
title: "fix: forward-commits workflow push permissions"
type: fix
status: completed
date: 2026-05-24
origin: lfg-forward-commits-residual
strategy_track: test-signal-quality
---

# fix: Forward Commits Workflow Push Permissions

## Summary

`Forward Commits to Bleeding-Edge` cherry-picks master commits onto `bleeding-edge` but push fails when the cherry-pick touches `.github/workflows/*` because the job token only has `contents: write`, not `workflows: write`.

## Problem Frame

Run [26361732290](https://github.com/OpenKotOR/PyKotor/actions/runs/26361732290) failed after cherry-pick #268:

```
refusing to allow a GitHub App to create or update workflow `.github/workflows/verify-pypi-regression.yml` without `workflows` permission
```

Bleeding-edge `.gitmodules` is fixed (`f15e4769d`); checkout succeeds. Push is blocked on workflow file updates.

## Requirements

- R1. Grant `workflows: write` to the forward-commits workflow job token.
- R2. Keep `contents: write` for pushing to `bleeding-edge`.
- R3. No change to cherry-pick logic in this slice.

## Scope Boundaries

- Do not rewrite verify-pypi-regression workflow content.
- Do not change bleeding-edge branch history manually.

## Implementation Units

- U1. **Add workflows permission**

**Files:**
- Modify: `.github/workflows/commit-all-to-bleeding-edge.yml`

**Approach:** Extend top-level `permissions` with `workflows: write`.

**Verification:**
- YAML change: `permissions.workflows: write` added alongside `contents: write`. ✅
- PR: https://github.com/OpenKotOR/PyKotor/pull/273 (open, ready for review)
- Post-merge: re-run Forward Commits after merge; confirm push succeeds when cherry-pick touches `.github/workflows/*`.

---

## Verification (closeout)

| Check | Evidence | Result |
|-------|----------|--------|
| R1 workflows permission | `.github/workflows/commit-all-to-bleeding-edge.yml` diff | ✅ landed on branch |
| R2 contents permission | unchanged `contents: write` | ✅ |
| R3 cherry-pick logic | no script changes | ✅ |
| Forward Commits re-test | run 26362844673 after #273 merge | ❌ invalid `workflows:` permission key — superseded by plan 028 |

---

## Sources & References

- Workflow: `.github/workflows/commit-all-to-bleeding-edge.yml`
- Failed run: https://github.com/OpenKotOR/PyKotor/actions/runs/26361732290
- Plan 020 bleeding-edge: `docs/plans/2026-05-24-020-fix-bleeding-edge-gitmodules-plan.md`
