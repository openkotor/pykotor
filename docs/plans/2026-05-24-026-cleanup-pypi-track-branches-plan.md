---
title: "chore: cleanup pypi regression track stale branches"
type: chore
status: completed
date: 2026-05-24
origin: lfg-pypi-track-closeout
strategy_track: test-signal-quality
---

# chore: Cleanup PyPI Regression Track Stale Branches

## Summary

PR #275 merged the concurrency fix from `fix/pypi-verify-regression-concurrency`, but the remote branch accumulated stray doc commits (including mistaken PR #270 conflict resolution). Remove the stale remote branch and record final merge-readiness for open PRs #273 and #270.

## Problem Frame

Merged branches with post-merge pushes confuse agents and duplicate plan edits. Forward Commits failures on feature-branch pushes are expected until #273 lands on `master`.

## Requirements

- R1. Delete remote `fix/pypi-verify-regression-concurrency` (merged via #275; polluted with extra commits).
- R2. Delete local tracking branch if present.
- R3. Record merge order and post-merge verification in this plan.
- R4. Re-run local `discover_tools.py --cli-only` smoke test for plan 019 evidence.

## Implementation Units

- U1. `git push origin --delete fix/pypi-verify-regression-concurrency`
- U2. `git branch -D fix/pypi-verify-regression-concurrency` (local, if exists)
- U3. Update plan 020 track row noting cleanup complete.

## Verification

| Check | Expected |
|-------|----------|
| Remote branch gone | `git ls-remote origin fix/pypi-verify-regression-concurrency` empty |
| PR #273 | MERGEABLE (merge first) |
| PR #270 | MERGEABLE (merge after #273) |
| Local discovery | holopatcher, kotordiff, kotormcp |

## Post-merge checklist (manual)

1. Merge **#273** → next master push should allow Forward Commits to push workflow files.
2. Merge **#270** → docs closeout only.
3. Dispatch one **Verify PyPI Regression** run on `master` after queue is quiet.

## Scope Boundaries

- Does not merge PRs (await reviewer/CI).
- Does not modify workflow YAML on open PR branches.

## Sources & References

- PR #273: https://github.com/OpenKotOR/PyKotor/pull/273
- PR #270: https://github.com/OpenKotOR/PyKotor/pull/270
- PR #275: https://github.com/OpenKotOR/PyKotor/pull/275
